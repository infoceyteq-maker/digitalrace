#!/usr/bin/env python3
"""Ceyteq Digital Race — 10 Flyer Generator (1080x1350, bilingual EN+SI)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from PIL.ImageFont import Layout
import os

W, H = 1080, 1350
ROOT = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(ROOT, 'assets')
OUT = os.path.join(ROOT, 'flyers')
os.makedirs(OUT, exist_ok=True)

BG_TOP = (5, 13, 25)
BG_BOT = (11, 44, 78)
CYAN = (0, 208, 255)
CYAN_DEEP = (0, 150, 220)
WHITE = (255, 255, 255)
MUTED = (188, 203, 218)
SI_COLOR = (155, 233, 255)
NAVY = (6, 20, 36)
GOLD = (255, 196, 66)

def F(name, size):
    return ImageFont.truetype(f'{A}/{name}', size, layout_engine=Layout.RAQM)

FONTS = {
    'display': lambda s: F('Montserrat-Black.ttf', s),
    'heading': lambda s: F('Montserrat-ExtraBold.ttf', s),
    'sub': lambda s: F('Montserrat-Bold.ttf', s),
    'body_b': lambda s: F('Inter-Bold.ttf', s),
    'body_sb': lambda s: F('Inter-SemiBold.ttf', s),
    'body': lambda s: F('Inter-Regular.ttf', s),
    'si_b': lambda s: F('Sinhala-Bold.ttf', s),
    'si': lambda s: F('Sinhala-Regular.ttf', s),
}

def gradient_bg():
    img = Image.new('RGB', (W, H), BG_TOP)
    px = img.load()
    for y in range(H):
        t = y / H
        r = int(BG_TOP[0] + (BG_BOT[0]-BG_TOP[0])*t)
        g = int(BG_TOP[1] + (BG_BOT[1]-BG_TOP[1])*t)
        b = int(BG_TOP[2] + (BG_BOT[2]-BG_TOP[2])*t)
        for x in range(0, W, 4):
            px[x, y] = (r, g, b)
            px[x+1, y] = (r, g, b)
            px[x+2, y] = (r, g, b)
            px[x+3, y] = (r, g, b)
    # grid overlay
    grid = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    for x in range(0, W, 90):
        gd.line([(x, 0), (x, H)], fill=(255, 255, 255, 9))
    for y in range(0, H, 90):
        gd.line([(0, y), (W, y)], fill=(255, 255, 255, 9))
    # glow orbs
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    gd2 = ImageDraw.Draw(glow)
    gd2.ellipse([W-420, -160, W+120, 340], fill=(0, 200, 255, 55))
    gd2.ellipse([-260, H-560, 320, H-60], fill=(40, 120, 255, 50))
    gd2.ellipse([W-300, H-420, W+80, H-120], fill=(0, 220, 255, 30))
    glow = glow.filter(ImageFilter.GaussianBlur(60))
    img = Image.alpha_composite(img.convert('RGBA'), grid)
    img = Image.alpha_composite(img, glow)
    return img.convert('RGB')

def wrap(draw, text, font, max_w):
    words, lines, cur = text.split(), [], ''
    for w_ in words:
        t = (cur + ' ' + w_).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def center(draw, cx, y, text, font, fill):
    draw.text((cx - draw.textlength(text, font=font)/2, y), text, font=font, fill=fill)

def draw_header(img, num):
    d = ImageDraw.Draw(img, 'RGBA')
    # logo badge (wide, cropped logo)
    d.rounded_rectangle([56, 50, 366, 180], radius=26, fill=(255, 255, 255, 255))
    try:
        logo = Image.open(f'{A}/logo-crop.jpg').convert('RGB')
        logo.thumbnail((286, 106), Image.LANCZOS)
        lx = 56 + (310 - logo.size[0]) // 2
        ly = 50 + (130 - logo.size[1]) // 2
        img.paste(logo, (lx, ly))
    except Exception as e:
        print('logo fail', e)
    d.text((392, 58), 'CEYTEQ', font=FONTS['display'](62), fill=WHITE)
    d.text((394, 132), 'EMPOWERING DIGITAL EVOLUTION', font=FONTS['body_b'](21), fill=CYAN)
    # pill
    pill = f'{num:02d} / 10'
    d.rounded_rectangle([W-236, 58, W-56, 118], radius=30, outline=CYAN, width=3)
    center(d, W-146, 68, pill, FONTS['body_b'](26), CYAN)

def draw_footer(img):
    d = ImageDraw.Draw(img, 'RGBA')
    band_h = 148
    y0 = H - band_h
    for y in range(y0, H):
        t = (y - y0) / band_h
        c = (int(0 + 0*t), int(208 - 48*t), int(255 - 45*t))
        d.line([(0, y), (W, y)], fill=c)
    d.line([(0, y0), (W, y0)], fill=(255, 255, 255, 200), width=3)
    center(d, W/2, y0+18, 'Hotline +94 78 860 7143   •   WhatsApp +94 76 860 7143', FONTS['heading'](29), NAVY)
    center(d, W/2, y0+62, 'info.ceyteq@gmail.com', FONTS['body_b'](27), NAVY)
    center(d, W/2, y0+98, 'FB • IG • TikTok • YouTube • LinkedIn   @ceyteq', FONTS['body_sb'](23), (10, 40, 70))

def draw_card(img, y, head, lines, accent=CYAN, min_h=0):
    """lines: list of (text, fontkey, size, color). Returns bottom y."""
    d = ImageDraw.Draw(img, 'RGBA')
    tmp = ImageDraw.Draw(img)
    max_w = 860
    rendered = []
    h_total = 30
    head_font = FONTS['heading'](31)
    hl = wrap(tmp, head, head_font, max_w)
    for t in hl:
        rendered.append((t, head_font, WHITE, 40))
        h_total += 40
    h_total += 6
    for (text, fk, size, color) in lines:
        f = FONTS[fk](size)
        lh = int(size * 1.42)
        for t in wrap(tmp, text, f, max_w):
            rendered.append((t, f, color, lh))
            h_total += lh
    h_total += 26
    h_total = max(h_total, min_h)
    x0, x1 = 56, W - 56
    d.rounded_rectangle([x0, y, x1, y + h_total], radius=24, fill=(255, 255, 255, 15))
    d.rounded_rectangle([x0, y, x1, y + h_total], radius=24, outline=(255, 255, 255, 40), width=2)
    d.rounded_rectangle([x0+14, y+20, x0+26, y+h_total-20], radius=6, fill=accent + (255,))
    cy = y + 28
    for (t, f, color, lh) in rendered:
        d.text((x0+52, cy), t, font=f, fill=color)
        cy += lh
    return y + h_total

def draw_price(img, y, big, big_sub, right_lines):
    d = ImageDraw.Draw(img, 'RGBA')
    x0, x1, hh = 56, W-56, 190
    for yy in range(y, y+hh):
        t = (yy-y)/hh
        c = (int(0+0*t), int(215-55*t), int(255-60*t))
        d.line([(x0+2, yy), (x1-2, yy)], fill=c)
    # round corners effect: overlay rounded mask
    mask = Image.new('L', (x1-x0, hh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, x1-x0, hh], radius=24, fill=255)
    # redraw gradient inside rounded rect by compositing
    box = Image.new('RGBA', (x1-x0, hh), (0,0,0,0))
    bd = ImageDraw.Draw(box)
    for yy in range(hh):
        t = yy/hh
        bd.line([(0, yy), (x1-x0, yy)], fill=(int(0), int(215-55*t), int(255-60*t), 255))
    box.putalpha(mask)
    img.paste(box, (x0, y), box)
    d = ImageDraw.Draw(img, 'RGBA')
    d.text((x0+44, y+18), big, font=FONTS['display'](96), fill=NAVY)
    bw = d.textlength(big, font=FONTS['display'](96))
    d.text((x0+44, y+126), big_sub, font=FONTS['body_b'](25), fill=(8, 40, 70))
    rx = x0 + 44 + bw + 36
    tot_h = sum(int(size*1.5) for (_, _, size, _) in right_lines)
    ry = y + (hh - tot_h) // 2
    for (t, fk, size, color) in right_lines:
        d.text((rx, ry), t, font=FONTS[fk](size), fill=color)
        ry += int(size*1.5)
    return y + hh

def draw_tiers(img, y, rows):
    """rows: list of (tier, price, content)"""
    d = ImageDraw.Draw(img, 'RGBA')
    x0, x1 = 56, W-56
    rh = 76
    gap = 12
    total = len(rows)*(rh+gap)-gap
    for i, (tier, price, content) in enumerate(rows):
        ry = y + i*(rh+gap)
        d.rounded_rectangle([x0, ry, x1, ry+rh], radius=18, fill=(255, 255, 255, 15))
        d.rounded_rectangle([x0, ry, x0+250, ry+rh], radius=18, fill=CYAN+(255,))
        # fix right corners of cyan block
        d.rectangle([x0+232, ry, x0+250, ry+rh], fill=CYAN+(255,))
        center(d, x0+125, ry+8, tier, FONTS['heading'](27), NAVY)
        center(d, x0+125, ry+40, price, FONTS['body_b'](24), NAVY)
        d.text((x0+276, ry+20), content, font=FONTS['body_sb'](27), fill=WHITE)
    return y + total

def draw_highlight(img, y, text_en, text_si=None):
    d = ImageDraw.Draw(img, 'RGBA')
    tmp = ImageDraw.Draw(img)
    x0, x1 = 56, W-56
    f1 = FONTS['body_b'](28)
    lines = wrap(tmp, text_en, f1, x1-x0-80)
    hh = 26 + len(lines)*40 + (52 if text_si else 0) + 22
    d.rounded_rectangle([x0, y, x1, y+hh], radius=20, outline=GOLD, width=3, fill=(255, 196, 66, 22))
    cy = y + 22
    for t in lines:
        center(d, W/2, cy, t, f1, GOLD)
        cy += 40
    if text_si:
        center(d, W/2, cy+2, text_si, FONTS['si'](27), WHITE)
    return y + hh

def draw_titles(img, y, eyebrow, title_en, title_si=None, title_size=100, sub_en=None, sub_si=None, si_size=44):
    d = ImageDraw.Draw(img)
    center(d, W/2, y, eyebrow, FONTS['body_b'](24), CYAN)
    y += 44
    f = FONTS['display'](title_size)
    for t in wrap(d, title_en, f, W-120):
        center(d, W/2, y, t, f, WHITE)
        y += int(title_size*1.08)
    y += 2
    if title_si:
        fs = FONTS['si_b'](si_size)
        for t in wrap(d, title_si, fs, W-120):
            center(d, W/2, y, t, fs, SI_COLOR)
            y += int(si_size*1.42)
    if sub_en:
        y += 6
        center(d, W/2, y, sub_en, FONTS['heading'](33), CYAN)
        y += 48
    if sub_si:
        center(d, W/2, y, sub_si, FONTS['si'](30), MUTED)
        y += 44
    # divider
    y += 8
    d.line([(W/2-260, y), (W/2+260, y)], fill=CYAN, width=3)
    for gx in range(-260, 261, 4):
        pass
    y += 22
    return y

def build(num, slug, eyebrow, title_en, title_si, title_size, sub_en, sub_si, blocks, si_size=44):
    img = gradient_bg()
    draw_header(img, num)
    y = draw_titles(img, 218, eyebrow, title_en, title_si, title_size, sub_en, sub_si, si_size)
    for b in blocks:
        y += 14
        if b[0] == 'card':
            _, head, lines = b
            y = draw_card(img, y, head, lines)
        elif b[0] == 'price':
            _, big, sub, right = b
            y = draw_price(img, y, big, sub, right)
        elif b[0] == 'tiers':
            y = draw_tiers(img, y, b[1])
        elif b[0] == 'hl':
            _, en, si = b
            y = draw_highlight(img, y, en, si)
    draw_footer(img)
    img.save(f'{OUT}/flyer-{num:02d}-{slug}.png')
    print(f'saved flyer {num} {slug} end_y={y} (footer at {H-148})')
    return y

os.makedirs(OUT, exist_ok=True)

# ---------------- FLYER 1: PROGRAM INTRO ----------------
build(1, 'program-intro',
  'CEYTEQ PRESENTS  •  B2B DIGITAL TRANSFORMATION',
  'DIGITAL RACE', 'ඩිජිටල් රේස් වැඩසටහන', 94,
  'Upgrade Your Business', 'ඔබේ ව්‍යාපාරය ඩිජිටල් යුගයට උසස් කරන්න',
  [
    ('card', 'WHAT IS IT?',
      [("A 90-day hands-on program turning your restaurant or shop into an online sales machine.", 'body', 27, MUTED),
       ("ඔබේ ව්‍යාපාරය online විකුණුම් යන්ත්‍රයක් බවට පත් කරන දින 90 වැඩසටහන.", 'si', 26, SI_COLOR)]),
    ('card', 'ALIEN MARKETING MATRIX METHOD',
      [("An unconventional, hyper-efficient web marketing system. Morning + evening campaign matrices.", 'body', 27, MUTED),
       ("අතිශය කාර්යක්ෂම නවීන marketing ක්‍රමයක්.", 'si', 26, SI_COLOR)]),
    ('hl', "We don't just build websites. We deploy sales engines.", "Website එකක් විතරක් නෙවෙයි — විකුණුම් යන්ත්‍රයක්."),
  ])

# ---------------- FLYER 2: WHY NOW / SL STATUS ----------------
build(2, 'why-now',
  'THE RACE IS ON  •  SRI LANKA',
  'GO DIGITAL OR GET LEFT BEHIND', 'ඩිජිටල් නොවුණොත් පිටුපසින්', 54,
  None, None,
  [
    ('card', 'CUSTOMERS ARE ONLINE',
      [("Sri Lankans order food and shop by phone every single day.", 'body', 26, MUTED),
       ("ලංකාවේ customersලා දවසේම phone එකෙන් order කරනවා.", 'si', 26, SI_COLOR)]),
    ('card', 'MOST SHOPS ARE STILL OFFLINE',
      [("No website. No online orders. Orders go to competitors.", 'body', 26, MUTED),
       ("බොහෝ කඩවල website එකක්වත්, order ක්‍රමයක්වත් නෑ.", 'si', 26, SI_COLOR)]),
    ('card', 'EARLY MOVERS WIN',
      [("First to go digital wins Google, Maps and social media.", 'body', 26, MUTED),
       ("කලින් digital වෙන අය Google, Maps, social ජය ගන්නවා.", 'si', 26, SI_COLOR)]),
    ('hl', "Going digital is no longer an option — it's a race.", "Digital වීම විකල්පයක් නොවෙයි — එය තරඟයක්."),
  ], si_size=38)

# ---------------- FLYER 3: WHAT CHANGES ----------------
build(3, 'what-changes',
  'FROM SHOP TO SALES ENGINE',
  'WHAT THE PROGRAM CHANGES', 'වැඩසටහනෙන් ලැබෙන වෙනස', 62,
  None, None,
  [
    ('card', '1  •  ONLINE ORDERING',
      [("Web panel + WhatsApp orders. No missed calls, no lost orders.", 'body', 28, MUTED),
       ("Web panel + WhatsApp orders. ඇණවුම් අතපසු නොවේ.", 'si', 27, SI_COLOR)]),
    ('card', '2  •  MONTHLY MARKETING MACHINE',
      [("Videos + flyers every month on Facebook, Instagram, TikTok, YouTube.", 'body', 28, MUTED),
       ("හැම මාසෙම videos + flyers. Social media පුරා ප්‍රචාරය.", 'si', 27, SI_COLOR)]),
    ('card', '3  •  TRAINED TEAM + AI AUTOMATION',
      [("Staff trained on digital. Chatbots serve customers 24/7.", 'body', 28, MUTED),
       ("Staff පුහුණු වෙනවා. Chatbotලා 24/7 customersලා බලාගන්නවා.", 'si', 27, SI_COLOR)]),
  ])

# ---------------- FLYER 4: HOW IT WORKS ----------------
build(4, 'how-it-works',
  'ALIEN MARKETING MATRIX METHOD',
  'HOW THE MATRIX WORKS', 'මැට්‍රික්ස් ක්‍රමය වැඩ කරන හැටි', 66,
  None, None,
  [
    ('card', 'MORNING MATRIX  •  6 AM – 11 AM',
      [("Breakfast & lunch crowd campaigns. Catch customers early.", 'body', 28, MUTED),
       ("උදේ customersලා ඉලක්ක කරගත් ප්‍රචාරණ.", 'si', 27, SI_COLOR)]),
    ('card', 'EVENING MATRIX  •  12 PM – 9 PM',
      [("Dinner & peak-hour push. Maximum orders at maximum hours.", 'body', 28, MUTED),
       ("හවස peak hours ඉලක්ක කරගත් ප්‍රචාරණ.", 'si', 27, SI_COLOR)]),
    ('card', 'ONLY $1–$2 / DAY AD SPEND',
      [("You pay Meta/TikTok directly. Ceyteq setup & optimization is FREE.", 'body', 28, MUTED),
       ("ඔබ platforms වලටම ගෙවන්න. Ceyteq optimization නොමිලේ.", 'si', 27, SI_COLOR)]),
  ])

# ---------------- FLYER 5: 90-DAY TRAINING ----------------
build(5, 'training-90-day',
  'PRACTICAL TRAINING & SUPPORT  •  90 DAYS',
  '3-MONTH SUCCESS ROADMAP', 'මාස 3 සාර්ථක මාවත', 62,
  None, None,
  [
    ('card', 'MONTH 1  •  FOUNDATION (DAY-BY-DAY)',
      [("Daily coaching: web panel, WhatsApp bot orders, $1–$2 ads, promos, staff training.", 'body', 27, MUTED),
       ("දිනපතා පුහුණුව: panel එක, ads, staff පුහුණුව.", 'si', 27, SI_COLOR)]),
    ('card', 'MONTH 2  •  OPTIMIZATION (WEEK-BY-WEEK)',
      [("Weekly analytics review. Tune morning + evening matrices. Sync kitchen with demand.", 'body', 27, MUTED),
       ("සතිපතා විශ්ලේෂණය සහ campaign tuning.", 'si', 27, SI_COLOR)]),
    ('card', 'MONTH 3  •  GROWTH & AUTOMATION',
      [("Full 90-day ROI audit. AI tools + automation. A self-running digital system.", 'body', 27, MUTED),
       ("ROI audit + AI automation. ස්වයංක්‍රීය ක්‍රමයක්.", 'si', 27, SI_COLOR)]),
  ])

# ---------------- FLYER 6: STARTER ----------------
build(6, 'package-starter',
  'PACKAGE 01  •  STARTER',
  'STARTER', 'ආරම්භක පැකේජය', 100,
  'Perfect first step online', None,
  [
    ('price', '$19', 'ONE-TIME SETUP', [('$3 – $5 / MONTH', 'heading', 34, NAVY), ('monthly matrix fee', 'body_b', 24, (8,40,70))]),
    ('card', 'SYSTEM + MONTHLY CONTENT',
      [("3–4 page custom website: brand colors, mobile responsive, direct WhatsApp ordering.", 'body', 27, MUTED),
       ("2 Videos + 4 Flyers every month.", 'body_b', 27, WHITE),
       ("මාසෙට videos 2 + flyers 4.", 'si', 26, SI_COLOR)]),
    ('hl', "Best for small shops starting online.", "Online යන්න පටන්ගන්න කුඩා කඩ සඳහා."),
  ])

# ---------------- FLYER 7: STANDARD ----------------
build(7, 'package-standard',
  'PACKAGE 02  •  STANDARD  •  MOST POPULAR',
  'STANDARD', 'සම්මත පැකේජය', 110,
  'Dynamic website + Admin Panel', 'Booking + menu කළමනාකරණය සමඟ',
  [
    ('price', '$60', 'ONE-TIME SETUP', [('High customization', 'heading', 30, NAVY), ('design matched to brand', 'body_b', 23, (8,40,70))]),
    ('tiers', [
      ('TIER 1', '$10/mo', '3 Videos + 4 Flyers'),
      ('TIER 2', '$15/mo', '5 Videos + 7 Flyers'),
      ('TIER 3', '$20/mo', '7 Videos + 10 Flyers'),
    ]),
  ])

# ---------------- FLYER 8: ADVANCED ----------------
build(8, 'package-advanced',
  'PACKAGE 03  •  ADVANCED',
  'ADVANCED', 'උසස් පැකේජය', 110,
  'Bookings + Analytics Dashboard', None,
  [
    ('price', '$80', 'ONE-TIME SETUP', [('FREE Messenger Chatbot', 'heading', 29, NAVY), ('Voice Caller Bot +$15/mo', 'body_b', 23, (8,40,70))]),
    ('tiers', [
      ('TIER 1', '$15/mo', '5 Videos + 7 Flyers'),
      ('TIER 2', '$20/mo', '7 Videos + 10 Flyers'),
      ('TIER 3', '$30/mo', '10 Videos + 15 Flyers'),
    ]),
  ])

# ---------------- FLYER 9: PREMIUM ----------------
build(9, 'package-premium',
  'PACKAGE 04  •  PREMIUM ULTIMATE',
  'PREMIUM ULTIMATE', 'ඉහළම පැකේජය', 68,
  '100% fully custom • 3D visuals • full backend control', None,
  [
    ('price', '$250', 'ONE-TIME SETUP', [('$150 / MONTH FLAT', 'heading', 33, NAVY), ('all-inclusive matrix', 'body_b', 24, (8,40,70))]),
    ('card', 'DUAL BOT SYSTEM INCLUDED',
      [("Text Messaging Bot + Voice Caller Bot. Full automation.", 'body', 28, MUTED),
       ("Text Bot + Voice Bot දෙකම. සම්පූර්ණ automation.", 'si', 27, SI_COLOR)]),
    ('card', 'MONTHLY CONTENT + ADS',
      [("15 Videos + 25 Flyers. Cross-platform + exclusive external ad placements.", 'body', 28, MUTED),]),
  ])

# ---------------- FLYER 10: AI + CONTACT ----------------
build(10, 'ai-future-contact',
  'FUTURE-READY  •  AI SOLUTIONS',
  'AI TODAY & TOMORROW', 'අද සහ හෙට AI විසඳුම්', 64,
  None, None,
  [
    ('card', 'TODAY  •  WHATSAPP + MESSENGER BOTS',
      [("Auto orders, bookings and replies 24/7. Never miss a customer.", 'body', 28, MUTED),
       ("Auto orders සහ replies 24/7.", 'si', 27, SI_COLOR)]),
    ('card', 'TODAY  •  VOICE CALLER BOT',
      [("AI answers calls, confirms orders and bookings for you.", 'body', 28, MUTED),
       ("AI calls වලට උත්තර දී orders තහවුරු කරනවා.", 'si', 27, SI_COLOR)]),
    ('card', 'TOMORROW  •  FULL AI AUTOMATION',
      [("Sales forecasts, smart promos, self-running marketing mindset.", 'body', 28, MUTED),
       ("ස්වයංක්‍රීය marketing අනාගතය.", 'si', 27, SI_COLOR)]),
    ('hl', "START YOUR DIGITAL RACE TODAY — Message us now!", "අදම Digital Race පටන්ගන්න — දැන් message කරන්න!"),
  ])

print('ALL DONE')
