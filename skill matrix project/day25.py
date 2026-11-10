
import sqlite3

DB_NAME = "skillmatrix.db"


def get_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()

    conn.close()
    return employees


def count_skills(skills):
    return len([
        skill.strip()
        for skill in skills.split(",")
        if skill.strip()
    ])


def show_all_statistics():
    employees = get_employees()

    print("\n===== EMPLOYEE SKILLS STATISTICS =====")

    if not employees:
        print("No employees found.")
        return

    total_skills = 0

    for emp_id, name, skills in employees:
        skill_count = count_skills(skills)
        total_skills += skill_count

        print("-----------------------------------")
        print("Employee ID :", emp_id)
        print("Name        :", name)
        print("Total Skills:", skill_count)

    average = total_skills / len(employees)

    print("-----------------------------------")
    print("Total Employees:", len(employees))
    print("Total Skill Records:", total_skills)
    print("Average Skills per Employee:", round(average, 2))


def show_most_skilled():
    employees = get_employees()

    if not employees:
        print("No employees found.")
        return

    max_count = max(count_skills(emp[2]) for emp in employees)

    print("\n===== MOST SKILLED EMPLOYEE(S) =====")

    for emp in employees:
        if count_skills(emp[2]) == max_count:
            print("-----------------------------------")
            print("Employee ID :", emp[0])
            print("Name        :", emp[1])
            print("Total Skills:", max_count)


def show_least_skilled():
    employees = get_employees()

    if not employees:
        print("No employees found.")
        return

    min_count = min(count_skills(emp[2]) for emp in employees)

    print("\n===== LEAST SKILLED EMPLOYEE(S) =====")

    for emp in employees:
        if count_skills(emp[2]) == min_count:
            print("-----------------------------------")
            print("Employee ID :", emp[0])
            print("Name        :", emp[1])
            print("Total Skills:", min_count)


def main():
    while True:
        print("\n===== SkillMatrix Day 25 =====")
        print("1. View Employee Skills Statistics")
        print("2. Find Most Skilled Employee")
        print("3. Find Least Skilled Employee")
        print("4. Calculate Average Skills")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_all_statistics()

        elif choice == "2":
            show_most_skilled()

        elif choice == "3":
            show_least_skilled()

        elif choice == "4":
            employees = get_employees()

            if not employees:
                print("No employees found.")
            else:
                total = sum(count_skills(emp[2]) for emp in employees)
                average = total / len(employees)
                print("Average Skills per Employee:", round(average, 2))

        elif choice == "5":
            print("SkillMatrix Day 25 closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
