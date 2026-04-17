#!/usr/bin/env bash
set -euo pipefail

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
COPILOT_BIN="${COPILOT_BIN:-copilot5}"   # change to "copilot" if needed
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
FRONTEND_ROOT="${FRONTEND_ROOT:-$REPO_ROOT}"
LEGACY_FRONTEND_ROOT="${LEGACY_FRONTEND_ROOT:-}"
BACKEND_ROOT="${BACKEND_ROOT:-}"

WORK_DIR="$REPO_ROOT/.copilot_frontend"
DOCS_DIR="$REPO_ROOT/docs/ADMIN/frontend"
PROMPT_FILE="$WORK_DIR/current_prompt.md"
STATE_FILE="$WORK_DIR/state.json"
LOG_FILE="$WORK_DIR/run.log"
AUDIT_FILE="$DOCS_DIR/FRONTEND_RELOCATION_AUDIT.md"
PLAN_FILE="$DOCS_DIR/FRONTEND_MASTER_PLAN.md"
QUEUE_FILE="$DOCS_DIR/FRONTEND_TASK_QUEUE.md"
PROGRESS_FILE="$DOCS_DIR/PROGRESS_REPORT_FRONTEND.md"
INSTR_FILE="$REPO_ROOT/.github/copilot-instructions.md"

mkdir -p "$WORK_DIR" "$DOCS_DIR" "$(dirname "$INSTR_FILE")"

timestamp() {
  date -Iseconds
}

next_unchecked_task() {
  python3 - "$QUEUE_FILE" <<'PY'
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
if not path.exists():
    print("")
    raise SystemExit(0)
for line in path.read_text(encoding="utf-8").splitlines():
    if re.match(r"^\s*-\s\[\s\]\s", line):
        print(line.strip())
        raise SystemExit(0)
print("")
PY
}

json_escape() {
  python3 - <<'PY'
import json, sys
print(json.dumps(sys.stdin.read()))
PY
}

BOOTSTRAP_MODE="true"
if [[ -f "$QUEUE_FILE" ]] && grep -qE '^\s*-\s\[\s\]\s' "$QUEUE_FILE"; then
  BOOTSTRAP_MODE="false"
fi

NEXT_TASK="$(next_unchecked_task)"

cat > "$PROMPT_FILE" <<EOF
You are operating inside the Workforce frontend repository.

## Runtime context

- frontend repo root: $FRONTEND_ROOT
- legacy frontend root: ${LEGACY_FRONTEND_ROOT:-<not provided>}
- backend/workforce root: ${BACKEND_ROOT:-<not provided>}
- docs directory: $DOCS_DIR
- state file: $STATE_FILE

## General rules

- Read these files first when they exist:
  - $AUDIT_FILE
  - $PLAN_FILE
  - $QUEUE_FILE
  - $PROGRESS_FILE
  - $STATE_FILE
  - $INSTR_FILE
- Work in small, atomic, reviewable steps.
- Update docs and state after every completed task.
- Do not weaken auth, tenancy, RBAC, deployment safety, or API contract stability.
- Prefer documenting uncertainty over guessing.

EOF

if [[ "$BOOTSTRAP_MODE" == "true" ]]; then
cat >> "$PROMPT_FILE" <<'EOF'
## Mode: bootstrap

This appears to be the first frontend bootstrap pass.

Do all of the following:

1. Scan the repo and related directories.
2. Create/update:
   - docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md
   - docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md
   - docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md
   - docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md
   - .copilot_frontend/state.json
   - .github/copilot-instructions.md
3. Catalogue:
   - current frontend structure
   - old/new path differences
   - alias/import issues
   - env/config issues
   - backend integration points
   - broken or likely broken relocation references
4. After documentation exists, perform only the safest low-risk normalization changes.
5. End by identifying the next atomic task.

Keep initial code changes narrow and safe.
EOF
else
cat >> "$PROMPT_FILE" <<EOF
## Mode: resume

Continue from the documented state.

Current next unchecked task:
$NEXT_TASK

Required actions:
1. Re-read the audit, master plan, queue, progress report, state, and copilot instructions.
2. Complete only the current next unchecked atomic task.
3. Make narrowly scoped changes required for that task.
4. Update:
   - docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md
   - docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md
   - docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md
   - .copilot_frontend/state.json
5. Mark completed tasks clearly and identify the next suggested task.

Do not broaden scope beyond the current task unless required for correctness.
EOF
fi

cat >> "$PROMPT_FILE" <<EOF

## State update requirements

Ensure .copilot_frontend/state.json includes:
- phase
- last_completed_task
- next_suggested_task
- inspected_paths
- updated_files
- blockers
- last_run_at

Set last_run_at to $(timestamp).

Begin now.
EOF

echo "[$(timestamp)] Running Copilot frontend workflow..." | tee -a "$LOG_FILE"
echo "[$(timestamp)] Mode: $([[ "$BOOTSTRAP_MODE" == "true" ]] && echo bootstrap || echo resume)" | tee -a "$LOG_FILE"
echo "[$(timestamp)] Prompt file: $PROMPT_FILE" | tee -a "$LOG_FILE"

# Adjust this line to match your local Copilot CLI wrapper if needed.
"$COPILOT_BIN" "$(cat "$PROMPT_FILE")" | tee -a "$LOG_FILE"

echo "[$(timestamp)] Copilot frontend workflow finished." | tee -a "$LOG_FILE"