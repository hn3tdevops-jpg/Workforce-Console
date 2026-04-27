#!/usr/bin/env python3
"""
Apply a staged package: make backups and copy files into target project tree.
Usage: python3 package_installer.py /path/to/upload_dir
"""
import sys, json, shutil, os
from pathlib import Path
ROOT = Path('/home/hn3t')
DATA = Path(__file__).parent.parent / 'data'
RUNS = DATA / 'packages' / 'runs'
RUNS.mkdir(parents=True, exist_ok=True)

ALLOWED_PROJECTS = {'workforce_api':'workforce_api','workforce_frontend_app':'workforce_frontend_app','dev_hub':'dev_hub'}

def main(upload_dir):
    upload_dir = Path(upload_dir)
    statusf = upload_dir / 'status.json'
    if not statusf.exists():
        print('no status file')
        return 2
    status = json.loads(statusf.read_text())
    if status.get('state')!='validated':
        print('not validated')
        return 3
    m = status.get('manifest')
    target_proj = m.get('target_project')
    if target_proj not in ALLOWED_PROJECTS:
        print('invalid target project')
        return 4
    run_ts = __import__('time').strftime('%Y%m%dT%H%M%SZ')
    run_dir = RUNS / run_ts
    run_dir.mkdir(parents=True)
    backups = run_dir / 'backups'
    backups.mkdir()
    # apply files
    for rel in m.get('files'):
        src = upload_dir / 'extracted' / rel
        target_base = ROOT / ALLOWED_PROJECTS[target_proj]
        target = target_base / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            b = backups / (rel.replace('/','_'))
            shutil.copy2(str(target), str(b))
        shutil.copy2(str(src), str(target))
    # record install history
    hist = DATA / 'packages' / 'install_history.json'
    hist.parent.mkdir(parents=True, exist_ok=True)
    h = []
    if hist.exists():
        try:
            h = json.loads(hist.read_text())
        except Exception:
            h = []
    entry = {'ts': run_ts, 'package': m.get('name'), 'version': m.get('version'), 'project': target_proj}
    h.insert(0, entry)
    hist.write_text(json.dumps(h, indent=2))
    # update status
    status['state']='applied'
    statusf.write_text(json.dumps(status, indent=2))
    print('applied')
    return 0

if __name__=='__main__':
    if len(sys.argv)<2:
        print('usage: package_installer.py /path/to/upload_dir')
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
