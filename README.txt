CEYTEQ DIGITAL RACE — Website Pack v2.4 (2026-09-14)
================================================
UI SKIN: Hotelmate-matched design language (inspiration only, no content
copied): Mona Sans font, primary #27A3C9, dark teal #0c1e21, page bg
#ecf0f0, pill buttons, 12px cards, kicker+H2 sections, pastel animated
hero panel, dark CTA, scroll-reveal. Fonts load when hosted (graceful
system-font fallback in offline preview).
THEME: Light ash background + white cards + navy blue + logo cyan.
LOGO: Transparent (assets/logo-transparent.png) — no white box.
LANGUAGES (exclusive, default Full Sinhala):
  [සිංහල] Full Sinhala | [ENGLISH] Full English | [FRANÇAIS] Full French
  Every label translated incl. nav, tables, tiers, months, footer,
  switcher, tab title. Only brand names/numbers stay universal.
HOME = zero package details (except general $1-2/day ad-spend FAQ).
CONTACT lives on sub-pages (esp. Packages).

PAGES (6) — open index.html, use top menu:
  index.html    = HOME (no prices, no contact block):
                  Hero (Digital Race + Alien Method highlight)
                  -> What is Digital Race? -> Quick Answers (+package link)
                  -> Why Now -> Mission -> 5 tagline teasers -> mini footer
  system.html   = Matrix windows, $1-2/day, launch steps
                  + Keep-exploring tags + Contact at bottom
  training.html = 90-day roadmap + daily habits + tags + Contact
  packages.html = All 4 packages (exact locked prices) + Package
                  Questions FAQ + tags + Contact at bottom
  ai.html       = AI today/tomorrow + roadmap + tags + Contact
  flyers.html   = Gallery of 10 flyers + tags + Contact
  CONTACT lives on sub-pages (esp. Packages); nav Contact
  jumps to packages.html#contact. Floating WhatsApp on all pages.

LANGUAGES (top-right switcher, auto-remembered):
  [සිංහල]  Full Sinhala (default)
  [ENGLISH] Full English
  [FRANÇAIS] Full French

FLYERS x10 in ./flyers/ (1080x1350, bilingual EN+SI):
  01 program-intro  02 why-now  03 what-changes  04 how-it-works
  05 training-90-day  06 starter $19  07 standard $60
  08 advanced $80  09 premium $250  10 ai-future-contact

PRICE LOCK (never alter):
  Starter $19 | $3-5/mo :: Standard $60 | 10/15/20
  Advanced $80 | 15/20/30 (+Voice $15) :: Premium $250 | $150 flat
  Client ad spend $1-$2/day direct to platforms. Ceyteq optimization FREE.

SHARE AS ONE LINK (free): drag this folder to app.netlify.com/drop
  (or Vercel / GitHub Pages / Cloudflare Pages).

REBUILD: python3 build_site.py  (regenerates all 6 pages from templates)
REGENERATE FLYERS: python3 make_flyers.py

CONTACT: Hotline +94 78 860 7143 | WhatsApp +94 76 860 7143
Intl WA +33 7 44 28 42 69 | info.ceyteq@gmail.com | @ceyteq

ADMIN (v2.5):
  Page: admin.html — entry ONLY via small "Admin Login" link at the
  bottom of the Flyers page (not in main menu).
  Login: user=admin  pass=ceyteq@2026
  Change it: edit ADMIN_SIG in build_site.py (generate with the
  python one-liner in the comment), then: python3 build_site.py
  NOTE: front-end lock for a static site — keeps casual visitors
  out, not hacker-proof. Real auth needs a backend later.
DATABASE (Google Sheet = live flyer list):
  Sheet: https://docs.google.com/spreadsheets/d/1iT7QmbY0b-u5xjmGcaHBw8vOOpu2xNb5GTuKaPVBaKw/edit
  First tab, row 1: file | title_en | title_si | title_fr | visible
  Paste the 10 ready rows from the Admin page copy-box (cell A1).
  Sharing must stay: Anyone with link = Viewer.
  Flyers page auto-loads Sheet rows when online (else built-in 10).
  visible=NO hides a flyer. Drag rows to reorder. File = name in
  flyers/ folder (or full https URL).
