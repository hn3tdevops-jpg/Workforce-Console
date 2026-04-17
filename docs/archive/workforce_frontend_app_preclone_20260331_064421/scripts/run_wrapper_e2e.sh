#!/usr/bin/env bash
set -euo pipefail

# scripts/run_wrapper_e2e.sh
# Launch the Flask wrapper against dist-staging, run the Puppeteer E2E script,
# collect artifacts under docs/ADMIN/frontend/artifact-diffs/, and stop the wrapper.

OUT_DIR="docs/ADMIN/frontend/artifact-diffs"
mkdir -p "$OUT_DIR"

HOST=127.0.0.1
PORT=8086
WRAPPER_LOG="$OUT_DIR/e2e-wrapper.log"
E2E_LOG="$OUT_DIR/e2e-wrapper-e2e.log"

# Notes:
# - Puppeteer (system Chromium) usage: ensure a Chromium binary (e.g., /usr/bin/chromium) is installed and required libs (libffmpeg.so, etc.) are present.
# - Playwright alternative: install playwright and browsers (npm i playwright && npx playwright install) and ensure scripts/e2e_wrapper_test.js uses the correct executablePath.

echo "Starting wrapper on ${HOST}:${PORT} serving dist-staging" > "$WRAPPER_LOG"
FRONTEND_DIST_DIR=dist-staging FLASK_APP=app.py nohup flask run --host ${HOST} --port ${PORT} >> "$WRAPPER_LOG" 2>&1 &
WRAPPER_PID=$!
sleep 1

echo "Wrapper PID: $WRAPPER_PID" >> "$WRAPPER_LOG"

echo "Running E2E script (scripts/e2e_wrapper_test.js)" > "$E2E_LOG"
if node scripts/e2e_wrapper_test.js >> "$E2E_LOG" 2>&1; then
  E2E_EXIT=0
else
  E2E_EXIT=$?
fi

# Stop wrapper
if kill "${WRAPPER_PID}" >/dev/null 2>&1; then
  echo "Stopped wrapper PID ${WRAPPER_PID}" >> "$WRAPPER_LOG"
else
  echo "Failed to stop wrapper PID ${WRAPPER_PID}" >> "$WRAPPER_LOG"
fi

# Return E2E exit code
exit ${E2E_EXIT}
