# Databek — Architecture Plan

> **Product:** Databek — an outsourcing/staff-augmentation management platform.
> A company supplies employees to clients on projects, and manages the whole
> lifecycle: clients, projects, hiring, assignments, pay, time-off, learning,
> and AI-assisted management.
>
> **Stack:** Frappe v15 = backend + **internal UI via Frappe Desk** (admin, HR,
> accountant, recruiter, PM, employee, client portal — fast, permission-aware).
> A separate modern **React (Next.js) app** in `frontend/` is **only the public
> Databek site** (marketing + public job openings + apply form). The **AI layer
> is provider-agnostic** (default **OpenAI**, **Gemini** as a drop-in adapter,
> configured by env — not hardcoded). `databek` is the backend app package;
> **Databek** is the brand.
>
> **Status: PLAN ONLY — nothing here is built yet.** This document is for review.
> We build module by module, in the order in §7, after you approve.

---

## 1. Actors & access (who logs in, what they are)

Everyone is a Frappe **User**; what they can do is decided by **Role**. Internal
people work in the **Frappe Desk**; the public/candidate experience is the React
site.

| Actor | Logs in where | Roles (examples) | Sees |
|-------|---------------|------------------|------|
| **Superadmin / Dev** | Desk | System Manager | everything |
| **Internal staff (Employee)** | **Desk** | functional: `HR`, `Accountant`, `Recruiter`, `Project Manager` + level: `Intern`, `Engineer`, `Manager` | their work, per functional role |
| **Client** | **Desk portal** (read-only-ish) | `Client` | only their own company, projects |
| **Candidate / visitor** | **React public site** (no Desk) | Guest / `Applicant` | public job pages + own application |

Two role axes for employees (kept separate):
- **Level** (seniority): `Intern → Engineer → Manager` — affects pay bands, who
  can approve, default permissions.
- **Functional role** (what desk they sit at): `HR`, `Accountant`, `Recruiter`,
  `Project Manager`, … — grants module access (HR sees time-off; Accountant sees
  payroll; etc.). Default-deny: each role gets only its module.

A person = one **User** + one **Employee** or one **Client** record linked to it.

### Roles to create (PLAN ONLY — built per-module, not now)

> Decision: roles are **not** created up front. Each is created together with the
> module that needs it (via `/manage-access`), default-deny, then frozen to
> fixtures. Listed here so the plan is complete.

| Role | Created in phase | Grants (when its module exists) |
|------|------------------|---------------------------------|
| `Client` | P1 (crm) | own company + own projects (row-level) |
| `HR` | P1/P3 (hr/attendance) | employees, time-off |
| `Project Manager` | P2 (projects) | projects, assignments they manage |
| `Recruiter` | P5 (recruitment) | job openings, applications |
| `Accountant` | P4 (payroll) | payroll, payslips |
| level: `Intern` / `Engineer` / `Manager` | P1 (hr) | seniority axis; Manager can approve |

Brand note: product/UI/email brand is **Databek**; backend app package stays
`databek` (the framework layer).

---

## 2. Modules & DocTypes (the data model)

Frappe "module" = a folder of DocTypes. Proposed modules and their DocTypes
(fields are indicative; we refine per module when we build it):

### M1 — `crm` (Clients)
- **Client** — `client_type` (Individual / Company), name, legal/tax info,
  contact, `user` (Link → User for portal), status. (Company clients can have
  multiple Client Contact people.)
- **Client Contact** (child/linked) — name, role, email, phone.

### M2 — `projects` (Projects)
- **Project** — title, `client` (Link), `start_date`, `end_date_type`
  (Fixed / Estimated), `end_date`, `status`
  (`Draft → Hiring → Active → On Hold → Done → Cancelled`), description,
  `project_manager` (Link → Employee), budget.
