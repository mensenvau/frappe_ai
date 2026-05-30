# ---------------------------------------------------------------------------
# Frappe AI — app manifest (hooks.py)
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

app_name = "frappe_ai"
app_title = "Frappe AI"
app_publisher = "Frappe AI"
app_description = "AI-extensible internal-tools platform on Frappe."
app_email = "noreply@frappe_ai.localhost"
app_license = "MIT"

# ---------------------------------------------------------------------------
# Document Events  (managed by: add-logic, create-doctype)
# ---------------------------------------------------------------------------
# Maps DocType -> {event: "dotted.path.to.handler"}.
# Example:
#   doc_events = {
#       "Task": {
#           "validate": "frappe_ai.<module>.doctype.task.task.validate",
#           "on_submit": "frappe_ai.<module>.doctype.task.task.on_submit",
#       }
#   }
# >>> FRAPPEAI:doc_events:start
doc_events = {}
# <<< FRAPPEAI:doc_events:end

# ---------------------------------------------------------------------------
# Scheduler Events  (managed by: add-job)
# ---------------------------------------------------------------------------
# Example:
#   scheduler_events = {
#       "daily": ["frappe_ai.<module>.tasks.cleanup"],
#       "cron": {"0 * * * *": ["frappe_ai.<module>.tasks.hourly_sync"]},
#   }
# >>> FRAPPEAI:scheduler_events:start
scheduler_events = {}
# <<< FRAPPEAI:scheduler_events:end

# ---------------------------------------------------------------------------
# Fixtures  (managed by: export-fixtures, manage-permissions, customize-doctype)
# ---------------------------------------------------------------------------
# Declares what `bench export-fixtures` freezes into frappe_ai/fixtures/*.json so
# the site is reproducible. Filter custom records to frappe_ai-owned ones to avoid
# dragging in unrelated core data.
# >>> FRAPPEAI:fixtures:start
fixtures = [
    {"dt": "Role", "filters": [["name", "in", []]]},
    {"dt": "Custom Field", "filters": [["module", "=", "Frappe AI"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Frappe AI"]]},
    {"dt": "Workspace", "filters": [["module", "=", "Frappe AI"]]},
    # Add {"dt": "<Custom DocType>"} entries as create-doctype adds modules.
]
# <<< FRAPPEAI:fixtures:end
