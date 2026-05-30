# Databek — Changelog

Every skill appends one line per change here, in the format:

```
- YYYY-MM-DD · <what changed> · skill:<skill-name> · rule:<rule number(s)>
```

---

- 2026-05-30 · Scaffolded foundation: docker stack, empty `databek` app, RULES.md, SKILL template, 10 skill folders, empty fixtures · skill:bootstrap · rule:1,2,3,8
- 2026-05-30 · Renamed app mason -> databek (dirs + all refs, MASON.md -> FRAPPE_AI.md) · skill:bootstrap · rule:2
- 2026-05-30 · Added default module dir databek/databek/databek/ (Frappe needs apps/<app>/<app>/<app>/) · skill:bootstrap · rule:2
- 2026-05-30 · Hardened docker entrypoint: bench init in-place (no venv-break move), sudo-chown volume, apps.txt newline, half-site heal, new-site --force · skill:run · rule:3,6
- 2026-05-30 · Verified: empty Frappe v15 site live at http://localhost:8080 (HTTP 200, login page), apps = frappe + databek, NO ERPNext · skill:run · rule:1
- 2026-05-30 · Added 10 Claude Code skills under .claude/skills/ (auto /slash commands); updated FRAPPE_AI.md brief + manual-steps section · skill:bootstrap · rule:7
- 2026-05-30 · Restructured Claude skills: replaced 10 verb skills with 4 intent skills (/build, /manage-access, /manage-ui, /manage-deploy); added access_report.py audit helper; building-block contracts retained · skill:bootstrap · rule:7
- 2026-05-30 · Added Databek architecture plan (ARCHITECTURE.md, 10 modules, phases), MODULES.md memory index, HOW_MEMORY_WORKS.md; RULES §8 (Desk internal + React public-only) + §9 (provider-agnostic AI: OpenAI default, Gemini drop-in); /build now reads+updates MODULES.md; brand=Databek, app stays databek · skill:bootstrap · rule:7,8,9
- 2026-05-30 · Renamed app frappe_ai -> databek (dirs apps/databek/databek/databek, all refs, FRAPPE_AI.md -> DATABEK.md, hooks markers DATABEK:, docker .env/compose/entrypoint, .claude skills); app=databek, brand=Databek · skill:bootstrap · rule:2
