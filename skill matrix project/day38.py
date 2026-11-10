
import sqlite3

DB_NAME = "skillmatrix.db"

REQUIRED_SKILLS = [
    "Python", "Java", "C++", "SQL", "Excel",
    "Machine Learning", "Data Analysis",
    "Web Development", "Communication", "Problem Solving"
]


def get_connection():
    return sqlite3.connect(DB_NAME)


def show_dashboard():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT emp_id, name, skills FROM employees")
    employees = cursor.fetchall()

    if not employees:
        print("\nNo employees found!")
        conn.close()
        return

    total_employees = len(employees)
    total_skill_records = 0
    all_unique_skills = set()

    print("\n========== SKILLMATRIX DASHBOARD ==========")
    print("Total Employees:", total_employees)

    for emp_id, name, skills_text in employees:
        skills = {
            s.strip().lower()
            for s in skills_text.split(",")
            if s.strip()
        }

        total_skill_records += len(skills)
        all_unique_skills.update(skills)

    print("Total Unique Skills:", len(all_unique_skills))
    print("Total Employee Skill Records:", total_skill_records)

    print("\n========== EMPLOYEE DETAILS ==========")

    for emp_id, name, skills_text in employees:
        skills = {
            s.strip().lower()
            for s in skills_text.split(",")
            if s.strip()
        }

        completed = [
            skill for skill in REQUIRED_SKILLS
            if skill.lower() in skills
        ]

        missing = [
            skill for skill in REQUIRED_SKILLS
            if skill.lower() not in skills
        ]

        progress = len(completed) / len(REQUIRED_SKILLS) * 100

        print("\n----------------------------------------")
        print("Employee ID:", emp_id)
        print("Name:", name)
        print("Total Skills:", len(skills))
        print("Completed Required Skills:", len(completed))
        print("Missing Required Skills:", len(missing))
        print("Skill Progress: {:.2f}%".format(progress))

        print("Skills:", ", ".join(sorted(skills)))

        if missing:
            print("Missing:", ", ".join(missing))
        else:
            print("Missing: None")

    # Learning goals summary
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name='learning_goals'
    """)

    if cursor.fetchone():
        cursor.execute("""
            SELECT COUNT(*) FROM learning_goals
            WHERE status = 'Completed'
        """)
        completed_goals = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*) FROM learning_goals
            WHERE status = 'Pending'
        """)
        pending_goals = cursor.fetchone()[0]

        print("\n========== LEARNING GOALS SUMMARY ==========")
        print("Completed Goals:", completed_goals)
        print("Pending Goals:", pending_goals)
    else:
        print("\nLearning goals table not found.")

    print("\n============================================")
    conn.close()


def search_employee():
    emp_id = input("Enter Employee ID: ").strip().upper()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id=?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()

    if employee is None:
        print("Employee not found!")
        return

    print("\n===== EMPLOYEE PROFILE =====")
    print("Employee ID:", employee[0])
    print("Name:", employee[1])
    print("Skills:", employee[2])


def main():
    while True:
        print("\n========== SkillMatrix Day 38 ==========")
        print("1. View Complete Dashboard")
        print("2. Search Employee Profile")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            show_dashboard()

        elif choice == "2":
            search_employee()

        elif choice == "3":
            print("SkillMatrix Day 38 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
