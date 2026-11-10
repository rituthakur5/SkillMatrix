
import sqlite3

DB_NAME = "skillmatrix.db"


def show_availability():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Check that the required tables exist
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
              AND name IN ('employees', 'projects', 'assignments')
        """)
        tables = {row[0] for row in cursor.fetchall()}

        if not {"employees", "projects", "assignments"}.issubset(tables):
            print("Required tables missing. Run day3.py and day5.py first.")
            return

        cursor.execute("""
            SELECT e.emp_id, e.name, e.skills,
                   COUNT(a.project_id) AS project_count
            FROM employees e
            LEFT JOIN assignments a ON e.emp_id = a.emp_id
            GROUP BY e.emp_id, e.name, e.skills
            ORDER BY e.emp_id
        """)

        employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found. Add employees first.")
        return

    print("\n===== Employee Availability =====")

    for emp_id, name, skills, project_count in employees:
        if project_count == 0:
            status = "BENCH / AVAILABLE"
        else:
            status = f"ASSIGNED ({project_count} project(s))"

        print(f"\nEmployee ID : {emp_id}")
        print(f"Name        : {name}")
        print(f"Skills      : {skills}")
        print(f"Projects    : {project_count}")
        print(f"Status      : {status}")
        print("-" * 35)


def show_bench_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT e.emp_id, e.name, e.skills
            FROM employees e
            WHERE NOT EXISTS (
                SELECT 1
                FROM assignments a
                WHERE a.emp_id = e.emp_id
            )
            ORDER BY e.emp_id
        """)

        employees = cursor.fetchall()

    print("\n===== Bench Employees =====")

    if not employees:
        print("No employees are currently on bench.")
        return

    for emp_id, name, skills in employees:
        print(f"ID: {emp_id} | Name: {name} | Skills: {skills}")


def main():
    while True:
        print("\n===== SkillMatrix: Day 6 =====")
        print("1. View All Employee Availability")
        print("2. View Bench Employees Only")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_availability()
        elif choice == "2":
            show_bench_employees()
        elif choice == "3":
            print("SkillMatrix Day 6 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
