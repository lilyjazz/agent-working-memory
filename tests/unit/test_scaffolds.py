import unittest
import os
import subprocess
import json
import sys

# List of skills that are currently placeholders
SCAFFOLD_SKILLS = [
    "black_box", "mind_clone", "checkpoint", "private_analyst",
    "trend_watcher", "team_board", "instant_api", "time_machine"
]

class TestScaffolds(unittest.TestCase):
    def test_all_scaffolds(self):
        print("\n[Contract] Verifying 8 Scaffolded Skills...")
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../skills'))
        
        for skill in SCAFFOLD_SKILLS:
            script = os.path.join(base_dir, skill, "run.py")
            print(f"  - Checking {skill}...", end=" ")
            
            # Run script
            cmd = [sys.executable, script]
            # Some might require dummy args? Scaffold scripts usually assume none or basic
            # Let's try running without args first (they are placeholders)
            
            try:
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
                
                if res.returncode != 0:
                    # If it asks for args, that's fine, but it should output JSON error or help
                    # For our scaffolds, they just print success.
                    print(f"❌ Failed (Exit {res.returncode})")
                    print(res.stderr)
                    self.fail(f"{skill} crashed")
                
                # Check JSON
                try:
                    data = json.loads(res.stdout)
                    if data.get('success'):
                        print("✅ JSON OK")
                    else:
                        print(f"⚠️ JSON Fail: {data}")
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {res.stdout.strip()}")
                    self.fail(f"{skill} did not output JSON")
                    
            except Exception as e:
                print(f"❌ Exec Error: {e}")
                self.fail(f"{skill} execution failed")

if __name__ == '__main__':
    unittest.main()
