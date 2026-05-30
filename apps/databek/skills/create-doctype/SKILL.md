---
name: create-doctype
description: Create a new Frappe DocType (data model) inside a databek module — JSON schema + Python controller + optional client script + a SKILL.md stub. Use when the user asks for a new model, table, record type, or "doc".
---

# create-doctype

Creates a new DocType: the schema file Frappe reads to generate the table, list
view, form UI, REST API, and permission surface. This is the most common skill —
every business module starts here.

## When to use

- Triggers: "I need an X model", "make a Y record/table", "create a doctype for Z".
- Use this for a **new** DocType. To add fields to an **existing** one (yours or
  core), use `customize-doctype`. To add behavior, use `add-logic`.

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- [`../../databek/SKILL.md`](../../databek/SKILL.md) — app layout.
- [`../../databek/modules.txt`](../../databek/modules.txt) — existing modules.
- The SKILL.md of any related/linked module.

## Produces / edits

- `databek/<module>/doctype/<name>/<name>.json` — schema (from `doctype.json.template`).
- `databek/<module>/doctype/<name>/<name>.py` — controller (from `controller.py.template`).
- `databek/<module>/doctype/<name>/<name>.js` — optional client script (from `client.js.template`).
- `databek/<module>/doctype/<name>/__init__.py`, `databek/<module>/doctype/__init__.py`,
  `databek/<module>/__init__.py` — empty package files if the module is new.
- `databek/<module>/SKILL.md` — module contract stub (from `module.SKILL.template.md`) if new.
- `databek/modules.txt` — add the module label if new.

## Procedure

1. Read RULES.md + app SKILL.md. Decide the module (snake_case) and DocType name.
2. Copy `doctype.json.template`; fill `name`, `module`, `fields`, `permissions`.
   - Snake_case the folder; PascalCase nothing in the file except nothing — JSON
     uses the human name in `"name"`.
   - Set `"custom": 0` (app-owned), `"issingle"`/`"istable"` as needed.
   - Permissions: default-deny — grant the minimum role(s) only (RULES.md §5).
3. Copy `controller.py.template`; rename class to PascalCase of the DocType.
   Leave lifecycle methods as no-ops unless behavior was requested (that's
   `add-logic`).
4. Create the `__init__.py` package files and, if the module is new, the module
   `SKILL.md` stub + add to `modules.txt`.
5. If the DocType should be reproducible, add `{"dt": "<Name>"}` to `fixtures`
   in `hooks.py` (between the markers), then run `export-fixtures`.
6. Append to `CHANGELOG.md`: *created DocType <Name> · skill:create-doctype · rule:1,2,5*.

## Invariants & prohibitions

- `"custom": 0` for app-owned DocTypes (they ship as files, not data).
- Every DocType has at least one permission rule; never default to open.
- Folder name = snake_case of DocType name; controller class = PascalCase.
- Do not add business logic here — only the schema + empty controller.

## Examples

A minimal DocType "Widget" in module `catalog`:

```
databek/catalog/doctype/widget/widget.json   # name:"Widget", module:"Catalog"
databek/catalog/doctype/widget/widget.py     # class Widget(Document): pass
```

## Templates & snippets

- `doctype.json.template` — DocType schema scaffold.
- `controller.py.template` — Python controller scaffold.
- `client.js.template` — optional client-side form script.
- `module.SKILL.template.md` — per-module AI contract stub.
