CURRENT_STATE — evidence-based snapshot (2026-04-17)

Labeling rule: each claim has one of: Confirmed / Inferred / Needs verification / Blocked. Evidence path is required for Confirmed and Inferred.

1) Repo state
- ./HN3T_MASTER_PLAN.md — Confirmed. (file present at repo root)
- ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md — Confirmed. (file present)
- ./PROGRESS_REPORT.md — Confirmed. (file present at repo root)
- ./upload/Workforce Docs/workforce_consolidated_master_plan_2026-04-17.md — Confirmed (upload/export present)

2) Frontend state
- ./docs/workstreams/workforce-web-ui/WORKFORCE_WEB_UI_COPILOT_IMPLEMENTATION.md — Confirmed. (frontend implementation notes present at this path)
- ./workforce_frontend_app/docs/ADMIN/frontend/ — Confirmed (frontend admin docs under this path)
- Canonical frontend artifact host/path — Needs verification (no single artifact host path found in repo; search for CI artifact store required)

3) Backend / API state
- FastAPI app entrypoint: ./workforce_api/apps/api/app/main.py — Confirmed (file present)
- Starter endpoints stubs (rooms, tasks, assignments, shifts): ./workforce_api/apps/api/app/api/v1/endpoints/{rooms.py,tasks.py,assignments.py,shifts.py} — Confirmed (created by ./workforce_api/scripts/phase3_bootstrap.sh)
- Session/bootstrap contract endpoint (GET /api/v1/bootstrap) — Confirmed (file present at ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py). Router wiring confirmed: ./workforce_api/apps/api/app/api/router.py includes bootstrap_router; ./workforce_api/apps/api/app/main.py mounts api_router at /api/v1 — canonical route: /api/v1/bootstrap.
- RBAC core files referenced in master plan (example paths in HN3T_MASTER_PLAN.md) — Inferred (master plan references files in workforce/ tree; exact implementation paths vary across repo trees)

4) Deployment / PythonAnywhere state
- ./RUNNING_SERVICES.md — Confirmed (file present)
- ./run_plan.sh — Confirmed (file present)
- PythonAnywhere host mapping matrix — Missing from canonical docs (no ./docs/boundary/pythonanywhere-matrix.md found)

5) Docs / Planning state
- Canonical master plan: ./HN3T_MASTER_PLAN.md — Confirmed
- Consolidated plan export: ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md and ./upload/Workforce Docs/workforce_consolidated_master_plan_2026-04-17.md — Confirmed
- REFERENCE_CATALOGUE.pdf — Missing from canonical docs (referenced in plans but not found in repo at ./REFERENCE_CATALOGUE.pdf)
- WF_Server_Boundary_Reference_Catalogue.pdf — Missing from canonical docs (referenced but not found)

6) Known gaps / conflicts
- Missing boundary/reference PDFs (REFERENCE_CATALOGUE.pdf, WF_Server_Boundary_Reference_Catalogue.pdf) — [MISSING]
- No discovered canonical bootstrap/session endpoint — [NEEDS VERIFICATION]
- Frontend artifact delivery location (CI artifact store or CDN) — [NEEDS VERIFICATION]

Operational next steps
- Bootstrap endpoint stub added at ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py and example schema available at ./docs/00_START_HERE/specs/bootstrap.json. Import verification: python -c "import sys, importlib; sys.path.insert(0, '/home/hn3t/workforce_api'); m = importlib.import_module('apps.api.app.main'); print('IMPORTED_APP_TITLE:', m.app.title)" -> IMPORTED_APP_TITLE: Workforce API
- Search and, if found, import the boundary/reference PDFs into ./docs/boundary/ as .md and keep PDFs in ./upload/exports/ if they are only exports.
- Assign owners for missing items and update OPEN_DECISIONS.md.


7) Active backend surfaces
- Active backend repo surface: ./workforce_api/  — Confirmed (primary implementation surface for FastAPI app, models, schemas, services, and bootstrap scripts)
- Legacy/secondary backend surfaces: ./workforce_new/  — LEGACY/REFERENCE/EXPERIMENTAL. Do not treat as the active implementation by default; verify any referenced artifacts before use.

Snapshot date: 2026-04-17
