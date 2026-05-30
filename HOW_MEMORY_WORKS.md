# How Databek remembers — skills, modules, and memory across sessions

You asked the key question: *"Do I need a new skill for every Databek feature?
Does Claude write the skills itself? Next time I build, how does it remember and
find them?"* Here is the full answer.

---

## There are TWO different things called "skill" — don't mix them

### 1. Intent skills (`.claude/skills/`) — FIXED, never per-feature
These are the 4 commands you type in Claude Code. They are **universal** and do
**not** multiply as you add features:

| Command | Job |
|---------|-----|
| `/build` | build ANY new feature/module (model + logic + UI + run) |
| `/manage-access` | roles & permissions: audit, risk, create/fix, explain |
| `/manage-ui` | inspect/edit/hide/remove menus, dashboards, reports |
| `/manage-deploy` | docker: status, start/stop, logs, apply, backup, health |

➡️ **You never create a new `.claude` skill for a new module.** `/build` handles
the Customer module, the Project module, the Payroll module — all of them.
You only add a new intent skill if you invent a genuinely new *kind of action*
(rare).

### 2. Module memory (`apps/frappe_ai/frappe_ai/<module>/SKILL.md`) — GROWS per module
This is the part that "remembers." Every time `/build` creates or extends a
module, it writes that module's own `SKILL.md`: its domain, DocTypes, invariants,
APIs, AI hooks, prohibitions. **Claude writes this itself** as the last step of
building — you don't write it by hand.

---

## How it remembers next time (the chain)

```
You type /build  "add invoices to projects"
        │
        ▼
1. Reads apps/frappe_ai/MODULES.md      ← the INDEX of every module that exists
2. Sees "projects" is already built → opens projects/SKILL.md   ← full memory
3. Builds the change, respecting the existing schema & invariants
4. Updates projects/SKILL.md            ← writes new memory
5. Updates MODULES.md row               ← keeps the index current
6. Logs to CHANGELOG.md
```

So the **memory is on disk, in git** — not in Claude's head. Even a brand-new
chat session "remembers" everything, because step 1 always re-reads the index
and step 2 re-reads the module contract. Nothing is forgotten between sessions.

### The three memory files

| File | Role |
|------|------|
| [`apps/frappe_ai/MODULES.md`](apps/frappe_ai/MODULES.md) | **Index** — one line per built module → its SKILL.md. The first thing `/build` reads. |
| `apps/frappe_ai/frappe_ai/<module>/SKILL.md` | **Per-module memory** — full context for that module. |
| [`apps/frappe_ai/frappe_ai/CHANGELOG.md`](apps/frappe_ai/frappe_ai/CHANGELOG.md) | **History** — one line per change (what · skill · rule). |

Plus [`ARCHITECTURE.md`](ARCHITECTURE.md) (the long-term plan) and
[`apps/frappe_ai/RULES.md`](apps/frappe_ai/RULES.md) (the laws), which `/build`
also reads every time.

---

## What YOU do vs what CLAUDE does

| | You | Claude (`/build`) |
|---|-----|-------------------|
| Describe the feature in plain words | ✅ | |
| Decide DocTypes/fields/logic | | ✅ (asks only if blocking) |
| Write the code + UI | | ✅ |
| Write the module `SKILL.md` (memory) | | ✅ |
| Update `MODULES.md` index | | ✅ |
| Approve destructive changes | ✅ | (stops & asks) |
| Run / verify in browser | ✅ (open the URL) | ✅ (applies) |

---

## TL;DR

- **No** — you don't open a new skill per Databek feature. The 4 skills are enough.
- **Yes** — Claude writes a `SKILL.md` for each module automatically while building.
- **Yes** — next session it finds them via `MODULES.md` and reads the module's
  `SKILL.md`, so it remembers the schema, rules, and history. The memory lives in
  git, so it survives across sessions and machines.
