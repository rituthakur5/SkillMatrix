
from pathlib import Path

README = """# SkillMatrix - Employee Skill Management System

## Project Overview
SkillMatrix is a Python-based employee skill management
system using SQLite database.

It helps manage employee information, skills, learning
goals, skill gaps, progress and reports.

## Technologies Used
- Python
- SQLite3
- CSV
- VS Code

## Main Features
1. Add, update and search employees
2. Manage employee skills
3. Search and filter employees
4. Sort employees by different criteria
5. Employee skill statistics
6. Skill recommendations
7. Skill gap analysis
8. Learning progress tracking
9. Employee skill comparison
10. Learning goals management
11. CSV report generation
12. Employee dashboard
13. Database testing

## Database
Database file: skillmatrix.db

Main table:
employees
- emp_id
- name
- skills

Additional table:
learning_goals
- goal_id
- emp_id
- goal
- status

## Project Files
Each day has an individual Python script.
Run the required script using:

python day40.py

## How to Run
1. Install Python.
2. Open the project folder in VS Code.
3. Open the terminal.
4. Run a Python file, for example:

   python day38.py

5. Follow the menu instructions.

## Reports
Employee reports are generated in CSV format.
Example: E101_report.csv

## Testing
Day 39 testing confirmed:
- Database check passed
- Employee check passed
- Learning goals check passed
- CSV report check passed

## Project Status
SkillMatrix Day 40 - Documentation Completed.
"""


def create_documentation():
    filename = Path("README.md")

    filename.write_text(README, encoding="utf-8")

    print("\n===== DOCUMENTATION CREATED =====")
    print("File Name: README.md")
    print("Project: SkillMatrix")
    print("Documentation saved successfully!")


def main():
    while True:
        print("\n===== SkillMatrix Day 40 =====")
        print("1. Create Project Documentation")
        print("2. View Project Summary")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_documentation()

        elif choice == "2":
            print("\n===== FINAL PROJECT SUMMARY =====")
            print("Project Name: SkillMatrix")
            print("Language: Python")
            print("Database: SQLite")
            print("Project Duration: 40 Days")
            print("Testing: 4/4 Checks Passed")
            print("Status: Documentation Ready")

        elif choice == "3":
            print("SkillMatrix Day 40 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
