---
name: run
description: Bring the platform up (or apply changes) via Docker — docker compose up, then bench migrate + build + clear-cache + restart. Use when the user says "run", "start it", "deploy locally", or after any change that needs to go live.
---

# run

The "docker run" of the build loop. Brings the stack up and applies pending
artifact changes so they go live in the Desk UI. Idempotent.

## When to use

- Triggers: "run", "start it up", "bring it up", "apply", "make it live",
  and as the final step after any artifact change.
- Run `doctor` first if you want a pre-flight check.

## Reads (context)

- The docker stack at [`../../../../docker/`](../../../../docker/).

## Does

1. `docker compose up -d` (starts mariadb, redis, backend).
2. Inside the backend (via `entrypoint.sh` on first run, or explicitly on later
   runs): `bench migrate` → `bench build` → `bench clear-cache` → serve.

The first `up` also creates the empty site and installs `mason`. Later runs just
re-apply migrations/assets.

## Procedure

1. (Optional) run `doctor`.
2. From repo root: `cd docker && docker compose up -d`.
3. To apply changes to an already-running stack without a full restart:
   `skills/run/apply.sh` (runs migrate + build + clear-cache in the container).
4. Open <http://localhost:8080> and verify the change is live.
5. Append to `CHANGELOG.md`: *ran (migrate+build) · skill:run · rule:6*.

## Commands

```bash
cd docker && docker compose up -d          # start / first-run bootstrap
docker compose logs -f backend             # watch
# apply changes to a running stack:
docker compose exec backend bench --site mason.localhost migrate
docker compose exec backend bench build --app mason
docker compose exec backend bench --site mason.localhost clear-cache
```

## Invariants & prohibitions

- Never `docker compose down -v` (drops db + sites) unless the user explicitly
  asks to reset — it's destructive (RULES.md §4).
- Never installs ERPNext.

## Templates & snippets

- `apply.sh` — migrate + build + clear-cache against a running stack.
