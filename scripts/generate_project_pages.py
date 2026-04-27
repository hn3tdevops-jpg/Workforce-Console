#!/usr/bin/env python3
"""
Generate static project dashboard pages and optionally discover sibling repositories to seed projects.json.
"""
import json
from pathlib import Path
import argparse
import re
import datetime

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
INDEX = DIST / 'index.html'
PROJECTS_JSON = ROOT / 'projects.json'
OUT_DIR = DIST / 'projects'
PROJECTS_JS = DIST / 'projects_data.js'

DISCOVER_CANDIDATES = [
    'workforce', 'workforce_api', 'workforce_frontend_app', 'workforce_frontend', 'hospitable',
    'wf-site', 'projects_active', 'projects_archive', 'dev_hub'
]

# Names and patterns to ignore during discovery (temp/output dirs)
IGNORE_NAMES = set([
    '.git', 'node_modules', '__pycache__', 'pytest_cache', 'nvm', 'dist', 'logs', 'artifacts', 'venv', '.venv', '.venv_canonical312', 'openai_backup_20260318', 'cache', 'cachedir', 'upload', 'workspace_quarantine'
])


def extract_style(index_path: Path) -> str:
    text = index_path.read_text(encoding='utf-8')
    start = text.find('<style>')
    end = text.find('</style>', start)
    if start == -1 or end == -1:
        return ''
    # include closing tag length
    return text[start:end+8]

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{name} — Project Dashboard</title>
{style}
</head>
<body>
  <main class="shell">
    <a href="../index.html">← Back to Dev Hub</a>
    <section style="margin-top:18px">
      <article class="hero-card">
        <h1>{name}</h1>
        <p class="muted">{description}</p>
        <div style="margin-top:12px"><strong>Status:</strong> {status} &nbsp; <em>Last updated: {last_updated}</em></div>
      </article>

      <div style="height:18px"></div>

      <article class="panel">
        <div class="panel-body">
          <h2>Key Links</h2>
          <ul>
            {links}
          </ul>
        </div>
      </article>

      <article class="panel">
        <div class="panel-body">
          <h2>Documents</h2>
          <ul>
            {docs}
          </ul>
        </div>
      </article>

      {routes_section}

      {ops_section}

      {next_section}

      {integrations_section}

    </section>
  </main>
