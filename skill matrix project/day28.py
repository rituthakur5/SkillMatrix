
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


def analyze_skills(employee):
    current = {
        skill.strip().lower()
        for skill in employee[2].split(",")
        if skill.strip()
    }

    available = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() in current
    ]

    missing = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() not in current
    ]

    return available, missing


def show_required_skills():
    print("\n===== REQUIRED SKILLS =====")

    for index, skill in enumerate(REQUIRED_SKILLS, start=1):
        print(f"{index}. {skill}")

    print("Total Required Skills:", len(REQUIRED_SKILLS))


def check_skill_gap():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    available, missing = analyze_skills(employee)

    print("\n===== EMPLOYEE SKILL GAP =====")
    print("Employee:", employee[1])
    print("Employee ID:", employee[0])
    print("Skills Already Has:", len(available))
    print("Skills Missing:", len(missing))

    if missing:
        print("\nSkills to Learn:")
        for skill in missing:
            print("-", skill)
    else:
        print("No skill gap found!")


def show_existing_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    available, missing = analyze_skills(employee)

    print("\n===== SKILLS ALREADY AVAILABLE =====")
    print("Employee:", employee[1])

    for skill in available:
        print("-", skill)

    print("Total Matching Skills:", len(available))


def show_missing_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    available, missing = analyze_skills(employee)

    print("\n===== SKILLS TO LEARN =====")
    print("Employee:", employee[1])

    if missing:
        for skill in missing:
            print("-", skill)
    else:
        print("No missing skills!")

    print("Total Missing Skills:", len(missing))


def complete_report():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    available, missing = analyze_skills(employee)

    total = len(REQUIRED_SKILLS)
    percentage = (len(available) / total) * 100

    print("\n===== COMPLETE SKILL GAP REPORT =====")
    print("Employee ID:", employee[0])
    print("Name:", employee[1])
    print("Required Skills:", total)
    print("Skills Available:", len(available))
    print("Skills Missing:", len(missing))
    print("Skill Match Percentage:", round(percentage, 2), "%")

    print("\nSkills Already Has:")
    for skill in available:
        print("-", skill)

    print("\nSkills To Learn:")
    for skill in missing:
        print("-", skill)


def main():
    while True:
        print("\n===== SkillMatrix Day 28 =====")
        print("1. View Required Skills")
        print("2. Check Employee Skill Gap")
        print("3. Show Existing Skills")
        print("4. Show Missing Skills")
        print("5. Complete Skill Gap Report")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_required_skills()
        elif choice == "2":
            check_skill_gap()
        elif choice == "3":
            show_existing_skills()
        elif choice == "4":
            show_missing_skills()
        elif choice == "5":
            complete_report()
        elif choice == "6":
            print("SkillMatrix Day 28 closed.")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
