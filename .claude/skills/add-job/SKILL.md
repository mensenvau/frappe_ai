---
name: add-job
description: Add background work to frappe_ai — a scheduled (cron/periodic) job via hooks.py scheduler_events, or an async task via frappe.enqueue. Use when the user wants something to run on a schedule or off the request thread.
---

# add-job

Read the full contract and snippets first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md).
2. Read [`apps/frappe_ai/skills/add-job/SKILL.md`](../../../apps/frappe_ai/skills/add-job/SKILL.md) — scheduled vs async, idempotency.
3. Use the snippets in [`apps/frappe_ai/skills/add-job/`](../../../apps/frappe_ai/skills/add-job/) (`scheduler_events.py.snippet`, `tasks.py.snippet`, `enqueue.py.snippet`).
4. Wire `scheduler_events` in `hooks.py` (keep `# >>> FRAPPEAI:scheduler_events` markers); add the task in `tasks.py`.
5. Append to `CHANGELOG.md`, then `/run`. (Scheduler must be enabled — `/doctor` checks.)
