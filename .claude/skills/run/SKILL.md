---
name: run
description: Bring the Frappe AI platform up (or apply changes) via Docker — docker compose up, then bench migrate + build + clear-cache + restart. Use when the user says "run", "start it", "deploy locally", or after any change that needs to go live.
---

# run

Read the full contract first, then act:

1. Read [`apps/frappe_ai/skills/run/SKILL.md`](../../../apps/frappe_ai/skills/run/SKILL.md).
2. (Optional) run `/doctor` first.
3. Start / first-run bootstrap:
   ```bash
   cd docker && docker compose up -d
   docker compose logs -f backend     # wait for "Frappe AI is up"
   ```
4. To apply changes to a running stack without a full restart:
   `apps/frappe_ai/skills/run/apply.sh` (migrate + build + clear-cache), or
   `docker compose -f docker/docker-compose.yml restart backend`.
5. Verify at <http://localhost:8080> (Administrator / admin). Append to `CHANGELOG.md`.

NEVER `docker compose down -v` (drops db + sites) unless the user explicitly asks — destructive.
