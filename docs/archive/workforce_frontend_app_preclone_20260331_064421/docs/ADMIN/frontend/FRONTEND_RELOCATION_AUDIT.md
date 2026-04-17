# Frontend Relocation Audit

Audit date: 2026-03-30T22:55:45Z

[Full audit above retained]

Dist provenance verification (this pass)

Deployed dist:
- Path: /home/hn3t/workforce_frontend_app/dist
- Size: ~3.3M
- Top-level assets:
  - assets/index-BtRHlc7J.js (sha256: 31fcdc31ac79b7c570f87139c03d2592bbe3fbc3878dcf13ed1d33eb1bd4aeee)
  - assets/index-BsqAJ34Y.css (sha256: c3a881ee1c69ac6892bae40f101107ab32824a1f8030cc15316a4824e6f062e7)

Built from canonical-likely tree (/home/hn3t/workforce_new/packages/workforce/workforce/frontend) — artifacts from fresh build (this pass):
- assets/index-DyiOv8K_.js (sha256: e0e5dff96402b0bf4341b83c8a6feead3973ac0b56c65fda7e185d219aeae2af)
- assets/index-BQBo6zK2.css (sha256: e03f3a8ef1b0dff7fb3d60e9f428bff47e447ef20a8e2213289db2ce27be0838)

Comparison result:
- Deployed artifacts DO NOT match freshly-built artifacts from canonical-likely source (checksums and file names differ).
- A copy of the deployed asset filenames was found in repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public (matching checksums).

Implication:
- The deployed /home/hn3t/workforce_frontend_app/dist was created elsewhere (a different build machine, CI artifact, or an older snapshot) and was copied into this repo's dist/ directory.

Next safe actions (recommended):
1. locate-build-artifact
   - Search CI pipelines and artifact stores for the built files matching deployed checksums or names (index-BtRHlc7J.js). Check GitHub Actions artifacts, Render deploy logs, and any artifact storage.
2. rebuild-and-compare (completed for canonical-likely tree)
   - Already performed: fresh build in workforce_new; artifacts differ.
3. If locate-build-artifact fails, consider replacing deployed dist with canonical build after confirming canonical decision and running QA.

CI logs checked (this pass):
- GitHub Actions workflow run id: 23722712796 (repo: hn3tdevops-jpg/Workforce-Showcase).
- Retrieved job logs for job id 69104109130 (job name: "deploy"). Logs saved to /tmp/1774911636223-copilot-tool-output-zgkrkf.txt.
- Findings: no artifact uploads were present in the workflow run; no references to deployed asset filenames (index-BtRHlc7J.js / index-BsqAJ34Y.css) were found in the downloaded logs.
- Implication: CI run did not produce or upload the deployed assets as artifacts; deployed files likely originated from a different pipeline, build host, or manual copy.

Repository-local provenance discovery (this pass):
- Found a matching artifact copy at /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public with identical checksums.
- Found artifact metadata at /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/.replit-artifact/artifact.toml indicating build commands (pnpm --filter @workspace/workforce-console run build) and publicDir pointing to artifacts/workforce-console/dist/public.
- Found shell history entries showing rsync commands that copied the repo_imports artifact into ~/workforce_frontend_app/dist.

Evidence summary:
- artifact.toml present (replit-style metadata)
- sha256 checksums match between repo_imports artifact and deployed dist
- bash history contains rsync copy commands

Conclusion:
- Local evidence strongly indicates the deployed artifact was produced by the repo_imports Replit-style artifact and copied into this repo's dist using rsync.

Recommended next steps:
- Document the operational release pipeline (create docs/ADMIN/frontend/README.frontend-deploy.md) capturing the rsync copy and the artifact location.
- Archive the operational artifact into artifacts/operational/ with checksum metadata and a timestamped restore procedure.
- Update state.json to record adoption of artifact lineage and set next task to document-release-pipeline.

=== Canonical build vs deployed artifact comparison ===

Exact compared paths:
- Canonical-likely source tree: /home/hn3t/workforce_new/packages/workforce/workforce/frontend (build: npm run build -> vite build)
- Canonical build output: /home/hn3t/workforce_new/packages/workforce/workforce/frontend/dist
- Deployed dist (served by wrapper): /home/hn3t/workforce_frontend_app/dist
- Local artifact copy (strong match): /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public

