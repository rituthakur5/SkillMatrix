
import sqlite3

DB_NAME = "skillmatrix.db"


def search_employee():
    emp_id = input("Enter Employee ID to search: ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()

    if employee:
        print("\n===== EMPLOYEE FOUND =====")
        print("Employee ID:", employee[0])
        print("Name       :", employee[1])
        print("Skills     :", employee[2])
    else:
        print("\nEmployee not found!")


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

    for emp in employees:
        print("-----------------------------------")
        print("Employee ID:", emp[0])
        print("Name       :", emp[1])
        print("Skills     :", emp[2])


def main():
    while True:
        print("\n===== SkillMatrix Day 15 =====")
        print("1. Search Employee by ID")
        print("2. View All Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_employee()
        elif choice == "2":
            view_all_employees()
        elif choice == "3":
            print("SkillMatrix Day 15 closed.")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
