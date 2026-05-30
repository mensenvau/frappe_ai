#!/usr/bin/env bash
# Apply pending Frappe AI changes to an already-running stack (no full restart).
# Usage: skills/run/apply.sh [site]
set -euo pipefail

SITE="${1:-frappe_ai.localhost}"
DC="docker compose -f docker/docker-compose.yml exec -T backend"

echo "[run] migrating schema..."
$DC bench --site "$SITE" migrate

echo "[run] building assets..."
$DC bench build --app frappe_ai || $DC bench build

echo "[run] clearing cache..."
$DC bench --site "$SITE" clear-cache

echo "[run] done. Desk: http://localhost:8080"
