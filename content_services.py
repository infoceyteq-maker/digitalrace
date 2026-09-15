#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEYTEQ — Ceylon Technology : main website content (services 01–08).
Imported by build_site.py. Pure data + small HTML helpers — no build logic here.

Trilingual rule: every visible label has lang-en / lang-si / lang-fr spans.
Brand names, platform names and numbers stay universal (no translation).
Edit any text below and run:  python3 build_site.py
"""

import content_hotelmate as HM   # featured-partner campaign layer (additive)


# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------


def T(en, si, fr):
    """Three sibling language spans (the pattern the whole site uses)."""
    return (f'<span class="lang-en">{en}</span>'
            f'<span class="lang-si">{si}</span>'
            f'<span class="lang-fr">{fr}</span>')


def hero(eyebrow_en, eyebrow_si, eyebrow_fr, h1_en, h1_si, h1_fr, lead_en, lead_si, lead_fr):
    return f"""<div class="pagehero">
<div class="eyebrow">{T(eyebrow_en, eyebrow_si, eyebrow_fr)}</div>
<h1>{T(h1_en, h1_si, h1_fr)}</h1>
<p class="lead" style="margin:10px auto">{T(lead_en, lead_si, lead_fr)}</p>
</div>"""


def blk(title_en, title_si, title_fr, items=None, note_en='', note_si='', note_fr='', links=None):
    """A titled white block with optional chip list (universal names) + note."""
    out = [f'<div class="blk"><h3>{T(title_en, title_si, title_fr)}</h3>']
    if note_en:
        out.append(f'<p class="note">{T(note_en, note_si, note_fr)}</p>')
    if items:
        out.append('<div class="chips">' + ''.join(f'<span>{i}</span>' for i in items) + '</div>')
    if links:
        out.append('<div class="cta-row" style="justify-content:flex-start;margin:16px 0 0">'
                   + ''.join(links) + '</div>')
    out.append('</div>')
    return '\n'.join(out)


def quote_cta(text_en='Get a free quote on WhatsApp', text_si='නොමිලේ මිල ගණන් WhatsApp එකෙන්',
              text_fr='Devis gratuit sur WhatsApp', wa='94788607143'):
    return (f'<div class="cta-row" style="margin-top:26px">'
            f'<a class="btn btn-cyan" href="https://wa.me/{wa}" target="_blank">💬 {T(text_en, text_si, text_fr)}</a>'
            f'<a class="btn btn-ghost" href="contact.html">📩 {T("Send an enquiry", "විමසුමක් යවන්න", "Envoyer une demande")}</a>'
            f'</div>')


def svc_card(s):
    return f"""<a class="svc" href="{s['f']}">
<div class="ico">{s['icon']}</div>
<div class="no">{s['n']} • {T(s['tag_en'], s['tag_si'], s['tag_fr'])}</div>
<h3>{T(s['en'], s['si'], s['fr'])}</h3>
<p>{T(s['desc_en'], s['desc_si'], s['desc_fr'])}</p>
<ul>{''.join(f'<li>{i}</li>' for i in s['items'][:4])}</ul>
<div class="go">{T('Open ' + s['en'] + ' →', s['si'] + ' බලන්න →', 'Voir ' + s['fr'] + ' →')}</div>
</a>"""


# ----------------------------------------------------------------------------
# 08 service divisions (01–08) — the main menu / hub data
# ----------------------------------------------------------------------------

SERVICES = [
    dict(f='web.html', n='01', icon='🌐',
         tag_en='Division 01', tag_si='අංශය 01', tag_fr='Division 01',
         en='Web Services', si='වෙබ් සේවා', fr='Services web',
         desc_en='Web platform creation & optimization, e-commerce, SEO, Google Business Profile and every social channel connected and managed for you.',
         desc_si='වෙබ් පද්ධති නිර්මාණය හා ප්‍රශස්තකරණය, e-commerce, SEO, Google Business Profile සහ හැම social channel එකක්ම ඔබ වෙනුවෙන් සකසා කළමනාකරණය.',
         desc_fr='Création et optimisation de plateformes web, e-commerce, SEO, Google Business Profile et gestion de tous vos réseaux sociaux.',
         items=['Website', 'E-Commerce', 'SEO', 'Google Business Profile', 'Booking channels', 'Social networks']),
    dict(f='ads.html', n='02', icon='📣',
         tag_en='Division 02', tag_si='අංශය 02', tag_fr='Division 02',
         en='Advertising', si='ප්‍රචාරණ', fr='Publicité',
         desc_en='Social media ad campaigns, Google Ads, YouTube promotions and web traffic campaigns that bring real customers.',
         desc_si='Social media ad campaigns, Google Ads, YouTube ප්‍රචාරණ සහ web traffic campaigns — ඇත්ත customers ගෙනෙන ප්‍රචාරණ.',
         desc_fr='Campagnes publicitaires sociales, Google Ads, promotions YouTube et campagnes de trafic web qui amènent de vrais clients.',
         items=['Facebook Ads', 'Instagram Ads', 'TikTok Ads', 'Google Ads', 'YouTube', 'Web traffic']),
    dict(f='print.html', n='03', icon='🖨️',
         tag_en='Division 03', tag_si='අංශය 03', tag_fr='Division 03',
         en='Printing & Digital', si='මුද්‍රණ හා ඩිජිටල්', fr='Impression & Digital',
         desc_en='Offset printing, packaging, business cards, menus, posters, digital LED boards, signage, paper bags, food packing and merchandise.',
         desc_si='Offset මුද්‍රණ, packaging, business cards, menu, poster, digital LED board, signage, paper bag, food packing සහ merchandise.',
         desc_fr='Impression offset, emballage, cartes de visite, menus, affiches, panneaux LED, signalétique, sacs en papier et produits dérivés.',
         items=['Offset printing', 'Packaging', 'Signage & LED', 'Paper bags', 'T-shirts & caps', 'Menu books']),
    dict(f='media.html', n='04', icon='📸',
         tag_en='Division 04', tag_si='අංශය 04', tag_fr='Division 04',
         en='Photography & Video', si='ඡායාරූප හා වීඩියෝ', fr='Photo & Vidéo',
         desc_en='Professional photography and videography for events, weddings, cultural events, products, business places and marketing content.',
         desc_si='Event, මංගල උත්සව, සංස්කෘතික උත්සව, products, ව්‍යාපාරික ස්ථාන සහ marketing content සඳහා වෘත්තීය ඡායාරූප හා වීඩියෝ.',
         desc_fr='Photographie et vidéo professionnelles pour événements, mariages, événements culturels, produits et locaux commerciaux.',
         items=['Events', 'Weddings', 'Product shoots', 'Business places', 'Reels & shorts', 'Drone-ready']),
    dict(f='design.html', n='05', icon='🎨',
         tag_en='Division 05', tag_si='අංශය 05', tag_fr='Division 05',
         en='Design & Editing', si='නිර්මාණ හා එඩිටින්', fr='Design & Montage',
         desc_en='Graphic design, photo editing, flyer and poster design, video editing and film production for your brand.',
         desc_si='Graphic design, photo editing, flyer හා poster නිර්මාණ, video editing සහ film නිර්මාණ — ඔබේ brand එකට.',
         desc_fr='Design graphique, retouche photo, création de flyers et affiches, montage vidéo et production de films pour votre marque.',
         items=['Photo editing', 'Graphic design', 'Flyer design', 'Poster design', 'Video editing', 'Filming']),
    dict(f='ai.html', n='06', icon='🤖',
         tag_en='Division 06', tag_si='අංශය 06', tag_fr='Division 06',
         en='AI & ERP', si='AI හා ERP', fr='IA & ERP',
         desc_en='AI integration consulting, ERP for hospitality & retail, AI customer care, CRM automation and AI messaging robots.',
         desc_si='AI integration consulting, hospitality හා retail සඳහා ERP, AI customer care, CRM automation සහ AI messaging robots.',
         desc_fr='Conseil en intégration IA, ERP pour l’hôtellerie et le commerce, service client IA, automatisation CRM et robots de messagerie IA.',
         items=['AI chatbots', 'Voice bots', 'CRM automation', 'Hospitality ERP', 'Retail ERP', 'AI consulting']),
    dict(f='travel.html', n='07', icon='✈️',
         tag_en='Division 07', tag_si='අංශය 07', tag_fr='Division 07',
         en='Ceylon Voyage', si='Ceylon Voyage', fr='Ceylon Voyage',
         desc_en='Travel division with Sri Lanka and France offices: itinerary planning, hotel & vehicle bookings, tickets and tourist information.',
         desc_si='ශ්‍රී ලංකා සහ ප්‍රංශ කාර්යාල සහිත සංචාරක අංශය: itinerary සැලසුම්, hotel හා වාහන bookings, tickets සහ සංචාරක තොරතුරු.',
         desc_fr='Division voyage avec bureaux au Sri Lanka et en France : itinéraires, réservations d’hôtels et de véhicules, billets et informations touristiques.',
         items=['Itineraries', 'Hotel booking', 'Vehicle booking', 'Event tickets', 'Air tickets', 'Tour guide']),
    dict(f='careers.html', n='08', icon='🤝',
         tag_en='Division 08', tag_si='අංශය 08', tag_fr='Division 08',
         en='Careers', si='රැකියා අවස්ථා', fr='Carrières',
         desc_en='Join the Ceyteq team — marketing, development, design, media and travel roles, plus internships.',
         desc_si='Ceyteq කණ්ඩායමට එකතු වන්න — marketing, development, design, media සහ travel රැකියා, internship සමඟ.',
         desc_fr='Rejoignez l’équipe Ceyteq — marketing, développement, design, médias et voyage, ainsi que des stages.',
         items=['Marketing', 'Development', 'Design', 'Videography', 'Internships', 'Part-time']),
]

# Locked prices (never alter — README «PRICE LOCK»). Compact table used on the
# web / advertising service pages; the full package detail lives on packages.html.
PACKAGES_TABLE = """<table class="tiers">
<tr><th>Package</th><th>One-time</th><th>Monthly</th><th>Content / month</th></tr>
<tr><td><b>Starter</b></td><td><b>$19</b></td><td>$3–$5</td><td>2 Videos + 4 Flyers</td></tr>
<tr><td><b>Standard</b> ★</td><td><b>$60</b></td><td>$10 / $15 / $20</td><td>3–7 Videos + 4–10 Flyers</td></tr>
<tr><td><b>Advanced</b></td><td><b>$80</b></td><td>$15 / $20 / $30</td><td>5–10 Videos + 7–15 Flyers</td></tr>
<tr><td><b>Premium Ultimate</b></td><td><b>$250</b></td><td>$150 flat</td><td>Full ecosystem + AI</td></tr>
</table>
<p class="note" style="margin-top:10px"><span class="lang-en">Client ad spend of $1–$2/day is paid directly to Meta/Google. Ceyteq optimization is FREE. Full details on the <a href="packages.html">Packages</a> page.</span><span class="lang-si">දවසට $1–$2 ad මුදල Meta/Google වලට කෙලින්ම ගෙවනවා. Ceyteq optimization නොමිලේ. සම්පූර්ණ විස්තර <a href="packages.html">Packages</a> පිටුවේ.</span><span class="lang-fr">1–2 $/jour de pub payés directement à Meta/Google. Optimisation Ceyteq GRATUITE. Détails sur la page <a href="packages.html">Forfaits</a>.</span></p>"""


# universal platform list (brand names — no translation needed, per site rules)
PLATFORMS = ['Facebook', 'Instagram', 'TikTok', 'X (Twitter)', 'Pinterest', 'Reddit', 'Threads',
             'LinkedIn', 'WhatsApp Business', 'WhatsApp Channel', 'Telegram', 'YouTube',
             'Google Business Profile', 'Apple Maps', 'SEO', 'Email']
BOOKING_CHANNELS = ['Booking.com', 'Airbnb', 'Agoda', 'Expedia', 'HostelWorld', 'TripAdvisor', 'PikMe', 'Uber']


# ----------------------------------------------------------------------------
# HOME
# ----------------------------------------------------------------------------

def home():
    cards = ''.join(svc_card(s) for s in SERVICES)
    return f"""
