# CEYTEQ Digital Race — Site Audit + Fix Report

**Date:** 2026-09-14
**Branch:** `arena/01a0a0ff-digitalrace`
**Scope:** whole website (`index, system, training, packages, ai, flyers, admin` + build scripts)
**Status:** 🔴 red-flag bugs fixed · 🟠 security items pending backend · 🟢 improvements applied

---

## 1. හමුවුණු අඩුපාඩු (Defects Found)

### 🔴 Critical — site එක live එකේ කැඩිලා තිබ්බා

| # | අඩුපාඩුව | සැබෑ තත්ත්වය | තත්ත්වය |
|---|---|---|---|
| 1 | **Flyers පිටුවේ ෆ්ලයර් 10ම කැඩිලා** — HTML එකේ `src="flyers/flyer-01-...png"` කියලා තියෙනවා, නමුත් repo එකේ `flyers/` folder එකක් **නෑ**. PNG files root එකේ. | Live site එකේ broken-image icon 10ක් පෙන්නුවා | ✅ නිවැරදි කළා |
| 2 | **Home page video එක කැඩිලා** — `src="assets/intro-720p.mp4"`, නමුත් video එක root එකේ තිබ්බා. | "Watch: Digital Race introduction" කොටස play වුණේ නෑ | ✅ නිවැරදි කළා |
| 3 | **`build_site.py` run වෙන්නේම නෑ** — `ROOT = '/home/user/ceyteq-digital-race'` කියලා hardcode කරලා. | README එකේ කියන විදියට rebuild කරන්න ගියාම `FileNotFoundError` | ✅ නිවැරදි කළා |
| 4 | **`make_flyers.py` — ඒ වගේම hardcoded paths** (`assets/`, `flyers/`). | ෆ්ලයර් regenerate කරන්න බෑ | ✅ නිවැරදි කළා |
| 5 | **"Database" එක (Google Sheet) හිස්** — Sheet එක පිටුවක් තියෙනවා, නමුත් `file \| title_en \| title_si \| title_fr \| visible` rows **paste කරලා නෑ**. | Admin page එකේ `EMPTY` කියලා පෙන්නනවා — data එකක් නෑ | ⚠️ Backend + DB එකක් ඕන (පහළ බලන්න) |

### 🟠 Security

| # | ප්‍රශ්නය | විස්තරය | තත්ත්වය |
|---|---|---|---|
| 6 | **Admin "login" එක ඇත්තටම login එකක් නොවෙයි** | `ADMIN_SIG = base64('admin::ceyteq@2026')` කියන එක **හැම visitor ගේම browser එකට** යවනවා. දන්න කෙනෙක්ට base64 decode කරලා password එක කියවන්න පුළුවන්. අනික README එකේ password එක plain text වල තියෙනවා. `sessionStorage.setItem('ceyteq_admin','1')` කියලා console එකෙන් type කරාම ඕන කෙනෙක්ට dashboard එකට ඇතුළු වෙන්න පුළුවන්. | ⚠️ Backend auth එකකින් විසඳන්න ඕන |
| 7 | **XSS** (script injection) | Google Sheet එකේ cell එකක `<img onerror=...>` වගේ දෙයක් තිබ්බොත් ඒක හැම visitor ගේම browser එකේ run වෙනවා (Sheet data එක `innerHTML` හරහා ගිය නිසා). | ✅ Escape කළා (`esc()` + `safeSrc()`) |
| 8 | **Sheet ID + credentials client-side** | Sheet එක public-read නිසා flyer list එක කවුරුත් බලන්න පුළුවන් — හානියක් නෑ, නමුත් editing වලට real backend එකක් හොඳයි. | ℹ️ |

### 🟡 Cleanup / quality

| # | දේ | තත්ත්වය |
|---|---|---|
| 9 | `index_template.html` — පරණ **dark-theme** version එකක්, කිසිම script එකකින් use කරන්නේ නෑ, `{{LOGO_DATA_URI}}` placeholder එකත් unresolved. | ✅ අයින් කළා (git history එකේ safe) |
| 10 | `download` (ඇත්තටම `.gitignore` content එකක්), `download (1)` (0 bytes) — junk files. | ✅ අයින් කරලා ඇත්ත `.gitignore` එකක් දැම්මා |
| 11 | `name="description"`, OG tags, favicon **කිසිම page එකක නෑ** — WhatsApp/FB වල link එක share කරාම preview එකක් එන්නේ නෑ. | ✅ හැම page එකකටම දැම්මා (og:image = flyer) |
| 12 | README එකේ pages 6 කියලා තියෙනවා, ඇත්තටම 7ක්. Paths වැරදි. | ✅ README update කළා |
| 13 | Home page video 15.9 MB — mobile data වලට බරයි, GitHub Pages slow. | ℹ️ යෝජනාව: compress කරන්න හෝ YouTube/Dailymotion embed කරන්න |

