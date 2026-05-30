---
name: build
description: Turn one plain request into a complete feature — model + logic + UI + freeze + run. The full contract behind the /build Claude skill.
---

# build (project contract)

Backs the `/build` Claude skill. One request → a working feature, end to end.
You orchestrate the existing per-artifact contracts; the user names a goal, not
DocTypes.

## Read first (memory)
`../../RULES.md` → `../../MODULES.md` (index of built modules) →
`../../../ARCHITECTURE.md` (plan) → target module `SKILL.md` if it exists.

## Pipeline (do what the request needs, in order)

1. **Model** → [`../create-doctype/`](../create-doctype/) (schema + controller).
2. **Logic** → [`../add-logic/`](../add-logic/) (validation, computed fields,
   state, APIs).
3. **UI** → [`../add-ui/`](../add-ui/) (list/menu/dashboard/report so it's reachable).
4. **Access** → hand to [`../manage-access/`](../manage-access/) if the feature
   implies who-can-do-what (else default-deny inline).
5. **Freeze** → [`../export-fixtures/`](../export-fixtures/).
6. **Remember** → write/update `<module>/SKILL.md` (from
   [`../create-doctype/module.SKILL.template.md`](../create-doctype/module.SKILL.template.md))
   and add/update its row in [`../../MODULES.md`](../../MODULES.md). Never skip.
7. **Run** → [`../run/`](../run/) (migrate + build).
8. **Log** → one CHANGELOG line per artifact.

## Principles
- Infer sensible fields/types; ask only when a choice changes the schema.
- Finish the whole request in one pass — don't stop after just the model.
- Additive → do it; destructive → STOP and confirm.
- Never edit core Frappe; never install ERPNext.
- End by telling the user what was created + the URL to see it.
