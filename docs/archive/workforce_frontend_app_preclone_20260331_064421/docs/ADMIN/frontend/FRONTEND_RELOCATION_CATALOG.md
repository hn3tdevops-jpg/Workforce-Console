# Frontend Relocation Catalog

Summary of current frontend structure, important diffs, env and integration points.

1) Current frontend structure (local repo)
- Wrapper: app.py (Flask) serves compiled SPA from ./dist
- Deployed artifact: /home/hn3t/workforce_frontend_app/dist (assets, index.html, /assets/*)
- Operational artifact copy: /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public
- Candidate maintained sources:
  - /home/hn3t/workforce_new (canonical-likely)
  - /home/hn3t/projects_active (canonical-possible)
  - /home/hn3t/PROJECTS_ARCHIVE (archive-likely)

2) Old vs new path differences
- Deployed dist is placed at workforce_frontend_app/dist. Canonical source builds under subproject dist/ (workforce_new/.../dist).
- repo_imports artifact uses public/ subfolder (artifacts/.../dist/public) that was rsynced into deployed dist/.
- Keep deploy wrapper mapping: FRONTEND_DIST_DIR -> deployed dist root. No code change needed now.

3) Alias/import issues
- Multiple package managers/tools detected: pnpm (repo_imports build), npm/vite (workforce_new). This can cause lockfile and node_modules discrepancies.
- Path aliases (tsconfig) present in some source trees; verify tsconfig.json paths when reconciling source to artifact.
- Recommend NOT to change imports yet; reconcile canonical source and ensure build reproduces artifact before changing aliases.

4) Env / config issues
- Observed env variable patterns:
  - NEXT_PUBLIC_API_BASE_URL (Next.js client)
  - VITE_API_BASE / import.meta.env.VITE_API_BASE (Vite clients)
  - Some clients fallback to pythonanywhere host strings; these should be parameterized to same-origin or NEXT_PUBLIC_API_BASE_URL with fallback only for legacy testing.
- SPA bundles appear to use same-origin "/api/..." by default; ensure wrapper proxies or the backend serves API at same host.

5) Backend integration points
- API endpoints used by clients are primarily same-origin: "/api/..." (relative URLs observed in built bundle)
- Dev proxies observed: vite.config.js often proxies '/api' -> http://localhost:8000 (backend local dev)
- Ensure env standardization: choose canonical env var names and document in README.frontend-deploy.md

6) Broken or likely-broken relocation references
- Different bundle contents (deployed vs canonical) may contain differing feature sets or dependencies; replacing deployed artifact with canonical build without QA risks behavioral regressions.
- Hard-coded fallback host strings in some source trees may be stale (api-hn3t.pythonanywhere.com). These are not used by deployed artifact (same-origin), but should be normalized.

7) Recommendations (next atomic steps)
- Task 1: confirm-deployed-dist-origin — collect Replit/CI export logs for repo_imports artifact
- Task 2: map-repo_imports-artifact-to-maintained-source-tree — identify which source tree produced repo_imports artifact
- Task 3: standardize env var names across candidate sources (NEXT_PUBLIC_API_BASE_URL / VITE_API_BASE) after mapping
- Task 4: create README.frontend-deploy.md documenting operational artifact path and restore procedure

Evidence paths:
- Deployed dist: /home/hn3t/workforce_frontend_app/dist
- Artifact copy: /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public
- Candidate source: /home/hn3t/workforce_new/packages/workforce/workforce/frontend

