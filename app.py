from pathlib import Path
import os
from flask import Flask, send_from_directory, abort, jsonify, Blueprint, request, render_template, url_for

DIST_DIR = Path("/home/hn3t/dev_hub/dist")

app = Flask(__name__, static_folder=None)
app_secret = os.environ.get('DEVHUB_FLASK_SECRET') or os.environ.get('DEVHUB_FLASK_SECRET')
if not app_secret:
    skfile = Path(__file__).parent / '.devhub_secret'
    try:
        if skfile.exists():
            app_secret = skfile.read_text().strip()
        else:
            import secrets
            app_secret = secrets.token_hex(32)
            skfile.write_text(app_secret)
    except Exception:
        app_secret = 'devhub-fallback-secret'
app.secret_key = app_secret


def health():
    return jsonify({"ok": True, "service": "dev-hub"})

# Keep a simple health endpoint at /health for monitoring
app.add_url_rule("/health", endpoint="health", view_func=health, methods=["GET"])

# Serve the SPA under the /dev-hub/ prefix so it can be mounted at
# hn3t.pythonanywhere.com/dev-hub/
devhub = Blueprint("devhub", __name__)

@devhub.route('/api/search')
def api_search():
    """Search using sqlite FTS index if available, otherwise fall back to in-memory scan.
    Params: q, tag, kind, limit, offset
    """
    q = request.args.get('q', '').strip()
    tag = request.args.get('tag')
    kind = request.args.get('kind')
    try:
        limit = int(request.args.get('limit', 50))
    except Exception:
        limit = 50
    try:
        offset = int(request.args.get('offset', 0))
    except Exception:
        offset = 0

    # Prefer using sqlite index if present
    INDEX_DB = Path('/home/hn3t/dev_hub/search_index.db')
    if INDEX_DB.exists():
        import sqlite3
        conn = sqlite3.connect(str(INDEX_DB))
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if q:
            # FTS5 MATCH against docs_fts, join back to docs for metadata
            sql = "SELECT d.kind,d.ident AS id,d.title,d.path,d.summary,d.tags,d.mtime FROM docs_fts JOIN docs d ON d.rowid = docs_fts.rowid WHERE docs_fts MATCH ?"
            params = [q]
            if tag:
                sql += " AND d.tags LIKE ?"
                params.append('%'+tag+'%')
            if kind:
                sql += " AND d.kind = ?"
                params.append(kind)
            sql += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            cur.execute(sql, params)
        else:
            sql = "SELECT d.kind,d.ident AS id,d.title,d.path,d.summary,d.tags,d.mtime FROM docs d"
            params = []
            where = []
            if tag:
                where.append("d.tags LIKE ?")
                params.append('%'+tag+'%')
            if kind:
                where.append("d.kind = ?")
                params.append(kind)
            if where:
                sql += " WHERE " + " AND ".join(where)
            sql += " LIMIT ? OFFSET ?"
            params.extend([limit, offset])
            cur.execute(sql, params)
        rows = [dict(r) for r in cur.fetchall()]
        # compute simple relevance score when query present
        if q:
            toks = [t.strip().lower() for t in q.split() if t.strip()]
            for row in rows:
                score = 0
                title = (row.get('title') or '').lower()
                summary = (row.get('summary') or '').lower()
                tags = (row.get('tags') or '').lower()
                for t in toks:
                    score += 3 * title.count(t)
                    score += 1 * summary.count(t)
                    score += 2 * tags.count(t)
                row['score'] = score
            rows.sort(key=lambda r: r.get('score', 0), reverse=True)
        conn.close()
        return jsonify({'total': len(rows), 'items': rows})

    # Fallback: load JSON and filter
    items = []
    pj_file = DIST_DIR / 'projects.json'
    if pj_file.exists():
        try:
            import json
            pj = json.loads(pj_file.read_text())
            for p in pj:
                items.append({
                    'kind': 'project',
                    'id': p.get('slug'),
                    'title': p.get('name'),
                    'path': (p.get('key_links') or [{}])[0].get('href') if p.get('key_links') else '#',
                    'summary': p.get('description',''),
                    'tags': p.get('tags',[]),
                    'mtime': p.get('last_updated')
                })
        except Exception:
            pass

    cat_file = DIST_DIR / 'catalog.json'
    if cat_file.exists():
        try:
            import json
            cat = json.loads(cat_file.read_text())
            for d in cat.get('items', []):
                items.append({
                    'kind': 'doc',
                    'id': d.get('path'),
                    'title': d.get('title') or d.get('path'),
                    'path': d.get('path'),
                    'summary': d.get('summary',''),
                    'tags': d.get('tags',[]),
                    'mtime': d.get('mtime')
                })
        except Exception:
            pass

    def matches(it):
        if tag and tag not in (it.get('tags') or []):
            return False
        if kind and it.get('kind') != kind:
            return False
        if not q:
            return True
        qv = q.lower()
        if (it.get('title') or '').lower().find(qv) != -1:
            return True
        if (it.get('summary') or '').lower().find(qv) != -1:
            return True
        if (it.get('path') or '').lower().find(qv) != -1:
            return True
        return False

    filtered = [it for it in items if matches(it)]
    total = len(filtered)
    sliced = filtered[offset:offset+limit]
    return jsonify({'total': total, 'items': sliced})


