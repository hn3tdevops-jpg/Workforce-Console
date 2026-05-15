# Repo Evaluation Report: Workforce-Console

> **Report date:** 2026-05-04
> **Evaluator:** GitHub Copilot Task Agent (audit/documentation pass only — no product-code changes made)
> **Labeling convention:** `[CONFIRMED]` = directly verified from repo files · `[INFERRED]` = conclusion drawn from evidence · `[NEEDS VERIFICATION]` = cannot be confirmed from this repo alone · `[MISSING]` = referenced but not present

---

## 1. Executive Summary

### Purpose of this repo

`Workforce-Console` is a **mixed-purpose repository** that acts as the primary coordination hub for the Workforce platform — a multi-tenant workforce management SaaS product. It contains:

- **Frontend source artifact fragments** (React/Vite/TypeScript library files under `workforce_frontend_app/artifacts/workforce-console/src/lib/`)
- **Frontend build artifacts** (compiled `dist/` and `dist-staging/` bundles, archived under `docs/archive/`)
- **A Flask static-file wrapper** (`app.py` — archived copy present; current canonical location on the deploy host is outside this repo `[NEEDS VERIFICATION]`)
- **All planning, architecture, and operations documentation** for the Workforce platform
- **A Node.js smoke-test script** for the `/api/v1/bootstrap` endpoint
- **One GitHub Actions CI workflow** that installs the backend Python package and runs targeted pytest tests for the `employee-link` feature

The frontend **SPA source is primarily hosted in the related `Workforce-Showcase` repo** and is imported into this repo as build artifacts. This repo is **not a self-contained build environment** — it does not contain a `package.json` at the root or `pnpm-workspace.yaml`; it stores pre-built frontend artifacts.

### Current overall health

**Partially ready / actively in progress.** Core infrastructure work (auth, RBAC, bootstrap API contract, identity model) is underway. Multiple blocking items remain open. Documentation is unusually thorough for this stage but references numerous external paths (`/home/hn3t/...`) that are outside the repo and cannot be verified here.

### Production readiness status

**Blocked**

Specific blockers (from `OPEN_DECISIONS.md` and `PROGRESS_REPORT_FRONTEND.md`):

1. **Browser validation never passed** — Playwright on-host run failed (SIGTRAP browser crash); off-host CI workflow was never pushed due to missing `workflow` scope on the PAT `[CONFIRMED]`
2. **Login endpoint returns HTTP 500 in production** — inferred root cause is DB/migration not run on the production host `[INFERRED from PROGRESS_REPORT.md]`
3. **UserEmployeeLink / EmployeeProfile models not merged** — D-008 is `In Progress`; missing models block RBAC and assignment correctness `[CONFIRMED from OPEN_DECISIONS.md]`
4. **Frontend artifact delivery path unresolved** — D-001 `Needs verification`; no CI artifact store confirmed `[CONFIRMED from OPEN_DECISIONS.md]`
5. **Frontend typecheck fails** — recorded locally; tsc option error `[CONFIRMED from PROGRESS_REPORT_FRONTEND.md]`

### Biggest risks

| # | Risk | Severity | Evidence |
|---|------|----------|----------|
| R-1 | Production login endpoint returning 500 | Critical | `PROGRESS_REPORT.md` 2026-04-18 entry |
| R-2 | Frontend browser validation never passed; NO-GO status standing | High | `PROGRESS_REPORT_FRONTEND.md` |
| R-3 | Identity/employee-link model incomplete; blocks RBAC correctness | High | `OPEN_DECISIONS.md` D-008 |
| R-4 | No CI pipeline for frontend build/test; single workflow covers only `employee-link` Python test | High | `.github/workflows/` contains only one workflow |
| R-5 | Deployment relies on paths external to this repo (`/home/hn3t/…`); no Dockerfile or container manifest in this repo | Medium | `README.frontend-deploy.md`, `CURRENT_STATE.md` |
| R-6 | Frontend source artifacts in repo are fragments only (4 lib files); the full app source lives elsewhere | Medium | `workforce_frontend_app/artifacts/workforce-console/src/lib/` (4 files only) |
| R-7 | `auth-context.tsx` has a syntax error (malformed object literal on line 166–168) that would break the TypeScript build | High | `workforce_frontend_app/artifacts/workforce-console/src/lib/auth-context.tsx` lines 165–170 |
| R-8 | Multiple planning docs with conflicting paths and status labels | Low/Medium | `OPEN_DECISIONS.md` D-004, D-007 |

