# Copyright (c) 2026, Databek and contributors
# Controller for the Employee DocType.

import frappe
from frappe import _
from frappe.model.document import Document


class Employee(Document):
    def validate(self):
        # A linked User makes the employee a login; keep it unique per employee.
        if self.user:
            existing = frappe.db.get_value(
                "Employee",
                {"user": self.user, "name": ["!=", self.name]},
                "name",
            )
            if existing:
                frappe.throw(
                    _("User {0} is already linked to employee {1}.").format(
                        self.user, existing
                    )
                )

    def on_update(self):
        # Sync the employee's functional roles onto their User account so Frappe
        # permissions actually apply (advisory: only when a User is linked).
        if not self.user:
            return
        wanted = {r.role for r in (self.functional_roles or []) if r.role}
        if not wanted:
            return
        user = frappe.get_doc("User", self.user)
        have = {r.role for r in user.roles}
        added = False
        for role in wanted - have:
            user.append("roles", {"role": role})
            added = True
        if added:
            user.save(ignore_permissions=True)
