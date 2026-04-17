Staging / Local Preview Validation Plan — Canonical Build

Purpose
- Provide a low-risk, repeatable plan to validate the canonical build in a staging or local preview environment without touching the operational artifact.
- Rehearse cutover and rollback using archived operational artifact.

Environment assumptions
- Operator has shell access to the host where dist and wrapper live (/home/hn3t/workforce_frontend_app).
- Port 8000 (or configured port) is available for local preview; wrapper app.py configured to serve files from a chosen directory via FRONTEND_DIST_DIR.
- Staging path will be: /home/hn3t/workforce_frontend_app/dist-staging
- The canonical build source: /home/hn3t/workforce_new/packages/workforce/workforce/frontend
- The operational artifact archive: /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/ARTIFACT_ARCHIVE/workforce-console-archive
- Scripts available: scripts/restore_operational_artifact.sh

Exact build and preview commands
1. Build canonical artifact (isolated)
   cd /home/hn3t/workforce_new/packages/workforce/workforce/frontend
   npm ci --no-audit --no-fund
   npm run build
   # artifact produced in dist/

2. Prepare staging directory
   mkdir -p /home/hn3t/workforce_frontend_app/dist-staging
   rsync -av --delete /home/hn3t/workforce_new/packages/workforce/workforce/frontend/dist/ /home/hn3t/workforce_frontend_app/dist-staging/

3. Run local preview using the existing wrapper without replacing prod
   # Option A: run the Flask wrapper in preview mode with FRONTEND_DIST_DIR override
   FRONTEND_DIST_DIR="dist-staging" python3 app.py
   # Option B: use a simple static server (node or python) if previewing only static files
   python3 -m http.server --directory /home/hn3t/workforce_frontend_app/dist-staging 8001

Smoke-test checklist (staging)
- Server responds:
  - curl -fsS -o /dev/null -w "%{http_code}" http://localhost:8001/  => expect 200
- Assets served:
  - curl -fsS -I http://localhost:8001/assets/index-*.js | head -n 1 => expect 200
- API integration (if backend accessible):
  - curl -fsS http://localhost:8001/api/health => expect 200 (or adjust to real endpoint)
- Main UI load and JS execution:
  - Use Playwright/Playwright CLI or Puppeteer to load http://localhost:8001/ and assert:
    - No page-level console errors
    - Key element exists (#root, [data-test=app])
- Visual diff baseline (optional):
  - Take a screenshot of the main page: playwright screenshot or puppeteer
  - Save to /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/preview-evidence/screenshots/canonical-<timestamp>.png

Comparison points vs operational frontend
- Checksums: record checksums for canonical staging assets
  - sha256sum /home/hn3t/workforce_frontend_app/dist-staging/assets/* > /tmp/staging-checksums.txt
  - Compare to operational checksums: /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/ARTIFACT_ARCHIVE/checksums-archive.txt
- File list: ls -R dist-staging/ > /tmp/staging-filelist.txt
  - Compare to archived file list: docs/ADMIN/frontend/artifact-diffs/file-list-diff.txt
- Visual/UI differences: compare screenshots
- Runtime behavior: API responses, client-side flows (login, create task, mark task complete)
- Bundle size and load time: compare page size and main JS asset size vs operational artifact

Acceptance criteria (staging)
- HTTP root and assets load successfully
- No critical console errors on main page load
- Key API endpoints used by UI return expected responses
- Core user flows succeed in staging (login, view rooms, create/assign/complete task)
- QA reviewer sign-off recorded (name, timestamp, notes)

Rollback rehearsal using restore script
1. Before rehearsing rollback, ensure the real operational artifact is intact in the archive and restoration script works with --dry-run.
   sudo bash scripts/restore_operational_artifact.sh --dry-run
2. Perform a dry-run restore into a sandbox target (e.g., /home/hn3t/workforce_frontend_app/dist-sandbox)
   Modify script variables or run rsync manually:
     rsync -av --delete /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/ARTIFACT_ARCHIVE/workforce-console-archive/ /home/hn3t/workforce_frontend_app/dist-sandbox/
   Verify checksums and smoke-tests against dist-sandbox.
3. After successful rehearsal, do a full restore to /home/hn3t/workforce_frontend_app/dist (operator action) using the script (no --dry-run) in a controlled maintenance window.

Evidence to capture
- Checksums: /tmp/staging-checksums.txt
- File lists: /tmp/staging-filelist.txt
- Screenshot(s): docs/ADMIN/frontend/preview-evidence/screenshots/
- Playwright/Puppeteer logs for load and console errors
- HTTP traces: curl outputs for root, assets, and API endpoints
- A short QA sign-off note in PROGRESS_REPORT_FRONTEND.md

Minimal-risk workflow summary
1. Build canonical artifact locally/CI
2. Rsync into dist-staging
3. Run static server or wrapper pointed at dist-staging on a non-prod port
4. Run smoke tests and capture evidence
5. Compare artifacts and logs to archived operational artifact
6. Rehearse rollback in sandbox using restore script (dry-run then full) without touching prod

Post-actions
- If staging validation passes, schedule execute-staging-preview-validation (next suggested task) to run the scripts and collect evidence under the guidance of QA.
- If staging validation fails, collect diffs and file lists, and open a reconciliation task to align maintained source with operational artifact.
