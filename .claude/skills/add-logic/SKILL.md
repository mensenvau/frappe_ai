---
name: add-logic
description: Add behavior to an existing Frappe DocType in frappe_ai — controller lifecycle methods (validate/before_save/on_submit), whitelisted API endpoints, or hooks.py doc_events. Use when the user asks to add a function, rule, calculation, validation, or automation to a model.
---

# add-logic

Read the full contract and snippets first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md).
2. Read [`apps/frappe_ai/skills/add-logic/SKILL.md`](../../../apps/frappe_ai/skills/add-logic/SKILL.md) — placement rules (controller vs whitelist vs doc_events), invariants.
3. Read the target module's `SKILL.md` to preserve its invariants.
4. Use the snippets in [`apps/frappe_ai/skills/add-logic/`](../../../apps/frappe_ai/skills/add-logic/) (`controller_methods.py.snippet`, `whitelist_api.py.snippet`, `doc_events.py.snippet`).
5. Edit the controller `.py` or `hooks.py` `doc_events` (keep the `# >>> FRAPPEAI:` markers intact).
6. Append a line to `CHANGELOG.md`, then `/run`.
