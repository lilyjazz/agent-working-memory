import argparse
import json
import subprocess
import time
import sys
import os
try:
    import pymysql
except ImportError:
    print(json.dumps({"verified": False, "error": "Missing dependency: pymysql"}))
    sys.exit(1)

# --- 1. Provisioner (TiDB Zero) ---
def create_temp_db():
    """Provisions a database via TiDB Zero API using curl."""
    api_url = "https://zero.tidbapi.com/v1alpha1/instances"
    try:
        # Use curl for simplicity and zero-dep (besides system curl)
        cmd = [
            "curl", "-sS", "-X", "POST", api_url,
            "-H", "content-type: application/json",
            "-d", "{}"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            raise Exception(f"Curl failed: {result.stderr}")
        
        data = json.loads(result.stdout)
        conn_info = data.get("instance", {}).get("connection", {})
        dsn = data.get("instance", {}).get("connectionString")
        
        if not dsn:
            raise Exception("No connection string in response")
            
        return conn_info, dsn
    except Exception as e:
        return None, str(e)

# --- 2. Executor (PyMySQL) ---
def run_sql(dsn, sql):
    """Parses DSN and runs SQL."""
    try:
        # Parse DSN manually to avoid extra libs
        # Format: mysql://user:pass@host:port/db
        prefix = "mysql://"
        if not dsn.startswith(prefix):
            raise ValueError("Invalid DSN format")
        
        auth_part, rest = dsn[len(prefix):].split("@")
        user, password = auth_part.split(":")
        host_port, db = rest.split("/")
        host, port = host_port.split(":")
        
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database="", # Connect without DB first? Zero gives access to created DB usually.
            ssl={"check_hostname": False},
            connect_timeout=10,
            charset='utf8mb4'
        )
        
        results = []
        with conn:
            with conn.cursor() as cursor:
                # TiDB Zero usually gives you a DB, or you need to CREATE DATABASE.
                # Let's try running the SQL directly.
                # If SQL is DDL/DML, execute it.
                cursor.execute(sql)
                if cursor.description:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]
                else:
                    results = {"affected_rows": cursor.rowcount}
            conn.commit()
            
        return True, results, None

    except pymysql.MySQLError as e:
        return False, None, f"MySQL Error {e.args[0]}: {e.args[1]}"
    except Exception as e:
        return False, None, f"System Error: {str(e)}"

# --- Main Flow ---
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql", required=True, help="SQL to verify")
    args = parser.parse_args()
    
    # 1. Provision
    conn_info, dsn_or_err = create_temp_db()
    if not conn_info:
        print(json.dumps({
            "verified": False,
            "error": f"Failed to provision database: {dsn_or_err}",
            "infrastructure": "TiDB Cloud Zero (Provision Failed)"
        }))
        return

    # 2. Execute
    success, result, error = run_sql(dsn_or_err, args.sql)
    
    # 3. Output
    output = {
        "verified": success,
        "infrastructure": "Powered by TiDB Cloud Zero"
    }
    
    if success:
        output["result"] = result
    else:
        output["error"] = error
        # Simple heuristic suggestion
        if "syntax" in str(error).lower():
            output["fix_suggestion"] = "Check SQL syntax correctness."
        elif "no database selected" in str(error).lower():
            output["fix_suggestion"] = "Try adding 'USE test;' or 'CREATE DATABASE x;' first."

    print(json.dumps(output, default=str))

if __name__ == "__main__":
    main()
