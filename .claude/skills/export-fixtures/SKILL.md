---
name: export-fixtures
description: Freeze frappe_ai config records (roles, custom fields, property setters, workspaces, custom doctypes) to fixtures/*.json for reproducibility. Run after any change that creates config data records. Driven by the fixtures list in hooks.py.
---

# export-fixtures

Read the full contract first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §3 reproducibility.
2. Read [`apps/frappe_ai/skills/export-fixtures/SKILL.md`](../../../apps/frappe_ai/skills/export-fixtures/SKILL.md).
3. Confirm the record's DocType + filter is declared in `hooks.py` `fixtures` (between the markers).
4. Run the export against the dockerized site:
   ```bash
   docker compose -f docker/docker-compose.yml exec -T backend \
     bench --site frappe_ai.localhost export-fixtures --app frappe_ai
   ```
   (or `apps/frappe_ai/skills/export-fixtures/run.sh`)
5. Review the diff in `apps/frappe_ai/frappe_ai/fixtures/*.json`; append to `CHANGELOG.md`.
