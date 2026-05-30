#!/usr/bin/env bash
# Export Databek fixtures from the dockerized site to apps/databek/databek/fixtures/.
# Usage: skills/export-fixtures/run.sh [site]
set -euo pipefail

SITE="${1:-databek.localhost}"

# If running on the host, exec into the backend container; if already inside the
# bench, call bench directly.
if command -v docker >/dev/null 2>&1 && docker compose ps backend >/dev/null 2>&1; then
  docker compose -f docker/docker-compose.yml exec -T backend \
    bench --site "$SITE" export-fixtures --app databek
else
  bench --site "$SITE" export-fixtures --app databek
fi

echo "[export-fixtures] wrote apps/databek/databek/fixtures/*.json"
echo "[export-fixtures] review the diff before committing."
