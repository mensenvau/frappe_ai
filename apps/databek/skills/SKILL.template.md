---
name: <skill-or-module-name>
description: <one sentence — when to use this skill/module and what it produces. This line is what the AI matches against, so make it specific.>
---

# <Title>

<One paragraph: what this skill/module is for and its place in the build loop.>

## When to use

- Trigger phrases: "<...>", "<...>"
- Use this when <...>; do NOT use this when <...> (point to the right skill).

## Reads (context)

- [`../../RULES.md`](../../RULES.md) — always.
- <other files this skill needs to read before acting>

## Produces / edits

- <exact files created or edited, with paths>

## Procedure

1. Read RULES.md and this file.
2. <step>
3. <step>
4. If config changed → run `export-fixtures`.
5. Append to `databek/CHANGELOG.md`: *what · skill:<name> · rule:<n>*.

## Invariants & prohibitions

- <invariant the artifact must satisfy>
- <thing this skill must never do — e.g. "never edit core Frappe">

## Examples

```
<concrete before/after or a minimal artifact snippet>
```

## Templates & snippets

- `<file>` — <what it is>
