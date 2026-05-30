# Access audit/risk report for the Databek site.
#
# Install once into the app package so bench can import it:
#   cp apps/databek/skills/manage-access/access_report.py \
#      apps/databek/databek/databek/access_report.py
# Then run:
#   bench --site databek.localhost execute databek.databek.access_report.run
#
# Read-only: it never changes permissions. Output is a Role x DocType matrix plus
# a RISK section the AI summarizes for the user.

import frappe

# Roles that are expected to be powerful; flagging them is just-informational.
ADMIN_ROLES = {"System Manager", "Administrator"}
# Permission columns we report on.
PERMS = ["read", "write", "create", "delete", "submit", "cancel"]


def run():
    frappe.connect()
    rows = frappe.get_all(
        "DocPerm",
        fields=["parent as doctype", "role"] + PERMS + ["permlevel", "if_owner"],
        order_by="parent, role",
    )
    custom = frappe.get_all(
        "Custom DocPerm",
        fields=["parent as doctype", "role"] + PERMS + ["permlevel", "if_owner"],
        order_by="parent, role",
    )
    all_perms = rows + custom

    print("=== ROLE x DOCTYPE PERMISSIONS ===")
    for p in all_perms:
        flags = "".join(c[0].upper() if p.get(c) else "-" for c in PERMS)
        owner = " (if_owner)" if p.get("if_owner") else ""
        lvl = f" L{p['permlevel']}" if p.get("permlevel") else ""
        print(f"  {p['doctype']:<30} {p['role']:<22} {flags}{lvl}{owner}")

    print("\n=== RISK FLAGS ===")
    risks = []

    # 1) Guest / All with read/write.
    for p in all_perms:
        if p["role"] in ("Guest", "All") and (p.get("read") or p.get("write")):
            risks.append(f"PUBLIC: {p['role']} can access {p['doctype']}")

    # 2) Non-admin role with delete on app DocTypes.
    for p in all_perms:
        if p.get("delete") and p["role"] not in ADMIN_ROLES:
            risks.append(f"DELETE: role '{p['role']}' can delete {p['doctype']}")

    # 3) App DocTypes with NO permission rule (inaccessible) — Databek module only.
    fa_doctypes = frappe.get_all(
        "DocType", filters={"module": "Databek", "istable": 0}, pluck="name"
    )
    with_perms = {p["doctype"] for p in all_perms}
    for dt in fa_doctypes:
        if dt not in with_perms:
            risks.append(f"NO-PERMS: {dt} has no permission rule (inaccessible)")

    if risks:
        for r in risks:
            print(f"  ! {r}")
    else:
        print("  (none)")

    print(f"\nSummary: {len(all_perms)} permission rules, {len(risks)} risk flags.")
