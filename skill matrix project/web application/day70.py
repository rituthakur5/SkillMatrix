
import unittest
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "skillmatrix.db")


class SkillMatrixTests(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def test_database_connection(self):
        self.assertIsNotNone(self.connection)

    def test_employees_table(self):
        self.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='employees'
        """)
        self.assertIsNotNone(self.cursor.fetchone())

    def test_learning_goals_table(self):
        self.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='learning_goals'
        """)
        self.assertIsNotNone(self.cursor.fetchone())

    def test_employee_records(self):
        self.cursor.execute("SELECT COUNT(*) FROM employees")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 0)

    def test_learning_goals_records(self):
        self.cursor.execute("SELECT COUNT(*) FROM learning_goals")
        count = self.cursor.fetchone()[0]
        self.assertGreaterEqual(count, 0)

    def tearDown(self):
        self.connection.close()


if __name__ == "__main__":
    print("\n===== SkillMatrix Day 70 =====")
    print("Final Testing Started\n")

    unittest.main(verbosity=2)
