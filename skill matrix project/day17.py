
import sqlite3

DB_NAME = "skillmatrix.db"


def delete_employee():
    emp_id = input("Enter Employee ID to delete: ").strip()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )
    employee = cursor.fetchone()

    if employee is None:
        print("\nEmployee not found!")
        conn.close()
        return

    print("\n===== EMPLOYEE DETAILS =====")
    print("Employee ID:", employee[0])
    print("Name       :", employee[1])
    print("Skills     :", employee[2])

    confirm = input("\nAre you sure you want to delete? (yes/no): ").strip().lower()

    if confirm == "yes":
        cursor.execute(
            "DELETE FROM employees WHERE emp_id = ?",
            (emp_id,)
        )
        conn.commit()
        print("\nEmployee deleted successfully!")
    else:
        print("\nDelete cancelled. Employee record is safe.")

    conn.close()


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
        print("\n===== SkillMatrix Day 17 =====")
        print("1. Delete Employee by ID")
        print("2. View All Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            delete_employee()
        elif choice == "2":
            view_all_employees()
        elif choice == "3":
            print("SkillMatrix Day 17 closed.")
            break
        else:
            print("Invalid choice! Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
