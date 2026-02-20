import argparse
import json
import subprocess
import sys
import os
import base64
import tarfile
import io

try:
    import pymysql
except ImportError:
    print(json.dumps({"success": False, "error": "Missing dependency: pymysql"}))
    sys.exit(1)

# --- Provisioner (Standard) ---
def create_temp_db():
    api_url = "https://zero.tidbapi.com/v1alpha1/instances"
    try:
        cmd = ["curl", "-sS", "-X", "POST", api_url, "-H", "content-type: application/json", "-d", "{}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        data = json.loads(result.stdout)
        return data.get("instance", {}).get("connectionString")
    except: return None

def parse_dsn(dsn):
    prefix = "mysql://"
    auth_part, rest = dsn[len(prefix):].split("@")
    user, password = auth_part.split(":")
    host_port, db = rest.split("/")
    host, port = host_port.split(":")
    return host, int(port), user, password, (db or "test")

# --- Logic ---
def pack_workspace():
    """Compress workspace to in-memory tar.gz"""
    # For safety, only pack specific config files, not everything
    files_to_pack = ["AGENTS.md", "TOOLS.md", "MEMORY.md", "SOUL.md", "USER.md"]
    
    bio = io.BytesIO()
    with tarfile.open(fileobj=bio, mode="w:gz") as tar:
        for f in files_to_pack:
            if os.path.exists(f):
                tar.add(f)
    return bio.getvalue()

def teleport_out():
    dsn = create_temp_db()
    if not dsn: return {"success": False, "error": "Provision failed"}
    
    blob = pack_workspace()
    # Chunking? For MVP, we assume blob fits in MEDIUMBLOB (16MB). 
    # TiDB Serverless limit is generous.
    
    host, port, user, password, db = parse_dsn(dsn)
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, ssl={"check_hostname": False})
    
    with conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE teleport (id INT, data MEDIUMBLOB)")
            cur.execute("INSERT INTO teleport VALUES (1, %s)", (blob,))
        conn.commit()
    
    restore_cmd = f"python skills/agent_teleport/run.py --action restore --dsn '{dsn}'"
    return {
        "success": True, 
        "message": "Agent packed and uploaded to TiDB Zero.",
        "restore_command": restore_cmd,
        "expires_in": "30 days"
    }

def teleport_in(dsn):
    try:
        host, port, user, password, db = parse_dsn(dsn)
        conn = pymysql.connect(host=host, port=port, user=user, password=password, database=db, ssl={"check_hostname": False})
        
        blob = None
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT data FROM teleport WHERE id=1")
                blob = cur.fetchone()[0]
        
        if not blob: return {"success": False, "error": "No data found in teleport DB"}
        
        # Extract
        bio = io.BytesIO(blob)
        with tarfile.open(fileobj=bio, mode="r:gz") as tar:
            tar.extractall(path=".") # Current dir
            
        return {"success": True, "message": "Agent restored successfully!"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["pack", "restore"], required=True)
    parser.add_argument("--dsn", help="DSN for restore")
    args = parser.parse_args()
    
    if args.action == "pack":
        print(json.dumps(teleport_out()))
    else:
        print(json.dumps(teleport_in(args.dsn)))
