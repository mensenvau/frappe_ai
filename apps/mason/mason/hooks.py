# ---------------------------------------------------------------------------
# Mason — app manifest (hooks.py)
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

app_name = "mason"
app_title = "Mason"
app_publisher = "Mason"
app_description = "AI-extensible internal-tools platform on Frappe."
app_email = "noreply@mason.localhost"
app_license = "MIT"

# ---------------------------------------------------------------------------
# Document Events  (managed by: add-logic, create-doctype)
# ---------------------------------------------------------------------------
# Maps DocType -> {event: "dotted.path.to.handler"}.
# Example:
#   doc_events = {
#       "Task": {
#           "validate": "mason.<module>.doctype.task.task.validate",
#           "on_submit": "mason.<module>.doctype.task.task.on_submit",
#       }
#   }
# >>> MASON:doc_events:start
doc_events = {}
# <<< MASON:doc_events:end

# ---------------------------------------------------------------------------
# Scheduler Events  (managed by: add-job)
# ---------------------------------------------------------------------------
# Example:
#   scheduler_events = {
#       "daily": ["mason.<module>.tasks.cleanup"],
#       "cron": {"0 * * * *": ["mason.<module>.tasks.hourly_sync"]},
#   }
# >>> MASON:scheduler_events:start
scheduler_events = {}
# <<< MASON:scheduler_events:end

# ---------------------------------------------------------------------------
# Fixtures  (managed by: export-fixtures, manage-permissions, customize-doctype)
# ---------------------------------------------------------------------------
# Declares what `bench export-fixtures` freezes into mason/fixtures/*.json so
# the site is reproducible. Filter custom records to mason-owned ones to avoid
# dragging in unrelated core data.
# >>> MASON:fixtures:start
fixtures = [
    {"dt": "Role", "filters": [["name", "in", []]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Mason"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Mason"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Mason"]]},
    # Add {"dt": "<Custom DocType>"} entries as create-doctype adds modules.
]
# <<< MASON:fixtures:end
