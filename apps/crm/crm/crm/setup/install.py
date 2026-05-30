# Copyright (c) 2026, Databek and contributors
# Idempotently ensure the Client role exists (default-deny).

import frappe


def ensure_client_role():
    if not frappe.db.exists("Role", "Client"):
        frappe.get_doc(
            {"doctype": "Role", "role_name": "Client", "desk_access": 1}
        ).insert(ignore_permissions=True)
    frappe.db.commit()


def after_install():
    ensure_client_role()
