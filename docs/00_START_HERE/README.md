00_START_HERE — Execution operator guide

Purpose
- Single entry and operating layer for contributors working on Workforce deliverables. Use this pack as the execution command layer.

Immediate authoritative files (paths)
- Master plan: ./HN3T_MASTER_PLAN.md
- Consolidated plan: ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md
- Progress log: ./PROGRESS_REPORT.md
- Running services / deploy notes: ./RUNNING_SERVICES.md
- Run plan helper: ./run_plan.sh
- FastAPI bootstrap scaffolding: ./workforce_api/apps/api/app/main.py [CONFIRMED]
- Bootstrap script (writes endpoints): ./workforce_api/scripts/phase3_bootstrap.sh [CONFIRMED]
- Frontend admin docs: ./workforce_frontend_app/docs/ADMIN/frontend/
- Frontend workstream implementation notes: ./docs/workstreams/workforce-web-ui/WORKFORCE_WEB_UI_COPILOT_IMPLEMENTATION.md

Reading order (new contributors)
1. README.md (this file)
2. CURRENT_STATE.md (evidence snapshot with exact paths)
3. EXECUTION_QUEUE.md (approved ordered queue and implementation targets)
4. OPEN_DECISIONS.md (decisions blocking work)
5. CANONICAL_SOURCES.md (where to consult artifacts and exports)

File status model
- Canonical: single source of truth (e.g., ./HN3T_MASTER_PLAN.md)
- Working: active, editable (.md) — e.g., ./PROGRESS_REPORT.md, docs/00_START_HERE/*
- Reference: exports (PDF/.docx) kept read-only in upload/ or exports
- Template: starter files under workforce_new/scripts or docs/planning/templates
- Archived: historic artifacts under docs/archive or PROJECTS_ARCHIVE

Rules (strict)
- Markdown (.md) under repo is the editable source of truth. Treat .pdf/.docx in upload/ as exports only.
- Every factual claim must include an evidence path. Use labels: [CONFIRMED], [INFERRED], [NEEDS VERIFICATION], [BLOCKED].
- If an implementation target is named, include the exact repo path (file or directory) that will be changed in the PR description.
- Before starting any queue item, update CURRENT_STATE.md with new evidence and add a decision entry in OPEN_DECISIONS.md if blocked.

Quick checklist before a PR
- Confirm owner for the slice and add to the PR description.
- Link the EXECUTION_QUEUE item and CURRENT_STATE evidence paths in the PR.
- If moving an uploaded export into canonical docs, create a .md in ./docs/ and update CANONICAL_SOURCES.md.

Contact and ownership
- Owners are recorded in the master plan and in OPEN_DECISIONS.md where assigned. If unassigned, set owner in the PR and update OPEN_DECISIONS.md.

