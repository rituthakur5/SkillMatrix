
import sqlite3

DB_NAME = "skillmatrix.db"


def view_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, name, skills FROM employees ORDER BY emp_id"
        )
        employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found.")
        return

    print("\n--- All Employees ---")
    for emp_id, name, skills in employees:
        print(f"ID: {emp_id} | Name: {name} | Skills: {skills}")


def search_by_skill():
    skill = input("Enter skill to search: ").strip()

    if not skill:
        print("Please enter a skill.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT emp_id, name, skills FROM employees ORDER BY emp_id"
        )
        employees = cursor.fetchall()

    # Case-insensitive, comma-separated skill matching
    matches = []
    for emp_id, name, skills in employees:
        employee_skills = [
            item.strip().casefold()
            for item in skills.split(",")
        ]

        if skill.casefold() in employee_skills:
            matches.append((emp_id, name, skills))

    if not matches:
        print(f"\nNo employees found with skill: {skill}")
        return

    print(f"\n--- Employees with {skill} ---")
    for emp_id, name, skills in matches:
        print(f"ID: {emp_id} | Name: {name} | Skills: {skills}")


def main():
    while True:
        print("\n===== SkillMatrix: Day 4 =====")
        print("1. View All Employees")
        print("2. Search Employees by Skill")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employees()
        elif choice == "2":
            search_by_skill()
        elif choice == "3":
            print("SkillMatrix closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()

