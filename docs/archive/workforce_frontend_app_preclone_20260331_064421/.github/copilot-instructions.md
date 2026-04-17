## Frontend continuation rules

For all frontend migration/rebuild sessions, read these files before making changes:

- `docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md`
- `docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md`
- `docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md`
- `docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md`
- `.copilot_frontend/state.json`

### Required operating behavior

- Work in small, atomic, reviewable tasks.
- Update the audit/plan/queue/progress/state files after every completed task.
- Prefer the next unchecked task from `FRONTEND_TASK_QUEUE.md`.
- Keep changes scoped to the current task.
- Do not silently change backend API contracts.
- Do not weaken auth, tenancy, RBAC, environment separation, or deployment safety.
- When relocating code, normalize imports, aliases, config, env references, and scripts consistently.
- When uncertain, document the issue and add a task instead of guessing.
- Keep progress append-only in `PROGRESS_REPORT_FRONTEND.md`.

### Session resume rule

At the start of a new session:
1. Read the files above.
2. Identify the next unchecked atomic task.
3. Complete that task only.
4. Update all tracking files.
5. End with a clear next suggested task.

### Continuation behavior
- Do not stop to ask for confirmation between safe atomic tasks.
- Continue automatically through the next logical atomic task when no real blocker exists.
- Only ask for input when a blocker prevents correct progress.
- Always update progress/state/queue before ending a session.
- End with a concise summary and next recommended task, not a yes/no question.

### Provenance tracing behavior
- When canonical source and deployed artifacts differ, prioritize build/deploy provenance tracing before rewrites.
- Exhaust repository-visible and local evidence before requesting external CI or deployment access.
- Never ask vaguely for credentials; request the smallest specific evidence needed.
- Classify conclusions by confidence and cite exact file/path evidence.

### Operational canonical artifact vs canonical maintained source
- Operational canonical artifact: the artifact lineage currently proven to back production deployment (a built artifact directory, checksums, and local provenance evidence). Treat this as the operational truth for deployment until reconciliation is proven.
- Canonical maintained source: the repository/source tree intended to become the long-term maintained build source. This may differ from the operational artifact and requires reconciliation (environment, lockfiles, CI reproduction, QA) before cutover.
- When they differ: protect the operational canonical artifact (preserve, archive, and document it) and run reconciliation of the maintained source in parallel. Do not perform a production cutover until the maintained source reproduces matching artifacts and a QA/rollback plan is validated.
- Any session working on frontend relocation must record which concept is being referenced ("operational canonical artifact" or "canonical maintained source") and follow decision rules that favor operational safety.