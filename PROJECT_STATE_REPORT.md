# Workforce Project State Report

Generated: 2026-04-17T18:50:42Z (UTC)

## 1. Executive summary
- Evidence-first audit reconciled against local artifacts in /home/hn3t/dev_hub/artifacts/latest-repo-state-audit.
- All claims below are labeled: Confirmed / Inferred / Blocked / Needs verification.

## 2. Evidence base used for this report
Artifact files consulted (exact paths saved during audit):
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-branch.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-log.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-files.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-branch.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-status.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-log.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-files.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce-branch.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce-status.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt

Current report files consulted (exact paths):
- /home/hn3t/dev_hub/PROJECT_STATE_REPORT.md (this file, updated)
- /home/hn3t/workforce_api/PROGRESS_REPORT_API.md
- /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md

Source of truth: local filesystem artifacts and git state captured under /home/hn3t/dev_hub/artifacts/latest-repo-state-audit and live repo files under /home/hn3t. Remote systems were NOT queried.

## 3. Active repositories and their roles
- /home/hn3t/workforce_api — Backend FastAPI monorepo (Confirmed: directory and files exist; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt lines showing apps/, alembic/, pyproject.toml).
- /home/hn3t/workforce_frontend_app — Frontend monorepo / pnpm workspace (Confirmed: directory and artifacts present; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt and /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-files.txt).
- /home/hn3t/workforce — Packaged/legacy backend workspace (Confirmed: directory exists with .git and wsgi.py; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt).
- /home/hn3t/dev_hub — Docs and artifacts hub (Confirmed: directory exists and contains PROJECT_STATE_REPORT.md and artifacts/; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt and /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt).

## 4. Git status summary by repo
- /home/hn3t/workforce_api: branch = 'main' (Confirmed). Short status shows multiple modified files and several untracked files (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt).
- /home/hn3t/workforce_frontend_app: branch = 'master' (Confirmed). Short status shows added/modified artifact files under artifacts/ and lib/ (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-status.txt).
- /home/hn3t/workforce: branch = 'rbac/location-assignments' (Confirmed from artifact file).
- /home/hn3t/dev_hub: not a git repo according to the audit artifacts (Confirmed: no .git info captured; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt).

## 5. Backend state (workforce_api)
- apps/api/app/ structure present (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-files.txt lines listing api/, core/, db/, models/, main.py).
- Alembic migrations folder present (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-files.txt).
- Local DB files (workforce.db) present at repo root (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt line showing workforce.db).
- PROGRESS_REPORT_API.md: Present now at /home/hn3t/workforce_api/PROGRESS_REPORT_API.md (Created by this audit). Evidence: file exists on filesystem (Confirmed).
- Alembic heads/current status: Not executed in this audit (Needs verification).
- Tests (pytest) execution status: Not run here (Needs verification).

## 6. Frontend state (workforce_frontend_app)
- package.json, pnpm-workspace.yaml, tsconfig.json present (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-files.txt and /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt).
- Build artifacts present: dist and dist-staging directories exist (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt lines showing dist and dist-staging).
- Playwright artifacts and config present (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-files.txt lines listing playwright/ and playwright-or-browser-test-log.txt).
- PROGRESS_REPORT_FRONTEND.md content claims "Status: NO-GO for production". Classification: Inferred (supported by local state.json and artifacts but the push-rejection claim in that document is not independently verified here). Evidence: /home/hn3t/workforce_frontend_app/.copilot_frontend/state.json (contains last_completed_task and notes that browser validation remains NO-GO) — supports NO-GO inference.
- Vite/Next config files missing (vite.config.js / next.config.js absent) (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-files.txt shows MISSING entries).

## 7. Dev hub state
- dev_hub contains reports and saved artifacts (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt and overview.txt).
- latest audit artifacts symlinked at /home/hn3t/dev_hub/artifacts/latest-repo-state-audit (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt line for latest-repo-state-audit).

## 8. Deployment / hosting state
- Presence of dist archives and deploy docs is Confirmed locally (evidence: artifact zip and docs present under workforce_frontend_app and dev_hub).
- Remote deployment/live status: Needs verification (no remote checks performed).
- Artifact provenance linking build artifacts to CI run/commit SHA: Blocked / Not found in local artifacts (Confirmed missing; evidence: absence of metadata files in artifact dir and note in previous report).

## 9. Verification coverage and gaps
Confirmed (direct evidence):
- Repo directories exist and contain the listed files (apps/, alembic/, pyproject.toml, package.json, dist, playwright logs).
- Git branches: workforce_api=main, frontend=master, workforce=rbac/location-assignments (evidence: *-branch.txt files).

Inferred:
- Frontend validation NO-GO is inferred from .copilot_frontend/state.json and existing Playwright logs; the CI push-rejection claim is inferred (not directly evidenced).

Needs verification:
- Alembic migration current/heads output (run in venv).
- Test suite results (pytest) for backend and frontend.
- Whether dist artifacts were produced by CI and which commit/CI run produced them (remote-dependent).

Blocked:
- Any claim about remote workflow run status or remote repo push events (blocked without remote access or git remote logs).

