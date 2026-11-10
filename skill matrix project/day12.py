
import sqlite3

DB_NAME = "skillmatrix.db"


def find_matching_employees():
    required_input = input(
        "\nEnter required skills separated by commas: "
    ).strip()

    required_skills = {
        skill.strip().lower()
        for skill in required_input.split(",")
        if skill.strip()
    }

    if not required_skills:
        print("Please enter at least one skill.")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT emp_id, name, skills
                FROM employees
                ORDER BY name
            """)
            employees = cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return

    matches = []

    for emp_id, name, skills in employees:
        employee_skills = {
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        }

        # Employee must have ALL required skills
        if required_skills.issubset(employee_skills):
            matches.append((emp_id, name, skills))

    print("\n===== PROJECT SKILL MATCH RESULTS =====")
    print("Required Skills:", ", ".join(sorted(required_skills)))

    if not matches:
        print("No employees found with ALL required skills.")
        print("Please check the skills saved in the database.")
        return

    for emp_id, name, skills in matches:
        print("-" * 35)
        print("Employee ID:", emp_id)
        print("Name       :", name)
        print("Skills     :", skills)
        print("Skill Match:", f"{len(required_skills)}/{len(required_skills)}")
        print("Match      : 100%")

    print("-" * 35)
    print("Total matching employees:", len(matches))


def main():
    while True:
        print("\n===== SkillMatrix Day 12 =====")
        print("1. Find Employees for a Project")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            find_matching_employees()
        elif choice == "2":
            print("SkillMatrix Day 12 closed.")
            break
        else:
            print("Invalid choice. Enter 1 or 2.")


if __name__ == "__main__":
    main()
