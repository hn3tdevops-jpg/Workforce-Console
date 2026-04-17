E2E Operator Runbook — Wrapper-based browser-level smoke/E2E

Purpose
- Validate the patched Flask wrapper serving dist-staging (FRONTEND_DIST_DIR=dist-staging) before any production cutover. Ensures SPA routes return index.html and key flows render.

Prerequisites
- A machine with Node.js (>=14) and npm installed.
- Either:
  - System Chromium/Chrome installed with required shared libraries (libffmpeg, libnss3, libatk-bridge2.0-0, libxss1, libasound2, libatk1.0-0, libcups2, libxcomposite1, libxdamage1, libxrandr2, libgbm1, libgtk-3-0, libpangocairo-1.0-0, libgdk-pixbuf2.0-0), OR
  - Use Playwright to download/ship browsers (npm install playwright && npx playwright install)
- Network: none required; tests run locally against 127.0.0.1 only.

Wrapper launch (example)
Run from repository root (/home/hn3t/workforce_frontend_app):

# Launch wrapper bound to localhost on port 8086 and log to file
FRONTEND_DIST_DIR=dist-staging FLASK_APP=app.py nohup flask run --host 127.0.0.1 --port 8086 > docs/ADMIN/frontend/artifact-diffs/e2e-wrapper.log 2>&1 &

# Confirm wrapper is up
curl -I http://127.0.0.1:8086/

E2E execution (Puppeteer / system Chromium)
1. Install dependencies (one-time):
   npm install --no-audit --no-fund puppeteer-core@^21.0.0
2. Ensure system Chromium is present and accessible (example path /usr/bin/chromium).
3. Run the provided E2E script:
   node scripts/e2e_wrapper_test.js

Alternative (Playwright-managed browsers)
1. Install Playwright and browsers (one-time):
   npm install --no-audit --no-fund playwright@latest
   npx playwright install
2. Modify scripts/e2e_wrapper_test.js to use Playwright if desired, or use Playwright test runner. (The puppeteer script will work against Playwright browsers if executablePath is pointed to the Playwright browser binary.)

Artifacts produced (stored under docs/ADMIN/frontend/artifact-diffs/)
- e2e-wrapper-launch-command.txt
- e2e-wrapper-env.txt
- e2e-wrapper.log
- e2e-console-errors.txt
- e2e-network-failures.txt
- e2e-summary.md
- screenshot-root.png
- screenshot-login.png
- e2e-asset-http-checks.txt

Pass/Fail criteria
- PASS if:
  - GET / returns 200 and page renders
  - GET /login returns 200 and page renders
  - GET /some/nonexistent/spa/route returns 200 (index.html served)
  - No fatal console errors preventing app render
  - All referenced JS/CSS assets return 200
- FAIL if any of the above fail.

Cutover decision rule
- If PASS: proceed to a staged promotion rehearsal (create timestamped archive of current dist, rsync staged artifact into place during a maintenance window, exercise checks, then either promote or restore using scripts/restore_operational_artifact.sh).
- If FAIL: do NOT cut over. Diagnose and fix the app/build/wrapper/configuration and re-run E2E until PASS.

Known blocker in this environment
- Attempted E2E run in this environment failed: Chromium launch error due to missing libffmpeg.so. Install system libffmpeg (and other browser deps) or use Playwright to provide browsers before running E2E.

Operator notes
- Tests are local-only and safe to run without network access.
- Keep the wrapper patch (app.py) in place during testing; it enables SPA fallback.
- All artifacts and logs will be written under docs/ADMIN/frontend/artifact-diffs/ for audit and QA.

Quick run (one-line)
From repo root, in a compatible environment with browser dependencies installed:

# runs wrapper, executes E2E, stops wrapper, and writes artifacts
scripts/run_wrapper_e2e.sh

Running in CI (GitHub Actions)
- A GitHub Actions workflow has been added: .github/workflows/frontend-wrapper-e2e.yml
- Trigger the workflow from the repository Actions tab -> "Frontend Wrapper E2E" -> Run workflow. You may optionally provide a branch input.
- The workflow runs on ubuntu-latest, installs Node dependencies and Chromium system libs, executes ./scripts/run_wrapper_e2e.sh, and uploads artifacts.
- Uploaded artifacts are available from the workflow run page under "Artifacts" (artifact name: frontend-wrapper-e2e-artifacts).

Contact
- If E2E fails with browser errors, collect e2e-wrapper.log and e2e-summary.md and open an incident with the platform/ops team.
