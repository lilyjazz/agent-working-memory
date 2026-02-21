import unittest
import os
import sys
import json

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.hive_mind import run as hive

class TestHiveMindLive(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("\n[E2E] Provisioning Hive Mind DB...")
        cls.dsn = hive.create_temp_db()
        if not cls.dsn:
            raise Exception("Failed to provision DB for Hive Mind")
        print(f"[E2E] DB Ready: {cls.dsn}")

    def test_lifecycle(self):
        # 1. Set
        print("Test: Set Preference")
        res = hive.manage_prefs(self.dsn, "set", "theme", "dark")
        self.assertTrue(res['success'], f"Set failed: {res.get('error')}")
        
        # 2. Get
        print("Test: Get Preference")
        res = hive.manage_prefs(self.dsn, "get", "theme")
        self.assertEqual(res['value'], "dark")
        
        # 3. Update
        hive.manage_prefs(self.dsn, "set", "theme", "light")
        res = hive.manage_prefs(self.dsn, "get", "theme")
        self.assertEqual(res['value'], "light")
        
        # 4. List
        print("Test: List Preferences")
        res = hive.manage_prefs(self.dsn, "list")
        self.assertTrue(res['success'], f"List failed: {res.get('error')}")
        self.assertIn("theme", res['prefs'])

if __name__ == '__main__':
    unittest.main()
