# skills/ — Databek skill catalog

Each folder is one skill: a `SKILL.md` contract plus templates/snippets the AI
uses. Every skill follows the same rhythm:

> **read [`../RULES.md`](../RULES.md) → read the skill's `SKILL.md` → write/edit
> the Frappe artifact → (if config changed) `export-fixtures` → append to
> `databek/CHANGELOG.md`.**

## Intent skills (what you type in Claude Code — `/name`)

These 4 are the ones you actually use. Each orchestrates the building-block
contracts below.

| Skill | Use it when… |
|-------|--------------|
| [build](build/SKILL.md) — `/build` | "I need a `<feature>`" → model + logic + UI + run, one pass |
| [manage-access](manage-access/SKILL.md) — `/manage-access` | roles/permissions: audit · risk-check · create/fix · explain "why can't X see Y" |
| [manage-ui](manage-ui/SKILL.md) — `/manage-ui` | inspect / edit / reorder / hide / remove existing menus, dashboards, reports |
| [manage-deploy](manage-deploy/SKILL.md) — `/manage-deploy` | docker: status · start/stop/restart · logs · apply changes · backup · health |

## Building-block contracts (used by the intent skills)

| Contract | Covers |
|----------|--------|
| [create-doctype](create-doctype/SKILL.md) | a new model/table/record type |
| [add-logic](add-logic/SKILL.md) | behavior/validation/API on a DocType |
| [customize-doctype](customize-doctype/SKILL.md) | extend an existing/core DocType (Custom Field / Property Setter) |
| [add-job](add-job/SKILL.md) | scheduled (cron) or async background work |
| [add-ui](add-ui/SKILL.md) | create menu / dashboard / report / KPI |
| [manage-permissions](manage-permissions/SKILL.md) | role + DocType permission mechanics |
| [export-fixtures](export-fixtures/SKILL.md) | freeze config records to `fixtures/*.json` |
| [install-app](install-app/SKILL.md) | install an external Frappe app from git |
| [run](run/SKILL.md) | bring the stack up / apply changes |
| [doctor](doctor/SKILL.md) | static health check of the whole app |

New skills follow [`SKILL.template.md`](SKILL.template.md).
