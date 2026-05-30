---
name: doctor
description: Pre-flight health check of the whole frappe_ai app before a run — DocType JSON validity, controllers import, hooks markers intact, fixtures consistency, no ERPNext. Use before run, or when something is broken and you need a diagnosis.
---

# doctor

Read the full contract first, then act:

1. Read [`apps/frappe_ai/skills/doctor/SKILL.md`](../../../apps/frappe_ai/skills/doctor/SKILL.md).
2. Run the static validator (no bench needed):
   ```bash
   python apps/frappe_ai/skills/doctor/check.py apps/frappe_ai
   ```
   Checks: DocType JSON valid (+ has permissions, default-deny), controllers parse,
   `# >>> FRAPPEAI:` hook markers balanced, fixtures JSON valid, no `erpnext` imports.
3. (Optional, against the running container) migration dry-run.
4. Report ✅/❌ per check. Do NOT auto-fix — report and let the right skill fix it.
