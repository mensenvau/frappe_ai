---
name: doctor
description: Pre-flight health check of the whole databek app before a run — DocType JSON validity, controllers import, hooks markers intact, fixtures consistency, and migration dry-run. Use before run, or when something is broken and you need a diagnosis.
---

# doctor

A read-only diagnostic. Validates the app's artifacts so `run` doesn't fail
mid-migration. Produces a report; it does not change files.

## When to use

- Triggers: "check before run", "is it healthy?", "why is it broken?",
  "validate the app", or automatically before a `run` on a risky change.

## Reads (context)

- The whole `apps/databek/` tree.
- [`../../RULES.md`](../../RULES.md).

## Checks

1. **DocType JSON valid** — every `doctype/*/*.json` parses; has `name`,
   `module`, `fields`, at least one `permissions` entry (default-deny).
2. **Controllers import** — every `<name>.py` imports without error; class name
   = PascalCase of the DocType.
3. **Hooks intact** — `hooks.py` parses; the `# >>> DATABEK:*` marker pairs are
   present and balanced; `doc_events`/`scheduler_events` paths resolve.
4. **Fixtures consistent** — every `fixtures/*.json` parses; DocTypes referenced
   exist; `fixtures` list in hooks declares them.
5. **ERPNext absence** — confirm `erpnext` is not in apps / not imported
   (RULES.md §1).
6. **Migration dry-run** — `bench migrate` produces no errors (optionally
   against a scratch context).
7. **Scheduler** — if `scheduler_events` is non-empty, the scheduler is enabled.

## Procedure

1. Run `check.py` (static checks 1–5) — pure file inspection, safe anywhere.
2. Optionally run the bench checks (6–7) against the running container.
3. Emit a report: ✅ pass / ❌ fail per check, with file:line for failures.
4. Do NOT auto-fix — report and let the relevant skill fix it.

## Command

```bash
python skills/doctor/check.py apps/databek        # static checks (no bench needed)
docker compose exec backend bench --site databek.localhost migrate --dry-run  # opt.
```

## Invariants & prohibitions

- Read-only — never edits files or the DB.
- Reports every failure; never silently passes a degraded app.

## Templates & snippets

- `check.py` — static validator (JSON, controllers, hooks markers, fixtures, ERPNext).
