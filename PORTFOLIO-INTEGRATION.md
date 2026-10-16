# Ceyteq Portfolio Page — Integration Guide

The complete page is `portfolio.html`. Its CSS and JavaScript are embedded, so the only local file dependency is the existing Ceyteq logo at `assets/logo-transparent.png`. The Client Work section additionally reads `GET /api/portfolio` (see below) and degrades to an explainer when no backend is reachable.

## Add it to an existing website

1. Upload `portfolio.html` to the website document root, beside `index.html`.
2. Keep `assets/logo-transparent.png` in the existing `assets/` directory. If the page is installed in a subdirectory, update the two logo paths in `portfolio.html`.
3. Add the Portfolio navigation link shown below to the shared header/template. In this repository it is already added to `build_site.py`, so rebuilding keeps the link on generated pages.
4. Confirm these URLs after upload:
   - `https://www.ceyteq.linkpc.net/portfolio.html`
   - `https://www.ceyteq.linkpc.net/assets/logo-transparent.png`
5. Test the five service tabs, keyboard arrow navigation, mobile hamburger menu, counter animations, WhatsApp quote links, email and telephone links, and the Client Work block (Clients/Services buttons, search bar, category chips, media viewer, client logo strip). `node check_portfolio.mjs` exercises all of that against a running backend.
6. Replace the Open Graph image if a dedicated 1200 × 630 portfolio share image becomes available. The current fallback is `assets/logo.jpg`.
7. Clear any hosting/CDN cache and submit `portfolio.html` in Google Search Console or include it in the site's sitemap.

## Navigation snippet

Add this anchor alongside the existing header links:

```html
<a href="portfolio.html" aria-current="page">Portfolio</a>
```

Only include `aria-current="page"` while rendering `portfolio.html`. On every other page use:

```html
<a href="portfolio.html">Portfolio</a>
```

The equivalent multilingual link for the current Ceyteq header is:

```html
<a href="portfolio.html">
  <span class="lang-en">Portfolio</span>
  <span class="lang-si">Portfolio</span>
  <span class="lang-fr">Portfolio</span>
</a>
```

## Brand variables

The page's theme can be aligned with a future site redesign by changing only these variables at the beginning of the embedded `<style>` block:

```css
:root {
  --page-bg: #ecf0f0;
  --primary-dark: #0c1e21;
  --primary-blue: #16424b;
  --accent-gold: #27a3c9; /* Portfolio alias for the Ceyteq cyan accent */
  --accent-gold-hover: #1b7a99;
  --text-white: #0c1e21;
  --text-gray: #52696d;
  --card-bg: #ffffff;
  --card-bg-hover: #f4fafa;
  --surface: #ffffff;
  --tint: #d8e5e5;
  --line: #c9d1d1;
}
```

## Client Work section (fed by the admin form)

Below **Our Services**, `portfolio.html` renders the client projects that the
Ceyteq team publishes in `admin.html` → **Portfolio Upload**. The page reads
`GET /api/portfolio` and paints one card per entry, using the same cards, chips
and hover style as the rest of the page.

| Form field (admin) | Card on `portfolio.html` |
|---|---|
| Client Name | small caps line above the headline, and the animated logo strip |
| Project Title | card headline (falls back to “<client> — Ceyteq project”) |
| Area | 📍 in the meta line |
| Business Category | badge on the cover image + the filter chip row |
| Service Model (tick many) | meta line; also the grouping used by the **Services** button |
| Image / Video links, uploaded images | cover image + **Media (n)** viewer (Drive, YouTube, Vimeo, mp4, png/jpg) |
| Folder Link | 📁 button on the card and in the viewer |
| Client website link | 🌐 button |
| Service Tags | tag chips |
| Show on the Portfolio page | `visible` — hidden rows never reach the public feed |
| ★ Featured | pinned first + ★ ribbon |

Three UI pieces sit above the grid:

* **Clients / Services buttons** — the same data shown as a client list or
  grouped by the service model that was delivered (`?view=service` deep-links it).
* **Search bar** — filters client, area, category, service model, tags and date,
  all words must match (`?q=…` pre-fills it).
* **Client logo animation** — a logo strip under the grid that scrolls, pauses on
  hover/focus and wraps instead when the visitor prefers reduced motion. Clicking
  a logo filters the grid to that client.

Counters: the stats band gains a live **Client Projects Published** number, driven
by the same feed.

### Publishing without the developer

1. Open `contact.html` → **Admin — Portfolio Upload** (top of the page) or `admin.html` directly.
2. Sign in (same session as the Offers/Enquiries tabs).
3. Fill the form. Only **Client Name** is required. Media can be pasted links
   (Google Drive share link, YouTube, direct image/video URL) or uploaded images,
   which are stored in `data/uploads/` beside the database.
4. **Save & publish** → refresh `portfolio.html#clients`. No rebuild, no redeploy.

The data lives in the `portfolio` table of `data/ceyteq.db`, so the normal
database backup already covers it. `POST/PATCH` need an admin session; `GET
/api/portfolio` is public, returns only visible rows and escapes nothing but
`http(s)` / on-server asset links, so a pasted `javascript:` value can never
become a link on the page.

### The two pick-lists

Business Category and Service Model come from `PORTFOLIO_CATEGORIES` /
`PORTFOLIO_SERVICES` in `build_site.py` (the admin form) and the same lists in
`server.py` (the API). Add a category there and it appears in the form, and the
Portfolio page picks it up as a filter chip automatically — chips are built from
the published data, not hard-coded.

### Static hosting

On GitHub Pages there is no `/api/portfolio`, so the Client Work section shows
one short explainer line instead of a broken grid (the rest of the page —
products, the 100-service tabs, counters — is untouched). Connect the backend to
publish client work.

## Contact and social links

Contact and social URLs use the currently published Ceyteq details. If any account changes, search `portfolio.html` for the old URL and replace all occurrences. Each service's **Get Quote** button creates a pre-filled WhatsApp message for `+94 78 860 7143`.

## Rebuild this repository

Generated Ceyteq pages should not be edited directly. Their shared navigation is maintained in `build_site.py`:

```bash
python3 build_site.py
```

`portfolio.html` is standalone and is intentionally not overwritten by that command.
