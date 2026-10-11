#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Standalone, shareable Ceyteq digital business card page."""
from html import escape
from urllib.parse import quote


def T(en: str, si: str, fr: str) -> str:
    """Three language spans, matching the main site's EN / SI / FR pattern."""
    return (f'<span class="lang-en">{en}</span>'
            f'<span class="lang-si">{si}</span>'
            f'<span class="lang-fr">{fr}</span>')


# Small inline marks keep the social buttons self-contained and reliable on
# static hosting; the link labels remain visible even if an SVG cannot render.
SOCIAL_ICONS = {
    'facebook': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#1877F2"/><path fill="#fff" d="M13.8 20v-7h2.35l.35-2.74H13.8V8.52c0-.79.22-1.33 1.38-1.33h1.45V4.74c-.25-.04-1.1-.11-2.1-.11-2.08 0-3.5 1.27-3.5 3.62v2.01H8.68V13h2.35v7h2.77z"/></svg>',
    'instagram': '<svg viewBox="0 0 24 24"><defs><linearGradient id="ig-gradient" x1="0" y1="1" x2="1" y2="0"><stop stop-color="#FFB13D"/><stop offset=".48" stop-color="#E1306C"/><stop offset="1" stop-color="#833AB4"/></linearGradient></defs><rect x="2" y="2" width="20" height="20" rx="6" fill="url(#ig-gradient)"/><rect x="6.3" y="6.3" width="11.4" height="11.4" rx="3.5" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="12" cy="12" r="2.7" fill="none" stroke="#fff" stroke-width="1.8"/><circle cx="16.2" cy="7.9" r="1.15" fill="#fff"/></svg>',
    'linkedin': '<svg viewBox="0 0 24 24"><rect width="24" height="24" rx="5" fill="#0A66C2"/><circle cx="6.9" cy="7" r="1.35" fill="#fff"/><path fill="#fff" d="M5.7 9.2h2.4v9.1H5.7zM10 9.2h2.3v1.24c.52-.9 1.43-1.48 2.78-1.48 2.18 0 3.34 1.44 3.34 4.03v5.31H16v-4.84c0-1.38-.5-2.07-1.58-2.07-1.23 0-2.02.89-2.02 2.4v4.51H10z"/></svg>',
    'tiktok': '<svg viewBox="0 0 24 24"><path d="M15.4 3.1c.42 2.05 1.58 3.28 3.55 3.47v3.1a7.2 7.2 0 0 1-3.54-1.04v6.13c0 3.45-2.32 5.63-5.68 5.63a5.36 5.36 0 0 1 0-10.72c.35 0 .7.04 1.03.1v3.2a2.4 2.4 0 1 0 1.48 2.22V3.1z" fill="#25F4EE" transform="translate(-.55 .3)"/><path d="M15.4 3.1c.42 2.05 1.58 3.28 3.55 3.47v3.1a7.2 7.2 0 0 1-3.54-1.04v6.13c0 3.45-2.32 5.63-5.68 5.63a5.36 5.36 0 0 1 0-10.72c.35 0 .7.04 1.03.1v3.2a2.4 2.4 0 1 0 1.48 2.22V3.1z" fill="#FE2C55" transform="translate(.45 -.25)"/><path d="M15.4 3.1c.42 2.05 1.58 3.28 3.55 3.47v3.1a7.2 7.2 0 0 1-3.54-1.04v6.13c0 3.45-2.32 5.63-5.68 5.63a5.36 5.36 0 0 1 0-10.72c.35 0 .7.04 1.03.1v3.2a2.4 2.4 0 1 0 1.48 2.22V3.1z" fill="#fff"/></svg>',
    'youtube': '<svg viewBox="0 0 24 24"><rect x="1.5" y="4.4" width="21" height="15.2" rx="4.5" fill="#FF0033"/><path d="M10 8.4v7.2l6-3.6z" fill="#fff"/></svg>',
    'pinterest': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="12" fill="#E60023"/><text x="12" y="18" text-anchor="middle" font-family="Georgia,serif" font-size="17" font-weight="700" fill="#fff">P</text></svg>',
    'x': '<svg viewBox="0 0 24 24"><path fill="#fff" d="M18.9 2H22l-6.78 7.75L23.2 22h-6.26l-4.9-7.65L5.35 22H2.2l7.25-8.3L1.8 2h6.42l4.43 7.02L18.9 2zm-1.1 18h1.74L7.26 3.88H5.4L17.8 20z"/></svg>',
    'bilibili': '<svg viewBox="0 0 24 24"><path fill="#00A1D6" d="M8.2 3.1 10 5.3h4l1.8-2.2 1.55 1.25-1 1.2h1.4A3.25 3.25 0 0 1 21 8.8v8.05a3.25 3.25 0 0 1-3.25 3.25H6.25A3.25 3.25 0 0 1 3 16.85V8.8a3.25 3.25 0 0 1 3.25-3.25h1.4l-1-1.2z"/><path d="M8 10.2v4.5m8-4.5v4.5" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/><path d="M7.1 17h9.8" stroke="#fff" stroke-width="1.4" stroke-linecap="round"/></svg>',
    'contra': '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="11" fill="#FF5A35"/><path fill="#fff" d="M14.2 7.3c-1.23 0-2.16.5-2.78 1.4v-1.1H7.7v9.1h3.83v-3.25c0-1.63.7-2.4 2.1-2.4h2.35V7.3z"/><path fill="#fff" d="M16.2 7.3h1.1v3.75h-1.1z"/></svg>',
    'fiverr': '<svg viewBox="0 0 24 24"><text x="12" y="17" text-anchor="middle" font-family="Arial,sans-serif" font-size="15" font-weight="800" letter-spacing="-1.3" fill="#1DBF73">fi</text><circle cx="18.7" cy="15.6" r="1.05" fill="#1DBF73"/></svg>',
}