---

## 2. කළ නිවැරදි කිරීම් (Fixes Applied)

**Folder structure එක දැන් HTML එකේ හතරවන path වලට ගැලපෙනවා:**

```
digitalrace/
├── index.html  system.html  training.html  packages.html
├── ai.html     flyers.html  admin.html      ← build එකෙන් generate වෙනවා
├── build_site.py   make_flyers.py           ← දැන් ඕනෑම machine එකක run වෙනවා
├── assets/
│   ├── logo-transparent.png  logo.jpg  logo-crop.jpg
│   ├── intro-720p.mp4                       ← video එක දැන් හරි තැන
│   └── *.ttf                                ← Sinhala/Inter/Montserrat fonts
├── flyers/
│   └── flyer-01 … flyer-10 .png             ← ෆ්ලයර් 10 දැන් හරි තැන
├── .gitignore   README.txt   CNAME   AUDIT-REPORT.md
```

**Verify කළා:**

- `python3 build_site.py` → `BUILD OK`, pages 7ම regenerate වුණා.
- Link checker: **broken local references = 0** (කලින් 21ක් තිබ්බා).
- හැම page එකකම visible text content **100% කලින් වගේම** (similarity 1.0000) — rebuild එකෙන් කිසි content එකක් නැති වුණේ නෑ.
- Local server එකකින් හැම asset එකක්ම `200 OK`.
- Sheet data escaping (XSS fix) දෙන පිටුවේම (flyers + admin).
- හැම page එකකටම: description, canonical, og:title/description/image, twitter card, favicon, theme-color.

---

## 3. Backend + Database — තත්ත්වය සහ යෝජනාව

**දැන් තියෙන තත්ත්වය:** site එක **සම්පූර්ණයෙන් static** (GitHub Pages). "Database" එක කියන්නේ Google Sheet එකක් — සහ ඒක **හිස්**. Admin panel එක නම් බලන්න විතරයි; **ඇත්තටම edit කරන්න බෑ**.

**Backend එකකින් ලැබෙන දේවල්:**

1. **ඇත්තටම වැඩ කරන Admin login** — password එක hash කරලා (bcrypt) DB එකේ, session/token එකකින්. Credentials කවදාවත් browser එකට යන්නේ නෑ.
2. **Real database** — ෆ්ලයර්, packages, leads, visits වගේ දේවල් SQL database එකක (Google Sheet නොවෙයි).
3. **Flyers management UI** — upload, edit, reorder, hide/show — Google Sheet එකේ manual copy-paste නැතුව.
4. **Lead capture (contact form)** — දැන් customer කෙනෙක්ට message එකක් තියන්න form එකක් නෑ, Telegram/WhatsApp විතරයි. Form එකක් තිබ්බොත් leads DB එකේ save වෙනවා → ඔබට නැතිවුණු lead එකක් නෑ.
5. **Analytics** — කී දෙනෙක් ආවාද, කවර page එක බැලුවාද, කිනම් flyer එකෙන් ආවාද (රූ 1000ක් මිසින් වෙනවා නම් ඒක පෙනෙනවා).
6. **Multi-client option** — ඔබේ Standard/Advanced packages වල "Admin Panel" කියලා දෙනවා නේ. Backend එකක් තිබ්බොත් ඒක **restaurant/clients ලා 5-10 දෙනෙකුටත්** දෙන්න පුළුවන් (multi-tenant) — ඒකම ඔබේ product එක වෙනවා.

**Hosting ගැන වැදගත් කරුණ:** GitHub Pages එකට **Python/Node/PHP run කරන්න බෑ** (static විතරයි). ඒ නිසා backend එකට වෙන host එකක් ඕන — ඒක තමයි ඊළඟ තීරණය. හැම option එකක්ම පහත ප්‍රශ්නවල තියෙනවා.

