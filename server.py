#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEYTEQ — Ceylon Technology : website backend.

What it does
------------
* serves the static site (index.html, digitalrace.html, …) on one port
* provides the JSON API the site needs:
      public : GET  /api/health, GET /api/flyers, POST /api/leads
      admin  : POST /api/login, POST /api/logout, GET /api/me,
               GET/POST /api/admin/flyers, PATCH/DELETE /api/admin/flyers/<id>,
               POST /api/admin/flyers/reorder, POST /api/admin/upload,
               GET /api/admin/leads, PATCH/DELETE /api/admin/leads/<id>
* stores everything in SQLite (data/ceyteq.db) — flyers + customer enquiries
* keeps the admin password hashed with PBKDF2-HMAC-SHA256 (never in the HTML)

No third-party packages. Run it with:

    python3 server.py --init                 # first time: create db + admin
    python3 server.py                        # start on 0.0.0.0:8000
    python3 server.py --port 8080
    python3 server.py --set-password admin NEWPASSWORD
    python3 server.py --reseed-flyers        # restore the 10 known flyers
"""
from __future__ import annotations

import argparse
import base64
import binascii
import getpass
import hashlib
import hmac
import json
import os
import re
import secrets
import sqlite3
import sys
import threading
import time
from datetime import datetime, timezone
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse, parse_qs

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT, 'data')
DB_PATH = os.path.join(DATA_DIR, 'ceyteq.db')
SECRET_PATH = os.path.join(DATA_DIR, 'secret.key')
FLYER_DIR = os.path.join(ROOT, 'flyers')
UPLOAD_DIR = os.path.join(ROOT, 'uploads')
MAX_UPLOAD = 8 * 1024 * 1024                      # 8 MB per image
ALLOWED_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.gif'}
SESSION_COOKIE = 'ceyteq_session'
SESSION_DAYS = 7
LEAD_WINDOW = 600                                 # seconds
LEAD_LIMIT = 5                                    # enquiries per IP per window

# files/dirs that must never be served over HTTP
HIDDEN = {'data', 'uploads', '.git', '.github', '__pycache__', 'node_modules'}
HIDDEN_FILES = {'server.py', 'build_site.py', 'make_flyers.py', 'content_services.py',
                'README.txt', 'AUDIT-REPORT.md', '.gitignore', 'CNAME'}

# the 10 shipped flyers, in order (same list the admin TSV box offers)
SEED_FLYERS = [
    ('flyer-01-program-intro.png', 'Program Intro', 'වැඩසටහන', 'Intro'),
    ('flyer-02-why-now.png', 'Why Now', 'ඇයි දැන්ම', 'Pourquoi maintenant'),
    ('flyer-03-what-changes.png', 'What Changes', 'වෙනස', 'Changements'),
    ('flyer-04-how-it-works.png', 'How It Works', 'ක්‍රමය', 'Système'),
    ('flyer-05-training-90-day.png', '90-Day Training', 'පුහුණුව', 'Formation'),
    ('flyer-06-package-starter.png', 'Starter $19', 'ආරම්භක', 'Starter 19 $'),
    ('flyer-07-package-standard.png', 'Standard $60', 'සම්මත', 'Standard 60 $'),
    ('flyer-08-package-advanced.png', 'Advanced $80', 'උසස්', 'Avancé 80 $'),
    ('flyer-09-package-premium.png', 'Premium $250', 'ඉහළම', 'Premium 250 $'),
    ('flyer-10-ai-future-contact.png', 'AI + Contact', 'AI + සම්බන්ධය', 'IA + Contact'),
]

_db_lock = threading.Lock()
_rate: dict[str, list[float]] = {}


# ---------------------------------------------------------------------------
# database
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS admins (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT UNIQUE NOT NULL,
    salt       TEXT NOT NULL,
    pass_hash  TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS flyers (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    filename   TEXT NOT NULL,
    title_en   TEXT NOT NULL DEFAULT '',
    title_si   TEXT NOT NULL DEFAULT '',
    title_fr   TEXT NOT NULL DEFAULT '',
    visible    INTEGER NOT NULL DEFAULT 1,
    position   INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS leads (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    contact    TEXT NOT NULL,
    email      TEXT NOT NULL DEFAULT '',
    service    TEXT NOT NULL DEFAULT '',
    message    TEXT NOT NULL,
    page       TEXT NOT NULL DEFAULT '',
    status     TEXT NOT NULL DEFAULT 'new',
    created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_status ON leads(status);
CREATE INDEX IF NOT EXISTS idx_flyers_pos  ON flyers(position);
"""


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M')


