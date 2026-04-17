You are working inside the new frontend project for Workforce.

Your job is to initialize this frontend migration/rebuild effort in a controlled, resumable way.

## Primary objectives

1. Scan the frontend repository and all clearly related local directories.
2. Catalogue current progress and the existing implementation state.
3. Determine what code, config, imports, paths, aliases, assets, API references, environment variables, and scripts need to change for the new setup location.
4. Create and maintain a durable implementation plan that can be resumed in later Copilot sessions.
5. Update repository guidance so future Copilot sessions follow the same rules automatically.
6. Start with safe organizational and compatibility work first. Do not begin broad rewrites without documenting the findings and plan.

## Related directories to inspect

Use the current repository as the primary source of truth.

Also inspect these related directories when they exist:
- legacy frontend location
- main Workforce/backend repository
- shared component or design-system directories
- shared types, API client, schema, or config directories
- documentation folders
- scripts folders
- package manager / workspace root
- CI/CD files
- deployment configs
- environment templates
- path alias configuration
- lint / format / tsconfig / bundler config

Treat missing paths as non-fatal. Note them in the audit.

## Mandatory output files

Create or update all of the following:

1. `docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md`
2. `docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md`
3. `docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md`
4. `docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md`
5. `.copilot_frontend/state.json`

Also update:
6. `.github/copilot-instructions.md`

## Audit requirements

`FRONTEND_RELOCATION_AUDIT.md` must include:

- repo overview
- detected framework/tooling stack
- current directory map
- route/page/app structure
- state management pattern
- API client pattern
- environment variable usage
- asset/static file usage
- import alias usage
- hard-coded absolute/relative paths
- references to old repo structure or old setup location
- backend integration touchpoints
- broken or likely broken imports
- config files needing normalization
- duplicate or stale code
- migration risks
- recommended normalization order

Be concrete. List exact files and directories whenever possible.

## Planning requirements

`FRONTEND_MASTER_PLAN.md` must include:

- goals
- assumptions
- constraints
- architecture notes
- dependency notes
- known blockers
- phased task list with checkboxes
- smallest safe next task first

The plan must be incremental and resume-friendly.

## Task queue requirements

`FRONTEND_TASK_QUEUE.md` must contain atomic tasks only.

Each task should:
- be small enough for one Copilot pass
- identify exact files likely to change
- include acceptance criteria
- include rollback notes where relevant

## Progress report requirements

`PROGRESS_REPORT_FRONTEND.md` must be append-only and dated.

Each entry must include:
- what was inspected
- what was changed
- what remains blocked
- recommended next step

## State file requirements

`.copilot_frontend/state.json` must track at minimum:
- current phase
- last completed task
- next suggested task
- key directories inspected
- files created/updated
- unresolved blockers
- last run timestamp

## Copilot instruction update requirements

Update `.github/copilot-instructions.md` so future Copilot sessions follow these rules:

- always read:
  - `docs/ADMIN/frontend/FRONTEND_RELOCATION_AUDIT.md`
  - `docs/ADMIN/frontend/FRONTEND_MASTER_PLAN.md`
  - `docs/ADMIN/frontend/FRONTEND_TASK_QUEUE.md`
  - `docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md`
  - `.copilot_frontend/state.json`
- perform work in small atomic steps
- update documentation and state after every task
- prefer repo-safe, reversible changes
- do not silently change API contracts
- do not weaken auth, RBAC, tenancy, or environment separation
- keep frontend aligned with backend contracts and shared types
- document assumptions instead of inventing hidden behavior

## Change execution rules

During this first initialization pass:

1. Inspect and document everything first.
2. Create the audit, plan, queue, progress report, state file, and Copilot instructions updates.
3. After documentation exists, you may complete only the safest low-risk fixes that are clearly required by relocation, such as:
   - import path normalization
   - tsconfig/jsconfig alias updates
   - package/workspace script path corrections
   - env template cleanup
   - obvious broken references to old directories
4. Do not perform large feature rewrites yet.
5. If a change is uncertain, record it in the plan instead of forcing it.

## Output style

- Be explicit.
- Use exact file paths.
- Keep tasks small and reviewable.
- Favor correctness over speed.
- Leave the repository in a cleaner, more resumable state than you found it.

Now begin by scanning the repository and related directories, then create/update the required files and perform only the safest initial normalization work.