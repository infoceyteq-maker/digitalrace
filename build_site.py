#!/usr/bin/env python3
"""Build Ceyteq Digital Race multi-page site: light ash theme, transparent logo, EN/SI/FR."""
import base64, os

# Project root = the folder this script lives in (works on any machine / CI).
ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(ROOT, 'assets')
FLYER_DIR = os.path.join(ROOT, 'flyers')

with open(os.path.join(ASSETS, 'logo-transparent.png'), 'rb') as f:
    LOGO = 'data:image/png;base64,' + base64.b64encode(f.read()).decode()

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#ecf0f0;--card:#fff;--ink:#0c1e21;--mut:#364e52;--mut2:#67787a;--cyan:#27a3c9;
--cyanb:#27a3c9;--navy:#0c1e21;--deep:#18292c;--tint:#d8e5e5;--tint2:#cee0e0;--line:#c9d1d1;
--gold:#0c1e21;--goldb:#27a3c9;--prime:#27a3c9;--primed:#1b7a99}
html{scroll-behavior:smooth}
::selection{background:#27a3c9;color:#fff}
body{font-family:'Mona Sans','Segoe UI',Inter,Roboto,'Noto Sans Sinhala','Iskoola Pota',Arial,sans-serif;
background:var(--bg);color:var(--mut);font-size:16px;line-height:1.5}
a{color:var(--primed)}
.wrap{max-width:1180px;margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:'Mona Sans','Segoe UI',Inter,'Noto Sans Sinhala',sans-serif;color:var(--ink);
letter-spacing:-.03em;line-height:1.12}
.lang-si{letter-spacing:0!important}
/* language visibility (exclusive modes) */
body[data-langmode] .lang-en,body[data-langmode] .lang-si,body[data-langmode] .lang-fr{display:none}
body[data-langmode="en"] .lang-en{display:revert}
body[data-langmode="si"] .lang-si{display:revert}
body[data-langmode="fr"] .lang-fr{display:revert}
body[data-langmode="en"] .price .lang-en,body[data-langmode="si"] .price .lang-si,body[data-langmode="fr"] .price .lang-fr{display:block}
/* nav */
nav{position:sticky;top:0;z-index:50;background:rgba(255,255,255,.92);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;align-items:center;gap:12px;padding:12px 24px;flex-wrap:wrap}
nav img.logo{height:46px}
nav .brand{font-weight:800;letter-spacing:.5px;font-size:19px;color:var(--ink)}
nav .brand small{display:block;font-size:9px;color:var(--primed);letter-spacing:2.5px;font-weight:700}
nav .links{display:flex;gap:2px;flex-wrap:wrap;margin-left:8px}
nav .links a{color:var(--ink);text-decoration:none;font-size:15px;font-weight:600;padding:8px 13px;border-radius:50px;transition:.2s}
nav .links a:hover{color:var(--prime);background:rgba(39,163,201,.1)}
nav .links a.active{background:var(--ink);color:#fff}
.langsw{margin-left:auto;display:flex;gap:6px}
.langsw button{border:1.5px solid var(--prime);background:#fff;color:var(--ink);font-weight:700;font-size:12px;
border-radius:50px;padding:7px 15px;cursor:pointer;transition:.2s;font-family:inherit}
.langsw button.active,.langsw button:hover{background:var(--prime);color:#fff;border-color:var(--prime)}
/* hero panel */
.hero{text-align:center;padding:64px 34px 54px;margin:26px 0 6px;border-radius:24px;color:var(--ink);
background:linear-gradient(270deg,#e4f5fc,#dff1f0,#e6f4fb,#d9efe9,#e4f5fc,#dcefea);background-size:200% 200%;
animation:hmshift 18s ease infinite;border:1px solid rgba(39,163,201,.25);box-shadow:0 20px 50px rgba(12,30,33,.08)}
@keyframes hmshift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
.hero img.main-logo{width:min(380px,82%);filter:drop-shadow(0 10px 26px rgba(12,30,33,.18))}
.pill{display:inline-block;border:1.5px solid var(--prime);color:var(--primed);background:#fff;border-radius:50px;
padding:7px 20px;font-size:12.5px;font-weight:700;letter-spacing:2px;margin:20px 0 12px}
h1{font-size:clamp(44px,7vw,74px);font-weight:700}
h1 .lang-si{display:block;font-size:clamp(24px,4.5vw,38px);color:var(--primed);margin-top:8px;font-weight:600}
h1 .lang-fr{font-size:clamp(20px,4vw,32px);color:var(--primed)}
.alien{background:linear-gradient(135deg,#0c1e21,#14333a 60%,#0c1e21);border:1px solid rgba(39,163,201,.55);
border-radius:20px;padding:28px 26px;margin:24px auto;max-width:860px;box-shadow:0 18px 44px rgba(12,30,33,.25)}
.alien .kick{color:#7fd4ef;font-weight:700;letter-spacing:3px;font-size:12.5px;text-transform:uppercase}
.alien .ah{font-size:clamp(22px,4.6vw,36px);font-weight:700;color:#fff;line-height:1.25;margin:8px 0;letter-spacing:-.02em}
.alien .lang-si{color:#aee3f5}
.alien p{color:#cfe3e8;margin-top:8px;font-size:15.5px}
.tag{font-size:clamp(18px,3vw,24px);color:var(--ink);font-weight:700;margin-top:16px;letter-spacing:-.02em}
.tag2{color:var(--mut);font-size:16px}
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin:26px 0 8px}
.btn{display:inline-block;text-decoration:none;font-weight:600;padding:14px 30px;border-radius:50px;font-size:16px;transition:.2s;border:1.5px solid transparent}
.btn-cyan{background:var(--prime);color:#fff;box-shadow:0 10px 26px rgba(39,163,201,.35)}
.btn-cyan:hover{background:var(--primed);transform:translateY(-2px)}
.btn-navy{background:var(--ink);color:#fff}
.btn-navy:hover{background:var(--deep);transform:translateY(-2px)}
.btn-ghost{border-color:var(--ink);color:var(--ink);background:transparent}
.btn-ghost:hover{background:var(--ink);color:#fff}
.stats{display:flex;gap:14px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.stat{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 24px;min-width:145px;
box-shadow:0 10px 26px rgba(12,30,33,.07)}
.stat b{display:block;font-size:23px;color:var(--ink);font-weight:800;letter-spacing:-.02em}
.stat span{font-size:12.5px;color:var(--mut2)}
section{padding:80px 0;border-top:1px solid var(--line)}
.eyebrow{color:var(--primed);font-weight:700;letter-spacing:2.5px;font-size:13px;text-transform:uppercase}
.eyebrow::before{content:'';display:inline-block;width:26px;height:2px;background:var(--prime);vertical-align:middle;margin-right:10px;border-radius:2px}
h2{font-size:clamp(30px,5vw,48px);font-weight:600;margin:10px 0 6px}
h2 .lang-si{color:var(--primed);font-size:.6em;display:block;margin-top:4px}
.lead{color:var(--mut);max-width:780px;margin:10px 0 6px;font-size:16.5px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:18px;margin-top:26px}
.card{background:#fff;border:1px solid var(--line);border-radius:12px;padding:26px 24px;position:relative;
box-shadow:0 10px 30px rgba(12,30,33,.06);transition:.25s}
.card:hover{border-color:var(--prime);transform:translateY(-4px);box-shadow:0 18px 40px rgba(39,163,201,.16)}
.card h3{font-size:18px;margin-bottom:10px;font-weight:600}
.card p{font-size:15px;color:var(--mut)}
.card p.lang-si{color:var(--primed)}
.teaser{display:block;text-decoration:none;background:#fff;border:1px solid var(--line);border-top:4px solid var(--prime);
border-radius:12px;padding:26px 24px;box-shadow:0 10px 30px rgba(12,30,33,.06);transition:.25s}
.teaser:hover{transform:translateY(-5px);box-shadow:0 20px 44px rgba(39,163,201,.2);border-color:var(--prime)}
.teaser h3{color:var(--ink);font-size:19px;font-weight:700}
.teaser .tagline{font-style:italic;color:var(--primed);font-size:15px;margin:10px 0}
.teaser .go{font-weight:700;color:var(--ink);font-size:15px}
.hlbox{border:1px solid var(--prime);background:var(--tint);border-radius:12px;padding:22px 24px;margin-top:22px;text-align:center}
.hlbox b{color:var(--ink);font-size:18px;font-weight:700}
.hlbox span{display:block;color:var(--mut);margin-top:6px}
.timeline{display:grid;gap:16px;margin-top:24px}
.month{display:grid;grid-template-columns:150px 1fr;background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;
box-shadow:0 10px 30px rgba(12,30,33,.06)}
.month .m{background:var(--ink);color:#fff;font-weight:700;display:flex;align-items:center;flex-direction:column;
justify-content:center;text-align:center;padding:20px 10px;font-size:16px;line-height:1.4;gap:6px}
.month .d{padding:20px 24px}
.month .d b{font-size:17.5px;color:var(--ink)}
.month .d p{color:var(--mut);font-size:15px;margin-top:6px}
.month .d p.lang-si{color:var(--primed)}
ul.check{list-style:none;margin-top:16px;display:grid;gap:10px}
ul.check li{background:#fff;border:1px solid var(--line);border-radius:10px;padding:12px 16px;font-size:15px}
.pkg{border:1px solid var(--line);border-radius:16px;overflow:hidden;margin-top:20px;background:#fff;
box-shadow:0 14px 36px rgba(12,30,33,.09)}
.pkg-head{padding:18px 24px;background:var(--ink);display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.pkg-head .num{background:var(--prime);color:#fff;font-weight:800;border-radius:50px;padding:5px 14px;font-size:14px}
.pkg-head h3{font-size:22px;color:#fff;font-weight:700}
.pkg-head h3 small{color:#a9d8e8;font-size:14px;font-weight:500}
.pkg-head .pop{margin-left:auto;background:#fff;color:var(--ink);font-size:12px;font-weight:800;border-radius:50px;padding:5px 16px}
.pkg-body{padding:22px 24px}
.price{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:14px}
.price div{flex:1;min-width:200px;background:#f2f6f6;border:1.5px solid var(--prime);border-radius:12px;padding:12px 16px;text-align:center}
.price b{font-size:28px;color:var(--ink);font-weight:800;letter-spacing:-.02em}
.price span{display:block;font-size:12px;color:var(--mut2);letter-spacing:1px;font-weight:600}
ul.feat{list-style:none;margin:6px 0}
ul.feat li{padding:8px 0 8px 30px;position:relative;font-size:15px;color:var(--mut);border-bottom:1px dashed var(--line)}
ul.feat li::before{content:'◆';position:absolute;left:8px;color:var(--prime);font-size:12px;top:12px}
ul.feat li .lang-si{color:var(--primed)}
table.tiers{width:100%;border-collapse:collapse;margin-top:12px;font-size:15px}
table.tiers th,table.tiers td{border:1px solid var(--line);padding:11px;text-align:center}
table.tiers th{background:var(--ink);color:#fff;font-weight:600}
table.tiers td{color:var(--mut)}
.gallery{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:22px}
.gallery figure{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;transition:.25s}
.gallery figure:hover{transform:translateY(-4px);box-shadow:0 16px 36px rgba(39,163,201,.16)}
.gallery img{width:100%;display:block;min-height:120px;background:#0c1e21}
.gallery figcaption{padding:10px 12px;font-size:12.5px;color:var(--mut2);text-align:center}
details{background:#fff;border:1px solid var(--line);border-radius:12px;padding:16px 20px;margin-top:12px}
summary{font-weight:600;cursor:pointer;font-size:16px;color:var(--ink)}
details p{color:var(--mut);font-size:15px;margin-top:8px}
.contact-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:22px}
.cbox{background:#fff;border:1.5px solid var(--prime);border-radius:12px;padding:18px 14px;text-align:center}
.cbox small{display:block;color:var(--mut2);font-size:11.5px;letter-spacing:2px;font-weight:700}
.cbox a,.cbox b{font-size:17px;font-weight:700;text-decoration:none;color:var(--ink)}
.socials{display:flex;gap:10px;flex-wrap:wrap;justify-content:center;margin-top:18px}
.socials a{text-decoration:none;border:1.5px solid var(--ink);color:var(--ink);border-radius:50px;padding:8px 20px;
font-size:14px;font-weight:600;background:#fff;transition:.2s}
.socials a:hover{background:var(--ink);color:#fff}
footer{text-align:center;padding:36px 20px;font-size:14px;background:var(--ink);color:#a9b8b8;margin-top:60px;line-height:2}
footer b{color:#fff}
.big-cta{background:linear-gradient(135deg,#0c1e21,#16424b);color:#fff;border-radius:24px;padding:48px 26px;
text-align:center;margin-top:10px;border:1px solid rgba(255,255,255,.12)}
.big-cta h2{color:#fff}
.big-cta p{color:#cfe0e6;font-weight:500}
.big-cta .btn{margin:6px}
.wa-float{position:fixed;right:18px;bottom:18px;z-index:60;background:#25d366;color:#fff;font-size:26px;text-decoration:none;
width:58px;height:58px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(0,0,0,.3)}
.pagehero{text-align:center;padding:54px 30px 40px;margin:26px 0 6px;border-radius:24px;
background:linear-gradient(270deg,#e4f5fc,#dff1f0,#e6f4fb,#d9efe9,#e4f5fc);background-size:200% 200%;
animation:hmshift 18s ease infinite;border:1px solid rgba(39,163,201,.25)}
.pagehero h1{font-size:clamp(32px,5.5vw,54px)}
.login-wrap{max-width:470px;margin:10px auto 30px;background:#fff;border:1px solid var(--line);border-radius:16px;
padding:36px 32px;box-shadow:0 18px 44px rgba(12,30,33,.1);text-align:center}
.login-wrap h3{font-size:22px;margin:8px 0 14px}
.login-wrap input{width:100%;padding:13px 18px;margin:7px 0;border:1.5px solid var(--line);border-radius:50px;
font-size:15px;font-family:inherit;text-align:center;color:var(--ink)}
.login-wrap input:focus{outline:none;border-color:var(--prime)}
.login-wrap .btn{margin-top:12px;cursor:pointer;font-family:inherit}
.login-err{color:#c0392b;font-size:14px;min-height:24px;font-weight:600;margin-top:6px}
.dash-table{width:100%;border-collapse:collapse;margin-top:14px;font-size:13.5px;background:#fff}
.dash-table th,.dash-table td{border:1px solid var(--line);padding:8px 10px;text-align:left;color:var(--mut)}
.dash-table th{background:var(--ink);color:#fff}
.pill-ok{display:inline-block;background:#1e9e6a;color:#fff;border-radius:50px;padding:2px 12px;font-size:12px;font-weight:700}
.pill-no{display:inline-block;background:#c0392b;color:#fff;border-radius:50px;padding:2px 12px;font-size:12px;font-weight:700}
code.k{background:#f2f6f6;border:1px solid var(--line);border-radius:6px;padding:1px 8px;font-size:13px;color:var(--ink)}
textarea.tsv{width:100%;border:1.5px solid var(--line);border-radius:12px;padding:12px;font-size:12.5px;
font-family:monospace;color:var(--ink);background:#f8fbfb}
ol.steps{margin:12px 0 12px 22px;color:var(--mut);font-size:15px;display:grid;gap:10px}
.video-wrap{position:relative;padding-bottom:56.25%;height:0;overflow:hidden;border-radius:16px;
border:1px solid var(--line);box-shadow:0 18px 44px rgba(12,30,33,.14);margin:22px auto 0;max-width:860px;background:#0c1e21}
.video-wrap video{position:absolute;top:0;left:0;width:100%;height:100%;display:block;background:#0c1e21}
.vid-cap{text-align:center;color:var(--mut2);font-size:14px;margin:12px 0 0}
.vid-cap a{color:var(--primed);font-weight:600}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}
.rv.in{opacity:1;transform:none}
@media(max-width:640px){.month{grid-template-columns:1fr}.langsw{margin-left:0}section{padding:56px 0}.hero{padding:44px 20px}}
"""

JS = """
var _T0=document.title;
function _T(m){try{var p=_T0.split('|');if(p.length>=3){document.title=m==='en'?p[0].trim():m==='si'?p[1].trim():(p[0].split('—')[0].trim()+' — '+p[2].trim())}}catch(e){}}
function setLang(m){try{
document.documentElement.lang=m;document.body.setAttribute('data-langmode',m);_T(m);
document.querySelectorAll('.langsw button').forEach(function(b){b.classList.toggle('active',b.dataset.m===m)});
try{localStorage.setItem('ceyteq_lang',m)}catch(e){}
}catch(e){}}
(function(){var m='si';try{m=localStorage.getItem('ceyteq_lang')||'si'}catch(e){}
if(['si','en','fr'].indexOf(m)<0)m='si';
document.documentElement.lang=m;document.body.setAttribute('data-langmode',m);_T(m);
document.querySelectorAll('.langsw button').forEach(function(b){b.classList.toggle('active',b.dataset.m===m)});
})();
(function(){try{var els=document.querySelectorAll('.card,.teaser,.pkg,.month,.hlbox,.stat');if(!('IntersectionObserver' in window))return;var o=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');o.unobserve(e.target)}})},{threshold:.08});els.forEach(function(el){el.classList.add('rv');o.observe(el)});}catch(e){}})();
"""

SHEET_ID = '1iT7QmbY0b-u5xjmGcaHBw8vOOpu2xNb5GTuKaPVBaKw'
SHEET_EDIT_URL = 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit'
# Admin login signature = base64(user + '::' + pass). To change credentials run:
#   python3 -c "import base64; print(base64.b64encode(b'USER::PASS').decode())"
# and paste the result below (front-end lock: keeps casual visitors out).
ADMIN_SIG = 'YWRtaW46OmNleXRlcUAyMDI2'

# ---- SEO / social sharing (WhatsApp, Facebook, Instagram previews) ----
SITE_URL = 'https://www.ceyteq.linkpc.net'
SITE_NAME = 'CEYTEQ Digital Race'
# per page: (meta description, og:image)
PAGE_META = {
    'index.html': ("CEYTEQ Digital Race — 90-day digital transformation program for Sri Lankan restaurants & local businesses. Websites, WhatsApp ordering, AI bots, training & monthly marketing. | ඩිජිටල් රේස් වැඩසටහන — දින 90 වැඩසටහන.",
                   'flyer-01-program-intro.png'),
    'system.html': ("The Matrix System — morning + evening campaign matrices, Facebook/Instagram/TikTok/YouTube. Only $1–$2/day ad spend paid direct to platforms, Ceyteq optimization free. | මැට්‍රික්ස් ක්‍රමය.",
                    'flyer-04-how-it-works.png'),
    'training.html': ("90-day Digital Race training roadmap: month-by-month coaching, daily habits and full automation. | දින 90 පුහුණු පටිපාටිය.",
                      'flyer-05-training-90-day.png'),
    'packages.html': ("Digital Race packages: Starter $19, Standard $60, Advanced $80, Premium Ultimate $250. Website, admin panel, AI chatbots & monthly content. | පැකේජ 4 — Starter $19 සිට.",
                      'flyer-06-package-starter.png'),
    'ai.html': ("AI solutions for local business: chatbots, voice bots, automation and a future-ready AI roadmap. | AI bots සහ automation විසඳුම්.",
                'flyer-10-ai-future-contact.png'),
    'flyers.html': ("10 bilingual (English + Sinhala) flyers ready to share on WhatsApp, Facebook, Instagram, TikTok and YouTube. | Share කිරීමට ෆ්ලයර් 10.",
                    'flyer-01-program-intro.png'),
    'admin.html': ("Ceyteq admin panel — flyers database management. | පරිපාලක පුවිසුම.",
                   'flyer-01-program-intro.png'),
}
FAVICON = 'assets/logo-transparent.png'


def head_meta(fname, title):
    desc, ogimg = PAGE_META.get(fname, (SITE_NAME, 'flyer-01-program-intro.png'))
    url = f'{SITE_URL}/{fname}'
    img = f'{SITE_URL}/flyers/{ogimg}'
    return (f'<meta name="description" content="{desc}">\n'
            f'<meta name="author" content="Ceylon Technology — Ceyteq">\n'
            f'<meta name="theme-color" content="#0c1e21">\n'
            f'<link rel="canonical" href="{url}">\n'
            f'<link rel="icon" type="image/png" href="{FAVICON}">\n'
            f'<link rel="apple-touch-icon" href="{FAVICON}">\n'
            f'<meta property="og:type" content="website">\n'
            f'<meta property="og:site_name" content="{SITE_NAME}">\n'
            f'<meta property="og:title" content="{title}">\n'
            f'<meta property="og:description" content="{desc}">\n'
            f'<meta property="og:url" content="{url}">\n'
            f'<meta property="og:image" content="{img}">\n'
            f'<meta property="og:image:width" content="1080">\n'
            f'<meta property="og:image:height" content="1350">\n'
            f'<meta property="og:locale" content="si_LK">\n'
            f'<meta property="og:locale:alternate" content="en_US">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n'
            f'<meta name="twitter:title" content="{title}">\n'
            f'<meta name="twitter:description" content="{desc}">\n'
            f'<meta name="twitter:image" content="{img}">')

NAVITEMS = [
    ('index.html', 'Home', 'මුල් පිටුව', 'Accueil'),
    ('system.html', 'System', 'ක්‍රමය', 'Système'),
    ('training.html', 'Training', 'පුහුණුව', 'Formation'),
    ('packages.html', 'Packages', 'පැකේජ', 'Forfaits'),
    ('ai.html', 'AI', 'AI', 'IA'),
    ('flyers.html', 'Flyers', 'ෆ්ලයර්', 'Flyers'),
    ('packages.html#contact', 'Contact', 'සම්බන්ධය', 'Contact'),
]

def nav(active):
    links = []
    for href, en, si, fr in NAVITEMS:
        cls = 'active' if href == active else ''
        links.append(f'<a class="{cls}" href="{href}"><span class="lang-en">{en}</span><span class="lang-si">{si}</span><span class="lang-fr">{fr}</span></a>')
    return f"""<nav><div class="wrap">
<img class="logo" src="{LOGO}" alt="Ceyteq logo">
<div class="brand">CEYTEQ<small><span class="lang-en">EMPOWERING DIGITAL EVOLUTION</span><span class="lang-si">ඩිජිටල් පරිණාමය සවිබල ගැන්වීම</span><span class="lang-fr">FAVORISER L'ÉVOLUTION NUMÉRIQUE</span></small></div>
<div class="links">{''.join(links)}</div>
<div class="langsw">
<button data-m="si" onclick="setLang('si')"><span class="lang-en">SINHALA</span><span class="lang-si">සිංහල</span><span class="lang-fr">SINGHALAIS</span></button>
<button data-m="en" onclick="setLang('en')"><span class="lang-en">ENGLISH</span><span class="lang-si">ඉංග්‍රීසි</span><span class="lang-fr">ANGLAIS</span></button>
<button data-m="fr" onclick="setLang('fr')"><span class="lang-en">FRENCH</span><span class="lang-si">ප්‍රංශ</span><span class="lang-fr">FRANÇAIS</span></button>
</div></div></nav>
<a class="wa-float" href="https://wa.me/94768607143" target="_blank" title="WhatsApp">✆</a>"""

CONTACT = f"""<section id="contact"><div class="wrap">
<div class="big-cta">
<h2><span class="lang-en">START YOUR DIGITAL RACE TODAY</span><span class="lang-si">අදම Digital Race පටන්ගන්න</span><span class="lang-fr">DÉMARREZ VOTRE DIGITAL RACE AUJOURD'HUI</span></h2>
<p><span class="lang-en">Message us now — reply within business hours. Team Creat + Ceyteq.</span><span class="lang-si">දැන් message කරන්න — Team Creat + Ceyteq.</span><span class="lang-fr">Écrivez-nous — réponse pendant les heures ouvrables.</span></p>
<p><a class="btn btn-cyan" href="https://wa.me/94768607143" target="_blank">💬 WhatsApp: +94 76 860 7143</a>
<a class="btn btn-cyan" href="tel:+94788607143" style="background:#fff;color:#0b1f33">📞 +94 78 860 7143</a></p>
</div>
<div class="contact-grid">
<div class="cbox"><small><span class="lang-en">HOTLINE</span><span class="lang-si">හොට්ලයින්</span><span class="lang-fr">LIGNE DIRECTE</span></small><a href="tel:+94788607143">+94 78 860 7143</a></div>
<div class="cbox"><small><span class="lang-en">WHATSAPP INTL</span><span class="lang-si">WHATSAPP (විදේශ)</span><span class="lang-fr">WHATSAPP INTL</span></small><a href="https://wa.me/33744284269" target="_blank">+33 7 44 28 42 69</a></div>
<div class="cbox"><small><span class="lang-en">WHATSAPP / MOBILE</span><span class="lang-si">WHATSAPP / ජංගම</span><span class="lang-fr">WHATSAPP / MOBILE</span></small><a href="https://wa.me/94768607143" target="_blank">+94 76 860 7143</a></div>
<div class="cbox"><small><span class="lang-en">EMAIL</span><span class="lang-si">ඊමේල්</span><span class="lang-fr">E-MAIL</span></small><a href="mailto:info.ceyteq@gmail.com">info.ceyteq@gmail.com</a></div>
</div>
<div class="socials">
<a href="https://www.facebook.com/share/1KM2kZvaCC/" target="_blank">Facebook</a>
<a href="https://www.instagram.com/ceyteq/" target="_blank">Instagram</a>
<a href="https://www.tiktok.com/@ceyteq?is_from_webapp=1&sender_device=pc" target="_blank">TikTok</a>
<a href="https://youtube.com/@ceylontechnology-ceyteq?si=a4L-B_OZjvhjO7sw" target="_blank">YouTube</a>
<a href="https://www.linkedin.com/in/ceylon-technology" target="_blank">LinkedIn</a>
<a href="https://www.pinterest.com/infoceyteq/" target="_blank">Pinterest</a>
<a href="https://x.com/CeylonTech22598" target="_blank">X (Twitter)</a>
</div></div></section>
<footer><b>© 2026 Ceylon Technology — Ceyteq</b> • <span class="lang-en">Empowering Digital Evolution • Digital Race Program</span><span class="lang-si">ඩිජිටල් පරිණාමය සවිබල ගැන්වීම • ඩිජිටල් රේස් වැඩසටහන</span><span class="lang-fr">Favoriser l'évolution numérique • Programme Digital Race</span><br>
<span class="lang-en">Starter $19 • Standard $60 • Advanced $80 • Premium Ultimate $250 • Ad spend $1–$2/day to platforms</span><span class="lang-si">Starter $19 • Standard $60 • Advanced $80 • Premium Ultimate $250 • Platforms වලට දවසට $1–$2</span><span class="lang-fr">Starter 19 $ • Standard 60 $ • Advanced 80 $ • Premium Ultimate 250 $ • 1–2 $/jour aux plateformes</span></footer>"""

FOOTMINI = """<footer><b>© 2026 Ceylon Technology — Ceyteq</b> • <span class="lang-en">Empowering Digital Evolution • Digital Race Program</span><span class="lang-si">ඩිජිටල් පරිණාමය සවිබල ගැන්වීම • ඩිජිටල් රේස් වැඩසටහන</span><span class="lang-fr">Favoriser l'évolution numérique • Programme Digital Race</span></footer>"""

LOADER_JS = """<script>
(function(){try{
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function safeSrc(f){f=String(f||'').trim();return /^(https?:)?\\/\\//i.test(f)?f:'flyers/'+f.replace(/[^A-Za-z0-9._\\-]/g,'')}
var SHEET_ID='__SHEET_ID__';
var url='https://docs.google.com/spreadsheets/d/'+SHEET_ID+'/gviz/tq?tqx=out:json&gid=0';
fetch(url).then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(t){
var m=t.match(/google\\.visualization\\.Query\\.setResponse\\(([\\s\\S]+?)\\);?\\s*$/);
if(!m)return;var d=JSON.parse(m[1]);
var rows=((d.table||{}).rows||[]).map(function(r){return (r.c||[]).map(function(c){return c&&c.v!==null&&c.v!==undefined?String(c.v):''})});
if(!rows.length)return;
var s=0;if(rows[0]&&/^file$/i.test((rows[0][0]||'').trim()))s=1;
var items=[];
for(var i=s;i<rows.length;i++){var r=rows[i];var f=(r[0]||'').trim();if(!f)continue;
var v=(r[4]||'').toString().trim().toLowerCase();
if(v==='no'||v==='false'||v==='0'||v==='hide'||v==='hidden'||v==='off')continue;
items.push({f:f,en:r[1]||'',si:r[2]||'',fr:r[3]||''});}
if(!items.length)return;
var g=document.getElementById('flyerGallery');if(!g)return;
var h='';
for(var k=0;k<items.length;k++){var it=items[k];
var n=('0'+(k+1)).slice(-2);
h+='<figure><img loading="lazy" src="'+esc(safeSrc(it.f))+'" alt="'+esc(it.en)+'"><figcaption>'+n+' • <span class="lang-en">'+esc(it.en)+'</span><span class="lang-si">'+esc(it.si)+'</span><span class="lang-fr">'+esc(it.fr)+'</span></figcaption></figure>';}
g.innerHTML=h;
}).catch(function(){});
}catch(e){}})();
</script>"""

ADMIN_LINK = """<div style="text-align:center;margin-top:28px"><a href="admin.html" style="color:#67787a;font-size:13px;text-decoration:none;border:1px solid #c9d1d1;border-radius:50px;padding:7px 18px;background:#fff"><span class="lang-en">\\U0001f510 Admin Login</span><span class="lang-si">\\U0001f510 Admin \\u0db4\\u0dd2\\u0dc0\\u0dd2\\u0dc3\\u0dd4\\u0db8</span><span class="lang-fr">\\U0001f510 Connexion admin</span></a></div>"""

TSV_DATA = ('file\\ttitle_en\\ttitle_si\\ttitle_fr\\tvisible\\n'
'flyer-01-program-intro.png\\tProgram Intro\\t\\u0dc0\\u0dd0\\u0da9\\u0dc3\\u0da7\\u0dc4\\u0db1\\tIntro\\tYES\\n'
'flyer-02-why-now.png\\tWhy Now\\t\\u0d87\\u0dba\\u0dd2 \\u0daf\\u0db1\\u0dca\\u0db8\\tPourquoi maintenant\\tYES\\n'
'flyer-03-what-changes.png\\tWhat Changes\\t\\u0dc0\\u0dd9\\u0db1\\u0dc3\\tChangements\\tYES\\n'
'flyer-04-how-it-works.png\\tHow It Works\\t\\u0d9a\\u0ddca\\u0dbb\\u0dca\\u0db8\\u0dba\\tSyst\\u00e8me\\tYES\\n'
'flyer-05-training-90-day.png\\t90-Day Training\\t\\u0db4\\u0dd4\\u0dc4\\u0dd4\\u0dab\\u0dd4\\u0dc0\\tFormation\\tYES\\n'
'flyer-06-package-starter.png\\tStarter $19\\t\\u0d86\\u0dbb\\u0db8\\u0dca\\u0db7\\u0d9a\\tStarter 19 $\\tYES\\n'
'flyer-07-package-standard.png\\tStandard $60\\t\\u0dc3\\u0db8\\u0dca\\u0db8\\u0d9a\\tStandard 60 $\\tYES\\n'
'flyer-08-package-advanced.png\\tAdvanced $80\\t\\u0d8b\\u0dc3\\u0dc3\\tAvanc\\u00e9 80 $\\tYES\\n'
'flyer-09-package-premium.png\\tPremium $250\\t\\u0d89\\u0dc4\\u0dc5\\u0db8\\tPremium 250 $\\tYES\\n'
'flyer-10-ai-future-contact.png\\tAI + Contact\\tAI + \\u0dc3\\u0db8\\u0dca\\u0db6\\u0dca\\u0db0\\u0dba\\tIA + Contact\\tYES')

TEASERS = [
 ("system.html", "⚙️", "SYSTEM", "ක්‍රමය", "SYSTÈME", "\"Morning + evening campaign matrices that never sleep.\"", "\"නිදා නොගන්නා උදේ + හවස campaign මැට්‍රික්ස්.\"", "« Des matrices matin + soir qui ne dorment jamais. »", "Open System →", "ක්‍රමය බලන්න →", "Voir le système →"),
 ("training.html", "🎓", "TRAINING", "පුහුණුව", "FORMATION", "\"90 days: from first login to full automation.\"", "\"දින 90: පළමු login සිට සම්පූර්ණ automation දක්වා.\"", "« 90 jours : de la première connexion à l'automatisation. »", "Open Training →", "පුහුණුව බලන්න →", "Voir la formation →"),
 ("packages.html", "💎", "PACKAGES", "පැකේජ", "FORFAITS", "\"Four tiers for every budget — see full details.\"", "\"සෑම budget එකකටම tiers 4 — details බලන්න.\"", "\"Quatre paliers pour chaque budget — voir les détails.\"", "Open Packages →", "පැකේජ බලන්න →", "Voir les forfaits →"),
 ("ai.html", "🤖", "AI SOLUTIONS", "AI විසඳුම්", "SOLUTIONS IA", "\"Bots today, full automation tomorrow.\"", "\"අද bots, හෙට සම්පූර්ණ automation.\"", "« Des bots aujourd'hui, l'automatisation demain. »", "Open AI →", "AI බලන්න →", "Voir l'IA →"),
 ("flyers.html", "🖼️", "FLYERS", "ෆ්ලයර්", "FLYERS", "\"10 bilingual flyers ready to share.\"", "\"Share කිරීමට සූදානම් ෆ්ලයර් 10.\"", "\"10 flyers bilingues prêts à partager.\"", "Open Flyers →", "ෆ්ලයර් බලන්න →", "Voir les flyers →"),
]

def teaser_card(t):
    href, icon, en, si, fr, tag_en, tag_si, tag_fr, go_en, go_si, go_fr = t
    return ('<a class="teaser" href="' + href + '"><h3>' + icon + ' <span class="lang-en">' + en + '</span>'
            '<span class="lang-si">' + si + '</span><span class="lang-fr">' + fr + '</span></h3>'
            '<div class="tagline"><span class="lang-en">' + tag_en + '</span><span class="lang-si">' + tag_si + '</span><span class="lang-fr">' + tag_fr + '</span></div>'
            '<div class="go"><span class="lang-en">' + go_en + '</span><span class="lang-si">' + go_si + '</span><span class="lang-fr">' + go_fr + '</span></div></a>')

def explore_more(exclude):
    cards = ''.join(teaser_card(t) for t in TEASERS if t[0] != exclude)
    return ('<section><div class="eyebrow"><span class="lang-en">Keep exploring</span>'
            '<span class="lang-si">තව ගවේෂණය කරන්න</span>'
            '<span class="lang-fr">Continuez à explorer</span></div>'
            '<h2><span class="lang-en">More Doors of the Race</span>'
            '<span class="lang-si">තරඟයේ තවත් දොරටු</span>'
            '<span class="lang-fr">Autres portes de la course</span></h2>'
            '<div class="grid">' + cards + '</div></section>')

def page(title, active, body, contact=True, fname='index.html'):
    return f"""<!DOCTYPE html>
<html lang="si"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Mona+Sans:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
<title>{title}</title>
{head_meta(fname, title)}
<style>{CSS}</style></head>
<body data-langmode="si">{nav(active)}<div class="wrap">{body}</div>{CONTACT if contact else FOOTMINI}
<script>{JS}</script></body></html>"""

# ================= HOME =================
HOME = f"""
<div class="hero">
<img class="main-logo" src="{LOGO}" alt="Ceyteq — Empowering Digital Evolution">
<div><span class="pill"><span class="lang-en">B2B DIGITAL TRANSFORMATION PROGRAM</span><span class="lang-si">B2B ඩිජිටල් පරිවර්තන වැඩසටහන</span><span class="lang-fr">PROGRAMME DE TRANSFORMATION NUMÉRIQUE B2B</span></span></div>
<h1><span class="lang-en">DIGITAL RACE PROGRAM</span><span class="lang-si">ඩිජිටල් රේස් වැඩසටහන</span><span class="lang-fr">PROGRAMME DIGITAL RACE</span></h1>
<div class="alien">
<div class="kick">★ <span class="lang-en">HIGHLIGHTED CORE METHOD</span><span class="lang-si">ප්‍රධාන ක්‍රමවේදය</span><span class="lang-fr">MÉTHODE CENTRALE</span> ★</div>
<div class="ah"><div class="lang-en">👽 THE ALIEN MARKETING MATRIX METHOD</div><div class="lang-si">👽 ඒලියන් මාර්කටින් මැට්‍රික්ස් ක්‍රමය</div><div class="lang-fr">👽 LA MÉTHODE ALIEN MARKETING MATRIX</div></div>
<p><span class="lang-en">A highly advanced, unconventional, hyper-efficient approach to web marketing. We don't just build websites — we deploy powerful sales engines.</span><span class="lang-si">ඉතා දියුණු, සම්ප්‍රදායික නොවන, අතිශය කාර්යක්ෂම web marketing ක්‍රමයක්. Website විතරක් නෙවෙයි — බලවත් විකුණුම් යන්ත්‍ර.</span><span class="lang-fr">Une approche webmarketing avancée, non conventionnelle et hyper-efficace. Nous déployons de puissants moteurs de vente, pas de simples sites.</span></p>
</div>
<div class="tag"><span class="lang-en">Upgrade Your Business</span><span class="lang-si">ඔබේ ව්‍යාපාරය ඩිජිටල් යුගයට උසස් කරන්න</span><span class="lang-fr">Faites évoluer votre entreprise</span></div>
<div class="tag2"><span class="lang-en">Going digital is no longer an option — it's a race.</span><span class="lang-si">Digital වීම විකල්පයක් නොවෙයි — එය තරඟයක්.</span><span class="lang-fr">Passer au numérique n'est plus une option — c'est une course.</span></div>
<div class="cta-row">
<a class="btn btn-cyan" href="tel:+94788607143">📞 <span class="lang-en">Hotline: 078 860 7143</span><span class="lang-si">හොට්ලයින්: 078 860 7143</span><span class="lang-fr">Ligne directe : 078 860 7143</span></a>
<a class="btn btn-navy" href="https://wa.me/94768607143" target="_blank">💬 WhatsApp</a>
<a class="btn btn-ghost" href="#explore"><span class="lang-en">Explore ↓</span><span class="lang-si">ගවේෂණය ↓</span><span class="lang-fr">Explorer ↓</span></a>
</div>
<div class="stats">
<div class="stat"><b>90 <span class="lang-en">Days</span><span class="lang-si">දින</span><span class="lang-fr">jours</span></b><span class="lang-en">Hands-on training</span><span class="lang-si">ප්‍රායෝගික පුහුණුව</span><span class="lang-fr">Formation pratique</span></div>
<div class="stat"><b><span class="lang-en">Alien Matrix</span><span class="lang-si">මැට්‍රික්ස්</span><span class="lang-fr">Matrice Alien</span></b><span class="lang-en">Morning + evening system</span><span class="lang-si">උදේ + හවස ක්‍රමය</span><span class="lang-fr">Système matin + soir</span></div>
<div class="stat"><b><span class="lang-en">FREE</span><span class="lang-si">නොමිලේ</span><span class="lang-fr">GRATUIT</span></b><span class="lang-en">Setup + optimization</span><span class="lang-si">සැකසුම + optimization</span><span class="lang-fr">Installation + optimisation</span></div>
<div class="stat"><b>24/7 AI</b><span class="lang-en">Bots & automation</span><span class="lang-si">Bots සහ automation</span><span class="lang-fr">Bots et automatisation</span></div>
</div></div>



<section id="program">
<div class="eyebrow"><span class="lang-en">01 • The Program</span><span class="lang-si">01 • වැඩසටහන</span><span class="lang-fr">01 • Le programme</span></div>
<h2><span class="lang-en">What is Digital Race?</span><span class="lang-si">Digital Race කියන්නේ මොකක්ද?</span><span class="lang-fr">Qu'est-ce que Digital Race ?</span></h2>
<p class="lead"><span class="lang-en">A 90-day, hands-on ecosystem program for restaurants, food outlets and local businesses. We deploy powerful sales engines, train your team, and integrate future-ready AI.</span><span class="lang-si">Restaurants, කඩ සහ දේශීය ව්‍යාපාර සඳහා දින 90 ප්‍රායෝගික වැඩසටහනක්. විකුණුම් යන්ත්‍රයක් + පුහුණුව + AI විසඳුම්.</span><span class="lang-fr">Un programme pratique de 90 jours pour restaurants et commerces locaux. Moteurs de vente, formation d'équipe et IA d'avenir.</span></p>
<div class="video-wrap"><video controls playsinline preload="metadata" src="assets/intro-720p.mp4"></video></div>
<p class="vid-cap"><span class="lang-en">▶ Watch: Digital Race introduction</span><span class="lang-si">▶ බලන්න: Digital Race හැඳින්වීම</span><span class="lang-fr">▶ Regarder : présentation Digital Race</span> • <a href="https://drive.google.com/file/d/1OCmMFWlya_NTx4hsyMupTXh2ytCtyWVJ/view" target="_blank"><span class="lang-en">Watch on Google Drive</span><span class="lang-si">Google Drive eke බලන්න</span><span class="lang-fr">Voir sur Google Drive</span></a></p>
<div class="grid">
<div class="card"><h3>🎯 <span class="lang-en">Who is it for?</span><span class="lang-si">කාටද?</span><span class="lang-fr">Pour qui ?</span></h3><p class="lang-en">Local restaurant owners & outlets ready for online orders.</p><p class="lang-si">Online orders ගන්න කැමති restaurants සහ කඩ හිමියන්ට.</p><p class="lang-fr">Restaurateurs et commerçants prêts pour les commandes en ligne.</p></div>
<div class="card"><h3>👽 <span class="lang-en">Alien Marketing Matrix</span><span class="lang-si">මැට්‍රික්ස් ක්‍රමය</span><span class="lang-fr">Matrice Alien</span></h3><p class="lang-en">Unconventional, hyper-efficient web marketing: morning + evening matrices.</p><p class="lang-si">අතිශය කාර්යක්ෂම නවීන marketing — උදේ + හවස.</p><p class="lang-fr">Webmarketing hyper-efficace et non conventionnel : matrices matin + soir.</p></div>
<div class="card"><h3>🚀 <span class="lang-en">Sales engine, not a site</span><span class="lang-si">විකුණුම් යන්ත්‍රයක්</span><span class="lang-fr">Un moteur de vente</span></h3><p class="lang-en">Web panel, WhatsApp ordering, promos, analytics & automation in one.</p><p class="lang-si">Orders, promos, analytics — සියල්ල එක system එකක.</p><p class="lang-fr">Commandes, promos, statistiques et automatisation en un seul système.</p></div>
</div></section>

<section id="faq">
<div class="eyebrow"><span class="lang-en">FAQ</span><span class="lang-si">නිතර අසන ප්‍රශ්න</span><span class="lang-fr">FAQ</span></div>
<h2><span class="lang-en">Quick Answers</span><span class="lang-si">ඉක්මන් පිළිතුරු</span><span class="lang-fr">Réponses rapides</span></h2>
<details open><summary><span class="lang-en">💵 What must I pay besides the package?</span><span class="lang-si">💵 පැකේජයට අමතරව ගෙවිය යුතුද?</span><span class="lang-fr">💵 Que payer en plus du forfait ?</span></summary><p class="lang-en">Only $1–$2/day ad spend, paid by YOU directly to Meta/TikTok. Ceyteq optimization FREE.</p><p class="lang-si">දවසට $1–$2 platforms වලට පමණයි. Ceyteq optimization නොමිලේ.</p><p class="lang-fr">Seulement 1–2 $/jour de pub, payés par VOUS à Meta/TikTok. Optimisation Ceyteq GRATUITE.</p></details>
<details><summary><span class="lang-en">⏱️ How long is the program?</span><span class="lang-si">⏱️ කාලය කොච්චරද?</span><span class="lang-fr">⏱️ Quelle durée ?</span></summary><p class="lang-en">90 days: Month 1 daily coaching, Month 2 weekly optimization, Month 3 automation & ROI audit.</p><p class="lang-si">මාස 3: පළමු මාසය දිනපතා, දෙවන මාසය සතිපතා, තෙවන මාසය automation.</p><p class="lang-fr">90 jours : 1er mois quotidien, 2e hebdomadaire, 3e automatisation et audit ROI.</p></details>
<details><summary><span class="lang-en">📲 Zero digital knowledge — can I join?</span><span class="lang-si">📲 Digital දැනුම නැත්නම්?</span><span class="lang-fr">📲 Sans connaissances numériques ?</span></summary><p class="lang-en">Yes — Month 1 is exactly for that. Day-by-day coaching + staff training included.</p><p class="lang-si">ඔව් — පළමු මාසයම ඒ සඳහායි. Staff පුහුණුවත් ඇතුළත්.</p><p class="lang-fr">Oui — le 1er mois est fait pour cela. Formation du personnel incluse.</p></details>
<details><summary><span class="lang-en">🤖 Do I get AI bots?</span><span class="lang-si">🤖 AI bots ලැබෙනවාද?</span><span class="lang-fr">🤖 Des bots IA inclus ?</span></summary><p class="lang-en">Yes — selected tiers include AI chatbots and voice bots. See the Packages page for full details.</p><p class="lang-si">ඔව් — තෝරාගත් tiers වල AI chatbots සහ voice bots ඇතුළත්. සම්පූර්ණ details Packages page එකේ බලන්න.</p><p class="lang-fr">Oui — certains paliers incluent des chatbots IA et vocaux. Voir la page Forfaits.</p></details>
<div class="cta-row" style="margin-top:16px"><a class="btn btn-navy" href="packages.html">📦 <span class="lang-en">Package-related questions? See more →</span><span class="lang-si">පැකේජ ගැන ප්‍රශ්න? තව බලන්න →</span><span class="lang-fr">Questions sur les forfaits ? Voir plus →</span></a></div>
</section>

<section id="whynow">
<div class="eyebrow"><span class="lang-en">02 • Why Now</span><span class="lang-si">02 • ඇයි දැන්ම?</span><span class="lang-fr">02 • Pourquoi maintenant</span></div>
<h2><span class="lang-en">Sri Lanka's Digital Reality</span><span class="lang-si">ලංකාවේ ව්‍යාපාර ඉන්න තැන</span><span class="lang-fr">La réalité numérique au Sri Lanka</span></h2>
<p class="lead"><span class="lang-en">Customers live on their phones — but most local businesses are still fully offline.</span><span class="lang-si">Customersලා phone එකේ — නමුත් බොහෝ ව්‍යාපාර තවම offline.</span><span class="lang-fr">Les clients vivent sur leur téléphone — mais la plupart des commerces sont encore hors ligne.</span></p>
<div class="grid">
<div class="card"><h3>📱 <span class="lang-en">Customers are online</span><span class="lang-si">Customersලා online</span><span class="lang-fr">Clients connectés</span></h3><p class="lang-en">Sri Lankans order & shop by phone daily — Google, Maps, Facebook, TikTok.</p><p class="lang-si">Customersලා දවසේම phone එකෙන් order කරනවා.</p><p class="lang-fr">Les Sri Lankais commandent par téléphone chaque jour.</p></div>
<div class="card"><h3>🏚️ <span class="lang-en">Most shops offline</span><span class="lang-si">බොහෝ කඩ offline</span><span class="lang-fr">Commerces hors ligne</span></h3><p class="lang-en">No website, no ordering system, invisible to new customers.</p><p class="lang-si">Website එකක්වත්, order ක්‍රමයක්වත් නෑ.</p><p class="lang-fr">Pas de site, pas de commandes, invisibles pour les nouveaux clients.</p></div>
<div class="card"><h3>🏁 <span class="lang-en">Early movers win</span><span class="lang-si">කලින් අය දිනනවා</span><span class="lang-fr">Les premiers gagnent</span></h3><p class="lang-en">First to go digital owns Google, Maps & social in their area.</p><p class="lang-si">කලින් digital වෙන අය ප්‍රදේශය ජය ගන්නවා.</p><p class="lang-fr">Les premiers en ligne dominent Google, Maps et les réseaux.</p></div>
<div class="card"><h3>⏳ <span class="lang-en">Cost of waiting</span><span class="lang-si">බලා සිටීමේ පාඩුව</span><span class="lang-fr">Coût de l'attente</span></h3><p class="lang-en">Every offline day = lost orders, reviews, repeat customers.</p><p class="lang-si">Offline හැම දවසක්ම නැතිවෙන orders.</p><p class="lang-fr">Chaque jour hors ligne = commandes et clients perdus.</p></div>
</div>
<div class="hlbox"><b class="lang-en">The business world is moving fast — going digital is no longer an option, it's a race.</b><span class="lang-si">Digital වීම විකල්පයක් නොවෙයි — එය තරඟයක්. අදම පටන්ගන්න.</span><span class="lang-fr">Le monde avance vite — le numérique n'est plus une option, c'est une course.</span></div>
</section>

<section id="mission">
<div class="eyebrow"><span class="lang-en">Our Objective</span><span class="lang-si">ප්‍රධාන අරමුණ</span><span class="lang-fr">Notre objectif</span></div>
<h2><span class="lang-en">Why We Built This Program</span><span class="lang-si">මේ වැඩසටහනේ අරමුණ</span><span class="lang-fr">Pourquoi ce programme</span></h2>
<p class="lead"><span class="lang-en">To empower every Sri Lankan restaurant and local business to win the Digital Race — practical training, affordable systems, automated sales, future-ready AI. No one left offline.</span><span class="lang-si">ලංකාවේ සෑම restaurant එකක්ම, සෑම කඩයක්ම digital තරඟය ජයගන්න සවිබල ගැන්වීම — පුහුණුව, දැරිය හැකි system, ස්වයංක්‍රීය විකුණුම්, AI දැනුම.</span><span class="lang-fr">Donner à chaque restaurant et commerce sri-lankais les moyens de gagner la course numérique — formation, systèmes abordables, ventes automatisées et IA.</span></p>
</section>




<section id="explore">
<div class="eyebrow"><span class="lang-en">Explore the program</span><span class="lang-si">වැඩසටහන ගවේෂණය කරන්න</span><span class="lang-fr">Explorez le programme</span></div>
<h2><span class="lang-en">One Race. Five Doors.</span><span class="lang-si">එක තරඟයක්. දොරටු පහක්.</span><span class="lang-fr">Une course. Cinq portes.</span></h2>
<div class="grid">
<a class="teaser" href="system.html"><h3>⚙️ <span class="lang-en">SYSTEM</span><span class="lang-si">ක්‍රමය</span><span class="lang-fr">SYSTÈME</span></h3><div class="tagline"><span class="lang-en">"Morning + evening campaign matrices that never sleep."</span><span class="lang-si">"නිදා නොගන්නා උදේ + හවස campaign මැට්‍රික්ස්."</span><span class="lang-fr">« Des matrices matin + soir qui ne dorment jamais. »</span></div><div class="go"><span class="lang-en">Open System →</span><span class="lang-si">ක්‍රමය බලන්න →</span><span class="lang-fr">Voir le système →</span></div></a>
<a class="teaser" href="training.html"><h3>🎓 <span class="lang-en">TRAINING</span><span class="lang-si">පුහුණුව</span><span class="lang-fr">FORMATION</span></h3><div class="tagline"><span class="lang-en">"90 days: from first login to full automation."</span><span class="lang-si">"දින 90: පළමු login සිට සම්පූර්ණ automation දක්වා."</span><span class="lang-fr">« 90 jours : de la première connexion à l'automatisation. »</span></div><div class="go"><span class="lang-en">Open Training →</span><span class="lang-si">පුහුණුව බලන්න →</span><span class="lang-fr">Voir la formation →</span></div></a>
<a class="teaser" href="packages.html"><h3>💎 <span class="lang-en">PACKAGES</span><span class="lang-si">පැකේජ</span><span class="lang-fr">FORFAITS</span></h3><div class="tagline"><span class="lang-en">"Four tiers for every budget — see full details."</span><span class="lang-si">"සෑම budget එකකටම tiers 4 — details බලන්න."</span><span class="lang-fr">« Quatre paliers pour chaque budget — voir les détails. »</span></div><div class="go"><span class="lang-en">Open Packages →</span><span class="lang-si">පැකේජ බලන්න →</span><span class="lang-fr">Voir les forfaits →</span></div></a>
<a class="teaser" href="ai.html"><h3>🤖 <span class="lang-en">AI SOLUTIONS</span><span class="lang-si">AI විසඳුම්</span><span class="lang-fr">SOLUTIONS IA</span></h3><div class="tagline"><span class="lang-en">"Bots today, full automation tomorrow."</span><span class="lang-si">"අද bots, හෙට සම්පූර්ණ automation."</span><span class="lang-fr">« Des bots aujourd'hui, l'automatisation demain. »</span></div><div class="go"><span class="lang-en">Open AI →</span><span class="lang-si">AI බලන්න →</span><span class="lang-fr">Voir l'IA →</span></div></a>
<a class="teaser" href="flyers.html"><h3>🖼️ <span class="lang-en">FLYERS</span><span class="lang-si">ෆ්ලයර්</span><span class="lang-fr">FLYERS</span></h3><div class="tagline"><span class="lang-en">"10 bilingual flyers ready to share."</span><span class="lang-si">"Share කිරීමට සූදානම් ෆ්ලයර් 10."</span><span class="lang-fr">« 10 flyers bilingues prêts à partager. »</span></div><div class="go"><span class="lang-en">Open Flyers →</span><span class="lang-si">ෆ්ලයර් බලන්න →</span><span class="lang-fr">Voir les flyers →</span></div></a>
</div></section>
"""

# ================= SYSTEM =================
SYSTEM = """
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">How it works</span><span class="lang-si">කොහොමද කරන්නේ?</span><span class="lang-fr">Fonctionnement</span></div>
<h1><span class="lang-en">THE MATRIX SYSTEM</span><span class="lang-si">මැට්‍රික්ස් ක්‍රමය</span><span class="lang-fr">LE SYSTÈME MATRIX</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">Platforms: Facebook, Instagram, TikTok, YouTube + your Website. Ceyteq setup & optimization <b>FREE</b> — you pay only a tiny ad budget directly to platforms.</span><span class="lang-si">Facebook, Instagram, TikTok, YouTube + Website. Ceyteq setup සහ optimization <b>නොමිලේ</b> — කුඩා ad මුදලක් platforms වලට පමණයි.</span><span class="lang-fr">Facebook, Instagram, TikTok, YouTube + votre site. Installation et optimisation Ceyteq <b>GRATUITES</b> — petit budget pub direct aux plateformes.</span></p>
</div>
<section><div class="grid">
<div class="card"><h3>🌅 <span class="lang-en">Morning Matrix • 6–11 AM</span><span class="lang-si">උදේ මැට්‍රික්ස් • 6–11</span><span class="lang-fr">Matrice du matin • 6h–11h</span></h3><p class="lang-en">Breakfast & lunch campaigns. Catch customers when they plan meals.</p><p class="lang-si">උදේ සහ දවල් customersලා ඉලක්ක කරගත් ප්‍රචාරණ.</p><p class="lang-fr">Campagnes petit-déjeuner et déjeuner. Captez les clients tôt.</p></div>
<div class="card"><h3>🌙 <span class="lang-en">Evening Matrix • 12–9 PM</span><span class="lang-si">හවස මැට්‍රික්ස් • 12–9</span><span class="lang-fr">Matrice du soir • 12h–21h</span></h3><p class="lang-en">Dinner & peak-hour push. Maximum visibility at maximum hours.</p><p class="lang-si">හවස peak hours වල උපරිම ප්‍රචාරණ.</p><p class="lang-fr">Dîner et heures de pointe. Visibilité maximale aux heures clés.</p></div>
<div class="card"><h3>💵 <span class="lang-en">Only $1–$2 / day ad spend</span><span class="lang-si">දවසට $1–$2 පමණයි</span><span class="lang-fr">Seulement 1–2 $/jour</span></h3><p class="lang-en">Paid by YOU directly to Meta/TikTok. Ceyteq optimization is free.</p><p class="lang-si">ඔබ platforms වලටම ගෙවන්න. Ceyteq optimization නොමිලේ.</p><p class="lang-fr">Payés par VOUS directement à Meta/TikTok. Optimisation offerte.</p></div>
<div class="card"><h3>🛠️ <span class="lang-en">We do the heavy lifting</span><span class="lang-si">බර වැඩ අපට</span><span class="lang-fr">On s'occupe de tout</span></h3><p class="lang-en">Setup, tuning, content matrix, analytics — handled by Team Creat.</p><p class="lang-si">Setup, tuning, content — සියල්ල අපි බලාගන්නවා.</p><p class="lang-fr">Installation, réglages, contenus — gérés par Team Creat.</p></div>
</div></section>
<section>
<div class="eyebrow"><span class="lang-en">Launch steps</span><span class="lang-si">පියවර</span><span class="lang-fr">Étapes</span></div>
<h2><span class="lang-en">From Zero to Live in 4 Steps</span><span class="lang-si">පියවර 4න් live</span><span class="lang-fr">En ligne en 4 étapes</span></h2>
<div class="timeline">
<div class="month"><div class="m"><span class="lang-en">STEP 1<br>Setup</span><span class="lang-si">පියවර 1<br>සැකසුම</span><span class="lang-fr">ÉTAPE 1<br>Install.</span></div><div class="d"><b class="lang-en">🔌 Connect everything</b><b class="lang-si">🔌 සියල්ල සම්බන්ධ කිරීම</b><b class="lang-fr">🔌 Tout connecter</b><p class="lang-en">Website + web panel + WhatsApp + bots connected to your business.</p><p class="lang-si">Website + panel + WhatsApp + bots සම්බන්ධ කරනවා.</p><p class="lang-fr">Site, panneau, WhatsApp et bots connectés à votre commerce.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">STEP 2<br>Launch</span><span class="lang-si">පියවර 2<br>ආරම්භය</span><span class="lang-fr">ÉTAPE 2<br>Lancement</span></div><div class="d"><b class="lang-en">🚀 Matrices go live</b><b class="lang-si">🚀 Campaign live</b><b class="lang-fr">🚀 Lancement</b><p class="lang-en">Morning + evening matrices launch with your $1–$2/day budget.</p><p class="lang-si">$1–$2/day සමඟ උදේ + හවස campaign live.</p><p class="lang-fr">Matrices matin + soir lancées avec 1–2 $/jour.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">STEP 3<br>Optimize</span><span class="lang-si">පියවර 3<br>Tuning</span><span class="lang-fr">ÉTAPE 3<br>Optimiser</span></div><div class="d"><b class="lang-en">📊 Weekly tuning</b><b class="lang-si">📊 සතිපතා tuning</b><b class="lang-fr">📊 Réglages hebdo</b><p class="lang-en">Real analytics drive precision tuning of every campaign.</p><p class="lang-si">Analytics බලලා හැම campaign එකම tuning කරනවා.</p><p class="lang-fr">Statistiques réelles et réglages précis de chaque campagne.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">STEP 4<br>Automate</span><span class="lang-si">පියවර 4<br>Automation</span><span class="lang-fr">ÉTAPE 4<br>Automatiser</span></div><div class="d"><b class="lang-en">🤖 Bots run sales</b><b class="lang-si">🤖 Bots විකුණුම් දුවවනවා</b><b class="lang-fr">🤖 Les bots vendent</b><p class="lang-en">Bots + AI handle orders, bookings and follow-ups 24/7.</p><p class="lang-si">Bots + AI orders, bookings 24/7 බලාගන්නවා.</p><p class="lang-fr">Bots et IA gèrent commandes et réservations 24/7.</p></div></div>
</div>

</section>
"""

# ================= TRAINING =================
TRAINING = """
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">Training & Support • 90 Days</span><span class="lang-si">පුහුණුව • දින 90</span><span class="lang-fr">Formation • 90 jours</span></div>
<h1><span class="lang-en">90-DAY PRACTICAL TRAINING</span><span class="lang-si">දින 90 ප්‍රායෝගික පුහුණුව</span><span class="lang-fr">FORMATION PRATIQUE 90 JOURS</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">Total duration: <b>3 months</b> — from foundation habits to full automation.</span><span class="lang-si">මුළු කාලය: <b>මාස 3</b> — අඩිතාලමේ සිට automation දක්වා.</span><span class="lang-fr">Durée totale : <b>3 mois</b> — des bases à l'automatisation.</span></p>
</div>
<section><div class="timeline">
<div class="month"><div class="m"><span class="lang-en">MONTH 1<br>Day-by-Day</span><span class="lang-si">මාස 1<br>දිනපතා</span><span class="lang-fr">MOIS 1<br>Quotidien</span></div><div class="d"><b class="lang-en">🏗️ Foundation</b><b class="lang-si">🏗️ අඩිතාලම</b><b class="lang-fr">🏗️ Fondations</b><p class="lang-en">Daily coaching: website & panel, WhatsApp bot orders, $1–$2 ads, promos, staff training.</p><p class="lang-si">දිනපතා පුහුණුව: panel, WhatsApp orders, ads, staff පුහුණුව.</p><p class="lang-fr">Coaching quotidien : panneau, commandes WhatsApp, pubs 1–2 $, promos, personnel.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">MONTH 2<br>Week-by-Week</span><span class="lang-si">මාස 2<br>සතිපතා</span><span class="lang-fr">MOIS 2<br>Hebdo</span></div><div class="d"><b class="lang-en">⚙️ Matrix Optimization</b><b class="lang-si">⚙️ ප්‍රශස්තකරණය</b><b class="lang-fr">⚙️ Optimisation</b><p class="lang-en">Weekly analytics review. Tune morning/evening matrices. Sync kitchen with demand.</p><p class="lang-si">සතිපතා විශ්ලේෂණය. Campaign tuning. Kitchen + digital sync.</p><p class="lang-fr">Analyse hebdo. Réglage des matrices. Cuisine synchronisée à la demande.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">MONTH 3<br>Growth</span><span class="lang-si">මාස 3<br>වර්ධනය</span><span class="lang-fr">MOIS 3<br>Croissance</span></div><div class="d"><b class="lang-en">👽 Alien-Level Growth & Automation</b><b class="lang-si">👽 වර්ධනය සහ automation</b><b class="lang-fr">👽 Croissance et automatisation</b><p class="lang-en">Full 90-day ROI & sales audit. AI tools + automation. Self-sustaining system.</p><p class="lang-si">ROI audit + AI automation. ස්වයංක්‍රීයව දුවන system එකක්.</p><p class="lang-fr">Audit ROI 90 jours, outils IA, système autonome.</p></div></div>
</div></section>
<section>
<div class="eyebrow"><span class="lang-en">Daily habits we install</span><span class="lang-si">දිනපතා පුරුදු</span><span class="lang-fr">Habitudes quotidiennes</span></div>
<h2><span class="lang-en">Your New Daily Rhythm</span><span class="lang-si">අලුත් දිනපතා ක්‍රමය</span><span class="lang-fr">Votre nouveau rythme</span></h2>
<ul class="check">
<li>☀️ <span class="lang-en">Check web panel orders</span><span class="lang-si">Panel orders බලන්න</span><span class="lang-fr">Vérifier les commandes</span></li>
<li>🤖 <span class="lang-en">Review bot chats & bookings</span><span class="lang-si">Bot chats සහ bookings බලන්න</span><span class="lang-fr">Vérifier bots et réservations</span></li>
<li>📣 <span class="lang-en">Confirm $1–$2 ads are live</span><span class="lang-si">Ads liveද කියා බලන්න</span><span class="lang-fr">Vérifier les pubs 1–2 $</span></li>
<li>🎁 <span class="lang-en">Post today's promo</span><span class="lang-si">අද promo එක දාන්න</span><span class="lang-fr">Publier la promo du jour</span></li>
<li>🌙 <span class="lang-en">Close the day & count online sales</span><span class="lang-si">Online විකුණුම් ගණන් කරන්න</span><span class="lang-fr">Compter les ventes en ligne</span></li>
</ul>
<div class="hlbox"><b class="lang-en">Outcome: trained staff, a self-running system, measurable ROI.</b><span class="lang-si">ප්‍රතිඵලය: පුහුණු staff, ස්වයංක්‍රීය system, මැනිය හැකි ROI.</span><span class="lang-fr">Résultat : équipe formée, système autonome, ROI mesurable.</span></div>

</section>
"""

# ================= PACKAGES =================
PACKAGES = """
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">Investment</span><span class="lang-si">මිල ගණන්</span><span class="lang-fr">Investissement</span></div>
<h1><span class="lang-en">4 PRICING TIERS</span><span class="lang-si">පැකේජ 4</span><span class="lang-fr">4 FORFAITS</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">Pick the tier that fits your budget — message us and we will recommend the right fit.</span><span class="lang-si">ඔබේ budget එකට ගැලපෙන එක තෝරන්න.</span><span class="lang-fr">Choisissez le forfait adapté à votre budget.</span></p>
</div>
<section>
<div class="pkg"><div class="pkg-head"><span class="num">01</span><h3>STARTER <small class="lang-en">Starter package</small><small class="lang-si">ආරම්භක පැකේජය</small><small class="lang-fr">Forfait de démarrage</small></h3></div>
<div class="pkg-body"><div class="price"><div><b>$19</b><span class="lang-en">ONE-TIME SETUP</span><span class="lang-si">එකවර සැකසුම් ගාස්තුව</span><span class="lang-fr">INSTALLATION UNIQUE</span></div><div><b>$3 – $5</b><span class="lang-en">MONTHLY FEE</span><span class="lang-si">මාසික ගාස්තුව</span><span class="lang-fr">FRAIS MENSUELS</span></div></div>
<ul class="feat">
<li><span class="lang-en">3–4 page custom website — brand colors/logo, mobile-responsive</span><span class="lang-si">පිටු 3–4 website — brand colors, ජංගම දුරකථනයට ගැලපෙන</span><span class="lang-fr">Site 3–4 pages, couleurs de marque, adapté aux mobiles</span></li>
<li><span class="lang-en">Direct WhatsApp ordering (no backend)</span><span class="lang-si">Orders කෙලින්ම WhatsApp එකට</span><span class="lang-fr">Commandes WhatsApp directes (sans back-office)</span></li>
<li><span class="lang-en">Monthly: <b>2 Videos + 4 Flyers</b></span><span class="lang-si">මාසෙට: <b>videos 2 + flyers 4</b></span><span class="lang-fr">Par mois : <b>2 vidéos + 4 flyers</b></span></li>
</ul></div></div>

<div class="pkg"><div class="pkg-head"><span class="num">02</span><h3>STANDARD <small class="lang-en">Standard package</small><small class="lang-si">සම්මත පැකේජය</small><small class="lang-fr">Forfait standard</small></h3><span class="pop"><span class="lang-en">★ MOST POPULAR</span><span class="lang-si">★ ජනප්‍රියම</span><span class="lang-fr">★ LE PLUS POPULAIRE</span></span></div>
<div class="pkg-body"><div class="price"><div><b>$60</b><span class="lang-en">ONE-TIME SETUP</span><span class="lang-si">එකවර සැකසුම් ගාස්තුව</span><span class="lang-fr">INSTALLATION UNIQUE</span></div></div>
<ul class="feat">
<li><span class="lang-en">Dynamic website + <b>Admin Panel</b> — booking/menu management</span><span class="lang-si">Dynamic website + <b>Admin Panel</b> — booking + menu කළමනාකරණය</span><span class="lang-fr">Site dynamique + <b>panneau admin</b> — réservations et menus</span></li>
<li><span class="lang-en">High customization — design matched to your brand</span><span class="lang-si">ඔබේ brand එකට ගැලපෙන design</span><span class="lang-fr">Haute personnalisation selon votre marque</span></li>
</ul>
<table class="tiers"><tr><th><span class="lang-en">Tier</span><span class="lang-si">මට්ටම</span><span class="lang-fr">Palier</span></th><th><span class="lang-en">Monthly</span><span class="lang-si">මාසික</span><span class="lang-fr">Mensuel</span></th><th><span class="lang-en">Content / month</span><span class="lang-si">මාසික content</span><span class="lang-fr">Contenu / mois</span></th></tr>
<tr><td><span class="lang-en">Tier 1</span><span class="lang-si">මට්ටම 1</span><span class="lang-fr">Palier 1</span></td><td><b><span class="lang-en">$10/mo</span><span class="lang-si">$10/මාස</span><span class="lang-fr">10 $/mois</span></b></td><td><span class="lang-en">3 Videos + 4 Flyers</span><span class="lang-si">වීඩියෝ 3 + ෆ්ලයර් 4</span><span class="lang-fr">3 vidéos + 4 flyers</span></td></tr>
<tr><td><span class="lang-en">Tier 2</span><span class="lang-si">මට්ටම 2</span><span class="lang-fr">Palier 2</span></td><td><b><span class="lang-en">$15/mo</span><span class="lang-si">$15/මාස</span><span class="lang-fr">15 $/mois</span></b></td><td><span class="lang-en">5 Videos + 7 Flyers</span><span class="lang-si">වීඩියෝ 5 + ෆ්ලයර් 7</span><span class="lang-fr">5 vidéos + 7 flyers</span></td></tr>
<tr><td><span class="lang-en">Tier 3</span><span class="lang-si">මට්ටම 3</span><span class="lang-fr">Palier 3</span></td><td><b><span class="lang-en">$20/mo</span><span class="lang-si">$20/මාස</span><span class="lang-fr">20 $/mois</span></b></td><td><span class="lang-en">7 Videos + 10 Flyers</span><span class="lang-si">වීඩියෝ 7 + ෆ්ලයර් 10</span><span class="lang-fr">7 vidéos + 10 flyers</span></td></tr></table></div></div>

<div class="pkg"><div class="pkg-head"><span class="num">03</span><h3>ADVANCED <small class="lang-en">Advanced package</small><small class="lang-si">උසස් පැකේජය</small><small class="lang-fr">Forfait avancé</small></h3></div>
<div class="pkg-body"><div class="price"><div><b>$80</b><span class="lang-en">ONE-TIME SETUP</span><span class="lang-si">එකවර සැකසුම් ගාස්තුව</span><span class="lang-fr">INSTALLATION UNIQUE</span></div></div>
<ul class="feat">
<li><span class="lang-en">Large-scale ecosystem — table/event bookings + <b>analytics dashboard</b></span><span class="lang-si">විශාල system — bookings + <b>analytics dashboard</b></span><span class="lang-fr">Écosystème complet — réservations + <b>tableau de bord</b></span></li>
<li><span class="lang-en"><b>FREE Messenger Chatbot</b> included</span><span class="lang-si"><b>නොමිලේ Messenger Bot</b></span><span class="lang-fr"><b>Bot Messenger GRATUIT</b> inclus</span></li>
<li><span class="lang-en">Optional Voice Caller Bot: <b>+$15/mo</b></span><span class="lang-si">Voice Caller Bot: <b>+$15/mo</b></span><span class="lang-fr">Bot vocal en option : <b>+15 $/mois</b></span></li>
</ul>
<table class="tiers"><tr><th><span class="lang-en">Tier</span><span class="lang-si">මට්ටම</span><span class="lang-fr">Palier</span></th><th><span class="lang-en">Monthly</span><span class="lang-si">මාසික</span><span class="lang-fr">Mensuel</span></th><th><span class="lang-en">Content / month</span><span class="lang-si">මාසික content</span><span class="lang-fr">Contenu / mois</span></th></tr>
<tr><td><span class="lang-en">Tier 1</span><span class="lang-si">මට්ටම 1</span><span class="lang-fr">Palier 1</span></td><td><b><span class="lang-en">$15/mo</span><span class="lang-si">$15/මාස</span><span class="lang-fr">15 $/mois</span></b></td><td><span class="lang-en">5 Videos + 7 Flyers</span><span class="lang-si">වීඩියෝ 5 + ෆ්ලයර් 7</span><span class="lang-fr">5 vidéos + 7 flyers</span></td></tr>
<tr><td><span class="lang-en">Tier 2</span><span class="lang-si">මට්ටම 2</span><span class="lang-fr">Palier 2</span></td><td><b><span class="lang-en">$20/mo</span><span class="lang-si">$20/මාස</span><span class="lang-fr">20 $/mois</span></b></td><td><span class="lang-en">7 Videos + 10 Flyers</span><span class="lang-si">වීඩියෝ 7 + ෆ්ලයර් 10</span><span class="lang-fr">7 vidéos + 10 flyers</span></td></tr>
<tr><td><span class="lang-en">Tier 3</span><span class="lang-si">මට්ටම 3</span><span class="lang-fr">Palier 3</span></td><td><b><span class="lang-en">$30/mo</span><span class="lang-si">$30/මාස</span><span class="lang-fr">30 $/mois</span></b></td><td><span class="lang-en">10 Videos + 15 Flyers</span><span class="lang-si">වීඩියෝ 10 + ෆ්ලයර් 15</span><span class="lang-fr">10 vidéos + 15 flyers</span></td></tr></table></div></div>

<div class="pkg"><div class="pkg-head"><span class="num">04</span><h3>PREMIUM ULTIMATE <small class="lang-en">Flagship package</small><small class="lang-si">ඉහළම පැකේජය</small><small class="lang-fr">Forfait phare</small></h3><span class="pop"><span class="lang-en">★ FLAGSHIP</span><span class="lang-si">★ විශේෂ</span><span class="lang-fr">★ PHARE</span></span></div>
<div class="pkg-body"><div class="price"><div><b>$250</b><span class="lang-en">ONE-TIME SETUP</span><span class="lang-si">එකවර සැකසුම් ගාස්තුව</span><span class="lang-fr">INSTALLATION UNIQUE</span></div><div><b>$150</b><span class="lang-en">FLAT MONTHLY FEE</span><span class="lang-si">ස්ථාවර මාසික ගාස්තුව</span><span class="lang-fr">FORFAIT MENSUEL</span></div></div>
<ul class="feat">
<li><span class="lang-en">100% fully custom design — <b>3D visuals</b>, complete backend control</span><span class="lang-si">100% custom design — <b>3D visuals</b>, සම්පූර්ණ backend control</span><span class="lang-fr">Design 100% sur mesure — <b>visuels 3D</b>, contrôle total</span></li>
<li><span class="lang-en"><b>Dual Bot System:</b> Text Bot + Voice Caller Bot</span><span class="lang-si"><b>Dual Bot:</b> Text Bot + Voice Bot</span><span class="lang-fr"><b>Double bot :</b> texte + vocal</span></li>
<li><span class="lang-en">Monthly: <b>15 Videos + 25 Flyers</b></span><span class="lang-si">මාසෙට: <b>videos 15 + flyers 25</b></span><span class="lang-fr">Par mois : <b>15 vidéos + 25 flyers</b></span></li>
<li><span class="lang-en">Cross-platform marketing + <b>exclusive external ad placements</b></span><span class="lang-si">Cross-platform + <b>external ad placements</b></span><span class="lang-fr">Marketing multi-plateformes + <b>placements externes exclusifs</b></span></li>
</ul></div></div>

<div class="hlbox"><b class="lang-en">All packages: only $1–$2/day ad spend direct to platforms. Ceyteq optimization = FREE.</b><span class="lang-si">සියලු පැකේජ: දවසට $1–$2 platforms වලට පමණයි. Ceyteq optimization නොමිලේ.</span><span class="lang-fr">Tous forfaits : seulement 1–2 $/jour aux plateformes. Optimisation Ceyteq GRATUITE.</span></div>
</section>

<section>
<div class="eyebrow"><span class="lang-en">Package questions</span><span class="lang-si">පැකේජ ප්‍රශ්න</span><span class="lang-fr">Questions forfaits</span></div>
<h2><span class="lang-en">Package Questions</span><span class="lang-si">පැකේජ ගැන ප්‍රශ්න</span><span class="lang-fr">Questions sur les forfaits</span></h2>
<details open><summary><span class="lang-en">🍽️ Which package fits a small restaurant?</span><span class="lang-si">🍽️ කුඩා restaurant එකකට ගැලපෙන්නේ?</span><span class="lang-fr">🍽️ Quel forfait pour un petit restaurant ?</span></summary><p class="lang-en">Starter ($19) is the perfect first step with WhatsApp ordering. Standard ($60) is most popular for booking + menu management. Message us — we'll recommend the right fit.</p><p class="lang-si">Starter ($19) පළමු පියවරට හොඳයි. Standard ($60) booking + menu සඳහා ජනප්‍රියම. අපට message කරන්න — ගැලපෙන එක කියන්නම්.</p><p class="lang-fr">Starter (19 $) pour débuter avec commandes WhatsApp. Standard (60 $) le plus choisi pour réservations et menus. Écrivez-nous pour un conseil.</p></details>
<details><summary><span class="lang-en">📦 What does the monthly fee include?</span><span class="lang-si">📦 මාසික ගාස්තුවෙන් ලැබෙන්නේ?</span><span class="lang-fr">📦 Que comprend le mensuel ?</span></summary><p class="lang-en">Fresh videos + flyers every month per your tier, published across Facebook, Instagram, TikTok, YouTube + website.</p><p class="lang-si">හැම මාසෙම tier එකට අනුව අලුත් videos + flyers — FB, IG, TikTok, YT + website.</p><p class="lang-fr">Nouvelles vidéos + flyers chaque mois selon votre palier, publiés sur FB, IG, TikTok, YT + site.</p></details>
<details><summary><span class="lang-en">🤖 Is the chatbot really free?</span><span class="lang-si">🤖 Chatbot නොමිලේද?</span><span class="lang-fr">🤖 Le bot est-il vraiment gratuit ?</span></summary><p class="lang-en">Yes — Advanced includes a FREE Messenger Chatbot. Voice Caller Bot is +$15/mo. Premium Ultimate includes both bots.</p><p class="lang-si">ඔව් — Advanced සමඟ නොමිලේ Messenger Bot. Voice Bot +$15/mo. Premium සමඟ දෙකම.</p><p class="lang-fr">Oui — Advanced inclut le bot Messenger GRATUIT. Bot vocal +15 $/mois. Premium inclut les deux.</p></details>
</section>
"""

# ================= AI =================
AI = """
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">AI Solutions</span><span class="lang-si">AI විසඳුම්</span><span class="lang-fr">Solutions IA</span></div>
<h1><span class="lang-en">AI TODAY & TOMORROW</span><span class="lang-si">අද සහ හෙට AI</span><span class="lang-fr">L'IA AUJOURD'HUI ET DEMAIN</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">Current AI usage in business — and the future solutions coming in the Digital Race roadmap.</span><span class="lang-si">ව්‍යාපාරවල දැනට AI භාවිතය — සහ ඉදිරියේ එන විසඳුම්.</span><span class="lang-fr">L'usage actuel de l'IA en entreprise — et les solutions à venir.</span></p>
</div>
<section><div class="grid">
<div class="card"><h3>💬 <span class="lang-en">Today: WhatsApp & Messenger Bots</span><span class="lang-si">අද: WhatsApp සහ Messenger Bots</span><span class="lang-fr">Aujourd'hui : Bots WhatsApp et Messenger</span></h3><p class="lang-en">Auto orders, bookings & instant replies 24/7. Never miss a customer.</p><p class="lang-si">Auto orders සහ replies 24/7. Customer කෙනෙක්වත් මගහැරෙන්නේ නෑ.</p><p class="lang-fr">Commandes, réservations et réponses auto 24/7. Aucun client perdu.</p></div>
<div class="card"><h3>📞 <span class="lang-en">Today: Voice Caller Bot</span><span class="lang-si">අද: Voice Caller Bot</span><span class="lang-fr">Aujourd'hui : Bot vocal</span></h3><p class="lang-en">AI answers calls, confirms orders & bookings in your business voice.</p><p class="lang-si">AI calls වලට උත්තර දී orders තහවුරු කරනවා.</p><p class="lang-fr">L'IA répond aux appels et confirme commandes et réservations.</p></div>
<div class="card"><h3>🔮 <span class="lang-en">Tomorrow: Full AI Automation</span><span class="lang-si">හෙට: සම්පූර්ණ AI Automation</span><span class="lang-fr">Demain : automatisation totale</span></h3><p class="lang-en">Sales forecasts, smart promos, self-running campaigns.</p><p class="lang-si">විකුණුම් පුරෝකථන, smart promos, ස්වයංක්‍රීය campaign.</p><p class="lang-fr">Prévisions de ventes, promos intelligentes, campagnes autonomes.</p></div>
<div class="card"><h3>🏪 <span class="lang-en">How businesses use it</span><span class="lang-si">ව්‍යාපාර භාවිතා කරන හැටි</span><span class="lang-fr">Usages en entreprise</span></h3><p class="lang-en">Order-taking, table booking, follow-ups, reviews, repeat promos — automated.</p><p class="lang-si">Orders, bookings, follow-ups, reviews — සියල්ල ස්වයංක්‍රීයව.</p><p class="lang-fr">Commandes, réservations, relances, avis — tout automatisé.</p></div>
</div></section>
<section>
<div class="eyebrow"><span class="lang-en">Roadmap</span><span class="lang-si">ඉදිරි මාවත</span><span class="lang-fr">Feuille de route</span></div>
<h2><span class="lang-en">The AI Road Ahead</span><span class="lang-si">ඉදිරි AI මාවත</span><span class="lang-fr">La route de l'IA</span></h2>
<div class="timeline">
<div class="month"><div class="m"><span class="lang-en">NOW</span><span class="lang-si">දැන්</span><span class="lang-fr">MAINTENANT</span></div><div class="d"><b class="lang-en">💬 Bots handle orders & chats</b><b class="lang-si">💬 Bots orders සහ chats බලනවා</b><b class="lang-fr">💬 Les bots gèrent commandes et chats</b><p class="lang-en">WhatsApp + Messenger automation live from Month 1.</p><p class="lang-si">1 වන මාසයේ සිට WhatsApp + Messenger automation.</p><p class="lang-fr">Automatisation WhatsApp + Messenger dès le 1er mois.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">NEXT</span><span class="lang-si">ඊළඟට</span><span class="lang-fr">ENSUITE</span></div><div class="d"><b class="lang-en">📞 Voice AI + smart promos</b><b class="lang-si">📞 Voice AI + smart promos</b><b class="lang-fr">📞 IA vocale + promos intelligentes</b><p class="lang-en">Voice Caller Bot + demand-based smart promotions.</p><p class="lang-si">Voice Caller Bot + smart promos.</p><p class="lang-fr">Bot vocal + promotions intelligentes selon la demande.</p></div></div>
<div class="month"><div class="m"><span class="lang-en">FUTURE</span><span class="lang-si">අනාගතය</span><span class="lang-fr">FUTUR</span></div><div class="d"><b class="lang-en">🚀 Self-driving marketing</b><b class="lang-si">🚀 ස්වයංක්‍රීය marketing</b><b class="lang-fr">🚀 Marketing autopiloté</b><p class="lang-en">Forecasts, auto-budgets and campaigns that run themselves.</p><p class="lang-si">පුරෝකථන සහ තනිවම දුවන campaign.</p><p class="lang-fr">Prévisions et campagnes entièrement autonomes.</p></div></div>
</div>

</section>
"""

# ================= ADMIN =================
ADMIN = """
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">Admin Panel</span><span class="lang-si">පරිපාලක පුවරුව</span><span class="lang-fr">Panneau d'administration</span></div>
<h1><span class="lang-en">ADMIN LOGIN</span><span class="lang-si">පරිපාලක පිවිසුම</span><span class="lang-fr">CONNEXION ADMIN</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">Manage the Flyers database (Google Sheet). Other website content stays fixed.</span><span class="lang-si">Flyers database (Google Sheet) කළමනාකරණය. අනිත් website content ස්ථිරයි.</span><span class="lang-fr">Gérez la base Flyers (Google Sheet). Le reste du site est fixe.</span></p>
</div>
<section>
<div id="loginBox" class="login-wrap">
<div style="font-size:42px">\U0001f510</div>
<h3><span class="lang-en">Admin Login</span><span class="lang-si">පරිපාලක පිවිසුම</span><span class="lang-fr">Connexion admin</span></h3>
<input id="auser" autocomplete="username" placeholder="Username">
<input id="apass" type="password" autocomplete="current-password" placeholder="Password">
<div><button class="btn btn-navy" onclick="doLogin()"><span class="lang-en">Login</span><span class="lang-si">ඇතුළු වන්න</span><span class="lang-fr">Se connecter</span></button></div>
<div id="aerr" class="login-err"></div>
</div>
<div id="dashBox" style="display:none">
<div class="card"><h3>\U0001f4ca <span class="lang-en">Database Status</span><span class="lang-si">Database තත්ත්වය</span><span class="lang-fr">État de la base</span></h3>
<p><span id="sheetStatus">…</span> <b id="sheetCount"></b></p>
<div class="cta-row" style="justify-content:flex-start"><a class="btn btn-cyan" href="__EDIT_URL__" target="_blank">\U0001f4dd <span class="lang-en">Open Google Sheet</span><span class="lang-si">Google Sheet අරින්න</span><span class="lang-fr">Ouvrir Google Sheet</span></a>
<a class="btn btn-ghost" href="flyers.html"><span class="lang-en">View Flyers page</span><span class="lang-si">Flyers පිටුව බලන්න</span><span class="lang-fr">Voir la page Flyers</span></a>
<a class="btn btn-ghost" href="#" onclick="doLogout();return false;"><span class="lang-en">Logout</span><span class="lang-si">ඉවත් වන්න</span><span class="lang-fr">Déconnexion</span></a></div></div>
<h2 style="margin-top:26px"><span class="lang-en">Live Flyers Table</span><span class="lang-si">සජීවී Flyers වගුව</span><span class="lang-fr">Table Flyers en direct</span></h2>
<div style="overflow-x:auto"><table class="dash-table" id="dashTable"><thead><tr><th>#</th><th>File</th><th>EN</th><th>SI</th><th>FR</th><th><span class="lang-en">Visible</span><span class="lang-si">පෙන්වන</span><span class="lang-fr">Visible</span></th></tr></thead><tbody><tr><td colspan="6">…</td></tr></tbody></table></div>
<h2 style="margin-top:26px"><span class="lang-en">Setup Guide</span><span class="lang-si">සැකසුම් මාර්ගෝපදේශය</span><span class="lang-fr">Guide d'installation</span></h2>
<ol class="steps">
<li><span class="lang-en">Open the Google Sheet and use the first tab. First row must be:</span><span class="lang-si">Google Sheet අරින්න. පළමු පේළිය මෙසේ විය යුතුයි:</span><span class="lang-fr">Ouvrez Google Sheet. La première ligne doit être :</span><br><code class="k">file | title_en | title_si | title_fr | visible</code></li>
<li><span class="lang-en">Copy the block below, select cell A1 in the Sheet, paste. (10 rows ready.)</span><span class="lang-si">පහළ කොටුව copy කර Sheet එකේ A1 තෝරා paste කරන්න. (පේළි 10 සූදානම්.)</span><span class="lang-fr">Copiez le bloc ci-dessous, sélectionnez A1, collez. (10 lignes prêtes.)</span></li>
<li><span class="lang-en">To hide a flyer set visible = NO. To reorder, drag rows. To add, append a row.</span><span class="lang-si">Flyer එකක් හංගන්න visible = NO. අනුපිළිවෙලට rows අදින්න. අලුත් එකක් පහළට එකතු කරන්න.</span><span class="lang-fr">Pour masquer : visible = NO. Réordonnez les lignes. Ajoutez en bas.</span></li>
<li><span class="lang-en">Sharing is ON (Anyone with link = Viewer). Changes appear on the Flyers page automatically (~1 min, needs internet).</span><span class="lang-si">Sharing ON (link එකෙන් Viewer). වෙනස්කම් Flyers පිටුවේ ස්වයංක්‍රීයව පෙනේ (~මිනිත්තුවයි, internet අවශ්‍යයි).</span><span class="lang-fr">Partage ACTIF (lecteur via lien). Modifications auto sur Flyers (~1 min, internet requis).</span></li>
</ol>
<textarea class="tsv" id="tsvBox" readonly rows="12" onclick="this.select()">__TSV__</textarea>
<div class="cta-row" style="justify-content:flex-start"><button class="btn btn-navy" onclick="copyTSV()"><span class="lang-en">Copy rows</span><span class="lang-si">පේළි copy කරන්න</span><span class="lang-fr">Copier</span></button></div>
<div class="hlbox"><b class="lang-en">Note: this login is a front-end lock for a static website.</b><span class="lang-si">සටහන: මෙය static website එකක front-end lock එකකි.</span><span class="lang-fr">Note : verrou frontal pour site statique.</span></div>
</div>
</section>
<script>
var ADMIN_SIG='__ADMIN_SIG__';
var SHEET_ID='__SHEET_ID__';
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function LM(){return document.body.getAttribute('data-langmode')||'si'}
function T(si,en,fr){var m=LM();return m==='si'?si:(m==='fr'?fr:en)}
function showDash(s){document.getElementById('loginBox').style.display=s?'none':'block';document.getElementById('dashBox').style.display=s?'block':'none';if(s)loadSheet()}
function doLogin(){var u=document.getElementById('auser').value.trim();var p=document.getElementById('apass').value;
var sig='';try{sig=btoa(unescape(encodeURIComponent(u+'::'+p)))}catch(e){sig=''}
if(sig&&sig===ADMIN_SIG){try{sessionStorage.setItem('ceyteq_admin','1')}catch(e){}document.getElementById('aerr').textContent='';showDash(true)}
else{document.getElementById('aerr').textContent=T('වැරදි username හෝ password','Invalid username or password','Identifiants invalides')}}
function doLogout(){try{sessionStorage.removeItem('ceyteq_admin')}catch(e){}showDash(false)}
function copyTSV(){var t=document.getElementById('tsvBox');t.select();try{document.execCommand('copy')}catch(e){}}
function loadSheet(){
var st=document.getElementById('sheetStatus'),ct=document.getElementById('sheetCount'),tb=document.querySelector('#dashTable tbody');
st.innerHTML=T('සම්බන්ධ වෙමින්…','Connecting…','Connexion…');ct.textContent='';
fetch('https://docs.google.com/spreadsheets/d/'+SHEET_ID+'/gviz/tq?tqx=out:json&gid=0').then(function(r){if(!r.ok)throw 0;return r.text()}).then(function(t){
var m=t.match(/google\.visualization\.Query\.setResponse\(([\s\S]+?)\);?\s*$/);if(!m)throw 0;
var d=JSON.parse(m[1]);var rows=((d.table||{}).rows||[]).map(function(r){return (r.c||[]).map(function(c){return c&&c.v!==null&&c.v!==undefined?String(c.v):''})});
if(!rows.length){st.innerHTML='<span class="pill-no">EMPTY</span> '+T('Sheet හිස්යි — පහළ rows paste කරන්න.','Sheet is empty — paste the rows below.','Feuille vide — collez les lignes.');tb.innerHTML='';return}
var s=0;if(rows[0]&&/^file$/i.test((rows[0][0]||'').trim()))s=1;
var h='',n=0;
for(var i=s;i<rows.length;i++){var r=rows[i];if(!(r[0]||'').trim())continue;n++;
var v=(r[4]||'').toString().trim().toLowerCase();
var hid=(v==='no'||v==='false'||v==='0'||v==='hide'||v==='hidden'||v==='off');
h+='<tr><td>'+n+'</td><td><code class="k">'+esc(r[0])+'</code></td><td>'+esc(r[1]||'')+'</td><td>'+esc(r[2]||'')+'</td><td>'+esc(r[3]||'')+'</td><td>'+(hid?'<span class="pill-no">NO</span>':'<span class="pill-ok">YES</span>')+'</td></tr>'}
if(!n){st.innerHTML='<span class="pill-no">EMPTY</span>';tb.innerHTML='';return}
st.innerHTML='<span class="pill-ok">CONNECTED</span>';ct.textContent=' • '+n+' rows';
tb.innerHTML=h;
}).catch(function(){st.innerHTML='<span class="pill-no">OFFLINE</span> '+T('Sheet වෙත ළඟා විය නොහැක — internet / sharing බලන්න.','Cannot reach Sheet — check internet / sharing.','Sheet inaccessible — vérifiez internet / partage.');tb.innerHTML=''})}
(function(){try{if(sessionStorage.getItem('ceyteq_admin')==='1')showDash(true)}catch(e){}})();
document.getElementById('apass').addEventListener('keydown',function(e){if(e.key==='Enter')doLogin()});
document.getElementById('auser').addEventListener('keydown',function(e){if(e.key==='Enter')doLogin()});
</script>
"""

# ================= FLYERS =================
def fig(n, slug, en, si, fr):
    return f'<figure><img src="flyers/flyer-{n:02d}-{slug}.png" alt="{en}"><figcaption>{n:02d} • <span class="lang-en">{en}</span><span class="lang-si">{si}</span><span class="lang-fr">{fr}</span></figcaption></figure>'

FLYERS = f"""
<div class="pagehero">
<div class="eyebrow"><span class="lang-en">Flyer Pack</span><span class="lang-si">ෆ්ලයර් කට්ටලය</span><span class="lang-fr">Pack flyers</span></div>
<h1><span class="lang-en">10 FLYERS, READY TO SHARE</span><span class="lang-si">SHARE කිරීමට ෆ්ලයර් 10</span><span class="lang-fr">10 FLYERS PRÊTS À PARTAGER</span></h1>
<p class="lead" style="margin:10px auto"><span class="lang-en">One per topic & package — send any single flyer, or share this site link for full details. Post 1/day on FB + IG + TikTok + YT.</span><span class="lang-si">මාතෘකාව සහ පැකේජයට එක බැගින් — WhatsApp, FB, IG, TikTok වල share කරන්න.</span><span class="lang-fr">Un par sujet et forfait — partagez sur WhatsApp, FB, IG, TikTok.</span></p>
</div>
<section><div class="gallery" id="flyerGallery">
{fig(1,'program-intro','Program Intro','වැඩසටහන','Intro')}
{fig(2,'why-now','Why Now','ඇයි දැන්ම','Pourquoi maintenant')}
{fig(3,'what-changes','What Changes','වෙනස','Changements')}
{fig(4,'how-it-works','How It Works','ක්‍රමය','Système')}
{fig(5,'training-90-day','90-Day Training','පුහුණුව','Formation')}
{fig(6,'package-starter','Starter $19','ආරම්භක','Starter 19 $')}
{fig(7,'package-standard','Standard $60','සම්මත','Standard 60 $')}
{fig(8,'package-advanced','Advanced $80','උසස්','Avancé 80 $')}
{fig(9,'package-premium','Premium $250','ඉහළම','Premium 250 $')}
{fig(10,'ai-future-contact','AI + Contact','AI + සම්බන්ධය','IA + Contact')}
</div>
{ADMIN_LINK}
__FLYER_JS__

</section>
"""

PAGES = [
    ('index.html', 'CEYTEQ Digital Race — Home | මුල් පිටුව | Accueil', 'index.html', HOME),
    ('system.html', 'Digital Race — System | ක්‍රමය | Système', 'system.html', SYSTEM),
    ('training.html', 'Digital Race — Training | පුහුණුව | Formation', 'training.html', TRAINING),
    ('packages.html', 'Digital Race — Packages | පැකේජ | Forfaits', 'packages.html', PACKAGES),
    ('ai.html', 'Digital Race — AI | AI විසඳුම් | IA', 'ai.html', AI),
    ('flyers.html', 'Digital Race — Flyers | ෆ්ලයර් | Flyers', 'flyers.html', FLYERS),
    ('admin.html', 'Ceyteq Admin | පරිපාලක | Admin', 'admin.html', ADMIN),
]

for fname, title, active, body in PAGES:
    if fname not in ('index.html', 'admin.html'):
        body = body + explore_more(active)
    body = body.replace('__FLYER_JS__', LOADER_JS).replace('__SHEET_ID__', SHEET_ID).replace('__EDIT_URL__', SHEET_EDIT_URL).replace('__ADMIN_SIG__', ADMIN_SIG).replace('__TSV__', TSV_DATA)
    html = page(title, active, body, contact=(fname not in ('index.html', 'admin.html')), fname=fname)
    assert '__' not in html.replace('data-langmode', ''), fname
    with open(f'{ROOT}/{fname}', 'w') as f:
        f.write(html)
    print(fname, len(html)//1024, 'KB')
print('BUILD OK')
