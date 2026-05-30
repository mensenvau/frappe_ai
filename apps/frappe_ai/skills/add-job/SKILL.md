---
name: add-job
description: Add background work — a scheduled (cron/periodic) job via hooks.py scheduler_events, or an async task via frappe.enqueue. Use when the user wants something to run on a schedule or off the request thread.
---

# add-job

Adds background processing. Two kinds:

- **Scheduled** — runs periodically via the Frappe scheduler. Declared in
  `hooks.py` `scheduler_events` (`hourly`/`daily`/`weekly`/`cron`).
- **Async / enqueued** — runs once, off the web request, via
  `frappe.enqueue(...)` (e.g. heavy work triggered from a controller).

## When to use

- Triggers: "every night...", "run a cron", "process this in the background",
  "send a daily digest", "do X asynchronously".

## Reads (context)

- [`../../RULES.md`](../../RULES.md)
- [`../../frappe_ai/hooks.py`](../../frappe_ai/hooks.py) — `scheduler_events` markers.

## Produces / edits

- `hooks.py` `scheduler_events` between the `# >>> FRAPPEAI:scheduler_events` markers.
- A task function in `frappe_ai/<module>/tasks.py`.
- (Async) a `frappe.enqueue(...)` call inside a controller/API.

## Procedure

1. Read RULES.md.
2. Implement the task function in `frappe_ai/<module>/tasks.py`.
3. **Scheduled:** add it to `scheduler_events` between the markers
   (`hourly`/`daily`/`weekly`/`monthly`, or `cron` with a crontab string).
4. **Async:** call `frappe.enqueue("frappe_ai.<module>.tasks.fn", **kwargs)` from
   the trigger point; choose a queue (`short`/`default`/`long`).
5. Note: the scheduler must be enabled on the site
   (`bench --site <site> enable-scheduler`); the `doctor` skill checks this.
6. Append to `CHANGELOG.md`: *added job <name> · skill:add-job · rule:1*.

## Invariants & prohibitions

- Tasks must be idempotent where possible (a run may repeat).
- Wrap risky work and `frappe.db.commit()` deliberately; log failures via
  `frappe.log_error`.
- No long synchronous work in web requests — enqueue it.

## Examples

See `scheduler_events.py.snippet`, `tasks.py.snippet`, `enqueue.py.snippet`.

## Templates & snippets

- `scheduler_events.py.snippet` — hooks.py periodic + cron wiring.
- `tasks.py.snippet` — a task function skeleton.
- `enqueue.py.snippet` — fire-and-forget async enqueue.
