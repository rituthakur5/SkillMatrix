
import sqlite3

DB_NAME = "skillmatrix.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_goals (
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            emp_id TEXT NOT NULL,
            goal TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    """)

    conn.commit()
    conn.close()


def add_goal():
    emp_id = input("Enter Employee ID: ").strip().upper()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM employees WHERE emp_id = ?",
        (emp_id,)
    )
    employee = cursor.fetchone()

    if employee is None:
        print("Employee not found!")
        conn.close()
        return

    goal = input("Enter Learning Goal: ").strip()

    if not goal:
        print("Learning goal cannot be empty!")
        conn.close()
        return

    cursor.execute(
        "INSERT INTO learning_goals (emp_id, goal) VALUES (?, ?)",
        (emp_id, goal)
    )

    conn.commit()
    conn.close()

    print("Learning goal added successfully!")


def view_goals():
    emp_id = input("Enter Employee ID: ").strip().upper()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM employees WHERE emp_id = ?",
        (emp_id,)
    )
    employee = cursor.fetchone()

    if employee is None:
        print("Employee not found!")
        conn.close()
        return

    cursor.execute("""
        SELECT goal_id, goal, status
        FROM learning_goals
        WHERE emp_id = ?
        ORDER BY goal_id
    """, (emp_id,))

    goals = cursor.fetchall()
    conn.close()

    print("\n===== LEARNING GOALS =====")
    print("Employee:", employee[0])

    if not goals:
        print("No learning goals found!")
        return

    for goal_id, goal, status in goals:
        print(f"{goal_id}. {goal} | Status: {status}")


def complete_goal():
    emp_id = input("Enter Employee ID: ").strip().upper()

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM employees WHERE emp_id = ?",
        (emp_id,)
    )

    if cursor.fetchone() is None:
        print("Employee not found!")
        conn.close()
        return

    cursor.execute("""
        SELECT goal_id, goal, status
        FROM learning_goals
        WHERE emp_id = ? AND status = 'Pending'
        ORDER BY goal_id
    """, (emp_id,))

    goals = cursor.fetchall()

    if not goals:
        print("No pending learning goals!")
        conn.close()
        return

    print("\n===== PENDING GOALS =====")
    for goal_id, goal, status in goals:
        print(f"{goal_id}. {goal}")

    try:
        goal_id = int(input("Enter Goal ID to mark completed: "))
    except ValueError:
        print("Please enter a valid Goal ID!")
        conn.close()
        return

    cursor.execute("""
        UPDATE learning_goals
        SET status = 'Completed'
        WHERE goal_id = ? AND emp_id = ? AND status = 'Pending'
    """, (goal_id, emp_id))

    if cursor.rowcount > 0:
        print("Learning goal marked as completed!")
    else:
        print("Invalid Goal ID!")

    conn.commit()
    conn.close()


def main():
    create_table()

    while True:
        print("\n===== SkillMatrix Day 36 =====")
        print("1. Add Learning Goal")
        print("2. View Learning Goals")
        print("3. Mark Goal as Completed")
        print("4. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_goal()

        elif choice == "2":
            view_goals()

        elif choice == "3":
            complete_goal()

        elif choice == "4":
            print("SkillMatrix Day 36 closed.")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
