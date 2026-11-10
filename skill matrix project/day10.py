
import sqlite3
import csv

DB_NAME = "skillmatrix.db"


def export_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT emp_id, name, skills
            FROM employees
            ORDER BY emp_id
        """)
        employees = cursor.fetchall()

    with open("employees_report.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["Employee ID", "Name", "Skills"])
        writer.writerows(employees)

    print("Employee report exported: employees_report.csv")


def export_projects():
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
        projects = cursor.fetchall()

    with open("projects_report.csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Project ID",
            "Project Name",
            "Employee ID",
            "Employee Name"
        ])
        writer.writerows(projects)

    print("Project report exported: projects_report.csv")


def main():
    while True:
        print("\n===== SkillMatrix Day 10 =====")
        print("1. Export Employee Report")
        print("2. Export Project Report")
        print("3. Export Both Reports")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            export_employees()
        elif choice == "2":
            export_projects()
        elif choice == "3":
            export_employees()
            export_projects()
        elif choice == "4":
            print("SkillMatrix Day 10 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
