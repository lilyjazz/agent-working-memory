import unittest
import os
import pandas as pd
import sys
import json

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.data_refinery import run as refinery

class TestRefineryLive(unittest.TestCase):
    
    def setUp(self):
        # Create a dummy CSV
        self.csv_path = "test_leads.csv"
        df = pd.DataFrame({
            "User ID": [1, 2, 3],
            "User Name": ["Alice", "Bob", "Charlie"],
            "Score": [99.5, 88.0, 70.2]
        })
        df.to_csv(self.csv_path, index=False)

    def tearDown(self):
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

    def test_end_to_end_ingest(self):
        print("\n[E2E] Running Data Refinery on test_leads.csv...")
        
        # 1. Run Skill
        result = refinery.process_file(self.csv_path)
        
        # 2. Verify Output Structure
        self.assertTrue(result['success'], f"Skill failed: {result.get('error')}")
        self.assertIn("dsn", result['db_info'])
        self.assertEqual(result['db_info']['table'], "test_leads")
        self.assertEqual(result['db_info']['row_count'], 3)
        
        print(f"[E2E] Ingested 3 rows to {result['db_info']['dsn']}")
        
        # 3. Verify Data in DB (Connect and Query back)
        host, port, user, password, db = refinery.parse_dsn(result['db_info']['dsn'])
        conn = refinery.pymysql.connect(
            host=host, port=port, user=user, password=password, database=db,
            ssl={"check_hostname": False}
        )
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM test_leads")
            rows = cur.fetchall()
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0][1], "Alice") # 0=id, 1=name, 2=score
        
        print("[E2E] Verification Query Passed!")

if __name__ == '__main__':
    unittest.main()
