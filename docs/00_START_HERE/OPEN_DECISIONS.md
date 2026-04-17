OPEN_DECISIONS — execution decision log

Format: ID | Date opened | Decision question | Owner | Target decision date | Options | Recommended | Unblock condition | Blocking impact | Status | Notes / Evidence

D-001 | 2026-04-17 | Canonical frontend artifact delivery path
- Owner: UNASSIGNED (assign in PR)
- Target decision date: TBD (owner to set)
- Options:
  A) repo-hosted static artifacts (./docs/artifacts)
  B) external CDN/host
  C) CI pipeline artifact store (recommended)
- Recommended: C (CI pipeline artifact store)
- Unblock condition: Owner confirms CI artifact store availability or selects external host and documents exact host/path in ./CANONICAL_SOURCES.md
- Blocking impact: Medium (blocks release automation)
- Status: Needs verification
- Evidence: frontend docs at ./docs/workstreams/workforce-web-ui/ and ./workforce_frontend_app/docs/ADMIN/frontend/ but no artifact host found in repo

D-002 | 2026-04-17 | Post-core future module priority
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) analytics/dashboarding
  B) integrations/webhooks
  C) AI helpers/future modules
- Recommended: A then B
- Unblock condition: Core demo vertical (EXECUTION_QUEUE item 4) completed end-to-end and metrics surfaced in PROGRESS_REPORT.md
- Blocking impact: Low/Medium (affects allocation after core work)
- Status: Open
- Evidence: execution order in ./docs/00_START_HERE/EXECUTION_QUEUE.md

D-003 | 2026-04-17 | Canonical placement of boundary/reference catalogues
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) Keep PDFs in ./upload/ as exports only
  B) Move authoritative copies into ./docs/boundary/ as .md and keep PDFs in ./upload/exports
- Recommended: B
- Unblock condition: locate source .docx or master .md for the PDFs or re-author into ./docs/boundary/ and update CANONICAL_SOURCES.md
- Blocking impact: Low
- Status: Open / Needs action
- Evidence: references in ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md to REFERENCE_CATALOGUE.pdf and WF_Server_Boundary_Reference_Catalogue.pdf (files not found in repo)

D-004 | 2026-04-17 | Overlap/conflict between old and canonical plan docs
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) Archive older versions with an ARCHIVED label and summarize deltas
  B) Merge older parts into canonical and track provenance
- Recommended: A (archive + migration summary)
- Unblock condition: Owner produces migration-summary PR that archives conflicted files under ./docs/archive/ and references canonical master plan
- Blocking impact: Medium
- Status: Open
- Evidence: multiple master-plan artifacts present at ./upload/Workforce Docs/ and ./docs/planning/ and ./HN3T_MASTER_PLAN.md

D-005 | 2026-04-17 | Bootstrap endpoint canonical path (workforce_api)
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) create ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py (recommended)
  B) implement bootstrap in alternative router file (specify path)
- Recommended: A
- Unblock condition: bootstrap endpoint file exists and documented in CURRENT_STATE.md/CANONICAL_SOURCES.md
- Blocking impact: High (blocks frontend shell)
- Status: Confirmed
- Evidence: bootstrap.py present at ./workforce_api/apps/api/app/api/v1/endpoints/bootstrap.py; apps/api/app/api/router.py includes bootstrap_router and main.py mounts api_router at /api/v1 (canonical route: /api/v1/bootstrap).\n  - Methods observed for /api/v1/bootstrap: GET and POST (GET added to support frontend hydration).\n  - Import+route verification command and output included in CURRENT_STATE.md.

D-006 | 2026-04-17 | SILVER_SANDS doc: migrate vs archive
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) Migrate content into ./workforce_api/docs/ (recommended)
  B) Archive under ./docs/archive/ and mark legacy
- Recommended: A
- Unblock condition: Owner confirms source and files are migrated or archived
- Blocking impact: Low/Medium
- Status: Needs verification
- Evidence: Document present only under ./workforce_new/SILVER_SANDS_INTEGRATION_PLAN.md

D-007 | 2026-04-17 | Remaining backend path conflicts
- Owner: UNASSIGNED
- Target decision date: TBD
- Options:
  A) Treat workforce_api as canonical and update all docs to match
  B) Maintain workforce_new as experimental and tag all references [LEGACY]
- Recommended: A
- Unblock condition: Owner runs repo-wide audit and updates docs (this PR addresses many items)
- Blocking impact: Medium
- Status: Open
- Evidence: Mixed references across docs; this PR reconciled many but some legacy items remain

Usage
- Assign an owner and a target date when opening a decision. The owner is accountable for the unblock condition and closure.
- Close decisions by appending a short rationale and the merged PR link.

