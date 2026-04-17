Cutover Readiness Assessment

Verdict: ready with caveats

Top risks:
- Behavioral drift: canonical build (dist-staging) bundles and filenames differ from operational artifact; may indicate missing runtime assets or feature differences.
- Runtime routing: SPA rewrite/fallback behavior depends on wrapper; local static server does not validate SPA rewrites.
- Config/env mismatch: build-time environment differences (pnpm vs npm, public base path, env flags) may cause runtime breakage.

Supporting reasons:
- dist-staging root served successfully and assets loaded (HTTP 200).
- Operational archive exists with checksums at artifacts/operational/20260331T023435Z and can be restored with scripts/restore_operational_artifact.sh.
- Differences in bundle filenames and checksums are consistent with a different build environment/tooling (expected for a fresh build) but require verification of functional parity.

Diff summary (dist-staging vs dist):
- Entry HTML differences:
  - dist/index.html title: "Workforce UI" vs dist-staging/index.html: "Workforce Console" and minor head tag differences (font preconnects present in operational dist, absent in staging or vice versa).
  - Script and CSS references differ by filename:
    - Operational: /assets/index-BtRHlc7J.js, /assets/index-BsqAJ34Y.css
    - Staging: /assets/index-DyiOv8K_.js, /assets/index-BQBo6zK2.css
- Asset filename/hash differences:
  - Checksums differ (see docs/ADMIN/frontend/artifact-diffs/checksum-diff.txt and artifacts/operational/20260331T023435Z-checksums.txt).
  - Staging assets: index-BQBo6zK2.css (sha256 e03f3a8...), index-DyiOv8K_.js (sha256 e0e5dff9...)
  - Operational assets: index-BsqAJ34Y.css (sha256 c3a881ee...), index-BtRHlc7J.js (sha256 31fcdc31...)
- Static content differences:
  - Both include favicon.svg and images/login-bg.png/opengraph.jpg; checksums differ where rebuilds occurred.
  - No large differences in file counts; both have assets/, images/, index.html.
- Interpretation: Differences appear consistent with a fresh build from a different toolchain/version rather than accidental deletion. Functional parity must be verified.

Functional risk checklist:
- Root route loading: PASSED in staging (index served, HTTP 200).
- Login page asset loading: Likely PASSED (assets referenced from index returned 200 in staging), but end-to-end login flow not executed.
- SPA fallback/rewrite dependency: WARNING — local static server does not test SPA rewrite; wrapper (app.py) must be tested in-situ to ensure fallback to index.html works for client-side routes.
- Environment/config dependency: WARNING — operational artifact built with pnpm workspace as per artifact metadata; staging was built with canonical npm/vite producing different bundles. Confirm environment variables and base path differences.
- Browser-level validation blocked by runtime dependencies: POSSIBLE — if canonical builds omitted polyfills, third-party libs, or environment-specific replacements, runtime errors could occur. Run a browser E2E or Playwright test to be sure.

Recommendation:
- Perform one more validation pass first: run wrapper in a local non-production environment pointing at dist-staging (set FRONTEND_DIST_DIR to dist-staging) and exercise core flows (root, login, create task, mark complete) via automated Playwright or scripted curl sequences. If flows pass, promote staged artifact. Otherwise, reconcile artifact lineage.

Next recommended task:
- execute-staging-preview-validation-part-2-local-serve-and-smoke-test (re-run with wrapper pointing at dist-staging and automated flow checks)

Appendix: Evidence locations
- artifact diffs: docs/ADMIN/frontend/artifact-diffs/
- staging file list: docs/ADMIN/frontend/artifact-diffs/staging-file-list.txt
- staging checksums: docs/ADMIN/frontend/artifact-diffs/staging-checksums.txt
- operational archive: artifacts/operational/20260331T023435Z and artifacts/operational/20260331T023435Z-checksums.txt
