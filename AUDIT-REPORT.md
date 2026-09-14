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