def connect() -> sqlite3.Connection:
    os.makedirs(DATA_DIR, exist_ok=True)
    con = sqlite3.connect(DB_PATH, timeout=10)
    con.row_factory = sqlite3.Row
    con.execute('PRAGMA journal_mode=WAL')
    con.execute('PRAGMA foreign_keys=ON')
    return con


def init_db(seed: bool = True) -> None:
    with _db_lock, connect() as con:
        con.executescript(SCHEMA)
        if seed and not con.execute('SELECT 1 FROM flyers LIMIT 1').fetchone():
            con.executemany(
                'INSERT INTO flyers (filename,title_en,title_si,title_fr,visible,position,created_at)'
                ' VALUES (?,?,?,?,1,?,?)',
                [(f, en, si, fr, i, now_iso()) for i, (f, en, si, fr) in enumerate(SEED_FLYERS)])


def secret_key() -> bytes:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SECRET_PATH):
        with open(SECRET_PATH, 'wb') as f:
            f.write(secrets.token_bytes(48))
        os.chmod(SECRET_PATH, 0o600)
    with open(SECRET_PATH, 'rb') as f:
        return f.read()


def hash_password(password: str, salt: str | None = None) -> tuple[str, str]:
    salt = salt or secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode(), bytes.fromhex(salt), 200_000)
    return salt, dk.hex()


def set_password(username: str, password: str) -> None:
    if len(password) < 8:
        sys.exit('Password must be at least 8 characters.')
    salt, hashed = hash_password(password)
    with _db_lock, connect() as con:
        con.execute('INSERT INTO admins (username,salt,pass_hash,created_at) VALUES (?,?,?,?)'
                    ' ON CONFLICT(username) DO UPDATE SET salt=excluded.salt, pass_hash=excluded.pass_hash',
                    (username, salt, hashed, now_iso()))
    print(f'Password set for "{username}".')


def check_password(username: str, password: str) -> bool:
    with _db_lock, connect() as con:
        row = con.execute('SELECT salt,pass_hash FROM admins WHERE username=?', (username,)).fetchone()
    if not row:
        # constant-time-ish: still do the work so timing does not reveal a missing user
        hash_password(password, '00' * 16)
        return False
    _, candidate = hash_password(password, row['salt'])
    return hmac.compare_digest(candidate, row['pass_hash'])


def admin_count() -> int:
    with _db_lock, connect() as con:
        return con.execute('SELECT COUNT(*) c FROM admins').fetchone()['c']


def session_token(username: str) -> str:
    exp = int(time.time()) + SESSION_DAYS * 86400
    body = f'{username}|{exp}'
    sig = hmac.new(secret_key(), body.encode(), hashlib.sha256).hexdigest()[:32]
    return base64.urlsafe_b64encode(f'{body}|{sig}'.encode()).decode()


def session_user(token: str | None) -> str | None:
    if not token:
        return None
    try:
        raw = base64.urlsafe_b64decode(token.encode()).decode()
        username, exp, sig = raw.rsplit('|', 2)
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None
    expect = hmac.new(secret_key(), f'{username}|{exp}'.encode(), hashlib.sha256).hexdigest()[:32]
    if not hmac.compare_digest(sig, expect) or int(exp) < time.time():
        return None
    return username


# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

