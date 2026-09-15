CEYTEQ — CEYLON TECHNOLOGY — Website + Backend v3.1 (2026-09-14)
================================================================

WHAT THIS IS
  The full Ceyteq company website (8 service divisions) with the Digital
  Race program as the highlighted main service, PLUS a real backend
  (server.py) with a database for flyers and customer enquiries.

  It runs in two ways:
   1. STATIC (GitHub Pages / Netlify drop / Cloudflare Pages)
      Just the HTML files. Contact form falls back to WhatsApp, the
      flyers page uses the built-in 10 flyers, admin panel says
      "server offline". Nothing breaks.
   2. SERVER MODE (recommended)
      python3 server.py  ->  static site + JSON API + SQLite database
      Enquiries are saved in the database, flyers are managed from the
      admin panel, admin login is real (hashed password + session).


RUN IT (2 minutes)
  python3 server.py --init --admin-password 'YourStrongPassword'
  python3 server.py
  -> open http://localhost:8000        (site)
  -> open http://localhost:8000/admin.html   (admin panel)

  Without --admin-password the first run generates a random one and
  prints it ONCE on the console. Change it any time:
     python3 server.py --set-password admin NEWPASSWORD
  Restore the 10 shipped flyers:  python3 server.py --reseed-flyers
  Options: --host 0.0.0.0  --port 8000   (env: CEYTEQ_ADMIN_USER /
  CEYTEQ_ADMIN_PASSWORD for automated deploys)


