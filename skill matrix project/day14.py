
import sqlite3

DB_NAME = "skillmatrix.db"


def add_employee():
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    skills = input(
        "Enter Skills (comma-separated, e.g. web development, python, excel): "
    ).strip()

    if not emp_id or not name or not skills:
        print("All fields are required.")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute("""
                INSERT INTO employees (emp_id, name, skills)
                VALUES (?, ?, ?)
            """, (emp_id, name, skills))

        print("Employee added successfully!")

    except sqlite3.IntegrityError:
        print("Employee ID already exists. Please use another ID.")
    except sqlite3.Error as error:
        print("Database error:", error)


def update_employee_skills():
    emp_id = input("Enter Employee ID: ").strip()
    new_skills = input(
        "Enter new skills (comma-separated): "
    ).strip()

    if not emp_id or not new_skills:
        print("Employee ID and skills are required.")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE employees
                SET skills = ?
                WHERE emp_id = ?
            """, (new_skills, emp_id))

            if cursor.rowcount == 0:
                print("Employee not found.")
            else:
                print("Employee skills updated successfully!")

    except sqlite3.Error as error:
        print("Database error:", error)


def view_employees():
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT emp_id, name, skills
                FROM employees
                ORDER BY name
            """)
            employees = cursor.fetchall()

        print("\n===== ALL EMPLOYEES =====")

        if not employees:
            print("No employees found.")
            return

        for emp_id, name, skills in employees:
            print("-" * 35)
            print("Employee ID:", emp_id)
            print("Name       :", name)
            print("Skills     :", skills)

    except sqlite3.Error as error:
        print("Database error:", error)


def main():
    while True:
        print("\n===== SkillMatrix Day 14 =====")
        print("1. Add New Employee")
        print("2. Update Employee Skills")
        print("3. View All Employees")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_employee()
        elif choice == "2":
            update_employee_skills()
        elif choice == "3":
            view_employees()
        elif choice == "4":
            print("SkillMatrix Day 14 closed.")
            break
        else:
            print("Invalid choice. Enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
