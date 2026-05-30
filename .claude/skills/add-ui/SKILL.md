---
name: add-ui
description: Build UI in frappe_ai from Frappe primitives only — Workspace (menu/cards/shortcuts), Dashboard Chart, Number Card, Report (Query/Script), List view settings. Use when the user wants a menu entry, dashboard, report, or to surface data. No freehand frontend.
---

# add-ui

Read the full contract and templates first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §8: Frappe primitives only, no bespoke frontend.
2. Read [`apps/frappe_ai/skills/add-ui/SKILL.md`](../../../apps/frappe_ai/skills/add-ui/SKILL.md).
3. Use the templates/snippets in [`apps/frappe_ai/skills/add-ui/`](../../../apps/frappe_ai/skills/add-ui/) (`workspace.json.template`, `dashboard_chart.json.template`, `number_card.json.template`, `query_report.sql.snippet`, `script_report.py.snippet`).
4. Create records with `module = "Frappe AI"`.
5. Run `/export-fixtures`, append to `CHANGELOG.md`, then `/run`.
