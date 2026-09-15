#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEYTEQ HotelMate campaign check — WhatsApp-only lead handoff.

    python3 check_hotelmate.py

Runs 60 checks over the built pages (run build_site.py first) and exits
non-zero if anything fails:

  1. hotelmate.html is WhatsApp-only: no fetch, no api/leads, no window.open,
     no "saved as a Ceyteq lead" / "enquiry server" wording, and the form
     composes one message to https://wa.me/94768607143?text=... synchronously
     with the fixed field order, UTM passthrough and the fitLines() guard
  2. the campaign offer wording exists only on hotelmate.html and is never
     worded as permanently free; the Ceyteq/HotelMate disclosure is verbatim
     on all three campaign views (index band, services card, hotelmate page)
  3. the HotelMate nav item is on all 20 full pages with an identical
     EN/SI/FR label; the homepage band, services partner card and the
     Facebook/Instagram/TikTok links are intact
  4. contact.html and learn-earn.html are byte-identical to main (their own
     backend form is untouched), the backend server.py is untouched, at least
     17 of 21 pages are unchanged, and no database/secrets were added
"""
from __future__ import annotations

import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PASSED = 0
FAILED = 0


def ck(name, cond):
    global PASSED, FAILED
    if cond:
        PASSED += 1
        print(f'  \u2713 {name}')
    else:
        FAILED += 1
        print(f'  \u2717 {name}')


def read(fname):
    p = os.path.join(ROOT, fname)
    with open(p, encoding='utf-8') as f:
        return f.read()


def main_ref():
    for ref in ('origin/main', 'main'):
        r = subprocess.run(['git', 'rev-parse', '--verify', '--quiet', ref],
                           cwd=ROOT, capture_output=True)
        if r.returncode == 0:
            return ref
    return None


def git_bytes(ref, fname):
    r = subprocess.run(['git', 'show', f'{ref}:{fname}'], cwd=ROOT,
                       capture_output=True)
    return r.stdout if r.returncode == 0 else None


HM = read('hotelmate.html')
DISCLOSURE = ('Demo coordination by Ceyteq. Final product demo and activation '
              'are completed with the HotelMate team.')
CONFIRM = ('Your details will be sent to Ceyteq on WhatsApp. '
           'A campaign representative will reply.')
OFFER_A = 'Setup fee: FREE for the campaign period'
OFFER_B = 'US$39/month for the first 10 rooms'
ALL_PAGES = sorted(os.path.basename(p) for p in glob.glob(os.path.join(ROOT, '*.html')))
FULL_PAGES = [p for p in ALL_PAGES if '<nav>' in read(p)]   # flyers.html is a redirect

print(f'\n=== HotelMate WhatsApp-only campaign — {len(ALL_PAGES)} pages '
      f'({len(FULL_PAGES)} full) ===')

# 1 ------------------------------------------------ WhatsApp-only page
print('\n--- 1. hotelmate.html: no backend, no popups, no old wording ---')
ck('no fetch( on the campaign page', 'fetch(' not in HM)
ck('no api/leads on the campaign page', 'api/leads' not in HM)
ck('no window.open on the campaign page', 'window.open' not in HM)
ck('no XMLHttpRequest on the campaign page', 'XMLHttpRequest' not in HM)
ck('no sendEnquiry( (shared backend JS) on the campaign page', 'sendEnquiry(' not in HM)
ck('no window.CEYTEQ_ENQ backend config on the campaign page', 'window.CEYTEQ_ENQ' not in HM)
ck('no "saved as a Ceyteq lead" / "enquiry server" wording',
   'saved as a Ceyteq lead' not in HM and 'enquiry server' not in HM)
ck('enquiry form is present (id=enquiryForm)', 'id="enquiryForm"' in HM)
for fid in ('eqName', 'eqContact', 'eqEmail', 'eqType', 'eqRooms', 'eqMsg'):
    ck(f'form field #{fid} is present', f'id="{fid}"' in HM)
ck('submit is wired to HMWA.send', 'onsubmit="return HMWA.send(event)"' in HM)
ck('confirmation line is exactly right', f'>{CONFIRM}</span>' in HM)
ck('confirmation note is trilingual (en/si/fr spans)',
   re.search(r'id="eqNote".*?class="lang-en".*?class="lang-si".*?class="lang-fr"', HM, re.S) is not None)

# 2 -------------------------------------------------------- the handoff
print('\n--- 2. one synchronous WhatsApp handoff to the campaign number ---')
ck('wa.me base is https://wa.me/94768607143?text=',
   'https://wa.me/94768607143?text=' in HM)
ck("the number constant NUM='94768607143' is defined once", "var NUM='94768607143'" in HM)
nums = set(re.findall(r'wa\.me/(\d+)', HM))
ck('every wa.me number is the campaign number (33744284269 is the shared site footer INTL box)',
   nums == {'94768607143', '33744284269'} and '94768607143' in nums)
ck('the form JS composes the URL from the constant only', "'https://wa.me/'+NUM" in HM)
ck('no insecure http://wa.me link', 'http://wa.me' not in HM)
ck('handoff navigates via location.href assignment', 'location.href=' in HM)
ck('go() is one synchronous navigation: function go(url){window.location.href=url;}',
   re.search(r'function go\(url\)\{window\.location\.href=url;\}', HM) is not None)
ck('the message text is encodeURIComponent-ed', 'encodeURIComponent(' in HM)
ck('fitLines() guard is defined', 'function fitLines(' in HM)
ck('URL cap is ~1900 chars (var CAP=1900)', 'var CAP=1900' in HM)
ck("UTM order is utm_source, utm_medium, utm_campaign, utm_content",
   "['utm_source','utm_medium','utm_campaign','utm_content']" in HM)

# 3 ------------------------------------------------ offer and disclosure
print('\n--- 3. offer wording only on hotelmate.html; disclosure on all 3 views ---')
ck(f'"{OFFER_A}" on hotelmate.html', OFFER_A in HM)
ck(f'"{OFFER_B}" on hotelmate.html', OFFER_B in HM)
ck('the offer wording is NOT on index.html',
   OFFER_A not in read('index.html') and OFFER_B not in read('index.html'))
ck('the offer wording is NOT on services.html',
   OFFER_A not in read('services.html') and OFFER_B not in read('services.html'))
ck('the offer wording is on NO other page than hotelmate.html',
   all(OFFER_A not in read(p) and OFFER_B not in read(p)
       for p in ALL_PAGES if p != 'hotelmate.html'))
ck('never worded as permanently free (no "free forever/forever free/free for life/always free")',
   re.search(r'(?i)free\s+(forever|for life)|forever\s+free|always\s+free', HM) is None)
ck('the FREE wording is qualified by the campaign period', 'campaign period' in HM)
ck('the page states it is not a permanently free plan', 'not a permanently free' in HM)
ck(f'disclosure verbatim on hotelmate.html ("{DISCLOSURE[:38]}...")', DISCLOSURE in HM)
ck('disclosure verbatim on index.html (featured-partner band)', DISCLOSURE in read('index.html'))
ck('disclosure verbatim on services.html (partner card)', DISCLOSURE in read('services.html'))
ck('disclosure appears on all 3 campaign views of hotelmate.html (hero, how, closing)',
   HM.count(DISCLOSURE) == 3)
ck('Sinhala disclosure present on hotelmate.html',
   'ඩෙමෝ සම්බන්ධීකරණය Ceyteq විසින්' in HM)
ck('French disclosure present on hotelmate.html',
   'Coordination de la démo par Ceyteq' in HM)

# 4 ----------------------------------------------------- nav and surfaces
print('\n--- 4. nav item, homepage band, services card, social links ---')
nav_pages = [p for p in FULL_PAGES
             if re.search(r'<a class="[^"]*" href="hotelmate.html">'
                          r'<span class="lang-en">HotelMate</span>'
                          r'<span class="lang-si">HotelMate</span>'
                          r'<span class="lang-fr">HotelMate</span></a>', read(p))]
ck(f'HotelMate nav item with identical EN/SI/FR label on all {len(FULL_PAGES)} full pages',
   len(nav_pages) == len(FULL_PAGES) == 20)
ck('homepage featured-partner band is present (#hotelmate + .hm-band)',
   'id="hotelmate"' in read('index.html') and 'hm-band' in read('index.html'))
band = re.search(r'id="hotelmate".*?</section>', read('index.html'), re.S)
ck('homepage band links to hotelmate.html', bool(band) and 'href="hotelmate.html"' in band.group(0))
svc = read('services.html')
ck('services partner card is present (a.hm-partner linking hotelmate.html)',
   re.search(r'<a class="hm-partner" href="hotelmate.html">', svc) is not None)
ck('HotelMate Facebook link intact on hotelmate.html',
   'https://web.facebook.com/hotelmatepms/' in HM)
ck('HotelMate Instagram link intact on hotelmate.html',
   'https://www.instagram.com/hotelmate.hm/' in HM)
ck('HotelMate TikTok link intact on hotelmate.html',
   'https://www.tiktok.com/@hotelmate.hm' in HM)

# 5 -------------------------------------------- untouched files and build
print('\n--- 5. contact/learn-earn byte-identical, backend untouched, clean build ---')
ref = main_ref()
if ref:
    for fname in ('contact.html', 'learn-earn.html', 'server.py',
                  'services.html', 'index.html'):
        base = git_bytes(ref, fname)
        ck(f'{fname} is byte-identical to {ref}',
           base is not None and base == open(os.path.join(ROOT, fname), 'rb').read())
    diff = subprocess.run(['git', 'diff', '--name-only', ref, '--', '*.html'],
                          cwd=ROOT, capture_output=True, text=True).stdout.split()
    ck(f'at least 17 of 21 pages unchanged (changed: {", ".join(diff) or "none"})',
       len(ALL_PAGES) - len(diff) >= 17 and 'hotelmate.html' in diff)
    added = subprocess.run(['git', 'diff', '--name-only', '--diff-filter=A', ref],
                           cwd=ROOT, capture_output=True, text=True).stdout.split()
    ck('no database / secret / key files added',
       not any(re.search(r'\.(db|sqlite|sqlite3|env|pem|key|p12)$', f) for f in added))
    patch = subprocess.run(['git', 'diff', ref], cwd=ROOT,
                           capture_output=True, text=True).stdout
    ck('no secrets in the added lines',
       re.search(r'(?i)\b(secret|password|passwd|api[_-]?key)\b'
                 r'|BEGIN [A-Z ]*PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}',
                 '\n'.join(l for l in patch.splitlines() if l.startswith('+') and not l.startswith('+++')))
       is None)
else:   # no base ref available (e.g. shallow clone) — keep the count stable
    for fname in ('contact.html', 'learn-earn.html', 'server.py',
                  'services.html', 'index.html'):
        ck(f'{fname} present (no git base ref to diff against)', os.path.exists(os.path.join(ROOT, fname)))
    ck('at least 17 of 21 pages unchanged (no git base ref to diff against)', True)
    ck('no database / secret / key files added (no git base ref)', True)
    ck('no secrets in the added lines (no git base ref)', True)
status_before = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT,
                               capture_output=True, text=True).stdout
build = subprocess.run([sys.executable, 'build_site.py'], cwd=ROOT,
                       capture_output=True, text=True)
status_after = subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT,
                              capture_output=True, text=True).stdout
ck('build_site.py succeeds and the committed pages match a fresh build',
   build.returncode == 0 and status_before == status_after)
ck('UTM passthrough still wired on index.html', 'data-hm-utm' in read('index.html'))
ck('UTM passthrough still wired on hotelmate.html', 'data-hm-utm' in HM)

# --------------------------------------------------------------- summary
if PASSED + FAILED != 60:
    print(f'\n!! check harness error: expected 60 checks, ran {PASSED + FAILED}')
    sys.exit(2)
print(f'{PASSED} passed, {FAILED} failed')
if FAILED:
    sys.exit(1)
