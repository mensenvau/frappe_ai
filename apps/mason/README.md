# mason

AI-extensible internal-tools platform on **Frappe Framework v15** (no ERPNext).

This app is an empty foundation. Business modules are added later by the AI via
the skills in [`skills/`](skills/), each of which writes Frappe artifacts
(DocType JSON, controllers, hooks, fixtures) that Frappe turns into live UI/API.

Start here:

- [`RULES.md`](RULES.md) — the global law every skill obeys.
- [`mason/SKILL.md`](mason/SKILL.md) — the app-level AI contract.
- [`skills/`](skills/) — the skill catalog.
- [`../../docker/`](../../docker/) — how to run it.

Run it: `cd docker && docker compose up -d` → <http://localhost:8080>.
