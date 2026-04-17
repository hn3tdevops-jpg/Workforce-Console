#!/usr/bin/env bash
set -euo pipefail

cd /home/hn3t/workforce_frontend_app

echo "--- git status ---"
git status --porcelain -b || true

BRANCH=$(git branch --show-current || true)
echo "Current branch: ${BRANCH}"

# Add files
git add app.py scripts/e2e_wrapper_test.js scripts/run_wrapper_e2e.sh .github/workflows/frontend-wrapper-e2e.yml docs/ADMIN/frontend/

# Commit (will fail if nothing to commit)
git commit -m "Add SPA fallback fix and wrapper E2E validation"

# Push branch to origin
if [ -z "${BRANCH}" ]; then
  echo "ERROR: could not determine current branch" >&2
  exit 2
fi

echo "Pushing branch ${BRANCH} to origin..."
git push -u origin "${BRANCH}"

# Trigger workflow
echo "Triggering GitHub Actions workflow for branch ${BRANCH}"
gh workflow run frontend-wrapper-e2e.yml --ref "${BRANCH}"

# List recent runs
gh run list --workflow frontend-wrapper-e2e.yml --limit 5

# Watch the most recent run (interactive)
gh run watch
