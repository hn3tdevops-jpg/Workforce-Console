# Playwright/browser validation plan - progress report

last_completed_task: prepare-github-actions-browser-validation
next_suggested_task: rerun-browser-functional-validation-in-supported-environment

Status: NO-GO for production — browser validation has not yet passed and finalize-production-cutover-decision must wait until validation runs and passes.

Notes:
- An on-host Playwright run previously failed: browser process exited during startup (SIGTRAP).
- This document provides an off-host/container validation runbook and instructions for running the same browser-level checks against dist-staging.
- Artifacts produced by the off-host run should be copied into docs/ADMIN/frontend/artifact-diffs/ for review.
- Do not modify operational artifacts during validation; use the provided dist-staging copy.

CI trigger attempt:
- A local attempt was made to commit and push the prepared GitHub Actions workflow and helper scripts, and then trigger the workflow via the GitHub CLI.
- Push was rejected by the remote: "refusing to allow a Personal Access Token to create or update workflow `.github/workflows/playwright-browser-validation.yml` without `workflow` scope". The push failed and the workflow was not created on the remote.
- The GitHub CLI attempt to run the workflow also failed (404 / not authenticated) because the workflow file does not exist on the remote or the CLI is not authenticated.

Next steps to actually run the CI workflow:
1. Provide a PAT/token with `workflow` scope or push the `.github/workflows/playwright-browser-validation.yml` via a user account with sufficient permissions.
2. Alternatively, run the workflow manually on a runner using the commands in docs/ADMIN/frontend/OFF_HOST_PLAYWRIGHT_RUNBOOK.md or execute the workflow from GitHub Actions UI after the workflow file is present.
3. After the workflow runs, upload the artifacts into docs/ADMIN/frontend/artifact-diffs/ and rerun the validation checks.

Progress updates:
- Staging smoke validation (dist-staging) passed locally (HTTP and asset checks) — see docs/ADMIN/frontend/README.frontend-deploy.md for recorded verification steps.
- The imported frontend deployment docs were present but referenced a rollback script and an archive (artifacts/operational/<timestamp>) that were missing from the repository at the time of review.
- A repo-relative rollback helper has now been added at scripts/restore_operational_artifact.sh. This helper defaults to dry-run when safety checks fail and supports a --dry-run mode; it does not automatically restart services.
- Archive creation (timestamped artifacts/operational/*) and a rehearsal of the restore procedure must still be completed before rollback validation is considered done unless that work is performed after this change.
- Production remains NO-GO until a rollback rehearsal and successful browser validation (off-host or CI) are completed and recorded.

Next manual steps:
1. If archive(s) exist, create/verify checksums alongside the archive (sha256sum) and place the checksum file next to the archive.
2. Rehearse the restore flow against a staging copy (dist-staging) using the new script and validate checksums + HTTP smoke tests.
3. After rehearsal and browser validation pass, update this report and proceed with cutover gating as described in QA-cutover-plan.



---

Audit reconciliation (added 2026-04-17T18:50:42Z UTC):
- Evidence files: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-status.txt, /home/hn3t/workforce_frontend_app/.copilot_frontend/state.json
- Classification: Overall 'NO-GO' claim is Inferred (supported by local state.json noting validation not completed). The CI push-rejection claim (lines 14-17) is Inferred and requires remote logs to Confirm.
Local verification artifacts saved at: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z


---

Local verification (added 2026-04-17T19:03:59Z UTC):
- node version (confirmed): /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-node-version.txt
- pnpm version (confirmed): /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-pnpm-version.txt
- pnpm workspace packages enumerated: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-pnpm-workspace-check.txt
- typecheck attempted: failed due to tsc option error; see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-typecheck.txt

Classification:
- Frontend build artifacts: Confirmed present on disk.
- Frontend typecheck: Failed locally; requires fix to workspace scripts or tsc args (Local-mutating).
