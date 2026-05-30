---
name: manage-permissions
description: Create roles and assign DocType permissions under a default-deny policy, then freeze them to fixtures. Use when the user wants a new role, to grant/restrict access, or to set who can read/write/create/delete a DocType.
---

# manage-permissions

Manages access control. Frappe is role-based: **Roles** are granted **Role
Permissions** on DocTypes. Frappe AI is default-deny — start from nothing and grant
the minimum (RULES.md §5).

## When to use

- Triggers: "add a role", "give X access to Y", "only managers can...",
  "restrict...", "who can edit...".

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- Existing `frappe_ai/fixtures/role.json` / `custom_docperm.json` to avoid clashes.

## Produces / edits

- A **Role** record (added to the `Role` fixtures filter in `hooks.py`).
- Role permissions on DocTypes — either in the DocType's own `permissions`
  (for app-owned DocTypes) or as **Custom DocPerm** records (for core/other).
- Adds the new role name to the `fixtures` `Role` filter `["name","in",[...]]`
  in `hooks.py`.

## Procedure

1. Read RULES.md. Default-deny: grant only what's asked.
2. Create the Role (see `create_role.py.snippet`).
3. Grant permissions:
   - App-owned DocType → edit its JSON `permissions` array.
   - Core/other DocType → create Custom DocPerm (see `role_permission.py.snippet`).
4. Add the role name to the `Role` fixtures filter in `hooks.py` between the
   `# >>> FRAPPEAI:fixtures` markers.
5. Run `export-fixtures`.
6. Append to `CHANGELOG.md`: *added role/permission <name> · skill:manage-permissions · rule:5*.

## Invariants & prohibitions

- Default-deny — never grant `System Manager` to satisfy a narrow need.
- Never widen core permissions silently; scope grants to the new role.
- Document the role's purpose in the changelog / module SKILL.md.

## Examples

See `create_role.py.snippet` and `role_permission.py.snippet`.

## Templates & snippets

- `create_role.py.snippet` — create a Role.
- `role_permission.py.snippet` — grant DocType permissions (JSON + Custom DocPerm).
