---
name: manage-deploy
description: Manage the Databek Docker deployment — start/stop/restart the stack, view status & logs, apply changes (migrate + build + clear-cache), back up / restore the site, and run a health check. Use for "run it", "start/stop", "restart", "show logs", "status", "apply my changes", "backup", "is it healthy?".
---

# manage-deploy

One skill to operate the dockerized stack. All commands assume repo root and the
compose file at `docker/docker-compose.yml`.

## Always read first

1. [`apps/databek/skills/run/SKILL.md`](../../../apps/databek/skills/run/SKILL.md) — the run contract.
2. [`apps/databek/skills/doctor/SKILL.md`](../../../apps/databek/skills/doctor/SKILL.md) — health check.

## Commands by intent

**Status**
```bash
docker compose -f docker/docker-compose.yml ps
```

**Start / first-run bootstrap** (first run is slow ~10 min: clones Frappe + venv once)
```bash
docker compose -f docker/docker-compose.yml up -d
docker compose -f docker/docker-compose.yml logs -f backend   # wait for "Databek is up"
```

**Logs**
```bash
docker compose -f docker/docker-compose.yml logs backend --tail 80
```

**Apply changes** (after editing artifacts — migrate + build + clear-cache, no full restart)
```bash
apps/databek/skills/run/apply.sh
# or:
docker compose -f docker/docker-compose.yml restart backend
```

**Stop** (keeps data)
```bash
docker compose -f docker/docker-compose.yml stop
```

**Health check** (static, no bench needed)
```bash
python apps/databek/skills/doctor/check.py apps/databek
```

**Backup the site**
```bash
docker compose -f docker/docker-compose.yml exec -T backend \
  bench --site databek.localhost backup --with-files
```

## Pre-flight

Before applying changes, run the health check (`doctor`) so a bad artifact fails
fast instead of mid-migration. Report ✅/❌ to the user.

## Rules (DESTRUCTIVE — STOP and confirm first)

- `docker compose down -v` — **drops the database and all sites**. Never run
  unless the user explicitly asks to wipe everything.
- `bench drop-site` / `restore` over a live site — confirm first.
- Engine note: Docker Desktop's Linux engine must be running first
  (`docker info` should succeed); the user starts it by hand.

Log notable deploy actions (apply, backup, reset) to `CHANGELOG.md`.
