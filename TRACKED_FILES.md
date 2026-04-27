Location: dev_hub/dist/docs_data.js

What this is
- The developer hub uses dev_hub/dist/docs_data.js as the tracked-files manifest for documents shown in the hub.

How to refresh
- Edit dev_hub/dist/docs_data.js and add/remove entries (objects with title, href, summary, owner).
- Optionally run workforce_api/scripts/generate_docsdata.py (if present) and copy its output into the file.

Notes
- Use relative hrefs from dev_hub/dist (e.g. ../../workforce_api/README.md).
- Exclude: .git, node_modules, dist, build, coverage, virtualenvs, __pycache__, caches, temp files, generated artifacts, and secrets (.env).
