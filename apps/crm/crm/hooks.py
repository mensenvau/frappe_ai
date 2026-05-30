# ---------------------------------------------------------------------------
# crm — Databek CRM module app (clients: individual / company)
# ---------------------------------------------------------------------------
app_name = "crm"
app_title = "Databek CRM"
app_publisher = "Databek"
app_description = "Clients (individual or company) for Databek."
app_email = "noreply@databek.localhost"
app_license = "MIT"

after_install = "crm.crm.setup.install.after_install"

# >>> DATABEK:doc_events:start
doc_events = {}
# <<< DATABEK:doc_events:end

# >>> DATABEK:scheduler_events:start
scheduler_events = {}
# <<< DATABEK:scheduler_events:end

# >>> DATABEK:fixtures:start
fixtures = [
    {"dt": "Role", "filters": [["name", "in", ["Client"]]]},
    {"dt": "Workspace", "filters": [["module", "=", "CRM"]]},
]
# <<< DATABEK:fixtures:end
