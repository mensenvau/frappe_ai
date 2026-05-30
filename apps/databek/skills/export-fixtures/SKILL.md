---
name: export-fixtures
description: Freeze config records (roles, custom fields, property setters, workspaces, custom doctypes) to databek/fixtures/*.json so the site is reproducible. Run after any change that creates config data records. Driven by the fixtures list in hooks.py.
---

# export-fixtures

Freezes data-shaped configuration into version-controlled JSON. Schema-shaped
artifacts (DocType JSON, controllers) already live on disk thanks to
`developer_mode=1`; **fixtures cover the records** (Role, Custom Field, Property
Setter, Workspace, Dashboard Chart, etc.) that otherwise live only in the DB.

This is the reproducibility backbone (RULES.md §3): on a fresh site,
`bench migrate` re-imports fixtures so the platform rebuilds identically.

## When to use

- After: `manage-permissions`, `customize-doctype`, `add-ui`, and any
  `create-doctype` that adds a record-style DocType to the fixtures list.
- Triggers (internal): "freeze config", "make this reproducible", end of a
  build-loop step.

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- [`../../databek/hooks.py`](../../databek/hooks.py) — the `fixtures` list decides
  what gets exported.

## Produces / edits

- `databek/fixtures/*.json` — one file per fixture DocType
  (`role.json`, `custom_field.json`, `property_setter.json`, `workspace.json`, …).

## Procedure

1. Read RULES.md and the `fixtures` list in `hooks.py` (between the markers).
   Make sure the new record's DocType + filter is declared there.
2. Run the export (see `run.sh` / the command below).
3. Review the diff — fixtures should contain only Databek-owned records (filters
   keep core data out).
4. Append to `CHANGELOG.md`: *exported fixtures · skill:export-fixtures · rule:3*.

## Command

```bash
# inside the bench (or: docker compose exec backend ...)
bench --site databek.localhost export-fixtures --app databek
```

`run.sh` wraps this for the dockerized stack.

## Invariants & prohibitions

- Only Databek-owned records — keep filters (`module = "Databek"`, name lists)
  tight so unrelated core data is never committed.
- Never hand-edit exported JSON to inject data that wasn't created on a site;
  create it properly, then re-export.

## Templates & snippets

- `run.sh` — runs export-fixtures against the dockerized site.
