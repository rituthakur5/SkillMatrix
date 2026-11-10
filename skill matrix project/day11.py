
import sqlite3

DB_NAME = "skillmatrix.db"


def find_employees_by_skill():
    skill = input("\nEnter skill to search (e.g. Python): ").strip()

    if not skill:
        print("Please enter a skill.")
        return

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT emp_id, name, skills
            FROM employees
            ORDER BY name
        """)
        employees = cursor.fetchall()

    matches = []

    for emp_id, name, skills in employees:
        skill_list = [s.strip().lower() for s in skills.split(",")]

        if skill.lower() in skill_list:
            matches.append((emp_id, name, skills))

    print(f"\n===== Employees with skill: {skill} =====")

    if not matches:
        print("No employees found with this skill.")
        return

    for emp_id, name, skills in matches:
        print(f"Employee ID: {emp_id}")
        print(f"Name       : {name}")
        print(f"Skills     : {skills}")
        print("-" * 30)

    print(f"Total matching employees: {len(matches)}")


def show_all_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT emp_id, name, skills
            FROM employees
            ORDER BY name
        """)
        employees = cursor.fetchall()

    print("\n===== All Employees =====")

    if not employees:
        print("No employees found.")
        return

    for emp_id, name, skills in employees:
        print(f"{emp_id} | {name} | {skills}")


def main():
    while True:
        print("\n===== SkillMatrix Day 11 =====")
        print("1. Search Employees by Skill")
        print("2. View All Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            find_employees_by_skill()
        elif choice == "2":
            show_all_employees()
        elif choice == "3":
            print("SkillMatrix Day 11 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
