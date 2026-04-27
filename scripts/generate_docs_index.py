#!/usr/bin/env python3
"""
Generate an index.json for dev_hub/dist/docs_extra with metadata for each file.
Run from repository root: python3 dev_hub/scripts/generate_docs_index.py
"""
import os, json, mimetypes, datetime
ROOT = os.path.join(os.path.dirname(__file__), '..', 'dist', 'docs_extra')
ROOT = os.path.normpath(ROOT)
entries = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel_dir = os.path.relpath(dirpath, ROOT)
    if rel_dir == '.':
        rel_dir = ''
    else:
        rel_dir = rel_dir.replace('\\','/')
    for d in sorted(dirnames):
        entries.append({
            'type': 'dir',
            'path': os.path.join(rel_dir, d).replace('\\','/').lstrip('/'),
            'name': d
        })
    for f in sorted(filenames):
        full = os.path.join(dirpath, f)
        try:
            stat = os.stat(full)
            size = stat.st_size
            mtime = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + 'Z'
        except Exception:
            size = None
            mtime = None
        mime, _ = mimetypes.guess_type(f)
        ext = os.path.splitext(f)[1].lower().lstrip('.')
        entries.append({
            'type': 'file',
            'path': os.path.join(rel_dir, f).replace('\\','/').lstrip('/'),
            'name': f,
            'ext': ext,
            'size': size,
            'mtime': mtime,
            'mime': mime
        })
# write index
out = os.path.join(ROOT, 'index.json')
with open(out, 'w') as fh:
    json.dump(entries, fh, indent=2)
print('Wrote', out)
