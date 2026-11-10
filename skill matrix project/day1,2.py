print("Welcome to SkillMatrix!")
print("Day 1: Project Setup")
print("Python is working successfully.")

# SkillMatrix Project
# Day 2: Employee Management

employees = []

def add_employee():
    emp_id = input("Enter Employee ID: ")
    name = input("Enter Employee Name: ")
    skills = input("Enter Skills (comma separated): ")

    employee = {
        "id": emp_id,
        "name": name,
        "skills": [skill.strip() for skill in skills.split(",")]
    }

    employees.append(employee)
    print("\nEmployee added successfully!")


def view_employees():
    if not employees:
        print("\nNo employees found.")
        return

    print("\n--- Employee List ---")

    for emp in employees:
        print(f"\nID: {emp['id']}")
        print(f"Name: {emp['name']}")
        print(f"Skills: {', '.join(emp['skills'])}")


def main():
    while True:
        print("\n===== SkillMatrix =====")
        print("1. Add Employee")
        print("2. View Employees")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            print("Thank you for using SkillMatrix!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
