Employee <-> User Link: Spec

Purpose
- Define canonical EmployeeProfile and UserEmployeeLink model shapes, minimal APIs, and migration guidance so backend and frontend teams can implement and integrate identity/employee linkage with clear tenant scoping and RBAC.

Guiding rules
- Users (accounts) are separate from EmployeeProfile records (employer-owned).
- Business is the tenant boundary; every EmployeeProfile belongs to a Business and optionally a Location.
- A User may be linked to an EmployeeProfile via a UserEmployeeLink row. Link lifecycle is explicit and auditable.
- Role assignment is separate and references either user_id (system roles) or employee_id (employee-scoped assignments) per existing RBAC model.

Canonical models (SQLAlchemy sketch)
- EmployeeProfile
  - id: UUID PK
  - business_id: UUID FK NOT NULL
  - location_id: UUID FK NULL
  - external_id: TEXT NULL  # supplier/HR system id
  - first_name: TEXT
  - last_name: TEXT
  - phone: TEXT NULL
  - email_work: TEXT NULL
  - job_title: TEXT NULL
  - is_active: BOOLEAN DEFAULT true
  - created_at: TIMESTAMP
  - updated_at: TIMESTAMP
  - unique constraint: (business_id, external_id) when external_id present

- UserEmployeeLink
  - id: UUID PK
  - user_id: UUID FK NOT NULL
  - employee_id: UUID FK NOT NULL
  - business_id: UUID FK NOT NULL  # redundancy for easy scoping queries
  - role_assignment_context: JSON / TEXT NULL  # optional: capture join-time metadata
  - is_active: BOOLEAN DEFAULT true
  - created_at: TIMESTAMP
  - created_by: UUID FK NULL
  - unique constraint: (user_id, employee_id)

API endpoints (initial minimal set)
- GET /api/v1/employees/?business_id=<>&location_id=<>  # list employees (admin scope)
  - Auth: business-admin or scoped role
  - Response: list[EmployeeProfileSchema]

- POST /api/v1/employees/
  - Auth: business-admin
  - Request: EmployeeCreate { business_id, location_id?, first_name, last_name, external_id?, email_work?, job_title? }
  - Response: EmployeeProfileSchema (201)

- POST /api/v1/users/{user_id}/link-employee
  - Auth: business-admin OR user self (depending on flow) — enforce RBAC server-side
  - Request: { employee_id: uuid, business_id: uuid }
  - Behavior: create UserEmployeeLink if permissions valid and employee belongs to business
  - Response: UserEmployeeLinkSchema (201)

- POST /api/v1/invitations/{token}/claim  # existing invite/claim flow for employee-to-user linking
  - Behavior: create user account + UserEmployeeLink in a single transactional flow (if token is employee invitation)
  - Response: per auth/register change: may return access_token + user summary

Field-level contract notes
- All tenant-scoped writes must validate business_id against requesting actor's scope.
- employee_id must reference an EmployeeProfile that belongs to the same business as business_id; reject cross-business linking.
- user_id must be a valid system User id.
- Responses should use consistent schemas under ./workforce_api/apps/api/app/schemas/ to ensure frontend typed DTOs can be generated.

Auth and UX decisions
- Admin-created user vs employee-to-user linking are distinct UXs and must map to different endpoints; do not conflate.
- Registration endpoint (/auth/register) remains the public account creation route; it now returns access_token (canonical). That token issuance is intentionally limited to auth/register and invite-claim flows where UX requires auto-login; it is not automatically applied to admin-created system-user flows unless product decides otherwise.

Migration guidance
- Create Alembic revision to add tables: employee_profiles, user_employee_links.
- Add FK constraints to businesses and locations tables; ensure ON DELETE behavior (restrict/NO ACTION) per tenancy rules.

Testing
- Backend pytest coverage:
  - test_create_employee_happy_path
  - test_link_user_to_employee_happy_path
  - test_link_rejects_cross_business
  - test_invite_claim_creates_user_and_link (integration)

Docs & spec files to add
- ./docs/00_START_HERE/specs/employee-link.md (this file)
- ./docs/00_START_HERE/specs/employee-link-api-examples.json (examples for frontend)

Owner & next steps (recommended)
- Owner: assign a backend engineer (PR should set owner in OPEN_DECISIONS.md)
- Next patch: add models/employee.py, schemas/employee.py, services/employee_service.py, migration stub, and 3 pytest tests under workforce_api/tests/. Keep routers thin: add endpoints in apps/api/app/api/v1/endpoints/employees.py and users link endpoint in users router.

Evidence paths (for follow-up)
- canonical backend root: ./workforce_api/
- bootstrap endpoint: ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py
- auth change (register token): ./workforce_api/apps/api/app/api/v1/endpoints/auth.py

Notes
- This spec is intentionally minimal to unblock implementation work and align frontend typed DTOs. Once implemented, update CURRENT_STATE.md with evidence and add/open an OPEN_DECISIONS entry for any unresolved choices (e.g., whether admin-created users should receive tokens).