> 💡 මගේ default යෝජනාව: **Python + FastAPI + SQLite** (single file `server.py`, extra service එකක් ඕන නෑ, local එකේ test කරන්න පුළුවන්, පස්සේ Postgres/MySQL එකට migrate කරන්නත් ලේසි) — site එකේ HTML pages ටික **එහෙම්මම** තියලා, `/api/...` endpoints හරහා backend එකට connect කරනවා. එතකොට design එකට කිසිම හානියක් නෑ.

---

# Round 2 — Main Ceyteq website + Backend + Database (2026-09-14)

**Request:** the Digital Race site was standing in for the whole company.
Home page must lead into **Digital Race** as the main service, and the
**full Ceyteq website** (company profile + all 8 service divisions) had to
be built *with* a backend and a database.

## 2.1 What was built — main website (18 pages)

| Page | Content |
|---|---|
| `index.html` | Company home: hero, **Digital Race highlighted as the main service**, 9 service-division cards, platform list, why-Ceyteq, Ceylon Voyage teaser |
| `services.html` | All 8 divisions in one grid + 5-step "how we work" |
| `web.html` | 01 — web platform creation & optimization, social networks + Google, business web network listings (Booking.com, Airbnb, Agoda, Expedia, HostelWorld, TripAdvisor, PikMe, Uber), hosting, AI messaging, website package table |
| `ads.html` | 02 — social ads (FB, IG, TikTok, X, Pinterest, Reddit, Threads, LinkedIn), Google Ads (search/display/business/YouTube/email), web-traffic campaigns, ad-budget model |
| `print.html` | 03 — general & offset printing, packaging, labels, digital signage / LED boards / laser printing, paper bags, gift & kraft boxes, food packing, T-shirts, mugs |
| `media.html` | 04 — events, weddings, cultural events, products, business places, reels, coverage packages |
| `design.html` | 05 — photo editing, graphic design, flyer/poster design, video editing, filming, monthly content packs |
| `ai.html` | 06 — chatbots, voice bot, AI customer care, CRM automation, hospitality & retail ERP, AI consulting + AI pricing |
| `travel.html` | 07/08 — **Ceylon Voyage**: itineraries, hotels, transport, event tickets, vehicle booking for foreigners, tourist-area directory, air tickets & emigration information, Sri Lanka + France offices |
| `careers.html` | 08 — open roles, how to apply, internships |
| `contact.html` | Contact hub + **working enquiry form** |
| `digitalrace.html` | The whole Digital Race program (old home) + the AI roadmap section, so the program keeps its own home now |
| `about.html` | Company profile text (EN/SI/FR), mission, who we serve, Sri Lanka + France |
| `packages / system / training / flyers / admin` | Kept, unchanged in content, prices still locked |

* Every new page is fully trilingual (Sinhala / English / French) with the
  same switcher and the same visual language as the existing site.
* Navigation is now: Home · Digital Race · Services · Packages · Flyers ·
  About · Careers · Contact (the old System/Training/AI pages are linked
  from inside Digital Race, so nothing was lost).
* **Page weight cut by ~90%:** the logo was inlined as base64 into every
  page (≈290 KB each, 603 KB home). It is now a normal file — pages are
  32–48 KB, which matters a lot on Sri Lankan mobile data.

## 2.2 What was built — backend + database (`server.py`)

* Python standard library only — **no pip install**, one file, runs anywhere.
* SQLite database `data/ceyteq.db` with `admins`, `flyers`, `leads`.
* Serves the static site **and** a JSON API on one port.
* Flyers page reads the **database first**, then the Google Sheet (static
  hosting), then the built-in 10 — so GitHub Pages keeps working as before.

**Admin panel is now real:**

* Login verified server-side against a PBKDF2-SHA256 hash (200 000
  iterations) — the password is **no longer inside the HTML** (finding #6
  from the first audit is closed by design, not by obscurity).
* Session cookie: HttpOnly, SameSite=Lax, 7 days, HMAC-signed.
* Flyers tab: reorder (↑ ↓), hide/show, edit titles, delete, and **upload
  new flyer images** (png/jpg/webp/gif, ≤ 8 MB) straight from the browser.
* Enquiries tab: every contact-form submission is stored, marked new/done,
  with one-click WhatsApp reply and delete.
* Setup tab keeps the Google-Sheet instructions for static hosting.

**Public API:** `GET /api/health`, `GET /api/flyers`, `POST /api/leads`.
**Admin API:** login/logout/me, flyers CRUD + reorder + upload, leads list/patch/delete.

## 2.3 Security hardening added this round