<div class="hero">
<img class="main-logo" src="__LOGO__" alt="Ceyteq — Empowering Digital Evolution">
<div><span class="pill">{T('FULL-SERVICE TECHNOLOGY & DIGITAL SOLUTIONS',
                           'සම්පූර්ණ තාක්ෂණික හා ඩිජිටල් විසඳුම්',
                           'SOLUTIONS TECHNIQUES ET NUMÉRIQUES COMPLÈTES')}</span></div>
<h1>{T('ONE PLATFORM. EVERY SOLUTION.', 'එක් වේදිකාවක්. සියලු විසඳුම්.', 'UNE PLATEFORME. TOUTES LES SOLUTIONS.')}</h1>
<div class="tag">{T('Empowering Digital Evolution', 'ඩිජිටල් පරිණාමය සවිබල ගැන්වීම', 'Favoriser l’évolution numérique')}</div>
<div class="tag2">{T('Websites, advertising, printing, media, AI &amp; travel — from one professional team.',
                     'වෙබ්, ප්‍රචාරණ, මුද්‍රණ, මාධ්‍ය, AI සහ සංචාරක — එකම වෘත්තීය කණ්ඩායමකින්.',
                     'Sites web, publicité, impression, médias, IA et voyage — une seule équipe professionnelle.')}</div>
<div class="cta-row">
<a class="btn btn-red" href="digitalrace.html#start">🏁 {T('Start Digital Race', 'ඩිජිටල් රේස් පටන්ගන්න', 'Démarrer Digital Race')}</a>
<a class="btn btn-navy" href="services.html">🧩 {T('All Services', 'සියලු සේවා', 'Tous les services')}</a>
<a class="btn btn-ghost" href="contact.html">📩 {T('Get a Quote', 'මිල ගණන් ගන්න', 'Devis')}</a>
</div>
<div class="stats">
<div class="stat"><b>08</b><span>{T('Service divisions', 'සේවා අංශ', 'Divisions de service')}</span></div>
<div class="stat"><b>90 <span class="lang-en">Days</span><span class="lang-si">දින</span><span class="lang-fr">jours</span></b><span>{T('Digital Race program', 'Digital Race වැඩසටහන', 'Programme Digital Race')}</span></div>
<div class="stat"><b>24/7 AI</b><span>{T('Bots & automation', 'Bots සහ automation', 'Bots et automatisation')}</span></div>
<div class="stat"><b>🇱🇰 + 🇫🇷</b><span>{T('Sri Lanka + France', 'ශ්‍රී ලංකා + ප්‍රංශය', 'Sri Lanka + France')}</span></div>
</div></div>

<section id="digitalrace">
<div class="alien">
<div class="kick">★ {T('FEATURED MAIN SERVICE', 'ප්‍රධාන සේවාව', 'SERVICE PRINCIPAL')} ★</div>
<div class="ah">{T('🏁 THE DIGITAL RACE PROGRAM', '🏁 ඩිජිටල් රේස් වැඩසටහන', '🏁 LE PROGRAMME DIGITAL RACE')}</div>
<p>{T('Our 90-day flagship program for restaurants, food outlets and local businesses — powered by the Alien Marketing Matrix method. Websites, WhatsApp ordering, AI bots and daily marketing, with packages from just $19.',
     'Restaurants, කඩ සහ දේශීය ව්‍යාපාර සඳහා දින 90 ප්‍රධාන වැඩසටහන — Alien Marketing Matrix ක්‍රමය සමඟ. වෙබ් අඩවි, WhatsApp orders, AI bots සහ දෛනික marketing — ඩොලර් 19 සිට පැකේජ.',
     'Notre programme phare de 90 jours pour restaurants et commerces locaux — méthode Alien Marketing Matrix. Sites, commandes WhatsApp, bots IA et marketing quotidien, forfaits dès 19 $.')}</p>
<div class="cta-row">
<a class="btn btn-cyan" href="digitalrace.html">{T('Explore Digital Race →', 'Digital Race බලන්න →', 'Découvrir Digital Race →')}</a>
<a class="btn btn-ghost" href="packages.html" style="border-color:#7fd4ef;color:#cfe3e8">{T('See packages & prices', 'පැකේජ හා මිල ගණන්', 'Forfaits et tarifs')}</a>
</div>
</div>
</section>

{HM.featured_band()}

<section id="learnearn">
<div class="eyebrow">{T('Learn &amp; Earn', 'ඉගෙන ගන්න, උපයන්න', 'Apprendre et gagner')}</div>
<h2>{T('Learn the Skill. Earn From It.', 'නිපුණතාව ඉගෙන ගන්න. එයින් උපයන්න.', 'Apprenez la compétence. Gagnez avec.')}</h2>
<p class="lead">{T('Professional courses in digital marketing, AI, web, design, video, photography, print and travel — taught by the team that does this work every day. Top students get paid projects from our own client queue.',
                   'ඩිජිටල් මාර්කටින්, AI, වෙබ්, design, video, photography, මුද්‍රණ සහ සංචාරක වෘත්තීය පාඨමාලා — මේ වැඩේ දිනපතා කරන කණ්ඩායමෙන්. හොඳම සිසුන්ට අපේම client queue එකෙන් ගෙවන ව්‍යාපෘති.',
                   'Formations professionnelles en marketing digital, IA, web, design, vidéo, photo, impression et voyage — par l’équipe qui fait ce travail chaque jour.')}</p>
<div class="cta-row" style="justify-content:flex-start">
<a class="btn btn-red" href="learn-earn.html">🎓 {T('See the courses', 'පාඨමාලා බලන්න', 'Voir les formations')}</a>
<a class="btn btn-ghost" href="careers.html">🤝 {T('Careers at Ceyteq', 'Ceyteq රැකියා', 'Carrières chez Ceyteq')}</a>
</div>
</section>

<section id="services">
<div class="eyebrow">{T('What we do', 'අප කරන දේ', 'Ce que nous faisons')}</div>
<h2>{T('09 Service Divisions, One Team', 'සේවා අංශ 09ක්, එකම කණ්ඩායමක්', '09 divisions de services, une seule équipe')}</h2>
<p class="lead">{T('From the first website to the last printed box — technology, creativity and marketing under one roof.',
                   'පළමු website එකේ සිට අවසන් printed box එක දක්වා — තාක්ෂණය, නිර්මාණශීලීත්වය සහ marketing එකම වහලක් යටට.',
                   'Du premier site web au dernier emballage imprimé — technologie, créativité et marketing sous un même toit.')}</p>
<div class="svcgrid">{cards}</div>
</section>

<section id="platforms">
<div class="eyebrow">{T('Always connected', 'හැමවිටම සම්බන්ධයි', 'Toujours connecté')}</div>
<h2>{T('Every Platform Your Customers Use', 'ඔබේ customers භාවිතා කරන හැම platform එකක්ම', 'Toutes les plateformes de vos clients')}</h2>
{blk('Social networks, Google, maps and booking channels', 'Social network, Google, maps සහ booking channels',
     'Réseaux sociaux, Google, cartes et canaux de réservation',
     items=PLATFORMS + BOOKING_CHANNELS,
     note_en='We create, verify, optimize and manage these accounts for your business — one team, one monthly report.',
     note_si='ඔබේ ව්‍යාපාරය සඳහා මේ ගිණුම් සාදා, තහවුරු කර, ප්‍රශස්ත කර කළමනාකරණය කරනවා — එකම කණ්ඩායමක්, එකම මාසික වාර්තාවක්.',
     note_fr='Nous créons, vérifions, optimisons et gérons ces comptes pour votre entreprise — une équipe, un rapport mensuel.')}
</section>

<section id="why">
<div class="eyebrow">{T('Why Ceyteq', 'ඇයි Ceyteq?', 'Pourquoi Ceyteq')}</div>
<h2>{T('Built for Real Business Growth', 'සැබෑ ව්‍යාපාරික වර්ධනය සඳහා', 'Conçu pour une vraie croissance')}</h2>
<div class="grid">
<div class="card"><h3>🧩 {T('One team, everything', 'එකම කණ්ඩායම, සියල්ල', 'Une équipe, tout')}</h3><p>{T('Website, ads, print, media and AI from the same team — no juggling five suppliers.', 'වෙබ්, ads, print, media සහ AI එකම කණ්ඩායමෙන් — සප්ලයර් පහක් සමඟ රස්සාවක් නෑ.', 'Site, pub, impression, médias et IA par la même équipe — pas cinq prestataires.')}</p></div>
<div class="card"><h3>⚡ {T('Fast &amp; affordable', 'වේගවත්, දැරිය හැකි', 'Rapide et abordable')}</h3><p>{T('Startup-friendly prices. Launch in days, upgrade whenever you grow.', 'Startup-friendly මිල. දින කිහිපයකින් launch, වැඩෙන විට upgrade.', 'Prix adaptés aux startups. Lancement en quelques jours, évolution à votre rythme.')}</p></div>
<div class="card"><h3>📈 {T('Systems that sell', 'විකුණන පද්ධති', 'Des systèmes qui vendent')}</h3><p>{T('We build ordering, booking and follow-up systems — not just pretty pages.', 'Orders, bookings සහ follow-up පද්ධති — ලස්සන පිටු විතරක් නොවෙයි.', 'Nous créons des systèmes de commande et de réservation, pas seulement de belles pages.')}</p></div>
<div class="card"><h3>🌍 {T('Local + international', 'දේශීය + ජාත්‍යන්තර', 'Local + international')}</h3><p>{T('Sri Lanka and France offices — local service with international standards.', 'ශ්‍රී ලංකා සහ ප්‍රංශ කාර්යාල — දේශීය සේවාව, ජාත්‍යන්තර තත්ත්වය.', 'Bureaux au Sri Lanka et en France — service local, standards internationaux.')}</p></div>
</div>
</section>

<section id="ceylonvoyage">
<div class="eyebrow">{T('Travel division', 'සංචාරක අංශය', 'Division voyage')}</div>
<h2>{T('Ceylon Voyage — Sri Lanka, France &amp; Beyond', 'Ceylon Voyage — ශ්‍රී ලංකා, ප්‍රංශය සහ ඉන් ඔබ්බට', 'Ceylon Voyage — Sri Lanka, France et au-delà')}</h2>
<p class="lead">{T('Itinerary planning, hotels, vehicles, event tickets, air tickets and tour guiding — with offices in Sri Lanka and France.',
                   'Itinerary සැලසුම්, hotels, වාහන, event tickets, air tickets සහ tour guide සේවා — ශ්‍රී ලංකා සහ ප්‍රංශ කාර්යාල සමඟ.',
                   'Itinéraires, hôtels, véhicules, billets d’événements et d’avion, guidage — bureaux au Sri Lanka et en France.')}</p>
<div class="cta-row" style="justify-content:flex-start">
<a class="btn btn-navy" href="travel.html">✈️ {T('Explore Ceylon Voyage →', 'Ceylon Voyage බලන්න →', 'Découvrir Ceylon Voyage →')}</a>
</div>
</section>
"""


# ----------------------------------------------------------------------------
# SERVICES HUB
# ----------------------------------------------------------------------------

def services_hub():
    cards = ''.join(svc_card(s) for s in SERVICES)
    return hero('Full service list', 'සම්පූර්ණ සේවා ලැයිස්තුව', 'Liste complète des services',
                'ALL CEYTEQ SERVICES', 'සියලු CEYTEQ සේවා', 'TOUS LES SERVICES CEYTEQ',
                'Technology, advertising, printing, media, AI and travel — pick a division to see what is included.',
                'තාක්ෂණය, ප්‍රචාරණ, මුද්‍රණ, මාධ්‍ය, AI සහ සංචාරක — අංශයක් තෝරා ඇතුළත් දේ බලන්න.',
                'Technologie, publicité, impression, médias, IA et voyage — choisissez une division.') + f"""