Major structural differences:
- Filenames and hashes: deployed/repo_imports use assets/index-BtRHlc7J.js and index-BsqAJ34Y.css (sha256: JS 31f...aeee, CSS c3a...2e7). Canonical build produced index-DyiOv8K_.js and index-BQBo6zK2.css (sha256: JS e0e5...2af, CSS e03f...838).
- Bundle sizes: deployed JS ~1.89 MB vs canonical JS ~151 KB (deployed bundle is ~12x larger), CSS similarly larger — indicates different source, dependencies, or bundling configuration.
- index.html layout: both use /assets/ path for assets and no explicit <base> tag; both use root-serving assumptions (same static_url_path) — compatible with existing Flask wrapper.
- Build tooling differences: canonical package.json (workforce_new frontend) uses npm/vite with minimal vite.config.ts (no explicit base/outDir). repo_imports artifact indicates a pnpm workspace build (pnpm --filter @workspace/workforce-console run build) and Replit artifact packaging (publicDir: artifacts/workforce-console/dist/public).

Env/API differences:
- Search of deployed assets and repo_imports artifact did not show hard-coded NEXT_PUBLIC_API_BASE_URL or VITE_API_BASE strings; many API calls are relative ("/api/..."), indicating same-origin calls expected when SPA and API share host via proxy. No authoritative hard-coded pythonanywhere host was found in the deployed JS during local grep for common host names.
- Canonical source client files (observed earlier) default to same-origin (BASE = ''), with some Next.js copies using NEXT_PUBLIC_API_BASE_URL with fallback to https://api-hn3t.pythonanywhere.com. Deployed artifact appears to rely on same-origin proxy behavior; no conflicting env contract detected in deployed bundle.

Packaging differences:
- repo_imports artifact produced by a workspace-level pnpm build and packaged into a publicDir path (Replit-style). Canonical build is a subfolder vite build producing dist/ assets under subproject path. Asset name hashing uses Vite default hashing but different content -> different hashes.

Serving-path differences:
- Both index.html in deployed and canonical build reference assets at /assets/*. The Flask wrapper (app.py) sets static_folder to FRONTEND_DIST_DIR and static_url_path="" and returns index.html for unknown paths — both artifact layouts are compatible with wrapper when placed under the configured dist folder.

Compatibility assessment and confidence:
- Deployed artifact is strongly-supported to be functionally equivalent to a built SPA but is not built from the current canonical-likely source (differences in bundle sizes and hashes are concrete). Confidence: high that repo_imports artifact is the immediate source for deployed dist (checksum + rsync history).
- Functional equivalence: Unknown without runtime QA. The deployed bundle is larger and may include extra features or dependencies not present in canonical-likely source. Risk of breaking UI if replaced by canonical build without QA is non-trivial. Confidence: medium for potential behavioral differences.

Recommended decision path: adopt-artifact-lineage (lower immediate risk)

Rationale:
- Adopting repo_imports artifact lineage preserves current production behavior and avoids immediate risk of replacing the live bundle with a differing canonical build.
- This should be a staged, documented decision: record repo_imports artifacts as canonical for deployment until the canonical-likely source (workforce_new) is reconciled and tested to produce matching artifacts.

Evidence gaps / external systems required to fully confirm provenance:
- Replit artifact logs or export metadata linking the artifact to a build run (artifacts/workforce-console record).
- Any CI run that uploaded the same artifact to a storage location (GHA artifacts, S3, Azure blob).


### Provenance confirmation (local evidence)

- rsync command found in shell history:
  - rsync -av --delete ~/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public/ ~/workforce_frontend_app/dist/
- artifact file timestamp and size (local copy):
  - /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/dist/public/assets/index-BtRHlc7J.js — 2026-03-30T18:09:35Z (size: 1,894,601 bytes)
- artifact metadata file timestamp:
  - /home/hn3t/repo_imports/Workforce-Showcase-master/artifacts/workforce-console/.replit-artifact/artifact.toml — 2026-03-29T23:29:18Z

These local artifacts and shell history strengthen the provenance linkage between the repo_imports artifact and the deployed /home/hn3t/workforce_frontend_app/dist. While the producing build system account is not yet proven, local evidence is strong enough to adopt the artifact lineage operationally while reconciliation proceeds.

