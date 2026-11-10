
import sqlite3
import csv
import os

DB_NAME = "skillmatrix.db"

REQUIRED_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Excel",
    "Machine Learning",
    "Data Analysis",
    "Web Development",
    "Communication",
    "Problem Solving"
]


def get_employee(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()
    return employee


def generate_employee_report():
    emp_id = input("Enter Employee ID: ").strip().upper()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    skills = {
        skill.strip().lower()
        for skill in employee[2].split(",")
        if skill.strip()
    }

    completed = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() in skills
    ]

    missing = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() not in skills
    ]

    total = len(REQUIRED_SKILLS)
    completed_count = len(completed)
    percentage = completed_count / total * 100 if total else 0

    goals = []
    if os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='learning_goals'
        """)

        if cursor.fetchone():
            cursor.execute("""
                SELECT goal, status
                FROM learning_goals
                WHERE emp_id = ?
            """, (emp_id,))
            goals = cursor.fetchall()

        conn.close()

    filename = f"{emp_id}_report.csv"

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["SKILLMATRIX EMPLOYEE REPORT"])
        writer.writerow(["Employee ID", employee[0]])
        writer.writerow(["Employee Name", employee[1]])
        writer.writerow(["Total Required Skills", total])
        writer.writerow(["Completed Skills", completed_count])
        writer.writerow(["Missing Skills", len(missing)])
        writer.writerow(["Progress Percentage", f"{percentage:.2f}%"])

        writer.writerow([])
        writer.writerow(["Completed Skills"])
        for skill in completed:
            writer.writerow([skill])

        writer.writerow([])
        writer.writerow(["Missing Skills"])
        for skill in missing:
            writer.writerow([skill])

        writer.writerow([])
        writer.writerow(["Learning Goals", "Status"])
        for goal, status in goals:
            writer.writerow([goal, status])

    print("\n===== EMPLOYEE REPORT GENERATED =====")
    print("Employee ID:", employee[0])
    print("Employee Name:", employee[1])
    print("Completed Skills:", completed_count)
    print("Missing Skills:", len(missing))
    print("Progress: {:.2f}%".format(percentage))
    print("Learning Goals:", len(goals))
    print("Report saved as:", filename)


def view_all_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name FROM employees")
    employees = cursor.fetchall()
    conn.close()

    print("\n===== EMPLOYEE LIST =====")

    if not employees:
        print("No employees found!")
        return

    for emp_id, name in employees:
        print(emp_id, "|", name)


def main():
    while True:
        print("\n===== SkillMatrix Day 37 =====")
        print("1. Generate Employee Report")
        print("2. View All Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_employee_report()

        elif choice == "2":
            view_all_employees()

        elif choice == "3":
            print("SkillMatrix Day 37 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
