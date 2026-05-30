---
name: manage-ui
description: Inspect, edit, reorder, hide, or remove existing Frappe UI (Workspaces, charts, cards, reports, list views). The full contract behind the /manage-ui Claude skill.
---

# manage-ui (project contract)

Backs the `/manage-ui` Claude skill. The manage/edit/remove side of UI;
creation lives in [`../add-ui/`](../add-ui/). Frappe primitives only (RULES.md §8).

## Inspect (read-only)
List Frappe AI-owned UI records on the live site, or read the frozen JSON in
`apps/frappe_ai/frappe_ai/fixtures/` (`workspace.json`, `dashboard_chart.json`, …).

## Edit / reorder / hide
Records are editable on disk in `developer_mode`. Change a Workspace's
`shortcuts`/`links`/`charts` order, set `is_hidden`, rename labels, adjust chart
filters, or change List-view columns. Keep `module = "Frappe AI"`. Re-export
fixtures after.

## Remove (DESTRUCTIVE)
Deleting a Workspace/Chart/Report affects everyone → STOP, confirm, then delete
the record and remove it from fixtures.

## After any change
`export-fixtures` → apply (build + clear-cache) → refresh the Desk. Log to CHANGELOG.
