# docker/ — Databek dev stack

Single-machine Frappe v15 stack. **No ERPNext.**

## Run

```bash
cd docker
docker compose up -d
docker compose logs -f backend     # watch first-run bootstrap (site creation)
```

Open <http://localhost:8080> → login `Administrator` / `admin`.

## Services

| Service       | Role                                   |
|---------------|----------------------------------------|
| `mariadb`     | Frappe database (MariaDB 10.6)         |
| `redis-cache` | Frappe cache                           |
| `redis-queue` | Frappe job queue + socketio            |
| `backend`     | Frappe bench (serves Desk on `:8000`)  |

The `databek` app at `../apps/databek` is **bind-mounted** into the bench, so edits
the AI makes on the host are immediately visible inside the container. Run the
`run` skill (or `docker compose restart backend`) to apply schema/asset changes.

## First run vs later runs

`scripts/entrypoint.sh` is idempotent:

- **First run** — inits the bench, creates the empty site, installs `databek`,
  sets `developer_mode=1`, migrates, builds, serves.
- **Later runs** — detects the existing site and just migrates + builds +
  clears cache, then serves.

## Reset everything

```bash
docker compose down -v   # also drops volumes (db + sites) — destructive
```