### Highest-priority next actions

1. Fix the HTTP 500 on the production login endpoint (run `alembic upgrade head` + seed DB on host; or re-provision).
2. Push `employee-link` backend models + migration to unblock RBAC (D-008).
3. Fix the TypeScript syntax error in `auth-context.tsx` (see R-7 above).
4. Add a CI workflow for the frontend build (`pnpm --filter @workspace/workforce-console run build`) — either in this repo or in `Workforce-Showcase`.
5. Resolve D-001 (artifact delivery path) to enable repeatable deployments.
6. Run off-host Playwright validation per the runbook and record a passing result.

### Repo type

**Mixed-purpose** — planning/docs hub + pre-built frontend artifact store + partial TypeScript library source + one backend CI workflow.

---

## 2. Repository Identity

### GitHub repository name

`hn3tdevops-jpg/Workforce-Console`

### Shell command outputs

```
$ pwd
/home/runner/work/Workforce-Console/Workforce-Console

$ git status --short
(no output — working tree clean)

$ git branch --show-current
copilot/create-repo-evaluation-report-again

$ git remote -v
origin  https://github.com/hn3tdevops-jpg/Workforce-Console (fetch)
origin  https://github.com/hn3tdevops-jpg/Workforce-Console (push)

$ git log -1 --oneline
2c3d8a5 (HEAD -> copilot/create-repo-evaluation-report-again, origin/copilot/create-repo-evaluation-report-again) Hydrate effective permissions in auth context
```

### Key files found (`find . -maxdepth 4 …`)

```
./PROGRESS_REPORT.md
./docs/00_START_HERE/CANONICAL_SOURCES.md
./docs/00_START_HERE/CURRENT_STATE.md
./docs/00_START_HERE/EXECUTION_QUEUE.md
./docs/00_START_HERE/OPEN_DECISIONS.md
./docs/00_START_HERE/README.md
./docs/00_START_HERE/specs/bootstrap.json
./docs/00_START_HERE/specs/employee-link-api-examples.json
./docs/00_START_HERE/specs/employee-link.md
./docs/planning/HN3T_MASTER_PLAN.md
./docs/planning/README.md
./docs/planning/workforce_consolidated_master_plan_2026-04-17.md
./docs/workstreams/README.md
./docs/workstreams/future-modules/AI_WIDGET_AGENT_IMPLEMENTATION_PLAN.md
./docs/workstreams/workforce-web-ui/CI_TRIGGER_ATTEMPT.md
./docs/workstreams/workforce-web-ui/OFF_HOST_PLAYWRIGHT_RUNBOOK.md
./docs/workstreams/workforce-web-ui/PROGRESS_REPORT_FRONTEND.md
./docs/workstreams/workforce-web-ui/QA-cutover-plan.md
./docs/workstreams/workforce-web-ui/README.frontend-deploy.md
./docs/workstreams/workforce-web-ui/ROLLBACK_TO_OPERATIONAL_ARTIFACT.md
./docs/workstreams/workforce-web-ui/WORKFORCE_WEB_UI_COPILOT_IMPLEMENTATION.md
./docs/workstreams/workforce-web-ui/artifact-diffs/browser-console-errors.txt
./docs/workstreams/workforce-web-ui/artifact-diffs/failed-network-requests.txt
./docs/workstreams/workforce-web-ui/artifact-diffs/playwright-or-browser-test-log.txt
./docs/workstreams/workforce-web-ui/artifact-diffs/route-validation-summary.md
./docs/workstreams/workforce-web-ui/artifact-diffs/staging-http-server.log
./docs/workstreams/workforce-web-ui/artifact-diffs/screenshots/README.txt
./workforce_frontend_app/artifacts/workforce-console/src/lib/api-client.ts
./workforce_frontend_app/artifacts/workforce-console/src/lib/auth-context.tsx
./workforce_frontend_app/artifacts/workforce-console/src/lib/business-settings-context.tsx
./workforce_frontend_app/artifacts/workforce-console/src/lib/permissions.ts
./workforce_frontend_app/scripts/smoke-bootstrap.js
./.github/workflows/validate-employee-link-editable-install.yml
```

