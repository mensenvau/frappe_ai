---
name: customize-doctype
description: Add fields to or tweak properties of an EXISTING Frappe DocType (yours or core) without modifying core — via Custom Field and Property Setter, exported as fixtures. Use when the user wants to extend an existing model.
---

# customize-doctype

Read the full contract and snippets first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — never edit core; additive vs destructive (§4).
2. Read [`apps/frappe_ai/skills/customize-doctype/SKILL.md`](../../../apps/frappe_ai/skills/customize-doctype/SKILL.md).
3. Use the snippets in [`apps/frappe_ai/skills/customize-doctype/`](../../../apps/frappe_ai/skills/customize-doctype/) (`create_custom_field.py.snippet`, `property_setter.py.snippet`).
4. Ensure `module = "Frappe AI"` on the Custom Field / Property Setter.
5. Run `/export-fixtures`, append to `CHANGELOG.md`, then `/run`.

Destructive property changes → STOP and confirm with the user first.
