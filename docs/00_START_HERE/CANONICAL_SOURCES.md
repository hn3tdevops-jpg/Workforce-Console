CANONICAL_SOURCES — exact source map

Policy: store editable canonical .md under ./docs/ or repo root. Keep uploaded PDFs/.docx in ./upload/ as export-only references.

Exact mappings (confirmed where present)
- ./HN3T_MASTER_PLAN.md
  - Status: Canonical
  - Purpose: High-level program and governance
  - Editable: yes
  - Consult when: scope, ownership, architecture

- ./docs/planning/workforce_consolidated_master_plan_2026-04-17.md
  - Status: Working
  - Purpose: Consolidated operational plan (synthesis)
  - Editable: yes
  - Consult when: execution ordering and consolidated rationale

- ./upload/Workforce Docs/workforce_consolidated_master_plan_2026-04-17.md
  - Status: Present only as export
  - Purpose: Uploaded export of consolidated plan
  - Editable: no (extract to ./docs/ to edit)

- ./PROGRESS_REPORT.md
  - Status: Working
  - Purpose: Active progress logging
  - Editable: yes

- ./docs/workstreams/workforce-web-ui/WORKFORCE_WEB_UI_COPILOT_IMPLEMENTATION.md
  - Status: Confirmed
  - Purpose: Frontend implementation notes
  - Editable: yes

- ./workforce_frontend_app/docs/ADMIN/frontend/ (directory)
  - Status: Confirmed
  - Purpose: Frontend admin docs and runbooks
  - Editable: yes (within frontend repo)

- ./workforce_api/apps/api/app/main.py
  - Status: Canonical (Confirmed)
  - Purpose: FastAPI app entrypoint (bootstrap area)
  - Editable: yes

- ./workforce_api/scripts/phase3_bootstrap.sh
  - Status: Confirmed
  - Purpose: scaffolds API endpoints and starter services
  - Editable: yes

- ./workforce_new/  
  - Status: Legacy/Reference/Experimental
  - Purpose: Historical/experimental copy of backend surfaces. Verify artifacts before treating as active.

- REFERENCE_CATALOGUE.pdf
  - Status: Missing from canonical docs (referenced in consolidated plan)
  - Purpose: (expected) identity + employment architecture reference
  - Action: locate source or re-author into ./docs/boundary/

- WF_Server_Boundary_Reference_Catalogue.pdf
  - Status: Missing from canonical docs (referenced in consolidated plan)
  - Purpose: (expected) deployment/boundary reference for PythonAnywhere
  - Action: locate source or re-author into ./docs/boundary/

Canonical backend implementation root
- ./workforce_api/  - Status: Canonical backend implementation root (Confirmed). Consult this path for API, models, schemas, services, and bootstrap scripts.

Non-canonical backend roots
- ./workforce_new/  - Status: Legacy/Reference/Experimental. Do not treat as active by default; verify artifacts before use.

How to promote an export into canonical
1. Extract content into ./docs/boundary/ or ./docs/planning/ as .md
2. Update this file with the new path and set status to Canonical or Working
3. Add a note in OPEN_DECISIONS.md indicating source provenance and link to PR

If a path above is inaccurate or you have a different canonical target, edit this file and add the verification evidence path.
