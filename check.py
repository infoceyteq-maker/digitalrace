#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEYTEQ pre-deploy check — run this before every push/merge:

    python3 check.py

It does four things and exits non-zero if anything fails:
  1. rebuilds all pages from content (build_site.py) and reports if the
     committed HTML is out of date
  2. checks every local link/image path in every page resolves
  3. boots the backend on a free port and exercises the API
     (/api/health, /api/flyers, admin 401 without login, POST /api/leads)
  4. prints a short summary

GitHub Actions: paste this into .github/workflows/build-check.yml on GitHub
(the Arena app token cannot create workflow files itself):

    name: Build check
    on: [push, pull_request, workflow_dispatch]
    jobs:
      check:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: { python-version: '3.12' }
          - run: python3 check.py
"""
from __future__ import annotations

import glob
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def step(title):
    print(f'\n=== {title} ===')


def fail(msg):
    FAIL.append(msg)
    print(f'  ✗ {msg}')


def ok(msg):
    print(f'  ✓ {msg}')


def free_port() -> int:
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


# 1 --------------------------------------------------------------- rebuild
step('1/4  Rebuild pages')
before = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
r = subprocess.run([sys.executable, 'build_site.py'], cwd=ROOT, capture_output=True, text=True)
if r.returncode:
    fail('build_site.py failed:\n' + (r.stderr or r.stdout))
else:
    pages = [l for l in r.stdout.splitlines() if l.endswith('KB')]
    ok(f'{len(pages)} pages built')
after = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout
if before != after and after.strip():
    fail('committed pages are out of date — run build_site.py and commit the result:\n' + after)
else:
    ok('committed pages match a fresh build')

# 2 ----------------------------------------------------------------- links
step('2/4  Local links and images')
broken = 0
for page in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
    html = open(page, encoding='utf-8').read()
    for ref in set(re.findall(r'(?:src|href)="([^"]+)"', html)):
        if ref.startswith(('data:', 'http', 'mailto:', 'tel:', '#', 'javascript:')):
            continue
        if "'" in ref or '+' in ref:
            continue
        target = ref.split('#')[0]
        if target and not os.path.exists(os.path.join(ROOT, target)):
            fail(f'{os.path.basename(page)}: missing {ref}')
            broken += 1
if not broken:
    ok('every local link and image resolves')

# 3 ------------------------------------------------------------------- api
step('3/4  Backend API')
port = free_port()
env = dict(os.environ, CEYTEQ_DATA_DIR=os.path.join(ROOT, 'data'))
log_path = os.path.join(ROOT, 'data', 'check-server.log')
os.makedirs(os.path.dirname(log_path), exist_ok=True)
log = open(log_path, 'w')
proc = subprocess.Popen([sys.executable, 'server.py', '--host', '127.0.0.1', '--port', str(port)],
                        cwd=ROOT, env=dict(env, PYTHONUNBUFFERED='1'),
                        stdout=log, stderr=subprocess.STDOUT)
base = f'http://127.0.0.1:{port}'


def get(path, method='GET', body=None):
    req = urllib.request.Request(base + path,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={'Content-Type': 'application/json'}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except (urllib.error.URLError, ConnectionError, OSError):
        return 0, ''          # server not listening yet


try:
    for _ in range(40):
        code, _ = get('/api/health')
        if code == 200:
            break
        time.sleep(0.25)
    code, body = get('/api/health')
    if code != 200:
        fail('backend did not answer /api/health — server log:')
        try:
            print(''.join(open(log_path).readlines()[-15:]))
        except OSError:
            pass
    else:
        data = json.loads(body)
        ok(f'/api/health {data}')

    code, body = get('/api/flyers')
    rows = json.loads(body) if code == 200 else []
    if code != 200 or not rows:
        fail('/api/flyers did not return rows')
    else:
        ok(f'/api/flyers returned {len(rows)} visible flyers (first src: {rows[0].get("src")})')

    code, _ = get('/api/admin/leads')
    if code != 401:
        fail(f'/api/admin/leads without login returned {code}, expected 401')
    else:
        ok('admin API is protected (401 without login)')

    code, _ = get('/api/leads', 'POST', {'name': 'Check', 'contact': '0770000000',
                                         'message': 'pre-deploy check'})
    if code not in (200, 201):
        fail(f'POST /api/leads returned {code}')
    else:
        ok('enquiry form endpoint accepts a lead')

    code, _ = get('/api/leads', 'POST', {'name': '', 'contact': '', 'message': ''})
    if code != 400:
        fail(f'empty lead was accepted ({code}) — validation problem')
    else:
        ok('empty leads are rejected (400)')

    code, _ = get('/server.py')
    if code != 403:
        fail(f'server.py is downloadable ({code}) — must be 403')
    else:
        ok('source files are not downloadable')
finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()

# 4 --------------------------------------------------------------- summary
step('4/4  Summary')
if FAIL:
    print(f'{len(FAIL)} problem(s) found:')
    for f in FAIL:
        print('  -', f)
    sys.exit(1)
print('All checks passed — safe to push / deploy.')
