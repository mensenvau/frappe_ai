# Frappe AI platform

An AI-extensible internal-tools platform on **Frappe Framework v15** — starting
from an empty foundation, with **no ERPNext**. You describe what you want; the AI
writes Frappe artifacts (DocType, controller, hooks, fixtures); you `docker run`;
it goes live in the Frappe Desk UI.

See [`FRAPPE_AI.md`](FRAPPE_AI.md) for the full build brief.

## Layout

```
docker/                  # Frappe v15 dev stack (compose + entrypoint)
apps/frappe_ai/              # the custom Frappe app (the empty foundation)
  RULES.md               # global law every skill obeys
  frappe_ai/                 # app package: hooks.py, modules.txt, fixtures/, SKILL.md
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

Tell the AI what you need. It picks a skill from [`apps/frappe_ai/skills/`](apps/frappe_ai/skills/),
writes the artifact, freezes config with `export-fixtures`, and you `run` to
apply. Every change is logged in [`apps/frappe_ai/frappe_ai/CHANGELOG.md`](apps/frappe_ai/frappe_ai/CHANGELOG.md).

The rules of the game live in [`apps/frappe_ai/RULES.md`](apps/frappe_ai/RULES.md):
Frappe-only, core never modified, default-deny permissions, destructive changes
require confirmation.
```