- **Project Role / Seat** — a needed position on a project (e.g. "2 React
  engineers"): `project`, `title`, `level`, `count`, `pay_type`, `pay_rate`,
  `status` (Open / Filled). Drives hiring.
- **Project Milestone** (optional) — title, due date, status.

### M3 — `hr` (Employees & org)
- **Employee** — `user` (Link), name, `level` (Intern/Engineer/Manager),
  `functional_roles` (Table → Role), join date, status (Active/On Leave/Left),
  base pay info, skills (Table).
- **Skill** — name (for matching employee ↔ project).
- **Team / Department** (optional) — grouping + manager.

### M4 — `assignments` (Employee on Project + pay model)
- **Project Assignment** — `project`, `employee`, `project_role`,
  `pay_type` (Fixed-per-project / Monthly / Hourly), `pay_rate`, currency,
  `start_date`, `end_date`, `allocation %`, status.
  *This is the heart of billing & payroll.*

### M5 — `attendance` (Time & time-off)
- **Time Off Type** — name, `is_paid` (Check), `max_days_per_year`, approval
  required. (e.g. Annual=paid, Sick=paid, Unpaid=unpaid.) → "turiga qarab
  pul berish/bermaslik".
- **Time Off Request** — `employee`, `type`, from/to, days, status
  (`Pending → Approved/Rejected`), approver. (AI can pre-score.)
- **Work Log / Attendance** — `employee`, date, hours (for hourly pay & rest-day
  calc), `project`. (Could be daily entries or timesheets.)
- **Holiday Calendar** — official days off (rest-day calculation base).

### M6 — `payroll` (Pay computation)
- **Payroll Run** — period (month), status, generated lines.
- **Payslip** — `employee`, period, computed from Assignments (monthly/hourly/
  fixed) + paid time-off − unpaid days; gross/net. (AI command: "compute this
  month".) *Computation is server-side, deterministic; AI only triggers/explains.*

### M7 — `recruitment` (Hiring)
- **Job Opening** — created (often auto) when a Project goes `Hiring` or a
  Project Role is `Open`: title, level, `project`, description, status
  (Open/Closed), public (Check → shows on public site).
- **Job Application** — applicant info, `job_opening`, resume, stage
  (`Applied → Screening → Interview → Offer → Hired/Rejected`). (AI screens/ranks.)
- **Candidate** — optional person record.

### M8 — `learning` (Courses)
- **Course** — title, description, content/links, `level`, published.
- **Course Group** — a cohort; `members` (Table → Employee), access rule.
- **Enrollment** — `employee`, `course` (or via group), progress, completed.
  → "guruhga qarab ruxsat beriladi".

### M9 — `ai` (AI layer — cross-cutting, provider-agnostic)
- **AI Provider Settings** (Single DocType) — `active_provider` (OpenAI default /
  Gemini / …), `model`, options. API keys come from env/site config, NOT stored
  in plaintext here.
- **AI Interaction** — log: provider, model, actor, module, prompt, response,
  tokens, cost, action taken. (RULES §9.)
- **AI Action** (optional) — a proposed action awaiting human confirm.
- Service code `databek/ai/` — a **provider interface** (`generate()`,
  `embed()`) with adapters `openai.py` (**default**), `gemini.py`, … selected by
  config. Used by all modules. Capabilities: NL-command, assist/recommend,
  summarize/report, **applicant↔job fit scoring** (RULES §9). Swapping provider =
  config change only.

### M10 — `notifications` / background jobs (cross-cutting)
- Scheduler jobs: project ending soon → alert PM & client; time-off pending →
  remind approver; payroll due; assignment ending; course deadline.
- Uses Frappe `scheduler_events` + `frappe.enqueue` + Notification/email.

### Cross-cutting: **public site** (React / Next.js) — PUBLIC ONLY
- Marketing/landing pages + public **Job Openings** list & detail + **apply
  form** (Databek brand, modern, SEO). Consumes whitelisted public APIs.
- On apply → creates a Job Application; **AI scores applicant↔job fit** for the
  recruiter (in Desk).
- Internal portals (Client/Employee/Admin) are **Frappe Desk**, NOT React.

---

## 3. Key relationships (text ER)

```
User 1─1 Employee            User 1─1 Client
Client 1─* Project
Project 1─* Project Role (Seat)
Project 1─* Project Assignment *─1 Employee
Project (status=Hiring) ─auto→ Job Opening *─* Job Application
Employee 1─* Time Off Request *─1 Time Off Type
Employee 1─* Work Log
Payroll Run 1─* Payslip *─1 Employee   (computed from Assignment + Attendance)
Course *─* Employee  (via Course Group / Enrollment)
AI Interaction logs every AI call across all modules
```

## 4. Automations (logic & jobs)

- **Project.status → Hiring**: auto-create Job Opening(s) for Open Project Roles.
- **Job Application → Hired**: offer to create Employee + Project Assignment.
- **Time Off Request → Approved**: feed into payroll (paid vs unpaid by type).
- **Payslip compute**: monthly = rate; hourly = Σ work-log hours × rate;
  fixed = once; minus unpaid days; plus paid time-off; honoring holidays.
- **Scheduler**: "project ending in N days" alerts; pending-approval reminders;
  payroll-due; assignment-ending.

## 5. AI integration points (where AI plugs in)

| Module | NL command | Assist / recommend | Summarize / report |
|--------|-----------|--------------------|--------------------|
| projects | "show projects ending this month" | estimate price/duration | weekly project digest + risk |
| assignments | "find idle engineers for project X" | match employee ↔ seat by skill/level | utilization report |
| recruitment | — | screen & rank applications | hiring funnel summary |
| payroll | "compute March payroll" | flag anomalies | payroll summary |
| attendance | — | score/triage time-off requests | absence report |
| learning | — | recommend courses per level/gap | progress report |

All via the one AI service; every call logged; output advisory → human confirms.

## 6. Security model (default-deny)

- Each functional Role gets ONLY its module's DocTypes (HR→hr/attendance,
  Accountant→payroll, Recruiter→recruitment, PM→projects/assignments).
- **Client** role: row-level — sees only records where `client == own company`
  (User Permission / `if_owner`-style restriction).
- **Employee**: sees own Employee, own assignments, own time-off, own courses.
- API enforces this too (not just React). `/manage-access` audits it.

## 7. Build order (phases — we do these one at a time)

| Phase | Modules | Outcome |
|-------|---------|---------|
| **P0** | RULES update, this plan, `ai/` provider-agnostic service skeleton (OpenAI default + Gemini adapter), AI Provider Settings + AI Interaction DocTypes | AI foundation (config-driven) |
| **P1** | `hr` (Employee, levels, functional roles) + `crm` (Client) + roles/permissions + Desk workspaces | core actors + Desk login for both |
| **P2** | `projects` (Project, Project Role, statuses) | projects tied to clients |
| **P3** | `assignments` (pay models) + `attendance` (time-off types, requests, work log) | who works where + time tracking |
| **P4** | `payroll` (compute) | pay from assignments + attendance |
| **P5** | `recruitment` (auto Job Opening on Hiring) + public whitelisted APIs | hiring flow + API for the site |
| **P6** | **`frontend/` React (Next.js) public site** — landing + job list/detail + apply, Databek brand | public site live |
| **P7** | `learning` (courses, groups, enrollment) | training |
| **P8** | `ai` capabilities wired into each module (NL command, recommend, summarize, applicant-fit) + `notifications`/jobs | AI everywhere + alerts |

Each phase: build DocTypes + logic + Desk UI (or React for P6) + permissions +
jobs, then `/manage-deploy` and verify, then move on.

## 8. Open questions (to refine as we go — not blocking the plan)

- Currency / multi-currency? (assume single currency first)
- Hourly pay: from Work Log entries or formal Timesheets? (assume Work Log first)
- Client portal scope in P1 or later? (assume read-only portal later, P8)
- React: **Next.js** for the public site (SSR → SEO for job pages). Confirmed:
  React is PUBLIC-ONLY; internal UI stays in Desk.
- AI: provider-agnostic, **OpenAI default**, **Gemini** drop-in via config.
  (Note: the app is named `databek`; the AI provider is independent of that
  name — OpenAI/Gemini, not necessarily Anthropic.)
- Public API auth: read endpoints public (job list/detail); apply = public POST
  with rate-limit/captcha later.

---

## 9. What changes vs the original empty foundation

- **RULES.md §8** rewritten: internal UI = Frappe Desk; **only the public site**
  is React (Next.js). **§9** added: provider-agnostic AI layer (OpenAI default,
  Gemini drop-in, env-configured, logged, advisory).
- New top-level **`frontend/`** (Next.js public site) added in P6.
- New backend modules m1–m10 added phase by phase.
- The 4 Claude skills still drive everything: `/build` (per module),
  `/manage-access`, `/manage-ui`, `/manage-deploy`.
