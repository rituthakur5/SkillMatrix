
import sqlite3

DB_NAME = "skillmatrix.db"


def search_by_skill():
    search_skill = input("Enter skill to search: ").strip().lower()

    if not search_skill:
        print("Please enter a skill.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()
    conn.close()

    found = []

    for emp in employees:
        emp_id, name, skills = emp

        skill_list = [
            skill.strip().lower()
            for skill in skills.split(",")
        ]

        if search_skill in skill_list:
            found.append(emp)

    if found:
        print("\n===== MATCHING EMPLOYEES =====")

        for emp_id, name, skills in found:
            print("-----------------------------------")
            print("Employee ID:", emp_id)
            print("Name       :", name)
            print("Skills     :", skills)

        print("-----------------------------------")
        print("Total matching employees:", len(found))
    else:
        print("\nNo employee found with this skill.")


def view_all_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees ORDER BY emp_id"
    )
    employees = cursor.fetchall()
    conn.close()

    print("\n===== ALL EMPLOYEES =====")

    if not employees:
        print("No employees found.")
        return

    for emp_id, name, skills in employees:
        print("-----------------------------------")
        print("Employee ID:", emp_id)
        print("Name       :", name)
        print("Skills     :", skills)


def main():
    while True:
        print("\n===== SkillMatrix Day 16 =====")
        print("1. Search Employees by Skill")
        print("2. View All Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_by_skill()
        elif choice == "2":
            view_all_employees()
        elif choice == "3":
            print("SkillMatrix Day 16 closed.")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
