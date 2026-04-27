#!/usr/bin/env python3
"""
Scan /home/hn3t for executable scripts and build a JSON index grouped by top-level project folder.
Writes to dev_hub/dist/scripts_index.json and dev_hub/scripts/scripts_index.json
"""
import os, json, stat, time
from pathlib import Path
ROOT = Path('/home/hn3t')
OUT = Path(__file__).parent.parent / 'dist' / 'scripts_index.json'
OUT2 = Path(__file__).parent / 'scripts_index.json'
EXCLUDE_DIRS = {'.git', 'node_modules', 'venv', 'venv3', '__pycache__', 'recovery_snapshots', 'workspace_quarantine', 'logs', 'run_plan.sh', 'upload'}
EXTS = {'.py', '.sh', '.pl', '.rb', '.js', '.ps1', '.bat'}
KEYWORDS = ['deploy','build','test','start','run','seed','migrate','install','setup','backup','import','export','rebuild','index','seed-demo','cli','manage','deploy','backup']

def is_text_file(path):
    try:
        with open(path, 'rb') as f:
            chunk = f.read(4096)
            if b"\0" in chunk:
                return False
    except Exception:
        return False
    return True


def detect_shebang(path):
    try:
        with open(path, 'rb') as f:
            l = f.readline()
            if l.startswith(b"#!"):
                return l.decode(errors='ignore').strip()[2:]
    except Exception:
        pass
    return None


def purpose_from_name(name, first_lines):
    lname = name.lower()
    for k in KEYWORDS:
        if k in lname:
            return k
    # try first lines
    txt = "\n".join(first_lines).lower()
    for k in KEYWORDS:
        if k in txt:
            return k
    return 'other'


def scan():
    by_project = {}
    total=0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        # prune
        parts = Path(dirpath).relative_to(ROOT).parts
        if parts and parts[0] in EXCLUDE_DIRS:
            dirnames[:] = []
            continue
        for fn in filenames:
            try:
                full = Path(dirpath) / fn
                # skip big files
                try:
                    if full.stat().st_size > 1024*1024:  # skip >1MB
                        continue
                except Exception:
                    continue
                # basic filters
                rel = str(full.relative_to(ROOT))
                ext = full.suffix.lower()
                executable = os.access(str(full), os.X_OK)
                shebang = detect_shebang(full)
                consider = False
                if executable:
                    consider = True
                elif ext in EXTS and is_text_file(full):
                    consider = True
                elif shebang:
                    consider = True
                if not consider:
                    continue
                # read first lines for description
                first_lines = []
                try:
                    with open(full, 'r', errors='ignore') as f:
                        for _ in range(5):
                            ln = f.readline()
                            if not ln:
                                break
                            first_lines.append(ln.strip())
                except Exception:
                    first_lines = []
                # determine project (top-level folder)
                parts = Path(rel).parts
                project = parts[0] if parts else ''
                if project == '':
                    project = 'root'
                entry = {
                    'name': fn,
                    'path': rel,
                    'project': project,
                    'size': full.stat().st_size,
                    'mtime': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(full.stat().st_mtime)),
                    'executable': bool(executable),
                    'shebang': shebang,
                    'purpose': purpose_from_name(fn, first_lines),
                    'summary': (' '.join(first_lines)).strip()
                }
                by_project.setdefault(project, []).append(entry)
                total += 1
            except Exception:
                continue
    out = {'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'total': total, 'by_project': by_project}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    try:
        OUT.write_text(json.dumps(out, indent=2))
    except Exception:
        pass
    try:
        OUT2.write_text(json.dumps(out, indent=2))
    except Exception:
        pass
    print('indexed', total)

if __name__ == '__main__':
    scan()
