import unittest
import os
import sys
import json

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
# Use subprocess to run the script because it's a simple print
import subprocess

class TestBlackBox(unittest.TestCase):
    def test_run_output(self):
        script = os.path.join(os.path.dirname(__file__), '../../skills/black_box/run.py')
        cmd = [sys.executable, script]
        res = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        data = json.loads(res.stdout)
        self.assertTrue(data['success'])

if __name__ == '__main__':
    unittest.main()
