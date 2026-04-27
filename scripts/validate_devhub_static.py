#!/usr/bin/env python3
"""
Validate the static Dev Hub distribution in dist/.
Creates dist/validation_report_generated.txt and prints a summary.
"""
import os, json, re, sys

ROOT = os.path.dirname(os.path.dirname(__file__))
DIST = os.path.join(ROOT, 'dist')
DEVHUB = os.path.join(DIST, 'devhub_data.js')
REPORT_OUT = os.path.join(DIST, 'validation_report_generated.txt')

def extract_json_from_js(path, varname='window.devhubData'):
    text = open(path, 'r', encoding='utf-8').read()
    idx = text.find('=')
    if idx == -1:
        return None
    # assume pattern: window.devhubData = { ... };
    start = text.find('{', idx)
    end = text.rfind('};')
    if start == -1 or end == -1:
        # fallback: try to find first [ or {
        start = text.find('=')+1
        body = text[start:].strip()
        try:
            return json.loads(body)
        except Exception:
            return None
    body = text[start:end+1]
    try:
        return json.loads(body)
    except Exception as e:
        print('JSON parse error:', e)
        return None


def main():
    notes = []
    ok = True
    lines = []
    lines.append('Dev Hub static validation')

    # basic file checks
    for fname in ['index.html', 'documents.html', 'docs_data.js', 'devhub_data.js']:
        p = os.path.join(DIST, fname)
        if os.path.exists(p):
            lines.append(f'OK: {fname} exists')
        else:
            lines.append(f'MISSING: {fname}')
            ok = False

    # validate devhub_data.js references
    if os.path.exists(DEVHUB):
        data = extract_json_from_js(DEVHUB)
        if not data:
            lines.append('ERROR: could not parse devhub_data.js')
            ok = False
        else:
            docs = data.get('documents', [])
            lines.append(f'Found {len(docs)} documents declared in devhub_data.js')
            missing = []
            for d in docs:
                href = d.get('href') or ''
                # ignore JS template placeholders
                if '${' in href:
                    lines.append(f'IGNORED placeholder href: {href}')
                    continue
                path = os.path.normpath(os.path.join(DIST, href.lstrip('./')))
                if not os.path.exists(path):
                    missing.append(href)
            if missing:
                lines.append('BROKEN: the following doc hrefs are missing:')
                for m in missing:
                    lines.append('  - ' + m)
                ok = False
            else:
                lines.append('OK: all document hrefs resolved')

            # docs_extra index
            extra_idx = os.path.join(DIST, 'docs_extra', 'index.json')
            if os.path.exists(extra_idx):
                try:
                    with open(extra_idx, 'r', encoding='utf-8') as fh:
                        arr = json.load(fh)
                    lines.append(f'OK: docs_extra/index.json found ({len(arr)} entries)')
                except Exception as e:
                    lines.append('ERROR: docs_extra/index.json parse error: '+str(e))
                    ok = False
            else:
                lines.append('MISSING: docs_extra/index.json (repository-wide index)')

    else:
        lines.append('SKIP: devhub_data.js not present, skipping doc resolution')

    lines.append('\nSummary: ' + ('OK' if ok else 'ISSUES_FOUND'))
    report = '\n'.join(lines)
    with open(REPORT_OUT, 'w', encoding='utf-8') as fh:
        fh.write(report)
    print(report)
    print('\nWrote:', REPORT_OUT)
    return 0 if ok else 2

if __name__ == '__main__':
    sys.exit(main())