SOCIAL_PROFILES = (
    ('Facebook', 'https://www.facebook.com/share/1KM2kZvaCC/', 'facebook'),
    ('Instagram', 'https://www.instagram.com/ceyteq/', 'instagram'),
    ('LinkedIn', 'https://www.linkedin.com/in/ceylon-technology', 'linkedin'),
    ('TikTok', 'https://www.tiktok.com/@ceyteq?lang=en-GB', 'tiktok'),
    ('YouTube', 'https://youtube.com/@ceylontechnology-ceyteq?si=a4L-B_OZjvhjO7sw', 'youtube'),
    ('Pinterest', 'https://www.pinterest.com/infoceyteq/', 'pinterest'),
    ('X / Twitter', 'https://x.com/CeylonTech22598', 'x'),
    ('BiliBili', 'https://space.bilibili.com/3745026628651356', 'bilibili'),
    ('Contra', 'https://contra.com/ceylon_technology_ao16fx0l/work?r=ceylon_technology_ao16fx0l', 'contra'),
    ('Fiverr', 'https://pro.fiverr.com/s/emmbpjk', 'fiverr'),
)


def social_links_html(link_class: str = 'social-link') -> str:
    """Render the supplied social profiles with local inline platform marks."""
    css_class = escape(link_class, quote=True)
    return ''.join(
        f'<a class="{css_class}" href="{escape(url, quote=True)}" target="_blank" '
        f'rel="noopener noreferrer" aria-label="Open Ceyteq on {escape(name, quote=True)}">'
        f'<span class="social-icon" aria-hidden="true">{SOCIAL_ICONS[icon]}</span>'
        f'<span class="social-name">{escape(name)}</span><b aria-hidden="true">↗</b></a>'
        for name, url, icon in SOCIAL_PROFILES
    )


def render(site_url: str, meta: str, logo: str = 'assets/logo-transparent.png') -> str:
    site_url = site_url.rstrip('/')
    website = site_url + '/'
    card_url = site_url + '/business-card.html'
    hello = 'https://wa.me/94788607143?text=' + quote(
        'Hello Ceyteq! I viewed your digital business card and would like to discuss a project.'
    )
    share_message = ('Meet Ceyteq — Ceylon Technology. Empowering Digital Evolution. '
                     'Explore our digital business card: ' + card_url)
    whatsapp_share = 'https://wa.me/?text=' + quote(share_message)

    services = [
        ('🌐', 'Web & E-commerce', 'වෙබ් සහ E-commerce', 'Web & e-commerce',
         'Mobile-first websites, online stores and SEO to help customers find you.',
         'Mobile-first websites, online stores සහ SEO මඟින් පාරිභෝගිකයන්ට ඔබව සොයාගැනීමට උදව් කරමු.',
         'Sites adaptés au mobile, boutiques en ligne et référencement SEO.'),
        ('📈', 'Digital Marketing & Branding', 'ඩිජිටල් අලෙවිකරණය සහ සන්නාමකරණය', 'Marketing digital & marque',
         'Social media management and brand building across the platforms your customers use.',
         'ඔබේ පාරිභෝගිකයන් භාවිතා කරන සමාජ මාධ්‍යවල කළමනාකරණය සහ සන්නාම ගොඩනැගීම.',
         'Gestion des réseaux sociaux et développement de votre marque.'),
        ('🎯', 'Advertising Campaigns', 'ප්‍රචාරණ ව්‍යාපාර', 'Campagnes publicitaires',
         'Google Ads, social media advertising and YouTube promotions.',
         'Google Ads, සමාජ මාධ්‍ය දැන්වීම් සහ YouTube ප්‍රවර්ධන.',
         'Google Ads, publicité sur les réseaux sociaux et promotions YouTube.'),
        ('🖨️', 'Premium Printing & Signage', 'ගුණාත්මක මුද්‍රණ සහ සංඥා පුවරු', 'Impression & signalétique',
         'Offset and packaging print, custom paper bags and digital LED boards.',
         'Offset සහ packaging මුද්‍රණය, custom paper bags සහ digital LED boards.',
         'Impression offset et emballages, sacs personnalisés et panneaux LED.'),
        ('🎨', 'Creative Media', 'නිර්මාණාත්මක මාධ්‍ය', 'Médias créatifs',
         'Graphic design, photography, videography and professional video editing.',
         'Graphic design, photography, videography සහ වෘත්තීය video editing.',
         'Design graphique, photographie, vidéo et montage professionnel.'),
        ('🤖', 'AI & ERP Solutions', 'AI සහ ERP විසඳුම්', 'Solutions IA & ERP',
         'AI customer care, CRM automation and smart business management platforms.',
         'AI customer care, CRM automation සහ බුද්ධිමත් ව්‍යාපාර කළමනාකරණ පද්ධති.',
         'Service client IA, automatisation CRM et gestion intelligente.'),
    ]
    service_cards = ''.join(
        f'''<article class="service-card">
  <div class="service-icon" aria-hidden="true">{icon}</div>
  <h3>{T(en, si, fr)}</h3>
  <p>{T(desc_en, desc_si, desc_fr)}</p>
</article>'''
        for icon, en, si, fr, desc_en, desc_si, desc_fr in services
    )

    social_links = social_links_html()

    return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="color-scheme" content="light">
