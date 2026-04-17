import os
from flask import Flask, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR_ENV = os.environ.get("FRONTEND_DIST_DIR")

if DIST_DIR_ENV and os.path.isabs(DIST_DIR_ENV):
    DIST_DIR = DIST_DIR_ENV
elif DIST_DIR_ENV:
    DIST_DIR = os.path.join(BASE_DIR, DIST_DIR_ENV)
else:
    DIST_DIR = os.path.join(BASE_DIR, "static")

app = Flask(__name__, static_folder=None)

@app.route('/health')
def health():
    return 'ok', 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def spa(path: str):
    requested = os.path.join(DIST_DIR, path)
    if path and os.path.isfile(requested):
        return send_from_directory(DIST_DIR, path)
    return send_from_directory(DIST_DIR, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
