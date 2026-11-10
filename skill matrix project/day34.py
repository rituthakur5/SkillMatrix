
import sqlite3

DB_NAME = "skillmatrix.db"


def get_employee(emp_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT emp_id, name, skills FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    employee = cursor.fetchone()
    conn.close()
    return employee


def compare_employees():
    first_id = input("Enter First Employee ID: ").strip().upper()
    second_id = input("Enter Second Employee ID: ").strip().upper()

    if first_id == second_id:
        print("Please enter two different Employee IDs!")
        return

    emp1 = get_employee(first_id)
    emp2 = get_employee(second_id)

    if emp1 is None:
        print("First Employee not found!")
        return

    if emp2 is None:
        print("Second Employee not found!")
        return

    skills1 = {s.strip().lower() for s in emp1[2].split(",") if s.strip()}
    skills2 = {s.strip().lower() for s in emp2[2].split(",") if s.strip()}

    common = skills1 & skills2
    unique1 = skills1 - skills2
    unique2 = skills2 - skills1

    total_unique = len(skills1 | skills2)

    similarity = (
        len(common) / total_unique * 100
        if total_unique else 0
    )

    print("\n===== EMPLOYEE SKILL COMPARISON =====")
    print("------------------------------------")
    print("First Employee :", emp1[1], f"({emp1[0]})")
    print("Second Employee:", emp2[1], f"({emp2[0]})")

    print("\nCommon Skills:")
    print(", ".join(sorted(common)) if common else "None")

    print("\nSkills Only in First Employee:")
    print(", ".join(sorted(unique1)) if unique1 else "None")

    print("\nSkills Only in Second Employee:")
    print(", ".join(sorted(unique2)) if unique2 else "None")

    print("\nTotal Common Skills:", len(common))
    print("Skill Similarity: {:.2f}%".format(similarity))
    print("------------------------------------")


def main():
    while True:
        print("\n===== SkillMatrix Day 34 =====")
        print("1. Compare Two Employees")
        print("2. View Common Skills")
        print("3. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            compare_employees()

        elif choice == "2":
            first_id = input("Enter First Employee ID: ").strip().upper()
            second_id = input("Enter Second Employee ID: ").strip().upper()

            emp1 = get_employee(first_id)
            emp2 = get_employee(second_id)

            if not emp1 or not emp2:
                print("Employee not found!")
            elif first_id == second_id:
                print("Please enter two different Employee IDs!")
            else:
                common = (
                    {s.strip().lower() for s in emp1[2].split(",") if s.strip()}
                    &
                    {s.strip().lower() for s in emp2[2].split(",") if s.strip()}
                )

                print("\n===== COMMON SKILLS =====")
                print(", ".join(sorted(common)) if common else "No common skills found.")
                print("Total Common Skills:", len(common))

        elif choice == "3":
            print("SkillMatrix Day 34 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
