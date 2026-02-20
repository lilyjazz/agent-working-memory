import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add project root to sys.path to allow importing skills
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from skills.verify_code import run as verify_code

class TestVerifyCodeSkill(unittest.TestCase):

    @patch('skills.verify_code.run.subprocess.run')
    def test_create_temp_db_success(self, mock_subprocess):
        # Mock successful curl response
        mock_response = MagicMock()
        mock_response.returncode = 0
        mock_response.stdout = json.dumps({
            "instance": {
                "connection": {"host": "test-host", "port": 4000},
                "connectionString": "mysql://user:pass@test-host:4000/db"
            }
        })
        # Fix: Use return_value
        mock_subprocess.return_value = mock_response

        info, dsn = verify_code.create_temp_db()
        self.assertEqual(dsn, "mysql://user:pass@test-host:4000/db")
        self.assertEqual(info['host'], "test-host")

    @patch('skills.verify_code.run.pymysql.connect')
    def test_run_sql_success(self, mock_connect):
        # Mock DB Connection and Cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.__enter__.return_value = mock_cursor
        
        # Mock SQL execution result
        mock_cursor.description = [('id',), ('name',)]
        mock_cursor.fetchall.return_value = [(1, 'Alice')]
        
        success, result, error = verify_code.run_sql("mysql://u:p@h:4000/db", "SELECT * FROM users")
        
        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(result, [{'id': 1, 'name': 'Alice'}])

    @patch('skills.verify_code.run.pymysql.connect')
    def test_run_sql_syntax_error(self, mock_connect):
        # Mock Exception
        mock_connect.side_effect = verify_code.pymysql.MySQLError(1064, "You have an error in your SQL syntax")
        
        success, result, error = verify_code.run_sql("mysql://u:p@h:4000/db", "SELEKT *")
        
        self.assertFalse(success)
        self.assertIn("1064", error)

if __name__ == '__main__':
    unittest.main()