> No `package.json`, `pnpm-workspace.yaml`, `pnpm-lock.yaml`, `tsconfig*.json`, `vite.config.*`, `pyproject.toml`, `requirements*.txt`, `alembic.ini`, `Dockerfile`, or `docker-compose*.yml` found at repo root or within `workforce_frontend_app/` (excluding the `docs/archive/` subtree which contains a legacy archived copy).

### Main languages

| Language | Evidence |
|----------|----------|
| TypeScript/TSX | `workforce_frontend_app/artifacts/workforce-console/src/lib/*.ts(x)` `[CONFIRMED]` |
| JavaScript (Node.js) | `workforce_frontend_app/scripts/smoke-bootstrap.js` `[CONFIRMED]` |
| Python | Referenced in CI workflow (`python 3.12`, `pytest`); backend (`workforce_api/`) referenced in docs but **not present in this repo** `[INFERRED from docs + CI]` |
| Markdown | Dominant file type in this repo `[CONFIRMED]` |

### Frameworks / libraries

| Item | Evidence | Status |
|------|----------|--------|
| React 18+ (with hooks) | `auth-context.tsx` uses `createContext`, `useContext`, `useEffect`, `useState` | `[CONFIRMED]` |
| `@tanstack/react-query` | Imported in `auth-context.tsx`, `business-settings-context.tsx` | `[CONFIRMED]` |
| Vite (SPA bundler) | `VITE_API_BASE_URL` / `VITE_DEMO_MODE` env vars in source; build command `pnpm --filter @workspace/workforce-console run build` | `[CONFIRMED]` |
| pnpm workspaces | Build command references `@workspace/workforce-console`; `@workspace/api-client-react` import in `auth-context.tsx` | `[CONFIRMED]` |
| FastAPI (Python backend) | Referenced extensively in docs; `workforce_api/` path referenced in CI workflow trigger; not present in this repo | `[INFERRED]` |
| Alembic | Referenced in docs/planning for DB migrations; `alembic.ini` not present in this repo | `[INFERRED]` |
| Flask | `app.py` static wrapper referenced in `README.frontend-deploy.md` | `[INFERRED — file not present in this repo]` |
| SQLAlchemy | RBAC/tenancy model described in `HN3T_MASTER_PLAN.md` | `[INFERRED]` |
| Playwright | Archived `package.json` and CI runbook docs present | `[CONFIRMED for archived copy]` |

### Package manager / build system

- **pnpm workspaces** — evidenced by build command `pnpm --filter @workspace/workforce-console run build` `[CONFIRMED]`
- Root `package.json` / `pnpm-workspace.yaml` are **not present in this repo** — they exist in the source repo (`Workforce-Showcase`) `[NEEDS VERIFICATION]`

### Runtime / deployment model

- **Frontend:** Pre-built Vite SPA. Served by a Python Flask static file wrapper (`app.py`). Deployed on **PythonAnywhere** (`hn3t.pythonanywhere.com`) `[CONFIRMED from README.frontend-deploy.md, CURRENT_STATE.md]`
- **Backend:** FastAPI app (`workforce_api/`). Also deployed on PythonAnywhere (separate WSGI process). `[INFERRED from docs; `workforce_api/` not in this repo]`
- **No Docker or container infrastructure found in this repo** `[CONFIRMED by absence]`

