import argparse
import json
import subprocess
import sys
import os
import re

try:
    import pymysql
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: pymysql"}))
    sys.exit(1)

# --- Provisioner ---
def create_temp_db():
    api_url = "https://zero.tidbapi.com/v1alpha1/instances"
    try:
        cmd = ["curl", "-sS", "-X", "POST", api_url, "-H", "content-type: application/json", "-d", "{}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        dsn = data.get("instance", {}).get("connectionString")
        if not dsn: raise Exception("No DSN")
        return dsn
    except Exception as e:
        return None

def parse_dsn(dsn):
    prefix = "mysql://"
    auth_part, rest = dsn[len(prefix):].split("@")
    user, password = auth_part.split(":")
    host_port, db = rest.split("/")
    host, port = host_port.split(":")
    return host, int(port), user, password, (db or "test")

# --- Loader ---
def load_sql_file(conn, filepath):
    with open(filepath, 'r') as f:
        sql_content = f.read()
    
    # Split by semicolon, but ignore semicolons inside quotes (Simple regex for MVP)
    # For robust splitting, we'd need a parser. For this MVP dataset, simple split works.
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    count = 0
    with conn.cursor() as cursor:
        for stmt in statements:
            try:
                cursor.execute(stmt)
                count += 1
            except Exception as e:
                print(f"Warning: Failed to execute statement: {stmt[:50]}... Error: {e}", file=sys.stderr)
    return count

# --- Main Logic ---
def setup_dojo(dataset):
    # 1. Resolve Dataset Path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_path = os.path.join(base_dir, "datasets", f"{dataset}.sql")
    
    if not os.path.exists(sql_path):
        return {"success": False, "error": f"Dataset '{dataset}' not found."}

    # 2. Provision
    dsn = create_temp_db()
    if not dsn:
        return {"success": False, "error": "Failed to provision TiDB Zero"}

    # 3. Load Data
    try:
        host, port, user, password, db = parse_dsn(dsn)
        conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=db,
            ssl={"check_hostname": False}, charset='utf8mb4',
            autocommit=True
        )
        
        with conn:
            stmt_count = load_sql_file(conn, sql_path)
            
        return {
            "success": True,
            "infrastructure": "Powered by TiDB Cloud Zero",
            "db_info": {
                "dsn": dsn,
                "dataset": dataset,
                "tables": ["actor", "film", "film_actor"] # Hardcoded for MVP, dynamic later
            },
            "message": f"Dojo ready! Loaded {stmt_count} SQL statements. You can now practice queries."
        }

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", default="mini_sakila", help="Dataset name")
    args = parser.parse_args()
    
    print(json.dumps(setup_dojo(args.dataset), default=str))