<title>CEYTEQ — Ceylon Technology | Digital Business Card</title>
{meta}
<link rel="preload" href="assets/Inter-Regular.ttf" as="font" type="font/ttf" crossorigin>
<link rel="preload" href="assets/Inter-Bold.ttf" as="font" type="font/ttf" crossorigin>
<style>
@font-face{{font-family:CardInter;src:url('assets/Inter-Regular.ttf') format('truetype');font-weight:400;font-display:swap}}
@font-face{{font-family:CardInter;src:url('assets/Inter-SemiBold.ttf') format('truetype');font-weight:600;font-display:swap}}
@font-face{{font-family:CardInter;src:url('assets/Inter-Bold.ttf') format('truetype');font-weight:700 900;font-display:swap}}
@font-face{{font-family:CardSinhala;src:url('assets/Sinhala-Regular.ttf') format('truetype');font-weight:400;font-display:swap}}
@font-face{{font-family:CardSinhala;src:url('assets/Sinhala-Bold.ttf') format('truetype');font-weight:700 900;font-display:swap}}
:root{{--ink:#0b1e2b;--navy:#081b28;--cyan:#21bed7;--blue:#1497b8;--muted:#62727d;--paper:#f2f6f7;--line:#dce5e8;--green:#19b65a}}
*{{box-sizing:border-box}}
html{{scroll-behavior:smooth}}
body{{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.55 CardInter,Inter,'Segoe UI',Arial,sans-serif}}
body[data-langmode="si"] .lang-en,body[data-langmode="si"] .lang-fr,body[data-langmode="en"] .lang-si,body[data-langmode="en"] .lang-fr,body[data-langmode="fr"] .lang-en,body[data-langmode="fr"] .lang-si{{display:none}}
.lang-si{{font-family:CardSinhala,CardInter,'Noto Sans Sinhala','Iskoola Pota',sans-serif;letter-spacing:0}}
a{{color:inherit}}
button{{font:inherit}}
.shell{{width:min(1160px,100% - 40px);margin:0 auto}}
.topbar{{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:22px 0 20px}}
.brand-logo{{display:block;width:min(210px,42vw);height:auto;mix-blend-mode:multiply}}
.top-actions{{display:flex;align-items:center;justify-content:flex-end;gap:14px;flex-wrap:wrap}}
.languages{{display:flex;gap:4px;padding:4px;border:1px solid var(--line);background:#fff;border-radius:50px}}
.languages button{{border:0;background:transparent;color:#52626d;padding:7px 10px;border-radius:50px;font-size:11px;font-weight:700;cursor:pointer}}
.languages button.active,.languages button:hover{{background:var(--navy);color:#fff}}
.main-link{{color:#385360;font-size:13px;font-weight:700;text-decoration:none;white-space:nowrap}}
.main-link:hover{{color:var(--blue)}}
.hero{{isolation:isolate;position:relative;overflow:hidden;display:block;text-align:center;padding:clamp(48px,8vw,88px) clamp(24px,7vw,78px);border:1px solid rgba(33,190,215,.25);border-radius:30px;background:radial-gradient(circle at 90% 10%,rgba(33,190,215,.23),transparent 32%),radial-gradient(circle at 6% 100%,rgba(33,190,215,.12),transparent 29%),linear-gradient(125deg,#071a27 0%,#0b2837 57%,#09202e 100%);box-shadow:0 26px 66px rgba(7,26,39,.16);color:#fff}}
.hero:after{{content:"";position:absolute;z-index:-1;width:360px;height:360px;border:1px solid rgba(84,219,238,.12);border-radius:50%;right:-210px;bottom:-230px;box-shadow:0 0 0 34px rgba(84,219,238,.035),0 0 0 68px rgba(84,219,238,.025)}}
.hero-copy{{max-width:850px;margin:0 auto}}
.eyebrow{{display:inline-flex;align-items:center;justify-content:center;gap:9px;color:#85dfeb;text-transform:uppercase;letter-spacing:2px;font-size:11px;font-weight:700}}
.eyebrow:before{{content:"";width:22px;height:2px;background:var(--cyan);border-radius:10px}}
.hero h1{{max-width:780px;margin:18px auto 16px;color:#fff;font-size:clamp(39px,5.3vw,65px);line-height:1.04;letter-spacing:-.055em;font-weight:700}}
.hero h1 em{{display:block;color:#61d8e9;font-style:normal}}
.hero-copy>p{{max-width:690px;color:#d0dce1;font-size:clamp(15px,1.5vw,17px);margin:0 auto}}
.hero-actions{{display:flex;justify-content:center;gap:11px;flex-wrap:wrap;margin-top:26px}}
.hero-services{{position:relative;z-index:1;display:flex;justify-content:center;gap:9px;flex-wrap:wrap;margin:31px auto 0}}
.hero-services>span{{display:inline-flex;align-items:center;gap:7px;padding:8px 11px;border:1px solid rgba(153,222,231,.22);border-radius:50px;background:rgba(255,255,255,.045);color:#d7e8eb;font-size:10px;font-weight:600}}
.hero-services i{{color:#65d8e7;font-size:8px;font-style:normal;font-weight:800}}
.btn{{min-height:47px;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:12px 18px;border:1px solid transparent;border-radius:12px;text-decoration:none;font-size:13px;font-weight:700;transition:transform .18s,background .18s,border-color .18s,box-shadow .18s;cursor:pointer}}
.btn:hover{{transform:translateY(-2px)}}
.btn-wa{{background:var(--green);color:#052817;box-shadow:0 9px 22px rgba(25,182,90,.22)}}
.btn-wa:hover{{background:#31cf70}}
.btn-light{{border-color:rgba(255,255,255,.3);color:#fff;background:rgba(255,255,255,.07)}}
.btn-light:hover{{background:rgba(255,255,255,.14)}}
.btn-dark{{background:var(--navy);color:#fff}}
.btn-dark:hover{{background:#12364a}}
.btn-outline{{border-color:#b8cbd2;color:var(--ink);background:#fff}}
.btn-outline:hover{{border-color:var(--cyan)}}
.btn svg{{width:17px;height:17px;flex:0 0 auto}}
.contact-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:22px 0 0}}
.contact-tile{{min-width:0;display:flex;align-items:center;gap:12px;padding:17px 16px;border:1px solid var(--line);border-radius:15px;background:#fff;text-decoration:none;box-shadow:0 6px 16px rgba(9,32,46,.035);transition:transform .18s,border-color .18s,box-shadow .18s}}
.contact-tile:hover{{transform:translateY(-3px);border-color:#9ddde5;box-shadow:0 11px 24px rgba(9,32,46,.08)}}
.contact-icon{{display:grid;place-items:center;flex:0 0 39px;width:39px;height:39px;border-radius:12px;background:#e8f6f8;color:#087c98;font-size:17px}}
.contact-tile small{{display:block;color:#70828c;text-transform:uppercase;letter-spacing:1px;font-size:8px;font-weight:700}}
.contact-tile strong{{display:block;overflow-wrap:anywhere;color:var(--ink);font-size:12px;font-weight:700;margin-top:3px}}
.section{{padding:76px 0 0}}
.section-head{{max-width:690px}}
.section-kicker{{margin:0 0 8px;color:#108ba5;text-transform:uppercase;letter-spacing:2px;font-size:10px;font-weight:700}}
.section h2{{margin:0;color:var(--ink);font-size:clamp(28px,4vw,43px);line-height:1.13;letter-spacing:-1.7px}}
.section-head>p:last-child{{margin:11px 0 0;color:var(--muted);font-size:15px}}
.service-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:13px;margin-top:26px}}
.service-card{{min-height:178px;padding:22px 21px;border:1px solid var(--line);border-radius:17px;background:rgba(255,255,255,.84);box-shadow:0 7px 22px rgba(9,32,46,.035);transition:transform .18s,border-color .18s,box-shadow .18s}}
.service-card:hover{{transform:translateY(-4px);border-color:#a8dce3;box-shadow:0 15px 29px rgba(9,32,46,.08)}}
.service-icon{{display:grid;place-items:center;width:40px;height:40px;border-radius:13px;background:#e8f6f8;font-size:20px}}
.service-card h3{{margin:15px 0 7px;color:var(--ink);font-size:15px;line-height:1.3;letter-spacing:-.3px}}
.service-card p{{margin:0;color:var(--muted);font-size:12px;line-height:1.65}}
.connect-panel{{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(270px,.75fr);gap:28px;align-items:center;margin-top:76px;padding:clamp(26px,5vw,50px);border-radius:25px;background:#fff;border:1px solid var(--line);box-shadow:0 16px 44px rgba(9,32,46,.065)}}
.connect-copy h2{{max-width:620px;margin:9px 0 11px;color:var(--ink);font-size:clamp(27px,4vw,40px);line-height:1.12;letter-spacing:-1.6px}}
.connect-copy>p{{max-width:560px;margin:0;color:var(--muted);font-size:14px}}
.connect-actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}}
.qr-box{{display:flex;flex-direction:column;align-items:center;text-align:center;padding:21px 17px 18px;border:1px solid #dfe8eb;border-radius:19px;background:linear-gradient(160deg,#f8fbfc,#f0f7f8)}}
.qr-img{{display:grid;place-items:center;width:164px;height:164px;padding:10px;border-radius:14px;background:#fff;border:1px solid #e6edef;box-shadow:0 8px 20px rgba(7,26,39,.08)}}
.qr-img img{{display:block;width:100%;height:100%;object-fit:contain}}
.qr-box h3{{margin:14px 0 4px;color:var(--ink);font-size:15px}}
.qr-box p{{max-width:230px;margin:0;color:var(--muted);font-size:11px}}
.card-url{{width:100%;max-width:290px;margin-top:11px;padding:8px 10px;border:1px solid #dce8eb;border-radius:10px;background:#fff;text-align:left}}
.card-url small{{display:block;color:#778994;font-size:8px;font-weight:700;letter-spacing:.8px;text-transform:uppercase}}
.card-url a{{display:block;margin-top:3px;color:#1d5260;text-decoration:none;font-size:9px;font-weight:700;overflow-wrap:anywhere}}
.card-url a:hover{{color:#087c98}}
.qr-actions{{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:13px}}
.qr-actions a{{padding:8px 11px;border-radius:9px;border:1px solid #d2e0e4;background:#fff;color:#1d5260;text-decoration:none;font-size:10px;font-weight:700}}
.qr-actions a:hover{{border-color:var(--cyan);color:#087c98}}
.hero-social{{position:relative;z-index:1;margin:38px auto 0;padding-top:23px;border-top:1px solid rgba(179,221,229,.17)}}
.hero-social-head{{margin:0 0 14px;color:#a7c4cc;text-align:center;text-transform:uppercase;letter-spacing:1.8px;font-size:9px;font-weight:700}}
.social-grid{{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:9px}}
.social-link{{min-width:0;min-height:52px;display:flex;align-items:center;gap:9px;padding:9px 11px;border:1px solid rgba(178,218,227,.17);border-radius:13px;background:rgba(255,255,255,.055);color:#f1f8fa;text-decoration:none;font-size:10px;font-weight:700;text-align:left;transition:background .18s,border-color .18s,transform .18s}}
.social-link:hover{{transform:translateY(-2px);border-color:rgba(77,215,232,.72);background:rgba(255,255,255,.12)}}
.social-icon{{flex:0 0 25px;width:25px;height:25px;display:grid;place-items:center}}
.social-icon svg{{display:block;width:24px;height:24px}}
.social-name{{min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.social-link>b{{margin-left:auto;color:#83a3ae;font-size:10px}}
.footer{{margin:70px 0 22px}}
.founder-panel{{position:relative;overflow:hidden;display:flex;align-items:center;justify-content:space-between;gap:26px;flex-wrap:wrap;padding:clamp(25px,4vw,40px);border-radius:22px;background:linear-gradient(115deg,#0b1e2b,#102e3c);color:#fff;box-shadow:0 16px 40px rgba(7,26,39,.12)}}
.founder-panel:after{{content:"";position:absolute;width:230px;height:230px;right:-120px;top:-155px;border:1px solid rgba(73,216,233,.3);border-radius:50%;box-shadow:0 0 0 23px rgba(73,216,233,.04),0 0 0 46px rgba(73,216,233,.03)}}
.founder-main{{position:relative;z-index:1}}
.founder-label{{display:flex;align-items:center;gap:8px;color:#92dce5;text-transform:uppercase;letter-spacing:2px;font-size:9px;font-weight:700}}
.founder-label:before{{content:"";width:7px;height:7px;border-radius:50%;background:#54d68a;box-shadow:0 0 0 4px rgba(84,214,138,.12)}}
.founder-main h2{{margin:9px 0 4px;color:#fff;font-size:clamp(27px,4vw,38px);letter-spacing:-1px}}
.founder-main p{{margin:0;color:#c6d7dd;font-size:13px}}
.credentials{{position:relative;z-index:1;display:flex;flex-wrap:wrap;gap:8px}}
.credentials span{{padding:9px 12px;border:1px solid rgba(132,218,229,.25);border-radius:50px;background:rgba(255,255,255,.05);color:#d8edf0;font-size:10px;font-weight:700}}
.legal{{padding:17px 4px 0;color:#7a8b94;text-align:center;font-size:10px}}
.toast{{position:fixed;z-index:10;left:50%;bottom:24px;max-width:calc(100% - 32px);padding:11px 16px;transform:translate(-50%,18px);opacity:0;pointer-events:none;border:1px solid rgba(255,255,255,.14);border-radius:12px;background:#071a27;color:#fff;box-shadow:0 10px 30px rgba(0,0,0,.22);font-size:12px;font-weight:600;transition:opacity .2s,transform .2s}}
.toast.show{{opacity:1;transform:translate(-50%,0)}}
:focus-visible{{outline:3px solid #2ebcd4;outline-offset:3px}}
@media(max-width:850px){{.hero h1{{max-width:670px}}.contact-grid{{grid-template-columns:repeat(2,1fr)}}.service-grid{{grid-template-columns:repeat(2,1fr)}}.social-grid{{grid-template-columns:repeat(3,minmax(0,1fr))}}.connect-panel{{grid-template-columns:1fr minmax(235px,.6fr)}}}}
@media(max-width:620px){{.shell{{width:min(100% - 28px,1160px)}}.topbar{{padding:15px 0;gap:10px}}.brand-logo{{width:150px}}.top-actions{{gap:8px}}.main-link{{display:none}}.languages{{gap:1px}}.languages button{{padding:7px 8px;font-size:10px}}.hero{{padding:43px 18px;border-radius:22px}}.hero h1{{font-size:clamp(36px,10.4vw,48px)}}.hero-actions{{gap:8px}}.hero-services{{gap:6px;margin-top:22px}}.hero-services>span{{gap:5px;padding:7px 9px;font-size:9px}}.btn{{min-height:44px;padding:11px 13px;font-size:12px}}.contact-grid{{gap:8px;margin-top:14px}}.contact-tile{{gap:8px;padding:12px 10px;border-radius:12px}}.contact-icon{{flex-basis:32px;width:32px;height:32px;font-size:14px;border-radius:10px}}.contact-tile small{{font-size:7px;letter-spacing:.6px}}.contact-tile strong{{font-size:10px}}.section{{padding-top:57px}}.service-grid{{gap:9px;margin-top:20px}}.service-card{{min-height:0;padding:16px 14px;border-radius:14px}}.service-icon{{width:34px;height:34px;font-size:17px;border-radius:10px}}.service-card h3{{font-size:12px;margin-top:12px}}.service-card p{{font-size:10px;line-height:1.55}}.connect-panel{{grid-template-columns:1fr;margin-top:57px;padding:22px 17px;gap:22px;border-radius:19px}}.connect-copy h2{{font-size:29px}}.qr-box{{padding:18px 12px}}.qr-img{{width:148px;height:148px}}.hero-social{{margin-top:27px;padding-top:18px}}.hero-social-head{{font-size:8px}}.social-grid{{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}}.social-link{{font-size:9px;min-height:46px;padding:8px 9px;gap:7px}}.social-icon{{flex-basis:23px;width:23px;height:23px}}.social-icon svg{{width:22px;height:22px}}.footer{{margin-top:53px}}.founder-panel{{align-items:flex-start;padding:24px 20px;border-radius:18px;gap:18px}}.credentials{{gap:6px}}.credentials span{{font-size:9px;padding:8px 9px}}}}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{scroll-behavior:auto!important;transition:none!important;animation:none!important}}}}
</style></head>
<body data-langmode="en">
<div class="shell">
<header class="topbar">
<a href="{website}" aria-label="Ceyteq home"><img class="brand-logo" src="{logo}" alt="Ceyteq — Ceylon Technology"></a>
<div class="top-actions">
<div class="languages" role="group" aria-label="Choose language">
<button type="button" data-card-lang="si" onclick="setCardLang('si')">සිංහල</button>
<button type="button" class="active" data-card-lang="en" onclick="setCardLang('en')">EN</button>
<button type="button" data-card-lang="fr" onclick="setCardLang('fr')">FR</button>
</div>
<a class="main-link" href="{website}"><span class="lang-en">Visit main website ↗</span><span class="lang-si">ප්‍රධාන වෙබ් අඩවිය ↗</span><span class="lang-fr">Site principal ↗</span></a>
</div>
</header>
<main>
<section class="hero" aria-labelledby="page-title">
<div class="hero-copy">
<div class="eyebrow"><span class="lang-en">Digital business card</span><span class="lang-si">ඩිජිටල් ව්‍යාපාරික කාඩ්පත</span><span class="lang-fr">Carte de visite numérique</span></div>
<h1 id="page-title"><span class="lang-en">Empowering <em>Digital Evolution.</em></span><span class="lang-si">ඩිජිටල් පරිණාමයට <em>අපෙන් සවිබලයක්.</em></span><span class="lang-fr">Accélérer <em>l'évolution numérique.</em></span></h1>
<p><span class="lang-en">Ceyteq — Ceylon Technology. Your all-in-one partner for digital growth, creative media and premium print.</span><span class="lang-si">Ceyteq — Ceylon Technology. ඩිජිටල් වර්ධනය, නිර්මාණාත්මක මාධ්‍ය සහ ගුණාත්මක මුද්‍රණ සඳහා ඔබේ එකම සහකරු.</span><span class="lang-fr">Ceyteq — Ceylon Technology. Votre partenaire pour le numérique, la création et l'impression de qualité.</span></p>
<div class="hero-actions">
<a class="btn btn-wa" href="{hello}" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">◉</span><span class="lang-en">Chat on WhatsApp</span><span class="lang-si">WhatsApp හරහා කතා කරන්න</span><span class="lang-fr">Discuter sur WhatsApp</span></a>
<a class="btn btn-light" href="ceyteq-contact.vcf" download="S-Nilan-Ceyteq.vcf"><span aria-hidden="true">↓</span><span class="lang-en">Save contact</span><span class="lang-si">සම්බන්ධතාව සුරකින්න</span><span class="lang-fr">Enregistrer le contact</span></a>
</div>
<div class="hero-services" aria-label="Ceyteq services">
<span><i>01</i><span class="lang-en">Web &amp; E-commerce</span><span class="lang-si">Web සහ E-commerce</span><span class="lang-fr">Web &amp; e-commerce</span></span>
<span><i>02</i><span class="lang-en">Digital Marketing</span><span class="lang-si">ඩිජිටල් අලෙවිකරණය</span><span class="lang-fr">Marketing digital</span></span>
<span><i>03</i><span class="lang-en">Advertising</span><span class="lang-si">ප්‍රචාරණය</span><span class="lang-fr">Publicité</span></span>
<span><i>04</i><span class="lang-en">Print &amp; Signage</span><span class="lang-si">මුද්‍රණ සහ සංඥා පුවරු</span><span class="lang-fr">Impression &amp; signalétique</span></span>
<span><i>05</i><span class="lang-en">Creative Media</span><span class="lang-si">නිර්මාණාත්මක මාධ්‍ය</span><span class="lang-fr">Médias créatifs</span></span>
<span><i>06</i><span class="lang-en">AI &amp; ERP</span><span class="lang-si">AI සහ ERP</span><span class="lang-fr">IA &amp; ERP</span></span>
</div>
<div class="hero-social" aria-labelledby="social-title">
<p class="hero-social-head" id="social-title"><span class="lang-en">Connect with Ceyteq</span><span class="lang-si">Ceyteq සමඟ සම්බන්ධ වන්න</span><span class="lang-fr">Retrouvez Ceyteq</span></p>
<div class="social-grid">{social_links}</div>
</div>
</div>
</section>
<section class="contact-grid" aria-label="Contact Ceyteq">
<a class="contact-tile" href="https://wa.me/94788607143" target="_blank" rel="noopener noreferrer"><span class="contact-icon" aria-hidden="true">◉</span><span><small><span class="lang-en">Hotline / WhatsApp</span><span class="lang-si">හොට්ලයින් / WhatsApp</span><span class="lang-fr">Ligne directe / WhatsApp</span></small><strong>+94 78 860 7143</strong></span></a>
<a class="contact-tile" href="tel:+94768607143"><span class="contact-icon" aria-hidden="true">⌕</span><span><small><span class="lang-en">Mobile</span><span class="lang-si">ජංගම දුරකථන</span><span class="lang-fr">Mobile</span></small><strong>+94 76 860 7143</strong></span></a>
<a class="contact-tile" href="mailto:info.ceyteq@gmail.com"><span class="contact-icon" aria-hidden="true">✉</span><span><small>Email</small><strong>info.ceyteq@gmail.com</strong></span></a>
<a class="contact-tile" href="{website}" target="_blank" rel="noopener noreferrer"><span class="contact-icon" aria-hidden="true">↗</span><span><small><span class="lang-en">Website</span><span class="lang-si">වෙබ් අඩවිය</span><span class="lang-fr">Site web</span></small><strong>ceyteq.linkpc.net</strong></span></a>
</section>
<section class="section" id="services">
<div class="section-head">
<p class="section-kicker"><span class="lang-en">What we do</span><span class="lang-si">අපගේ සේවා</span><span class="lang-fr">Nos services</span></p>
<h2><span class="lang-en">Everything your brand needs to grow.</span><span class="lang-si">ඔබේ සන්නාමය වර්ධනයට අවශ්‍ය සියල්ල.</span><span class="lang-fr">Tout pour développer votre marque.</span></h2>
<p><span class="lang-en">A complete suite of technology, marketing, advertising, creative and print solutions under one professional platform.</span><span class="lang-si">තාක්ෂණය, අලෙවිකරණය, ප්‍රචාරණය, නිර්මාණ සහ මුද්‍රණ විසඳුම් — එකම වෘත්තීය වේදිකාවකින්.</span><span class="lang-fr">Technologie, marketing, publicité, création et impression réunis sur une seule plateforme professionnelle.</span></p>
</div>
<div class="service-grid">{service_cards}</div>
</section>
<section class="connect-panel" id="share">
<div class="connect-copy">
<p class="section-kicker"><span class="lang-en">Let's connect</span><span class="lang-si">අප හා සම්බන්ධ වන්න</span><span class="lang-fr">Restons en contact</span></p>
<h2><span class="lang-en">Let's build a strong brand presence together.</span><span class="lang-si">එක්ව ඔබේ සන්නාමයට ශක්තිමත් පෙනුමක් ගොඩනගමු.</span><span class="lang-fr">Construisons ensemble une marque forte.</span></h2>
<p><span class="lang-en">Tell us about your next project. Chat with the team, save our details, or share this card with someone who needs a digital boost.</span><span class="lang-si">ඔබගේ මීළඟ ව්‍යාපෘතිය ගැන අපට කියන්න. කණ්ඩායම සමඟ කතා කරන්න, විස්තර සුරකින්න හෝ මේ කාඩ්පත බෙදාගන්න.</span><span class="lang-fr">Parlez-nous de votre prochain projet, enregistrez nos coordonnées ou partagez cette carte.</span></p>
<div class="connect-actions">
<a class="btn btn-wa" href="{whatsapp_share}" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">◉</span><span class="lang-en">Send link on WhatsApp</span><span class="lang-si">Link එක WhatsApp හරහා යවන්න</span><span class="lang-fr">Envoyer le lien sur WhatsApp</span></a>
<button class="btn btn-dark" type="button" onclick="shareCard()"><span aria-hidden="true">↗</span><span class="lang-en">More sharing options</span><span class="lang-si">වෙනත් ආකාරවලින් බෙදාගන්න</span><span class="lang-fr">Autres options de partage</span></button>
<button class="btn btn-outline" type="button" onclick="copyCardLink()"><span aria-hidden="true">▣</span><span class="lang-en">Copy link</span><span class="lang-si">Link එක පිටපත් කරන්න</span><span class="lang-fr">Copier le lien</span></button>
</div>
</div>
<div class="qr-box">
<div class="qr-img"><img src="assets/ceyteq-business-card-qr.png" alt="QR code — scan to open Ceyteq's digital business card" loading="lazy"></div>
<h3><span class="lang-en">Scan to open this card</span><span class="lang-si">කාඩ්පත විවෘත කිරීමට scan කරන්න</span><span class="lang-fr">Scannez pour ouvrir la carte</span></h3>
<p><span class="lang-en">Download the QR to share this page or show it from your phone.</span><span class="lang-si">මෙම පිටුව බෙදාගැනීමට හෝ දුරකථනයෙන් පෙන්වීමට QR එක download කරන්න.</span><span class="lang-fr">Téléchargez le QR pour partager cette page ou l'afficher sur votre téléphone.</span></p>
<div class="card-url"><small><span class="lang-en">Your shareable link</span><span class="lang-si">ඔබට බෙදාගත හැකි Link එක</span><span class="lang-fr">Votre lien à partager</span></small><a href="{card_url}">{card_url}</a></div>
<div class="qr-actions"><a href="assets/ceyteq-business-card-qr.png" download="Ceyteq-business-card-QR.png"><span class="lang-en">Download PNG</span><span class="lang-si">PNG download</span><span class="lang-fr">Télécharger PNG</span></a><a href="assets/ceyteq-business-card-qr.svg" download="Ceyteq-business-card-QR.svg"><span class="lang-en">Download SVG</span><span class="lang-si">SVG download</span><span class="lang-fr">Télécharger SVG</span></a></div>
</div>
</section>
</main>
<footer class="footer">
<section class="founder-panel" aria-labelledby="founder-name">
<div class="founder-main"><div class="founder-label"><span class="lang-en">Founder</span><span class="lang-si">නිර්මාතෘ</span><span class="lang-fr">Fondateur</span></div>
<h2 id="founder-name">S. Nilan</h2>
<p>Digital Business Marketing &amp; Management (BSc)</p></div>
<div class="credentials"><span>Meta &amp; Google Verified Specialist</span></div>
</section>
<div class="legal">© 2026 <strong>Ceyteq — Ceylon Technology</strong> · Empowering Digital Evolution · Sri Lanka</div>
</footer>
</div>
<div class="toast" id="toast" role="status" aria-live="polite"></div>
<script>
function setCardLang(mode){{
 if(['en','si','fr'].indexOf(mode)<0)mode='en';
 document.documentElement.lang=mode;document.body.setAttribute('data-langmode',mode);
 document.querySelectorAll('[data-card-lang]').forEach(function(btn){{btn.classList.toggle('active',btn.getAttribute('data-card-lang')===mode)}});
 try{{localStorage.setItem('ceyteq_card_lang',mode)}}catch(e){{}}
}}
(function(){{var mode='en';try{{mode=localStorage.getItem('ceyteq_card_lang')||'en'}}catch(e){{}}setCardLang(mode)}})();
function cardLink(){{var link=document.querySelector('link[rel="canonical"]');return link?link.href:window.location.href}}
var toastTimer;
function showToast(message){{var el=document.getElementById('toast');el.textContent=message;el.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(function(){{el.classList.remove('show')}},2400)}}
function copyCardLink(){{var url=cardLink();
 if(navigator.clipboard&&window.isSecureContext){{navigator.clipboard.writeText(url).then(function(){{showToast('Business card link copied.')}}).catch(function(){{copyFallback(url)}})}}else copyFallback(url);
}}
function copyFallback(text){{var input=document.createElement('textarea');input.value=text;input.setAttribute('readonly','');input.style.position='fixed';input.style.opacity='0';document.body.appendChild(input);input.select();try{{document.execCommand('copy');showToast('Business card link copied.')}}catch(e){{showToast('Copy this link: '+text)}}document.body.removeChild(input)}}
function shareWhatsApp(){{var message='Meet Ceyteq — Ceylon Technology. Empowering Digital Evolution. Explore our digital business card: '+cardLink();window.open('https://wa.me/?text='+encodeURIComponent(message),'_blank','noopener,noreferrer')}}
function shareCard(){{var url=cardLink();if(navigator.share){{navigator.share({{title:'CEYTEQ — Ceylon Technology',text:'Empowering Digital Evolution. View our digital business card.',url:url}}).catch(function(error){{if(error&&error.name!=='AbortError')shareWhatsApp()}})}}else{{shareWhatsApp()}}}}
</script>
</body></html>'''


def vcard(site_url: str) -> str:
    """vCard contact download for the Ceyteq founder, using supplied details."""
    website = site_url.rstrip('/') + '/'
    return ('BEGIN:VCARD\n'
            'VERSION:3.0\n'
            'N:Nilan;S.;;;\n'
            'FN:S. Nilan\n'
            'ORG:Ceyteq - Ceylon Technology\n'
            'TITLE:Founder\n'
            'TEL;TYPE=WORK,VOICE:+94788607143\n'
            'TEL;TYPE=CELL,VOICE:+94768607143\n'
            'EMAIL;TYPE=INTERNET,WORK:info.ceyteq@gmail.com\n'
            f'URL:{website}\n'
            'NOTE:Digital Business Marketing & Management (BSc); Meta and Google Verified Specialist\n'
            'END:VCARD\n')
