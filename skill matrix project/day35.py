
import sqlite3

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


def track_progress():
    emp_id = input("Enter Employee ID: ").strip().upper()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    employee_skills = {
        skill.strip().lower()
        for skill in employee[2].split(",")
        if skill.strip()
    }

    completed = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() in employee_skills
    ]

    missing = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() not in employee_skills
    ]

    total = len(REQUIRED_SKILLS)
    completed_count = len(completed)
    missing_count = len(missing)

    percentage = (completed_count / total) * 100 if total else 0

    print("\n===== SKILL GAP PROGRESS REPORT =====")
    print("------------------------------------")
    print("Employee ID   :", employee[0])
    print("Employee Name :", employee[1])
    print("Total Required Skills :", total)
    print("Completed Skills      :", completed_count)
    print("Missing Skills        :", missing_count)
    print("Progress              : {:.2f}%".format(percentage))

    print("\nCompleted Skills:")
    for skill in completed:
        print("-", skill)

    print("\nMissing Skills:")
    if missing:
        for skill in missing:
            print("-", skill)
    else:
        print("No missing skills!")

    print("------------------------------------")


def main():
    while True:
        print("\n===== SkillMatrix Day 35 =====")
        print("1. Track Employee Skill Progress")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            track_progress()

        elif choice == "2":
            print("SkillMatrix Day 35 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
