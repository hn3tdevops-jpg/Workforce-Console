E2E run summary

Status: FAILED - unable to launch headless Chromium

Observed error (from e2e-wrapper.log):
- /usr/lib/chromium/chromium: error while loading shared libraries: libffmpeg.so: cannot open shared object file: No such file or directory

Impact:
- Puppeteer (puppeteer-core) could not start system Chromium due to missing shared library (libffmpeg). Without a browser binary available, browser-level E2E cannot proceed in this environment.

Minimal operator commands to reproduce locally (from repo root):
- Ensure system has required libs and a Chromium/Chrome binary with libffmpeg available. Example (Debian/Ubuntu):
  sudo apt-get update
  sudo apt-get install -y chromium ffmpeg libnss3 libatk-bridge2.0-0 libxss1 libasound2 libatk1.0-0 libcups2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libgtk-3-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0

- Alternatively, install Playwright browsers and run tests via Playwright (may download browsers):
  npm install --no-audit --no-fund playwright@latest
  npx playwright install
  node scripts/e2e_wrapper_test.js

Notes:
- After installing system libs/browsers, re-run the e2e script to capture screenshots and logs.
- The wrapper must be running and accessible at http://127.0.0.1:8086 (FRONTEND_DIST_DIR=dist-staging) when running the E2E script.
