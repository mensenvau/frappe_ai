---
name: manage-access
description: Manage and reason about roles & permissions in frappe_ai — audit who can do what, flag risky/over-broad grants, create/fix roles and DocType permissions (default-deny), and explain why a user can or cannot see something. Use for any "role", "permission", "access", "who can…", "why can't X see…" request.
---

# manage-access

One skill for everything about access. It does four things:

1. **Audit** — report who (which role) can read/write/create/delete each DocType.
2. **Risk check** — flag over-broad grants (default-deny broken, System Manager
   handed out, public/guest access, write without need).
3. **Create / fix** — add roles, grant/revoke DocType permissions, freeze to fixtures.
4. **Explain** — answer "why can't user X see page Y?" with the concrete cause.

## Always read first

1. [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §5 default-deny.
2. [`apps/frappe_ai/skills/manage-permissions/SKILL.md`](../../../apps/frappe_ai/skills/manage-permissions/SKILL.md) — create/fix procedure + snippets.

## Audit & risk (read-only, run against the live site)

Use the helper, then summarize:

```bash
docker compose -f docker/docker-compose.yml exec -T backend \
  bench --site frappe_ai.localhost execute frappe_ai.frappe_ai.access_report.run
```
(Script: [`apps/frappe_ai/skills/manage-access/access_report.py`](../../../apps/frappe_ai/skills/manage-access/access_report.py) — copy it into the app package as `frappe_ai/access_report.py` the first time, then call it.)

Report a table: Role × DocType × (r/w/c/d). Then a **RISK** section flagging:
- any role with broad write/delete it doesn't need,
- `System Manager` granted to a non-admin role,
- DocTypes readable by `Guest`/`All`,
- DocTypes with NO permission rule (would be inaccessible) or open to everyone.

## Explain "why can't X see Y?"

Check, in order: is the user enabled? does the user have a role that has `read`
on DocType Y at the right permlevel? is there a User Permission / `if_owner`
restriction? Is Y hidden in the Workspace? State the exact blocking reason.

## Create / fix

Follow the manage-permissions contract: create Role, grant the **minimum**
permissions (in the app-owned DocType JSON, or as Custom DocPerm for core),
add the role to the `Role` fixtures filter in `hooks.py`, run `export-fixtures`,
then `/manage-deploy` to apply. Log to `CHANGELOG.md`.

## Rules

- Default-deny: never grant `System Manager` as a shortcut.
- Widening access on a core DocType, or anything that could expose data → STOP,
  confirm with the user first.
- Read-only audit never changes anything; only the create/fix path writes.
