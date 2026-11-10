
import sqlite3


def get_employees():
    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    rows = cursor.fetchall()

    conn.close()
    return rows


def search_by_skill():
    skill = input("Enter skill to search: ").strip().lower()

    employees = get_employees()
    found = []

    for emp_id, name, skills in employees:
        skill_list = [s.strip().lower() for s in skills.split(",")]

        if skill in skill_list:
            found.append((emp_id, name, skills))

    print("\n===== SEARCH RESULTS =====")

    if not found:
        print("No matching employees found!")
        return

    for emp_id, name, skills in found:
        print("-----------------------------------")
        print("Employee ID:", emp_id)
        print("Name:", name)
        print("Skills:", skills)

    print("Total Matching Employees:", len(found))


def search_by_minimum_skills():
    try:
        minimum = int(input("Enter minimum number of skills: "))
    except ValueError:
        print("Please enter a valid number!")
        return

    employees = get_employees()
    found = []

    for emp_id, name, skills in employees:
        skill_list = [s.strip() for s in skills.split(",") if s.strip()]

        if len(skill_list) >= minimum:
            found.append((emp_id, name, len(skill_list)))

    print("\n===== MINIMUM SKILL SEARCH =====")

    if not found:
        print("No matching employees found!")
        return

    for emp_id, name, count in found:
        print("-----------------------------------")
        print("Employee ID:", emp_id)
        print("Name:", name)
        print("Total Skills:", count)

    print("Total Matching Employees:", len(found))


def search_by_multiple_skills():
    user_input = input(
        "Enter skills separated by commas: "
    ).strip()

    required = [
        skill.strip().lower()
        for skill in user_input.split(",")
        if skill.strip()
    ]

    if not required:
        print("Please enter at least one skill!")
        return

    employees = get_employees()
    found = []

    for emp_id, name, skills in employees:
        skill_list = [
            s.strip().lower()
            for s in skills.split(",")
        ]

        if all(skill in skill_list for skill in required):
            found.append((emp_id, name, skills))

    print("\n===== MULTIPLE SKILL SEARCH =====")

    if not found:
        print("No employees have all the entered skills!")
        return

    for emp_id, name, skills in found:
        print("-----------------------------------")
        print("Employee ID:", emp_id)
        print("Name:", name)
        print("Skills:", skills)

    print("Total Matching Employees:", len(found))


def search_all_skills():
    user_input = input(
        "Enter all required skills separated by commas: "
    ).strip()

    required = [
        skill.strip().lower()
        for skill in user_input.split(",")
        if skill.strip()
    ]

    if not required:
        print("Please enter at least one skill!")
        return

    employees = get_employees()
    found = []

    for emp_id, name, skills in employees:
        skill_list = [
            s.strip().lower()
            for s in skills.split(",")
        ]

        if all(skill in skill_list for skill in required):
            found.append((emp_id, name, skills))

    print("\n===== EMPLOYEES WITH ALL REQUIRED SKILLS =====")

    if not found:
        print("No matching employees found!")
        return

    for emp_id, name, skills in found:
        print("-----------------------------------")
        print("Employee ID:", emp_id)
        print("Name:", name)
        print("Skills:", skills)

    print("Total Matching Employees:", len(found))


def main():
    while True:
        print("\n===== SkillMatrix Day 32 =====")
        print("1. Search Employee by Skill")
        print("2. Search Employees by Minimum Skills")
        print("3. Search Employees by Multiple Skills")
        print("4. View Employees with All Skills")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_by_skill()

        elif choice == "2":
            search_by_minimum_skills()

        elif choice == "3":
            search_by_multiple_skills()

        elif choice == "4":
            search_all_skills()

        elif choice == "5":
            print("SkillMatrix Day 32 closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
