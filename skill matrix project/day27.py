
import sqlite3

DB_NAME = "skillmatrix.db"

# Skills that can be recommended
RECOMMENDED_SKILLS = [
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


def view_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    emp_id, name, skills = employee

    print("\n===== EMPLOYEE SKILLS =====")
    print("Employee ID:", emp_id)
    print("Name:", name)
    print("Skills:", skills)


def recommend_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    current_skills = [
        s.strip() for s in employee[2].split(",") if s.strip()
    ]

    current_lower = {s.lower() for s in current_skills}

    missing = [
        skill for skill in RECOMMENDED_SKILLS
        if skill.lower() not in current_lower
    ]

    print("\n===== SKILL RECOMMENDATIONS =====")
    print("Employee:", employee[1])

    if not missing:
        print("No new skills to recommend!")
        return

    for i, skill in enumerate(missing, start=1):
        print(f"{i}. {skill}")


def find_missing_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    current_lower = {
        s.strip().lower()
        for s in employee[2].split(",")
        if s.strip()
    }

    missing = [
        skill for skill in RECOMMENDED_SKILLS
        if skill.lower() not in current_lower
    ]

    print("\n===== MISSING SKILLS =====")

    if missing:
        for skill in missing:
            print("-", skill)
    else:
        print("No missing skills!")


def view_profile():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    skills = [
        s.strip() for s in employee[2].split(",") if s.strip()
    ]

    print("\n===== EMPLOYEE PROFILE =====")
    print("Employee ID:", employee[0])
    print("Name:", employee[1])
    print("Total Skills:", len(skills))
    print("Skills:")

    for skill in skills:
        print("-", skill)


def main():
    while True:
        print("\n===== SkillMatrix Day 27 =====")
        print("1. View Employee Skills")
        print("2. Recommend New Skills")
        print("3. Find Missing Skills")
        print("4. View Employee Profile")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_skills()
        elif choice == "2":
            recommend_skills()
        elif choice == "3":
            find_missing_skills()
        elif choice == "4":
            view_profile()
        elif choice == "5":
            print("SkillMatrix Day 27 closed.")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