### Primary entrypoints

| Path | Role | Status |
|------|------|--------|
| `workforce_frontend_app/artifacts/workforce-console/src/lib/auth-context.tsx` | React auth/session provider — central to all frontend permission checks | `[CONFIRMED]` |
| `workforce_frontend_app/artifacts/workforce-console/src/lib/api-client.ts` | Frontend HTTP client with token injection and 401 handling | `[CONFIRMED]` |
| `workforce_frontend_app/artifacts/workforce-console/src/lib/permissions.ts` | Permission matching utilities (wildcard `scope:*` support) | `[CONFIRMED]` |
| `workforce_frontend_app/artifacts/workforce-console/src/lib/business-settings-context.tsx` | React context for per-business settings and enabled modules | `[CONFIRMED]` |
| `workforce_frontend_app/scripts/smoke-bootstrap.js` | Node.js smoke test for `GET /api/v1/bootstrap` | `[CONFIRMED]` |
| `workforce_api/apps/api/app/main.py` | FastAPI app entrypoint (referenced in docs + CI; **not in this repo**) | `[INFERRED]` |

### Main config files

| File | Present in repo | Notes |
|------|-----------------|-------|
| `.github/workflows/validate-employee-link-editable-install.yml` | ✅ | Only CI workflow in repo |
| `pnpm-workspace.yaml` | ❌ | Lives in `Workforce-Showcase` source repo |
| `vite.config.*` | ❌ | Lives in `Workforce-Showcase` source repo |
| `tsconfig*.json` | ❌ | Lives in `Workforce-Showcase` source repo |
| `alembic.ini` | ❌ | Lives in backend repo (`Workforce-backup` or local host) |
| `Dockerfile` / `docker-compose.yml` | ❌ | Not present anywhere in this repo |

### Documentation / source-of-truth files

| File | Purpose |
|------|---------|
| `docs/00_START_HERE/README.md` | Operator entry point and reading order |
| `docs/00_START_HERE/CURRENT_STATE.md` | Evidence-based snapshot of all known system state |
| `docs/00_START_HERE/EXECUTION_QUEUE.md` | Approved ordered work queue |
| `docs/00_START_HERE/OPEN_DECISIONS.md` | Blocking decisions log |
| `docs/00_START_HERE/CANONICAL_SOURCES.md` | Single source of truth registry |
| `docs/planning/HN3T_MASTER_PLAN.md` | Master architecture and governance doc |
| `docs/planning/workforce_consolidated_master_plan_2026-04-17.md` | Consolidated operational plan |
| `PROGRESS_REPORT.md` | Running session log (very long; predates repo structure) |
| `docs/workstreams/workforce-web-ui/PROGRESS_REPORT_FRONTEND.md` | Frontend QA/validation status log |
| `docs/workstreams/workforce-web-ui/README.frontend-deploy.md` | Operational deployment runbook |
| `docs/workstreams/workforce-web-ui/QA-cutover-plan.md` | Gated production cutover checklist |
| `docs/00_START_HERE/specs/employee-link.md` | Canonical spec for identity/employee-link model |
| `docs/00_START_HERE/specs/bootstrap.json` | Bootstrap API contract JSON schema |

---

## 3. Architecture Overview (inferred from docs and source)

### System planes (from `HN3T_MASTER_PLAN.md`)

The platform is described as having four logical planes on one backend:

1. **Control Plane** — platform admin, cross-tenant management, agent registry
2. **Tenant Plane** — business owner/manager console (scheduling, RBAC, locations, reports)
3. **Worker Plane** — employee self-service (schedule, timeclock, requests)
4. **Agent Plane** — AI/integration agents with scoped API credentials

### Multi-tenancy model

