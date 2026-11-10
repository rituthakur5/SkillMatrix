
import sqlite3

# Connect to database
conn = sqlite3.connect("skillmatrix.db")
cursor = conn.cursor()

# Create employee table
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    emp_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    skills TEXT NOT NULL
)
""")
conn.commit()


# Add employee
def add_employee():
    emp_id = input("Enter Employee ID: ").strip()
    name = input("Enter Employee Name: ").strip()
    skills = input("Enter Skills (comma separated): ").strip()

    if not emp_id or not name or not skills:
        print("Please fill in all fields!")
        return

    try:
        cursor.execute(
            "INSERT INTO employees (emp_id, name, skills) VALUES (?, ?, ?)",
            (emp_id, name, skills)
        )
        conn.commit()
        print("Employee saved successfully!")

    except sqlite3.IntegrityError:
        print("Employee ID already exists!")


# View employees
def view_employees():
    cursor.execute("SELECT * FROM employees ORDER BY emp_id")
    employees = cursor.fetchall()

    if not employees:
        print("No employees found.")
        return

    print("\n--- Employee Records ---")

    for emp_id, name, skills in employees:
        print(f"Employee ID: {emp_id}")
        print(f"Name: {name}")
        print(f"Skills: {skills}")
        print("-" * 30)


# Main menu
try:
    while True:
        print("\n===== SkillMatrix =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            print("Thank you for using SkillMatrix!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

finally:
    conn.close()