# Serve allowed host files from the workspace so SPA links to docs/projects work.
@devhub.route('/files/<path:file_path>')
def serve_workspace_file(file_path: str):
    # Publicly expose only files under /home/hn3t/docs and dist. Other workspace areas require admin.
    public_bases = [Path('/home/hn3t/docs').resolve(), DIST_DIR.resolve()]
    protected_bases = [Path('/home/hn3t/projects_active').resolve(), Path('/home/hn3t').resolve()]

    # special case: if path begins with 'archive/', attempt both dist/archive and docs/archive
    if file_path.startswith('archive/'):
        rel = Path(file_path).relative_to('archive')
        archive_bases = [DIST_DIR / 'archive', Path('/home/hn3t/docs') / 'archive']
        for archive_base in archive_bases:
            target = (archive_base / rel).resolve()
            try:
                if str(target).startswith(str(archive_base.resolve())) and target.exists():
                    # archive content may be sensitive; require admin
                    try:
                        _check_admin()
                    except Exception:
                        abort(403)
                    return send_from_directory(str(archive_base), str(rel))
            except Exception:
                pass
        # fall through

    # Try explicit top-level mapping first (e.g., docs/..., workforce/..., projects_active/...)
    parts = Path(file_path).parts
    if parts:
        top = parts[0]
        base_candidate = (Path('/home/hn3t') / top).resolve()
        target = (base_candidate / Path(*parts[1:]) if len(parts) > 1 else base_candidate).resolve()
        try:
            if str(target).startswith(str(base_candidate)) and target.exists():
                # determine if base is public
                if any(str(base_candidate).startswith(str(pb)) for pb in public_bases):
                    return send_from_directory(str(base_candidate), str(target.relative_to(base_candidate)))
                # otherwise require admin
                try:
                    _check_admin()
                except Exception:
                    abort(403)
                return send_from_directory(str(base_candidate), str(target.relative_to(base_candidate)))
        except Exception:
            pass

    # Generic attempt against public bases
    for base in public_bases:
        target = (base / file_path).resolve()
        try:
            if str(target).startswith(str(base)) and target.exists():
                return send_from_directory(str(base), file_path)
        except Exception:
            continue

    # If not found in public areas, attempt protected areas but require admin
    try:
        _check_admin()
    except Exception:
        abort(403)
    # check protected bases
    for base in protected_bases:
        target = (base / file_path).resolve()
        try:
            if str(target).startswith(str(base)) and target.exists():
                return send_from_directory(str(base), file_path)
        except Exception:
            continue
    abort(404)

# Also allow direct /<root>/<path> under the dev-hub prefix for legacy links. Attempt to serve
# the file if it exists under /home/hn3t/<root>/..., otherwise fall through to the SPA.
@devhub.route('/<root>/<path:subpath>')
def serve_workspace_file_legacy(root: str, subpath: str):
    try:
        base = (Path('/home/hn3t') / root).resolve()
        target = (base / subpath).resolve()
        if str(target).startswith(str(base)) and target.exists():
            # If base is not public, require admin
            public_bases = {str(Path('/home/hn3t/docs').resolve()), str(DIST_DIR.resolve())}
            if str(base) in public_bases:
                return send_from_directory(str(base), subpath)
            try:
                _check_admin()
            except Exception:
                abort(403)
            return send_from_directory(str(base), subpath)
    except Exception:
        pass
    # fallthrough to SPA handler
    return spa(subpath)


# Server-side markdown rendering endpoint with per-file caching, bleach sanitization, and eviction.
MD_CACHE_DIR = Path(__file__).parent / 'cache' / 'md_files'
MD_CACHE_MAX_ENTRIES = 300
MD_CACHE_MAX_BYTES = 8 * 1024 * 1024  # 8 MB
try:
    import hashlib
except Exception:
    hashlib = None

