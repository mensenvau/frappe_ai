---
name: frappe_ai
description: App-level AI contract for the Frappe AI platform. Read this after RULES.md to understand the app's shape, the build loop, and where artifacts live before invoking any skill.
---

# Frappe AI — app-level contract

Frappe AI is an empty, AI-extensible internal-tools platform on **Frappe v15**
(no ERPNext). You extend it by writing Frappe artifacts that Frappe turns into
live UI, API, permissions, and menus — you never build the engine.

## Read order (every task)

1. [`../RULES.md`](../RULES.md) — global law.
2. This file — app shape.
3. The relevant `skills/<skill>/SKILL.md`.
4. The target module's `SKILL.md` (if editing an existing module).

## Where things live

| Artifact            | Path                                                        |
|---------------------|-------------------------------------------------------------|
| App manifest        | `frappe_ai/hooks.py` (markers per section)                       |
| Modules list        | `frappe_ai/modules.txt`                                          |
| DocType             | `frappe_ai/<module>/doctype/<name>/<name>.json` + `.py` (+`.js`) |
| Fixtures (frozen)   | `frappe_ai/fixtures/*.json`                                      |
| Changelog           | `frappe_ai/CHANGELOG.md`                                         |
| Module AI contract  | `frappe_ai/<module>/SKILL.md`                                    |

## The build loop

1. User states intent.
2. Pick the matching skill in [`../skills/`](../skills/).
3. Write/edit the Frappe artifact per that skill.
4. `export-fixtures` (if config changed).
5. `run` → `bench migrate` + `bench build` + `clear-cache` + restart.
6. Append a line to `CHANGELOG.md`.

## Invariants

- `developer_mode=1` is always on in dev (artifacts must land on disk).
- ERPNext is never a dependency.
- Core Frappe is never edited; extend via Custom Field / Property Setter / new
  DocType only.
- Destructive changes require explicit user confirmation (RULES.md §4).

## Skill index

`create-doctype` · `add-logic` · `customize-doctype` · `add-job` · `add-ui` ·
`manage-permissions` · `export-fixtures` · `install-app` · `run` · `doctor`

See [`../skills/`](../skills/) for each contract.
