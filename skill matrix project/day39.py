
import sqlite3
import os
import csv

DB_NAME = "skillmatrix.db"


def check_database():
    print("\n===== DATABASE CHECK =====")

    if not os.path.exists(DB_NAME):
        print("FAIL: Database file not found!")
        return False

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
        """)

        tables = [row[0] for row in cursor.fetchall()]

        if "employees" in tables:
            print("PASS: Employees table exists.")
        else:
            print("FAIL: Employees table missing!")
            conn.close()
            return False

        if "learning_goals" in tables:
            print("PASS: Learning goals table exists.")
        else:
            print("INFO: Learning goals table not created yet.")

        conn.close()
        return True

    except sqlite3.Error as error:
        print("FAIL:", error)
        return False


def check_employees():
    print("\n===== EMPLOYEE CHECK =====")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT emp_id, name, skills FROM employees")
        employees = cursor.fetchall()

        if not employees:
            print("FAIL: No employees found!")
        else:
            print("PASS: Employee records found.")
            for emp in employees:
                print(emp[0], "|", emp[1], "|", emp[2])

        conn.close()
        return len(employees) > 0

    except sqlite3.Error as error:
        print("FAIL:", error)
        return False


def check_learning_goals():
    print("\n===== LEARNING GOALS CHECK =====")

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='learning_goals'
        """)

        if not cursor.fetchone():
            print("INFO: Learning goals table not found.")
            conn.close()
            return True

        cursor.execute("""
            SELECT goal_id, emp_id, goal, status
            FROM learning_goals
        """)

        goals = cursor.fetchall()

        print("PASS: Learning goals table is accessible.")
        print("Total Learning Goals:", len(goals))

        for goal in goals:
            print(goal)

        conn.close()
        return True

    except sqlite3.Error as error:
        print("FAIL:", error)
        return False


def check_report_file():
    print("\n===== REPORT FILE CHECK =====")

    filename = "E101_report.csv"

    if not os.path.exists(filename):
        print("INFO: E101_report.csv not found. Generate it using Day 37.")
        return True

    try:
        with open(filename, "r", newline="", encoding="utf-8") as file:
            rows = list(csv.reader(file))

        if rows:
            print("PASS: Report file exists and contains data.")
            print("Total rows:", len(rows))
            return True

        print("FAIL: Report file is empty.")
        return False

    except (OSError, csv.Error) as error:
        print("FAIL:", error)
        return False


def main():
    print("\n===================================")
    print("   SkillMatrix Day 39")
    print("   FINAL PROJECT TESTING")
    print("===================================")

    results = []

    results.append(check_database())
    results.append(check_employees())
    results.append(check_learning_goals())
    results.append(check_report_file())

    passed = sum(results)
    total = len(results)

    print("\n========== FINAL TEST SUMMARY ==========")
    print("Tests Passed:", passed)
    print("Tests Requiring Attention:", total - passed)

    if passed == total:
        print("All available checks passed!")
    else:
        print("Some checks need attention. Review messages above.")

    print("========================================")


if __name__ == "__main__":
    main()
