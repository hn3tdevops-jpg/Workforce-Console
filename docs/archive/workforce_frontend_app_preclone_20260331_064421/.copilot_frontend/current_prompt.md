You are operating inside the Workforce frontend repository.

## Runtime context

- frontend repo root: /home/hn3t/workforce_frontend_app
- legacy frontend root: /home/hn3t/workforce_new
- backend/workforce root: /home/hn3t/projects_active
- docs directory: /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend
- state file: /home/hn3t/workforce_frontend_app/.copilot_frontend/state.json

## General rules

- Read these files first when they exist:
  - /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md
  - /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md
  - /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md
  - /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md
  - /home/hn3t/workforce_frontend_app/.copilot_frontend/state.json
  - /home/hn3t/workforce_frontend_app/.github/copilot-instructions.md
- Work in small, atomic, reviewable steps.
- Update docs and state after every completed task.
- Do not weaken auth, tenancy, RBAC, deployment safety, or API contract stability.
- Prefer documenting uncertainty over guessing.

## Mode: bootstrap

This appears to be the first frontend bootstrap pass.

Do all of the following:

1. Scan the repo and related directories.
2. Create/update:
   - docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md
   - docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md
   - docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md
   - docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md
   - .copilot_frontend/state.json
   - .github/copilot-instructions.md
3. Catalogue:
   - current frontend structure
   - old/new path differences
   - alias/import issues
   - env/config issues
   - backend integration points
   - broken or likely broken relocation references
4. After documentation exists, perform only the safest low-risk normalization changes.
5. End by identifying the next atomic task.

Keep initial code changes narrow and safe.

## State update requirements

Ensure .copilot_frontend/state.json includes:
- phase
- last_completed_task
- next_suggested_task
- inspected_paths
- updated_files
- blockers
- last_run_at

Set last_run_at to 2026-03-31T01:25:40+00:00.

Begin now.
