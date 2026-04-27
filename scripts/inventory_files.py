#!/usr/bin/env python3
"""
Create a simple file inventory under data/generated/file_inventory.json
"""
import os, json, hashlib
from pathlib import Path
ROOTS = [Path('/home/hn3t/workforce_api'), Path('/home/hn3t/workforce_frontend_app'), Path('/home/hn3t/dev_hub')]
OUT = Path(__file__).parent.parent / 'data' / 'generated' / 'file_inventory.json'
OUT.parent.mkdir(parents=True, exist_ok=True)
entries = []
for r in ROOTS:
    if not r.exists():
        continue
    for p in list(r.rglob('*')):
        try:
            if p.is_file():
                st = p.stat()
                with open(p,'rb') as fh:
                    h = hashlib.sha256(fh.read()).hexdigest()
                entries.append({'path':str(p), 'project':r.name, 'mtime':int(st.st_mtime), 'size':st.st_size, 'sha256':h})
        except Exception:
            continue
OUT.write_text(json.dumps({'generated':__import__('time').strftime('%Y-%m-%dT%H:%M:%SZ'),'entries':entries}, indent=2))
print('wrote', OUT)
