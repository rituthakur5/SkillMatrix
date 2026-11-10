
import sqlite3

DB_NAME = "skillmatrix.db"


def view_employees():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT emp_id, name, skills FROM employees")
        employees = cursor.fetchall()

    print("\n===== Employee List =====")
    if not employees:
        print("No employees found.")
        return

    for emp_id, name, skills in employees:
        print(f"ID: {emp_id} | Name: {name} | Skills: {skills}")


def update_employee():
    emp_id = input("Enter Employee ID to update: ").strip()

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name, skills FROM employees WHERE emp_id = ?",
            (emp_id,)
        )
        employee = cursor.fetchone()

        if employee is None:
            print("Employee not found.")
            return

        print(f"Current Name: {employee[0]}")
        print(f"Current Skills: {employee[1]}")

        new_name = input("Enter new name (Enter to keep current): ").strip()
        new_skills = input("Enter new skills (Enter to keep current): ").strip()

        if not new_name:
            new_name = employee[0]
        if not new_skills:
            new_skills = employee[1]

        cursor.execute(
            "UPDATE employees SET name = ?, skills = ? WHERE emp_id = ?",
            (new_name, new_skills, emp_id)
        )

    print("Employee updated successfully!")


def delete_employee():
    emp_id = input("Enter Employee ID to delete: ").strip()

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM employees WHERE emp_id = ?",
            (emp_id,)
        )
        employee = cursor.fetchone()

        if employee is None:
            print("Employee not found.")
            return

        confirm = input(
            f"Delete {employee[0]}? Type YES to confirm: "
        ).strip()

        if confirm == "YES":
            cursor.execute(
                "DELETE FROM assignments WHERE emp_id = ?",
                (emp_id,)
            )
            cursor.execute(
                "DELETE FROM employees WHERE emp_id = ?",
                (emp_id,)
            )
            print("Employee deleted successfully!")
        else:
            print("Delete cancelled.")


def main():
    while True:
        print("\n===== SkillMatrix Day 8 =====")
        print("1. View Employees")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_employees()
        elif choice == "2":
            update_employee()
        elif choice == "3":
            delete_employee()
        elif choice == "4":
            print("SkillMatrix Day 8 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
