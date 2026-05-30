# skills/ — Frappe AI skill catalog

Each folder is one skill: a `SKILL.md` contract plus templates/snippets the AI
uses. Every skill follows the same rhythm:

> **read [`../RULES.md`](../RULES.md) → read the skill's `SKILL.md` → write/edit
> the Frappe artifact → (if config changed) `export-fixtures` → append to
> `frappe_ai/CHANGELOG.md`.**

| Skill | Use it when… |
|-------|--------------|
| [create-doctype](create-doctype/SKILL.md) | a new model/table/record type is needed |
| [add-logic](add-logic/SKILL.md) | adding behavior/validation/API to a DocType |
| [customize-doctype](customize-doctype/SKILL.md) | extending an existing/core DocType (Custom Field / Property Setter) |
| [add-job](add-job/SKILL.md) | scheduled (cron) or async background work |
| [add-ui](add-ui/SKILL.md) | menu / dashboard / report / KPI from Frappe primitives |
| [manage-permissions](manage-permissions/SKILL.md) | roles & DocType permissions (default-deny) |
| [export-fixtures](export-fixtures/SKILL.md) | freeze config records to `fixtures/*.json` |
| [install-app](install-app/SKILL.md) | install an external Frappe app from git |
| [run](run/SKILL.md) | bring the stack up / apply changes (docker) |
| [doctor](doctor/SKILL.md) | pre-flight health check of the whole app |

New skills follow [`SKILL.template.md`](SKILL.template.md).
