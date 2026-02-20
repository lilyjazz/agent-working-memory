import argparse
import json
import subprocess
import sys
import os
import re
import datetime

try:
    import pymysql
    import pandas as pd
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: pymysql or pandas"}))
    sys.exit(1)

# --- 1. Helper: Type Mapping ---
def map_dtype_to_sql(dtype):
    """Maps Pandas dtype to MySQL column type."""
    if pd.api.types.is_integer_dtype(dtype):
        return "BIGINT"
    elif pd.api.types.is_float_dtype(dtype):
        return "DOUBLE"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DATETIME"
    elif pd.api.types.is_bool_dtype(dtype):
        return "BOOLEAN"
    else:
        return "TEXT" # Safe fallback for string/mixed

def clean_col_name(name):
    """Makes string a valid SQL identifier."""
    # Replace non-alphanumeric with _
    clean = re.sub(r'[^a-zA-Z0-9]', '_', str(name)).lower()
    # Remove leading/trailing _
    clean = clean.strip('_')
    # Ensure not empty
    return clean if clean else "col"

# --- 2. Provisioner (Embedded from verify-code) ---
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

# --- 3. Main Logic ---
def process_file(filepath):
    # 1. Load File
    try:
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        elif filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            df = pd.read_json(filepath)
        else:
            return {"success": False, "error": "Unsupported file format"}
    except Exception as e:
        return {"success": False, "error": f"Failed to read file: {e}"}

    # 2. Clean Data
    df.columns = [clean_col_name(c) for c in df.columns]
    
    # 3. Generate Schema
    table_name = os.path.splitext(os.path.basename(filepath))[0]
    table_name = clean_col_name(table_name)
    
    schema_cols = []
    for col in df.columns:
        sql_type = map_dtype_to_sql(df[col].dtype)
        schema_cols.append(f"`{col}` {sql_type}")
    
    create_sql = f"CREATE TABLE `{table_name}` ({', '.join(schema_cols)});"

    # 4. Provision DB
    dsn = create_temp_db()
    if not dsn:
        return {"success": False, "error": "Failed to provision TiDB Zero"}

    # 5. Load to DB
    try:
        host, port, user, password, db = parse_dsn(dsn)
        conn = pymysql.connect(
            host=host, port=port, user=user, password=password, database=db,
            ssl={"check_hostname": False}, charset='utf8mb4'
        )
        
        with conn:
            with conn.cursor() as cursor:
                # Create Table
                cursor.execute(create_sql)
                
                # Insert Data (Batch)
                # Convert DF to list of tuples, handle NaN as None
                data = df.where(pd.notnull(df), None).values.tolist()
                
                placeholders = ", ".join(["%s"] * len(df.columns))
                insert_sql = f"INSERT INTO `{table_name}` VALUES ({placeholders})"
                
                # Batch insert (chunk size 1000)
                batch_size = 1000
                for i in range(0, len(data), batch_size):
                    cursor.executemany(insert_sql, data[i:i+batch_size])
            
            conn.commit()
            
        return {
            "success": True,
            "infrastructure": "Powered by TiDB Cloud Zero",
            "db_info": {
                "dsn": dsn,
                "table": table_name,
                "row_count": len(df),
                "columns": list(df.columns)
            },
            "next_steps": f"You can now run SQL queries on this table using the DSN."
        }

    except Exception as e:
        return {"success": False, "error": f"Database error: {e}"}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to data file")
    args = parser.parse_args()
    
    print(json.dumps(process_file(args.file), default=str))
