
import sqlite3

DB_NAME = "skillmatrix.db"


def show_dashboard():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM employees")
        total_employees = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM projects")
        total_projects = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM assignments")
        total_assignments = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM employees e
            WHERE NOT EXISTS (
                SELECT 1
                FROM assignments a
                WHERE a.emp_id = e.emp_id
            )
        """)
        bench_employees = cursor.fetchone()[0]

        cursor.execute("""
            SELECT e.name, COUNT(a.project_id)
            FROM employees e
            LEFT JOIN assignments a ON e.emp_id = a.emp_id
            GROUP BY e.emp_id, e.name
            ORDER BY e.name
        """)
        employee_details = cursor.fetchall()

    print("\n" + "=" * 40)
    print("       SKILLMATRIX DASHBOARD")
    print("=" * 40)
    print(f"Total Employees    : {total_employees}")
    print(f"Total Projects     : {total_projects}")
    print(f"Total Assignments  : {total_assignments}")
    print(f"Bench Employees    : {bench_employees}")
    print("-" * 40)

    print("EMPLOYEE PROJECT SUMMARY")
    print("-" * 40)

    if not employee_details:
        print("No employees found.")
    else:
        for name, project_count in employee_details:
            if project_count == 0:
                status = "BENCH"
            else:
                status = f"{project_count} project(s)"

            print(f"{name} - {status}")

    print("=" * 40)


def main():
    while True:
        print("\n===== SkillMatrix Day 7 =====")
        print("1. View Dashboard")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_dashboard()
        elif choice == "2":
            print("SkillMatrix Day 7 closed.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
