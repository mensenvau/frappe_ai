#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Mason bench entrypoint — idempotent bootstrap for the Frappe v15 dev stack.
# ---------------------------------------------------------------------------
# First run:  init bench (if missing) -> create empty site -> install mason
#             -> developer_mode=1 -> migrate/build -> start.
# Later runs: detect existing site -> just migrate/build/clear-cache -> start.
#
# This script is the body of the `run` skill. It NEVER installs ERPNext.
# ---------------------------------------------------------------------------
set -euo pipefail

BENCH_DIR=/workspace
SITE="${SITE_NAME:-mason.localhost}"
APP=mason

cd "$BENCH_DIR"

log() { echo "[mason-entrypoint] $*"; }

# --- 1. Ensure a bench exists -------------------------------------------------
if [ ! -f "$BENCH_DIR/sites/apps.txt" ]; then
  log "No bench detected — initializing Frappe ${FRAPPE_VERSION:-version-15} bench..."
  bench init \
    --skip-redis-config-generation \
    --frappe-branch "${FRAPPE_VERSION:-version-15}" \
    --no-procfile \
    --verbose \
    "$BENCH_DIR" || true
fi

# Point bench at the dockerized services (idempotent).
bench set-config -g db_host "${DB_HOST:-mariadb}"
bench set-config -g redis_cache "redis://${REDIS_CACHE:-redis-cache:6379}"
bench set-config -g redis_queue "redis://${REDIS_QUEUE:-redis-queue:6379}"
bench set-config -g redis_socketio "redis://${REDIS_QUEUE:-redis-queue:6379}"

# --- 2. Ensure mason is in apps.txt (the mounted app) -------------------------
if ! grep -qx "$APP" "$BENCH_DIR/sites/apps.txt" 2>/dev/null; then
  echo "$APP" >> "$BENCH_DIR/sites/apps.txt"
fi
# Make the mounted app pip-installed/editable so its hooks load.
pip install --quiet -e "$BENCH_DIR/apps/$APP" || true

# --- 3. Ensure the site exists -----------------------------------------------
if [ ! -d "$BENCH_DIR/sites/$SITE" ]; then
  log "Creating empty site $SITE (Frappe only, NO ERPNext)..."
  bench new-site "$SITE" \
    --no-mariadb-socket \
    --db-root-password "${DB_ROOT_PASSWORD:-123}" \
    --admin-password "${ADMIN_PASSWORD:-admin}" \
    --install-app "$APP"
  bench use "$SITE"
fi

# --- 4. developer_mode + reproducibility -------------------------------------
log "Setting developer_mode=${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p developer_mode "${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p mute_emails 1

# --- 5. Apply changes (the build loop tail) ----------------------------------
log "Migrating schema, building assets, clearing cache..."
bench --site "$SITE" migrate
bench build --app "$APP" || bench build
bench --site "$SITE" clear-cache

# --- 6. Serve ----------------------------------------------------------------
log "Mason is up. Desk: http://localhost:${HTTP_PORT:-8080}  (Administrator / ${ADMIN_PASSWORD:-admin})"
bench --site "$SITE" set-config -p host_name "http://localhost:${HTTP_PORT:-8080}"
exec bench serve --port 8000
