#!/usr/bin/env python3
import json
import sqlite3
from pathlib import Path

BASE = Path('/home/hn3t/dev_hub')
DIST = BASE / 'dist'
DB = BASE / 'search_index.db'

print('Reading data...')
projects = []
if (DIST / 'projects.json').exists():
    projects = json.loads((DIST / 'projects.json').read_text())

catalog = {'items': []}
if (DIST / 'catalog.json').exists():
    catalog = json.loads((DIST / 'catalog.json').read_text())

print('Creating sqlite DB at', DB)
if DB.exists():
    DB.unlink()
conn = sqlite3.connect(str(DB))
cur = conn.cursor()
# enable WAL for concurrency
cur.execute('PRAGMA journal_mode=WAL;')
# Create backing table
cur.execute('DROP TABLE IF EXISTS docs')
cur.execute('CREATE TABLE docs (id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT, ident TEXT, title TEXT, path TEXT, summary TEXT, tags TEXT, mtime TEXT)')
# Create FTS5 table that indexes docs (content='docs')
cur.execute("DROP TABLE IF EXISTS docs_fts")
cur.execute("CREATE VIRTUAL TABLE docs_fts USING fts5(title, summary, tags, content='docs', content_rowid='id')")

print('Indexing projects...')
for p in projects:
    tags = ' '.join(p.get('tags') or [])
    title = p.get('name') or ''
    path = (p.get('key_links') or [{}])[0].get('href') if p.get('key_links') else ''
    summary = p.get('description') or ''
    mtime = p.get('last_updated') or ''
    cur.execute('INSERT INTO docs(kind,ident,title,path,summary,tags,mtime) VALUES (?,?,?,?,?,?,?)',
                ('project', p.get('slug'), title, path, summary, tags, mtime))

print('Indexing docs...')
for d in catalog.get('items', []):
    tags = ' '.join(d.get('tags') or [])
    title = d.get('title') or ''
    path = d.get('path') or ''
    summary = d.get('summary') or ''
    mtime = str(d.get('mtime') or '')
    cur.execute('INSERT INTO docs(kind,ident,title,path,summary,tags,mtime) VALUES (?,?,?,?,?,?,?)',
                ('doc', d.get('path'), title, path, summary, tags, mtime))

# Populate the FTS index from docs
cur.execute("INSERT INTO docs_fts(docs_fts) VALUES('rebuild')")

conn.commit()
conn.close()
print('Indexing complete. DB size:', DB.stat().st_size)