- Entity hierarchy: `Business → Location → User / EmployeeProfile`
- Every tenant-owned table includes `business_id`; location-scoped rows add `location_id`
- RBAC: permissions derive from roles only; roles can be BUSINESS-scoped or LOCATION-scoped; users can hold different roles at different locations `[CONFIRMED from HN3T_MASTER_PLAN.md]`

### Frontend architecture (from source + docs)

- React SPA built with Vite inside a pnpm workspace (`@workspace/workforce-console`)
- `AuthProvider` → `BusinessSettingsProvider` → app shell pattern
- Session hydration: `GET /api/v1/bootstrap` (no-token path) or `GET /api/v1/auth/me` + `GET /api/v1/me/effective-permissions` (with token) + `GET /api/v1/auth/me/access-context` (employment scope)
- Demo mode (`VITE_DEMO_MODE=true`) bypasses all API calls with hardcoded `DEMO_SESSION` pointing to "Silver Sands Motel"
- Business-level module gating via `enabled_modules` list on `BusinessSettings`
- SPA served by Python Flask wrapper on PythonAnywhere

### Backend architecture (inferred from docs)

- FastAPI app at `workforce_api/apps/api/app/` — **not present in this repo** `[NEEDS VERIFICATION in Workforce-backup]`
- Canonical bootstrap route: `GET /api/v1/bootstrap` (returns `user`, `businesses`, `locations`, `roles`, `features`)
- Auth routes: `/api/v1/auth/login`, `/api/v1/auth/me`, `/api/v1/auth/register`, `/api/v1/auth/switch-business`, `/api/v1/auth/me/access-context`
- Business settings: `GET/PATCH /business/{id}/settings`
- Employee/RBAC routes: planned but not yet merged (D-008)
- DB: SQLite (local dev), likely SQLite on PythonAnywhere; Alembic migrations

---

## 4. CI / Automation

### Confirmed CI

| Workflow | File | Trigger | What it does |
|----------|------|---------|--------------|
| `validate/employee-link:editable-install` | `.github/workflows/validate-employee-link-editable-install.yml` | `workflow_dispatch` + PR touching `workforce_api/**` | Sets up Python 3.12, installs `workforce_api` editable with dev extras, runs `pytest -q tests/test_employee_link.py` |

### Missing CI (noted as gaps)

- No frontend build CI (no workflow to run `pnpm … build` or `tsc`) `[CONFIRMED by absence]`
- Playwright browser validation workflow was blocked from push (PAT lacked `workflow` scope) `[CONFIRMED from PROGRESS_REPORT_FRONTEND.md]`
- No deployment workflow (no auto-deploy to PythonAnywhere)

---

## 5. Known Issues and Gaps

### Source code issues

| Issue | File | Severity | Notes |
|-------|------|----------|-------|
| Syntax error in `auth-context.tsx` | `workforce_frontend_app/artifacts/workforce-console/src/lib/auth-context.tsx` line ~166 | High | Malformed object literal — the `memberships` map callback closing parenthesis is missing before `roles:` key, making this a syntax error that would fail `tsc` |
| `business-settings-context.tsx` defines its own local `fetchApi` that ignores auth tokens | `business-settings-context.tsx` lines 9–21 | Medium | Unlike the canonical `fetchApi` in `api-client.ts`, this local copy does not attach `Authorization` headers — may cause 401s on settings endpoints |
| Frontend typecheck failing | recorded in `PROGRESS_REPORT_FRONTEND.md` | High | tsc option error; build may not be reproducible |
| `@workspace/api-client-react` import in `auth-context.tsx` (line 5) | `auth-context.tsx` | Medium | Cross-workspace import — requires the full pnpm workspace from `Workforce-Showcase`; will fail as a standalone fragment |

### Deployment / operational issues

