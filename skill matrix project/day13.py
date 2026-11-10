
import sqlite3

DB_NAME = "skillmatrix.db"


def rank_employees():
    required_input = input(
        "\nEnter project required skills (comma-separated): "
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
            """)
            employees = cursor.fetchall()

    except sqlite3.Error as error:
        print("Database error:", error)
        return

    rankings = []

    for emp_id, name, skills in employees:
        employee_skills = {
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        }

        matched_skills = required_skills.intersection(employee_skills)

        if matched_skills:
            percentage = (
                len(matched_skills) * 100 / len(required_skills)
            )

            rankings.append((
                emp_id,
                name,
                skills,
                len(matched_skills),
                percentage
            ))

    # Highest match percentage first; names alphabetically on ties
    rankings.sort(key=lambda item: (-item[4], item[1].lower()))

    print("\n===== EMPLOYEE SKILL RANKING =====")
    print("Required skills:", ", ".join(sorted(required_skills)))

    if not rankings:
        print("No matching employees found.")
        return

    for rank, employee in enumerate(rankings, start=1):
        emp_id, name, skills, matched_count, percentage = employee

        print("-" * 35)
        print(f"Rank             : {rank}")
        print(f"Employee ID      : {emp_id}")
        print(f"Name             : {name}")
        print(f"Employee Skills  : {skills}")
        print(
            f"Skills Matched   : "
            f"{matched_count}/{len(required_skills)}"
        )
        print(f"Match Percentage : {percentage:.1f}%")

    print("-" * 35)
    print("Total matching employees:", len(rankings))


def main():
    while True:
        print("\n===== SkillMatrix Day 13 =====")
        print("1. Rank Employees for a Project")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            rank_employees()
        elif choice == "2":
            print("SkillMatrix Day 13 closed.")
            break
        else:
            print("Invalid choice. Enter 1 or 2.")


if __name__ == "__main__":
    main()
