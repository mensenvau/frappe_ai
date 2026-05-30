#!/usr/bin/env bash
# Export Mason fixtures from the dockerized site to apps/mason/mason/fixtures/.
# Usage: skills/export-fixtures/run.sh [site]
set -euo pipefail

SITE="${1:-mason.localhost}"

# If running on the host, exec into the backend container; if already inside the
# bench, call bench directly.
if command -v docker >/dev/null 2>&1 && docker compose ps backend >/dev/null 2>&1; then
  docker compose -f docker/docker-compose.yml exec -T backend \
    bench --site "$SITE" export-fixtures --app mason
else
  bench --site "$SITE" export-fixtures --app mason
fi

echo "[export-fixtures] wrote apps/mason/mason/fixtures/*.json"
echo "[export-fixtures] review the diff before committing."
