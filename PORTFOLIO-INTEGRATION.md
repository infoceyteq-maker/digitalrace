# Ceyteq Portfolio Page — Integration Guide

The complete page is `portfolio.html`. Its CSS and JavaScript are embedded, so the only local dependency is the existing Ceyteq logo at `assets/logo-transparent.png`.

## Add it to an existing website

1. Upload `portfolio.html` to the website document root, beside `index.html`.
2. Keep `assets/logo-transparent.png` in the existing `assets/` directory. If the page is installed in a subdirectory, update the two logo paths in `portfolio.html`.
3. Add the Portfolio navigation link shown below to the shared header/template. In this repository it is already added to `build_site.py`, so rebuilding keeps the link on generated pages.
4. Confirm these URLs after upload:
   - `https://www.ceyteq.linkpc.net/portfolio.html`
   - `https://www.ceyteq.linkpc.net/assets/logo-transparent.png`
5. Test the five service tabs, keyboard arrow navigation, mobile hamburger menu, counter animations, WhatsApp quote links, email and telephone links.
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

## Contact and social links

Contact and social URLs use the currently published Ceyteq details. If any account changes, search `portfolio.html` for the old URL and replace all occurrences. Each service's **Get Quote** button creates a pre-filled WhatsApp message for `+94 78 860 7143`.

## Rebuild this repository

Generated Ceyteq pages should not be edited directly. Their shared navigation is maintained in `build_site.py`:

```bash
python3 build_site.py
```

`portfolio.html` is standalone and is intentionally not overwritten by that command.
