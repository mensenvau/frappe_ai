---
name: install-app
description: Install an external Frappe app from a git URL onto the frappe_ai site (bench get-app + install-app). Use ONLY when the user explicitly names an app/URL. Never installs ERPNext unless explicitly requested.
---

# install-app

Read the full contract first, then act:

1. Read [`apps/frappe_ai/RULES.md`](../../../apps/frappe_ai/RULES.md) — §1: ERPNext only on explicit request.
2. Read [`apps/frappe_ai/skills/install-app/SKILL.md`](../../../apps/frappe_ai/skills/install-app/SKILL.md).
3. If the app is/pulls ERPNext → STOP and confirm.
4. Fetch + install (pin a branch):
   ```bash
   docker compose -f docker/docker-compose.yml exec -T backend bench get-app <git-url> --branch version-15
   docker compose -f docker/docker-compose.yml exec -T backend bench --site frappe_ai.localhost install-app <app>
   docker compose -f docker/docker-compose.yml exec -T backend bench --site frappe_ai.localhost migrate
   ```
   (or `apps/frappe_ai/skills/install-app/run.sh <git-url> <app> [branch]`)
5. Record the app + URL + branch in `CHANGELOG.md`.