| Item | Status |
|---|---|
| Credentials in client HTML (old `admin::ceyteq@2026`) | ✅ removed — server-side hash + session |
| Enquiry form spam | ✅ 5 submissions / IP / 10 minutes |
| CSRF on state-changing calls | ✅ JSON-only + SameSite=Lax cookie |
| Path traversal / source download | ✅ `data/`, `.git`, `server.py`, `build_site.py`, `README.txt`, database file all return 403 |
| Login brute force | ✅ 350 ms delay per attempt, no user enumeration |
| XSS from database/Sheet values | ✅ all output HTML-escaped (round 1 fix still in place) |

## 2.4 How to run it

```bash
python3 server.py --init --admin-password 'YourStrongPassword'   # first time
python3 server.py                                                # start
# site   http://localhost:8000
# admin  http://localhost:8000/admin.html
```

Production notes: put it behind HTTPS, set `CEYTEQ_ADMIN_PASSWORD` in the
environment for automated deploys, and back up `data/ceyteq.db` (that one
file is the whole database). GitHub Pages cannot run Python — there the site
stays static and the admin/database features are simply unavailable, with
no broken pages.

## 2.5 Still open (your decisions)

1. **Deploy target** for the backend: Render / Railway / Fly.io free tier,
   a VPS, or cPanel-PHP+MySQL instead of Python.
2. **Print / media / travel prices** — those pages currently say
   "quote on request". Give me your price list (LKR or $) and I'll insert
   it exactly like the locked Digital Race prices.
3. **Company details** — physical address(es), opening hours, registration
   numbers, team photos: anything you want on `about`/`contact`.
4. **Video** — 15.9 MB is heavy for mobile; compress it or host on YouTube.
5. **Analytics + multi-client admin** (one panel per restaurant client) —
   the natural next build once the backend is hosted.

---

# Round 3 — Language, branding, always-on CTA, Learn & Earn, Offers (2026-09-14)

**Request:** default language English · "Digital Race" in red · an
always-visible, animated **Start Digital Race** button (like the WhatsApp
button) on every page · a new **Learn & Earn** page with professional
courses tied to our services (digital marketing, AI, …) · rename
**Flyers → Offers**.

| # | Change | Where it lives now |
|---|---|---|
| 1 | **Default language = English** (Sinhala/French still one click away; a visitor's own choice is remembered) | `build_site.py` — `<html lang>`, `data-langmode`, switcher JS, admin `T()` |
| 2 | **"Digital Race" in red** — menu item red, Digital Race headline red, red buttons | `--red:#d81f26`, `.r`, `.btn-red`, `nav .links a.hot` |
| 3 | **Always-on, animated "Start Digital Race"** button on **all 19 pages**, stacked above the WhatsApp button (both now pulse + bob) | `.floats`, `.fab`, `.fab.wa` + `@keyframes ringRed / ringGreen / fabBob`; anchor target `digitalrace.html#start` |
| 4 | **New START section** on the Digital Race page (3 steps + WhatsApp / Packages / form buttons) | `#start` section |
| 5 | **Learn & Earn page** — 8 professional courses (digital marketing, AI & automation, web, graphic design, video editing, photography, print & packaging, travel & tourism) at 3 levels | `learn-earn.html` + `content_services.py` |
| 6 | Course enrolment form saves to the database like the contact form | `#enquiryForm` reuses the same API + WhatsApp fallback |
| 7 | **Flyers → Offers**: menu, page, headings, admin tab, meta, teasers | `offers.html` (+ `flyers.html` now redirects, so shared links never break) |

**Design decisions worth knowing**

* Red is a brand accent only — cyan (`#27a3c9`) and navy stay the base
  colours, so the site keeps the same identity it had.
* Animations stop automatically for visitors whose device sets
  "reduce motion" (accessibility).
* Course fees are the one price set that is **not** part of the locked
  Digital Race price list: Foundation $19 · Professional $60 ·
  Elite $150 per course · Career Bundle (all 8 + mentorship) $250.
  Confirm or change them before publishing.
* The word "flyer" is kept only where it describes the artwork format
  (e.g. the "Flyer design" service and the monthly content counts in the
  packages) — every page name and menu label now says **Offers**.

## Verification (this round)

* 19 pages + `flyers.html` redirect build cleanly (`BUILD OK`), **0 broken
  local links**, every page carries the two floating buttons, and all pages
  still serve 200 from the running server (`python3 server.py`).
* Admin panel: the Offers tab manages the same database rows as before
  (reorder, hide, edit, upload, delete) — only the labels changed.
