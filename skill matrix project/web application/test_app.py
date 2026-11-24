
from app import app, get_connection

client = app.test_client()

passed = 0
failed = 0

print("\n====================================")
print("       SKILLMATRIX DAY 52 TEST")
print("====================================")


def test_page(name, method, url, data=None):
    global passed, failed

    try:
        if method == "GET":
            response = client.get(url)
        else:
            response = client.post(url, data=data or {})

        if response.status_code == 200:
            print("PASS:", name)
            passed += 1
        else:
            print("FAIL:", name, "| Status:", response.status_code)
            failed += 1

    except Exception as error:
        print("FAIL:", name, "| Error:", error)
        failed += 1


# Page tests
test_page("Dashboard", "GET", "/")
test_page("Add Employee Page", "GET", "/add_employee")
test_page("View Employees Page", "GET", "/view_employees")
test_page("Search Employee Page", "GET", "/search_employee")
test_page("Skill Gap Page", "GET", "/skill_gap")
test_page("Learning Goals Page", "GET", "/learning_goals")
test_page("Employee Progress Report", "GET", "/employee_progress")


# Employee-specific tests
conn = get_connection()
employee = conn.execute(
    "SELECT emp_id FROM employees LIMIT 1"
).fetchone()
conn.close()

if employee:
    emp_id = employee["emp_id"]

    test_page(
        "Employee Search Functionality",
        "POST",
        "/search_employee",
        {"search": emp_id}
    )

    test_page(
        "Skill Gap Functionality",
        "POST",
        "/skill_gap",
        {"emp_id": emp_id}
    )

    test_page(
        "Edit Employee Page",
        "GET",
        f"/edit_employee/{emp_id}"
    )
else:
    print("SKIP: No employee found")


# Final result
print("\n====================================")
print("          FINAL TEST RESULT")
print("====================================")
print("Total Passed:", passed)
print("Total Failed:", failed)

if failed == 0:
    print("\nALL TESTS PASSED SUCCESSFULLY!")
else:
    print("\nSOME TESTS FAILED. CHECK THE ERRORS.")

print("====================================")
