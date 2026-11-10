
import sqlite3
from collections import Counter

conn = sqlite3.connect("skillmatrix.db")
cursor = conn.cursor()

def skill_analysis():
    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found!")
        return

    skill_count = Counter()

    for emp in employees:
        skills = [skill.strip().lower() for skill in emp[2].split(",") if skill.strip()]
        skill_count.update(set(skills))

    print("\n===== EMPLOYEE SKILL ANALYSIS =====")
    print("Total Employees:", len(employees))
    print("Total Unique Skills:", len(skill_count))

    print("\n===== SKILL-WISE EMPLOYEE COUNT =====")
    for skill, count in sorted(skill_count.items()):
        print(f"{skill.title():<20} : {count}")

    most_common = skill_count.most_common()

    if most_common:
        highest = most_common[0][1]
        print("\n===== MOST COMMON SKILL =====")
        for skill, count in most_common:
            if count == highest:
                print(f"{skill.title()} : {count} employee(s)")

def main():
    while True:
        print("\n===== SkillMatrix Day 19 =====")
        print("1. View Skill Analysis")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            skill_analysis()
        elif choice == "2":
            print("SkillMatrix Day 19 closed.")
            break
        else:
            print("Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()

