# Frontend Task Queue (ordered, atomic tasks)

Updated: 2026-03-31T05:31:33Z (UTC)

1. confirm-deployed-dist-origin — completed
   - Files/paths: repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public, .replit-artifact/artifact.toml, /home/hn3t/workforce_frontend_app/dist
   - Acceptance criteria: deployed dist checksums match repo_imports artifact; rsync provenance observed in shell history.
   - Rollback notes: N/A

2. document-release-pipeline — completed
   - Files/paths: docs/ADMIN/frontend/README.frontend-deploy.md, scripts/restore_operational_artifact.sh
   - Acceptance criteria: README contains exact archive/restore commands; restore script accepts archive dir argument and is executable in-repo.
   - Rollback notes: restore script documented; operator must perform archive and verify restoration in staging.

3. verify-deploy-wrapper-paths — pending
   - Files/paths: app.py, deploy wrapper configs (systemd or container manifests), README.frontend-deploy.md
   - Acceptance criteria: wrapper serves ./dist or FRONTEND_DIST_DIR and returns index.html for SPA routes; restart command documented.
   - Rollback notes: do not change wrapper without an existing archive present.

4. map-repo_imports-source-to-maintained-source-tree — pending
   - Files/paths: repo_imports/.../artifacts/workforce-console, /home/hn3t/workforce_new, /home/hn3t/projects_active
   - Acceptance criteria: mapping document linking the artifact workspace packages and maintained source with clear diffs.
   - Rollback notes: none

5. normalize-build-contract-around-workforce-console — pending
   - Files/paths: README.frontend-deploy.md, package.json, pnpm workspace config
   - Acceptance criteria: documented build command that deterministicly produces expected publicDir layout.
   - Rollback notes: keep operational archive before making changes.

6. diff-maintained-source-build-vs-operational-artifact — pending
   - Files/paths: docs/ADMIN/frontend/artifact-diffs/checksum-diff.txt
   - Acceptance criteria: checksum diff produced and actionable reconciliation items listed.
   - Rollback notes: N/A

7. define-QA-cutover-plan — pending
   - Files/paths: docs/ADMIN/frontend/QA-cutover-plan.md
   - Acceptance criteria: staging / smoke tests and rollback rehearsal steps included and owners assigned.
   - Rollback notes: must include exact restore commands and contacts.

8. define-rollback-to-operational-artifact — pending (documentation completed)
   - Files/paths: docs/ADMIN/frontend/ROLLBACK_TO_OPERATIONAL_ARTIFACT.md, scripts/restore_operational_artifact.sh
   - Acceptance criteria: restore script present and documented; documentation marked COMPLETE. However, operator verification in staging is still required (see pending items below).
   - Rollback notes: archive and checksum must exist before attempting restore in production.

Special operator tasks (explicit, pending)
A. perform-archive-and-generate-checksums (OPERATOR ACTION — pending)
   - Files/paths: artifacts/operational/<timestamp>/, artifacts/operational/<timestamp>-checksums.txt
   - Exact commands (run from repo root):
     TIMESTAMP="$(date -u +%Y%m%dT%H%M%SZ)"
     ARCHIVE_DIR="artifacts/operational/$TIMESTAMP"
     mkdir -p "$ARCHIVE_DIR"
     rsync -av --delete dist/ "$ARCHIVE_DIR"/
     find "$ARCHIVE_DIR" -type f -print0 | xargs -0 sha256sum > "artifacts/operational/${TIMESTAMP}-checksums.txt"
     chmod +x scripts/restore_operational_artifact.sh
     echo "$TIMESTAMP"
   - Acceptance criteria: artifacts/operational/<timestamp>/ exists and artifacts/operational/<timestamp>-checksums.txt is present and matches contents.
   - Rollback notes: this archive is the canonical fallback for rollback.

B. verify-restore-in-staging (OPERATOR ACTION — pending)
   - Files/paths: staging environment, scripts/restore_operational_artifact.sh, artifacts/operational/<timestamp>/*
   - Exact commands (run from repo root):
     scripts/restore_operational_artifact.sh "artifacts/operational/<timestamp>"
     # then run smoke tests (examples):
     curl -fsS -o /dev/null -w "%{http_code}" http://localhost:8000/  # expect 200
     sha256sum dist/assets/*
   - Acceptance criteria: checksum comparison matches archived checksums; smoke tests return expected responses; no fatal errors in wrapper logs.
   - Rollback notes: restore must be rehearsed in staging before any production rollback.

C. run-smoke-tests-after-restore (OPERATOR ACTION — pending)
   - Commands (examples, run after restore):
     curl -fsS http://localhost:8000/ | grep "<title>"  # basic page load
     curl -fsS http://localhost:8000/assets/index-*.js -o /dev/null  # expect 200
   - Acceptance criteria: HTTP 200 for index and assets; basic route responses correct; no console-level runtime errors observed during tests.

