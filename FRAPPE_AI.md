# Mason — Build Brief for Claude Code

> This document is handed to Claude Code. Goal: an internal-tools platform built on
> top of the Frappe Framework, **extensible by AI**, starting from an **empty
> foundation**. `Mason` is a working name (metaphor: AI = mason, laying modules onto
> the Frappe foundation brick by brick). If you change the name, replace `mason`
> with the new name throughout the document and code (a Frappe app name must be
> lowercase, snake_case).

---

## 0. IMPORTANT constraints (read this first)

- **ERPNext IS NOT INSTALLED.** Only the Frappe Framework. ERPNext's HR/Recruitment/
  Accounting modules are NOT NEEDED — the user's business model is different.
- **Empty foundation.** Only Frappe-native User / Role / Permission / DocType /
  Workspace. No prebuilt business modules.
- Business modules are added later by the AI **via skills** (in the form of Frappe
  DocType + hooks); this document only builds the foundation + the skill
  infrastructure.
- (Note: if a recruitment/job-opening example appears in the conversation — that was
  only an illustration, it will not be built.)

---

## 1. What the app is

Mason is an internal-tools platform built on top of Frappe that the AI extends
itself. The idea: **you say it → the AI writes/edits Frappe artifacts (DocType,
controller, hooks, fixtures) → you `docker run` → it goes live in the Frappe Desk
UI.**

You don't build the engine — registry, routing, schema→UI, RBAC, migration,
background jobs, auth/SSO, asset build — Frappe provides all of it. What Mason adds:
(1) conventions and skills for the AI, (2) a self-describing `SKILL.md` contract per
module, (3) a global `RULES.md`, (4) a fixtures flow for reproducibility and a single
"run" command.

The UI is also Frappe (Desk). There is NO separate React frontend.

---

## 2. Tech foundation

- **Frappe Framework v15** (latest stable). NOT ERPNext.
- **MariaDB** + **Redis** (required by Frappe).
- **bench** (the Frappe CLI).
- Via **Docker** — `frappe_docker` (official). This is the "docker run" flow.
- **developer_mode = 1** — DocType and config changes are written to disk as JSON
  files (not from the UI). Because of this they land in version control and the AI
  can read/edit them. This is the basis of the whole loop.
- A single custom Frappe app: **`mason`**.

---

## 3. Repo structure

```
mason-platform/                  # git repo
  docker/                        # frappe_docker compose + entrypoint
    docker-compose.yml
    .env
  apps/
    mason/                       # custom Frappe app (bench new-app mason)
      mason/
        hooks.py                 # manifest: doc_events, scheduler_events, fixtures
        modules.txt
        <module>/                # later: business modules go here
          doctype/<name>/        # DocType JSON + .py controller + .js client script
        fixtures/                # roles, custom fields, workspaces (export-fixtures)
        SKILL.md                 # app-level AI contract
        CHANGELOG.md
      RULES.md                   # global law (the AI reads it in every skill)
      skills/                    # Claude skills (SKILL.md folders)
        create-doctype/SKILL.md
        add-logic/SKILL.md
        customize-doctype/SKILL.md
        add-job/SKILL.md
        add-ui/SKILL.md
        manage-permissions/SKILL.md
        export-fixtures/SKILL.md
        install-app/SKILL.md
        run/SKILL.md
        doctor/SKILL.md
```

---

## 4. Default empty state

- No custom role is added — Frappe's native roles are enough (System Manager, All,
  Guest). When a new role is needed, it is added via the `manage-permissions` skill
  and written to fixtures.
- The site is empty: Frappe login + an empty Desk. No business DocType.
- `fixtures/` starts empty (or minimal). Every added role/permission/workspace is
  exported here.

---

## 5. Build loop (the most important part)

1. You say it ("I need an X model", "add this logic", "add it to the menu").
2. The AI writes/edits the Frappe artifact with the relevant skill (DocType JSON,
   controller `.py`, `hooks.py`, client script, custom field).
3. `export-fixtures` — freezes the config into `fixtures/*.json` (reproducibility).
4. You `run` (= docker) → inside it: `bench migrate` (schema) + `bench build`
   (assets) + `bench clear-cache` + restart.
5. The change is live in the Frappe Desk UI.

