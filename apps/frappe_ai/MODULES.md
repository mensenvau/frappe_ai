# Databek — Module Index

> **This is the memory.** Every module the AI builds is registered here, one line
> each, pointing at its `SKILL.md`. On the next `/build`, the AI reads THIS file
> first to learn what already exists, then reads the relevant module `SKILL.md`
> for full context. Keep it current: **when you build or change a module, update
> this index.**

| Module | Status | Domain | Contract |
|--------|--------|--------|----------|
| _(none built yet)_ | — | foundation only | — |

<!--
When a module is built, add a row like:
| crm | built | clients (individual/company) | [crm/SKILL.md](frappe_ai/crm/SKILL.md) |
| projects | built | projects per client + statuses | [projects/SKILL.md](frappe_ai/projects/SKILL.md) |
-->

## Planned modules (see [../ARCHITECTURE.md](../../ARCHITECTURE.md))

`crm` · `projects` · `hr` · `assignments` · `attendance` · `payroll` ·
`recruitment` · `learning` · `ai` · `notifications`

## How memory works (read this)

- **Intent skills never change.** `/build`, `/manage-access`, `/manage-ui`,
  `/manage-deploy` are universal — you do NOT create a new Claude skill per
  module. `/build` builds any module.
- **Each module carries its own `SKILL.md`** (domain, DocTypes, invariants,
  APIs, AI hooks, prohibitions). That file IS the AI's long-term memory of the
  module.
- **This `MODULES.md` is the directory of those memories.** It lets the AI find
  modules across sessions without scanning the whole tree.
- **The loop:** `/build` → reads `MODULES.md` → reads the target module's
  `SKILL.md` (if it exists) → writes/edits artifacts → writes/updates that
  module's `SKILL.md` → **adds/updates the row here** → logs to `CHANGELOG.md`.
