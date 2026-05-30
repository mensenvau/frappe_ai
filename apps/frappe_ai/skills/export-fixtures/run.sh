#!/usr/bin/env bash
# Export Frappe AI fixtures from the dockerized site to apps/frappe_ai/frappe_ai/fixtures/.
# Usage: skills/export-fixtures/run.sh [site]
set -euo pipefail

SITE="${1:-frappe_ai.localhost}"

# If running on the host, exec into the backend container; if already inside the
# bench, call bench directly.
if command -v docker >/dev/null 2>&1 && docker compose ps backend >/dev/null 2>&1; then
  docker compose -f docker/docker-compose.yml exec -T backend \
    bench --site "$SITE" export-fixtures --app frappe_ai
else
  bench --site "$SITE" export-fixtures --app frappe_ai
fi

echo "[export-fixtures] wrote apps/frappe_ai/frappe_ai/fixtures/*.json"
echo "[export-fixtures] review the diff before committing."
