---
name: hr
description: Databek HR module app — Employee records, seniority levels (Intern/Engineer/Manager), functional roles (HR/Accountant/PM/Recruiter), and skills. Read before editing anything in the hr app.
---

# HR module (app `hr`)

Separate Frappe app under `apps/hr`. Part of Databek.

## Domain
Internal staff of the outsourcing company. An **Employee** is a person who may
have a login (`user`), a seniority **level**, one or more **functional roles**
(what they're allowed to do), and **skills** (for matching to projects later).

## DocTypes
| DocType | Purpose | Key fields |
|---------|---------|------------|
| Employee | a staff member | employee_name, user (Link User), level (Intern/Engineer/Manager), status (Active/On Leave/Left), join_date, functional_roles (Table), skills (Table) |
| Employee Functional Role | child: a granted role | role (Link Role) |
| Employee Skill | child: a skill | skill, proficiency |

## Invariants
- One `user` maps to at most one Employee (validate enforces uniqueness).
- On save, an Employee's `functional_roles` are synced onto their linked User's
  roles (so Frappe permissions actually apply). Additive only — never strips.

## Relationships
- `Employee.user` → core `User`.
- `functional_roles[].role` → core `Role` (HR, Accountant, Project Manager,
  Recruiter — created with default-deny perms).
- Later: projects/assignments link to Employee.

## Roles created by this app (default-deny)
Functional: `HR`, `Accountant`, `Project Manager`, `Recruiter`.
Level: `Intern`, `Engineer`, `Manager`.
Frozen via `fixtures` in `hooks.py`. HR can manage Employees; Manager read-only.

## APIs (whitelisted)
- _(none yet)_

## AI hooks (planned)
- match Employee ↔ project seat by skill/level; "find idle engineers".

## Prohibitions
- Never grant System Manager via functional roles.
- Don't strip a User's existing roles on Employee save (additive only).
