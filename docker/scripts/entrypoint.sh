#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Databek bench entrypoint — idempotent bootstrap on the official frappe/bench
# image (ships ONLY the bench CLI; the bench itself is created here).
# ---------------------------------------------------------------------------
# Multi-app: databek (core) + hr + crm + … are each a separate Frappe app,
# mounted under /home/frappe/apps-src/<app> and symlinked into the bench.
#
# Runs as `frappe`; sudo-chowns the root-owned bench-root volume once. `bench
# init` runs IN PLACE inside the volume (moving a bench breaks its venv paths).
#
# This script is the body of the `manage-deploy` skill. NEVER installs ERPNext.
# ---------------------------------------------------------------------------
set -euo pipefail

ROOT=/home/frappe/bench-root
BENCH_DIR="$ROOT/frappe-bench"
APPS_SRC=/home/frappe/apps-src
SITE="${SITE_NAME:-databek.localhost}"
FRAPPE_BRANCH="${FRAPPE_BRANCH:-version-15}"

# Install order matters: core first, then modules that may depend on it.
APPS=(databek hr crm)

log() { echo "[databek-entrypoint] $*"; }

# --- 0. Make the persisted volume writable by frappe -------------------------
if [ ! -w "$ROOT" ]; then
  log "Fixing ownership of $ROOT ..."
  sudo chown -R frappe:frappe "$ROOT" || log "WARN: chown failed (continuing)."
fi

# --- 1. Initialize the bench once (in place — no move) -----------------------
if [ ! -f "$BENCH_DIR/sites/apps.txt" ]; then
  log "No bench yet — running 'bench init' for Frappe ${FRAPPE_BRANCH} (slow, once)..."
  cd "$ROOT"
  rm -rf "$BENCH_DIR"
  bench init --frappe-branch "$FRAPPE_BRANCH" --skip-redis-config-generation \
    --no-procfile --verbose frappe-bench
  log "bench init complete."
fi
cd "$BENCH_DIR"

# --- 2. Symlink + pip-install every Databek app ------------------------------
for app in "${APPS[@]}"; do
  src="$APPS_SRC/$app"
  [ -d "$src" ] || { log "WARN: $src missing, skipping $app"; continue; }
  if [ ! -e "$BENCH_DIR/apps/$app" ]; then
    log "Linking app $app into the bench..."
    ln -s "$src" "$BENCH_DIR/apps/$app"
  fi
  # apps.txt: one app per line (newline-safe append).
  APPS_TXT="$BENCH_DIR/sites/apps.txt"
  if ! grep -qx "$app" "$APPS_TXT" 2>/dev/null; then
    [ -s "$APPS_TXT" ] && [ -n "$(tail -c1 "$APPS_TXT")" ] && echo >> "$APPS_TXT"
    echo "$app" >> "$APPS_TXT"
  fi
  log "pip install -e $app ..."
  "$BENCH_DIR/env/bin/python" -m pip install --quiet -e "$BENCH_DIR/apps/$app" || \
    log "WARN: pip install -e $app failed (continuing)."
  # Frappe imports an app as `<app>.<app>`; verify early.
  if ! "$BENCH_DIR/env/bin/python" -c "import ${app}.${app}" >/dev/null 2>&1; then
    log "FATAL: 'import ${app}.${app}' failed — bad app structure for $app. Aborting."
    exit 1
  fi
done

# --- 3. Point bench at the dockerized services -------------------------------
log "Configuring db_host/redis..."
bench set-config -g db_host "${DB_HOST:-mariadb}"
bench set-config -g redis_cache "redis://${REDIS_CACHE:-redis-cache:6379}"
bench set-config -g redis_queue "redis://${REDIS_QUEUE:-redis-queue:6379}"
bench set-config -g redis_socketio "redis://${REDIS_QUEUE:-redis-queue:6379}"

# --- 3b. Heal a half-created site from a previous failed run ------------------
if [ -d "$BENCH_DIR/sites/$SITE" ]; then
  if ! bench --site "$SITE" list-apps 2>/dev/null | grep -qx databek; then
    log "Healing half-created site $SITE ..."
    bench drop-site "$SITE" --db-root-password "${DB_ROOT_PASSWORD:-123}" --force 2>/dev/null \
      || rm -rf "$BENCH_DIR/sites/$SITE"
  fi
fi

# --- 4. Ensure the site exists, with all apps installed ----------------------
if [ ! -d "$BENCH_DIR/sites/$SITE" ]; then
  log "Creating empty site $SITE (Frappe only, NO ERPNext)..."
  bench new-site "$SITE" --no-mariadb-socket --force \
    --db-root-password "${DB_ROOT_PASSWORD:-123}" \
    --admin-password "${ADMIN_PASSWORD:-admin}" \
    --install-app databek
fi
bench use "$SITE"

# Install the remaining apps onto the site if not already installed.
for app in "${APPS[@]}"; do
  if ! bench --site "$SITE" list-apps 2>/dev/null | grep -qx "$app"; then
    log "Installing app $app on $SITE ..."
    bench --site "$SITE" install-app "$app" || log "WARN: install-app $app failed."
  fi
done

# --- 5. developer_mode + reproducibility -------------------------------------
log "Setting developer_mode=${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p developer_mode "${DEVELOPER_MODE:-1}"
bench --site "$SITE" set-config -p mute_emails 1

# --- 6. Apply changes --------------------------------------------------------
log "Migrating schema..."
bench --site "$SITE" migrate
log "Building assets..."
bench build || log "WARN: build skipped"
log "Clearing cache..."
bench --site "$SITE" clear-cache

# --- 7. Serve ----------------------------------------------------------------
log "Databek is up. Desk: http://localhost:${HTTP_PORT:-8080}  (Administrator / ${ADMIN_PASSWORD:-admin})"
exec bench serve --port 8000
