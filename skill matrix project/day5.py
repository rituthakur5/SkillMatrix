
import sqlite3

DB_NAME = "skillmatrix.db"


def setup_database():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                project_id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                emp_id TEXT,
                project_id TEXT,
                PRIMARY KEY (emp_id, project_id),
                FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
                FOREIGN KEY (project_id) REFERENCES projects(project_id)
            )
        """)


def add_project():
    project_id = input("Enter Project ID: ").strip()
    project_name = input("Enter Project Name: ").strip()

    if not project_id or not project_name:
        print("All fields are required!")
        return

    try:
        with sqlite3.connect(DB_NAME) as conn:
            conn.execute(
                "INSERT INTO projects VALUES (?, ?)",
                (project_id, project_name)
            )
        print("Project added successfully!")

    except sqlite3.IntegrityError:
        print("Project ID already exists!")


def view_projects():
    with sqlite3.connect(DB_NAME) as conn:
        projects = conn.execute(
            "SELECT project_id, project_name FROM projects ORDER BY project_id"
        ).fetchall()

    if not projects:
        print("No projects found.")
        return

    print("\n--- Projects ---")
    for project_id, name in projects:
        print(f"Project ID: {project_id} | Name: {name}")


def assign_employee():
    emp_id = input("Enter Employee ID: ").strip()
    project_id = input("Enter Project ID: ").strip()

    with sqlite3.connect(DB_NAME) as conn:
        employee = conn.execute(
            "SELECT name FROM employees WHERE emp_id = ?", (emp_id,)
        ).fetchone()

        project = conn.execute(
            "SELECT project_name FROM projects WHERE project_id = ?",
            (project_id,)
        ).fetchone()

        if employee is None:
            print("Employee not found! Add the employee first.")
            return

        if project is None:
            print("Project not found! Add the project first.")
            return

        try:
            conn.execute(
                "INSERT INTO assignments (emp_id, project_id) VALUES (?, ?)",
                (emp_id, project_id)
            )
            print(f"{employee[0]} assigned to {project[0]} successfully!")

        except sqlite3.IntegrityError:
            print("This employee is already assigned to this project.")


def view_assignments():
    with sqlite3.connect(DB_NAME) as conn:
        rows = conn.execute("""
            SELECT e.emp_id, e.name, p.project_id, p.project_name
            FROM assignments a
            JOIN employees e ON a.emp_id = e.emp_id
            JOIN projects p ON a.project_id = p.project_id
            ORDER BY e.emp_id, p.project_id
        """).fetchall()

    if not rows:
        print("No assignments found.")
        return

    print("\n--- Project Assignments ---")
    for emp_id, name, project_id, project_name in rows:
        print(
            f"Employee: {emp_id} - {name} | "
            f"Project: {project_id} - {project_name}"
        )


def main():
    setup_database()

    while True:
        print("\n===== SkillMatrix: Day 5 =====")
        print("1. Add Project")
        print("2. View Projects")
        print("3. Assign Employee to Project")
        print("4. View Assignments")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_project()
        elif choice == "2":
            view_projects()
        elif choice == "3":
            assign_employee()
        elif choice == "4":
            view_assignments()
        elif choice == "5":
            print("SkillMatrix closed.")
            break
        else:
            print("Invalid choice. Enter 1 to 5.")


if __name__ == "__main__":
    main()
