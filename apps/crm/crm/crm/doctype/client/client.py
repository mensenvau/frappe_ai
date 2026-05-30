# Copyright (c) 2026, Databek and contributors
# Controller for the Client DocType.

import frappe
from frappe import _
from frappe.model.document import Document


class Client(Document):
    def validate(self):
        # Individuals don't carry a tax id / multiple contacts conceptually, but
        # we don't hard-block — just a light guard on type/name.
        if self.client_type == "Company" and not self.client_name:
            frappe.throw(_("A company client needs a name."))
