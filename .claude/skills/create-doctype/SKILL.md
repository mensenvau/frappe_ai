---
name: create-doctype
description: Create a new Frappe DocType (data model) in the frappe_ai app — JSON schema + Python controller + optional client script + module SKILL.md stub. Use when the user asks for a new model, table, record type, or "doc".
---

# create-doctype

Read the full contract and templates first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — global law.
2. Read [`apps/frappe_ai/skills/create-doctype/SKILL.md`](../../../apps/frappe_ai/skills/create-doctype/SKILL.md) — full procedure, invariants, examples.
3. Use the templates in [`apps/frappe_ai/skills/create-doctype/`](../../../apps/frappe_ai/skills/create-doctype/) (`doctype.json.template`, `controller.py.template`, `client.js.template`, `module.SKILL.template.md`).
4. Write the artifact under `apps/frappe_ai/frappe_ai/<module>/doctype/<name>/`.
5. If reproducible, add to `fixtures` in `hooks.py` and run `/export-fixtures`.
6. Append one line to `apps/frappe_ai/frappe_ai/CHANGELOG.md`.

Then apply with `/run`. Validate with `/doctor`.
