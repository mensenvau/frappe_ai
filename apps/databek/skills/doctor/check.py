#!/usr/bin/env python3
"""Databek doctor — static health check of the databek app (no bench required).

Usage:
    python skills/doctor/check.py apps/databek

Exit code 0 = all checks pass, 1 = at least one failure.
Read-only: it never edits files.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

PASS, FAIL = "PASS", "FAIL"
results: list[tuple[str, str, str]] = []  # (status, check, detail)


def record(status: str, check: str, detail: str = "") -> None:
    results.append((status, check, detail))


def check_doctype_json(app_pkg: Path) -> None:
    for jf in app_pkg.glob("**/doctype/*/*.json"):
        if jf.stem != jf.parent.name:
            continue  # only the DocType file shares its folder name
        try:
            data = json.loads(jf.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            record(FAIL, "doctype-json", f"{jf}: invalid JSON ({e})")
            continue
        for key in ("name", "module", "fields"):
            if key not in data:
                record(FAIL, "doctype-json", f"{jf}: missing '{key}'")
        # Child tables (istable=1) inherit the parent's permissions and
        # legitimately declare none.
        perms = data.get("permissions") or []
        if not perms and not data.get("istable"):
            record(FAIL, "doctype-perms", f"{jf}: no permissions (default-deny violated)")
        else:
            record(PASS, "doctype-json", str(jf))


def check_controllers(app_pkg: Path) -> None:
    for py in app_pkg.glob("**/doctype/*/*.py"):
        if py.stem != py.parent.name:
            continue
        try:
            ast.parse(py.read_text(encoding="utf-8"))
            record(PASS, "controller-parse", str(py))
        except SyntaxError as e:
            record(FAIL, "controller-parse", f"{py}: {e}")


def check_no_bom(app_pkg: Path) -> None:
    # A UTF-8 BOM breaks flit's __version__ parsing (pip install -e fails) and
    # can confuse Frappe's JSON loaders. Catch it statically.
    offenders = []
    for p in app_pkg.rglob("*"):
        if p.is_file() and p.suffix in {".py", ".json", ".txt", ".toml"}:
            if p.read_bytes()[:3] == b"\xef\xbb\xbf":
                offenders.append(str(p))
    if offenders:
        record(FAIL, "no-bom", "UTF-8 BOM in: " + ", ".join(offenders[:5]))
    else:
        record(PASS, "no-bom", "no BOM")


def check_hooks(app_pkg: Path) -> None:
    hooks = app_pkg / "hooks.py"
    if not hooks.exists():
        record(FAIL, "hooks-exists", f"{hooks}: missing")
        return
    src = hooks.read_text(encoding="utf-8")
    try:
        ast.parse(src)
        record(PASS, "hooks-parse", str(hooks))
    except SyntaxError as e:
        record(FAIL, "hooks-parse", f"{hooks}: {e}")
    for section in ("doc_events", "scheduler_events", "fixtures"):
        starts = len(re.findall(rf"# >>> DATABEK:{section}:start", src))
        ends = len(re.findall(rf"# <<< DATABEK:{section}:end", src))
        if starts == 1 and ends == 1:
            record(PASS, "hooks-markers", section)
        else:
            record(FAIL, "hooks-markers", f"{section}: start={starts} end={ends} (expected 1/1)")


def check_fixtures(app_pkg: Path) -> None:
    fx_dir = app_pkg / "fixtures"
    for jf in fx_dir.glob("*.json"):
        try:
            json.loads(jf.read_text(encoding="utf-8"))
            record(PASS, "fixtures-json", str(jf))
        except Exception as e:  # noqa: BLE001
            record(FAIL, "fixtures-json", f"{jf}: invalid JSON ({e})")


def check_no_erpnext(app_pkg: Path) -> None:
    hits = []
    for py in app_pkg.glob("**/*.py"):
        if re.search(r"\bimport +erpnext\b|\bfrom +erpnext\b", py.read_text(encoding="utf-8")):
            hits.append(str(py))
    if hits:
        record(FAIL, "no-erpnext", "erpnext imported in: " + ", ".join(hits))
    else:
        record(PASS, "no-erpnext", "no erpnext imports")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "apps/databek")
    # The Python package dir is the inner folder that holds hooks.py. For a
    # Frappe app `apps/<app>`, that is `apps/<app>/<app>`. Resolve generically so
    # the same doctor works for databek, hr, crm, … (not hardcoded to databek).
    if (root / root.name / "hooks.py").exists():
        app_pkg = root / root.name
    elif (root / "hooks.py").exists():
        app_pkg = root
    else:
        # fall back: any immediate subdir containing hooks.py
        app_pkg = next((d for d in root.iterdir()
                        if d.is_dir() and (d / "hooks.py").exists()), root)
    if not app_pkg.exists():
        print(f"doctor: app package not found at {app_pkg}", file=sys.stderr)
        return 1

    check_doctype_json(app_pkg)
    check_controllers(app_pkg)
    check_hooks(app_pkg)
    check_fixtures(app_pkg)
    check_no_erpnext(app_pkg)
    check_no_bom(app_pkg)

    failures = [r for r in results if r[0] == FAIL]
    for status, check, detail in results:
        mark = "OK " if status == PASS else "XX "
        print(f"{mark}[{check}] {detail}")
    print("-" * 60)
    print(f"doctor: {len(results) - len(failures)} passed, {len(failures)} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
