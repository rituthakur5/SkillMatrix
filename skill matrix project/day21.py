
import sqlite3
import csv

def export_employees():
    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()

    conn.close()

    if not employees:
        print("\nNo employees found!")
        return

    with open("employees_report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(["Employee ID", "Name", "Skills"])
        writer.writerows(employees)

    print("\nEmployee data exported successfully!")
    print("File created: employees_report.csv")
    print("Total employees exported:", len(employees))

def main():
    while True:
        print("\n===== SkillMatrix Day 21 =====")
        print("1. Export Employees to CSV")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            export_employees()
        elif choice == "2":
            print("SkillMatrix Day 21 closed.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