PAGES (20 + 1 redirect)
  index.html          HOME — company: hero, Digital Race highlight,
                      9 service cards, platforms, why Ceyteq, Ceylon
                      Voyage teaser. No long price lists.
  digitalrace.html    DIGITAL RACE (main service) — program intro, the
                      intro video, quick answers FAQ, why now, mission,
                      5 doors (System / Training / Packages / AI /
                      Flyers) and the AI roadmap section (#ai).
  services.html       All 8 service divisions + how-we-work steps.
  web.html            01 Web Services — platforms, e-commerce, SEO,
                      Google Business Profile, booking channels,
                      hosting, AI messaging + website packages table.
  ads.html            02 Advertising — social ads, Google Ads, traffic
                      campaigns, $1–$2/day ad-spend model.
  print.html          03 Printing & Digital — offset, packaging,
                      signage/LED, paper bags, food packing, merch.
  media.html          04 Photography & Video — events, weddings,
                      cultural events, products, business places.
  design.html         05 Design & Editing — graphic, flyer, poster,
                      photo editing, video editing, filming.
  ai.html             06 AI & ERP — chatbots, voice bot, CRM, AI
                      customer care, hospitality & retail ERP + pricing.
  travel.html         07 Ceylon Voyage — itineraries, hotels, vehicles,
                      event tickets, tourist info, air tickets &
                      emigration information (LK + France offices).
  careers.html        08 Careers — roles, how to apply, internships.
  learn-earn.html     LEARN & EARN — 8 professional courses (digital
                      marketing, AI, web, design, video, photography,
                      print, travel) at 3 levels: Foundation $19 /
                      Professional $60 / Elite $150, Career Bundle
                      $250. Enrolment form saves to the database.
  contact.html        Contact hub — WhatsApp/hotline/email + enquiry
                      form that SAVES TO THE DATABASE (falls back to
                      WhatsApp when the backend is offline).
  packages.html       Digital Race 4 packages (locked prices) + FAQ.
  system.html         Digital Race — the Matrix system.
  training.html       Digital Race — 90-day roadmap.
  offers.html         OFFERS (was "flyers") — gallery of the 10
                      ready-to-share offers (reads the database first,
                      then the Google Sheet, then the built-in list)
                      + hidden Admin Login link.
  hotelmate.html      HOTELMATE PARTNER CAMPAIGN — Ceyteq's featured hospitality
                      technology partner. Campaign offer, the WhatsApp-first flow
                      (WhatsApp -> Ceyteq qualification -> HotelMate back-office
                      final demo), HotelMate social links and an enquiry form
                      that saves to the same leads table. UTM parameters on the
                      page URL are passed through to the WhatsApp links.
  flyers.html         redirect to offers.html (old links keep working).
  admin.html          Admin panel — flyers CRUD (order, titles,
                      visibility, upload) + customer enquiries.

LANGUAGES
  [ENGLISH] Full English (DEFAULT) | [සිංහල] Full Sinhala | [FRANÇAIS] Full French
  Top-right switcher, remembered per visitor (localStorage) — a visitor
  who picks Sinhala keeps Sinhala on every page and every visit. Every label is translated
  (nav, tables, tiers, buttons, footer, form). Brand names, platform
  names and numbers stay universal by design.


BACKEND (server.py) — stdlib only, no pip install needed
  Database : SQLite at data/ceyteq.db (created automatically)
  Tables   : admins (PBKDF2-SHA256, 200k iterations) · flyers · leads
  Security : password hashed in DB — nothing secret in the HTML;
             HttpOnly + SameSite=Lax session cookie (7 days);
             JSON-only state changes; login rate-limited by delay;
             enquiry form limited to 5 submissions / IP / 10 min;
             path traversal and source files (server.py, data/, .git)
             are not servable; all API output JSON-escaped.
  API
    public  GET  /api/health                     server + row counts
            GET  /api/flyers                     visible flyers (ordered)
            POST /api/leads                      save an enquiry
    admin   POST /api/login | /api/logout        session
            GET  /api/me
            GET|POST        /api/admin/flyers
            PATCH|DELETE    /api/admin/flyers/<id>
            POST            /api/admin/flyers/reorder
            POST            /api/admin/upload    (png/jpg/webp/gif, ≤8 MB)
            GET             /api/admin/leads
            PATCH|DELETE    /api/admin/leads/<id>
  Backup: copy data/ceyteq.db (that file is the whole database).

  Deploy: any host that runs Python 3, behind HTTPS.
    * Render / Railway / Fly.io free tier: start command `python3 server.py`
      (set CEYTEQ_ADMIN_PASSWORD in the environment).
    * VPS: run with systemd + nginx reverse proxy (or the
      --host 0.0.0.0 --port 8000 defaults directly).
    * cPanel shared hosting cannot run this file — keep the static mode
      there, or use the PHP/MySQL variant if you need one.
  GitHub Pages cannot run Python: the site there stays static and the
  admin/DB features are simply not available (no error, just fallback).


FILES
  *.html                       the 19 pages (generated — do not hand-edit)
  build_site.py                builds all pages (path-independent)
  content_services.py          all main-site service content (edit text here)
  content_hotelmate.py         HotelMate campaign layer: colours, campaign
                               WhatsApp number, homepage band, Services partner
                               card, the /hotelmate.html page, UTM passthrough
                               and campaign CSS. Additive and isolated: Ceyteq
                               content is not rewritten by it.
  assets/hotelmate-logo.png    HOTELMATE LOGO — NOT SUPPLIED YET. Until the file
                               exists the build renders a CSS wordmark; drop the
                               supplied logo in (png/svg/jpg) and re-run
                               build_site.py — every HotelMate mark switches to
                               the real logo with no code change. (Also accepted:
                               assets/hotelmate-logo.svg / .jpg / .jpeg.)
  server.py                    backend: static + API + SQLite
  make_flyers.py               regenerates the 10 flyers (needs Pillow)
  assets/logo-transparent.png  logo (also used as favicon)
  assets/logo.jpg, logo-crop.jpg, *.ttf   source images + flyer fonts
  assets/intro-720p.mp4        Digital Race intro video (15.9 MB)
  flyers/flyer-01..10.png      the 10 shareable flyers (1080×1350)
  data/ceyteq.db               database (created at runtime, gitignored)
  uploads/                     free folder for future uploads (gitignored)
  .gitignore  README.txt  AUDIT-REPORT.md

REBUILD THE PAGES:      python3 build_site.py
REGENERATE THE FLYERS:  python3 make_flyers.py   (pip install Pillow)
RUN THE SITE LOCALLY:   python3 server.py --port 8000


HOTELMATE FEATURED-PARTNER CAMPAIGN (see content_hotelmate.py)
  Nav: a 10th item "HotelMate" (brand name identical in EN/SI/FR per the site
  rule) on all 20 pages, styled as a partner pill, not as a Ceyteq division.
  Home: #hotelmate band under the Digital Race feature block — two buttons only:
  "Explore HotelMate" -> hotelmate.html and "WhatsApp a HotelMate specialist"
  -> https://wa.me/94768607143. No price is shown on the homepage.
  Services: a "Technology partners" section with the HotelMate card, added AFTER
  the 08 divisions — nothing removed or renumbered.
  Colours: HotelMate #00AEEF, site accent #27A3C9, navy #1A1A2E. Small text on
  white uses a darker tint of the brand blue (#0179AB) because #00AEEF on white
  fails WCAG AA; every fill and border uses the approved #00AEEF exactly.
  Campaign wording rules: the setup-fee waiver and US$39/month are written ONLY
  on hotelmate.html and always "for the campaign period"; the page states the
  offer is not permanently free; no "official partner", no testimonials, no
  revenue or occupancy guarantees. "Demo coordination by Ceyteq. Final product
  demo and activation are completed with the HotelMate team." is printed on all
  three campaign views. The campaign WhatsApp number is +94 76 860 7143, and on
  this page only, the form's offline WhatsApp fallback is routed to that number
  too (window.CEYTEQ_ENQ; other pages keep the Ceyteq hotline).
  To remove the campaign: delete the content_hotelmate imports + the two call
  sites in content_services.py, the HotelMate nav item and the two hotelmate
  entries in build_site.py, then rebuild.

ALWAYS-ON FLOATING ACTIONS (every page)
  * "Start Digital Race" (red, pulsing) -> digitalrace.html#start
  * WhatsApp circle (green, pulsing)    -> wa.me/94768607143
  Both animate gently (ring pulse + bob) and switch off automatically for
  visitors who set "reduce motion" in their system. Red is also used for
  the "Digital Race" menu item and the Digital Race headline.

COURSE FEES (the only prices not from the original price lock — confirm
them before publishing: Foundation $19, Professional $60, Elite $150,
Career Bundle $250 per student)

PRICE LOCK (never alter)
  Starter $19 | $3–5/mo :: Standard $60 | 10/15/20
  Advanced $80 | 15/20/30 (+Voice $15) :: Premium $250 | $150 flat
  Client ad spend $1–$2/day direct to platforms. Ceyteq optimization FREE.
  Print / media / design / travel work is quoted per job — the backend
  and pages use "quote on request" wherever a price is not locked above.


CONTACT
  Hotline  +94 78 860 7143      WhatsApp +94 76 860 7143
  France   +33 7 44 28 42 69    Email    info.ceyteq@gmail.com
  Web      www.ceyteq.lk        Social   @ceyteq (FB, IG, TikTok, YT,
                                         LinkedIn, Pinterest, X)

NEXT STEPS (talk to us before adding)
  * compress the 15.9 MB intro video (or host it on YouTube)
  * analytics dashboard (visits, pages, flyer clicks) in the admin
  * multi-client mode: give each restaurant its own admin panel
    (this is what the Standard/Advanced "Admin Panel" promise can become)
