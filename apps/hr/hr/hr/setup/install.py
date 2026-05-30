# Copyright (c) 2026, Databek and contributors
# Idempotently ensure Databek roles exist (default-deny: created with no global
# permissions; DocType-level perms grant access per role).

import frappe

DATABEK_ROLES = [
    # functional roles
    "HR",
    "Accountant",
    "Project Manager",
    "Recruiter",
    # seniority levels (also used as roles for approval/visibility)
    "Intern",
    "Engineer",
    "Manager",
]


def ensure_roles():
    for role_name in DATABEK_ROLES:
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc(
                {
                    "doctype": "Role",
                    "role_name": role_name,
                    "desk_access": 1,
                }
            ).insert(ignore_permissions=True)
    frappe.db.commit()


def after_install():
    ensure_roles()
