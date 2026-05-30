---
name: add-logic
description: Add behavior to an existing DocType — controller lifecycle methods (validate/before_save/on_submit), whitelisted API endpoints, or hooks.py doc_events. Use when the user asks to add a function, rule, calculation, validation, or automation to a model.
---

# add-logic

Adds Python behavior to an existing DocType. Three places, in order of
preference:

1. **Controller methods** in `<name>.py` — for logic owned by that DocType.
2. **Whitelisted API** (`@frappe.whitelist()`) — for actions called from JS/HTTP.
3. **`hooks.py` `doc_events`** — for cross-DocType reactions or logic on core
   DocTypes you don't own.

## When to use

- Triggers: "add a function", "validate that...", "when X is saved do Y",
  "compute Z", "expose an endpoint".
- Use `create-doctype` first if the DocType doesn't exist. Use `add-job` for
  scheduled/background work.

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- The target `databek/<module>/doctype/<name>/<name>.py`.
- The module `SKILL.md` (invariants you must preserve).
- [`../../databek/hooks.py`](../../databek/hooks.py) if using `doc_events`.

## Produces / edits

- Edits the target controller `.py` (lifecycle methods / whitelisted funcs).
- OR edits `hooks.py` `doc_events` between the `# >>> DATABEK:doc_events` markers.
- Optionally a `.js` client script to call a new endpoint.

## Procedure

1. Read RULES.md + the module SKILL.md to learn invariants.
2. Decide placement (controller method vs whitelisted API vs doc_events).
3. Implement. For validation, `frappe.throw(_("message"))` on failure.
4. For APIs: add `@frappe.whitelist()`, check permissions explicitly, never
   trust client input for the acting user.
5. For `doc_events`: add `"DocType": {"event": "databek.<...>.handler"}` between
   the markers; implement the handler.
6. Append to `CHANGELOG.md`: *added logic to <Name> · skill:add-logic · rule:1,2*.

## Invariants & prohibitions

- Never bypass permissions in whitelisted methods — call
  `frappe.has_permission(...)` or `doc.check_permission(...)`.
- Never modify core Frappe controllers; react via `doc_events` instead.
- Preserve module invariants documented in its SKILL.md.
- Raise via `frappe.throw` (localized) for user-facing failures.

## Examples

See `controller_methods.py.snippet`, `whitelist_api.py.snippet`,
`doc_events.py.snippet`.

## Templates & snippets

- `controller_methods.py.snippet` — validate / before_save / on_submit patterns.
- `whitelist_api.py.snippet` — a permission-checked API endpoint.
- `doc_events.py.snippet` — hooks.py wiring + handler.
