
import sqlite3

def search_by_id(cursor):
    emp_id = input("Enter Employee ID: ").strip()

    cursor.execute(
        "SELECT * FROM employees WHERE emp_id = ?",
        (emp_id,)
    )
    display_results(cursor.fetchall())

def search_by_name(cursor):
    name = input("Enter Employee Name: ").strip()

    cursor.execute(
        "SELECT * FROM employees WHERE name LIKE ?",
        ("%" + name + "%",)
    )
    display_results(cursor.fetchall())

def search_by_skill(cursor):
    skill = input("Enter Skill: ").strip()

    cursor.execute(
        "SELECT * FROM employees WHERE LOWER(skills) LIKE LOWER(?)",
        ("%" + skill + "%",)
    )
    display_results(cursor.fetchall())

def display_results(employees):
    print("\n===== SEARCH RESULTS =====")

    if not employees:
        print("No matching employee found!")
        return

    for emp in employees:
        print("-----------------------------------")
        print("Employee ID:", emp[0])
        print("Name       :", emp[1])
        print("Skills     :", emp[2])

    print("-----------------------------------")
    print("Total matching employees:", len(employees))

def main():
    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    while True:
        print("\n===== SkillMatrix Day 23 =====")
        print("1. Search by Employee ID")
        print("2. Search by Employee Name")
        print("3. Search by Employee Skill")
        print("4. View All Employees")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            search_by_id(cursor)

        elif choice == "2":
            search_by_name(cursor)

        elif choice == "3":
            search_by_skill(cursor)

        elif choice == "4":
            cursor.execute("SELECT * FROM employees")
            display_results(cursor.fetchall())

        elif choice == "5":
            print("SkillMatrix Day 23 closed.")
            break

        else:
            print("Invalid choice! Please try again.")

    conn.close()

if __name__ == "__main__":
    main()
