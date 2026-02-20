import unittest
import sys
import os
import time

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from skills.verify_code import run as verify_code

class TestVerifyCodeLive(unittest.TestCase):
    """
    WARNING: This test makes REAL network calls to TiDB Zero API.
    It may fail if the API is down or rate-limited.
    """

    @classmethod
    def setUpClass(cls):
        print("\n[Setup] Provisioning a REAL TiDB Zero database for testing...")
        cls.conn_info, cls.dsn = verify_code.create_temp_db()
        if not cls.dsn:
            raise Exception("Failed to provision database. Cannot run live tests.")
        print(f"[Setup] DB Created: {cls.dsn}")
        # Give it a second to propagate if needed
        time.sleep(1)

    def test_1_simple_select(self):
        print("Test 1: Running SELECT 1...")
        success, result, error = verify_code.run_sql(self.dsn, "SELECT 1 as val")
        self.assertTrue(success, f"SQL failed: {error}")
        self.assertEqual(result[0]['val'], 1)

    def test_2_create_and_insert(self):
        print("Test 2: Creating Table & Inserting...")
        
        # 1. Create Database
        s, r, e = verify_code.run_sql(self.dsn, "CREATE DATABASE IF NOT EXISTS test_db")
        print(f"   > Create DB result: {s}, {e}")
        
        # 2. Append DB to DSN for subsequent calls
        # Current DSN ends with /, so just append test_db
        db_dsn = self.dsn + "test_db"
        print(f"   > Using DSN: {db_dsn}")
        
        # 3. Create Table
        success, res, err = verify_code.run_sql(db_dsn, "CREATE TABLE integration_test (id INT)")
        self.assertTrue(success, f"Create Table failed: {err}")
        
        # 4. Insert
        success, res, err = verify_code.run_sql(db_dsn, "INSERT INTO integration_test VALUES (999)")
        self.assertTrue(success, f"Insert failed: {err}")
        
        # 5. Verify
        s, r, e = verify_code.run_sql(db_dsn, "SELECT * FROM integration_test")
        self.assertTrue(s)
        self.assertEqual(r[0]['id'], 999)

    def test_3_syntax_error(self):
        print("Test 3: Expecting Syntax Error...")
        success, result, error = verify_code.run_sql(self.dsn, "SELEKT * FROM world")
        self.assertFalse(success)
        self.assertIn("You have an error", error)
        print(f"Caught expected error: {error}")

if __name__ == '__main__':
    unittest.main()
