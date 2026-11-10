
import sqlite3


def get_employee(emp_id):
    conn = sqlite3.connect("skillmatrix.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()

    return employee


def get_skill_set(skills):
    return {
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    }


def compare_employees():
    id1 = input("Enter First Employee ID: ").strip()
    id2 = input("Enter Second Employee ID: ").strip()

    if id1 == id2:
        print("Please enter two different Employee IDs!")
        return

    emp1 = get_employee(id1)
    emp2 = get_employee(id2)

    if emp1 is None:
        print("First employee not found!")
        return

    if emp2 is None:
        print("Second employee not found!")
        return

    skills1 = get_skill_set(emp1[2])
    skills2 = get_skill_set(emp2[2])

    common = skills1 & skills2
    unique1 = skills1 - skills2
    unique2 = skills2 - skills1

    print("\n===== EMPLOYEE SKILL COMPARISON =====")

    print("\nEmployee 1:", emp1[1])
    print("Employee ID:", emp1[0])
    print("Total Skills:", len(skills1))

    print("\nEmployee 2:", emp2[1])
    print("Employee ID:", emp2[0])
    print("Total Skills:", len(skills2))

    print("\n===== COMMON SKILLS =====")
    if common:
        for skill in sorted(common):
            print("-", skill.title())
    else:
        print("No common skills!")

    print("\n===== UNIQUE SKILLS OF EMPLOYEE 1 =====")
    if unique1:
        for skill in sorted(unique1):
            print("-", skill.title())
    else:
        print("No unique skills!")

    print("\n===== UNIQUE SKILLS OF EMPLOYEE 2 =====")
    if unique2:
        for skill in sorted(unique2):
            print("-", skill.title())
    else:
        print("No unique skills!")

    print("\n===== SKILL COUNT COMPARISON =====")
    if len(skills1) > len(skills2):
        print(emp1[1], "has more skills.")
    elif len(skills2) > len(skills1):
        print(emp2[1], "has more skills.")
    else:
        print("Both employees have equal number of skills.")


def view_common_skills():
    id1 = input("Enter First Employee ID: ").strip()
    id2 = input("Enter Second Employee ID: ").strip()

    emp1 = get_employee(id1)
    emp2 = get_employee(id2)

    if emp1 is None or emp2 is None:
        print("Employee not found!")
        return

    common = get_skill_set(emp1[2]) & get_skill_set(emp2[2])

    print("\n===== COMMON SKILLS =====")

    if common:
        for skill in sorted(common):
            print("-", skill.title())
    else:
        print("No common skills found!")


def main():
    while True:
        print("\n===== SkillMatrix Day 33 =====")
        print("1. Compare Two Employees")
        print("2. View Common Skills")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            compare_employees()

        elif choice == "2":
            view_common_skills()

        elif choice == "3":
            print("SkillMatrix Day 33 closed.")
            break

        else:
            print("Invalid choice! Try again.")


if __name__ == "__main__":
    main()
