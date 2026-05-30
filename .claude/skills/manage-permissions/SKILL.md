---
name: manage-permissions
description: Create roles and assign Frappe DocType permissions under a default-deny policy, then freeze to fixtures. Use when the user wants a new role, to grant/restrict access, or to set who can read/write/create/delete a DocType.
---

# manage-permissions

Read the full contract and snippets first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §5: default-deny, never grant System Manager as a shortcut.
2. Read [`apps/frappe_ai/skills/manage-permissions/SKILL.md`](../../../apps/frappe_ai/skills/manage-permissions/SKILL.md).
3. Use the snippets in [`apps/frappe_ai/skills/manage-permissions/`](../../../apps/frappe_ai/skills/manage-permissions/) (`create_role.py.snippet`, `role_permission.py.snippet`).
4. Add the new role to the `Role` fixtures filter in `hooks.py`.
5. Run `/export-fixtures`, append to `CHANGELOG.md`, then `/run`.