def ok(handler, payload, code=200, cookie: str | None = None):
    body = json.dumps(payload, ensure_ascii=False).encode()
    handler.send_response(code)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.send_header('Cache-Control', 'no-store')
    if cookie:
        handler.send_header('Set-Cookie', cookie)
    handler.end_headers()
    handler.wfile.write(body)


def fail(handler, code, message):
    ok(handler, {'error': message}, code)


def clean(value, limit=2000) -> str:
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(value or '')).strip()[:limit]


def safe_filename(name: str) -> str:
    name = os.path.basename(str(name or '')).strip()
    name = re.sub(r'[^A-Za-z0-9._-]', '', name)
    return name[:120]


# ---------------------------------------------------------------------------
# request handler
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    server_version = 'Ceyteq/1.0'
    protocol_version = 'HTTP/1.1'

    # ---------- plumbing ----------
    def log_message(self, fmt, *args):        # keep the console readable
        sys.stderr.write('%s - %s\n' % (self.address_string(), fmt % args))

    def _json_body(self):
        try:
            length = int(self.headers.get('Content-Length') or 0)
        except ValueError:
            length = 0
        if length <= 0 or length > MAX_UPLOAD * 2:
            return None
        try:
            return json.loads(self.rfile.read(length).decode('utf-8'))
        except (ValueError, UnicodeDecodeError):
            return None

    def _user(self):
        raw = self.headers.get('Cookie')
        if not raw:
            return None
        try:
            cookie = SimpleCookie(raw)
        except Exception:
            return None
        morsel = cookie.get(SESSION_COOKIE)
        return session_user(morsel.value) if morsel else None

    def _same_origin_json(self) -> bool:
        """State-changing requests must be JSON (blocks simple form CSRF)."""
        ctype = (self.headers.get('Content-Type') or '').split(';')[0].strip().lower()
        return ctype == 'application/json'

    # ---------- verbs ----------
    def do_GET(self):
        self.route('GET')

    def do_POST(self):
        self.route('POST')

    def do_PATCH(self):
        self.route('PATCH')

    def do_DELETE(self):
        self.route('DELETE')

    def route(self, method):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        query = parse_qs(parsed.query)
        if path.startswith('/api/'):
            try:
                self.handle_api(method, path[5:], query)
            except Exception as exc:                      # never leak a traceback
                self.log_message('api error: %r', exc)
                fail(self, 500, 'server error')
            return
        if method == 'GET':
            self.serve_static(path)
        else:
            fail(self, 405, 'method not allowed')

    # ---------- API ----------
    def handle_api(self, method, route, query):
        route = route.strip('/')
        user = self._user()

        # --- public ---
        if route == 'health' and method == 'GET':
            with connect() as con:
                return ok(self, {
                    'ok': True, 'db': True, 'time': now_iso(),
                    'flyers': con.execute('SELECT COUNT(*) c FROM flyers').fetchone()['c'],
                    'leads': con.execute('SELECT COUNT(*) c FROM leads').fetchone()['c'],
                    'new_leads': con.execute("SELECT COUNT(*) c FROM leads WHERE status='new'").fetchone()['c'],
                })

        if route == 'flyers' and method == 'GET':
            with connect() as con:
                rows = con.execute('SELECT id,filename,title_en,title_si,title_fr,visible,position'
                                   ' FROM flyers WHERE visible=1 ORDER BY position,id').fetchall()
            return ok(self, [dict(r) for r in rows])

        if route == 'leads' and method == 'POST':
            if not self._same_origin_json():
                return fail(self, 415, 'JSON required')
            data = self._json_body() or {}
            name, contact, message = clean(data.get('name'), 120), clean(data.get('contact'), 60), clean(data.get('message'), 2000)
            if not (name and contact and message):
                return fail(self, 400, 'name, contact and message are required')
            ip = self.client_address[0]
            hits = [t for t in _rate.get(ip, []) if time.time() - t < LEAD_WINDOW]
            if len(hits) >= LEAD_LIMIT:
                return fail(self, 429, 'too many enquiries, please try again later')
            hits.append(time.time())
            _rate[ip] = hits
            with _db_lock, connect() as con:
                cur = con.execute('INSERT INTO leads (name,contact,email,service,message,page,status,created_at)'
                                  ' VALUES (?,?,?,?,?,?,?,?)',
                                  (name, contact, clean(data.get('email'), 160),
                                   clean(data.get('service'), 80), message,
                                   clean(data.get('page'), 200), 'new', now_iso()))
                lead_id = cur.lastrowid
            self.log_message('new enquiry #%s from %s', lead_id, name)
            return ok(self, {'ok': True, 'id': lead_id}, 201)

        # --- auth ---
        if route == 'login' and method == 'POST':
            if not self._same_origin_json():
                return fail(self, 415, 'JSON required')
            data = self._json_body() or {}
            username = clean(data.get('username'), 60)
            password = str(data.get('password') or '')
            time.sleep(0.35)                              # slow brute force a little
            if not (username and password) or not check_password(username, password):
                return fail(self, 401, 'invalid username or password')
            cookie = (f'{SESSION_COOKIE}={session_token(username)}; Path=/; HttpOnly; SameSite=Lax;'
                      f' Max-Age={SESSION_DAYS * 86400}')
            return ok(self, {'ok': True, 'username': username}, 200, cookie=cookie)

        if route == 'logout' and method == 'POST':
            cookie = f'{SESSION_COOKIE}=deleted; Path=/; HttpOnly; SameSite=Lax; Max-Age=0'
            return ok(self, {'ok': True}, 200, cookie=cookie)

        if route == 'me' and method == 'GET':
            return ok(self, {'username': user}) if user else fail(self, 401, 'not signed in')

        # --- everything below needs a session ---
        if not user:
            return fail(self, 401, 'admin login required')

        if route == 'admin/flyers' and method == 'GET':
            with connect() as con:
                rows = con.execute('SELECT * FROM flyers ORDER BY position,id').fetchall()
            return ok(self, [dict(r) for r in rows])

        if route == 'admin/flyers' and method == 'POST':
            data = self._json_body() or {}
            filename = safe_filename(data.get('filename'))
            if not filename:
                return fail(self, 400, 'filename required')
            with _db_lock, connect() as con:
                pos = con.execute('SELECT COALESCE(MAX(position),-1)+1 p FROM flyers').fetchone()['p']
                cur = con.execute('INSERT INTO flyers (filename,title_en,title_si,title_fr,visible,position,created_at)'
                                  ' VALUES (?,?,?,?,?,?,?)',
                                  (filename, clean(data.get('title_en'), 120), clean(data.get('title_si'), 120),
                                   clean(data.get('title_fr'), 120), 1 if data.get('visible', 1) else 0,
                                   pos, now_iso()))
                row = con.execute('SELECT * FROM flyers WHERE id=?', (cur.lastrowid,)).fetchone()
            return ok(self, dict(row), 201)

        m = re.fullmatch(r'admin/flyers/(\d+)', route)
        if m and method in ('PATCH', 'DELETE'):
            fid = int(m.group(1))
            with _db_lock, connect() as con:
                if not con.execute('SELECT 1 FROM flyers WHERE id=?', (fid,)).fetchone():
                    return fail(self, 404, 'flyer not found')
                if method == 'DELETE':
                    con.execute('DELETE FROM flyers WHERE id=?', (fid,))
                    return ok(self, {'ok': True})
                data = self._json_body() or {}
                sets, vals = [], []
                for col in ('filename', 'title_en', 'title_si', 'title_fr'):
                    if col in data:
                        val = safe_filename(data[col]) if col == 'filename' else clean(data[col], 120)
                        sets.append(f'{col}=?')
                        vals.append(val)
                if 'visible' in data:
                    sets.append('visible=?')
                    vals.append(1 if data['visible'] in (1, '1', True, 'true', 'yes') else 0)
                if 'position' in data:
                    sets.append('position=?')
                    vals.append(int(data['position']))
                if not sets:
                    return fail(self, 400, 'nothing to update')
                vals.append(fid)
                con.execute(f'UPDATE flyers SET {",".join(sets)} WHERE id=?', vals)
                row = con.execute('SELECT * FROM flyers WHERE id=?', (fid,)).fetchone()
            return ok(self, dict(row))

        if route == 'admin/flyers/reorder' and method == 'POST':
            ids = (self._json_body() or {}).get('ids') or []
            if not isinstance(ids, list):
                return fail(self, 400, 'ids list required')
            with _db_lock, connect() as con:
                for pos, fid in enumerate(ids):
                    try:
                        con.execute('UPDATE flyers SET position=? WHERE id=?', (pos, int(fid)))
                    except (TypeError, ValueError):
                        continue
            return ok(self, {'ok': True})

        if route == 'admin/upload' and method == 'POST':
            data = self._json_body() or {}
            name = safe_filename(data.get('filename'))
            blob = str(data.get('data') or '')
            ext = os.path.splitext(name)[1].lower()
            if not name or ext not in ALLOWED_EXT:
                return fail(self, 400, 'only png / jpg / webp / gif images are allowed')
            if ',' in blob and blob.strip().startswith('data:'):
                blob = blob.split(',', 1)[1]
            try:
                raw = base64.b64decode(blob, validate=True)
            except (binascii.Error, ValueError):
                return fail(self, 400, 'invalid image data')
            if not raw or len(raw) > MAX_UPLOAD:
                return fail(self, 413, 'image too large (max 8 MB)')
            os.makedirs(FLYER_DIR, exist_ok=True)
            base, ext = os.path.splitext(name)
            target = safe_filename(name)
            if os.path.exists(os.path.join(FLYER_DIR, target)):
                target = f'{base}-{secrets.token_hex(3)}{ext}'
            with open(os.path.join(FLYER_DIR, target), 'wb') as f:
                f.write(raw)
            self.log_message('flyer uploaded: %s (%d bytes)', target, len(raw))
            return ok(self, {'ok': True, 'filename': target}, 201)

        if route == 'admin/leads' and method == 'GET':
            status = (query.get('status') or [''])[0]
            sql = 'SELECT * FROM leads'
            args: tuple = ()
            if status in ('new', 'done'):
                sql += ' WHERE status=?'
                args = (status,)
            sql += ' ORDER BY id DESC LIMIT 500'
            with connect() as con:
                rows = con.execute(sql, args).fetchall()
            return ok(self, [dict(r) for r in rows])

        m = re.fullmatch(r'admin/leads/(\d+)', route)
        if m and method in ('PATCH', 'DELETE'):
            lid = int(m.group(1))
            with _db_lock, connect() as con:
                if not con.execute('SELECT 1 FROM leads WHERE id=?', (lid,)).fetchone():
                    return fail(self, 404, 'lead not found')
                if method == 'DELETE':
                    con.execute('DELETE FROM leads WHERE id=?', (lid,))
                    return ok(self, {'ok': True})
                status = clean((self._json_body() or {}).get('status'), 20)
                if status not in ('new', 'done'):
                    return fail(self, 400, 'status must be new or done')
                con.execute('UPDATE leads SET status=? WHERE id=?', (status, lid))
            return ok(self, {'ok': True})

        return fail(self, 404, 'unknown api route')

    # ---------- static files ----------
    def serve_static(self, path):
        rel = path.lstrip('/')
        parts = [p for p in rel.split('/') if p not in ('', '.')]
        if any(p == '..' for p in parts) or (parts and parts[0] in HIDDEN):
            return fail(self, 403, 'forbidden')
        if parts and parts[-1] in HIDDEN_FILES:
            return fail(self, 403, 'forbidden')
        candidate = os.path.join(ROOT, *parts) if parts else os.path.join(ROOT, 'index.html')
        if parts and not os.path.splitext(candidate)[1] and not os.path.exists(candidate):
            candidate += '.html'                          # /contact -> contact.html
        if os.path.isdir(candidate):
            candidate = os.path.join(candidate, 'index.html')
        if not os.path.isfile(candidate) or not os.path.abspath(candidate).startswith(ROOT):
            return self.not_found()
        ext = os.path.splitext(candidate)[1].lower()
        ctype = {
            '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
            '.js': 'application/javascript; charset=utf-8', '.json': 'application/json',
            '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif',
            '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
            '.mp4': 'video/mp4', '.webm': 'video/webm', '.ttf': 'font/ttf', '.txt': 'text/plain; charset=utf-8',
            '.md': 'text/markdown; charset=utf-8', '.pdf': 'application/pdf',
        }.get(ext, 'application/octet-stream')
        size = os.path.getsize(candidate)
        self.send_response(200)
        self.send_header('Content-Type', ctype)
        self.send_header('Content-Length', str(size))
        self.send_header('Cache-Control', 'no-cache' if ext == '.html' else 'public, max-age=3600')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.end_headers()
        with open(candidate, 'rb') as f:
            while True:
                chunk = f.read(64 * 1024)
                if not chunk:
                    break
                self.wfile.write(chunk)

    def not_found(self):
        body = (b'<h1>404 &mdash; not found</h1>'
                b'<p><a href="/">Ceyteq home</a></p>')
        self.send_response(404)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description='Ceyteq website backend (static site + JSON API + SQLite)')
    ap.add_argument('--host', default='0.0.0.0')
    ap.add_argument('--port', type=int, default=8000)
    ap.add_argument('--init', action='store_true', help='create the database, seed flyers and admin')
    ap.add_argument('--set-password', nargs=2, metavar=('USERNAME', 'PASSWORD'))
    ap.add_argument('--reseed-flyers', action='store_true', help='restore the 10 shipped flyers')
    ap.add_argument('--admin-user', default=os.environ.get('CEYTEQ_ADMIN_USER', 'admin'))
    ap.add_argument('--admin-password', default=os.environ.get('CEYTEQ_ADMIN_PASSWORD', ''))
    args = ap.parse_args()

    init_db(seed=True)

    if args.set_password:
        set_password(args.set_password[0], args.set_password[1])
        return
    if args.reseed_flyers:
        with _db_lock, connect() as con:
            con.execute('DELETE FROM flyers')
            con.executemany('INSERT INTO flyers (filename,title_en,title_si,title_fr,visible,position,created_at)'
                            ' VALUES (?,?,?,?,1,?,?)',
                            [(f, en, si, fr, i, now_iso()) for i, (f, en, si, fr) in enumerate(SEED_FLYERS)])
        print('10 flyers restored.')
        return
    created = False
    if not admin_count() or (args.init and args.admin_password):
        password = args.admin_password
        generated = False
        if not password:
            password = secrets.token_urlsafe(12)
            generated = True
        set_password(args.admin_user, password)
        created = True
        if generated:
            print('\n' + '=' * 62)
            print('  ADMIN LOGIN CREATED — write this down, it is shown once')
            print(f'    user     : {args.admin_user}')
            print(f'    password : {password}')
            print('  change it: python3 server.py --set-password admin NEWPASS')
            print('=' * 62 + '\n')

    if args.init:
        print('Database ready: data/ceyteq.db'
              + (f'  (admin "{args.admin_user}" created)' if created else '  (admin already existed)'))
        print('Start the site with:  python3 server.py')
        return

    print(f'Ceyteq backend on http://{args.host}:{args.port}   (db: data/ceyteq.db)')
    ThreadingHTTPServer.daemon_threads = True
    httpd = ThreadingHTTPServer((args.host, args.port), Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nstopped')
    finally:
        httpd.server_close()


if __name__ == '__main__':
    main()
