import argparse
import json
import subprocess
import sys
import os
try:
    import pymysql
    import pandas as pd
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: pymysql or pandas"}))
    sys.exit(1)

# --- Provisioner (Standard) ---
def create_temp_db():
    # Simple retry logic for provisioning
    for i in range(3):
        try:
            cmd = ["curl", "-sS", "-X", "POST", "https://zero.tidbapi.com/v1alpha1/instances", "-H", "content-type: application/json", "-d", "{}"]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if res.returncode == 0:
                data = json.loads(res.stdout)
                dsn = data.get("instance", {}).get("connectionString")
                if dsn: return dsn
        except:
            time.sleep(2)
    return None

def parse_dsn(dsn):
    prefix = "mysql://"
    auth_part, rest = dsn[len(prefix):].split("@")
    user, password = auth_part.split(":")
    host_port, db = rest.split("/")
    host, port = host_port.split(":")
    return host, int(port), user, password, (db or "test")

# --- Logic ---
def load_df(conn, df, table_name):
    # Create Table
    cols = []
    for c in df.columns:
        cols.append(f"`{c}` TEXT") # Use TEXT for diff simplicity
    create_sql = f"CREATE TABLE `{table_name}` ({', '.join(cols)});"
    
    with conn.cursor() as cursor:
        cursor.execute(create_sql)
        data = df.where(pd.notnull(df), None).values.tolist()
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
        for i in range(0, len(data), 1000):
            cursor.executemany(sql, data[i:i+1000])
    conn.commit()

def run_diff(file_a, file_b):
    dsn = create_temp_db()
    if not dsn: return {"success": False, "error": "Provision failed"}
    
    try:
        print(f"DEBUG: Reading {file_a}...")
        df_a = pd.read_csv(file_a) if file_a.endswith('.csv') else pd.read_excel(file_a)
        print(f"DEBUG: df_a type: {type(df_a)}")
        
        print(f"DEBUG: Reading {file_b}...")
        df_b = pd.read_csv(file_b) if file_b.endswith('.csv') else pd.read_excel(file_b)
        print(f"DEBUG: df_b type: {type(df_b)}")
        
        # Ensure schemas match for simple diff
        common_cols = list(set(df_a.columns) & set(df_b.columns))
        df_a = df_a[common_cols]
        df_b = df_b[common_cols]
        
        host, port, user, password, db = parse_dsn(dsn)
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, ssl={"check_hostname": False})
        
        with conn:
            load_df(conn, df_a, "table_a")
            load_df(conn, df_b, "table_b")
            
            # Diff Logic: A EXCEPT B (Removed), B EXCEPT A (Added)
            # MySQL/TiDB doesn't support EXCEPT. Use LEFT JOIN / NULL check.
            
            col_list = ", ".join([f"`{c}`" for c in common_cols])
            join_cond = " AND ".join([f"a.`{c}` <=> b.`{c}`" for c in common_cols])
            
            # Removed Rows (In A but not B)
            sql_removed = f"SELECT {col_list} FROM table_a a LEFT JOIN table_b b ON {join_cond} WHERE b.`{common_cols[0]}` IS NULL"
            
            # Added Rows (In B but not A)
            sql_added = f"SELECT {col_list} FROM table_b b LEFT JOIN table_a a ON {join_cond} WHERE a.`{common_cols[0]}` IS NULL"
            
            removed = []
            with conn.cursor() as cur:
                cur.execute(sql_removed)
                removed = [dict(zip(common_cols, row)) for row in cur.fetchall()]
                
            added = []
            with conn.cursor() as cur:
                cur.execute(sql_added)
                added = [dict(zip(common_cols, row)) for row in cur.fetchall()]
                
        return {
            "success": True,
            "diff": {
                "added_count": len(added),
                "removed_count": len(removed),
                "added_rows": added[:5], # Preview
                "removed_rows": removed[:5]
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_a", required=True)
    parser.add_argument("--file_b", required=True)
    args = parser.parse_args()
    print(json.dumps(run_diff(args.file_a, args.file_b), default=str))
