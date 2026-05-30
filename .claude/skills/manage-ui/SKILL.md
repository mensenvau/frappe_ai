---
name: manage-ui
description: Manage existing UI in frappe_ai — list/inspect, edit, reorder, hide, or remove Workspaces (menus), Dashboard Charts, Number Cards, Reports, and List-view settings. Use for "change the menu", "move/rename this card", "hide that report", "what's on the dashboard", "remove this from the menu". For brand-new UI, /build covers it.
---

# manage-ui

Manage UI that already exists (not just add). Inspect what's there, then
edit / reorder / hide / remove — using Frappe primitives only (RULES.md §8).

## When to use

- "What's on the Catalog workspace?" / "list the dashboards"
- "Rename this card", "move Widgets above Orders", "hide the old report"
- "Remove X from the menu", "change the list columns for Widget"

For creating brand-new UI from scratch, `/build` (or the add-ui contract) is fine
too — this skill is the manage/edit/remove side.

## Always read first

1. [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §8 primitives only.
2. [`apps/frappe_ai/skills/add-ui/SKILL.md`](../../../apps/frappe_ai/skills/add-ui/SKILL.md) — the UI primitives + templates.

## Inspect (read-only)

List Frappe AI-owned UI records on the live site:

```bash
docker compose -f docker/docker-compose.yml exec -T backend bash -lc '
  cd /home/frappe/bench-root/frappe-bench
  for dt in Workspace "Dashboard Chart" "Number Card" Report; do
    echo "== $dt =="; bench --site frappe_ai.localhost list-documents "$dt" 2>/dev/null || \
    bench --site frappe_ai.localhost execute frappe.client.get_list --kwargs "{\"doctype\":\"$dt\",\"filters\":{\"module\":\"Frappe AI\"},\"fields\":[\"name\"]}"
  done'
```

(Or read the frozen JSON in `apps/frappe_ai/frappe_ai/fixtures/workspace.json` etc.)

## Edit / reorder / hide

These live as records; in `developer_mode` they're editable on disk via fixtures.
Edit the workspace's `shortcuts` / `links` / `charts` order, set `is_hidden`,
rename labels, adjust a chart's filters, or change List-view columns. Keep
`module = "Frappe AI"`. Re-`export-fixtures` after.

## Remove (DESTRUCTIVE — confirm first)

Deleting a Workspace/Chart/Report removes it for everyone. STOP and confirm with
the user, then delete the record and remove it from fixtures.

## After any change

`export-fixtures` → `/manage-deploy` (build + clear-cache) → refresh
<http://localhost:8080>. Log to `CHANGELOG.md`.