NO manual wiring. Frappe itself generates the UI, API, permissions, and menu from the
schema.

---

## 6. Skill catalog (with approximate context)

Every skill follows the same rhythm: **read RULES.md → read the relevant SKILL.md →
write/edit the Frappe artifact → (if needed) export-fixtures → write to
CHANGELOG.md.**

| Skill | Trigger | Reads (context) | Creates / edits |
|---|---|---|---|
| **create-doctype** | "need a model/doc" | RULES.md, app structure, related DocType SKILL.md | `doctype/<name>/<name>.json` (fields, type, link, permission) + `.py` controller + optional `.js` + SKILL.md stub |
| **add-logic** | "add a function/logic" | target DocType `.py` + SKILL.md invariants + RULES.md | controller methods (validate/before_save/on_submit), `@frappe.whitelist()` API, or hooks.py `doc_events` |
| **customize-doctype** | "add a field to an existing/external DocType" | target DocType + RULES.md | Custom Field / Property Setter (fixtures) — does not break core |
| **add-job** | "need a background job" | RULES.md, hooks.py | hooks.py `scheduler_events` (cron) + function, or `frappe.enqueue` (async) |
| **add-ui** | "menu/dashboard/report/UI" | RULES.md, existing Workspace | Workspace (menu/cards/shortcut), Dashboard Chart/Number Card, Report (Query/Script), List view settings |
| **manage-permissions** | "role/permission" | RULES.md, existing roles fixture | Role + Role Permission (DocType permissions or fixtures), default-deny |
| **export-fixtures** | after every config change | hooks.py `fixtures` list | `bench export-fixtures` → `fixtures/*.json` (roles, custom fields, workspaces, custom doctypes) |
| **install-app** | "install an external Frappe app" | git URL | `bench get-app <url>` + `bench install-app`, apps.txt is updated |
| **run** (= "docker run") | "run" / "start it up" | — | `docker compose up` + `bench migrate` + `bench build` + `bench clear-cache` + restart |
| **doctor** | check before run | the whole app | report: DocType JSON valid, controllers import, hooks in place, fixtures consistent, migration clean |

Note: later, each business module becomes a separate "module" inside the Frappe app —
with its own DocTypes + its own `SKILL.md` (the AI contract).

---

## 7. RULES.md (global law — the AI reads it in every skill)

```markdown
1. Only the Frappe Framework. ERPNext is not installed (unless the user explicitly
   asks for it).
2. Core Frappe is never modified — extension only via Custom Field /
   Property Setter / new DocType.
3. Every change is written to disk (developer_mode=1) and frozen into fixtures/ with
   export-fixtures (reproducibility).
4. Additive (new DocType/field/role) → do it right away. Destructive (deleting a
   field/DocType, changing a type, possible data loss) → STOP, ask for confirmation.
5. Permissions are default-deny.
6. After every change: export-fixtures → run (migrate + build). Write to CHANGELOG.md:
   what · which skill · which rule.
7. Every business module keeps its own SKILL.md (domain, schema, invariants, examples,
   prohibitions).
8. The UI is not written freehand — use Frappe DocType/Workspace/Report primitives.
```

---

## 8. Conventions

- **developer_mode=1** is always on in dev — changes land in files.
- **fixtures** — the key to reproducibility. `hooks.py` declares what gets exported
  (roles, custom fields, workspaces, specific DocTypes).
- **SKILL.md per module** — the AI gets full context from a single folder.
- **CHANGELOG.md** — a trail of every change.

---

## 9. FIRST TASK for Claude Code

> Build only the foundation, NOT a business module:
>
> 1. Frappe v15 bench with `frappe_docker` + a single empty site (Docker compose).
> 2. `bench new-app mason` — create the custom app, `install-app` it onto the site.
> 3. Set `developer_mode = 1`.
> 4. Inside the `mason` app create: `RULES.md` (the text above), a `SKILL.md`
>    template, the `skills/` folder (an empty `SKILL.md` stub for each skill), an
>    empty `fixtures/`.
> 5. Confirm `docker run` works: an empty Frappe site, the login page, an empty Desk.
> 6. DO NOT INSTALL ERPNext / HR / Recruitment.
> 7. When done, show how it works and stop — I'll tell you the next step.