@devhub.route('/api/render_markdown', methods=['GET','POST'])
def api_render_markdown():
    # ensure cache dir exists
    try:
        MD_CACHE_DIR.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

    def cache_file_for(key):
        if not hashlib:
            name = key.replace('/', '_')[-160:]
        else:
            name = hashlib.sha256(key.encode('utf-8')).hexdigest()
        return MD_CACHE_DIR / (name + '.json')

    def load_cache_entry(key):
        try:
            cf = cache_file_for(key)
            if cf.exists():
                return json.loads(cf.read_text())
        except Exception:
            pass
        return None

    def save_cache_entry(key, entry):
        try:
            cf = cache_file_for(key)
            cf.write_text(json.dumps(entry))
            # eviction
            files = list(MD_CACHE_DIR.glob('*.json'))
            total_bytes = sum(f.stat().st_size for f in files)
            if len(files) > MD_CACHE_MAX_ENTRIES or total_bytes > MD_CACHE_MAX_BYTES:
                metas = []
                for f in files:
                    try:
                        m = json.loads(f.read_text())
                        metas.append((f, m.get('last_access', 0)))
                    except Exception:
                        metas.append((f, 0))
                metas.sort(key=lambda x: x[1] or 0)
                while len(metas) > MD_CACHE_MAX_ENTRIES or sum((p.stat().st_size for p,_ in metas)) > MD_CACHE_MAX_BYTES:
                    rmf, _ = metas.pop(0)
                    try:
                        rmf.unlink()
                    except Exception:
                        pass
        except Exception:
            pass

    def sanitize_server_html_with_bleach(raw_html):
        try:
            import bleach
            allowed_tags = list(bleach.sanitizer.ALLOWED_TAGS) + ['p','pre','h1','h2','h3','br','table','thead','tbody','tr','td','th','code']
            allowed_attrs = {'a': ['href', 'title', 'rel', 'target'], 'img': ['src','alt','title'], '*': ['class']}
            return bleach.clean(raw_html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
        except Exception:
            import re
            html = re.sub(r'<(script|iframe|style)[\s\S]*?>[\s\S]*?<\/\1>', '', raw_html, flags=re.I)
            html = re.sub(r'\son\w+\s*=\s*"[^"]*"', '', html)
            html = re.sub(r"\son\w+\s*=\s*'[^']*'", '', html)
            html = re.sub(r'\son\w+\s*=\s*[^\s>]+', '', html)
            return html

    if request.method == 'GET':
        path = request.args.get('path')
        if not path:
            return jsonify({'ok': False, 'error': 'path required'}), 400
        if not path.startswith('docs/') and not path.startswith('.') and not path.startswith('dist') and not path.startswith('archive/'):
            try:
                _check_admin()
            except Exception:
                return jsonify({'ok': False, 'error': 'admin required for this path'}), 403
        candidates = [Path('/home/hn3t/docs') / path.replace('docs/',''), DIST_DIR / path, Path('/home/hn3t') / path]
        target = None
        for c in candidates:
            try:
                if c.exists() and c.is_file():
                    target = c
                    break
            except Exception:
                continue
        if target is None:
            return jsonify({'ok': False, 'error': 'file not found'}), 404
        key = str(target.resolve())
        try:
            mtime = int(target.stat().st_mtime)
        except Exception:
            mtime = None
        entry = load_cache_entry(key)
        if entry and mtime and entry.get('mtime') == mtime and entry.get('html'):
            entry['last_access'] = int(time.time())
            try:
                save_cache_entry(key, entry)
            except Exception:
                pass
            _log_action('render_markdown_cache_hit', {'path': path})
            return jsonify({'ok': True, 'html': entry.get('html'), 'cached': True})
        try:
            text = target.read_text(errors='ignore')
        except Exception:
            return jsonify({'ok': False, 'error': 'failed to read file'}), 500
    else:
        data = request.get_json() or {}
        text = data.get('md') or ''
        if not text:
            return jsonify({'ok': False, 'error': 'md required in body'}), 400
        key = None
        mtime = None

    try:
        import markdown as _md
        raw_html = _md.markdown(text, extensions=['fenced_code','tables','toc'])
    except Exception:
        import html as _html
        esc = _html.escape(text)
        import re
        html_out = esc
        html_out = re.sub(r'```([\s\S]*?)```', lambda m: '<pre><code>'+_html.escape(m.group(1))+'</code></pre>', html_out)
        html_out = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="/dev-hub/files/\2" rel="noopener">\1</a>', html_out)
        html_out = re.sub(r'^### (.*)$', r'<h3>\1</h3>', html_out, flags=re.M)
        html_out = re.sub(r'^## (.*)$', r'<h2>\1</h2>', html_out, flags=re.M)
        html_out = re.sub(r'^# (.*)$', r'<h1>\1</h1>', html_out, flags=re.M)
        raw_html = '<div class="md">' + html_out.replace('\n','<br/>') + '</div>'

    safe_html = sanitize_server_html_with_bleach(raw_html)

    if request.method == 'GET' and key:
        try:
            entry = {'mtime': mtime, 'html': safe_html, 'last_access': int(time.time())}
            save_cache_entry(key, entry)
            _log_action('render_markdown_cache_store', {'path': path})
        except Exception:
            pass

    _log_action('render_markdown', {'path': path if request.method=='GET' else None, 'cached': False})
    return jsonify({'ok': True, 'html': safe_html, 'cached': False})

# Clear markdown cache (admin only)
@devhub.route('/api/clear_md_cache', methods=['POST'])
def api_clear_md_cache():
    _check_admin()
    try:
        if MD_CACHE_DIR.exists():
            for f in MD_CACHE_DIR.glob('*.json'):
                try: f.unlink()
                except Exception: pass
        _log_action('clear_md_cache', {})
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# Scripts metadata endpoints
@devhub.route('/api/scripts/meta')
def api_scripts_meta():
    meta_file = Path(__file__).parent / 'scripts' / 'scripts_meta.json'
    if meta_file.exists():
        return send_from_directory(str(meta_file.parent), meta_file.name)
    return jsonify({})

@devhub.route('/api/scripts/update_meta', methods=['POST'])
def api_update_scripts_meta():
    _check_admin()
    data = request.get_json() or {}
    path = data.get('path')
    if not path:
        return jsonify({'ok': False, 'error': 'path required'}), 400
    meta_file = Path(__file__).parent / 'scripts' / 'scripts_meta.json'
    meta = {}
    try:
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
    except Exception:
        meta = {}
    entry = meta.get(path, {})
    for k in ('safe','tags','purpose'):
        if k in data:
            entry[k] = data[k]
    meta[path] = entry
    try:
        meta_file.write_text(json.dumps(meta, indent=2))
        _log_action('update_script_meta', {'path': path, 'meta': entry})
        return jsonify({'ok': True, 'path': path, 'meta': entry})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

# Admin audit endpoints
@devhub.route('/api/admin_actions', methods=['GET'])
def api_admin_actions():
    _check_admin()
    n = int(request.args.get('n', 50))
    logf = Path(__file__).parent / 'admin_actions.log'
    entries = []
    try:
        if logf.exists():
            lines = logf.read_text().splitlines()
            lines = [l for l in lines if l.strip()]
            import json as _json
            for l in lines[-n:]:
                try:
                    entries.append(_json.loads(l))
                except Exception:
                    continue
    except Exception:
        pass
    return jsonify(entries)

@devhub.route('/api/script_runs', methods=['GET'])
def api_script_runs():
    _check_admin()
    path = request.args.get('path')
    logf = Path(__file__).parent / 'admin_actions.log'
    runs = []
    try:
        if logf.exists():
            import json as _json
            for l in logf.read_text().splitlines():
                if not l.strip():
                    continue
                try:
                    e = _json.loads(l)
                except Exception:
                    continue
                if e.get('action') in ('exec_script','exec_script_error'):
                    d = e.get('details') or {}
                    if not path or d.get('path') == path or d.get('script') == path:
                        runs.append(e)
    except Exception:
        pass
    return jsonify(runs)

@devhub.route('/', defaults={'req_path': ''})
@devhub.route('/<path:req_path>')
def spa(req_path: str):
    target = DIST_DIR / req_path

    if req_path and target.is_file():
        return send_from_directory(str(DIST_DIR), req_path)

    index_file = DIST_DIR / 'index.html'
    if index_file.exists():
        return send_from_directory(str(DIST_DIR), 'index.html')

    abort(500, description='dist/index.html not found')

# Endpoint to rebuild the search index (runs scripts/build_search_index.py)
@devhub.route('/api/build_index', methods=['POST'])
def api_build_index():
    # require admin for remote rebuilds
    try:
        _check_admin()
    except Exception:
        return jsonify({'ok': False, 'error': 'admin required'}), 403
    script = str(Path(__file__).parent / 'scripts' / 'build_search_index.py')
    try:
        import subprocess
        res = subprocess.run(['python3', script], capture_output=True, text=True, timeout=300)
        ok = res.returncode == 0
        out = res.stdout + '\n' + res.stderr
        _log_action('build_index', {'ok': ok, 'script': script})
        return jsonify({'ok': ok, 'output': out[:20000]}), (200 if ok else 500)
    except Exception as e:
        _log_action('build_index_error', {'error': str(e)})
        return jsonify({'ok': False, 'error': str(e)}), 500

@devhub.route('/api/schedule_rebuild', methods=['POST'])
def api_schedule_rebuild():
    _check_admin()
    data = request.get_json() or {}
    interval = int(data.get('interval_minutes', 1440))
    schedule_file = Path(__file__).parent / 'schedule.json'
    sched = {'interval_minutes': interval, 'last_run': None}
    schedule_file.write_text(json.dumps(sched, indent=2))
    _log_action('schedule_rebuild_set', {'interval_minutes': interval})
    return jsonify({'ok': True, 'schedule': sched})

@devhub.route('/api/schedule_rebuild', methods=['GET'])
def api_get_schedule():
    schedule_file = Path(__file__).parent / 'schedule.json'
    if schedule_file.exists():
        return send_from_directory(str(Path(__file__).parent), 'schedule.json')
    return jsonify({})

# Admin endpoints: project listing, scripts, exec, archive, tag updates
import os, subprocess, json, shutil, time
ADMIN_TOKEN = os.environ.get('DEV_HUB_ADMIN_TOKEN') or os.environ.get('DEVHUB_ADMIN_PASSWORD')  # support legacy env name DEVHUB_ADMIN_PASSWORD

def _check_admin():
    # Admin check: session flag, X-ADMIN-TOKEN header, or HTTP Basic auth password
    from flask import request, session, abort
    token = (os.environ.get('DEVHUB_ADMIN_PASSWORD') or os.environ.get('DEV_HUB_ADMIN_TOKEN') or os.environ.get('DEVHUB_ADMIN_TOKEN'))
    if session.get('devhub_admin'):
        return True
    hdr = request.headers.get('X-ADMIN-TOKEN')
    if hdr and token and hdr == token:
        return True
    auth = request.authorization
    if auth and getattr(auth, 'password', None) and token and auth.password == token:
        return True
    abort(403)




def _log_action(action, details=None):
    try:
        log_file = Path(__file__).parent / 'admin_actions.log'
        entry = {
            'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'remote': request.remote_addr,
            'action': action,
            'details': details
        }
        with open(log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except Exception:
        pass

@devhub.route('/api/projects')
def api_projects():
    pj_file = DIST_DIR / 'projects.json'
    if pj_file.exists():
        return send_from_directory(str(DIST_DIR), 'projects.json')
    return jsonify([])

@devhub.route('/api/scripts')
def api_scripts():
    # Serve paginated scripts index with filtering and merged metadata
    idx = DIST_DIR / 'scripts_index.json'
    if not idx.exists():
        return jsonify({'total': 0, 'items': []})
    import json
    data = json.loads(idx.read_text())
    items = []
    for proj, arr in data.get('by_project', {}).items():
        for it in arr:
            items.append(it)
    q = (request.args.get('q') or '').strip().lower()
    project = request.args.get('project')
    purpose = request.args.get('purpose')
    exec_only = request.args.get('executable')
    try:
        limit = int(request.args.get('limit', 50))
    except Exception:
        limit = 50
    try:
        offset = int(request.args.get('offset', 0))
    except Exception:
        offset = 0

    def match(it):
        if project and it.get('project') != project:
            return False
        if purpose and it.get('purpose') != purpose:
            return False
        if exec_only and exec_only.lower() in ('1','true','yes') and not it.get('executable'):
            return False
        if not q:
            return True
        if q in (it.get('name') or '').lower():
            return True
        if q in (it.get('summary') or '').lower():
            return True
        if q in (it.get('path') or '').lower():
            return True
        return False

    filtered = [it for it in items if match(it)]
    total = len(filtered)
    sliced = filtered[offset:offset+limit]

    # merge metadata (safe, tags, purpose overrides)
    meta_file = Path(__file__).parent / 'scripts' / 'scripts_meta.json'
    meta = {}
    if meta_file.exists():
        try:
            meta = json.loads(meta_file.read_text())
        except Exception:
            meta = {}
    for it in sliced:
        m = meta.get(it.get('path')) or {}
        if m:
            it.update(m)

    return jsonify({'total': total, 'items': sliced})

@devhub.route('/api/exec', methods=['POST'])
def api_exec():
    _check_admin()
    data = request.get_json() or {}
    # accept either a path (relative to /home/hn3t) or a script name inside dev_hub/scripts
    rel_path = data.get('path') or data.get('script')
    args = data.get('args') or []
    if not rel_path:
        return jsonify({'ok': False, 'error': 'script path required'}), 400
    root = Path('/home/hn3t')
    target = (root / rel_path).resolve()
    # ensure target exists
    if not target.exists():
        return jsonify({'ok': False, 'error': 'script not found'}), 404
    # verify against scripts_index.json if present
    idx_file = DIST_DIR / 'scripts_index.json'
    allowed = False
    if idx_file.exists():
        try:
            import json
            idx = json.loads(idx_file.read_text())
            for proj, items in idx.get('by_project', {}).items():
                for it in items:
                    if it.get('path') == rel_path:
                        allowed = True
                        break
                if allowed: break
        except Exception:
            allowed = False
    else:
        # allow scripts under dev_hub/scripts by name
        scripts_dir = Path(__file__).parent / 'scripts'
        if scripts_dir.joinpath(rel_path).exists() or scripts_dir.joinpath(Path(rel_path).name).exists():
            allowed = True
    # allow if metadata marks script as safe
    meta_file = Path(__file__).parent / 'scripts' / 'scripts_meta.json'
    if meta_file.exists():
        try:
            import json
            meta = json.loads(meta_file.read_text())
            m = meta.get(rel_path) or meta.get(str(target))
            if m and m.get('safe'):
                allowed = True
        except Exception:
            pass
    if not allowed:
        return jsonify({'ok': False, 'error': 'script not in index or not allowed'}), 403
    # execute: prefer interpreter for .py, otherwise direct exec if executable
    try:
        if str(target).endswith('.py'):
            cmd = [sys.executable, str(target)] + args
        elif os.access(str(target), os.X_OK):
            cmd = [str(target)] + args
        else:
            # try invoking by interpreter from shebang
            with open(str(target), 'r', errors='ignore') as f:
                first = f.readline()
            if first.startswith('#!'):
                shell = first[2:].strip().split()[0]
                cmd = [shell, str(target)] + args
            else:
                # fallback to python
                cmd = [sys.executable, str(target)] + args
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
        res = {'ok': proc.returncode==0, 'cmd': cmd, 'stdout': proc.stdout, 'stderr': proc.stderr, 'returncode': proc.returncode}
        _log_action('exec_script', {'path': rel_path, 'args': args, 'returncode': proc.returncode})
        return jsonify(res)
    except Exception as e:
        _log_action('exec_script_error', {'path': rel_path, 'error': str(e)})
        return jsonify({'ok': False, 'error': str(e)}), 500

@devhub.route('/api/archive', methods=['POST'])
def api_archive():
    _check_admin()
    data = request.get_json() or {}
    path = data.get('path')
    if not path:
        return jsonify({'ok': False, 'error': 'path required'}), 400
    src = DIST_DIR / path
    if not src.exists():
        return jsonify({'ok': False, 'error': 'source not found'}), 404
    ts = time.strftime('%Y%m%d_%H%M%S')
    dest_dir = DIST_DIR / 'archive' / ts
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name
    shutil.move(str(src), str(dest))
    archive_index = DIST_DIR / 'archive_index.json'
    entries = []
    if archive_index.exists():
        entries = json.loads(archive_index.read_text())
    entry = {'original': path, 'archived': str(dest.relative_to(DIST_DIR)), 'timestamp': ts}
    entries.insert(0, entry)
    archive_index.write_text(json.dumps(entries, indent=2))
    _log_action('archive', {'path': path, 'archived': entry['archived']})
    return jsonify({'ok': True, 'entry': entry})

@devhub.route('/api/archive', methods=['GET'])
def api_archive_list():
    idx = DIST_DIR / 'archive_index.json'
    if idx.exists():
        return send_from_directory(str(DIST_DIR), 'archive_index.json')
    return jsonify([])

@devhub.route('/api/update_project_tags', methods=['POST'])
def api_update_project_tags():
    _check_admin()
    data = request.get_json() or {}
    slug = data.get('slug')
    tags = data.get('tags') or []
    pj_file = DIST_DIR / 'projects.json'
    if not pj_file.exists():
        return jsonify({'ok': False, 'error': 'projects.json not found'}), 404
    pj = json.loads(pj_file.read_text())
    updated = False
    for p in pj:
        if p.get('slug') == slug:
            p['tags'] = tags
            updated = True
            break
    if not updated:
        return jsonify({'ok': False, 'error': 'project not found'}), 404
    pj_file.write_text(json.dumps(pj, indent=2))
    _log_action('update_project_tags', {'slug': slug, 'tags': tags})
    return jsonify({'ok': True, 'slug': slug, 'tags': tags})

# Package upload and management endpoints (admin only)
@devhub.route('/api/packages/upload', methods=['POST'])
def api_package_upload():
    _check_admin()
    from werkzeug.utils import secure_filename
    up = request.files.get('package')
    if not up:
        return jsonify({'ok': False, 'error': 'package file required'}), 400
    name = secure_filename(up.filename)
    ts = __import__('time').strftime('%Y%m%dT%H%M%SZ')
    dest_dir = Path(__file__).parent / 'data' / 'packages' / 'uploads' / (ts + '-' + name)
    dest_dir.mkdir(parents=True, exist_ok=True)
    pkg_path = dest_dir / 'package.zip'
    up.save(str(pkg_path))
    # run validator
    validator = Path(__file__).parent / 'scripts' / 'package_validator.py'
    try:
        import subprocess
        res = subprocess.run(['python3', str(validator), str(dest_dir)], capture_output=True, text=True, timeout=120)
        out = res.stdout + '\n' + res.stderr
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    # read status
    statusf = dest_dir / 'status.json'
    status = {}
    if statusf.exists():
        try:
            import json
            status = json.loads(statusf.read_text())
        except Exception:
            status = {'state':'unknown'}
    return jsonify({'ok': True, 'status': status, 'log': out[:20000]})

@devhub.route('/api/packages/status', methods=['GET'])
def api_package_status():
    _check_admin()
    path = request.args.get('path')
    if not path:
        return jsonify({'ok': False, 'error': 'path required'}), 400
    f = Path(__file__).parent / 'data' / 'packages' / 'uploads' / path / 'status.json'
    if not f.exists():
        return jsonify({'ok': False, 'error': 'not found'}), 404
    import json
    return jsonify(json.loads(f.read_text()))

# UI routes: control panel and packages info
@devhub.route('/control')
def control_panel():
    _check_admin()
    # load registry
    try:
        import importlib.util
        regp = Path(__file__).parent / 'scripts' / 'command_registry.py'
        spec = importlib.util.spec_from_file_location('cmdreg', str(regp))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        REG = getattr(mod, 'REGISTRY', [])
    except Exception:
        REG = []
    return render_template('control_panel.html', commands=REG)

@devhub.route('/packages/ui')
def packages_ui():
    return render_template('packages.html')

@devhub.route('/dashboard')
def dashboard():
    # load status
    OUT = Path(__file__).parent / 'data' / 'generated' / 'devhub_status.json'
    last = None
    status = 'unknown'
    if OUT.exists():
        try:
            import json
            d = json.loads(OUT.read_text())
            last = d.get('ts')
            status = 'ok'
        except Exception:
            status = 'error'
    return render_template('dashboard.html', status=status, last_refresh=last)

@devhub.route('/docs')
def docs_ui():
    return render_template('docs.html')

@devhub.route('/progress')
def progress_ui():
    items = []
    pj = Path(__file__).parent / 'data' / 'generated' / 'progress_index.json'
    if pj.exists():
        try:
            import json
            items = json.loads(pj.read_text()).get('items', [])
        except Exception:
            items = []
    return render_template('progress.html', items=items)

@devhub.route('/scripts')
def scripts_ui():
    return render_template('scripts.html')

@devhub.route('/file-tracker')
def file_tracker_ui():
    return render_template('file_tracker.html')

@devhub.route('/deployment')
def deployment_ui():
    return render_template('deployment.html')

@devhub.route('/settings')
def settings_ui():
    return render_template('settings.html')

@devhub.route('/static/<path:filename>')
def devhub_static(filename):
    # serve local static assets like CSS
    static_dir = Path(__file__).parent / 'static'
    return send_from_directory(str(static_dir), filename)

# API endpoints for generated indexes
@devhub.route('/api/docs_index')
def api_docs_index():
    # prefer generated index
    p = Path(__file__).parent / 'data' / 'generated' / 'docs_index.json'
    if not p.exists():
        # fallback to dist/docs_extra/index.json
        p = Path(__file__).parent / 'dist' / 'docs_extra' / 'index.json'
    if p.exists():
        try:
            import json
            return jsonify(json.loads(p.read_text()))
        except Exception:
            return jsonify({})
    return jsonify({})

@devhub.route('/api/progress_index')
def api_progress_index():
    p = Path(__file__).parent / 'data' / 'generated' / 'progress_index.json'
    if p.exists():
        try:
            import json
            return jsonify(json.loads(p.read_text()))
        except Exception:
            return jsonify({})
    return jsonify({})

@devhub.route('/api/file_inventory')
def api_file_inventory():
    p = Path(__file__).parent / 'data' / 'generated' / 'file_inventory.json'
    if p.exists():
        try:
            import json
            return jsonify(json.loads(p.read_text()))
        except Exception:
            return jsonify({})
    return jsonify({})

@devhub.route('/api/script_index')
def api_script_index():
    p = Path(__file__).parent / 'dist' / 'scripts_index.json'
    if p.exists():
        try:
            import json
            return jsonify(json.loads(p.read_text()))
        except Exception:
            return jsonify({})
    return jsonify({})

# Package staging and apply endpoints (admin only)
@devhub.route('/packages/stage')
def packages_stage_ui():
    _check_admin()
    base = Path(__file__).parent / 'data' / 'packages'
    uploads = base / 'uploads'
    staged = base / 'staged'
    ups = []
    sts = []
    try:
        if uploads.exists():
            ups = sorted([p.name for p in uploads.iterdir() if p.is_dir()])
    except Exception:
        ups = []
    try:
        if staged.exists():
            sts = sorted([p.name for p in staged.iterdir() if p.is_dir()])
    except Exception:
        sts = []
    return render_template('packages_stage.html', uploads=ups, staged=sts)

@devhub.route('/api/packages/stage', methods=['POST'])
def api_stage_package():
    _check_admin()
    data = request.get_json() or {}
    path = data.get('path')
    if not path:
        return jsonify({'ok': False, 'error': 'path required'}), 400
    # simple safety: no traversal in provided name
    if '..' in Path(path).parts or path.startswith('/') or '/' in path:
        return jsonify({'ok': False, 'error': 'invalid path'}), 400
    src = Path(__file__).parent / 'data' / 'packages' / 'uploads' / path
    if not src.exists() or not src.is_dir():
        return jsonify({'ok': False, 'error': 'upload not found'}), 404
    dest = Path(__file__).parent / 'data' / 'packages' / 'staged' / path
    if dest.exists():
        return jsonify({'ok': False, 'error': 'already staged'}), 409
    try:
        import shutil
        shutil.copytree(str(src), str(dest))
        # update status
        stf = dest / 'status.json'
        s = {'state':'staged'}
        import json
        stf.write_text(json.dumps(s, indent=2))
        _log_action('stage_package', {'path': path})
        return jsonify({'ok': True, 'staged': path})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@devhub.route('/packages/staged/ui')
def packages_staged_ui():
    _check_admin()
    base = Path(__file__).parent / 'data' / 'packages' / 'staged'
    items = []
    try:
        if base.exists():
            for p in sorted(base.iterdir()):
                if p.is_dir():
                    st = p / 'status.json'
                    stj = {}
                    if st.exists():
                        try:
                            stj = json.loads(st.read_text())
                        except Exception:
                            stj = {}
                    items.append({'name': p.name, 'status': stj.get('state','unknown')})
    except Exception:
        items = []
    return render_template('packages_stage.html', uploads=[], staged=[it['name'] for it in items], staged_items=items)

@devhub.route('/api/packages/apply', methods=['POST'])
def api_apply_staged():
    _check_admin()
    data = request.get_json() or {}
    path = data.get('path')
    if not path:
        return jsonify({'ok': False, 'error': 'path required'}), 400
    # safety checks
    if '..' in Path(path).parts or path.startswith('/') or '/' in path:
        return jsonify({'ok': False, 'error': 'invalid path'}), 400
    staged_dir = Path(__file__).parent / 'data' / 'packages' / 'staged' / path
    if not staged_dir.exists() or not staged_dir.is_dir():
        return jsonify({'ok': False, 'error': 'staged package not found'}), 404
    # call package_installer.py on staged_dir
    installer = Path(__file__).parent / 'scripts' / 'package_installer.py'
    try:
        res = subprocess.run(['python3', str(installer), str(staged_dir)], capture_output=True, text=True, timeout=600)
        out = res.stdout + '\n' + res.stderr
        # update status file
        stf = staged_dir / 'status.json'
        try:
            st = json.loads(stf.read_text()) if stf.exists() else {}
        except Exception:
            st = {}
        st['last_apply_returncode'] = res.returncode
        st['last_apply_output'] = (out or '')[:10000]
        st['state'] = 'applied' if res.returncode==0 else 'apply_failed'
        stf.write_text(json.dumps(st, indent=2))
        _log_action('apply_staged_package', {'path': path, 'returncode': res.returncode})
        return jsonify({'ok': res.returncode==0, 'returncode': res.returncode, 'output': out[:20000]})
    except Exception as e:
        _log_action('apply_staged_error', {'path': path, 'error': str(e)})
        return jsonify({'ok': False, 'error': str(e)}), 500

# Register the blueprint at /dev-hub
app.register_blueprint(devhub, url_prefix='/dev-hub')

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8099, debug=True)



@devhub.route('/admin/login', methods=['GET','POST'])
def admin_login():
    from flask import request, session, redirect, url_for
    token = (os.environ.get('DEVHUB_ADMIN_PASSWORD') or os.environ.get('DEV_HUB_ADMIN_TOKEN') or os.environ.get('DEVHUB_ADMIN_TOKEN'))
    if request.method == 'POST':
        pw = request.form.get('password') if request.form else (request.json.get('password') if request.is_json else None)
        if token and pw == token:
            session['devhub_admin'] = True
            return redirect(url_for('devhub.api_search'))
        return ('Forbidden', 403)
    return ('<form method="post"><input type="password" name="password"/><input type="submit" value="Login"/></form>', 200)

@devhub.route('/admin/logout')
def admin_logout():
    session.pop('devhub_admin', None)
    return ('logged out', 200)
