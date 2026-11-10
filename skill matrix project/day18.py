
import sqlite3

conn = sqlite3.connect("skillmatrix.db")
cursor = conn.cursor()

def update_name():
    emp_id = input("Enter Employee ID: ").strip()

    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    employee = cursor.fetchone()

    if employee:
        print("Current Name:", employee[1])
        new_name = input("Enter New Name: ").strip()

        if new_name:
            cursor.execute(
                "UPDATE employees SET name = ? WHERE emp_id = ?",
                (new_name, emp_id)
            )
            conn.commit()
            print("Employee name updated successfully!")
        else:
            print("Name cannot be empty!")
    else:
        print("Employee not found!")

def update_skills():
    emp_id = input("Enter Employee ID: ").strip()

    cursor.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,))
    employee = cursor.fetchone()

    if employee:
        print("Current Skills:", employee[2])
        new_skills = input("Enter New Skills (comma separated): ").strip()

        if new_skills:
            cursor.execute(
                "UPDATE employees SET skills = ? WHERE emp_id = ?",
                (new_skills, emp_id)
            )
            conn.commit()
            print("Employee skills updated successfully!")
        else:
            print("Skills cannot be empty!")
    else:
        print("Employee not found!")

def view_all_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    print("\n===== ALL EMPLOYEES =====")

    if not employees:
        print("No employees found!")
        return

    for emp in employees:
        print("-----------------------------------")
        print("Employee ID:", emp[0])
        print("Name       :", emp[1])
        print("Skills     :", emp[2])

def main():
    while True:
        print("\n===== SkillMatrix Day 18 =====")
        print("1. Update Employee Name")
        print("2. Update Employee Skills")
        print("3. View All Employees")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            update_name()
        elif choice == "2":
            update_skills()
        elif choice == "3":
            view_all_employees()
        elif choice == "4":
            print("SkillMatrix Day 18 closed.")
            break
        else:
            print("Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
