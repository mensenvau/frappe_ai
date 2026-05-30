# RULES.md — Frappe AI global law

> Every skill reads this file first, before doing anything else. These rules
> override convenience. If a rule conflicts with a request, surface the conflict
> and stop — do not silently break a rule.

1. **Only the Frappe Framework.** ERPNext is not installed (unless the user
   explicitly asks for it). Do not import from or depend on `erpnext`.

2. **Core Frappe is never modified.** Extend only via **Custom Field**,
   **Property Setter**, or a **new DocType**. Never edit files under
   `apps/frappe/`.

3. **Every change is written to disk** (because `developer_mode=1`) and frozen
   into `frappe_ai/fixtures/` via the `export-fixtures` skill, so the site is
   reproducible.

4. **Additive vs destructive.**
   - Additive (new DocType / field / role / job / UI) → do it right away.
   - Destructive (deleting a field/DocType, changing a fieldtype, renaming,
     anything that can lose data) → **STOP and ask for confirmation** before
     proceeding.

5. **Permissions are default-deny.** New roles get the minimum permissions
   needed; never grant `System Manager` as a shortcut.

6. **After every change:** `export-fixtures` → `run` (migrate + build) →
   append one line to `frappe_ai/CHANGELOG.md` recording: *what · which skill ·
   which rule(s)*.

7. **Every business module keeps its own `SKILL.md`** (domain, schema,
   invariants, examples, prohibitions). The AI loads full context from a single
   module folder.

8. **Frontend is a separate React SPA; Frappe is headless (API-only).**
   Frappe is the backend: DocTypes (data + permissions), whitelisted REST/RPC
   APIs, jobs, auth. The whole user-facing UI is a separate React app in
   `frontend/` that talks to Frappe over HTTP (token/session auth). The Frappe
   **Desk is NOT the product UI** — it is admin-only (developers/superadmin).
   - Backend rule still holds: business logic, validation, and permissions live
     in Frappe (controllers + DocType perms), NOT only in React. React must
     never be the only place a rule is enforced — the API enforces it too.
   - Every screen the React app needs is backed by a whitelisted API or the
     standard Frappe REST resource API; document each endpoint in the module's
     `SKILL.md`.

9. **AI layer (Claude API).** "AI for management everywhere" is a first-class,
   modular layer, not ad-hoc calls:
   - All model calls go through one service (`frappe_ai/ai/` — a thin Anthropic
     client) with **prompt caching**, the latest Claude model, and every call
     logged (DocType `AI Interaction`: prompt, response, tokens, cost, actor).
   - Three capabilities, each opt-in per module: (a) **natural-language command**
     ("compute this month's payroll", "find idle engineers") → proposes an
     action a human confirms; (b) **assist/recommend** (match employee→project,
     estimate price/duration, screen candidates, score time-off) → suggestion +
     human approval; (c) **summarize/report** (weekly digest, risk alerts).
   - AI never writes to the DB directly or bypasses permissions: it proposes,
     a permission-checked API applies. AI output is advisory unless a human (or
     an explicit rule) confirms. Secrets (`ANTHROPIC_API_KEY`) come from env /
     site config, never committed.

---

### Naming & layout conventions (enforced by skills)

- **Product brand = "Databek"** (titles, public site, emails). `frappe_ai` is
  only the backend app package name.
- App name `frappe_ai` — lowercase, snake_case (Frappe requirement).
- Module folder = snake_case under `frappe_ai/`; module label in `modules.txt`.
- DocType folder = snake_case of the DocType name; JSON + `.py` + optional `.js`
  share that folder name.
- Controller class = PascalCase of the DocType name.
- Whitelisted API methods carry `@frappe.whitelist()` and validate permissions
  explicitly (whitelisting ≠ authorization).
- Keep the `# >>> FRAPPEAI:<section>:start / <<< end` markers in `hooks.py` intact.
- Public React site lives in `frontend/` (own package.json/build); consumes only
  whitelisted public APIs. No business rule lives solely in React.
