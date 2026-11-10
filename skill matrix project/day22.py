
import sqlite3
import csv
import os

def import_employees():
    filename = "employees_report.csv"

    if not os.path.exists(filename):
        print("\nCSV file not found!")
        return

    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    imported = 0
    skipped = 0

    try:
        with open(filename, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            required_columns = {"Employee ID", "Name", "Skills"}

            if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
                print("Invalid CSV format!")
                return

            for row in reader:
                emp_id = row["Employee ID"].strip()
                name = row["Name"].strip()
                skills = row["Skills"].strip()

                if not emp_id or not name or not skills:
                    skipped += 1
                    continue

                try:
                    cursor.execute(
                        """
                        INSERT INTO employees (emp_id, name, skills)
                        VALUES (?, ?, ?)
                        """,
                        (emp_id, name, skills)
                    )
                    imported += 1

                except sqlite3.IntegrityError:
                    skipped += 1

        conn.commit()

        print("\n===== IMPORT REPORT =====")
        print("Employees imported:", imported)
        print("Rows skipped:", skipped)
        print("CSV import completed!")

    except Exception as e:
        conn.rollback()
        print("Import error:", e)

    finally:
        conn.close()

def main():
    while True:
        print("\n===== SkillMatrix Day 22 =====")
        print("1. Import Employees from CSV")
        print("2. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            import_employees()
        elif choice == "2":
            print("SkillMatrix Day 22 closed.")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
