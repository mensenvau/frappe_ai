---
name: crm
description: Databek CRM module app — Client records (individual or company), their contacts, and an optional portal user. Read before editing anything in the crm app.
---

# CRM module (app `crm`)

Separate Frappe app under `apps/crm`. Part of Databek.

## Domain
The customers the outsourcing company serves. A **Client** is an Individual or a
Company; companies can have multiple **Client Contacts**. A client may have a
portal `user` (login) to see only their own data later.

## DocTypes
| DocType | Purpose | Key fields |
|---------|---------|------------|
| Client | a customer | client_name (unique), client_type (Individual/Company), status (Lead/Active/Inactive), user (Link User, portal), email, phone, tax_id, address, contacts (Table) |
| Client Contact | child: a person at the client | contact_name, role, email, phone |

## Invariants
- `client_name` is unique. A Company client must have a name.

## Relationships
- `Client.user` → core `User` (portal login, optional).
- Later: Project links to Client; Client role sees only own rows (`if_owner`).

## Roles created by this app (default-deny)
- `Client` — read own records only (`if_owner`). Project Manager can create/edit
  clients; System Manager full. Frozen via `fixtures` in `hooks.py`.

## APIs (whitelisted)
- _(none yet)_

## AI hooks (planned)
- summarize client/project health for account managers.

## Prohibitions
- Client role must never see other clients' rows (keep `if_owner`).
