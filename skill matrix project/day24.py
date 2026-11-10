
import sqlite3

DB_NAME = "skillmatrix.db"


def get_employees():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees"
    )
    employees = cursor.fetchall()

    conn.close()
    return employees


def count_skills(skills):
    return len([s.strip() for s in skills.split(",") if s.strip()])


def display_employees(employees):
    print("\n===== EMPLOYEE RECORDS =====")

    if not employees:
        print("No employees found.")
        return

    for emp_id, name, skills in employees:
        print("-----------------------------------")
        print("Employee ID :", emp_id)
        print("Name        :", name)
        print("Skills      :", skills)
        print("Total Skills:", count_skills(skills))

    print("-----------------------------------")
    print("Total Employees:", len(employees))


def sort_by_name():
    employees = get_employees()
    employees.sort(key=lambda x: x[1].lower())
    display_employees(employees)


def sort_by_id():
    employees = get_employees()
    employees.sort(key=lambda x: x[0].lower())
    display_employees(employees)


def sort_by_skills():
    employees = get_employees()
    employees.sort(
        key=lambda x: count_skills(x[2]),
        reverse=True
    )
    display_employees(employees)


def main():
    while True:
        print("\n===== SkillMatrix Day 24 =====")
        print("1. Sort Employees by Name")
        print("2. Sort Employees by ID")
        print("3. Sort Employees by Total Skills")
        print("4. View All Employees")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            sort_by_name()
        elif choice == "2":
            sort_by_id()
        elif choice == "3":
            sort_by_skills()
        elif choice == "4":
            display_employees(get_employees())
        elif choice == "5":
            print("SkillMatrix Day 24 closed.")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
