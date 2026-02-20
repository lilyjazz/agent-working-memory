import argparse
import sys
import json
import time
import datetime
import decimal
from urllib.parse import urlparse, unquote
import pymysql

# Custom JSON Encoder for Database Types
class DBEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='ignore')
        return super().default(obj)

def parse_dsn(dsn):
    """Parse mysql://user:pass@host:port/db string."""
    parsed = urlparse(dsn)
    if parsed.scheme != 'mysql':
        raise ValueError("DSN scheme must be 'mysql'")
    
    # Handle user:password
    user = parsed.username
    password = unquote(parsed.password) if parsed.password else None
    
    # Handle host:port
    host = parsed.hostname
    port = parsed.port or 4000
    
    # Handle database name (strip leading /)
    db = parsed.path.lstrip('/') or None
    
    return {
        'host': host,
        'port': port,
        'user': user,
        'password': password,
        'database': db
    }

def run_query(dsn, sql):
    start_time = time.time()
    
    try:
        config = parse_dsn(dsn)
        
        # Connect
        # TiDB Cloud requires SSL. passing ssl={} enables it using system CAs.
        conn = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursorclass=pymysql.cursors.Cursor,
            ssl={"check_hostname": False}, # Basic SSL context
            connect_timeout=10,
            charset='utf8mb4'
        )
        
        results = []
        columns = []
        row_count = 0
        
        with conn:
            with conn.cursor() as cursor:
                # Support multi-statement scripts? 
                # pymysql executes one statement by default unless client flags are set.
                # For safety/simplicity MVP, we stick to single statement or let execute() handle it.
                # If sql has multiple statements joined by ';', execute() usually runs the first one or errors.
                # We will treat it as a single execution block.
                
                rows_affected = cursor.execute(sql)
                
                # Fetch results if any
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    row_count = len(rows)
                    results = list(rows)
                else:
                    # For INSERT/UPDATE/DDL
                    row_count = rows_affected
                    results = []
            
            conn.commit() # Auto-commit for DML

        duration = (time.time() - start_time) * 1000
        
        return {
            "status": "success",
            "columns": columns,
            "rows": results,
            "row_count": row_count,
            "duration_ms": round(duration, 2)
        }

    except pymysql.MySQLError as e:
        # e.args is usually (code, message)
        code = e.args[0] if len(e.args) > 0 else 0
        msg = e.args[1] if len(e.args) > 1 else str(e)
        
        return {
            "status": "error",
            "error_code": code,
            "error_message": msg,
            "type": "DatabaseError"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error_message": str(e),
            "type": "SystemError"
        }

def main():
    parser = argparse.ArgumentParser(description='Execute SQL via DSN')
    parser.add_argument('--dsn', required=True, help='Connection string (mysql://...)')
    parser.add_argument('--sql', required=True, help='SQL statement')
    
    args = parser.parse_args()
    
    result = run_query(args.dsn, args.sql)
    
    # Print JSON to stdout
    print(json.dumps(result, cls=DBEncoder, ensure_ascii=False))

if __name__ == "__main__":
    main()
