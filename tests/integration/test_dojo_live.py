import unittest
import os
import sys
import json

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.sql_dojo import run as dojo

class TestDojoLive(unittest.TestCase):
    
    def test_dojo_setup(self):
        print("\n[E2E] Setting up SQL Dojo (Mini Sakila)...")
        
        # 1. Run Skill
        result = dojo.setup_dojo("mini_sakila")
        
        self.assertTrue(result['success'], f"Skill failed: {result.get('error')}")
        dsn = result['db_info']['dsn']
        print(f"[E2E] Dojo Ready at {dsn}")
        
        # 2. Verify Data
        host, port, user, password, db = dojo.parse_dsn(dsn)
        conn = dojo.pymysql.connect(
            host=host, port=port, user=user, password=password, database=db,
            ssl={"check_hostname": False}
        )
        with conn.cursor() as cur:
            # Check Actor table
            cur.execute("SELECT count(*) as cnt FROM actor")
            cnt = cur.fetchone()[0]
            self.assertEqual(cnt, 3)
            
            # Check Join
            cur.execute("SELECT title FROM film f JOIN film_actor fa ON f.film_id = fa.film_id WHERE fa.actor_id=1")
            rows = cur.fetchall()
            self.assertTrue(len(rows) >= 1)
        
        print("[E2E] Dojo Data Verified!")

if __name__ == '__main__':
    unittest.main()
