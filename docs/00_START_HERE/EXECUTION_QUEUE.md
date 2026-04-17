Approved execution queue (order preserved)

1) identity / employee-link architecture
- Objective: Define canonical identity model and explicit user <-> employee linkage.
- Why it matters: Required for role assignment, task assignment, auditing.
- Dependencies: repo model files and frontend account/employee UI docs.
- Current status: [NEEDS VERIFICATION]
- Evidence (repo paths):
  - plan references: ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md (see section 'Identity and workforce linkage')
  - suggested model/table names: ./workforce_new/SILVER_SANDS_INTEGRATION_PLAN.md [LEGACY/REFERENCE - NEEDS VERIFICATION] (section 'Status Model')
- Most likely implementation targets:
  - Repo area: ./workforce_api/apps/api/app/models/  (create employee/user linkage models) [CONFIRMED]
  - File/module family: ./workforce_api/apps/api/app/schemas/ (pydantic schemas), ./workforce_api/apps/api/app/services/ (linking service) [CONFIRMED]
  - Frontend: ./workforce_frontend_app/ (exact component path needs confirmation)
- Next concrete slice: Add apps/api/app/schemas/employee.py and apps/api/app/models/employee.py + a migration stub; publish mapping doc to ./docs/00_START_HERE/specs/employee-link.md

2) bootstrap / session API contract
- Objective: Publish a stable bootstrap/session JSON contract used by the frontend shell to hydrate user, business, location, roles, and enabled workspaces.
- Why it matters: Single endpoint reduces race conditions and centralizes effective permissions.
- Dependencies: auth/session logic, role assignment model, frontend shell integration
- Current status: [INFERRED]
- Evidence (repo paths):
  - FastAPI bootstrap scaffolding: ./workforce_api/apps/api/app/main.py [CONFIRMED]
  - bootstrap design in consolidated plan: ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md (lines describing bootstrap hydration)
  - frontend consumer docs: ./docs/workstreams/workforce-web-ui/WORKFORCE_WEB_UI_COPILOT_IMPLEMENTATION.md
- Most likely implementation targets:
  - Repo area: ./workforce_api/apps/api/app/api/v1/endpoints/ [CONFIRMED]
  - File/module family: ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py (endpoint: GET /api/v1/bootstrap) [CONFIRMED - mounted via ./workforce_api/apps/api/app/api/router.py and ./workforce_api/apps/api/app/main.py]
  - Frontend entrypoint: frontend bootstrap consumer (path under ./workforce_frontend_app/; confirm exact file before PR)
- Next concrete slice: Create endpoint stub apps/api/app/api/v1/endpoints/bootstrap.py that returns example roles+scopes; publish JSON schema in ./docs/00_START_HERE/specs/bootstrap.json

3) Workforce shell and permission-aware navigation
- Objective: Implement a shell that consumes bootstrap contract and renders navigation and workspace selectors per effective permissions.
- Why it matters: UX correctness and security; minimizes extra API calls.
- Dependencies: item 2 (bootstrap contract), frontend router, role/perms model
- Current status: [BLOCKED] until bootstrap contract is stabilized
- Evidence (repo paths):
  - frontend design docs: ./docs/workstreams/workforce-web-ui/README.frontend-deploy.md and ./workforce_frontend_app/docs/ADMIN/frontend/
- Most likely implementation targets:
  - Repo area: ./workforce_frontend_app/
  - File/module family: components/shell, components/nav, lib/auth (exact paths to be confirmed)
  - UI entrypoint: shell root (Next.js _app or app shell component) — path needs confirmation in frontend repo
- Next concrete slice: Implement shell scaffold that consumes /api/v1/bootstrap and exposes a mocked nav; add a frontend smoke test referencing the exact file changed.

4) core hospitable loop
- Objective: Implement rooms -> tasks -> inspections -> event logging vertical for demo flow.
- Why it matters: Demo-critical vertical that validates Workforce + Hospitable integration.
- Dependencies: hk_rooms, hk_tasks models, event log table, RBAC enforcement
- Current status: [INFERRED]
- Evidence (repo paths):
  - starter endpoints scaffold: ./workforce_api/scripts/phase3_bootstrap.sh (creates apps/api/app/api/v1/endpoints/{rooms,tasks,assignments,shifts}.py) [CONFIRMED]
  - starter services: ./workforce_api/apps/api/app/services/housekeeping_service.py and room_board_service.py (created by bootstrap script) [CONFIRMED]
  - recommended data model: ./workforce_new/SILVER_SANDS_INTEGRATION_PLAN.md [LEGACY/REFERENCE - NEEDS VERIFICATION] (data model section)
- Most likely implementation targets:
  - Repo area: ./workforce_api/apps/api/app/api/v1/endpoints/ [CONFIRMED]
  - File/module family: ./workforce_api/apps/api/app/models/ (hk_rooms, hk_tasks), ./workforce_api/apps/api/app/schemas/, ./workforce_api/apps/api/app/services/ [CONFIRMED]
  - Endpoints/UI entrypoints: /api/v1/rooms/, /api/v1/tasks/ (existing stubs at apps/api/app/api/v1/endpoints/rooms.py and tasks.py), and frontend room-board pages under ./workforce_frontend_app/ (path TBD)
- Next concrete slice: Implement hk_rooms table and API create/list endpoints, and wire a task-create flow that emits a hk_task_events row and an event log entry.

5) PythonAnywhere separation
- Objective: Document and apply separation for PythonAnywhere-hosted services and their configuration differences.
- Why it matters: Deployment clarity and operational boundaries.
- Dependencies: RUNNING_SERVICES.md, run_plan.sh, deployment inventories
- Current status: [NEEDS VERIFICATION]
- Evidence (repo paths):
  - ./RUNNING_SERVICES.md
  - ./run_plan.sh
  - references in docs/planning/workforce_consolidated_master_plan_2026-04-17.md
- Most likely implementation targets:
  - Repo area: ./ (top-level deployment docs) and ./docs/boundary/ (recommended)
  - File/module family: deployment manifests and host mapping (create ./docs/boundary/pythonanywhere-matrix.md)
- Next concrete slice: Produce a table mapping services to hosts and required PYTHONANYWHERE config; add to ./docs/boundary/pythonanywhere-matrix.md

6) planning / state normalization
- Objective: Normalize planning artifacts and canonicalize status labels across master plan, progress report, and dashboards.
- Why it matters: Reduces ambiguity and speeds onboarding.
- Dependencies: ./HN3T_MASTER_PLAN.md, ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md, ./PROGRESS_REPORT.md, docs/00_START_HERE/
- Current status: [WORKING]
- Evidence (repo paths):
  - ./HN3T_MASTER_PLAN.md
  - ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md
  - ./PROGRESS_REPORT.md
- Most likely implementation targets:
  - Repo area: ./docs/ and ./docs/00_START_HERE/
  - File/module family: canonical mapping file ./docs/00_START_HERE/CANONICAL_SOURCES.md (update with exact paths)
- Next concrete slice: Reconcile status labels in ./HN3T_MASTER_PLAN.md, update ./docs/00_START_HERE/CANONICAL_SOURCES.md and publish a short reconciliation note in ./PROGRESS_REPORT.md

Guidance
- Keep the approved order. Before work on an item, update CURRENT_STATE.md with exact evidence paths and create or update an OPEN_DECISIONS entry if blocked.