<section>
<div class="svcgrid">{cards}</div>
</section>
{HM.partners_section()}
<section>
<div class="eyebrow">{T('How we work', 'අප වැඩ කරන ආකාරය', 'Notre méthode')}</div>
<h2>{T('Five Steps From Idea to Launch', 'අදහසේ සිට launch දක්වා පියවර 5', 'Cinq étapes de l’idée au lancement')}</h2>
<div class="timeline">
<div class="month"><div class="m">{T('Step 1', 'පියවර 1', 'Étape 1')}</div><div class="d"><b>{T('Free consultation', 'නොමිලේ උපදේශනය', 'Consultation gratuite')}</b><p>{T('Tell us your business on WhatsApp or the contact form. We recommend the right service.', 'WhatsApp හෝ contact form එකෙන් ඔබේ ව්‍යාපාරය ගැන කියන්න. ගැලපෙන සේවාව අපි යෝජනා කරනවා.', 'Parlez-nous de votre activité sur WhatsApp ou via le formulaire.')}</p></div></div>
<div class="month"><div class="m">{T('Step 2', 'පියවර 2', 'Étape 2')}</div><div class="d"><b>{T('Plan &amp; quote', 'සැලසුම හා මිල', 'Plan et devis')}</b><p>{T('Clear written scope and price before any work starts. No hidden costs.', 'වැඩ පටන් ගන්න කලින් ලිඛිත scope සහ මිල. සැඟවුණු ගාස්තු නෑ.', 'Périmètre et prix écrits avant tout travail. Aucun coût caché.')}</p></div></div>
<div class="month"><div class="m">{T('Step 3', 'පියවර 3', 'Étape 3')}</div><div class="d"><b>{T('Build &amp; create', 'නිර්මාණය', 'Création')}</b><p>{T('Website, creatives, print or campaign — produced by our in-house team.', 'වෙබ්, creatives, print හෝ campaign — අපේම කණ්ඩායමෙන්.', 'Site, créations, impression ou campagne — réalisés en interne.')}</p></div></div>
<div class="month"><div class="m">{T('Step 4', 'පියවර 4', 'Étape 4')}</div><div class="d"><b>{T('Launch &amp; train', 'Launch හා පුහුණුව', 'Lancement et formation')}</b><p>{T('We go live and train your staff to use the system with confidence.', 'Live කරලා ඔබේ කණ්ඩායමට පද්ධතිය භාවිතා කරන්න පුහුණු කරනවා.', 'Mise en ligne et formation de votre équipe.')}</p></div></div>
<div class="month"><div class="m">{T('Step 5', 'පියවර 5', 'Étape 5')}</div><div class="d"><b>{T('Grow &amp; optimize', 'වර්ධනය හා ප්‍රශස්තකරණය', 'Croissance et optimisation')}</b><p>{T('Monthly content, analytics and optimization — or join the 90-day Digital Race program.', 'මාසික content, analytics සහ optimization — නැත්නම් දින 90 Digital Race වැඩසටහනට එකතු වන්න.', 'Contenu mensuel, analyses et optimisation — ou le programme Digital Race de 90 jours.')}</p></div></div>
</div>
{quote_cta()}
</section>
"""


# ----------------------------------------------------------------------------
# 01 WEB
# ----------------------------------------------------------------------------

def web():
    return hero('Division 01', 'අංශය 01', 'Division 01',
                'WEB SERVICES', 'වෙබ් සේවා', 'SERVICES WEB',
                'Web platform creation & optimization, social network setup, business web network listings and managed web services.',
                'වෙබ් පද්ධති නිර්මාණය හා ප්‍රශස්තකරණය, social network සැකසුම, business web network listings සහ කළමනාකරණ සේවා.',
                'Création et optimisation de plateformes web, réseaux sociaux, annuaires professionnels et services gérés.') + f"""
<section>
{blk('1.1 Web platform creation &amp; optimization', '1.1 වෙබ් පද්ධති නිර්මාණය හා ප්‍රශස්තකරණය',
     '1.1 Création et optimisation de plateformes web',
     items=['Business website', 'E-Commerce website', 'Online ordering', 'Booking & menu systems',
            'Admin panel', 'Multi-language', 'Mobile responsive', 'Speed & SEO optimization'],
     note_en='A website built to sell: fast, mobile-first, Sinhala/English/French ready, with an admin panel so your staff can update menus, prices and offers without a developer.',
     note_si='විකුණුම් සඳහා හදන ලද වෙබ් අඩවියක්: වේගවත්, mobile-first, සිංහල/English/ප්‍රංශ ready, staff ට developer එකෙක් නැතුව menu, මිල සහ offers update කරන්න admin panel එකක් සමඟ.',
     note_fr='Un site conçu pour vendre : rapide, mobile-first, prêt en cinghalais/anglais/français, avec un panneau admin pour mettre à jour menus et prix sans développeur.')}
{blk('Social network &amp; Google setup', 'Social network සහ Google සැකසුම', 'Réseaux sociaux et Google',
     items=PLATFORMS,
     note_en='Creation, verification, branding, SEO and ongoing management of every account, so your business is found everywhere your customers look.',
     note_si='හැම ගිණුමක්ම සෑදීම, තහවුරු කිරීම, branding, SEO සහ නිරන්තර කළමනාකරණය — customers සොයන හැම තැනකම ඔබේ ව්‍යාපාරය හම්බවෙන්න.',
     note_fr='Création, vérification, branding, SEO et gestion de chaque compte pour que votre activité soit visible partout.')}
{blk('Business web network listings', 'ව්‍යාපාරික web network listings', 'Annuaires professionnels',
     items=BOOKING_CHANNELS,
     note_en='We list, verify and optimize your property or business on the world’s biggest booking and travel platforms — pricing, photos and availability in sync.',
     note_si='ලෝකයේ ලොකුම booking හා travel platforms වල ඔබේ ව්‍යාපාරය list කර, verify කර, optimize කරනවා — මිල, ඡායාරූප සහ availability එකට.',
     note_fr='Nous inscrivons et optimisons votre établissement sur les plus grandes plateformes de réservation — tarifs, photos et disponibilités synchronisés.')}
{blk('1.2 Managed web services', '1.2 කළමනාකරණ වෙබ් සේවා', '1.2 Services web gérés',
     items=['Social Media Marketing', 'Hosting Service', 'Domain &amp; Email', 'SSL &amp; Security',
            'AI Robot Messaging Services', 'Monthly reporting'],
     note_en='Hosting, domain, email, backups, security updates and AI robot messaging — all handled by us, on a small monthly fee.',
     note_si='Hosting, domain, email, backups, security updates සහ AI robot messaging — සියල්ල අපි කරනවා, කුඩා මාසික ගාස්තුවකට.',
     note_fr='Hébergement, domaine, e-mail, sauvegardes, sécurité et robots de messagerie IA — gérés par nous, petit abonnement mensuel.')}
</section>
<section>
<div class="eyebrow">{T('Investment', 'මිල ගණන්', 'Investissement')}</div>
<h2>{T('Website Packages', 'වෙබ් පැකේජ', 'Forfaits web')}</h2>
<p class="lead">{T('Same locked prices as the Digital Race program. Monthly plans cover content, hosting support and optimization.',
                   'Digital Race වැඩසටහනේම ස්ථිර මිල. මාසික සැලසුම් වල content, hosting support සහ optimization ඇතුළත්.',
                   'Mêmes tarifs que le programme Digital Race. Les forfaits mensuels incluent contenu, hébergement et optimisation.')}</p>
{PACKAGES_TABLE}
{quote_cta('Order on WhatsApp', 'WhatsApp එකෙන් order කරන්න', 'Commander sur WhatsApp')}
</section>
"""


# ----------------------------------------------------------------------------
# 02 ADVERTISING
# ----------------------------------------------------------------------------

def ads():
    return hero('Division 02', 'අංශය 02', 'Division 02',
                'ADVERTISING &amp; PROMOTIONS', 'ප්‍රචාරණ හා promotions', 'PUBLICITÉ ET PROMOTIONS',
                'Social media ads, Google Ads, YouTube promotions and web traffic campaigns that sell.',
                'Social media ads, Google Ads, YouTube ප්‍රචාරණ සහ web traffic campaigns — විකුණන ප්‍රචාරණ.',
                'Publicités sociales, Google Ads, promotions YouTube et campagnes de trafic qui vendent.') + f"""
<section>
{blk('2.1 Social media ads &amp; campaigns', '2.1 Social media ads හා campaigns', '2.1 Publicités et campagnes sociales',
     items=['Facebook', 'Instagram', 'TikTok', 'X (Twitter)', 'Pinterest', 'Reddit', 'Threads', 'LinkedIn'],
     note_en='Creative, audience targeting, budget control and daily optimization. Turn this on and switch it off whenever you like — you always control the budget.',
     note_si='Creative, audience targeting, budget පාලනය සහ දෛනික optimization. කැමති වෙලාවක on/off කරන්න පුළුවන් — budget පාලනය හැමවිටම ඔබ ළඟ.',
     note_fr='Créations, ciblage, contrôle du budget et optimisation quotidienne. Activez ou désactivez à volonté — vous gardez le contrôle du budget.')}
{blk('2.2 Google ads &amp; campaigns', '2.2 Google ads හා campaigns', '2.2 Google Ads et campagnes',
     items=['Google Search Ads', 'Google Display', 'Google Business Ads', 'YouTube Ads', 'Email campaigns', 'Maps &amp; local ads'],
     note_en='Be the first result when a customer in your area searches for exactly what you sell.',
     note_si='ඔබේ ප්‍රදේශයේ customer කෙනෙක් හරියටම ඔබ විකුණන දේ සොයන විට පළමු ප්‍රතිඵලය ඔබ වෙන්න.',
     note_fr='Soyez le premier résultat quand un client de votre région cherche exactement ce que vous vendez.')}
{blk('2.3 Web marketing &amp; web traffic campaigns', '2.3 Web marketing සහ web traffic campaigns', '2.3 Webmarketing et campagnes de trafic',
     items=['E-Commerce website promotion', 'Web ads management', 'Landing pages', 'Conversion tracking', 'Retargeting', 'Analytics'],
     note_en='Traffic alone is not enough — we track which ad brought which order, then push the winners.',
     note_si='Traffic විතරක් ප්‍රමාණවත් නෑ — කවර ad එකෙන් කවර order එක ආවද track කරලා දිනන ඒවා තව දිගටම යවනවා.',
     note_fr='Le trafic ne suffit pas — nous suivons quelle annonce a généré quelle commande, puis poussons les gagnantes.')}
{blk('2.4 Ad budget — how it works', '2.4 Ad budget — කොහොමද වැඩ කරන්නේ', '2.4 Budget publicitaire — comment ça marche',
     items=['$1–$2 / day starter budget', 'Paid by you directly to the platform', 'Ceyteq setup &amp; optimization FREE',
            'Scale up when profitable', 'Full transparency reports'],
     note_en='Your money goes to Facebook/Google — never through us. We charge only for building and managing the campaign.',
     note_si='ඔබේ මුදල් Facebook/Google වලට කෙලින්ම යනවා — අප හරහා නොවේ. අප ගන්නේ campaign එක හදලා කළමනාකරණය කිරීමට පමණයි.',
     note_fr='Votre argent va directement à Facebook/Google — jamais via nous. Nous facturons la création et la gestion de campagne.')}
