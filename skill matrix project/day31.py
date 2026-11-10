
import sqlite3


def get_employees():
    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    rows = cursor.fetchall()

    conn.close()

    employees = []

    for emp_id, name, skills in rows:
        skill_list = [
            skill.strip()
            for skill in skills.split(",")
            if skill.strip()
        ]

        employees.append({
            "id": emp_id,
            "name": name,
            "skills": skill_list,
            "count": len(skill_list)
        })

    return employees


def view_all_employees():
    employees = get_employees()

    print("\n===== EMPLOYEE SKILL DETAILS =====")

    if not employees:
        print("No employees found!")
        return

    for emp in employees:
        print("-----------------------------------")
        print("Employee ID:", emp["id"])
        print("Name:", emp["name"])
        print("Total Skills:", emp["count"])
        print("Skills:", ", ".join(emp["skills"]))


def rank_employees():
    employees = get_employees()

    print("\n===== EMPLOYEE SKILL RANKING =====")

    if not employees:
        print("No employees found!")
        return

    employees.sort(
        key=lambda emp: (-emp["count"], emp["name"].lower())
    )

    for rank, emp in enumerate(employees, 1):
        print("-----------------------------------")
        print("Rank:", rank)
        print("Employee ID:", emp["id"])
        print("Name:", emp["name"])
        print("Total Skills:", emp["count"])


def highest_skilled_employee():
    employees = get_employees()

    print("\n===== HIGHEST SKILLED EMPLOYEE =====")

    if not employees:
        print("No employees found!")
        return

    highest = max(emp["count"] for emp in employees)

    for emp in employees:
        if emp["count"] == highest:
            print("Employee ID:", emp["id"])
            print("Name:", emp["name"])
            print("Total Skills:", emp["count"])


def lowest_skilled_employee():
    employees = get_employees()

    print("\n===== LOWEST SKILLED EMPLOYEE =====")

    if not employees:
        print("No employees found!")
        return

    lowest = min(emp["count"] for emp in employees)

    for emp in employees:
        if emp["count"] == lowest:
            print("Employee ID:", emp["id"])
            print("Name:", emp["name"])
            print("Total Skills:", emp["count"])


def main():
    while True:
        print("\n===== SkillMatrix Day 31 =====")
        print("1. View All Employees with Skill Count")
        print("2. Rank Employees by Total Skills")
        print("3. Find Highest Skilled Employee")
        print("4. Find Lowest Skilled Employee")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_all_employees()

        elif choice == "2":
            rank_employees()

        elif choice == "3":
            highest_skilled_employee()

        elif choice == "4":
            lowest_skilled_employee()

        elif choice == "5":
            print("SkillMatrix Day 31 closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
