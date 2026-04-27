#!/usr/bin/env python3
"""
Validate uploaded devhub package zip.
Usage: python3 package_validator.py /path/to/upload_dir
Writes status.json into upload_dir describing validation result.
"""
import sys, os, json, zipfile, shutil
from pathlib import Path
ALLOWED_PROJECTS = {'workforce_api','workforce_frontend_app','dev_hub'}

def safe_name(p):
    return not (p.startswith('/') or '..' in Path(p).parts)


def main(upload_dir):
    upload_dir = Path(upload_dir)
    pkg = upload_dir / 'package.zip'
    status = {'state': 'uploaded'}
    statusf = upload_dir / 'status.json'
    try:
        if not pkg.exists():
            status.update({'state':'rejected','reason':'package.zip not found'})
            statusf.write_text(json.dumps(status))
            print('no package')
            return 2
        # unzip into tmp dir
        extract_dir = upload_dir / 'extracted'
        if extract_dir.exists():
            shutil.rmtree(extract_dir)
        extract_dir.mkdir()
        with zipfile.ZipFile(str(pkg)) as z:
            # quick path traversal check
            for n in z.namelist():
                if n.startswith('/') or '..' in Path(n).parts:
                    status.update({'state':'rejected','reason':'path traversal in zip: '+n})
                    statusf.write_text(json.dumps(status))
                    print('rejected path traversal', n)
                    return 3
            z.extractall(path=str(extract_dir))
        manifest = extract_dir / 'devhub-package.json'
        if not manifest.exists():
            status.update({'state':'rejected','reason':'manifest missing'})
            statusf.write_text(json.dumps(status))
            print('manifest missing')
            return 4
        m = json.loads(manifest.read_text())
        # minimal checks
        for f in ('name','version','target_project','package_type','files'):
            if f not in m:
                status.update({'state':'rejected','reason':'manifest missing field '+f})
                statusf.write_text(json.dumps(status))
                print('manifest missing field', f)
                return 5
        if m['target_project'] not in ALLOWED_PROJECTS:
            status.update({'state':'rejected','reason':'invalid target_project'})
            statusf.write_text(json.dumps(status))
            print('invalid target_project')
            return 6
        # validate files list paths
        bad = []
        for p in m.get('files'):
            if not safe_name(p):
                bad.append(p)
        if bad:
            status.update({'state':'rejected','reason':'files contain unsafe paths','bad':bad})
            statusf.write_text(json.dumps(status))
            print('unsafe files', bad)
            return 7
        # validate commands against command registry
        try:
            import importlib.util
            regp = Path(__file__).parent / 'command_registry.py'
            spec = importlib.util.spec_from_file_location('cmdreg', str(regp))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            REG = getattr(mod, 'REGISTRY', [])
            allowed_ids = set(e.get('id') for e in REG if e.get('id'))
        except Exception:
            allowed_ids = set()
        bad_cmds = []
        for c in m.get('commands', []):
            if isinstance(c, str):
                if c not in allowed_ids:
                    bad_cmds.append(c)
            elif isinstance(c, dict):
                cid = c.get('id')
                if cid and cid not in allowed_ids:
                    bad_cmds.append(cid)
        if bad_cmds:
            status.update({'state':'rejected','reason':'commands not allowed','bad_commands':bad_cmds})
            statusf.write_text(json.dumps(status))
            print('bad commands', bad_cmds)
            return 8
        # build preview
        preview = {'files': m.get('files'), 'commands': m.get('commands',[]), 'tests': m.get('tests',[])}
        status.update({'state':'validated','manifest':m,'preview':preview})
        statusf.write_text(json.dumps(status, indent=2))
        print('validated')
        return 0
    except Exception as e:
        status.update({'state':'rejected','reason':'exception','exc':str(e)})
        try:
            statusf.write_text(json.dumps(status))
        except Exception:
            pass
        print('exception', e)
        return 99

if __name__=='__main__':
    if len(sys.argv)<2:
        print('usage: package_validator.py /path/to/upload_dir')
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
