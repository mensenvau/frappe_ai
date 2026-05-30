---
name: manage-deploy
description: Operate the dockerized Frappe AI stack — status, start/stop/restart, logs, apply changes, backup/restore, health check. The full contract behind the /manage-deploy Claude skill.
---

# manage-deploy (project contract)

Backs the `/manage-deploy` Claude skill. Operates the stack defined in
[`../../../docker/`](../../../docker/). Wraps [`../run/`](../run/) (apply) and
[`../doctor/`](../doctor/) (health).

## Intents → commands
- **status** → `docker compose -f docker/docker-compose.yml ps`
- **start** → `docker compose -f docker/docker-compose.yml up -d` (first run slow, once)
- **logs** → `docker compose -f docker/docker-compose.yml logs backend --tail 80`
- **apply** → `apps/frappe_ai/skills/run/apply.sh` (migrate + build + clear-cache)
- **stop** → `docker compose -f docker/docker-compose.yml stop` (keeps data)
- **health** → `python apps/frappe_ai/skills/doctor/check.py apps/frappe_ai`
- **backup** → `... exec -T backend bench --site frappe_ai.localhost backup --with-files`

## Pre-flight
Run `doctor` before `apply` so a bad artifact fails fast.

## Prohibitions (DESTRUCTIVE — confirm first)
- `docker compose down -v` drops db + all sites — only on explicit user request.
- `drop-site` / `restore` over a live site — confirm first.
- Docker Desktop's Linux engine must be running first (user starts it by hand).