</section>
<section>
<div class="eyebrow">{T('Investment', 'මිල ගණන්', 'Investissement')}</div>
<h2>{T('Campaign Setup &amp; Management', 'Campaign setup හා කළමනාකරණය', 'Création et gestion de campagne')}</h2>
<p class="lead">{T('One-time campaign build, then optional monthly management. Ad spend is always yours, paid directly to Meta/Google.',
                   'එක් වරක් campaign එක හදලා, පසුව කැමති නම් මාසික කළමනාකරණය. Ad මුදල් හැමවිටම ඔබේ, Meta/Google වලට කෙලින්ම.',
                   'Création unique de la campagne, puis gestion mensuelle optionnelle. Le budget pub reste le vôtre, payé à Meta/Google.')}</p>
{PACKAGES_TABLE}
{quote_cta('Start a campaign', 'Campaign එකක් පටන්ගන්න', 'Lancer une campagne')}
</section>
"""


# ----------------------------------------------------------------------------
# 03 PRINTING
# ----------------------------------------------------------------------------

def printing():
    return hero('Division 03', 'අංශය 03', 'Division 03',
                'PRINTING &amp; DIGITAL SOLUTIONS', 'මුද්‍රණ හා ඩිජිටල් විසඳුම්', 'IMPRESSION ET SOLUTIONS NUMÉRIQUES',
                'Offset printing, packaging, signage, LED boards, paper bags, food packing and promotional merchandise.',
                'Offset මුද්‍රණ, packaging, signage, LED boards, paper bag, food packing සහ promotional භාණ්ඩ.',
                'Impression offset, emballage, signalétique, panneaux LED, sacs papier, emballages alimentaires et objets promotionnels.') + f"""
<section>
{blk('3.1 General printing', '3.1 සාමාන්‍ය මුද්‍රණ', '3.1 Impression générale',
     items=['Business &amp; promotion documents', 'Marketing materials', 'Business cards', 'Menu book / diary / notebook',
            'Handbill', 'Poster', 'Sticker', 'Offset printing'],
     note_en='Send your artwork on WhatsApp, or let our designers create it. Bulk orders get better rates — ask for the quantity price breaks.',
     note_si='ඔබේ artwork එක WhatsApp එකෙන් යවන්න, නැත්නම් අපේ designers ලා හදලා දෙනවා. වැඩි ප්‍රමාණවලට හොඳ මිල — quantity price breaks අහන්න.',
     note_fr='Envoyez votre fichier sur WhatsApp ou laissez nos designers le créer. Meilleurs tarifs en grande quantité.')}
{blk('Packaging printing', 'Packaging මුද්‍රණය', 'Impression d’emballage',
     items=['Conduct packaging printing', 'Product packaging', 'Labels &amp; packaging printing', 'Food packing',
            'Paper bag (customized)', 'Gift box', 'Kraft bag'],
     note_en='Food-grade and retail packaging with your brand printed on it — designed, sampled and delivered.',
     note_si='ඔබේ brand එක සටහන් කරන ලද food-grade සහ retail packaging — design, sample සහ delivery සමඟ.',
     note_fr='Emballages alimentaires et retail à votre marque — conception, échantillon et livraison.')}
{blk('3.2 Digital solutions', '3.2 ඩිජිටල් විසඳුම්', '3.2 Solutions numériques',
     items=['Digital sign board', 'Digital banner', 'Digital LED board', 'Digital printing',
            'Digital wood laser printing', 'All kinds of digital advertising'],
     note_en='Bright, programmable LED boards and digital signage for shops, restaurants and hotels — installed and serviced by us.',
     note_si='කඩ, restaurants සහ hotels සඳහා දීප්තිමත් LED boards සහ digital signage — සවි කිරීම සහ සේවා සමඟ.',
     note_fr='Panneaux LED lumineux et signalétique numérique pour commerces, restaurants et hôtels — installés et entretenus par nous.')}
{blk('3.3 Other printing &amp; merchandise', '3.3 වෙනත් මුද්‍රණ සහ භාණ්ඩ', '3.3 Autres impressions et produits',
     items=['T-shirt', 'Jersey', 'Cap', 'Mug printing', 'Promotional items', 'Event branding'],
     note_en='Staff uniforms, event T-shirts and branded gifts — small runs welcome.',
     note_si='කණ්ඩායම් නිල ඇඳුම්, event T-shirts සහ branded තෑගි — කුඩා ප්‍රමාණත් සාදරයෙන් පිළිගන්නවා.',
     note_fr='Uniformes, t-shirts d’événement et cadeaux de marque — petites séries acceptées.')}
</section>
<section>
<div class="eyebrow">{T('How to order', 'Order කරන ආකාරය', 'Comment commander')}</div>
<h2>{T('Artwork In, Delivery Out', 'Artwork එක දෙන්න, delivery එක ගන්න', 'Votre fichier en entrée, la livraison en sortie')}</h2>
<div class="grid">
<div class="card"><h3>1️⃣ {T('Send artwork or idea', 'Artwork හෝ අදහස යවන්න', 'Envoyez le fichier ou l’idée')}</h3><p>{T('WhatsApp your design, or describe it and our designers will create it.', 'ඔබේ design එක WhatsApp කරන්න, නැත්නම් විස්තර කරන්න — අපේ designers හදනවා.', 'Envoyez votre fichier sur WhatsApp ou décrivez l’idée.')}</p></div>
<div class="card"><h3>2️⃣ {T('Free quote &amp; sample', 'නොමිලේ මිල හා sample', 'Devis et échantillon gratuits')}</h3><p>{T('Exact price by quantity, with a digital proof before printing.', 'ප්‍රමාණය අනුව හරි මිල, මුද්‍රණයට කලින් digital proof එකක් සමඟ.', 'Prix exact selon la quantité, avec un BAT numérique avant impression.')}</p></div>
<div class="card"><h3>3️⃣ {T('Print, deliver, install', 'මුද්‍රණය, delivery, සවි කිරීම', 'Impression, livraison, installation')}</h3><p>{T('Collection or island-wide delivery — LED boards and signage installed by our team.', 'එකතු කරගැනීම හෝ දිවයින පුරා delivery — LED boards සහ signage අපේ කණ්ඩායම සවි කරනවා.', 'Retrait ou livraison dans tout le pays — panneaux installés par notre équipe.')}</p></div>
</div>
{quote_cta('Send artwork for a quote', 'මිල ගණන් සඳහා artwork යවන්න', 'Envoyer un fichier pour un devis')}
</section>
"""


# ----------------------------------------------------------------------------
# 04 MEDIA
# ----------------------------------------------------------------------------

def media():
    return hero('Division 04', 'අංශය 04', 'Division 04',
                'PHOTOGRAPHY &amp; VIDEOGRAPHY', 'ඡායාරූප හා වීඩියෝ', 'PHOTOGRAPHIE ET VIDÉO',
                'Professional capture for events, weddings, cultural events, products, business places and marketing.',
                'Event, මංගල උත්සව, සංස්කෘතික උත්සව, products, ව්‍යාපාරික ස්ථාන සහ marketing සඳහා වෘත්තීය නිර්මාණ.',
                'Captation professionnelle pour événements, mariages, événements culturels, produits et locaux commerciaux.') + f"""
<section>
{blk('What we cover', 'අප ආවරණය කරන දේ', 'Ce que nous couvrons',
     items=['Events', 'Wedding functions', 'Cultural events', 'Business products', 'Business places',
            'Marketing content', 'Reels &amp; shorts', 'Corporate promotions'],
     note_en='All kinds of capture for marketing things — photo, video, reels and full edits, delivered in social-ready formats.',
     note_si='marketing සඳහා සියලු ආකාරයේ නිර්මාණ — ඡායාරූප, වීඩියෝ, reels සහ සම්පූර්ණ edits, social media formats වලින්.',
     note_fr='Toutes les captations marketing — photo, vidéo, reels et montages livrés aux formats réseaux sociaux.')}
{blk('Packages', 'පැකේජ', 'Forfaits',
     items=['Half-day coverage', 'Full-day coverage', 'Wedding package', 'Product shoot', 'Business place shoot',
            'Reels bundle (5–10)', 'Drone (on request)'],
     note_en='Pick a coverage type and we quote by location, hours and deliverables. Edited photos and video are included.',
     note_si='coverage වර්ගයක් තෝරන්න — ස්ථානය, පැය ගණන සහ deliverables අනුව මිල දෙනවා. Edited photos සහ video ඇතුළත්.',
     note_fr='Choisissez un type de couverture — devis selon lieu, durée et livrables. Photos et vidéos montées incluses.')}
{quote_cta('Book a shoot date', 'Shoot දිනයක් වෙන් කරන්න', 'Réserver une date')}
</section>
"""


# ----------------------------------------------------------------------------
# 05 DESIGN
# ----------------------------------------------------------------------------

def design():
    return hero('Division 05', 'අංශය 05', 'Division 05',
                'GRAPHIC DESIGN &amp; VIDEO EDITING', 'ග්‍රැෆික් නිර්මාණ හා වීඩියෝ එඩිටින්', 'DESIGN GRAPHIQUE ET MONTAGE VIDÉO',
                'Photos editing, graphic design, flyer &amp; poster design, video editing and filming.',
                'Photos editing, graphic design, flyer හා poster නිර්මාණ, video editing සහ film නිර්මාණ.',
                'Retouche photo, design graphique, flyers et affiches, montage vidéo et tournage.') + f"""
<section>
{blk('Design services', 'නිර්මාණ සේවා', 'Services de design',
     items=['Photos editing', 'Graphic design', 'Flyer design', 'Poster design', 'Video editing',
            'Filming', 'Logo &amp; brand identity', 'Menu &amp; price list design'],
     note_en='Consistent, professional-looking designs that match your brand — for social posts, print and advertising.',
     note_si='ඔබේ brand එකට ගැලපෙන ස්ථාවර, වෘත්තීය නිර්මාණ — social posts, print සහ ප්‍රචාරණ සඳහා.',
     note_fr='Des créations cohérentes et professionnelles à votre image — réseaux sociaux, impression et publicité.')}
{blk('Monthly content packs', 'මාසික content පැකේජ', 'Packs de contenu mensuels',
     items=['2 videos + 4 flyers', '3 videos + 4 flyers', '5 videos + 7 flyers', '7 videos + 10 flyers', '10 videos + 15 flyers'],
     note_en='Order design-only, or get it included in the Standard, Advanced and Premium packages.',
     note_si='Design විතරක් order කරන්න, නැත්නම් Standard, Advanced සහ Premium පැකේජ සමඟ නොමිලේ ලබාගන්න.',
     note_fr='Commandez le design seul, ou en inclus dans les forfaits Standard, Advanced et Premium.')}
<div class="cta-row" style="margin-top:22px">
<a class="btn btn-ghost" href="offers.html">🏷️ {T('See our offers', 'අපේ දීමනා බලන්න', 'Voir nos offres')}</a>
</div>
{quote_cta('Order a design', 'නිර්මාණයක් order කරන්න', 'Commander une création')}
</section>
"""


# ----------------------------------------------------------------------------
# 06 AI & ERP
# ----------------------------------------------------------------------------

def ai_erp():
    return hero('Division 06', 'අංශය 06', 'Division 06',
                'AI INTEGRATION &amp; ERP SOLUTIONS', 'AI සම්බන්ධකරණය හා ERP විසඳුම්', 'INTÉGRATION IA ET SOLUTIONS ERP',
                'AI consulting, hospitality &amp; retail ERP, AI customer care, CRM automation and AI messaging robots.',
                'AI උපදේශනය, hospitality සහ retail ERP, AI customer care, CRM automation සහ AI messaging robots.',
                'Conseil IA, ERP hôtellerie et retail, service client IA, automatisation CRM et robots de messagerie.') + f"""
