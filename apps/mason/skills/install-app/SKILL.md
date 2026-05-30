---
name: install-app
description: Install an external Frappe app from a git URL onto the site (bench get-app + install-app). Use ONLY when the user explicitly names an app/URL to add. Never installs ERPNext unless explicitly requested.
---

# install-app

Adds a third-party Frappe app to the bench and installs it on the site. This is
the one place new external dependencies enter the platform — handle with care.

## When to use

- Triggers: "install <app>", "add the <name> Frappe app", "get-app <git-url>".
- Only when the user explicitly identifies the app. Do not infer or auto-add.

## Reads (context)

- [`../../RULES.md`](../../RULES.md) — §1: ERPNext only on explicit request.
- The git URL / app name the user provides.

## Produces / edits

- `apps/<app>/` in the bench (fetched by `bench get-app`).
- The site's installed-apps list (`bench install-app`).
- `sites/apps.txt` is updated by bench.
- For the dockerized stack: the app must persist in the image/volume — note that
  bind-mounted `mason` persists, but `get-app`'d apps land in the bench volume;
  record the URL so the stack is reproducible.

## Procedure

1. Read RULES.md §1. If the app is ERPNext (or pulls it in), STOP and confirm
   the user truly wants it — the platform is Frappe-only by design.
2. Fetch: `bench get-app <git-url> --branch <branch>`.
3. Install on the site: `bench --site mason.localhost install-app <app>`.
4. `bench migrate` to apply its schema.
5. Record the app + URL + branch in `CHANGELOG.md` and, ideally, in a
   `docker/apps-extra.txt` so a fresh build re-fetches it.
6. Append to `CHANGELOG.md`: *installed app <name> (<url>) · skill:install-app · rule:1*.

## Command

```bash
bench get-app https://github.com/org/app --branch version-15
bench --site mason.localhost install-app app
bench --site mason.localhost migrate
```

`run.sh` wraps this for the dockerized stack.

## Invariants & prohibitions

- ERPNext (or any app that depends on it) requires explicit user confirmation.
- Pin a branch/tag — don't install from a moving default silently.
- Vet the source; only install apps the user asked for.

## Templates & snippets

- `run.sh` — get-app + install-app against the dockerized stack.
