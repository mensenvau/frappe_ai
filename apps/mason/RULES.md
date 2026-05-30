# RULES.md — Mason global law

> Every skill reads this file first, before doing anything else. These rules
> override convenience. If a rule conflicts with a request, surface the conflict
> and stop — do not silently break a rule.

1. **Only the Frappe Framework.** ERPNext is not installed (unless the user
   explicitly asks for it). Do not import from or depend on `erpnext`.

2. **Core Frappe is never modified.** Extend only via **Custom Field**,
   **Property Setter**, or a **new DocType**. Never edit files under
   `apps/frappe/`.

3. **Every change is written to disk** (because `developer_mode=1`) and frozen
   into `mason/fixtures/` via the `export-fixtures` skill, so the site is
   reproducible.

4. **Additive vs destructive.**
   - Additive (new DocType / field / role / job / UI) → do it right away.
   - Destructive (deleting a field/DocType, changing a fieldtype, renaming,
     anything that can lose data) → **STOP and ask for confirmation** before
     proceeding.

5. **Permissions are default-deny.** New roles get the minimum permissions
   needed; never grant `System Manager` as a shortcut.

6. **After every change:** `export-fixtures` → `run` (migrate + build) →
   append one line to `mason/CHANGELOG.md` recording: *what · which skill ·
   which rule(s)*.

7. **Every business module keeps its own `SKILL.md`** (domain, schema,
   invariants, examples, prohibitions). The AI loads full context from a single
   module folder.

8. **The UI is not written freehand.** Use Frappe primitives only —
   DocType / Workspace / Report / Dashboard Chart / Number Card / List view.
   No bespoke React/HTML frontend.

---

### Naming & layout conventions (enforced by skills)

- App name `mason` — lowercase, snake_case (Frappe requirement).
- Module folder = snake_case under `mason/`; module label in `modules.txt`.
- DocType folder = snake_case of the DocType name; JSON + `.py` + optional `.js`
  share that folder name.
- Controller class = PascalCase of the DocType name.
- Whitelisted API methods carry `@frappe.whitelist()` and validate permissions.
- Keep the `# >>> MASON:<section>:start / <<< end` markers in `hooks.py` intact.
