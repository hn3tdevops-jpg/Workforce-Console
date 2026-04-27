#!/usr/bin/env python3
"""
Generate progress_index.json by reading known progress files and summarizing basic metadata.
"""
import os, json, time
from pathlib import Path
ROOT = Path(__file__).parent.parent
OUT = ROOT / 'data' / 'generated' / 'progress_index.json'
OUT.parent.mkdir(parents=True, exist_ok=True)
files = [
    Path('/home/hn3t/workforce_api/PROGRESS_REPORT_API.md'),
    Path('/home/hn3t/workforce_frontend_app/docs/ADMIN/frontend/PROGRESS_REPORT_FRONTEND.md'),
    Path('/home/hn3t/dev_hub/PROJECT_STATE_REPORT.md'),
    Path('/home/hn3t/dev_hub/HN3T_MASTER_PLAN.md'),
    Path('/home/hn3t/workforce_api/docs/plans/HN3T_MASTER_PLAN.md')
]
entries = []
for p in files:
    try:
        if p.exists():
            txt = p.read_text(errors='ignore')
            # naive parse: first header line and last modified
            title = p.name
            lines = [l.strip() for l in txt.splitlines() if l.strip()]
            summary = lines[0] if lines else ''
            updated = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(p.stat().st_mtime))
            entries.append({'path': str(p), 'title': title, 'summary': summary, 'last_updated': updated})
    except Exception:
        continue
out = {'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ'), 'items': entries}
OUT.write_text(json.dumps(out, indent=2))
print('wrote', OUT)
