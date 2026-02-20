import unittest
import os
import sys
import shutil

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from skills.agent_teleport import run as teleport

class TestTeleportLive(unittest.TestCase):
    
    def setUp(self):
        # Create dummy AGENTS.md
        with open("AGENTS.md", "w") as f:
            f.write("Secret Agent Data")
            
    def tearDown(self):
        if os.path.exists("AGENTS.md"):
            os.remove("AGENTS.md")

    def test_pack_restore(self):
        print("\n[E2E] Testing Agent Teleport...")
        
        # 1. Pack
        pack_res = teleport.teleport_out()
        self.assertTrue(pack_res['success'], f"Pack failed: {pack_res.get('error')}")
        dsn = pack_res['restore_command'].split("'")[1] # Extract DSN from cmd string
        print(f"[E2E] Packed to: {dsn}")
        
        # Delete local file to simulate new machine
        os.remove("AGENTS.md")
        
        # 2. Restore
        restore_res = teleport.teleport_in(dsn)
        self.assertTrue(restore_res['success'], f"Restore failed: {restore_res.get('error')}")
        
        # 3. Verify
        self.assertTrue(os.path.exists("AGENTS.md"))
        with open("AGENTS.md", "r") as f:
            content = f.read()
        self.assertEqual(content, "Secret Agent Data")
        print("[E2E] File restored successfully!")

if __name__ == '__main__':
    unittest.main()
