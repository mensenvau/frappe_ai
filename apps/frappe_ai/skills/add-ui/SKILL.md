---
name: add-ui
description: Build UI from Frappe primitives only — Workspace (menu/cards/shortcuts), Dashboard Chart, Number Card, Report (Query/Script), and List view settings. Use when the user wants a menu entry, dashboard, report, or to surface data. No freehand frontend.
---

# add-ui

Surfaces data and navigation using Frappe's built-in UI primitives. Per
RULES.md §8 there is **no bespoke React/HTML** — you compose Desk objects, and
Frappe renders them.

Primitives:

- **Workspace** — the left-nav page: shortcuts, cards (links), charts.
- **Dashboard Chart** — time-series / aggregate chart bound to a DocType.
- **Number Card** — a single KPI tile.
- **Report** — Query Report (SQL) or Script Report (Python) for tabular output.
- **List view settings** — columns, filters, sort on a DocType's list.

## When to use

- Triggers: "add to the menu", "make a dashboard", "I want a report",
  "show a chart of...", "add a KPI", "put X on the homepage".

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- Existing `frappe_ai/fixtures/workspace.json` (if any) to extend rather than clash.
- The DocType(s) being surfaced.

## Produces / edits

- A **Workspace** record (module `Frappe AI`) — from `workspace.json.template`.
- A **Dashboard Chart** / **Number Card** record (module `Frappe AI`).
- A **Report** — `frappe_ai/<module>/report/<name>/` (Query/Script) or a Report record.
- List view tweaks via `<name>_list.js` or Property Setters.
- All exported via `export-fixtures`.

## Procedure

1. Read RULES.md. Pick the primitive that fits the ask.
2. Create the record(s) with `module = "Frappe AI"`.
3. For a Query Report, write SQL referencing the DocType's table
   (`tab<DocType>`); for a Script Report, write `execute()` returning
   `(columns, data)`.
4. Add shortcuts/cards to a Workspace so it's reachable.
5. Run `export-fixtures`.
6. Append to `CHANGELOG.md`: *added UI <name> · skill:add-ui · rule:8*.

## Invariants & prohibitions

- No custom frontend frameworks; Frappe primitives only (RULES.md §8).
- Records carry `module = "Frappe AI"`.
- Reports respect DocType permissions (don't leak rows via raw SQL — filter by
  permitted users or use `frappe.get_list`).

## Examples

See `workspace.json.template`, `dashboard_chart.json.template`,
`number_card.json.template`, `query_report.sql.snippet`, `script_report.py.snippet`.

## Templates & snippets

- `workspace.json.template` — Workspace with shortcut + card + chart slots.
- `dashboard_chart.json.template` — a chart bound to a DocType.
- `number_card.json.template` — a KPI tile.
- `query_report.sql.snippet` — Query Report SQL pattern.
- `script_report.py.snippet` — Script Report execute() pattern.