<section>
{blk('AI customer care &amp; messaging', 'AI customer care හා messaging', 'Service client IA et messagerie',
     items=['Website chatbot', 'Messenger chatbot', 'WhatsApp automation', 'Telegram bots', 'Voice caller bot',
            'Multi-language replies (SI / EN / FR)', 'After-hours auto answers', 'Order taking'],
     note_en='Your business keeps answering at 2 AM: prices, menu, availability, bookings and order taking — in Sinhala, English and French.',
     note_si='රාත්‍රී 2ටත් ඔබේ ව්‍යාපාරය පිළිතුරු දෙනවා: මිල, menu, availability, bookings සහ orders — සිංහල, English, ප්‍රංශ තුනෙන්ම.',
     note_fr='Votre activité répond à 2 h du matin : tarifs, menu, disponibilités, réservations et commandes — en cinghalais, anglais et français.')}
{blk('CRM &amp; business automation', 'CRM සහ ව්‍යාපාර automation', 'CRM et automatisation',
     items=['AI customer relationship (CRM)', 'Lead capture &amp; follow-up', 'Booking reminders', 'Review requests',
            'Loyalty campaigns', 'Staff task automation'],
     note_en='Every enquiry is stored, tagged and followed up automatically — no more lost customers in a phone notebook.',
     note_si='හැම විමසුමක්ම save වෙලා, tag වෙලා ස්වයංක්‍රීයව follow-up වෙනවා — phone notebook එකේ නැතිවෙන customers නෑ.',
     note_fr='Chaque demande est enregistrée, étiquetée et suivie automatiquement — plus de clients perdus.')}
{blk('Hospitality &amp; retail ERP', 'Hospitality සහ retail ERP', 'ERP hôtellerie et retail',
     items=['Restaurant ERP', 'Hotel &amp; guesthouse ERP', 'Inventory &amp; stock', 'POS integration',
            'Staff &amp; shift management', 'Sales analytics &amp; reports', 'Table &amp; room bookings'],
     note_en='One dashboard for orders, stock, staff and reports — built for Sri Lankan restaurants, hotels and shops.',
     note_si='Orders, stock, staff සහ reports සඳහා එකම dashboard එකක් — ශ්‍රී ලාංකික restaurants, hotels සහ කඩ සඳහා.',
     note_fr='Un tableau de bord pour commandes, stock, personnel et rapports — pensé pour les restaurants et hôtels sri-lankais.')}
</section>
<section>
<div class="eyebrow">{T('Investment', 'මිල ගණන්', 'Investissement')}</div>
<h2>{T('AI Pricing', 'AI මිල ගණන්', 'Tarifs IA')}</h2>
<div class="grid">
<div class="card"><h3>💬 {T('Messenger / Website chatbot', 'Messenger / Website chatbot', 'Chatbot Messenger / Site')}</h3><p class="price-inline"><b>{T('FREE', 'නොමිලේ', 'GRATUIT')}</b><br>{T('Included with the Advanced package ($80) and above.', 'Advanced පැකේජය ($80) සහ ඉහළ ඒවා සමඟ ඇතුළත්.', 'Inclus avec le forfait Advanced (80 $) et plus.')}</p></div>
<div class="card"><h3>📞 {T('Voice caller bot', 'Voice caller bot', 'Bot vocal')}</h3><p class="price-inline"><b>$15 / {T('month', 'මාස', 'mois')}</b><br>{T('Optional add-on for Advanced and Premium clients.', 'Advanced සහ Premium සේවාලාභීන්ට අමතර විකල්පයක්.', 'Option pour les clients Advanced et Premium.')}</p></div>
<div class="card"><h3>🏨 {T('ERP / CRM integration', 'ERP / CRM සම්බන්ධකරණය', 'Intégration ERP / CRM')}</h3><p class="price-inline"><b>{T('Quote', 'මිල විමසන්න', 'Sur devis')}</b><br>{T('Quoted by number of branches, staff and modules you need.', 'ශාඛා, staff සහ අවශ්‍ය modules ගණන අනුව මිල.', 'Devis selon le nombre de succursales, employés et modules.')}</p></div>
</div>
<div class="cta-row" style="margin-top:22px">
<a class="btn btn-ghost" href="digitalrace.html#ai">🤖 {T('See AI in the Digital Race program', 'Digital Race වැඩසටහනේ AI කොටස බලන්න', 'Voir l’IA dans Digital Race')}</a>
</div>
{quote_cta('Ask about AI for your business', 'ඔබේ ව්‍යාපාරයට AI ගැන අහන්න', 'Demandez l’IA pour votre activité')}
</section>
"""


# ----------------------------------------------------------------------------
# 07 TRAVEL — Ceylon Voyage
# ----------------------------------------------------------------------------

def travel():
    return hero('Division 07 • Ceylon Voyage', 'අංශය 07 • Ceylon Voyage', 'Division 07 • Ceylon Voyage',
                'CEYLON VOYAGE', 'CEYLON VOYAGE', 'CEYLON VOYAGE',
                'Our travel division with offices in Sri Lanka and France — itineraries, hotels, transport, tickets and guiding.',
                'ශ්‍රී ලංකා සහ ප්‍රංශ කාර්යාල සහිත අපේ සංචාරක අංශය — itineraries, hotels, transport, tickets සහ guiding.',
                'Notre division voyage avec bureaux au Sri Lanka et en France — itinéraires, hôtels, transport, billets et guidage.') + f"""
<section>
{blk('Sri Lankan travel &amp; tourism — direct, guided solutions', 'ශ්‍රී ලංකා සංචාරක — කෙලින්ම, guide සමඟ',
     'Tourisme sri-lankais — solutions directes et guidées',
     items=['Sri Lanka + France offices', 'English / French / Sinhala speaking', 'Airport pickup',
            'Local guides', 'Family &amp; group tours', 'Honeymoon packages', 'Adventure &amp; wildlife', 'Ayurveda &amp; wellness'],
     note_en='We are a Sri Lankan team with a French office — we plan trips that actually work on the ground, at local prices.',
     note_si='අපි ප්‍රංශ කාර්යාලයක් සහිත ශ්‍රී ලාංකික කණ්ඩායමක් — දේශීය මිලට, ඇත්තටම වැඩ කරන ගමන් සැලසුම් කරනවා.',
     note_fr='Une équipe sri-lankaise avec un bureau en France — des voyages réalistes, aux prix locaux.')}
{blk('7.1 Itinerary planning &amp; booking', '7.1 Itinerary සැලසුම් හා booking', '7.1 Itinéraires et réservations',
     items=['Custom itinerary', 'Hotel &amp; guesthouse booking', 'Tour packages', 'Day tours', 'Ticket booking', 'Travel insurance advice'])}
{blk('7.2 Tourist information directory', '7.2 සංචාරක තොරතුරු නාමාවලිය', '7.2 Répertoire touristique',
     items=['Kandy', 'Ella', 'Sigiriya', 'Dambulla', 'Galle &amp; Unawatuna', 'Mirissa', 'Yala &amp; Udawalawe',
            'Nuwara Eliya', 'Trincomalee', 'Jaffna', 'Anuradhapura', 'Negombo &amp; Colombo'],
     note_en='Up-to-date information on the areas tourists actually ask about: what to see, when to go, what it costs.',
     note_si='සංචාරකයන් ඇත්තටම අසන ප්‍රදේශ ගැන නවතම තොරතුරු: බලන්න ඕන දේ, යන්න හොඳ කාලය, වියදම.',
     note_fr='Informations à jour sur les régions demandées : quoi voir, quand partir, combien ça coûte.')}
{blk('7.3 Transport &amp; event tickets', '7.3 ප්‍රවාහන හා event tickets', '7.3 Transport et billets d’événements',
     items=['Airport transfers', 'Private car &amp; driver', 'Van &amp; bus hire', 'Train tickets', 'Cultural event tickets', 'Local experiences'])}
{blk('7.4 Vehicle booking for foreigners', '7.4 විදේශිකයන් සඳහා වාහන booking', '7.4 Location de véhicules pour étrangers',
     items=['Self-drive (with licence guidance)', 'Car with English-speaking driver', 'Tuk-tuk hire', 'Bikes &amp; scooters',
            'Long-term rental', 'Hotel-to-hotel transfers'])}
{blk('08 Air tickets, emigration information &amp; solutions', '08 Air tickets, emigration තොරතුරු සහ විසඳුම්',
     '08 Billets d’avion, informations et solutions d’émigration',
     items=['Air ticket booking', 'Route &amp; fare advice', 'Transit information', 'Emigration information',
            'Document guidance', 'Visa appointment help', 'France / Europe travel'],
     note_en='Straight information and real solutions — airline tickets, transit questions and the paperwork side of travelling abroad.',
     note_si='සෘජු තොරතුරු සහ සැබෑ විසඳුම් — ගුවන් ටිකට්පත්, transit ප්‍රශ්න සහ විදේශගත වීමේ ලේඛන පැත්ත.',
     note_fr='Informations claires et solutions concrètes — billets, transit et démarches pour voyager à l’étranger.')}
{quote_cta('Plan my trip on WhatsApp', 'මගේ ගමන WhatsApp එකෙන් සැලසුම් කරන්න', 'Planifier mon voyage sur WhatsApp', wa='33744284269')}
</section>
"""


# ----------------------------------------------------------------------------
# 08 CAREERS
# ----------------------------------------------------------------------------

def careers():
    jobs = [
        ('Digital Marketing Executive', 'ඩිජිටල් මාර්කටින් නිලධාරී', 'Chargé de marketing digital',
         'Manage client pages, ad campaigns and monthly content calendars. English + Sinhala required.',
         'Client පිටු, ad campaigns සහ මාසික content calendars කළමනාකරණය. English + සිංහල අවශ්‍යයි.',
         'Gestion des pages clients, campagnes et calendriers de contenu. Anglais + cinghalais requis.'),
        ('Web Developer / Designer', 'වෙබ් සංවර්ධක / නිර්මාණකරු', 'Développeur / designer web',
         'Build client websites and panels (HTML/CSS/JS, Python or PHP). Portfolio required.',
         'Client වෙබ් අඩවි සහ panels හදනවා (HTML/CSS/JS, Python හෝ PHP). Portfolio එකක් අවශ්‍යයි.',
         'Créer des sites et panneaux clients (HTML/CSS/JS, Python ou PHP). Portfolio demandé.'),
        ('Graphic Designer', 'ග්‍රැෆික් නිර්මාණකරු', 'Designer graphique',
         'Flyers, posters, menus, packaging artwork and social creatives.',
         'Flyers, posters, menu, packaging artwork සහ social creatives.',
         'Flyers, affiches, menus, packaging et visuels sociaux.'),
        ('Videographer / Photographer', 'වීඩියෝ / ඡායාරූප ශිල්පී', 'Vidéaste / photographe',
         'Events, weddings, product shoots and reels. Own equipment preferred.',
         'Events, මංගල, product shoots සහ reels. තමන්ගේ උපකරණ තිබීම වාසියක්.',
         'Événements, mariages, produits et reels. Équipement personnel apprécié.'),
        ('SEO &amp; Google Business Specialist', 'SEO සහ Google Business විශේෂඥ',
         'Spécialiste SEO et Google Business',
         'Rank local businesses on Google and Maps, manage profiles and reviews.',
         'දේශීය ව්‍යාපාර Google සහ Maps වල ඉහළට ගෙනෙන්න, profiles සහ reviews කළමනාකරණය.',
         'Positionner les commerces locaux sur Google et Maps, gérer profils et avis.'),
        ('Interns / Trainees', 'පුහුණු (Intern)', 'Stagiaires',
         'Marketing, design, media or travel — 3 to 6 month internships with real client work.',
         'Marketing, design, media හෝ travel — සැබෑ client වැඩ සමඟ මාස 3–6 පුහුණුව.',
         'Marketing, design, médias ou voyage — stages de 3 à 6 mois avec de vrais clients.'),
    ]
    cards = ''.join(
        f'<div class="card"><h3>💼 {T(en, si, fr)}</h3><p>{T(den, dsi, dfr)}</p></div>'
        for en, si, fr, den, dsi, dfr in jobs)
    return hero('Careers', 'රැකියා අවස්ථා', 'Carrières',
                'WORK WITH CEYTEQ', 'CEYTEQ සමඟ වැඩ කරන්න', 'TRAVAILLER AVEC CEYTEQ',
                'We are growing — marketing, development, design, media and travel roles, plus internships.',
                'අපි වැඩෙනවා — marketing, development, design, media සහ travel රැකියා මෙන්ම පුහුණු අවස්ථා.',
                'Nous grandissons — marketing, développement, design, médias, voyage et stages.') + f"""
