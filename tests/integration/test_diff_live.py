import unittest
import os
import pandas as pd
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.data_diff import run as diff

class TestDataDiffLive(unittest.TestCase):
    
    def setUp(self):
        # Create two CSVs
        self.csv_a = "file_a.csv" # Old
        self.csv_b = "file_b.csv" # New
        
        # A: Alice, Bob
        pd.DataFrame({
            "id": [1, 2], "name": ["Alice", "Bob"]
        }).to_csv(self.csv_a, index=False)
        
        # B: Alice, Charlie (Bob removed, Charlie added)
        pd.DataFrame({
            "id": [1, 3], "name": ["Alice", "Charlie"]
        }).to_csv(self.csv_b, index=False)

    def tearDown(self):
        if os.path.exists(self.csv_a): os.remove(self.csv_a)
        if os.path.exists(self.csv_b): os.remove(self.csv_b)

    def test_diff_logic(self):
        print("\n[E2E] Testing Data Diff (A vs B)...")
        res = diff.run_diff(self.csv_a, self.csv_b)
        
        self.assertTrue(res['success'], f"Diff failed: {res.get('error')}")
        d = res['diff']
        
        # Verify Logic
        self.assertEqual(d['added_count'], 1)   # Charlie added
        self.assertEqual(d['removed_count'], 1) # Bob removed
        
        print(f"[E2E] Diff Result: +{d['added_count']} / -{d['removed_count']}")
        self.assertEqual(d['added_rows'][0]['name'], "Charlie")
        self.assertEqual(d['removed_rows'][0]['name'], "Bob")

if __name__ == '__main__':
    unittest.main()