</body>
</html>
'''


def slugify(name: str) -> str:
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return name


def pretty_name(dirname: str) -> str:
    return dirname.replace('_', ' ').replace('-', ' ').title()


def read_readme_summary(path: Path) -> str:
    readme = path / 'README.md'
    if not readme.exists():
        return ''
    text = readme.read_text(encoding='utf-8').strip()
    # return first non-empty paragraph or first line
    for part in text.split('\n\n'):
        line = part.strip().splitlines()[0] if part.strip() else ''
        if line:
            return line[:250]
    return ''


def discover_projects(root: Path) -> list:
    candidates = []
    parent = root.parent
    for name in sorted(parent.iterdir()):
        if not name.is_dir():
            continue
        n = name.name
        if n in IGNORE_NAMES:
            continue
        # prefer explicit candidates or dirs with indicators
        indicators = any((name / f).exists() for f in ('README.md', 'pyproject.toml', 'package.json', 'docs', 'README'))
        if n in DISCOVER_CANDIDATES or indicators or n.startswith('workforce') or n in ('hospitable', 'wf-site'):
            candidates.append(name)
    projects = []
    for c in candidates:
        slug = slugify(c.name)
        name = pretty_name(c.name)
        desc = read_readme_summary(c) or f'Project directory: {c.name}'
        mtime = None
        rm = c / 'README.md'
        if rm.exists():
            mtime = datetime.date.fromtimestamp(rm.stat().st_mtime).isoformat()
        else:
            mtime = datetime.date.fromtimestamp(c.stat().st_mtime).isoformat()
        proj = {
            'slug': slug,
            'name': name,
            'description': desc,
            'status': 'unknown',
            'scope': '',
            'key_links': [
                {'label': 'Repo root', 'href': f'../{c.name}/', 'type': 'repo'}
            ],
            'docs': [],
            'related': [],
            'last_updated': mtime
        }
        # include docs if exists
        docs_dir = c / 'docs'
        if docs_dir.exists() and docs_dir.is_dir():
            for f in sorted(docs_dir.iterdir()):
                if f.suffix.lower() in ('.md', '.markdown'):
                    proj['docs'].append({'title': f.name, 'href': f'../{c.name}/docs/{f.name}'})
        # include README
        if (c / 'README.md').exists():
            proj['docs'].append({'title': 'README.md', 'href': f'../{c.name}/README.md'})
        projects.append(proj)
    return projects


def merge_projects(existing: list, discovered: list) -> list:
    out = {p['slug']: p for p in existing}
    for d in discovered:
        if d['slug'] in out:
            # update missing fields but keep existing details
            base = out[d['slug']]
            for k, v in d.items():
                if not base.get(k):
                    base[k] = v
            # ensure docs/key_links exist
            base.setdefault('docs', base.get('docs', []))
            base.setdefault('key_links', base.get('key_links', d.get('key_links', [])))
        else:
            out[d['slug']] = d
    # return sorted list by name
    return sorted(out.values(), key=lambda x: x.get('name',''))


def write_outputs(data: list):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    style = extract_style(INDEX)
    js = 'window.projectsData = ' + json.dumps(data, indent=2) + ';\n'
    PROJECTS_JS.write_text(js, encoding='utf-8')
    print('Wrote', PROJECTS_JS)
    for proj in data:
        links_html = '\n'.join([f"<li><a href=\"{link.get('href')}\">{link.get('label')}</a> ({link.get('type')})</li>" for link in proj.get('key_links', [])])
        docs_html = '\n'.join([f"<li><a href=\"{d.get('href')}\">{d.get('title')}</a></li>" for d in proj.get('docs', [])])

        # optional sections
        routes = proj.get('important_routes') or []
        if isinstance(routes, str):
            routes = [routes]
        routes_html = '\n'.join([f"<li><a href=\"{r.get('href', '#')}\">{r.get('label', r)}</a></li>" if isinstance(r, dict) else f"<li>{r}</li>" for r in routes])
        routes_section = f"<article class=\"panel\"><div class=\"panel-body\"><h2>Important routes/pages</h2><ul>{routes_html}</ul></div></article>" if routes_html else ''

        ops = proj.get('operational_notes') or ''
        ops_section = f"<article class=\"panel\"><div class=\"panel-body\"><h2>Operational notes / next actions</h2><div class=\"muted\">{ops}</div></div></article>" if ops else ''

        next_actions = proj.get('next_actions') or []
        next_html = '\n'.join([f"<li>{a}</li>" for a in next_actions])
        next_section = f"<article class=\"panel\"><div class=\"panel-body\"><h2>Next actions</h2><ul>{next_html}</ul></div></article>" if next_html else ''

        integrations = proj.get('integrations') or []
        integrations_html = '\n'.join([f"<li><a href=\"{it.get('href')}\">{it.get('name')}</a></li>" for it in integrations if isinstance(it, dict)])
        integrations_section = f"<article class=\"panel\"><div class=\"panel-body\"><h2>Integrations / Related modules</h2><ul>{integrations_html}</ul></div></article>" if integrations_html else ''

        content = TEMPLATE.format(
            name=proj.get('name'),
            description=proj.get('description',''),
            status=proj.get('status',''),
            last_updated=proj.get('last_updated',''),
            links=links_html or '<li>No key links defined</li>',
            docs=docs_html or '<li>No docs listed</li>',
            routes_section=routes_section,
            ops_section=ops_section,
            next_section=next_section,
            integrations_section=integrations_section,
            style=style
        )
        out_path = OUT_DIR / f"{proj.get('slug')}.html"
        out_path.write_text(content, encoding='utf-8')
        print('Wrote', out_path)


def load_existing(path: Path) -> list:
    if not path.exists():
        return []
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--discover', action='store_true', help='Discover sibling repos and merge into projects.json')
    args = parser.parse_args()

    existing = load_existing(PROJECTS_JSON)
    if args.discover:
        discovered = discover_projects(ROOT)
        merged = merge_projects(existing, discovered)
        # persist merged projects.json
        PROJECTS_JSON.write_text(json.dumps(merged, indent=2), encoding='utf-8')
        data = merged
        print('Discovered and merged projects; wrote projects.json')
    else:
        data = existing

    # Prune any projects matching ignore list (avoid publishing noise)
    data = [p for p in data if p.get('slug') and p.get('slug') not in IGNORE_NAMES]

    write_outputs(data)

if __name__ == '__main__':
    main()