<section>
<div class="grid">{cards}</div>
</section>
<section>
<div class="eyebrow">{T('How to apply', 'අයදුම් කරන ආකාරය', 'Comment postuler')}</div>
<h2>{T('Send Your CV in 2 Minutes', 'විනාඩි 2කින් ඔබේ CV එක යවන්න', 'Envoyez votre CV en 2 minutes')}</h2>
<div class="blk">
<h3>{T('What to send', 'යවන්න ඕන දේ', 'Ce qu’il faut envoyer')}</h3>
<div class="chips">
<span>{T('CV / portfolio link', 'CV / portfolio link', 'CV / lien portfolio')}</span>
<span>{T('The role you want', 'කැමති තනතුර', 'Le poste souhaité')}</span>
<span>{T('Languages you speak', 'ඔබ කතා කරන භාෂා', 'Langues parlées')}</span>
<span>{T('Available start date', 'පටන් ගන්න පුළුවන් දිනය', 'Date de disponibilité')}</span>
</div>
<p class="note" style="margin-top:12px">{T('Email your CV to info.ceyteq@gmail.com or send it on WhatsApp. Shortlisted candidates get a reply within one week.',
   'ඔබේ CV එක info.ceyteq@gmail.com වලට email කරන්න, නැත්නම් WhatsApp කරන්න. තෝරාගත් අයට සතියක් ඇතුළත පිළිතුරක්.',
   'Envoyez votre CV à info.ceyteq@gmail.com ou par WhatsApp. Réponse sous une semaine aux candidats retenus.')}</p>
<div class="cta-row" style="justify-content:flex-start;margin-top:18px">
<a class="btn btn-cyan" href="https://wa.me/94788607143" target="_blank">💬 {T('WhatsApp my CV', 'CV එක WhatsApp කරන්න', 'Envoyer mon CV sur WhatsApp')}</a>
<a class="btn btn-ghost" href="mailto:info.ceyteq@gmail.com">✉️ info.ceyteq@gmail.com</a>
</div>
</div>
</section>
"""


# ----------------------------------------------------------------------------
# ABOUT
# ----------------------------------------------------------------------------

def about():
    return hero('Company', 'සමාගම', 'Entreprise',
                'ABOUT CEYTEQ', 'CEYTEQ ගැන', 'À PROPOS DE CEYTEQ',
                'Ceyteq — Ceylon Technology : technology, digital marketing, advertising and business solutions under one roof.',
                'Ceyteq — Ceylon Technology : තාක්ෂණය, ඩිජිටල් මාර්කටින්, ප්‍රචාරණ සහ ව්‍යාපාරික විසඳුම් එකම වහලක් යටට.',
                'Ceyteq — Ceylon Technology : technologie, marketing digital, publicité et solutions d’entreprise sous un même toit.') + f"""
<section>
<div class="eyebrow">{T('Who we are', 'අපි කවුද', 'Qui sommes-nous')}</div>
<h2>{T('Empowering Digital Evolution', 'ඩිජිටල් පරිණාමය සවිබල ගැන්වීම', 'Favoriser l’évolution numérique')}</h2>
<p class="lead">{T('Ceyteq — Ceylon Technology is a full-service technology, digital marketing, advertising and business solutions company helping modern businesses build strong digital and physical brand presence. We provide web platforms, digital transformation services, AI-powered business solutions, creative media production and professional printing for startups, SMEs, hospitality brands, retail businesses and corporate organizations.',
   'Ceyteq — Ceylon Technology යනු නවීන ව්‍යාපාරවලට ශක්තිමත් ඩිජිටල් සහ භෞතික brand පැවැත්මක් ගොඩනගන්න උදව් කරන, තාක්ෂණ, ඩිජිටල් මාර්කටින්, ප්‍රචාරණ සහ ව්‍යාපාරික විසඳුම් සම්පූර්ණයෙන්ම සපයන සමාගමක්. Startup, SME, hospitality, retail සහ corporate ආයතන සඳහා වෙබ් පද්ධති, ඩිජිටල් පරිවර්තන සේවා, AI විසඳුම්, creative media නිෂ්පාදනය සහ වෘත්තීය මුද්‍රණ සේවා අපි සපයනවා.',
   'Ceyteq — Ceylon Technology est une société de services technologiques, marketing digital, publicité et solutions d’entreprise qui aide les entreprises modernes à bâtir une forte présence de marque. Nous fournissons plateformes web, transformation numérique, solutions d’IA, production média et impression professionnelle pour startups, PME, hôtellerie, commerce et entreprises.')}</p>
<div class="grid">
<div class="card"><h3>🎯 {T('Our mission', 'අපේ මෙහෙය', 'Notre mission')}</h3><p>{T('To empower every Sri Lankan business to win the digital race — with practical systems, affordable pricing and honest advice.', 'දැරිය හැකි මිලට, ප්‍රායෝගික පද්ධති සහ අවංක උපදෙස් සමඟ ලංකාවේ සෑම ව්‍යාපාරයක්ම ඩිජිටල් තරඟය ජයගන්න සවිබල ගැන්වීම.', 'Permettre à chaque entreprise sri-lankaise de gagner la course numérique — systèmes pratiques, prix abordables, conseils honnêtes.')}</p></div>
<div class="card"><h3>🏢 {T('Who we serve', 'අප සේවය කරන අය', 'Qui nous servons')}</h3><p>{T('Restaurants &amp; food outlets, hotels &amp; guesthouses, retail shops, travel &amp; tourism, startups, SMEs and corporate organizations.', 'Restaurants සහ food outlets, hotels සහ guesthouses, retail කඩ, travel හා tourism, startups, SMEs සහ corporate ආයතන.', 'Restaurants, hôtels et maisons d’hôtes, commerces, voyage et tourisme, startups, PME et entreprises.')}</p></div>
<div class="card"><h3>🌍 {T('Where we work', 'අප වැඩ කරන තැන්', 'Où nous travaillons')}</h3><p>{T('Sri Lanka headquarters with a branch in France — serving local and international clients in English, Sinhala and French.', 'ශ්‍රී ලංකා මූලස්ථානය සහ ප්‍රංශයේ ශාඛාව — English, සිංහල සහ ප්‍රංශ භාෂාවෙන් දේශීය හා ජාත්‍යන්තර සේවාලාභීන්ට.', 'Siège au Sri Lanka et succursale en France — clients locaux et internationaux en anglais, cinghalais et français.')}</p></div>
<div class="card"><h3>🧩 {T('What makes us different', 'අප වෙනස් ඇයි', 'Notre différence')}</h3><p>{T('One team for web, ads, print, media, AI and travel — plus our own 90-day growth program, the Digital Race.', 'වෙබ්, ads, print, media, AI සහ travel සඳහා එකම කණ්ඩායමක් — අපේම දින 90 වර්ධන වැඩසටහන Digital Race සමඟ.', 'Une seule équipe pour web, pub, impression, médias, IA et voyage — plus notre programme de croissance Digital Race.')}</p></div>
</div>
</section>
<section>
<div class="eyebrow">{T('Next step', 'ඊළඟ පියවර', 'Prochaine étape')}</div>
<h2>{T('Let’s Build Something That Sells', 'විකුණන දෙයක් හදමු', 'Créons quelque chose qui vend')}</h2>
<div class="cta-row" style="justify-content:flex-start">
<a class="btn btn-cyan" href="contact.html">📩 {T('Contact us', 'අප අමතන්න', 'Nous contacter')}</a>
<a class="btn btn-navy" href="careers.html">🤝 {T('Careers at Ceyteq', 'Ceyteq රැකියා', 'Carrières chez Ceyteq')}</a>
</div>
</section>
"""


# ----------------------------------------------------------------------------
# CONTACT (hub page with working enquiry form)
# ----------------------------------------------------------------------------

SERVICE_OPTIONS = ['Web Services', 'Advertising', 'Printing &amp; Digital', 'Photography &amp; Video',
                   'Design &amp; Editing', 'AI &amp; ERP', 'Ceylon Voyage (Travel)', 'Digital Race Program',
                   'HotelMate PMS (via Ceyteq)', 'Other']


def contact():
    opts = ''.join(f'<option value="{o}">{o}</option>' for o in SERVICE_OPTIONS)
    return hero('Contact', 'සම්බන්ධ වන්න', 'Contact',
                'TALK TO CEYTEQ', 'CEYTEQ සමඟ කතා කරන්න', 'PARLEZ À CEYTEQ',
                'WhatsApp, call or send the form — we reply during business hours, usually within the hour.',
                'WhatsApp, call හෝ form එක යවන්න — ව්‍යාපාරික වේලාවන්හිදී පැයක් ඇතුළත පිළිතුරු දෙනවා.',
                'WhatsApp, appel ou formulaire — nous répondons pendant les heures ouvrables.') + f"""
<section>
<div class="contact-grid">
<div class="cbox"><small>{T('HOTLINE', 'හොට්ලයින්', 'LIGNE DIRECTE')}</small><a href="tel:+94788607143">+94 78 860 7143</a></div>
<div class="cbox"><small>{T('WHATSAPP / MOBILE', 'WHATSAPP / ජංගම', 'WHATSAPP / MOBILE')}</small><a href="https://wa.me/94768607143" target="_blank">+94 76 860 7143</a></div>
<div class="cbox"><small>{T('WHATSAPP FRANCE', 'WHATSAPP ප්‍රංශය', 'WHATSAPP FRANCE')}</small><a href="https://wa.me/33744284269" target="_blank">+33 7 44 28 42 69</a></div>
<div class="cbox"><small>{T('EMAIL', 'ඊමේල්', 'E-MAIL')}</small><a href="mailto:info.ceyteq@gmail.com">info.ceyteq@gmail.com</a></div>
</div>
</section>
<section>
<div class="eyebrow">{T('Enquiry form', 'විමසුම් පෝරමය', 'Formulaire')}</div>
<h2>{T('Send Us the Details', 'විස්තර අපට එවන්න', 'Envoyez-nous les détails')}</h2>
<p class="lead">{T('Tell us what you need and we will come back with a clear plan and price. Your details are stored safely and never shared.',
                   'ඔබට අවශ්‍ය දේ කියන්න — පැහැදිලි සැලසුමක් සහ මිලක් සමඟ අපි නැවත කතා කරනවා. ඔබේ තොරතුරු සුරක්ෂිතව තබා ගන්නවා, කිසිවෙකුට දෙන්නේ නෑ.',
                   'Dites-nous ce dont vous avez besoin : nous revenons avec un plan et un prix clairs. Vos données restent confidentielles.')}</p>
