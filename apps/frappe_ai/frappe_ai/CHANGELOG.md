# Frappe AI — Changelog

Every skill appends one line per change here, in the format:

```
- YYYY-MM-DD · <what changed> · skill:<skill-name> · rule:<rule number(s)>
```

---

- 2026-05-30 · Scaffolded foundation: docker stack, empty `frappe_ai` app, RULES.md, SKILL template, 10 skill folders, empty fixtures · skill:bootstrap · rule:1,2,3,8
- 2026-05-30 · Renamed app mason -> frappe_ai (dirs + all refs, MASON.md -> FRAPPE_AI.md) · skill:bootstrap · rule:2
- 2026-05-30 · Added default module dir frappe_ai/frappe_ai/frappe_ai/ (Frappe needs apps/<app>/<app>/<app>/) · skill:bootstrap · rule:2
- 2026-05-30 · Hardened docker entrypoint: bench init in-place (no venv-break move), sudo-chown volume, apps.txt newline, half-site heal, new-site --force · skill:run · rule:3,6
- 2026-05-30 · Verified: empty Frappe v15 site live at http://localhost:8080 (HTTP 200, login page), apps = frappe + frappe_ai, NO ERPNext · skill:run · rule:1
- 2026-05-30 · Added 10 Claude Code skills under .claude/skills/ (auto /slash commands); updated FRAPPE_AI.md brief + manual-steps section · skill:bootstrap · rule:7
