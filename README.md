# Mason platform

An AI-extensible internal-tools platform on **Frappe Framework v15** — starting
from an empty foundation, with **no ERPNext**. You describe what you want; the AI
writes Frappe artifacts (DocType, controller, hooks, fixtures); you `docker run`;
it goes live in the Frappe Desk UI.

See [`MASON.md`](MASON.md) for the full build brief.

## Layout

```
docker/                  # Frappe v15 dev stack (compose + entrypoint)
apps/mason/              # the custom Frappe app (the empty foundation)
  RULES.md               # global law every skill obeys
  mason/                 # app package: hooks.py, modules.txt, fixtures/, SKILL.md
  skills/                # the 10 skills: SKILL.md + templates/snippets
MASON.md                 # the build brief
```

## Quick start

```bash
cd docker
docker compose up -d
docker compose logs -f backend     # watch first-run site creation
```

Open <http://localhost:8080> → `Administrator` / `admin` → empty Desk.

## How it grows

Tell the AI what you need. It picks a skill from [`apps/mason/skills/`](apps/mason/skills/),
writes the artifact, freezes config with `export-fixtures`, and you `run` to
apply. Every change is logged in [`apps/mason/mason/CHANGELOG.md`](apps/mason/mason/CHANGELOG.md).

The rules of the game live in [`apps/mason/RULES.md`](apps/mason/RULES.md):
Frappe-only, core never modified, default-deny permissions, destructive changes
require confirmation.
```
