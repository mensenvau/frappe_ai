---
name: manage-access
description: Audit, risk-check, create/fix, and explain roles & permissions in frappe_ai. The full contract behind the /manage-access Claude skill.
---

# manage-access (project contract)

Backs the `/manage-access` Claude skill. Four capabilities over one domain —
access control — all default-deny (RULES.md §5).

## 1. Audit (read-only)
Install the report once, then run it:
```bash
cp apps/frappe_ai/skills/manage-access/access_report.py \
   apps/frappe_ai/frappe_ai/frappe_ai/access_report.py
docker compose -f docker/docker-compose.yml exec -T backend \
  bench --site frappe_ai.localhost execute frappe_ai.frappe_ai.access_report.run
```
It prints a Role × DocType matrix (`RWCDSC` flags) and a RISK section.

## 2. Risk check
The report flags: Guest/All access, delete granted to non-admin roles, and app
DocTypes with no permission rule. Summarize these for the user and propose fixes.

## 3. Create / fix
Reuse the create/fix procedure + snippets in
[`../manage-permissions/`](../manage-permissions/): create Role, grant the
minimum perms (app DocType JSON, or Custom DocPerm for core), add the role to the
`Role` fixtures filter in `hooks.py`, `export-fixtures`, then apply.

## 4. Explain "why can't X see Y?"
Check in order: user enabled → has a role with `read` on Y at the right permlevel
→ no User Permission / `if_owner` block → Y visible in the Workspace. Name the
exact blocking reason.

## Prohibitions
- Default-deny; never grant System Manager as a shortcut.
- Any widening of access that could expose data → STOP, confirm first.
- The audit path is strictly read-only.
