
import sqlite3

DB_NAME = "skillmatrix.db"


def employee_report():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                e.emp_id,
                e.name,
                e.skills,
                p.project_name
            FROM employees e
            LEFT JOIN assignments a ON e.emp_id = a.emp_id
            LEFT JOIN projects p ON a.project_id = p.project_id
            ORDER BY e.emp_id, p.project_name
        """)

        rows = cursor.fetchall()

    print("\n========== EMPLOYEE REPORT ==========")

    if not rows:
        print("No employees found.")
        return

    current_id = None

    for emp_id, name, skills, project_name in rows:
        if emp_id != current_id:
            current_id = emp_id
            print("\n-------------------------------------")
            print(f"Employee ID : {emp_id}")
            print(f"Name        : {name}")
            print(f"Skills      : {skills}")
            print("Projects    :")

        if project_name:
            print(f"  - {project_name}")
        else:
            print("  - No project assigned")

    print("-------------------------------------")


def project_report():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                p.project_id,
                p.project_name,
                e.emp_id,
                e.name
            FROM projects p
            LEFT JOIN assignments a ON p.project_id = a.project_id
            LEFT JOIN employees e ON a.emp_id = e.emp_id
            ORDER BY p.project_id, e.name
        """)

        rows = cursor.fetchall()

    print("\n========== PROJECT REPORT ==========")

    if not rows:
        print("No projects found.")
        return

    current_project = None

    for project_id, project_name, emp_id, name in rows:
        if project_id != current_project:
            current_project = project_id
            print("\n-------------------------------------")
            print(f"Project ID   : {project_id}")
            print(f"Project Name : {project_name}")
            print("Employees    :")

        if emp_id:
            print(f"  - {name} (ID: {emp_id})")
        else:
            print("  - No employees assigned")

    print("-------------------------------------")


def main():
    while True:
        print("\n===== SkillMatrix Day 9 =====")
        print("1. Employee Report")
        print("2. Project Report")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            employee_report()
        elif choice == "2":
            project_report()
        elif choice == "3":
            print("SkillMatrix Day 9 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
