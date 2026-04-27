#!/usr/bin/env python3
import os,json,time
from pathlib import Path
ROOT=Path('/home/hn3t')
OUT=Path('/home/hn3t/dev_hub/dist/scripts_index.json')
OUT2=Path('/home/hn3t/dev_hub/scripts/scripts_index.json')
EXTS={'.py','.sh','.pl','.rb','.js','.ps1','.bat'}
KEYWORDS=['deploy','build','test','start','run','seed','migrate','install','setup','backup','import','export','rebuild','index','seed-demo','cli','manage']

def first_lines(p, n=5):
    try:
        with open(p,'r',errors='ignore') as f:
            return [f.readline().strip() for _ in range(n)]
    except Exception:
        return []

out={'generated':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'by_project':{}, 'total':0}
for dirpath, dirnames, filenames in os.walk(ROOT):
    parts=Path(dirpath).relative_to(ROOT).parts
    if parts and parts[0] in ('.git','node_modules','venv','workspace_quarantine','recovery_snapshots','logs'):
        dirnames[:] = []
        continue
    for fn in filenames:
        fp=Path(dirpath)/fn
        try:
            st=fp.stat()
        except Exception:
            continue
        if st.st_size>2*1024*1024:
            continue
        ext=fp.suffix.lower()
        exec_flag=os.access(str(fp), os.X_OK)
        sb=None
        try:
            with open(fp,'rb') as f:
                h=f.readline(200)
                if h.startswith(b'#!'):
                    sb=h.decode(errors='ignore').strip()[2:]
        except Exception:
            pass
        if not (exec_flag or ext in EXTS or sb):
            continue
        fl=first_lines(fp)
        purpose='other'
        name=fn.lower()
        for k in KEYWORDS:
            if k in name or any(k in l.lower() for l in fl):
                purpose=k
                break
        rel=str(fp.relative_to(ROOT))
        proj=rel.split('/')[0] if '/' in rel else rel
        if proj=='': proj='root'
        entry={'name':fn,'path':rel,'project':proj,'size':st.st_size,'mtime':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(st.st_mtime)),'executable':bool(exec_flag),'shebang':sb,'purpose':purpose,'summary':' '.join(fl)}
        out['by_project'].setdefault(proj,[]).append(entry)
        out['total']+=1
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT2.parent.mkdir(parents=True, exist_ok=True)
open(OUT,'w').write(json.dumps(out,indent=2))
open(OUT2,'w').write(json.dumps(out,indent=2))
print('written', OUT, 'entries', out['total'])