| Issue | Severity | Evidence |
|-------|----------|----------|
| Production login returns HTTP 500 | Critical | `PROGRESS_REPORT.md` 2026-04-18 |
| Browser validation never passed (SIGTRAP on Playwright launch) | High | `route-validation-summary.md`, `PROGRESS_REPORT_FRONTEND.md` |
| Deployment depends on external host paths not tracked in this repo | Medium | `README.frontend-deploy.md` (`/home/hn3t/…`) |
| No `Dockerfile` or container spec in repo | Medium | Confirmed by absence |
| CORS: production SPA calls `https://hn3t.pythonanywhere.com` directly; requires either CORS header or server-side proxy | Medium | `README.frontend-deploy.md` |

### Planning / documentation issues

| Issue | Severity | Evidence |
|-------|----------|----------|
| `PROGRESS_REPORT.md` contains unrelated historical shell sessions from other projects (pre-dates this repo) | Low | File contents 2026-03-02 entries |
| Referenced PDFs (`REFERENCE_CATALOGUE.pdf`, `WF_Server_Boundary_Reference_Catalogue.pdf`) missing from repo | Low | `OPEN_DECISIONS.md` D-003, `CANONICAL_SOURCES.md` |
| Multiple unresolved open decisions (D-001 through D-008); D-001, D-003, D-006 all unassigned | Medium | `OPEN_DECISIONS.md` |
| `workforce_api/` (canonical backend) is referenced throughout but is **not present in this repo** | High | `CURRENT_STATE.md`, `CANONICAL_SOURCES.md` |

---

## 6. Cross-Repo Dependencies

This repo explicitly depends on and/or references:

| Related repo | Dependency type | What to check there |
|---|---|---|
| `hn3tdevops-jpg/Workforce-Showcase` | **Frontend source** — the full Vite/React SPA source, `pnpm-workspace.yaml`, `tsconfig.json`, `vite.config.*`, and all non-lib components live here | Confirm build passes; check if `auth-context.tsx` / `permissions.ts` fragments here match what is in Showcase; check if `@workspace/api-client-react` is present and typed |
| `hn3tdevops-jpg/Workforce-backup` | **Backend source** — `workforce_api/` (FastAPI app, models, schemas, migrations) is referenced in docs/CI but not present in this repo | Confirm `alembic upgrade head` has been run on PythonAnywhere; confirm `test_employee_link.py` exists and passes; confirm `/api/v1/bootstrap` GET works end-to-end; confirm `/api/v1/auth/login` no longer returns 500 |

> **Cannot verify from this repo alone:**
> - Whether `workforce_api/tests/test_employee_link.py` passes (CI references it but the file is in `Workforce-backup`)
> - Whether DB migrations are up-to-date on the production host
> - Whether the full frontend builds cleanly in `Workforce-Showcase`
> - Whether the Flask wrapper (`app.py`) on PythonAnywhere is correctly proxying `/api` to the FastAPI backend

---

## 7. Assessment Summary

| Dimension | Status | Notes |
|-----------|--------|-------|
| Repo purpose clarity | ✅ Clear (once understood) | Mixed-purpose: docs hub + pre-built artifact store + lib fragments |
| Documentation quality | ✅ High | Unusually detailed for this stage; labeling convention (`[CONFIRMED]` etc.) is excellent |
| Frontend source completeness | ⚠️ Partial | Only 4 lib files present; full SPA lives in `Workforce-Showcase` |
| Backend presence | ❌ Absent | `workforce_api/` not in this repo; lives in `Workforce-backup` |
| CI coverage | ⚠️ Minimal | One workflow covering only `employee-link` Python test; no frontend build CI |
| Auth/RBAC design | ✅ Solid design | Multi-layered permission checks in `permissions.ts` + `auth-context.tsx`; employee scope layer planned |
| Identity model completeness | ⚠️ In progress | `UserEmployeeLink`/`EmployeeProfile` designed (spec present) but not confirmed merged |
| Deployment reproducibility | ⚠️ Partial | Runbook documented; relies on external host paths; no container spec |
| Production readiness | ❌ Blocked | Login 500, browser validation NO-GO, frontend typecheck failing |
