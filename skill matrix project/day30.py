
import sqlite3

REQUIRED_SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Excel",
    "Machine Learning",
    "Data Analysis",
    "Web Development",
    "Communication",
    "Problem Solving"
]


def connect_db():
    return sqlite3.connect("skillmatrix.db")


def get_employee(emp_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()
    return employee


def get_skill_lists(skills):
    existing = [s.strip() for s in skills.split(",") if s.strip()]
    existing_lower = [s.lower() for s in existing]

    completed = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() in existing_lower
    ]

    missing = [
        skill for skill in REQUIRED_SKILLS
        if skill.lower() not in existing_lower
    ]

    return completed, missing


def view_missing_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    _, name, skills = employee
    _, missing = get_skill_lists(skills)

    print("\n===== MISSING SKILLS =====")
    print("Employee:", name)

    if not missing:
        print("No missing skills!")
    else:
        for i, skill in enumerate(missing, 1):
            print(f"{i}. {skill}")

    print("Total Missing Skills:", len(missing))


def mark_skill_completed():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    _, name, skills = employee
    completed, missing = get_skill_lists(skills)

    print("\n===== MARK SKILL COMPLETED =====")
    print("Employee:", name)

    if not missing:
        print("All required skills are already completed!")
        return

    print("Skills available to complete:")
    for i, skill in enumerate(missing, 1):
        print(f"{i}. {skill}")

    skill_name = input("\nEnter completed skill name: ").strip()

    selected = next(
        (s for s in missing if s.lower() == skill_name.lower()),
        None
    )

    if selected is None:
        print("Invalid skill or skill already completed!")
        return

    updated_skills = skills.strip()
    if updated_skills:
        updated_skills += ", " + selected
    else:
        updated_skills = selected

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE employees SET skills = ? WHERE emp_id = ?",
        (updated_skills, emp_id)
    )

    conn.commit()
    conn.close()

    print(f"{selected} marked as completed successfully!")


def view_completed_skills():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    _, name, skills = employee
    completed, _ = get_skill_lists(skills)

    print("\n===== COMPLETED SKILLS =====")
    print("Employee:", name)

    if not completed:
        print("No required skills completed yet!")
    else:
        for i, skill in enumerate(completed, 1):
            print(f"{i}. {skill}")

    print("Total Completed Skills:", len(completed))


def view_learning_progress():
    emp_id = input("Enter Employee ID: ").strip()
    employee = get_employee(emp_id)

    if employee is None:
        print("Employee not found!")
        return

    _, name, skills = employee
    completed, missing = get_skill_lists(skills)

    total = len(REQUIRED_SKILLS)
    percentage = len(completed) / total * 100

    print("\n===== LEARNING PROGRESS =====")
    print("Employee:", name)
    print("Employee ID:", emp_id)
    print("Total Required Skills:", total)
    print("Completed Skills:", len(completed))
    print("Remaining Skills:", len(missing))
    print(f"Progress: {percentage:.2f}%")

    if percentage == 100:
        print("Congratulations! All skills completed!")
    else:
        print("Keep learning and improving!")


def main():
    while True:
        print("\n===== SkillMatrix Day 30 =====")
        print("1. View Missing Skills")
        print("2. Mark Skill as Completed")
        print("3. View Completed Skills")
        print("4. View Learning Progress")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_missing_skills()
        elif choice == "2":
            mark_skill_completed()
        elif choice == "3":
            view_completed_skills()
        elif choice == "4":
            view_learning_progress()
        elif choice == "5":
            print("SkillMatrix Day 30 closed.")
            break
        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()