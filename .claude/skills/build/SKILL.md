---
name: build
description: Build a complete feature in frappe_ai from one plain request — the data model, its business logic, AND the UI to use it, in one pass. Use when the user says "I need a <feature>", "add a <thing> with these fields", "make me a <X> that does <Y>". This is the main everyday skill.
---

# build

Turn one plain-language request into a working feature: **model → logic → UI →
freeze → run**, end to end. You decide which underlying artifacts are needed; the
user should not have to name DocTypes, controllers, or workspaces.

## When to use

- "I need a Project model with name, client, deadline, status."
- "Make me a way to track invoices and show overdue ones on a dashboard."
- "Add a leave-request feature where a manager approves."

If the request is purely about **access/roles** use `/manage-access`; purely
about **existing menus/dashboards** use `/manage-ui`; about **running/deploying**
use `/manage-deploy`.

## Always read first (this is how you "remember" across sessions)

1. [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — global law.
2. [`apps/frappe_ai/MODULES.md`](../../../apps/frappe_ai/MODULES.md) — the index
   of every module already built. **Read this first to know what exists.**
3. [`ARCHITECTURE.md`](../../../ARCHITECTURE.md) — the overall Databek plan +
   build phases, so a new feature lands in the right module.
4. The target module's `SKILL.md` if extending an existing module (found via
   MODULES.md).

## Procedure (do as much as the request needs, in order)

1. **Clarify only if blocking.** Infer sensible fields/types; ask only when a
   choice changes the schema materially.
2. **Model** — for each new model, follow
   [`apps/frappe_ai/skills/create-doctype/SKILL.md`](../../../apps/frappe_ai/skills/create-doctype/SKILL.md)
   and its templates. Write `apps/frappe_ai/frappe_ai/<module>/doctype/<name>/`.
3. **Logic** — validations, computed fields, state transitions, APIs: follow
   [`apps/frappe_ai/skills/add-logic/SKILL.md`](../../../apps/frappe_ai/skills/add-logic/SKILL.md).
4. **UI** — list/menu/dashboard/report so the feature is reachable: follow
   [`apps/frappe_ai/skills/add-ui/SKILL.md`](../../../apps/frappe_ai/skills/add-ui/SKILL.md).
5. **Access** — if the feature implies who-can-do-what, hand the role/permission
   part to `/manage-access` (or apply default-deny perms inline).
6. **Freeze** — `export-fixtures` for any config records
   ([contract](../../../apps/frappe_ai/skills/export-fixtures/SKILL.md)).
7. **Remember** — write/update the module's `SKILL.md` (use
   [`module.SKILL.template.md`](../../../apps/frappe_ai/skills/create-doctype/module.SKILL.template.md))
   AND add/update its row in
   [`apps/frappe_ai/MODULES.md`](../../../apps/frappe_ai/MODULES.md). This is what
   lets the next `/build` find and respect this module. **Do not skip this.**
8. **Run** — apply via `/manage-deploy` (migrate + build), then point the user to
   <http://localhost:8080>.
9. **Log** — append one line per artifact to `apps/frappe_ai/frappe_ai/CHANGELOG.md`.

## Rules

- Additive → just do it. Destructive (drop/rename field, change type) → STOP, ask.
- Never edit core Frappe; never install ERPNext.
- Finish the whole request in one pass; don't stop after only the model.
- End by telling the user exactly what was created and the URL to see it.
