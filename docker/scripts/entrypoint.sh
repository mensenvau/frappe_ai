#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Frappe AI bench entrypoint — idempotent bootstrap on the official frappe/bench
# image (which ships ONLY the bench CLI; the bench itself is created here).
# ---------------------------------------------------------------------------
# Runs as the `frappe` user. The bench-root volume mountpoint is root-owned, so
# we `sudo chown` it once (the image grants frappe passwordless sudo), then do
# all bench work unprivileged.
#
# KEY: `bench init` runs INSIDE the persisted volume and creates ./frappe-bench
# itself, so the Python venv's baked-in absolute paths stay valid (NO move —
# moving the bench breaks env/bin/python). Init happens once per volume.
#
# First run:  chown -> bench init bench-root/frappe-bench (Frappe v15, ~minutes)
#             -> symlink mounted frappe_ai app -> configure db/redis
#             -> create empty site -> install frappe_ai -> developer_mode=1
#             -> migrate/build/clear-cache -> serve.
# Later runs: bench already initialized -> migrate/build/clear-cache -> serve.
#
# This script is the body of the `run` skill. It NEVER installs ERPNext.
# ---------------------------------------------------------------------------
set -euo pipefail

ROOT=/home/frappe/bench-root
BENCH_DIR="$ROOT/frappe-bench"
FRAPPE_AI_SRC=/home/frappe/frappe_ai-src
SITE="${SITE_NAME:-frappe_ai.localhost}"
APP=frappe_ai
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"

log() { echo "[frappe_ai-entrypoint] $*"; }

# --- 0. Make the persisted volume writable by frappe -------------------------
if [ ! -w "$ROOT" ]; then
  log "Fixing ownership of $ROOT (root-owned volume mountpoint)..."
  sudo chown -R frappe:frappe "$ROOT" || log "WARN: chown failed (continuing)."
fi

# --- 1. Initialize the bench once (in place — no move) -----------------------
if [ ! -f "$BENCH_DIR/sites/apps.txt" ]; then
  log "No bench yet — running 'bench init' for Frappe ${FRAPPE_BRANCH} (slow, once)..."
  cd "$ROOT"
  # Clean any half-init from a previous failed run.
  rm -rf "$BENCH_DIR"
  bench init \
    --frappe-branch "$FRAPPE_BRANCH" \
    --skip-redis-config-generation \
    --no-procfile \
    --verbose \
    frappe-bench
  log "bench init complete."
fi

cd "$BENCH_DIR"

# --- 2. Symlink + install the mounted frappe_ai app ------------------------------
if [ -d "$FRAPPE_AI_SRC" ] && [ ! -e "$BENCH_DIR/apps/$APP" ]; then
  log "Linking mounted frappe_ai app into the bench..."
  ln -s "$FRAPPE_AI_SRC" "$BENCH_DIR/apps/$APP"
fi
if [ -d "$BENCH_DIR/apps/$APP" ]; then
  # Ensure apps.txt ends with a newline before appending, else the new app name
  # concatenates onto the previous line (e.g. "frappe" + "frappe_ai").
  APPS_TXT="$BENCH_DIR/sites/apps.txt"
  if ! grep -qx "$APP" "$APPS_TXT" 2>/dev/null; then
    [ -s "$APPS_TXT" ] && [ -n "$(tail -c1 "$APPS_TXT")" ] && echo >> "$APPS_TXT"
    echo "$APP" >> "$APPS_TXT"
  fi
  log "Installing $APP into the bench venv (editable)..."
  "$BENCH_DIR/env/bin/python" -m pip install --quiet -e "$BENCH_DIR/apps/$APP" || \
    log "WARN: pip install -e $APP failed (continuing)."
  # Sanity: Frappe imports the app as `<app>.<app>` (app package . default module).
  # This works only if the structure is apps/<app>/<app>/<app>/ — verify early so
  # a structural mistake fails loudly here, not deep inside `bench new-site`.
  if ! "$BENCH_DIR/env/bin/python" -c "import ${APP}.${APP}" >/dev/null 2>&1; then
    log "FATAL: 'import ${APP}.${APP}' failed — app package structure is wrong."
    log "       Expected apps/${APP}/${APP}/${APP}/ (default module dir). Aborting."
    exit 1
  fi
fi

# --- 2b. Heal a half-created site from a previous failed run ------------------
# If the site dir exists but frappe_ai isn't recorded as installed, the prior
# new-site failed mid-install; drop it so step 4 recreates it cleanly.
if [ -d "$BENCH_DIR/sites/$SITE" ]; then
  if ! bench --site "$SITE" list-apps 2>/dev/null | grep -qx "$APP"; then
    log "Healing half-created site $SITE (dropping incomplete site)..."
    bench drop-site "$SITE" --db-root-password "${DB_ROOT_PASSWORD:-123}" --force 2>/dev/null \
      || rm -rf "$BENCH_DIR/sites/$SITE"
  fi
fi

# --- 3. Point bench at the dockerized services -------------------------------
log "Configuring db_host/redis..."
bench set-config -g db_host "${DB_HOST:-mariadb}"
bench set-config -g redis_cache "redis://${REDIS_CACHE:-redis-cache:6379}"
bench set-config -g redis_queue "redis://${REDIS_QUEUE:-redis-queue:6379}"
bench set-config -g redis_socketio "redis://${REDIS_QUEUE:-redis-queue:6379}"

# --- 4. Ensure the site exists -----------------------------------------------
if [ ! -d "$BENCH_DIR/sites/$SITE" ]; then
  log "Creating empty site $SITE (Frappe only, NO ERPNext)..."
  # --force drops any leftover DB from a previous failed attempt before creating.
  bench new-site "$SITE" \
    --no-mariadb-socket \
    --force \
    --db-root-password "${DB_ROOT_PASSWORD:-123}" \
    --admin-password "${ADMIN_PASSWORD:-admin}" \
    --install-app "$APP"
fi
bench use "$SITE"

# --- 5. developer_mode + reproducibility -------------------------------------
log "Setting developer_mode=${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p developer_mode "${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p mute_emails 1

# --- 6. Apply changes (the build loop tail) ----------------------------------
log "Migrating schema..."
bench --site "$SITE" migrate
log "Building assets..."
bench build --app "$APP" || bench build || log "WARN: build skipped"
log "Clearing cache..."
bench --site "$SITE" clear-cache

# --- 7. Serve ----------------------------------------------------------------
log "Frappe AI is up. Desk: http://localhost:${HTTP_PORT:-8080}  (Administrator / ${ADMIN_PASSWORD:-admin})"
exec bench serve --port 8000
