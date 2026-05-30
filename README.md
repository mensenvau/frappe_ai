# Databek platform

An AI-extensible internal-tools platform on **Frappe Framework v15** — starting
from an empty foundation, with **no ERPNext**. You describe what you want; the AI
writes Frappe artifacts (DocType, controller, hooks, fixtures); you `docker run`;
it goes live in the Frappe Desk UI.

See [`FRAPPE_AI.md`](FRAPPE_AI.md) for the full build brief.

## Layout

```
docker/                  # Frappe v15 dev stack (compose + entrypoint)
apps/databek/              # the custom Frappe app (the empty foundation)
  RULES.md               # global law every skill obeys
  databek/                 # app package: hooks.py, modules.txt, fixtures/, SKILL.md
  skills/                # the 10 skills: SKILL.md + templates/snippets
FRAPPE_AI.md                 # the build brief
```

## Quick start

```bash
cd docker
docker compose up -d
docker compose logs -f backend     # watch first-run site creation
```

Open <http://localhost:8080> → `Administrator` / `admin` → empty Desk.

## How it grows

Tell the AI what you need, using one of the 4 Claude Code skills:

- **`/build`** — "I need a `<feature>`" → model + logic + UI, one pass.
- **`/manage-access`** — roles & permissions: audit, risk-check, create/fix, explain.
- **`/manage-ui`** — inspect / edit / reorder / hide / remove menus, dashboards, reports.
- **`/manage-deploy`** — docker: status, start/stop/restart, logs, apply, backup, health.

Under the hood these orchestrate the building-block contracts in
[`apps/databek/skills/`](apps/databek/skills/) (create-doctype, add-logic,
add-ui, export-fixtures, run, doctor, …). Every change is logged in
[`apps/databek/databek/CHANGELOG.md`](apps/databek/databek/CHANGELOG.md).

The rules of the game live in [`apps/databek/RULES.md`](apps/databek/RULES.md):
Frappe-only, core never modified, default-deny permissions, destructive changes
require confirmation.
```
