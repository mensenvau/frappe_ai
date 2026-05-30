---
name: customize-doctype
description: Add fields to or tweak the properties of an EXISTING DocType (yours or a core Frappe one) without modifying core — via Custom Field and Property Setter, exported as fixtures. Use when the user wants to extend an existing model.
---

# customize-doctype

Extends an existing DocType non-destructively. This is the **only** sanctioned
way to touch a core Frappe DocType (User, ToDo, File, …) — never edit core JSON.

- **Custom Field** — adds a new field to an existing DocType.
- **Property Setter** — overrides a property of an existing field/DocType
  (label, reqd, options, hidden, default, …).

Both are data records; they are made reproducible by exporting to fixtures.

## When to use

- Triggers: "add a field to <existing DocType>", "make <field> required",
  "add a column to User", "change the label of...".
- For a **new** DocType use `create-doctype`. For **behavior** use `add-logic`.

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- The target DocType (your JSON, or core via `bench` introspection).

## Produces / edits

- A **Custom Field** record (module = `Mason`).
- And/or a **Property Setter** record (module = `Mason`).
- These are exported to `mason/fixtures/custom_field.json` /
  `property_setter.json` via `export-fixtures`.

## Procedure

1. Read RULES.md. Confirm the field/property is **additive** (RULES.md §4).
   Changing a fieldtype or making an existing optional field required can break
   data → STOP and confirm first.
2. Create the Custom Field / Property Setter. Two ways:
   - Programmatically (preferred, reproducible): see
     `create_custom_field.py.snippet`.
   - Via Desk "Customize Form" (still lands on disk in developer_mode).
3. Ensure `module = "Mason"` so fixtures filters pick it up.
4. Run `export-fixtures`.
5. Append to `CHANGELOG.md`: *customized <DocType> · skill:customize-doctype · rule:2,3*.

## Invariants & prohibitions

- Never edit core DocType JSON or core controllers (RULES.md §2).
- Custom Fields/Property Setters must carry `module = "Mason"`.
- Destructive property changes (reqd on populated data, fieldtype change,
  removing options) → confirm first (RULES.md §4).

## Examples

See `create_custom_field.py.snippet` and `property_setter.py.snippet`.

## Templates & snippets

- `create_custom_field.py.snippet` — add a Custom Field via API.
- `property_setter.py.snippet` — override a field/DocType property.
