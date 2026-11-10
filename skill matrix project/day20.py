
import sqlite3
from collections import Counter

conn = sqlite3.connect("skillmatrix.db")
cursor = conn.cursor()

def show_dashboard():
    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()

    print("\n========== SKILLMATRIX DASHBOARD ==========")

    if not employees:
        print("No employees found!")
        return

    skill_count = Counter()
    employee_skill_data = []

    for emp_id, name, skills in employees:
        skill_list = list(set(
            skill.strip().lower()
            for skill in skills.split(",")
            if skill.strip()
        ))

        skill_count.update(skill_list)
        employee_skill_data.append((emp_id, name, skill_list))

    print("\n----- OVERALL SUMMARY -----")
    print("Total Employees     :", len(employees))
    print("Total Unique Skills :", len(skill_count))
    print("Total Skill Records :", sum(skill_count.values()))

    print("\n----- EMPLOYEE DETAILS -----")

    for emp_id, name, skills in employee_skill_data:
        print("-----------------------------------")
        print("Employee ID :", emp_id)
        print("Name        :", name)
        print("Total Skills:", len(skills))
        print("Skills      :", ", ".join(sorted(skills)))

    print("\n----- SKILL-WISE REPORT -----")

    for skill, count in sorted(skill_count.items()):
        print(f"{skill.title():<20}: {count} employee(s)")

    print("\n----- MOST COMMON SKILL -----")

    if skill_count:
        highest = max(skill_count.values())

        for skill, count in sorted(skill_count.items()):
            if count == highest:
                print(f"{skill.title()} : {count} employee(s)")

    print("\n==========================================")

def main():
    while True:
        print("\n===== SkillMatrix Day 20 =====")
        print("1. View Performance Dashboard")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_dashboard()
        elif choice == "2":
            print("SkillMatrix Day 20 closed.")
            break
        else:
            print("Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