<form class="enquiry" id="enquiryForm" onsubmit="return sendEnquiry(event)">
<input id="eqName" required maxlength="120" placeholder="Your name / ඔබේ නම" autocomplete="name">
<input id="eqContact" required maxlength="60" placeholder="WhatsApp / phone number / දුරකථන අංකය" autocomplete="tel">
<input id="eqEmail" type="email" maxlength="160" placeholder="Email (optional)">
<select id="eqService">{opts}</select>
<textarea id="eqMsg" required maxlength="2000" rows="5" placeholder="What do you need? / ඔබට අවශ්‍ය දේ?"></textarea>
<button class="btn btn-cyan" type="submit" id="eqBtn">{T('Send enquiry', 'විමසුම යවන්න', 'Envoyer la demande')}</button>
<div class="form-note" id="eqNote">{T('Or message us directly on WhatsApp — faster for photos and artwork.', 'නැත්නම් කෙලින්ම WhatsApp කරන්න — ඡායාරූප සහ artwork සඳහා වේගවත්.', 'Ou écrivez-nous sur WhatsApp — plus rapide pour les visuels.')}</div>
</form>
</section>
<section>
<div class="eyebrow">{T('Offices', 'කාර්යාල', 'Bureaux')}</div>
<h2>{T('Sri Lanka &amp; France', 'ශ්‍රී ලංකා සහ ප්‍රංශය', 'Sri Lanka et France')}</h2>
<div class="grid">
<div class="card"><h3>🇱🇰 {T('Sri Lanka', 'ශ්‍රී ලංකාව', 'Sri Lanka')}</h3><p>{T('Head office — hotline +94 78 860 7143, WhatsApp +94 76 860 7143. Business hours: 9 AM – 7 PM (Mon–Sat).', 'ප්‍රධාන කාර්යාලය — hotline +94 78 860 7143, WhatsApp +94 76 860 7143. ව්‍යාපාරික වේලාවන්: පෙ.ව. 9 – ප.ව. 7 (සඳුදා–සෙනසුරාදා).', 'Siège — ligne directe +94 78 860 7143, WhatsApp +94 76 860 7143. Horaires : 9 h – 19 h (lun–sam).')}</p></div>
<div class="card"><h3>🇫🇷 {T('France', 'ප්‍රංශය', 'France')}</h3><p>{T('European branch — WhatsApp +33 7 44 28 42 69. Serving travellers and French-speaking clients.', 'යුරෝපීය ශාඛාව — WhatsApp +33 7 44 28 42 69. සංචාරකයන් සහ ප්‍රංශ භාෂාව කතා කරන සේවාලාභීන්ට.', 'Succursale européenne — WhatsApp +33 7 44 28 42 69. Voyageurs et clients francophones.')}</p></div>
</div>
</section>
"""


# ----------------------------------------------------------------------------
# LEARN & EARN — professional courses
# ----------------------------------------------------------------------------

COURSES = [
    dict(ico='📣', en='Digital Marketing &amp; Social Media', si='ඩිජිටල් මාර්කටින් හා සමාජ මාධ්‍ය',
         fr='Marketing digital &amp; réseaux sociaux',
         den='Facebook, Instagram and TikTok ads, content calendars, offers that sell, and the numbers that actually matter.',
         dsi='Facebook, Instagram සහ TikTok ads, content calendars, විකුණන offers සහ ඇත්තටම වැදගත් numbers.',
         dfr='Publicités Facebook, Instagram et TikTok, calendriers de contenu, offres qui vendent et chiffres utiles.',
         meta=['8 weeks', 'Beginner friendly', 'English / Sinhala', 'Certificate']),
    dict(ico='🤖', en='AI for Business &amp; Automation', si='ව්‍යාපාරයට AI හා automation',
         fr='IA pour l’entreprise et automatisation',
         den='Chatbots, prompt writing, WhatsApp automation, AI customer care and CRM workflows — the skills every business now asks for.',
         dsi='Chatbots, prompt ලිවීම, WhatsApp automation, AI customer care සහ CRM workflows — දැන් හැම ව්‍යාපාරයක්ම ඉල්ලන නිපුණතා.',
         dfr='Chatbots, rédaction de prompts, automatisation WhatsApp, service client IA et CRM.',
         meta=['6 weeks', 'No coding needed', 'English / Sinhala', 'Certificate']),
    dict(ico='💻', en='Web Design &amp; Development', si='වෙබ් නිර්මාණ හා සංවර්ධන',
         fr='Création et développement web',
         den='Build real websites and admin panels — HTML, CSS, JavaScript, hosting, SEO and going live for a paying client.',
         dsi='සැබෑ වෙබ් අඩවි සහ admin panels හදන්න — HTML, CSS, JavaScript, hosting, SEO සහ client එකෙකුට deliver කිරීම.',
         dfr='Créer de vrais sites et panneaux admin — HTML, CSS, JavaScript, hébergement, SEO et mise en ligne.',
         meta=['10 weeks', 'Laptop needed', 'English / Sinhala', 'Portfolio project']),
    dict(ico='🎨', en='Graphic Design', si='ග්‍රැෆික් නිර්මාණ', fr='Design graphique',
         den='Flyers, posters, menus, packaging and social creatives — layout and colour rules that make people buy.',
         dsi='Flyers, posters, menu, packaging සහ social creatives — මිනිසුන් විකුණුමට ගෙනෙන layout සහ colour නීති.',
         dfr='Flyers, affiches, menus, emballage et visuels sociaux — la mise en page qui fait vendre.',
         meta=['8 weeks', 'Phone or laptop', 'English / Sinhala', 'Certificate']),
    dict(ico='🎬', en='Video Editing &amp; Content Creation', si='වීඩියෝ එඩිටින් හා content නිර්මාණය',
         fr='Montage vidéo et création de contenu',
         den='Reels, shorts and promo videos: shoot planning, editing, subtitles, sound and publishing for reach.',
         dsi='Reels, shorts සහ promo වීඩියෝ: shoot සැලසුම, editing, subtitles, sound සහ publish කිරීම.',
         dfr='Reels, shorts et vidéos promo : tournage, montage, sous-titres, son et publication.',
         meta=['6 weeks', 'Phone or laptop', 'English / Sinhala', 'Certificate']),
    dict(ico='📸', en='Photography &amp; Videography', si='ඡායාරූප හා වීඩියෝ ශිල්පය',
         fr='Photographie et vidéo',
         den='Camera basics, lighting, events, weddings, food and product shoots — finished with a real portfolio session.',
         dsi='Camera මූලික, lighting, events, මංගල, food සහ product shoots — සැබෑ portfolio session එකකින් අවසන්.',
         dfr='Bases de la caméra, lumière, événements, mariages, food et produits — avec une vraie séance portfolio.',
         meta=['8 weeks', 'Camera or phone', 'English / Sinhala', 'Portfolio project']),
    dict(ico='🖨️', en='Print &amp; Packaging Business', si='මුද්‍රණ හා packaging ව්‍යාපාරය',
         fr='Impression et emballage',
         den='Offset printing, paper bags, food packing, labels, quoting, sourcing and handling print clients profitably.',
         dsi='Offset මුද්‍රණ, paper bags, food packing, labels, මිල ගණන් දීම, sourcing සහ print clients කළමනාකරණය.',
         dfr='Impression offset, sacs papier, emballages alimentaires, étiquettes, devis et gestion des clients.',
         meta=['4 weeks', 'For shop owners', 'English / Sinhala', 'Supplier list included']),
    dict(ico='✈️', en='Travel &amp; Tourism Operations', si='සංචාරක මෙහෙයුම්', fr='Opérations touristiques',
         den='Itinerary building, hotel and vehicle booking, guest handling in English and French — the Ceylon Voyage way.',
         dsi='Itinerary හදන ආකාරය, hotel හා වාහන booking, English සහ ප්‍රංශ භාෂාවෙන් guests handling — Ceylon Voyage ක්‍රමයට.',
         dfr='Création d’itinéraires, réservations d’hôtels et véhicules, accueil des clients en anglais et français.',
         meta=['6 weeks', 'For tour staff', 'English / French', 'Job-ready']),
]

LEVELS = [
    ('LEVEL 1 · FOUNDATION', 'LEVEL 1 · ආධාරක', 'NIVEAU 1 · BASE', '$19',
     'Learn at your own pace', 'ඔබේ වේගයට ඉගෙන ගන්න', 'À votre rythme',
     'Recorded lessons plus a weekly live Q&amp;A class. Perfect if you have a job or studies and only a few hours a week.',
     'Recorded පාඩම් සහ සතිපතා live Q&amp;A පන්තියක්. රස්සාවක් හෝ ඉගෙනීමක් කරන අයට සතියකට පැය කිහිපයකින්.',
     'Leçons enregistrées et questions-réponses en direct chaque semaine. Idéal si vous travaillez ou étudiez.'),
    ('LEVEL 2 · PROFESSIONAL', 'LEVEL 2 · වෘත්තීය', 'NIVEAU 2 · PROFESSIONNEL', '$60',
     'Live classes + real project', 'Live පන්ති + සැබෑ ව්‍යාපෘතිය', 'Cours en direct + projet réel',
     'Live classes with a trainer, a real client-style project reviewed line by line, a portfolio and a Ceyteq certificate.',
     'පුහුණුකරු සමඟ live පන්ති, සැබෑ client ව්‍යාපෘතියක් පේළියෙන් පේළිය review කිරීම, portfolio එකක් සහ Ceyteq සහතිකයක්.',
     'Cours en direct, projet réel corrigé, portfolio et certificat Ceyteq.'),
    ('LEVEL 3 · ELITE (EARN)', 'LEVEL 3 · උපයන අවස්ථාව', 'NIVEAU 3 · ÉLITE', '$150',
     '1-on-1 + paid work', '1-on-1 + ගෙවන වැඩ', 'Coaching individuel + missions payées',
     'One-to-one mentorship, portfolio polish, freelancing and pricing coaching, plus paid projects handed over from Ceyteq’s own client queue.',
     'එකට එක mentorship, portfolio හදලා දීම, freelance සහ මිල ගණන් කියලා දීම, අපේම client queue එකෙන් ගෙවන ව්‍යාපෘති.',
     'Mentorat individuel, portfolio, coaching freelance et missions payées issues de notre vivier client.'),
]

LINK_ICONS = ['📣', '🤖', '💻', '🎨', '🎬', '📸', '🖨️', '✈️']


def learn_earn():
    cards = ''
    for c in COURSES:
        meta = ''.join(f'<span>{m}</span>' for m in c['meta'])
        cards += (f'<div class="course"><div class="ico">{c["ico"]}</div>'
                  f'<h3>{T(c["en"], c["si"], c["fr"])}</h3>'
                  f'<p>{T(c["den"], c["dsi"], c["dfr"])}</p>'
                  f'<div class="meta">{meta}</div></div>')

    levels = ''
    for tag_en, tag_si, tag_fr, fee, t_en, t_si, t_fr, d_en, d_si, d_fr in LEVELS:
        levels += (f'<div class="lvl"><div class="m">{T(tag_en, tag_si, tag_fr)}</div>'
                   f'<div class="d"><b>{T(t_en, t_si, t_fr)}</b>'
                   f'<p>{T(d_en, d_si, d_fr)}</p>'
                   f'<span class="fee">{fee} <span class="lang-en">per course</span>'
                   f'<span class="lang-si">එක් පාඨමාලාවකට</span>'
                   f'<span class="lang-fr">par formation</span></span></div></div>')

    courses_opts = ''.join(
        f'<option value="{c["en"].replace("&amp;", "&amp;amp;")}">{c["en"]}</option>' for c in COURSES)
    courses_opts += ('<option value="Career Bundle (all 8)">Career Bundle — all 8 courses</option>'
                     '<option value="Not sure yet">Not sure yet — advise me</option>')

    return hero('Learn &amp; Earn', 'ඉගෙන ගන්න, උපයන්න', 'Apprendre et gagner',
                'LEARN A SKILL. EARN FROM IT.',
                'නිපුණතාවක් ඉගෙන ගන්න. එයින් උපයන්න.',
                'APPRENEZ UNE COMPÉTENCE. GAGNEZ AVEC.',
                'Professional courses taught by the team that runs real client work every day — digital marketing, AI, web, design, video, photography, print and travel.',
                'දිනපතා සැබෑ client වැඩ කරන කණ්ඩායමෙන් වෘත්තීය පාඨමාලා — ඩිජිටල් මාර්කටින්, AI, වෙබ්, design, video, photography, මුද්‍රණ සහ සංචාරක.',
                'Formations professionnelles par l’équipe qui travaille chaque jour pour de vrais clients.') + f"""
<section>
<div class="eyebrow">{T('Why Ceyteq courses', 'ඇයි Ceyteq පාඨමාලා', 'Pourquoi nos formations')}</div>
<h2>{T('Taught by People Who Do the Work', 'වැඩේ ඇත්තටම කරන අයගෙන්', 'Enseigné par ceux qui font le travail')}</h2>
<div class="grid">
<div class="card"><h3>👩‍🏫 {T('Working trainers', 'වැඩ කරන පුහුණුකරුවන්', 'Formateurs en activité')}</h3><p>{T('Every trainer runs live client projects at Ceyteq — you learn what works this month, not a textbook from 2019.', 'හැම පුහුණුකරුවෙක්ම Ceyteq එකේ client ව්‍යාපෘති කරනවා — 2019 පොතක් නොවේ, මේ මාසේ වැඩ කරන දේ ඉගෙන ගන්නවා.', 'Chaque formateur travaille sur des projets clients — vous apprenez ce qui marche aujourd’hui.')}</p></div>
<div class="card"><h3>💼 {T('Earn while you learn', 'ඉගෙන ගන්න ගමන් උපයන්න', 'Gagnez en apprenant')}</h3><p>{T('Level 3 students get paid projects from our own client queue, with a fixed rate and a deadline — real experience on a CV.', 'Level 3 සිසුන්ට අපේ client queue එකෙන් ගෙවන ව්‍යාපෘති — නියමිත මිලක් සහ දිනක් සමඟ. CV එකට සැබෑ පළපුරුද්දක්.', 'Les élèves de niveau 3 reçoivent des missions payées de notre vivier client.')}</p></div>
<div class="card"><h3>🏆 {T('Portfolio + certificate', 'Portfolio + සහතිකය', 'Portfolio + certificat')}</h3><p>{T('Finish with real work to show and a Ceyteq certificate — what hotels, restaurants and agencies ask for.', 'පෙන්නන්න සැබෑ වැඩ සහ Ceyteq සහතිකයක් — hotels, restaurants සහ agencies ඉල්ලන දේ.', 'Repartez avec de vrais travaux et un certificat Ceyteq.')}</p></div>
<div class="card"><h3>🕒 {T('Evenings &amp; weekends', 'හවස් වරු සහ සති අන්ත', 'Soirs et week-ends')}</h3><p>{T('Live classes in the evening and on weekends, online plus in-person sessions in Sri Lanka where available.', 'හවස් වරු සහ සති අන්තයේ live පන්ති — online සහ ශ්‍රී ලංකාවේ හැකි තැන්වල ප්‍රායෝගිකව.',
   'Cours en direct le soir et le week-end, en ligne et en présentiel au Sri Lanka.')}</p></div>
