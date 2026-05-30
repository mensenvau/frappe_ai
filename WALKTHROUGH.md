# Walkthrough — how Databek grows

This shows the full build loop end-to-end with one concrete example, so you can
see how a plain request becomes live UI. Nothing here is pre-built; it's a
recipe the AI follows on demand.

> Reminder of the loop (see [`FRAPPE_AI.md`](FRAPPE_AI.md) §5):
> **you say it → AI writes a Frappe artifact → `export-fixtures` → `run`
> (migrate + build) → live in Desk.**

---

## 0. Bring the empty platform up

```bash
cd docker
docker compose up -d
docker compose logs -f backend     # wait for: "Databek is up. Desk: http://localhost:8080"
```

Open <http://localhost:8080>, log in as `Administrator` / `admin`. You get an
empty Desk — no business DocTypes. That's the foundation.

---

## 1. Example request: "I need a Widget model with a status, owned by a user"

The AI picks **create-doctype** (reads `apps/databek/skills/create-doctype/SKILL.md`
and `apps/databek/RULES.md` first).

It writes, from the templates in that skill folder:

```
apps/databek/databek/catalog/__init__.py
apps/databek/databek/catalog/doctype/__init__.py
apps/databek/databek/catalog/doctype/widget/__init__.py
apps/databek/databek/catalog/doctype/widget/widget.json     # schema
apps/databek/databek/catalog/doctype/widget/widget.py       # controller
apps/databek/databek/catalog/SKILL.md                        # module contract
```

and adds `Catalog` to `apps/databek/databek/modules.txt`.

`widget.json` (from `doctype.json.template`) has `title`, `status`, and an
`owner_user` Link → User, with a single `System Manager` permission (default-deny).

## 2. Add behavior: "an Active Widget must have an owner"

The AI picks **add-logic**, edits `widget.py`'s `validate()` using the pattern in
`add-logic/controller_methods.py.snippet`:

```python
def validate(self):
    if self.status == "Active" and not self.owner_user:
        frappe.throw(_("An Active Widget must have an owner."))
```

## 3. A role + permissions: "Widget Managers can edit, Viewers can read"

The AI picks **manage-permissions**: creates the two roles, grants them on the
Widget DocType (in `widget.json` `permissions`, since it's app-owned), and adds
the role names to the `Role` fixtures filter in `hooks.py`.

## 4. Surface it: "put Widgets on a dashboard with a count chart"

The AI picks **add-ui**: creates a Workspace (shortcut to Widget) and a Dashboard
Chart (`Count` of Widget over time) from the `add-ui` templates, all
`module = "Databek"`.

## 5. Freeze + run

```bash
# from repo root
apps/databek/skills/export-fixtures/run.sh        # freezes roles, workspace, chart
apps/databek/skills/run/apply.sh                  # migrate + build + clear-cache
```

(Or just `docker compose restart backend`, which re-runs the entrypoint's
migrate/build.)

## 6. Verify

`apps/databek/skills/doctor/check.py apps/databek` should still print all-pass, and
the Desk now shows the **Catalog** workspace, the **Widget** list, the validation
rule firing, and the count chart. The AI appended one line per step to
`apps/databek/databek/CHANGELOG.md`.

---

## What you never had to do

- Write a UI — Frappe rendered the form, list, and chart from the schema.
- Wire routing, REST, or permissions — Frappe derived them.
- Touch core Frappe — every change was a new DocType / Custom Field / record.
- Install ERPNext — it's never used.

That's the whole point: you describe intent, the AI lays the brick, Frappe holds
it up.
