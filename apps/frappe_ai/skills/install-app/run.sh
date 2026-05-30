#!/usr/bin/env bash
# Install an external Frappe app onto the dockerized Frappe AI site.
# Usage: skills/install-app/run.sh <git-url> <app-name> [branch] [site]
set -euo pipefail

URL="${1:?git URL required}"
APP="${2:?app name required}"
BRANCH="${3:-version-15}"
SITE="${4:-frappe_ai.localhost}"

# Guardrail: refuse ERPNext without an explicit override env var.
if [[ "$APP" == "erpnext" && "${FRAPPE_AI_ALLOW_ERPNEXT:-0}" != "1" ]]; then
  echo "[install-app] REFUSING to install ERPNext (platform is Frappe-only)."
  echo "[install-app] If you truly want it, re-run with FRAPPE_AI_ALLOW_ERPNEXT=1."
  exit 1
fi

DC="docker compose -f docker/docker-compose.yml exec -T backend"

$DC bench get-app "$URL" --branch "$BRANCH"
$DC bench --site "$SITE" install-app "$APP"
$DC bench --site "$SITE" migrate

echo "[install-app] installed $APP from $URL ($BRANCH)."
echo "[install-app] record it in CHANGELOG.md and docker/apps-extra.txt."