## 10. Known blockers and risks
- Missing artifact provenance for dist artifacts (Confirmed).
- Playwright CI trigger previously failed per PROGRESS_REPORT_FRONTEND.md; the specific push-rejection reason is Inferred (requires remote log to Confirm).
- Multiple modified/untracked files in workforce_api (Confirmed; evidence: /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt) — risk for CI reproducibility.
- Environment drift: multiple .env and DB copies exist locally (Confirmed by overview listings), risk to reproducibility.

## 11. Stale or conflicting documentation
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-files.txt showed PROGRESS_REPORT_API.md was MISSING at time of artifact capture. That is now corrected: /home/hn3t/workforce_api/PROGRESS_REPORT_API.md exists (Confirmed). Action: note creation date; this audit updated it.
- /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md contains the PAT push-rejection claim (file lines 14-17). Classification: Inferred (not independently confirmed by this audit). Path: /home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md.
- Prior master report text referenced some claims as Confirmed that were based on planning docs rather than the artifact captures; those claims were reclassified here as Inferred or Needs verification. (See section 9 for specifics.)

## 12. Recommended next actions
Read-only (no mutation)
- Read-only: Inspect /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt and decide which local changes should be committed or stashed.
- Read-only: Review /home/hn3t/workforce_frontend_app/.copilot_frontend/state.json for validation notes.

Local-mutating (will change local state)
- Local-mutating: Create and activate venv in /home/hn3t/workforce_api; run `pip install -e .` and `pytest -q` and save output to /home/hn3t/dev_hub/artifacts.
- Local-mutating: Run `alembic current` / `alembic heads` to verify migrations and save the output.
- Local-mutating: Run frontend `pnpm install` and `pnpm build` in /home/hn3t/workforce_frontend_app` to reproduce artifacts if needed.

Remote-dependent (requires network/CI)
- Remote-dependent: Verify remote GitHub workflow run status and fix PAT/workflow permissions to re-run Playwright workflow and capture artifacts.
- Remote-dependent: Confirm provenance of existing dist artifacts by locating CI logs or build metadata on CI or artifact storage.

## 13. Appendix: key commands, paths, and evidence files
Key commands (read-only):
- ls -la /home/hn3t/workforce_api
- cat /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt
- git -C /home/hn3t/workforce_api branch --show-current

Key commands (local-mutating):
- python -m venv venv && source venv/bin/activate && pip install -e . && pytest -q
- alembic -c /home/hn3t/workforce_api/alembic.ini current
- cd /home/hn3t/workforce_frontend_app && pnpm install && pnpm build

Evidence files (copied to artifact dir):
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/overview.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_api-status.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/workforce_frontend_app-status.txt
- /home/hn3t/dev_hub/artifacts/latest-repo-state-audit/dev_hub-files.txt

Local verification artifacts saved at: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z

## Verification run summary
- Run timestamp: 2026-04-17T19:03:59Z (UTC)
- Artifacts dir: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z

## Backend verification results
- Python: see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-python-version-run.txt (Confirmed).
- Pip: see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-pip-version.txt (Confirmed).
- Import check: apps.api.app.main -> output in /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-import-check.txt (Confirmed: shows app title).
- pytest: run and produced import-time errors preventing test collection. See /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-pytest.txt (Failure: SQLAlchemy InvalidRequestError duplicate table definitions).
- alembic heads: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-alembic-heads.txt (Confirmed).
- alembic current: failed with import errors; see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-alembic-current.txt and /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-alembic-current-pypath.txt (Failure).
- seed-demo: attempted and failed to import apps.api.app.cli; see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/backend-seed-demo-2.txt (Blocked).

## Frontend verification results
- node version: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-node-version.txt (Confirmed).
- pnpm version: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-pnpm-version.txt (Confirmed).
- pnpm workspace check: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-pnpm-workspace-check.txt (Confirmed workspaces).
- typecheck: attempted and failed due to tsc receiving unsupported '--silent' option in workspace scripts; see /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/frontend-typecheck.txt (Failure).

## Newly confirmed facts
- apps/, alembic/, pyproject.toml, package.json present (Confirmed by artifacts).
- dist and dist-staging dirs exist (Confirmed previously).

## Failures encountered
- pytest: SQLAlchemy InvalidRequestError during test collection (duplicate table 'memberships').
- alembic current: ImportError / ModuleNotFoundError issues when loading env.py.
- seed-demo: ModuleNotFoundError on apps.api.app.cli when invoking python -m app.cli.main seed-demo.
- frontend typecheck fails due to workspace scripts passing '--silent' to tsc.

## Remaining gaps
- Need to resolve SQLAlchemy duplicate-table import issue before tests can run (Blocked).
- Alembic environment import errors need fixing (Needs verification after PYTHONPATH or code fixes).
- Seed-demo requires correct import path / module resolution (Needs verification).
- Artifact provenance remains not found (Remote-dependent).

## Recommended next actions
- Local-mutating: fix duplicate model imports (investigate packages/workforce vs apps paths); re-run pytest.
- Local-mutating: adjust alembic env.py import paths or PYTHONPATH to ensure app modules importable; re-run alembic current.
- Local-mutating: run seed-demo after resolving import path issues.
- Read-only: attach these artifacts to PRs for developers to triage: /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z

## Artifacts produced by this verification pass
- (full listing) /home/hn3t/dev_hub/artifacts/local-verification-20260417T185828Z/artifact-listing.txt

