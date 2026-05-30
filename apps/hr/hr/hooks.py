# ---------------------------------------------------------------------------
# hr — Databek HR module app (employees, levels, functional roles)
# ---------------------------------------------------------------------------
app_name = "hr"
app_title = "Databek HR"
app_publisher = "Databek"
app_description = "Employees, seniority levels, and functional roles for Databek."
app_email = "noreply@databek.localhost"
app_license = "MIT"

# Ensure Databek roles exist right after this app is installed.
after_install = "hr.hr.setup.install.after_install"

# >>> DATABEK:doc_events:start
doc_events = {}
# <<< DATABEK:doc_events:end

# >>> DATABEK:scheduler_events:start
scheduler_events = {}
# <<< DATABEK:scheduler_events:end

# >>> DATABEK:fixtures:start
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "HR", "Accountant", "Project Manager", "Recruiter",
        "Intern", "Engineer", "Manager",
    ]]]},
    {"dt": "Workspace", "filters": [["module", "=", "HR"]]},
]
# <<< DATABEK:fixtures:end
