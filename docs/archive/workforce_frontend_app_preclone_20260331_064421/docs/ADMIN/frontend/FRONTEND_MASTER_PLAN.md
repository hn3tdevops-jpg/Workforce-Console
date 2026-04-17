# Frontend Master Plan — Two-track approach

Updated: 2026-03-31T05:31:33Z (UTC)

Overview
- Purpose: Protect the currently-deployed operational artifact lineage while reconciling the maintained source tree in parallel.
- Key distinction (must be preserved):
  - Operational canonical artifact: the artifact lineage currently proven to back production deployment
  - Canonical maintained source: the source tree intended for long-term maintenance, still under reconciliation

Priority
- Track A (Protect operational artifact): HIGH PRIORITY — must be preserved and restorable at all times.
- Track B (Reconcile maintained source): MEDIUM PRIORITY — proceed in parallel but do not cut over until QA and provenance are complete.

Track A — Protect current production artifact lineage (Immediate priorities)
1. confirm-deployed-dist-origin (COMPLETED)
   - Files/paths: docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md; repo_imports/Workforce-Showcase-master/artifacts/workforce-console/.replit-artifact/artifact.toml
   - Acceptance: checksums matched and rsync provenance recorded in shell history.
   - Rollback: N/A
2. document-release-pipeline (COMPLETED)
   - Files/paths: docs/ADMIN/frontend/README.frontend-deploy.md (updated), scripts/restore_operational_artifact.sh (updated)
   - Acceptance: README documents artifact path, archive and restore commands; restore script updated and executable in-repo.
   - Rollback: documented in README and scripts/restore_operational_artifact.sh
3. verify-deploy-wrapper-paths (PENDING)
   - Files/paths: app.py, deployment wrapper unit/service configs (systemd/container definitions)
   - Acceptance: wrapper reads FRONTEND_DIST_DIR and serves index.html for SPA routing; restart command documented.
   - Rollback: preserve current dist archive before making wrapper changes.
4. normalize-artifact-contract (PENDING)
   - Files/paths: README.frontend-deploy.md, QA-cutover-plan.md, ROLLBACK_TO_OPERATIONAL_ARTIFACT.md
   - Acceptance: documented artifact layout and file expectations.
5. preserve-rollback-path (PENDING — operator action required)
   - Files/paths: artifacts/operational/<timestamp>/ and artifacts/operational/<timestamp>-checksums.txt
   - Acceptance: archive created and checksum file present in repo; restore verification performed in staging.
   - Rollback: immediate via scripts/restore_operational_artifact.sh

Track B — Reconcile maintained source to production-ready state
1. map-repo_imports-source-to-maintained-source-tree (PENDING)
   - Files/paths: repo_imports/.../artifacts/workforce-console, /home/hn3t/workforce_new, /home/hn3t/projects_active
   - Acceptance: mapping document created; package.json and lockfile differences enumerated.
2. normalize-env-and-api-contract (PENDING)
   - Files/paths: .env.example, vite.config.js, NEXT_PUBLIC_* env docs
   - Acceptance: standardized env names and documented defaults.
3. reproduce-source-build (PENDING)
   - Files/paths: canonical source tree build scripts; documented build command should produce artifacts matching operational artifact.
   - Acceptance: sha256 checksums match operational artifact.
4. diff-source-build-vs-deployed-artifact (PENDING)
   - Files/paths: docs/ADMIN/frontend/artifact-diffs/
   - Acceptance: diff report produced and reconciliations planned.
5. define-QA-cutover-plan (PENDING)
   - Files/paths: docs/ADMIN/frontend/QA-cutover-plan.md
   - Acceptance: QA tests and rollbacks rehearsed in staging.
6. define-rollback-after-cutover (PENDING)
   - Files/paths: ROLLBACK_TO_OPERATIONAL_ARTIFACT.md, scripts/restore_operational_artifact.sh
   - Acceptance: restore path verified in staging and smoke tests pass.

Notes on precedence and safety
- Track A tasks are higher immediate priority and must be completed (or operator-acknowledged) before any production cutover.
- Any operator-run archive/restore steps must be performed from the repository root and their outputs (archive dir and checksum file) committed or recorded under artifacts/operational/ for provenance.

Operator-required actions (explicit and prominent)
- Create the operational archive and checksum file (repo-root commands are documented in README.frontend-deploy.md). This is REQUIRED before any production cutover and is intentionally NOT performed by automation.
- Verify the restore script in a non-production staging environment using the created archive.
- Run smoke tests after restore to verify rollback readiness.

