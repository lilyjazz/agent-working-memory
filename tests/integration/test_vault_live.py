import unittest
import os
import sys
import json

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.knowledge_vault import run as vault

class TestVaultLive(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Ensure API Key is present (Should be in our env)
        if not os.environ.get("GEMINI_API_KEY"):
            raise Exception("Skipping Vault test: GEMINI_API_KEY not found")
        
        # Reset DSN file to force new DB for test cleanliness
        dsn_file = os.path.expanduser("~/.openclaw_knowledge_vault_dsn")
        if os.path.exists(dsn_file):
            os.remove(dsn_file)

    def test_vector_flow(self):
        print("\n[E2E] Testing Knowledge Vault (Vector Search)...")
        
        # 1. Add Knowledge
        print("Adding: 'The secret code is 1234'")
        res = vault.manage_vault("add", content="The secret code is 1234")
        self.assertTrue(res['success'], f"Add failed: {res.get('error')}")
        
        # 2. Add Distractor
        print("Adding: 'The sky is blue'")
        vault.manage_vault("add", content="The sky is blue")
        
        # 3. Search (Semantic)
        print("Searching: 'What is the password?'")
        search_res = vault.manage_vault("search", query="What is the password?")
        
        self.assertTrue(search_res['success'])
        results = search_res['results']
        self.assertTrue(len(results) > 0)
        
        # Top result should be the secret code
        top_match = results[0]['content']
        print(f"Top Result: {top_match} (Distance: {results[0]['distance']})")
        self.assertIn("1234", top_match)

if __name__ == '__main__':
    unittest.main()
