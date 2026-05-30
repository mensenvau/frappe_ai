# ---------------------------------------------------------------------------
# Databek — app manifest (hooks.py)
# ---------------------------------------------------------------------------
# This is the single declarative manifest Frappe reads. Skills edit the marked
# sections only; everything outside the markers is app boilerplate.
#
#   doc_events       <- add-logic, create-doctype  (document lifecycle hooks)
#   scheduler_events <- add-job                     (cron / periodic jobs)
#   fixtures         <- export-fixtures             (what gets frozen to disk)
#
# Keep the markers intact so skills can locate their insertion points.
# ---------------------------------------------------------------------------

app_name = "databek"
app_title = "Databek"
app_publisher = "Databek"
app_description = "AI-extensible internal-tools platform on Frappe."
app_email = "noreply@databek.localhost"
app_license = "MIT"

# ---------------------------------------------------------------------------
# Document Events  (managed by: add-logic, create-doctype)
# ---------------------------------------------------------------------------
# Maps DocType -> {event: "dotted.path.to.handler"}.
# Example:
#   doc_events = {
#       "Task": {
#           "validate": "databek.<module>.doctype.task.task.validate",
#           "on_submit": "databek.<module>.doctype.task.task.on_submit",
#       }
#   }
# >>> DATABEK:doc_events:start
doc_events = {}
# <<< DATABEK:doc_events:end

# ---------------------------------------------------------------------------
# Scheduler Events  (managed by: add-job)
# ---------------------------------------------------------------------------
# Example:
#   scheduler_events = {
#       "daily": ["databek.<module>.tasks.cleanup"],
#       "cron": {"0 * * * *": ["databek.<module>.tasks.hourly_sync"]},
#   }
# >>> DATABEK:scheduler_events:start
scheduler_events = {}
# <<< DATABEK:scheduler_events:end

# ---------------------------------------------------------------------------
# Fixtures  (managed by: export-fixtures, manage-permissions, customize-doctype)
# ---------------------------------------------------------------------------
# Declares what `bench export-fixtures` freezes into databek/fixtures/*.json so
# the site is reproducible. Filter custom records to databek-owned ones to avoid
# dragging in unrelated core data.
# >>> DATABEK:fixtures:start
fixtures = [
    {"dt": "Role", "filters": [["name", "in", []]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Databek"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Databek"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Databek"]]},
    # Add {"dt": "<Custom DocType>"} entries as create-doctype adds modules.
]
# <<< DATABEK:fixtures:end
