import csv
import os
import sqlite3
import uuid
from datetime import datetime
from io import StringIO
from types import SimpleNamespace

from flask import Flask, Response, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# SkillMatrix Flask application
# Database stays in the project root; this file is inside "web application".
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
DB_PATH = os.path.join(PROJECT_DIR, "skillmatrix.db")
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "profile_pics")
ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}

app = Flask(__name__)
app.secret_key = os.environ.get("SKILLMATRIX_SECRET_KEY", "skillmatrix-local-development-key")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_connection():
    """Return a row-based SQLite connection to the existing project database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def table_columns(cursor, table_name):
    return {row[1] for row in cursor.execute(f'PRAGMA table_info("{table_name}")').fetchall()}


def create_tables():
    """Create only missing tables/columns. Existing records are never dropped."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            skills TEXT,
            deleted_at TEXT,
            profile_pic TEXT,
            department TEXT,
            designation TEXT
        )
    """)
    employee_columns = table_columns(cursor, "employees")
    for column, definition in {
        "deleted_at": "TEXT",
        "profile_pic": "TEXT",
        "department": "TEXT",
        "designation": "TEXT",
        "skills": "TEXT",
        "name": "TEXT",
    }.items():
        if column not in employee_columns:
            cursor.execute(f'ALTER TABLE employees ADD COLUMN "{column}" {definition}')

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS learning_goals (
            goal_id INTEGER PRIMARY KEY,
            emp_id TEXT,
            goal TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            title TEXT,
            description TEXT,
            target_date TEXT,
            created_at TEXT,
            id INTEGER
        )
    """)
    goal_columns = table_columns(cursor, "learning_goals")
    for column, definition in {
        "goal_id": "INTEGER",
        "emp_id": "TEXT",
        "goal": "TEXT",
        "status": "TEXT DEFAULT 'Pending'",
        "title": "TEXT",
        "description": "TEXT",
        "target_date": "TEXT",
        "created_at": "TEXT",
        "id": "INTEGER",
    }.items():
        if column not in goal_columns:
            cursor.execute(f'ALTER TABLE learning_goals ADD COLUMN "{column}" {definition}')

    # Keep the legacy goal and title columns synchronized without replacing rows.
    cursor.execute("UPDATE learning_goals SET title = goal WHERE (title IS NULL OR title = '') AND goal IS NOT NULL")
    cursor.execute("UPDATE learning_goals SET goal = title WHERE (goal IS NULL OR goal = '') AND title IS NOT NULL")
    cursor.execute("UPDATE learning_goals SET status = 'Pending' WHERE status IS NULL OR status = ''")
    cursor.execute("UPDATE learning_goals SET goal_id = rowid WHERE goal_id IS NULL OR goal_id = 0")
    cursor.execute("UPDATE learning_goals SET id = goal_id WHERE id IS NULL OR id = 0")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deleted_employees (
            emp_id TEXT,
            name TEXT,
            skills TEXT,
            profile_pic TEXT,
            department TEXT,
            designation TEXT,
            deleted_at TEXT
        )
    """)
    deleted_columns = table_columns(cursor, "deleted_employees")
    for column in ["name", "skills", "profile_pic", "department", "designation", "deleted_at"]:
        if column not in deleted_columns:
            cursor.execute(f'ALTER TABLE deleted_employees ADD COLUMN "{column}" TEXT')

    connection.commit()
    connection.close()


def get_employees(include_deleted=False):
    connection = get_connection()
    if include_deleted:
        rows = connection.execute("SELECT * FROM employees ORDER BY name COLLATE NOCASE").fetchall()
    else:
        rows = connection.execute(
            "SELECT * FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
        ).fetchall()
    connection.close()
    return rows


def get_goal_counts():
    connection = get_connection()
    total = connection.execute("SELECT COUNT(*) FROM learning_goals").fetchone()[0]
    completed = connection.execute(
        "SELECT COUNT(*) FROM learning_goals WHERE lower(COALESCE(status, 'pending')) = 'completed'"
    ).fetchone()[0]
    connection.close()
    return total, completed, total - completed


def allowed_image(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def csv_response(filename, headers, rows):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)
    writer.writerows(rows)
    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.route("/")
def index():
    employees = get_employees()
    total_goals, completed_goals, pending_goals = get_goal_counts()
    return render_template(
        "index.html",
        employees=employees,
        total_employees=len(employees),
        total_goals=total_goals,
        completed_goals=completed_goals,
        pending_goals=pending_goals,
        messages=[],
    )


@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        emp_id = request.form.get("emp_id", "").strip()
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()
        designation = request.form.get("designation", "").strip()
        skills = request.form.get("skills", "").strip()
        if not all([emp_id, name, skills]):
            return render_template("add_employee.html", error="Please fill all required fields.")
        connection = get_connection()
        try:
            connection.execute(
                "INSERT INTO employees (emp_id, name, skills, department, designation, deleted_at) VALUES (?, ?, ?, ?, ?, NULL)",
                (emp_id, name, skills, department, designation),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.close()
            return render_template("add_employee.html", error="Employee ID already exists. Please use another ID.")
        connection.close()
        flash("Employee added successfully.")
        return redirect(url_for("view_employees"))
    return render_template("add_employee.html", error=None)


@app.route("/view_employees")
def view_employees():
    department = request.args.get("department", "").strip()
    designation = request.args.get("designation", "").strip()
    connection = get_connection()
    query = "SELECT * FROM employees WHERE (deleted_at IS NULL OR deleted_at = '')"
    params = []
    if department:
        query += " AND department = ?"
        params.append(department)
    if designation:
        query += " AND designation = ?"
        params.append(designation)
    query += " ORDER BY name COLLATE NOCASE"
    employees = connection.execute(query, params).fetchall()
    departments = connection.execute(
        "SELECT DISTINCT department FROM employees WHERE department IS NOT NULL AND department != '' AND (deleted_at IS NULL OR deleted_at = '') ORDER BY department"
    ).fetchall()
    designations = connection.execute(
        "SELECT DISTINCT designation FROM employees WHERE designation IS NOT NULL AND designation != '' AND (deleted_at IS NULL OR deleted_at = '') ORDER BY designation"
    ).fetchall()
    connection.close()
    return render_template(
        "view_employees.html", employees=employees, departments=departments,
        designations=designations, selected_department=department,
        selected_designation=designation, total_employees=len(employees), messages=get_flashed_messages_safe()
    )


def get_flashed_messages_safe():
    from flask import get_flashed_messages
    return get_flashed_messages()


@app.route("/edit_employee/<emp_id>", methods=["GET", "POST"])
def edit_employee(emp_id):
    connection = get_connection()
    employee = connection.execute(
        "SELECT * FROM employees WHERE emp_id = ? AND (deleted_at IS NULL OR deleted_at = '')", (emp_id,)
    ).fetchone()
    if employee is None:
        connection.close()
        flash("Employee not found.")
        return redirect(url_for("view_employees"))
    if request.method == "POST":
        new_emp_id = request.form.get("emp_id", "").strip()
        name = request.form.get("name", "").strip()
        department = request.form.get("department", "").strip()
        designation = request.form.get("designation", "").strip()
        skills = request.form.get("skills", "").strip()
        try:
            connection.execute(
                "UPDATE employees SET emp_id=?, name=?, department=?, designation=?, skills=? WHERE emp_id=?",
                (new_emp_id, name, department, designation, skills, emp_id),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            connection.close()
            return render_template("edit_employee.html", employee=employee, error="That Employee ID is already in use.")
        connection.close()
        flash("Employee details updated successfully.")
        return redirect(url_for("view_employees"))
    connection.close()
    return render_template("edit_employee.html", employee=employee, error=None)


@app.route("/delete_employee/<emp_id>", methods=["POST"])
def delete_employee(emp_id):
    connection = get_connection()
    employee = connection.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,)).fetchone()
    if employee:
        deleted_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connection.execute(
            "INSERT INTO deleted_employees (emp_id, name, skills, profile_pic, department, designation, deleted_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (employee["emp_id"], employee["name"], employee["skills"], employee["profile_pic"], employee["department"], employee["designation"], deleted_at),
        )
        connection.execute("DELETE FROM employees WHERE emp_id = ?", (emp_id,))
        connection.commit()
        flash("Employee moved to Recycle Bin.")
    else:
        flash("Employee not found.")
    connection.close()
    return redirect(url_for("view_employees"))


@app.route("/search_employee", methods=["GET", "POST"])
def search_employee():
    query = request.form.get("query", "").strip() if request.method == "POST" else ""
    employees = []
    searched = request.method == "POST"
    if searched and query:
        connection = get_connection()
        employees = connection.execute(
            "SELECT emp_id, name, skills FROM employees WHERE (deleted_at IS NULL OR deleted_at = '') AND (emp_id LIKE ? OR name LIKE ?) ORDER BY name COLLATE NOCASE",
            (f"%{query}%", f"%{query}%"),
        ).fetchall()
        connection.close()
    return render_template("search_employee.html", employees=employees, query=query, searched=searched)


@app.route("/employee_profile/<emp_id>", methods=["GET", "POST"])
def employee_profile(emp_id):
    connection = get_connection()
    employee = connection.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,)).fetchone()
    if employee is None:
        connection.close()
        flash("Employee not found.")
        return redirect(url_for("view_employees"))
    if request.method == "POST":
        action = request.form.get("action")
        if action == "upload":
            photo = request.files.get("photo")
            if not photo or not photo.filename:
                connection.close()
                flash("Please select an image first.")
                return redirect(url_for("employee_profile", emp_id=emp_id))
            if not allowed_image(photo.filename):
                connection.close()
                flash("Please upload PNG, JPG, JPEG, GIF or WEBP image.")
                return redirect(url_for("employee_profile", emp_id=emp_id))
            extension = secure_filename(photo.filename).rsplit(".", 1)[1].lower()
            filename = f"{uuid.uuid4().hex}.{extension}"
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
            old_picture = employee["profile_pic"]
            connection.execute("UPDATE employees SET profile_pic = ? WHERE emp_id = ?", (filename, emp_id))
            connection.commit()
            if old_picture:
                old_path = os.path.join(UPLOAD_FOLDER, os.path.basename(old_picture))
                if os.path.isfile(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass
            flash("Profile picture uploaded successfully.")
        elif action == "remove":
            old_picture = employee["profile_pic"]
            connection.execute("UPDATE employees SET profile_pic = NULL WHERE emp_id = ?", (emp_id,))
            connection.commit()
            if old_picture:
                old_path = os.path.join(UPLOAD_FOLDER, os.path.basename(old_picture))
                if os.path.isfile(old_path):
                    try:
                        os.remove(old_path)
                    except OSError:
                        pass
            flash("Profile picture removed.")
        connection.close()
        return redirect(url_for("employee_profile", emp_id=emp_id))
    total_skills = len([x.strip() for x in (employee["skills"] or "").split(",") if x.strip()])
    connection.close()
    return render_template("employee_profile.html", employee=employee, total_skills=total_skills, messages=get_flashed_messages_safe())


@app.route("/recycle_bin")
def recycle_bin():
    connection = get_connection()
    employees = connection.execute("SELECT * FROM deleted_employees ORDER BY deleted_at DESC").fetchall()
    connection.close()
    return render_template("recycle_bin.html", employees=employees, messages=get_flashed_messages_safe())


@app.route("/restore_employee/<emp_id>", methods=["POST"])
def restore_employee(emp_id):
    connection = get_connection()
    employee = connection.execute("SELECT * FROM deleted_employees WHERE emp_id = ?", (emp_id,)).fetchone()
    if employee:
        existing = connection.execute("SELECT 1 FROM employees WHERE emp_id = ?", (emp_id,)).fetchone()
        if existing:
            flash("An employee with this ID already exists. Change the ID before restoring.")
        else:
            connection.execute(
                "INSERT INTO employees (emp_id, name, skills, profile_pic, department, designation, deleted_at) VALUES (?, ?, ?, ?, ?, ?, NULL)",
                (employee["emp_id"], employee["name"], employee["skills"], employee["profile_pic"], employee["department"], employee["designation"]),
            )
            connection.execute("DELETE FROM deleted_employees WHERE emp_id = ?", (emp_id,))
            connection.commit()
            flash("Employee restored successfully.")
    else:
        flash("Employee not found in Recycle Bin.")
    connection.close()
    return redirect(url_for("recycle_bin"))


@app.route("/permanently_delete_employee/<emp_id>", methods=["POST"])
def permanently_delete_employee(emp_id):
    connection = get_connection()
    connection.execute("DELETE FROM deleted_employees WHERE emp_id = ?", (emp_id,))
    connection.commit()
    connection.close()
    flash("Employee permanently deleted from Recycle Bin.")
    return redirect(url_for("recycle_bin"))


@app.route("/learning_goals", methods=["GET", "POST"])
def learning_goals():
    connection = get_connection()
    if request.method == "POST":
        emp_id = request.form.get("emp_id", "").strip()
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        target_date = request.form.get("target_date", "").strip()
        employee = connection.execute("SELECT emp_id FROM employees WHERE emp_id = ?", (emp_id,)).fetchone()
        if not employee or not title:
            connection.close()
            flash("Please select an employee and enter a goal title.")
            return redirect(url_for("learning_goals"))
        next_id = connection.execute(
            "SELECT COALESCE(MAX(COALESCE(goal_id, id, 0)), 0) + 1 FROM learning_goals"
        ).fetchone()[0]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        connection.execute(
            "INSERT INTO learning_goals (goal_id, emp_id, goal, status, title, description, target_date, created_at, id) VALUES (?, ?, ?, 'Pending', ?, ?, ?, ?, ?)",
            (next_id, emp_id, title, title, description, target_date, now, next_id),
        )
        connection.commit()
        connection.close()
        flash("Learning goal added successfully.")
        return redirect(url_for("learning_goals"))

    employees = connection.execute(
        "SELECT emp_id, name FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
    ).fetchall()
    goals = connection.execute("""
        SELECT lg.goal_id, lg.id, lg.emp_id, lg.goal, lg.status, lg.title, lg.description,
               lg.target_date, lg.created_at, e.name AS name
        FROM learning_goals lg LEFT JOIN employees e ON e.emp_id = lg.emp_id
        ORDER BY COALESCE(lg.created_at, '') DESC, lg.goal_id DESC
    """).fetchall()
    connection.close()
    return render_template("learning_goals.html", employees=employees, goals=goals, messages=get_flashed_messages_safe())


@app.route("/complete_goal/<int:goal_id>", methods=["POST"])
def complete_goal(goal_id):
    connection = get_connection()
    connection.execute("UPDATE learning_goals SET status = 'Completed' WHERE goal_id = ? OR id = ?", (goal_id, goal_id))
    connection.commit()
    connection.close()
    flash("Learning goal marked as completed.")
    return redirect(url_for("learning_goals"))


@app.route("/delete_goal/<int:goal_id>", methods=["POST"])
def delete_goal(goal_id):
    connection = get_connection()
    connection.execute("DELETE FROM learning_goals WHERE goal_id = ? OR id = ?", (goal_id, goal_id))
    connection.commit()
    connection.close()
    flash("Learning goal deleted.")
    return redirect(url_for("learning_goals"))


@app.route("/employee_progress")
def employee_progress():
    connection = get_connection()
    employees = connection.execute(
        "SELECT emp_id, name FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
    ).fetchall()
    progress = []
    for employee in employees:
        total = connection.execute("SELECT COUNT(*) FROM learning_goals WHERE emp_id = ?", (employee["emp_id"],)).fetchone()[0]
        completed = connection.execute(
            "SELECT COUNT(*) FROM learning_goals WHERE emp_id = ? AND lower(COALESCE(status, 'pending')) = 'completed'",
            (employee["emp_id"],),
        ).fetchone()[0]
        pending = total - completed
        percentage = round((completed / total) * 100) if total else 0
        progress.append(SimpleNamespace(
            emp_id=employee["emp_id"], name=employee["name"], total_goals=total,
            completed_goals=completed, pending_goals=pending, percentage=percentage
        ))
    connection.close()
    return render_template("employee_progress.html", progress=progress)


@app.route("/skill_gap", methods=["GET", "POST"])
def skill_gap():
    connection = get_connection()
    employees = connection.execute(
        "SELECT emp_id, name, skills FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
    ).fetchall()
    result = None
    selected_emp_id = ""
    required_skills_text = ""
    if request.method == "POST":
        selected_emp_id = request.form.get("emp_id", "").strip()
        required_skills_text = request.form.get("required_skills", "").strip()
        employee = connection.execute("SELECT * FROM employees WHERE emp_id = ?", (selected_emp_id,)).fetchone()
        if employee:
            existing = [x.strip() for x in (employee["skills"] or "").split(",") if x.strip()]
            required = [x.strip() for x in required_skills_text.split(",") if x.strip()]
            existing_map = {x.casefold(): x for x in existing}
            matched = [existing_map[x.casefold()] for x in required if x.casefold() in existing_map]
            missing = [x for x in required if x.casefold() not in existing_map]
            result = SimpleNamespace(
                employee=employee["name"], emp_id=employee["emp_id"], matched=matched,
                missing=missing, existing=existing,
                percentage=round(len(matched) / len(required) * 100) if required else 0,
                total=len(required)
            )
        else:
            flash("Please select a valid employee.")
    connection.close()
    return render_template(
        "skill_gap.html", employees=employees, result=result, selected_emp_id=selected_emp_id,
        required_skills_text=required_skills_text, messages=get_flashed_messages_safe()
    )


COURSE_RECOMMENDATIONS = {
    "python": "Python Programming Course",
    "sql": "SQL and Database Fundamentals",
    "excel": "Microsoft Excel Skills Training",
    "web development": "Full Stack Web Development Course",
    "java": "Java Programming Course",
    "c++": "C++ Programming Course",
    "machine learning": "Machine Learning Fundamentals",
    "data science": "Data Science Foundations",
    "html": "HTML and CSS Web Design",
    "css": "HTML and CSS Web Design",
    "javascript": "JavaScript for Web Development",
    "communication": "Workplace Communication Skills",
    "leadership": "Leadership Development Course",
}


@app.route("/training_recommendations", methods=["GET", "POST"])
def training_recommendations():
    connection = get_connection()
    employees = connection.execute(
        "SELECT emp_id, name, skills FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
    ).fetchall()
    selected_employee = None
    required_skills = ""
    missing_skills = []
    recommendations = []
    if request.method == "POST":
        emp_id = request.form.get("emp_id", "").strip()
        required_skills = request.form.get("required_skills", "").strip()
        selected_employee = connection.execute("SELECT * FROM employees WHERE emp_id = ?", (emp_id,)).fetchone()
        if selected_employee:
            current = {x.strip().casefold() for x in (selected_employee["skills"] or "").split(",") if x.strip()}
            required = [x.strip() for x in required_skills.split(",") if x.strip()]
            missing_skills = [x for x in required if x.casefold() not in current]
            recommendations = [
                {"skill": skill, "course": COURSE_RECOMMENDATIONS.get(skill.casefold(), f"{skill} Training Course")}
                for skill in missing_skills
            ]
        else:
            flash("Please select a valid employee.")
    connection.close()
    return render_template(
        "training_recommendations.html", employees=employees, selected_employee=selected_employee,
        required_skills=required_skills, missing_skills=missing_skills,
        recommendations=recommendations, messages=get_flashed_messages_safe()
    )


@app.route("/department_dashboard")
def department_dashboard():
    connection = get_connection()
    rows = connection.execute("""
        SELECT COALESCE(NULLIF(department, ''), 'Not Assigned') AS department, COUNT(*) AS count
        FROM employees WHERE deleted_at IS NULL OR deleted_at = ''
        GROUP BY COALESCE(NULLIF(department, ''), 'Not Assigned')
        ORDER BY count DESC, department
    """).fetchall()
    total_employees = connection.execute(
        "SELECT COUNT(*) FROM employees WHERE deleted_at IS NULL OR deleted_at = ''"
    ).fetchone()[0]
    assigned_employees = connection.execute(
        "SELECT COUNT(*) FROM employees WHERE department IS NOT NULL AND department != '' AND (deleted_at IS NULL OR deleted_at = '')"
    ).fetchone()[0]
    connection.close()
    department_data = [SimpleNamespace(
        name=row["department"], count=row["count"],
        percentage=round(row["count"] / total_employees * 100) if total_employees else 0
    ) for row in rows]
    return render_template(
        "department_dashboard.html", department_data=department_data,
        total_employees=total_employees, total_departments=len(rows), assigned_employees=assigned_employees
    )


@app.route("/reports")
def reports():
    connection = get_connection()
    employees = connection.execute(
        "SELECT * FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY name COLLATE NOCASE"
    ).fetchall()
    goals = connection.execute("""
        SELECT lg.*, e.name AS name FROM learning_goals lg
        LEFT JOIN employees e ON e.emp_id = lg.emp_id
        ORDER BY lg.goal_id DESC
    """).fetchall()
    connection.close()
    total_goals = len(goals)
    completed_goals = sum(1 for goal in goals if (goal["status"] or "Pending").lower() == "completed")
    return render_template(
        "reports.html", employees=employees, goals=goals, total_employees=len(employees),
        total_goals=total_goals, completed_goals=completed_goals, pending_goals=total_goals-completed_goals
    )


@app.route("/export_employees")
def export_employees():
    connection = get_connection()
    rows = connection.execute(
        "SELECT emp_id, name, department, designation, skills FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY emp_id"
    ).fetchall()
    connection.close()
    return csv_response("employees_report.csv", ["Employee ID", "Name", "Department", "Designation", "Skills"], rows)


@app.route("/export_goals")
def export_goals():
    connection = get_connection()
    rows = connection.execute("""
        SELECT lg.emp_id, COALESCE(e.name, ''), COALESCE(lg.title, lg.goal, ''),
               COALESCE(lg.description, ''), COALESCE(lg.target_date, ''), COALESCE(lg.status, 'Pending')
        FROM learning_goals lg LEFT JOIN employees e ON e.emp_id = lg.emp_id
        ORDER BY lg.goal_id
    """).fetchall()
    connection.close()
    return csv_response("learning_goals_report.csv", ["Employee ID", "Employee Name", "Goal", "Description", "Target Date", "Status"], rows)


@app.route("/export_skills")
def export_skills():
    connection = get_connection()
    rows = connection.execute(
        "SELECT emp_id, name, skills FROM employees WHERE deleted_at IS NULL OR deleted_at = '' ORDER BY emp_id"
    ).fetchall()
    connection.close()
    return csv_response("skills_report.csv", ["Employee ID", "Name", "Skills"], rows)


# Initialize missing schema safely when the app starts.
create_tables()


if __name__ == "__main__":
    app.run(debug=True)
