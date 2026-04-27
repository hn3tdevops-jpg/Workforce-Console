#!/usr/bin/env python3
"""
Refresh Dev Hub indexes and inventories.
Writes logs to data/runs/<timestamp>/refresh.log
"""
import os, subprocess, time, json
from pathlib import Path
ROOT = Path(__file__).parent.parent
DATA = ROOT / 'data'
RUNS = DATA / 'runs'
RUNS.mkdir(parents=True, exist_ok=True)

ts = time.strftime('%Y%m%dT%H%M%SZ')
run_dir = RUNS / ts
run_dir.mkdir(parents=True, exist_ok=True)
logf = run_dir / 'refresh.log'

def run_cmd(cmd, cwd=None):
    with open(logf, 'a') as fh:
        fh.write('\n--- running: ' + ' '.join(cmd) + '\n')
        try:
            res = subprocess.run(cmd, cwd=cwd or str(ROOT), capture_output=True, text=True, timeout=600)
            fh.write(res.stdout or '')
            fh.write(res.stderr or '')
            return res.returncode == 0
        except Exception as e:
            fh.write('EXCEPTION: ' + str(e) + '\n')
            return False

# call existing generators if present
scripts = [
    ['python3', str(Path(__file__).parent / 'generate_docs_index.py')],
    ['python3', str(Path(__file__).parent / 'build_scripts_index.py')],
    ['python3', str(Path(__file__).parent / 'validate_devhub_static.py')],
]
results = {}
for cmd in scripts:
    name = Path(cmd[-1]).name
    ok = run_cmd(cmd)
    results[name] = ok

# run inventory_files if present
inv = Path(__file__).parent / 'inventory_files.py'
if inv.exists():
    results['inventory_files'] = run_cmd(['python3', str(inv)])

# run progress index generator
prog = Path(__file__).parent / 'generate_progress_index.py'
if prog.exists():
    results['progress_index'] = run_cmd(['python3', str(prog)])

# write status summary
out = {
    'ts': ts,
    'results': results,
}
OUT_DIR = ROOT / 'data' / 'generated'
OUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUT_DIR / 'devhub_status.json', 'w') as fh:
    json.dump(out, fh, indent=2)
with open(logf, 'a') as fh:
    fh.write('\nWROTE devhub_status.json\n')
print('refresh complete, log:', str(logf))
