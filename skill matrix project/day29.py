
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


def connect_db():
    return sqlite3.connect(DB_NAME)


def recommend_skills():
    emp_id = input("Enter Employee ID: ").strip()

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
    "SELECT name, skills FROM employees WHERE emp_id = ?",
    (emp_id,)
)

    employee = cursor.fetchone()
    conn.close()

    if employee is None:
        print("Employee not found!")
        return

    name, skills = employee

    existing_skills = {
        skill.strip().lower()
        for skill in skills.split(",")
    }

    missing_skills = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() not in existing_skills
    ]

    print("\n===== SKILL DEVELOPMENT RECOMMENDATIONS =====")
    print("Employee ID:", emp_id)
    print("Employee Name:", name)

    if not missing_skills:
        print("\nExcellent! All required skills are completed.")
    else:
        print("\nRecommended Skills to Learn:")

        for i, skill in enumerate(missing_skills, 1):
            print(f"{i}. {skill}")

        print("\nTotal Recommended Skills:", len(missing_skills))


def main():
    while True:
        print("\n===== SkillMatrix Day 29 =====")
        print("1. View Skill Recommendations")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            recommend_skills()

        elif choice == "2":
            print("SkillMatrix Day 29 closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