</div>
</section>

<section>
<div class="eyebrow">{T('Courses', 'පාඨමාලා', 'Formations')}</div>
<h2>{T('08 Professional Courses', 'වෘත්තීය පාඨමාලා 08', '08 formations professionnelles')}</h2>
<p class="lead">{T('Choose a course, then choose a level (Foundation, Professional or Elite). Every course follows the same three levels.',
                   'පාඨමාලාවක් තෝරන්න, පසුව මට්ටමක් (Foundation, Professional හෝ Elite). හැම පාඨමාලාවකටම මේ මට්ටම් තුනම තියෙනවා.',
                   'Choisissez une formation, puis un niveau (Base, Professionnel ou Élite).')}</p>
<div class="grid">{cards}</div>
</section>

<section>
<div class="eyebrow">{T('Levels &amp; fees', 'මට්ටම් සහ මිල', 'Niveaux et tarifs')}</div>
<h2>{T('Three Levels, Same Price for Every Course', 'මට්ටම් තුනක්, හැම පාඨමාලාවකටම එකම මිල', 'Trois niveaux, même prix')}</h2>
<div class="timeline">{levels}</div>
<div class="hlbox"><b>{T('Career Bundle — all 8 courses + Level 3 mentorship: $250', 'Career Bundle — පාඨමාලා 8ම + Level 3 mentorship: $250', 'Pack Carrière — les 8 formations + mentorat : 250 $')}</b>
<span>{T('One payment, every skill, and the best chance of paid work at the end.', 'එකම ගෙවීමක්, හැම නිපුණතාවක්ම, අවසානයේ ගෙවන වැඩක් ලැබීමේ හොඳම අවස්ථාව.', 'Un paiement, toutes les compétences, et la meilleure chance de missions payées.')}</span></div>
<p class="note" style="margin-top:14px;color:#67787a">{T('Fees are in USD; LKR accepted at the day’s rate. Group and company packages, instalments and in-house training for staff teams: ask on WhatsApp.',
   'මිල ඩොලර් වලින්; දවසේ අනුපාතයට රුපියල් වලින් ගෙවිය හැක. කණ්ඩායම් සහ ආයතන පැකේජ, වාරික ගෙවීම් සහ staff පුහුණුව: WhatsApp එකෙන් අහන්න.',
   'Tarifs en USD ; LKR acceptés au taux du jour. Offres groupes, entreprises et paiements échelonnés : demandez sur WhatsApp.')}</p>
</section>

<section>
<div class="eyebrow">{T('How it works', 'වැඩ කරන ආකාරය', 'Comment ça marche')}</div>
<h2>{T('Enrol in Three Steps', 'පියවර තුනකින් ලියාපදිංචි වන්න', 'Inscription en trois étapes')}</h2>
<div class="grid">
<div class="card"><h3>1️⃣ {T('Send the form or WhatsApp', 'form එක යවන්න හෝ WhatsApp කරන්න', 'Formulaire ou WhatsApp')}</h3><p>{T('Tell us the course and level you want. We answer with the next intake date and payment details.', 'කැමති පාඨමාලාව සහ මට්ටම කියන්න. ඊළඟ batch දිනය සහ ගෙවීම් විස්තර සමඟ අපි පිළිතුරු දෙනවා.', 'Dites-nous la formation et le niveau. Nous répondons avec la prochaine date et le paiement.')}</p></div>
<div class="card"><h3>2️⃣ {T('Learn with a working team', 'වැඩ කරන කණ්ඩායමක් සමඟ ඉගෙන ගන්න', 'Apprenez avec une équipe active')}</h3><p>{T('Live classes, recorded lessons, real projects and honest feedback every week.', 'Live පන්ති, recorded පාඩම්, සැබෑ ව්‍යාපෘති සහ හැම සතියකම අවංක feedback.', 'Cours en direct, leçons enregistrées, projets réels et retours honnêtes.')}</p></div>
<div class="card"><h3>3️⃣ {T('Start earning', 'උපයන්න පටන්ගන්න', 'Commencez à gagner')}</h3><p>{T('Build your portfolio, take paid work from our queue, or apply the skills in your own business.', 'Portfolio හදන්න, අපේ queue එකෙන් ගෙවන වැඩ ගන්න, නැත්නම් ඔබේම ව්‍යාපාරයට යොදන්න.', 'Construisez votre portfolio, prenez des missions payées ou appliquez dans votre activité.')}</p></div>
</div>
</section>

<section>
<div class="eyebrow">{T('Who can join', 'කවුරුත් එකතු වෙන්න පුළුවන්', 'Qui peut participer')}</div>
<h2>{T('No Experience Needed', 'පළපුරුද්ද අවශ්‍ය නෑ', 'Aucune expérience requise')}</h2>
{blk('Open to', 'විවෘතයි', 'Ouvert à', items=[
    'School leavers', 'Students', 'Job seekers', 'Employees wanting side income',
    'Shop &amp; restaurant owners', 'Freelancers', 'Job seekers for hotels / agencies',
    'Company staff teams (in-house training)'])}
</section>

<section>
<div class="eyebrow">{T('Enrol now', 'දැන් ලියාපදිංචි වන්න', 'Inscrivez-vous')}</div>
<h2>{T('Save Your Seat', 'ඔබේ අසුන සුරකින්න', 'Réservez votre place')}</h2>
<p class="lead">{T('Send this form — we reply with the next intake date, the schedule and payment details. Or message us on WhatsApp.',
                   'මේ form එක යවන්න — ඊළඟ batch දිනය, කාලසටහන සහ ගෙවීම් විස්තර සමඟ අපි පිළිතුරු දෙනවා. නැත්නම් WhatsApp කරන්න.',
                   'Envoyez ce formulaire — nous répondons avec la prochaine session, le planning et le paiement.')}</p>
<form class="enquiry" id="enquiryForm" onsubmit="return sendEnquiry(event)">
<input id="eqName" required maxlength="120" placeholder="Your name / ඔබේ නම" autocomplete="name">
<input id="eqContact" required maxlength="60" placeholder="WhatsApp / phone number / දුරකථන අංකය" autocomplete="tel">
<input id="eqEmail" type="email" maxlength="160" placeholder="Email (optional)">
<select id="eqService">{courses_opts}</select>
<textarea id="eqMsg" required maxlength="2000" rows="4" placeholder="Which course and level? Any questions? / කැමති පාඨමාලාව සහ මට්ටම?"></textarea>
<button class="btn btn-red" type="submit" id="eqBtn">{T('Send enrolment', 'ලියාපදිංචි වීම යවන්න', 'Envoyer l’inscription')}</button>
<div class="form-note" id="eqNote">{T('Prefer WhatsApp? Send the same details and we will enrol you there.', 'WhatsApp කැමතිද? එම විස්තර එවන්න, එතනින්ම ලියාපදිංචි කරනවා.', 'WhatsApp ? Envoyez les mêmes détails.')}</div>
</form>
</section>

<section>
<div class="eyebrow">{T('Questions', 'ප්‍රශ්න', 'Questions')}</div>
<h2>{T('Course FAQ', 'පාඨමාලා ගැන ප්‍රශ්න', 'FAQ des formations')}</h2>
<details open><summary>{T('Do I need a laptop or experience?', 'Laptop එකක් හෝ පළපුරුද්දක් ඕනද?', 'Faut-il un ordinateur ou de l’expérience ?')}</summary><p>{T('No experience at all is fine. Marketing, design, AI and video courses can be done with a phone; web design needs a laptop — we will tell you the cheapest option that works.', 'පළපුරුද්දක් නැතත් කමක් නෑ. මාර්කටින්, design, AI සහ වීඩියෝ පාඨමාලා phone එකකින් කරන්න පුළුවන්; වෙබ් design සඳහා laptop එකක් ඕන — ලාබම විකල්පය අපි කියනවා.', 'Aucune expérience requise. Les formations marketing, design, IA et vidéo se font avec un téléphone ; le web nécessite un ordinateur.')}</p></details>
<details><summary>{T('Are classes online or physical?', 'පන්ති online ද physical ද?', 'Cours en ligne ou en présentiel ?')}</summary><p>{T('Live online classes (Zoom / WhatsApp) plus in-person sessions in Sri Lanka where available. Both are recorded so you never miss a class.', 'Live online පන්ති (Zoom / WhatsApp) සහ ශ්‍රී ලංකාවේ හැකි තැන්වල ප්‍රායෝගික පන්ති. දෙකම record වෙනවා, එක පන්තියක්වත් මගහැරෙන්නේ නෑ.', 'Cours en direct en ligne et sessions en présentiel au Sri Lanka. Tout est enregistré.')}</p></details>
<details><summary>{T('Will I really earn money?', 'ඇත්තටම සල්ලි හම්බවෙනවාද?', 'Vais-je vraiment gagner de l’argent ?')}</summary><p>{T('Honest answer: nobody can guarantee income. What we do guarantee is training on live methods, a real portfolio, and a place in our freelance queue — top students get paid projects from Ceyteq clients.', 'අවංක පිළිතුර: ආදායමක් කවුරුත් සහතික කරන්න බෑ. අපි සහතික කරන දේ: ජීවමාන ක්‍රම මත පුහුණුව, සැබෑ portfolio එකක් සහ අපේ freelance queue එකේ අවස්ථාවක් — හොඳම සිසුන්ට Ceyteq clients වෙතින් ගෙවන ව්‍යාපෘති.', 'Réponse honnête : personne ne peut garantir un revenu. Nous garantissons une formation sur des méthodes réelles, un portfolio et une place dans notre file de missions.')}</p></details>
<details><summary>{T('How long is a course?', 'පාඨමාලාවක් කොච්චර කල්ද?', 'Combien de temps ?')}</summary><p>{T('Level 1: 4 weeks. Level 2: 6–10 weeks depending on the course. Level 3: 12 weeks of mentorship with paid work.', 'Level 1: සති 4. Level 2: පාඨමාලාව අනුව සති 6–10. Level 3: ගෙවන වැඩ සමඟ සති 12 mentorship.', 'Niveau 1 : 4 semaines. Niveau 2 : 6 à 10 semaines. Niveau 3 : 12 semaines de mentorat.')}</p></details>
<details><summary>{T('Do you train company staff?', 'ආයතනවල staff පුහුණු කරනවාද?', 'Formez-vous les équipes d’entreprise ?')}</summary><p>{T('Yes — in-house training for restaurants, hotels and shops (menus, bookings, ads, AI answering). Ask for a team quotation.', 'ඔව් — restaurants, hotels සහ කඩ සඳහා ආයතනික පුහුණුව (menu, bookings, ads, AI පිළිතුරු). කණ්ඩායම් මිලක් අහන්න.', 'Oui — formation en entreprise pour restaurants, hôtels et commerces. Demandez un devis.')}</p></details>
</section>
"""
