# Project State Audit — Workforce / Hospitable
Generated: 2026-04-07T05:40:00Z (UTC)

This is an update to the prior project-state audit saved at `/home/hn3t/dev_hub/PROJECT_STATE_REPORT.md`. It includes results of non-invasive verification steps: git summaries, Alembic checks, pytest run, seed-demo attempt, DB snapshot, and focused provenance searches. All actions were read-only except writing this report and artifact files under `/home/hn3t/dev_hub/artifacts`.

Executive summary
- Actions performed: collected git summaries for key repositories, ran Alembic current/heads checks, ran pytest, attempted `python -m app.cli.main seed-demo`, captured outputs, and collected frontend artifact checksums and CI-provenance grep results. Artifacts are in `/home/hn3t/dev_hub/artifacts`.
- High-level result: repository code and docs are present and scaffolded, but automated verification failed due to Python packaging/import issues (ModuleNotFoundError: no module named 'app'). This prevents running Alembic and tests in-place without installing the package or setting PYTHONPATH. CI provenance search produced large results; relevant hits were saved for review.

Key verified items
- Git summary (workforce): branch `rbac/location-assignments`, remote origin points to https://github.com/HN3T-dev/workforce.git, last commit 2026-04-04 (adds scoped role assignment endpoint and tests).
- Git summary (frontend): branch `chore/playwright-ci-test`, remote origin https://github.com/hn3tdevops-jpg/Workforce-Showcase.git, local changes include `artifacts/workforce-console/src/App.tsx` and untracked `.env.production`.
- Alembic and pytest attempts ran but failed to import `app` package (see below).
- Seed-demo attempt failed similarly (ModuleNotFoundError when trying to locate `app.cli.main`).
- Large provenance search for keywords (workflow, commit, sha, artifact, dist) produced files: `ci_search.txt` (~531MB) and `ci_provenance_hits.txt` (~778MB). These contain potential provenance traces and require targeted review with binary exclusions; grep output was truncated into smaller samples in artifacts.

What failed (blocking issues)
1. Python import packaging: Alembic env.py and pytest conftest import `app` (the project package) but Python cannot resolve it when invoked directly from workspace without installing package or adding project paths to PYTHONPATH. Error excerpts:
   - `ModuleNotFoundError: No module named 'app'` (alembic/env.py and tests/conftest.py)
   - pytest aborted with ImportError while loading conftest
   - seed-demo: `Error while finding module specification for 'app.cli.main' (ModuleNotFoundError: No module named 'app')`
2. CI provenance search generated large output; however, it confirms many references to artifacts and logs exist in frontend and dev_hub but they are not clearly linked to signed CI build IDs. Manual review needed.
3. Frontend repo has untracked `.env.production` and other untracked files — potential secret or environment drift risk (do not open contents in this audit).

Detailed results (artifacts produced)
All artifacts written to: /home/hn3t/dev_hub/artifacts
- git_summary_workforce.txt — branch, remote, last commit for /home/hn3t/workforce
- git_summary_workforce_frontend_app.txt — branch, remote, status for frontend
- alembic_current.txt — Alembic `current` run output (shows ModuleNotFoundError)
- alembic_heads.txt — Alembic `heads` (empty/placeholder file)
- pytest_output.txt — pytest run output (ImportError: No module named 'app')
- seed_demo_output.txt — seed-demo run output (ModuleNotFoundError)
- workforce_db_snapshot.db — copied DB snapshot if present prior to seed (a snapshot was copied when present)
- frontend_dist_checksum.txt — checksum of frontend dist zip if present
- ci_search.txt, ci_provenance_hits.txt — large grep outputs for provenance keywords (binary files matched and made output large)
- listing.txt — directory listing of artifacts

Important excerpts (verbatim safe snippets)
- pytest_output.txt (excerpt):
  - `ModuleNotFoundError: No module named 'app'`
- alembic_current.txt (excerpt):
  - `File "/home/hn3t/workforce/alembic/env.py", line 9, in <module> from app.db.base import Base, import_models ModuleNotFoundError: No module named 'app'`
- git_summary_workforce.txt (excerpt): branch `rbac/location-assignments`, last commit `f8d168c...` "Add scoped role assignment endpoint, tests, CI, and migration"

Implications and immediate remediation steps
- The failure to import `app` is expected when invoking test/migration CLI from workspace without installing the package. Two safe remediation paths (pick one):
  1. Install the workspace package into the Python environment used for tests: `pip install -e .` (preferred in dev environments). This will make `app` importable and allow Alembic/tests to run.
  2. Run commands with PYTHONPATH including project root: `PYTHONPATH=$(pwd):$PYTHONPATH python -m pytest -q` and similar for alembic/seed-demo. This avoids install but achieves importability.
- After fixing importability, re-run Alembic current/heads, pytest, and seed-demo. Capture DB snapshot and attach to dev_hub.
- For CI provenance: inspect `ci_provenance_hits.txt` with targeted tools (ripgrep with JSON/lines focus) and search for `commit`, `run_id`, `workflow_run`, `replit` to extract build IDs. Consider rotating PAT and re-running workflow triggers for Playwright validation once PAT scopes are fixed.

Recommended next moves (concrete, ordered)
1. In a controlled dev venv, install the backend package: `python -m venv venv && source venv/bin/activate && pip install -e /home/hn3t/workforce` (or set PYTHONPATH). Then re-run Alembic and pytest. Save results to dev_hub/artifacts.
2. Re-run `python -m app.cli.main seed-demo` after installation; snapshot the DB and validate presence of Business/Location/User/Role/Room/Task/Inspection/Issue/EventLog entities. Save a short validation report to dev_hub.
3. Triaged CI provenance: open the large `ci_provenance_hits.txt` and search for `workflow_run`/`build id`/`commit` lines; extract build IDs and cross-check with `dist` artifact timestamps and zips. If PAT auth failed earlier, rotate or provide a scoped PAT to re-run workflow triggers and re-generate artifact metadata.

Security note
- Several `.env` files and DB backups exist in repositories. Treat them as sensitive; do not commit or display their contents. Recommend an immediate secure audit of `.env.production` and backups by a human with secrets access.

Files created/updated in dev_hub
- /home/hn3t/dev_hub/PROJECT_STATE_REPORT_2026-04-07.md (this report)
- Artifacts under `/home/hn3t/dev_hub/artifacts/` (git summaries, pytest_output.txt, alembic_current.txt, seed_demo_output.txt, workforce_db_snapshot.db if present, ci_search.txt, etc.)

Concise next step request (requires permission)
- Grant permission to (a) create a Python venv under `/home/hn3t/workforce/venv`, install the backend package with `pip install -e .`, re-run Alembic/current, pytest, and seed-demo; or (b) instruct preferred PYTHONPATH to run the commands without install. These actions will be executed in read-write in the workspace but only modify venv and dev_hub artifacts, not application source. If allowed, proceed with (a) to fully validate the demo flow.

---

If you want, proceed with creating a venv and installing the package so tests and migrations can be executed end-to-end. Otherwise, instruct which remediation to run.
