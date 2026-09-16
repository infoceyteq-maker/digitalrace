#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEYTEQ — HotelMate featured-partner campaign layer (isolated and additive).

Everything the campaign owns lives in this one file: the approved colours, the
campaign WhatsApp number, the homepage featured-partner band, the Services
partner card, the /hotelmate.html campaign landing page, the UTM-aware WhatsApp
tracking and the campaign CSS.

WHY A SEPARATE MODULE
  The Ceyteq core content (content_services.py) and the 08 service divisions
  are not rewritten by this campaign. To remove the campaign entirely: delete
  the `import content_hotelmate` line, the two call sites in
  content_services.py, the HotelMate nav item and the hotelmate.html entries in
  build_site.py. The site is then 100% Ceyteq again, byte for byte.

CAMPAIGN RULES ENFORCED HERE
  * Ceyteq remains the main company brand; HotelMate is presented as a featured
    hospitality technology partner — never as "the official HotelMate partner"
    (that wording is not approved).
  * The offer is always written "for the campaign period"; it is never
    described as permanently free.
  * No testimonials, no customer logos, no guaranteed revenue or occupancy
    claims.
  * "Demo coordination by Ceyteq. Final product demo and activation are
    completed with the HotelMate team." appears on every HotelMate view.
  * Lead handoff is WhatsApp-only: the campaign form composes ONE message and
    navigates to wa.me — no fetch, no api/leads, no window.open, nothing
    stored. contact.html and learn-earn.html keep the Ceyteq backend form.

CLIENT ASSET STATUS (at the time of this build)
  assets/hotelmate-logo.png  — not in the repository yet. While it is missing
      the build renders a plain CSS wordmark instead of invented artwork. Drop
      the supplied logo in and re-run `python3 build_site.py`: every HotelMate
      mark switches to the real file automatically, with no code edit.
  hotelmate.html (client's own page) — also not supplied, so the landing page
      below is assembled from the approved written brief. The UTM passthrough is
      already wired, so merging the client's version later only changes copy.
"""

import os
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- palette ----
HM_BLUE = '#00AEEF'      # HotelMate brand blue — fills, rules, accents
HM_ACCENT = '#27A3C9'    # Ceyteq website accent blue (the site's --prime)
HM_NAVY = '#1A1A2E'      # campaign dark navy — panel backgrounds
# #00AEEF on white is 2.4:1 and fails WCAG AA, so small text on light
# backgrounds uses a darker shade of the same hue (4.9:1, passes AA).
# Every fill and border still uses the exact approved #00AEEF.
HM_BLUE_TEXT = '#0179AB'

# ---------------------------------------------------------------- contacts ---
WA_NUMBER = '94768607143'          # the one campaign number, used everywhere
WA_DISPLAY = '+94 76 860 7143'

SOCIAL = [
    ('Facebook', '📘', 'https://web.facebook.com/hotelmatepms/'),
    ('Instagram', '📸', 'https://www.instagram.com/hotelmate.hm/'),
    ('TikTok', '🎵', 'https://www.tiktok.com/@hotelmate.hm'),
]

# First message a campaign lead arrives with.
WA_TEXT = ('Hello Ceyteq — I would like to speak with a HotelMate specialist '
           'about my hotel/guest house. Please send the campaign offer '
           '(setup fee FREE for the campaign period, US$39/month for the first '
           '10 rooms) and book my demo.')

# First message for the LED screens/signage enquiry (Ceyteq service, quoted
# per job — the US$39/month HotelMate licence wording is deliberately NOT
# bundled into this message).
LED_TEXT = ('Hello Ceyteq — I would like to talk about HotelMate for my '
            'hotel/guest house, and about LED screens/signage for the lobby '
            'or entrance. Please send the details and a quote.')

# The mandated disclosure — this English wording must stay verbatim.
DISCLOSURE = ('Demo coordination by Ceyteq. Final product demo and activation '
              'are completed with the HotelMate team.')
DISCLOSURE_SI = ('ඩෙමෝ සම්බන්ධීකරණය Ceyteq විසින්. අවසාන product demo එක සහ '
                 'activation සිදු කරන්නේ HotelMate කණ්ඩායම සමඟයි.')
DISCLOSURE_FR = ('Coordination de la démo par Ceyteq. La démo finale du produit '
                 'et l’activation sont réalisées avec l’équipe HotelMate.')


def T(en, si, fr):
    """The trilingual span pattern the whole Ceyteq site uses."""
    return (f'<span class="lang-en">{en}</span>'
            f'<span class="lang-si">{si}</span>'
            f'<span class="lang-fr">{fr}</span>')


def wa_link(text=WA_TEXT):
    """Campaign WhatsApp URL. UTM_JS appends the visitor's campaign parameters
    to it at load/click time, so the lead stays attributed in the chat."""
    return 'https://wa.me/' + WA_NUMBER + '?text=' + quote(text, safe='')


# ------------------------------------------------------------------- logo ----
LOGO_CANDIDATES = ('assets/hotelmate-logo.png', 'assets/hotelmate-logo.svg',
                   'assets/hotelmate-logo.jpg', 'assets/hotelmate-logo.jpeg')


def logo_path():
    """The supplied HotelMate logo, or None while it has not been added."""
    for name in LOGO_CANDIDATES:
        if os.path.exists(os.path.join(ROOT, name)):
            return name
    return None


def mark():
    """HotelMate lockup. Uses the real logo file the moment it exists in
    assets/, otherwise a CSS wordmark — a fabricated logo is never shipped.
    The shared nav deliberately keeps the plain text label "HotelMate"."""
    src = logo_path()
    if src:
        return (f'<img class="hm-logo" src="{src}" alt="HotelMate logo" '
                f'width="240" height="60" loading="lazy" decoding="async">')
    return ('<span class="hm-mark">'
            '<span class="hm-dot" aria-hidden="true"></span>'
            'Hotel<span class="hm-mate">Mate</span></span>')


# ---------------------------------------------------------------- the CSS ----
# Split in two so unrelated Ceyteq pages do not pay for the campaign:
#   CSS_NAV  ships on every page (10 nav items -> the partner pill needs it)
#   CSS_PAGE ships only on the three pages that render campaign markup
# Every rule is scoped to .hm-* / #hotelmate / #partners / .offer / .steps, so
# no existing Ceyteq rule is redefined.
CSS_NAV = f"""
/* HotelMate campaign — shared nav only (see CSS_PAGE for the rest) */
:root{{--hm:{HM_BLUE};--hmacc:{HM_ACCENT};--hmnavy:{HM_NAVY};--hmd:{HM_BLUE_TEXT}}}
nav .links a.hm{{color:var(--hmd);font-weight:800;border:1.5px solid rgba(0,174,239,.55);
padding:6.5px 13px;background:#f4fbfe}}
nav .links a.hm:hover{{background:var(--hm);color:#06222c;border-color:var(--hm)}}
nav .links a.hm.active{{background:var(--hm);color:#06222c;border-color:var(--hm)}}
"""

# pages that need the campaign markup CSS (home band, services card, landing page)
PAGES_WITH_CAMPAIGN_CSS = ('index.html', 'services.html', 'hotelmate.html')

CSS_PAGE = f"""
/* ============ HotelMate featured-partner campaign (additive layer) ============ */
/* wordmark + logo slot */
.hm-mark{{display:inline-flex;align-items:center;gap:10px;font-weight:800;
letter-spacing:-.02em;line-height:1.15}}
.hm-mark .hm-dot{{width:12px;height:12px;border-radius:50%;background:var(--hm);flex:none;
box-shadow:0 0 0 4px rgba(0,174,239,.2)}}
.hm-mark .hm-mate{{color:var(--hm)}}
img.hm-logo{{height:auto;max-width:100%;width:240px;filter:drop-shadow(0 6px 18px rgba(0,174,239,.35))}}
/* featured-partner band (home) + campaign closing band */
#hotelmate{{border-top:3px solid var(--hm)}}
.hm-band{{background:linear-gradient(135deg,{HM_NAVY},{HM_NAVY} 55%,#242a4d);
border:1px solid rgba(0,174,239,.55);border-radius:20px;padding:34px 30px;margin:6px auto 0;
max-width:980px;box-shadow:0 20px 48px rgba(26,26,46,.28);position:relative;overflow:hidden}}
.hm-band::before{{content:'';position:absolute;left:0;right:0;top:0;height:4px;
background:linear-gradient(90deg,var(--hm),var(--hmacc),var(--hm))}}
.hm-band .kick{{color:#9fe3ff;font-weight:800;letter-spacing:3px;font-size:12.5px;text-transform:uppercase}}
.hm-band .ah{{font-size:clamp(23px,4.4vw,34px);font-weight:800;color:#fff;line-height:1.2;
margin:12px 0 4px;letter-spacing:-.03em;display:flex;flex-wrap:wrap;gap:12px;align-items:baseline}}
.hm-band .ah .lang-si{{display:block;font-size:.62em;color:#bfeafc;margin-top:8px;font-weight:600}}
.hm-band .ah .lang-fr{{font-size:.8em;color:#bfeafc}}
.hm-band p{{color:#dbeaf2;font-size:16px;margin-top:10px;max-width:820px}}
.hm-band .lang-si{{color:#bfeafc}}
.hm-band ul{{list-style:none;display:grid;gap:9px;margin:20px 0 0;
grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}}
.hm-band ul li{{background:rgba(255,255,255,.07);border:1px solid rgba(0,174,239,.35);
border-radius:10px;padding:11px 15px;font-size:14.5px;color:#e7f4fa}}
.hm-band ul li b{{color:#fff}}
/* buttons — approved fills with AA-contrast labels */
.btn-hm{{background:var(--hm);color:#06222c;box-shadow:0 10px 26px rgba(0,174,239,.34)}}
.btn-hm:hover{{background:#33c1f7;color:#06222c;transform:translateY(-2px)}}
.btn-wa{{background:#25d366;color:#06222c;box-shadow:0 10px 26px rgba(37,211,102,.3)}}
.btn-wa:hover{{background:#1ebe5b;color:#06222c;transform:translateY(-2px)}}
.hm-band .cta-row{{justify-content:flex-start;margin:22px 0 4px}}
/* ghost buttons must stay legible on the navy bands */
.hm-band .btn-ghost,.hm-hero .btn-ghost{{border-color:#9fe3ff;color:#e7f4fa;background:transparent}}
.hm-band .btn-ghost:hover,.hm-hero .btn-ghost:hover{{background:var(--hm);color:#06222c;border-color:var(--hm)}}
.hm-terms{{border:1px dashed rgba(0,174,239,.6);border-radius:10px;padding:12px 16px;margin-top:16px;
color:#fff;font-weight:700;background:rgba(0,174,239,.09);max-width:820px}}
/* the mandated disclosure line */
.hm-disclose{{display:flex;margin-top:20px;border-left:3px solid var(--hm);padding:2px 0 2px 14px}}
.hm-disclose small{{color:#bfe0ef;font-size:13.5px;line-height:1.55;font-weight:500}}
/* services.html — partner card under the 08 divisions */
.hm-partner{{background:linear-gradient(135deg,#fff,#f2fbff);border:1px solid rgba(0,174,239,.45);
border-top:4px solid var(--hm);border-radius:14px;padding:26px;margin-top:22px;
box-shadow:0 14px 36px rgba(26,26,46,.09);display:block;text-decoration:none;color:inherit;transition:.25s}}
a.hm-partner:hover{{transform:translateY(-4px);box-shadow:0 22px 46px rgba(0,174,239,.2);
border-color:var(--hm)}}
.hm-ribbon{{display:inline-block;background:var(--hm);color:#06222c;font-weight:800;font-size:11.5px;
letter-spacing:1.6px;text-transform:uppercase;border-radius:50px;padding:6px 15px}}
.hm-lock{{font-size:clamp(21px,4vw,29px);font-weight:800;color:var(--hmnavy);margin:14px 0 8px;
letter-spacing:-.03em}}
.hm-partner p{{font-size:15.5px;color:var(--mut)}}
.hm-tags{{margin:14px 0 0;padding:0;list-style:none;display:flex;flex-wrap:wrap;gap:7px}}
.hm-tags li{{background:#f2fbff;border:1px solid rgba(0,174,239,.4);border-radius:50px;
padding:5px 13px;font-size:12.5px;color:var(--hmd);font-weight:700}}
.hm-goto{{margin-top:16px;font-weight:800;color:var(--hmd);font-size:15px}}
/* campaign landing page */
.hm-hero{{background:linear-gradient(135deg,{HM_NAVY},#20233f 60%,{HM_NAVY});
border:1px solid rgba(0,174,239,.5);border-radius:22px;padding:44px 32px;margin:26px 0 4px;
box-shadow:0 22px 54px rgba(26,26,46,.3);position:relative;overflow:hidden;text-align:center}}
.hm-hero::before{{content:'';position:absolute;left:0;right:0;top:0;height:5px;
background:linear-gradient(90deg,var(--hm),var(--hmacc),var(--hm))}}
.hm-hero .kick{{color:#9fe3ff;font-weight:800;letter-spacing:3px;font-size:12.5px;text-transform:uppercase}}
.hm-hero .lock{{display:flex;justify-content:center;margin:16px 0 8px;font-size:clamp(28px,6vw,42px)}}
.hm-hero h1{{color:#fff;font-size:clamp(30px,5.4vw,52px)}}
.hm-hero h1 .lang-si{{color:#bfeafc;display:block;font-size:clamp(19px,3.8vw,28px);margin-top:10px;font-weight:600}}
.hm-hero h1 .lang-fr{{color:#bfeafc;font-size:clamp(18px,3.4vw,26px)}}
.hm-hero .lead{{color:#dbeaf2;max-width:780px;margin:14px auto 0;font-size:16.5px}}
.hm-hero .cta-row{{margin:26px 0 6px}}
.offer{{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));margin-top:24px}}
.offer .o{{background:#fff;border:1px solid var(--line);border-top:4px solid var(--hm);
border-radius:14px;padding:26px 24px;box-shadow:0 12px 32px rgba(12,30,33,.07)}}
.offer .o small{{display:block;color:var(--hmd);font-weight:800;letter-spacing:1.8px;font-size:11.5px;
text-transform:uppercase}}
.offer .o b{{display:block;font-size:clamp(21px,3.6vw,27px);color:var(--hmnavy);margin:10px 0 2px;
letter-spacing:-.02em;font-weight:800;line-height:1.25}}
.offer .o b.free{{color:var(--hmd)}}
.offer .o p{{font-size:14.5px;color:var(--mut);margin-top:10px}}
.hm-note{{background:#f2fbff;border:1px solid rgba(0,174,239,.4);border-radius:12px;
padding:16px 20px;margin-top:20px;font-size:14.5px;color:var(--mut);text-align:left}}
.hm-note b{{color:var(--hmnavy)}}
.steps{{display:grid;gap:14px;margin-top:24px}}
.step{{display:grid;grid-template-columns:60px 1fr;gap:16px;align-items:start;background:#fff;
border:1px solid var(--line);border-radius:12px;padding:20px 22px;box-shadow:0 10px 28px rgba(12,30,33,.06)}}
.step .n{{width:44px;height:44px;border-radius:50%;background:var(--hm);color:#06222c;
font-weight:800;display:flex;align-items:center;justify-content:center;font-size:18px}}
.step b{{display:block;font-size:17.5px;color:var(--hmnavy)}}
.step p{{font-size:15px;color:var(--mut);margin-top:5px}}
.social{{display:flex;gap:12px;flex-wrap:wrap;margin-top:20px}}
.social a{{display:inline-flex;align-items:center;gap:9px;text-decoration:none;font-weight:700;
font-size:14.5px;color:var(--hmnavy);background:#fff;border:1.5px solid rgba(0,174,239,.5);
border-radius:50px;padding:11px 20px;transition:.2s}}
.social a:hover{{background:var(--hm);border-color:var(--hm);color:#06222c;transform:translateY(-2px)}}
@media(max-width:640px){{.hm-band{{padding:26px 18px}}.hm-hero{{padding:30px 18px}}
.hm-partner{{padding:22px 18px}}.step{{grid-template-columns:44px 1fr;gap:12px;padding:16px}}
.btn{{font-size:15px;padding:13px 22px}}}}
@media(prefers-reduced-motion:reduce){{.hm-partner,.social a,.btn-hm,.btn-wa{{transition:none}}
.hm-partner:hover,.social a:hover,.btn-hm:hover,.btn-wa:hover{{transform:none}}}}
"""

# Shipped ONLY on hotelmate.html — the LED screens/signage block renders
# nowhere else, so index.html and services.html stay byte-identical to the
# pre-LED build (see check_hotelmate.py section 5).
CSS_LED = f"""
/* hotel extra — LED screens & signage (a Ceyteq service, quoted per job) */
.hm-extra{{list-style:none;margin:18px 0 0;padding:0;display:grid;gap:10px;
grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}}
.hm-extra li{{background:#f2fbff;border:1px solid rgba(0,174,239,.4);border-left:5px solid var(--hm);
border-radius:10px;padding:13px 18px;font-size:14.5px;color:var(--mut)}}
.hm-extra li b{{color:var(--hmnavy);display:block;font-size:15.5px;margin-bottom:3px}}
"""

# ------------------------------------------------- UTM-aware WhatsApp JS ----
# Keeps campaign tracking alive through the WhatsApp hand-off:
#   * every utm_* parameter (plus the ad-network click ids) on the page URL is
#     appended to each wa.me link, so tag managers and server logs see it;
#   * and a readable "Campaign:" footer is added to the pre-filled message, so
#     the lead arrives already attributed in the chat.
# Progressive enhancement only: fully guarded, ES5, adds nothing when the
# visitor arrives without campaign parameters, and never rewrites the phone
# number or the destination host.
UTM_JS = """
<script>
/* HotelMate campaign — UTM passthrough into the wa.me links. */
(function(){try{
var KEEP=/^(utm_|gclid|fbclid|gbraid|wbraid|twclid|ttclid|msclkid|dclid|ef_id|gclsrc|ref|cid|igsh)/;
var out=[];
try{
  var qs=(self.location&&location.search)?String(location.search).replace(/^\\?/,''):'';
  var parts=qs?qs.split('&'):[];
  for(var i=0;i<parts.length;i++){
    var kv=parts[i];if(!kv)continue;
    var k=decodeURIComponent(kv.split('=')[0]||'').replace(/[^a-zA-Z0-9_.\\-]/g,'');
    if(k.length>40||!KEEP.test(k+'='))continue;
    var v=decodeURIComponent((kv.split('=')[1]||'').replace(/\\+/g,' ')).slice(0,120);
    v=v.replace(/[^a-zA-Z0-9_.:@+\\/ \\-]/g,'');
    if(k&&v)out.push([k,v]);
  }
}catch(e){out=[]}
function stamp(){
  if(!out.length)return'';
  var s='';
  for(var j=0;j<out.length;j++)s+='\\n  '+out[j][0]+' = '+out[j][1];
  return s;
}
function enhance(a){
  try{
    if(!a||!a.getAttribute)return;
    var href=a.getAttribute('href')||'';
    if(href.indexOf('wa.me/')<0)return;
    if(a.getAttribute('data-hm-utm')==='done')return;
    var qi=href.indexOf('?');
    var path=qi<0?href:href.slice(0,qi);
    var pairs=qi<0?[]:href.slice(qi+1).split('&');
    var pre='';
    for(var m=pairs.length-1;m>=0;m--){
      if(pairs[m].indexOf('text=')===0){pre=pairs[m];pairs.splice(m,1);}
    }
    if(!out.length){a.setAttribute('data-hm-utm','done');return;}
    for(var n=0;n<out.length;n++)
      pairs.push(encodeURIComponent(out[n][0])+'='+encodeURIComponent(out[n][1]));
    if(pre){
      var dec=pre.slice(5);
      try{dec=decodeURIComponent(pre.slice(5).replace(/\\+/g,' '));}catch(e3){}
      if(stamp()&&dec.indexOf('Campaign:')<0)dec+='\\n\\nCampaign:'+stamp();
      pairs.unshift('text='+encodeURIComponent(dec));
    }
    a.setAttribute('href',path+(pairs.length?'?'+pairs.join('&'):''));
    a.setAttribute('data-hm-utm','done');
  }catch(e){}
}
function run(){
  var list=document.querySelectorAll('a[href*="wa.me/"]');
  for(var i=0;i<list.length;i++)enhance(list[i]);
}
run();
if(document.addEventListener){
  document.addEventListener('click',function(ev){
    var t=ev.target;
    while(t&&t!==document){
      if(t.nodeName==='A'){enhance(t);return;}
      t=t.parentNode;
    }
  },true);
}
}catch(e){}})();
</script>
"""

# ------------------------------------------------ WhatsApp-only form JS -----
# The campaign page hands leads to Ceyteq on WhatsApp ONLY — no fetch, no
# api/leads call, no window.open and nothing stored anywhere. Submitting the
# form composes ONE WhatsApp message and navigates the same tab synchronously
# to https://wa.me/<campaign number>?text=...  The message keeps a fixed order
# (Name, Contact, Email when filled, Property type, Rooms when filled, then the
# message) followed by utm_source / utm_medium / utm_campaign / utm_content
# when the page URL carries them; blank optional fields are omitted entirely.
# fitLines() keeps the finished URL under ~1900 chars even for long Sinhala
# text (which URI-encodes at ~9 chars per letter). contact.html and
# learn-earn.html keep the shared Ceyteq backend form — this is campaign-only.
WA_FORM_JS = r"""<script>
/* HotelMate campaign — WhatsApp-only lead handoff (no backend, nothing
   stored). One submit = ONE WhatsApp message; the tab navigates synchronously
   to the campaign number. fitLines() guards the URL length, blank optional
   fields are omitted, and campaign parameters ride along only when the page
   URL has them. */
(function(){
var API={};
var NUM='""" + WA_NUMBER + r"""';
var BASE='https://wa.me/'+NUM+'?text=';
var CAP=1900;               /* max chars of the finished wa.me URL */
var UTM_ORDER=['utm_source','utm_medium','utm_campaign','utm_content'];
var ERR={en:'Please fill your name, contact number and a short message.',
         si:'ඔබේ නම, සම්බන්ධතා අංකය සහ කෙටි පණිවිඩයක් දෙන්න.',
         fr:'Indiquez votre nom, votre numéro et un court message.'};
function g(id){return document.getElementById(id)}
function val(id){var e=g(id);return e?String(e.value||'').trim():''}
function readUtms(){
  var qs=String((typeof location!=='undefined'&&location.search)||'').replace(/^\?/,'');
  var parts=qs?qs.split('&'):[],map={};
  for(var i=0;i<parts.length;i++){
    var kv=parts[i];if(!kv)continue;
    var eq=kv.indexOf('='),k='',v='';
    try{k=decodeURIComponent(eq<0?kv:kv.slice(0,eq));}catch(e){k=eq<0?kv:kv.slice(0,eq);}
    if(eq>=0){try{v=decodeURIComponent(kv.slice(eq+1).replace(/\+/g,' '));}catch(e2){v=kv.slice(eq+1);}}
    v=String(v).replace(/\s+/g,' ').trim();
    if(k&&v&&map[k]===undefined)map[k]=v;
  }
  var out=[];
  for(var j=0;j<UTM_ORDER.length;j++){var k2=UTM_ORDER[j];if(map[k2]!==undefined)out.push([k2,map[k2]]);}
  return out;
}
function compose(f){
  var L=[];
  L.push('Name: '+f.name);
  L.push('Contact: '+f.contact);
  if(f.email)L.push('Email: '+f.email);
  L.push('Property type: '+f.type);
  if(f.rooms)L.push('Rooms: '+f.rooms);
  var msgIndex=L.length;
  L.push(String(f.message||''));
  var u=f.utms||[];
  for(var i=0;i<u.length;i++)L.push(u[i][0]+': '+u[i][1]);
  return {lines:L,msgIndex:msgIndex};
}
function pairSafe(s){return /[\uD800-\uDBFF]$/.test(s)?s.slice(0,-1):s}
function fitLines(lines,msgIndex){
  /* URL-length guard: the finished wa.me URL must stay under ~1900 chars for
     long English AND long Sinhala text (which URI-encodes at ~9 chars per
     letter). Whole trailing lines are given up first — the campaign parameter
     lines sit last by design — then the free-text message is trimmed, then a
     final clamp guarantees the URL always fits. Fixed fields are never
     dropped and UTF-16 surrogate pairs are never split. */
  function ok(ls){try{return (BASE+encodeURIComponent(ls.join('\n'))).length<=CAP}catch(e){return false}}
  var ls=lines.slice();
  if(ok(ls))return ls.join('\n');
  while(ls.length>msgIndex+1&&!ok(ls))ls=ls.slice(0,-1);
  var m=String(ls[msgIndex]||'');
  while(m&&!ok(ls)){
    m=pairSafe(m.slice(0,Math.max(1,Math.floor(m.length*0.9)-1)));
    ls[msgIndex]=m;
  }
  if(ls[msgIndex]==='')ls.splice(msgIndex,1);
  var s=ls.join('\n');
  while(s&&!ok([s]))s=pairSafe(s.slice(0,Math.max(1,Math.floor(s.length*0.95))-1));
  return s;
}
function urlFor(f){
  var c=compose(f);
  return BASE+encodeURIComponent(fitLines(c.lines,c.msgIndex));
}
function go(url){window.location.href=url;}  /* ONE synchronous navigation — same tab */
function send(ev){
  if(ev&&ev.preventDefault)ev.preventDefault();
  var note=g('eqNote');
  var name=val('eqName'),contact=val('eqContact'),message=val('eqMsg');
  if(!name||!contact||!message){
    if(note){note.className='form-note form-err';
             note.textContent=ERR[document.body.getAttribute('data-langmode')||'en']||ERR.en;}
    return false;
  }
  var t=g('eqType');
  API.go(urlFor({name:name,contact:contact,email:val('eqEmail'),
                 type:t?String(t.value||'').trim():'',rooms:val('eqRooms'),
                 message:message,utms:readUtms()}));
  return false;
}
API.number=NUM;API.base=BASE;API.cap=CAP;API.readUtms=readUtms;API.compose=compose;
API.fitLines=fitLines;API.urlFor=urlFor;API.go=go;API.send=send;
window.HMWA=API;
})();
</script>
"""

# ------------------------------------------------- shared campaign content ---
# Campaign offer — the exact approved wording, "for the campaign period".
OFFER = [
    dict(
        key_en='Setup fee', key_si='Setup ගාස්තුව', key_fr='Frais d’installation',
        val_en='Setup fee: FREE for the campaign period',
        val_si='Setup ගාස්තුව: campaign කාලය සඳහා නොමිලේ',
        val_fr='Frais d’installation : OFFERTS pendant la campagne',
        free=True,
        note_en=('The one-time setup and configuration fee is waived for the campaign '
                 'period only. Standard setup fees apply once the campaign closes — ask '
                 'on WhatsApp for the exact end date.'),
        note_si=('One-time setup සහ configuration ගාස්තුව මඟ හරිනවා campaign කාලය සඳහා '
                 'විතරයි. Campaign එක ඉවර වුනාම සම්මත setup ගාස්තු අදාළ වෙනවා — exact අවසාන '
                 'date එක WhatsApp එකෙන් අහන්න.'),
        note_fr=('Les frais d’installation et de configuration sont offerts pour la durée de '
                 'la campagne uniquement. Après la campagne, les tarifs standard s’appliquent '
                 '— demandez la date de fin exacte sur WhatsApp.'),
    ),
    dict(
        key_en='Monthly licence', key_si='මාසික licence එක', key_fr='Licence mensuelle',
        val_en='US$39/month for the first 10 rooms',
        val_si='පළමු කාමර 10 සඳහා මාසයට US$39',
        val_fr='39 $ US/mois pour les 10 premières chambres',
        free=False,
        note_en=('Campaign rate for the first 10 rooms of your property. Rooms beyond 10, '
                 'POS, channel manager, hardware and any HotelMate add-on are quoted by the '
                 'HotelMate team at the final demo.'),
        note_si=('ඔබේ property එකේ පළමු කාමර 10 සඳහා campaign rate එක. කාමර 10 ට වැඩි '
                 'ප්‍රමාණය, POS, channel manager, hardware සහ HotelMate add-ons මිල ගණන් '
                 'දෙන්නේ final demo එකේදී HotelMate කණ්ඩායමයි.'),
        note_fr=('Tarif de campagne pour les 10 premières chambres de votre établissement. '
                 'Les chambres au-delà de 10, la caisse, le channel manager, le matériel et '
                 'les options sont chiffrés par l’équipe HotelMate lors de la démo finale.'),
    ),
]

# What a PMS in this category handles — the category, not invented module names.
COVERS = [
    dict(t_en='Front desk and reservations', t_si='Front desk එක සහ reservations',
         t_fr='Réception et réservations',
         n_en='Availability, room assignment and the booking list your team works from all day.',
         n_si='Availability, කාමර වෙන් කිරීම සහ දවස පුරා ඔබේ කණ්ඩායම බලන booking list එක.',
         n_fr='Disponibilités, attribution des chambres et la liste de réservations du quotidien.'),
    dict(t_en='Guests, rates and billing', t_si='Guests, rates සහ billing',
         t_fr='Clients, tarifs et facturation',
         n_en='Guest profiles, seasonal rates, folios and invoices that follow your tariff sheet.',
         n_si='Guest profiles, seasonal rates, folios සහ ඔබේ tariff sheet එකට ගැලපෙන invoices.',
         n_fr='Profils clients, tarifs saisonniers, folios et factures conformes à votre grille.'),
    dict(t_en='Owner and audit reporting', t_si='හිමිකරුට සහ audit එකට වාර්තා',
         t_fr='Rapports de direction et d’audit',
         n_en='Night-audit style reporting with occupancy and revenue views for owners and auditors.',
         n_si='Night audit style වාර්තා, occupancy සහ revenue දසුන් — හිමිකරුවන්ට සහ auditors ලාට.',
         n_fr='Rapports type night audit, avec vues occupation et revenus pour les propriétaires.'),
    dict(t_en='Works with the channels you already run', t_si='දැනට භාවිතා කරන channels සමඟ',
         t_fr='Compatible avec vos canaux actuels',
         n_en='Booking sites, Google and WhatsApp enquiries stay where they are; the room inventory '
              'is coordinated against them. Exact integrations are confirmed in the HotelMate demo.',
         n_si='Booking sites, Google සහ WhatsApp enquiries තියෙන තැනම තියෙනවා; room inventory එක '
              'ඒවාට ගැලපෙන විදිහට සම්බන්ධ කරනවා. Exact integrations HotelMate demo එකේදී තහවුරු වෙනවා.',
         n_fr='Vos sites de réservation, Google et les demandes WhatsApp restent en place ; '
              'l’inventaire des chambres est coordonné avec eux. Les intégrations exactes sont '
              'confirmées lors de la démo HotelMate.'),
]

# The required flow: WhatsApp → qualification → HotelMate back-office demo.
STEPS = [
    dict(t_en='Message the campaign WhatsApp', t_si='campaign WhatsApp එකට msg එකක් යවන්න',
         t_fr='Écrivez sur le WhatsApp de campagne',
         n_en=f'Send your message to Ceyteq on {WA_DISPLAY}. Tell us the property type, the room '
              'count and the system you use today.',
         n_si=f'CEYTEQ වෙත {WA_DISPLAY} WhatsApp එකෙන් msg එකක් යවන්න. ඔබේ property වර්ගය, කාමර '
              'ගණන සහ දැනට භාවිතා කරන පද්ධතිය කියන්න.',
         n_fr=f'Écrivez à Ceyteq au {WA_DISPLAY}. Indiquez le type d’établissement, le nombre de '
              'chambres et le système utilisé aujourd’hui.'),
    dict(t_en='Ceyteq qualifies the lead', t_si='Ceyteq විසින් lead එක qualify කරනවා',
         t_fr='Ceyteq qualifie la demande',
         n_en='A short call to confirm your rooms, your current setup and the first thing you want '
              'to fix. No obligation — and no promise made on the HotelMate team’s behalf.',
         n_si='කාමර ගණන, දැනට තියෙන setup එක සහ මුලින්ම හදන්න ඕන දේ තහවුරු කරන්න කෙටි call එකක්. '
              'කිසිම බැඳීමක් නෑ — HotelMate කණ්ඩායම වෙනුවෙන් කිසිම පොරොන්දුවක් නෑ.',
         n_fr='Un appel court pour confirmer vos chambres, votre configuration et la priorité du '
              'jour. Sans engagement — aucun engagement pris au nom de l’équipe HotelMate.'),
    dict(t_en='HotelMate back-office final demo', t_si='HotelMate back-office final demo එක',
         t_fr='Démo finale au back-office HotelMate',
         n_en='Ceyteq schedules you in; the HotelMate team runs the final product demonstration with '
              'the real screens, your rate plan and the contract terms.',
         n_si='Ceyteq schedule කරනවා; HotelMate කණ්ඩායම final product demo එක කරනවා — ඇත්ත '
              'screens, ඔබේ rate plan එක සහ contract conditions සමඟ.',
         n_fr='Ceyteq planifie la séance ; l’équipe HotelMate présente le produit réel, votre grille '
              'tarifaire et les conditions du contrat.'),
    dict(t_en='Setup and activation', t_si='setup සහ activation',
         t_fr='Installation et mise en service',
         n_en='Activation is completed with the HotelMate team. The campaign setup-fee waiver applies '
              'while the campaign period is open.',
         n_si='Activation සිදු කරන්නේ HotelMate කණ්ඩායම සමඟයි. Campaign setup ගාස්තු මඟ හැරීම '
              'අදාළ වන්නේ campaign කාලය තුළ පමණයි.',
         n_fr='La mise en service se fait avec l’équipe HotelMate. L’exonération des frais '
              'd’installation s’applique tant que la campagne est ouverte.'),
]


def disclose():
    """The mandated Ceyteq/HotelMate responsibility line."""
    return ('<div class="hm-disclose"><small>'
            + T(DISCLOSURE, DISCLOSURE_SI, DISCLOSURE_FR) + '</small></div>')


def wa_button(label_en='WhatsApp a HotelMate specialist',
              label_si='HotelMate specialist කෙනෙකුට WhatsApp කරන්න',
              label_fr='Écrire à un spécialiste HotelMate sur WhatsApp',
              cls='btn btn-wa'):
    """The campaign CTA. rel=noopener + target=_blank as the rest of the site does."""
    return (f'<a class="{cls}" href="{wa_link()}" target="_blank" rel="noopener" '
            f'data-utm aria-label="{label_en} — {WA_DISPLAY}">💬 '
            f'{T(label_en, label_si, label_fr)}</a>')


def explore_button(cls='btn btn-hm'):
    return (f'<a class="{cls}" href="hotelmate.html">🏨 '
            f'{T("Explore HotelMate →", "HotelMate බලන්න →", "Découvrir HotelMate →")}</a>')


# ------------------------------------------------------ HOMEPAGE BAND --------
def featured_band():
    """index.html featured-partner section.

    Ceyteq stays the main brand and the campaign price is NOT stated here —
    the setup-fee waiver wording belongs to the HotelMate campaign page only.
    """
    band = f"""
<section id="hotelmate">
<div class="hm-band">
<div class="kick">★ {T('FEATURED HOSPITALITY TECHNOLOGY PARTNER',
                       'ප්‍රධාන හෝටල් තාක්ෂණ හවුල්කරු',
                       'PARTENAIRE TECHNOLOGIQUE HÔTELIER EN VEDETTE')} ★</div>
<div class="ah">{mark()}
<span>{T('HotelMate, featured by Ceyteq',
         'Ceyteq highlight කරන HotelMate',
         'HotelMate, mis en avant par Ceyteq')}</span></div>
<p>{T('Ceyteq is your full-service technology company — websites, ads, print, media, AI and travel. '
       'HotelMate is the hospitality software we feature for hotels, villas and guest houses: '
       'reservations, rates, billing and owner reports in one cloud system.',
       'Ceyteq තමයි ඔබේ full-service technology company — වෙබ්, ads, print, media, AI සහ travel. '
       'හෝටල්, villas සහ guest houses සඳහා අපි highlight කරන hospitality software එක HotelMate: '
       'reservations, rates, billing සහ හිමිකරුට වාර්තා එකම cloud පද්ධතියක.',
       'Ceyteq est votre société de technologie complète — web, publicité, impression, médias, IA et '
       'voyage. HotelMate est le logiciel hôtelier que nous mettons en avant pour hôtels, villas et '
       'maisons d’hôtes : réservations, tarifs, facturation et rapports dans un seul système cloud.')}</p>
<ul>
<li><b>{T('Ceyteq coordinates', 'Ceyteq සම්බන්ධීකරණය කරනවා', 'Ceyteq coordonne')}</b> — {T(
    'introduction, qualification, demo booking', 'introduction, qualification, demo booking',
    'mise en relation, qualification, réservation de la démo')}</li>
<li><b>{T('HotelMate delivers', 'HotelMate සපයනවා', 'HotelMate fournit')}</b> — {T(
    'final product demo, licence and activation', 'අවසාන product demo, licence සහ activation',
    'démo finale, licence et mise en service')}</li>
<li><b>{T('Campaign offer', 'campaign offer එක', 'Offre de campagne')}</b> — {T(
    'terms and pricing on the HotelMate page', 'කොන්දේසි සහ මිල HotelMate පිටුවේ',
    'conditions et tarifs sur la page HotelMate')}</li>
</ul>
<div class="cta-row">
{explore_button()}
{wa_button()}
</div>
{disclose()}
</div>
</section>
"""
    return band


# --------------------------------------------------- services.html card -----
def partners_section():
    """Technology partners section shown under the 08 Ceyteq service divisions.
    It is appended after them — no division is removed, renamed or renumbered."""
    tags = ''.join(f'<li>{t}</li>' for t in [
        'PMS',
        T('Cloud', 'cloud', 'Cloud'),
        T('Villas and guest houses', 'villas සහ guest houses', 'Villas et maisons d’hôtes'),
        T('Ceyteq coordinated demo', 'Ceyteq සම්බන්ධීකරණය කළ ඩෙමෝ', 'Démo coordonnée par Ceyteq'),
    ])
    return f"""
<section id="partners">
<div class="eyebrow">{T('Technology partners', 'තාක්ෂණ හවුල්කරුවන්', 'Partenaires technologiques')}</div>
<h2>{T('Featured Partner: HotelMate', 'ප්‍රධාන හවුල්කරු: HotelMate', 'Partenaire en vedette : HotelMate')}</h2>
<p class="lead">{T('Alongside our own 08 divisions, Ceyteq features HotelMate for hotel property '
                   'management. Ceyteq handles the introduction, the qualification call and the demo '
                   'schedule; the product, its licence and the activation belong to the HotelMate team.',
                   'අපේම සේවා අංශ 08 ට අමතරව, හෝටල් property management සඳහා HotelMate අපි '
                   'highlight කරනවා. Ceyteq කරන්නේ introduction, qualification call එක සහ demo '
                   'schedule එක; product එක, licence එක සහ activation HotelMate කණ්ඩායමේ වගකීම.',
                   'En plus de nos 08 divisions, Ceyteq met en avant HotelMate pour la gestion '
                   'hôtelière. Ceyteq assure la mise en relation, l’appel de qualification et le '
                   'planning de la démo ; le produit, la licence et la mise en service relèvent de '
                   'l’équipe HotelMate.')}</p>
<a class="hm-partner" href="hotelmate.html">
<span class="hm-ribbon">{T('Main hospitality technology partner', 'ප්‍රධාන හෝටල් තාක්ෂණ හවුල්කරු',
                            'Partenaire technologique hôtelier principal')}</span>
<div class="hm-lock">{mark()}</div>
<p>{T('Reservations, rates, billing and owner reports in one cloud PMS for hotels, villas and guest '
       'houses. Full campaign details, terms and the demo booking are on the HotelMate page.',
       'Reservations, rates, billing සහ හිමිකරුට වාර්තා — හෝටල්, villas සහ guest houses සඳහා එකම '
       'cloud PMS එකකින්. සම්පූර්ණ campaign විස්තර, කොන්දේසි සහ demo booking HotelMate පිටුවේ.',
       'Réservations, tarifs, facturation et rapports de direction dans un seul PMS cloud pour hôtels, '
       'villas et maisons d’hôtes. Détails de la campagne, conditions et réservation de la démo sur la '
       'page HotelMate.')}</p>
<ul class="hm-tags">{tags}</ul>
<div class="hm-goto">{T('Open the HotelMate campaign page →', 'HotelMate campaign පිටුව විවෘත කරන්න →',
                        'Ouvrir la page de campagne HotelMate →')}</div>
</a>
{disclose()}
</section>
"""


# ------------------------------------------------- campaign landing page ----
def hero_block():
    return f"""<div class="hm-hero">
<div class="kick">{T('CEYTEQ PARTNER CAMPAIGN · HOSPITALITY TECHNOLOGY',
                     'CEYTEQ හවුල්කාර ව්‍යාපාරය · හෝටල් තාක්ෂණය',
                     'CAMPAGNE PARTENAIRE CEYTEQ · TECHNOLOGIE HÔTELIÈRE')}</div>
<div class="lock">{mark()}</div>
<h1>{T('HOTELMATE FOR YOUR HOTEL', 'ඔබේ හෝටල් එකට HotelMate', 'HOTELMATE POUR VOTRE HÔTEL')}</h1>
<p class="lead">{T('A cloud property management system for hotels, villas and guest houses, featured by '
                   'Ceyteq. Send one WhatsApp message: we qualify your property and book you into the '
                   'HotelMate team’s final demo.',
                   'හෝටල්, villas සහ guest houses සඳහා cloud property management (PMS) පද්ධතියක් — '
                   'Ceyteq highlight කරන one. එක WhatsApp msg එකක් යවන්න: අපි ඔබේ property එක '
                   'validate කරලා HotelMate කණ්ඩායමේ final demo එකට ඔබව place කරනවා.',
                   'Un PMS cloud pour hôtels, villas et maisons d’hôtes, mis en avant par Ceyteq. '
                   'Envoyez un message WhatsApp : nous qualifions votre établissement et réservons votre '
                   'démo finale avec l’équipe HotelMate.')}</p>
<div class="cta-row">
{wa_button('Start on WhatsApp', 'WhatsApp එකෙන් පටන් ගන්න', 'Commencer sur WhatsApp')}
<a class="btn btn-ghost" href="#offer">💵 {T('Campaign offer', 'campaign offer එක', 'Offre de campagne')}</a>
<a class="btn btn-ghost" href="#led">🖥️ {T('LED screens extra', 'LED screens extra', 'Écrans LED en plus')}</a>
<a class="btn btn-ghost" href="#how">🧭 {T('How the demo works', 'ඩෙමෝ ක්‍රමය', 'Déroulé de la démo')}</a>
</div>
{disclose()}
</div>"""


def offer_block():
    """The campaign offer. This wording lives ONLY on this page."""
    cards = ''
    for o in OFFER:
        cards += ('<div class="o"><small>'
                  + T(o['key_en'], o['key_si'], o['key_fr']) + '</small><b'
                  + (' class="free"' if o['free'] else '') + '>'
                  + T(o['val_en'], o['val_si'], o['val_fr']) + '</b><p>'
                  + T(o['note_en'], o['note_si'], o['note_fr']) + '</p></div>')
    return f"""
<section id="offer">
<div class="eyebrow">{T('Campaign offer', 'campaign දීමනාව', 'Offre de campagne')}</div>
<h2>{T('The Campaign Offer', 'campaign offer එක', 'L’offre de campagne')}</h2>
<p class="lead">{T('The campaign offer in two lines: the setup fee is waived for the campaign period and '
                   'the licence is US$39 a month for your first 10 rooms. It is a campaign offer — not a '
                   'permanently free plan.',
                   'campaign offer එක පේළි දෙකකින්: setup ගාස්තුව campaign කාලය සඳහා නොමිලේ, සහ '
                   'පළමු කාමර 10 සඳහා මාසයට US$39. මේක campaign offer එකක් — සදහටම නොමිලේ plan '
                   'එකක් නොවෙයි.',
                   'L’offre de campagne en deux lignes : frais d’installation offerts pendant la campagne '
                   'et licence à 39 $ US par mois pour vos 10 premières chambres. C’est une offre de '
                   'campagne — pas un forfait gratuit permanent.')}</p>
<div class="offer">{cards}</div>
<div class="hm-note"><b>{T('Read this before you plan your budget:', 'budget එක සකසන්න කලින් මේක කියවන්න:',
                           'À lire avant de préparer votre budget :')}</b> {T(
    'The setup fee is FREE for the campaign period only, and US$39/month covers the first 10 rooms. '
    'Rooms beyond 10, POS, channel manager, hardware and hosting add-ons are quoted separately by the '
    'HotelMate team. Ask on WhatsApp for the current campaign end date and rate card before you sign '
    'anything.',
    'setup ගාස්තුව නොමිලේ වන්නේ campaign කාලය සඳහා විතරයි; මාසයට US$39 යනු පළමු කාමර 10 සඳහායි. '
    'කාමර 10 ට වැඩි ප්‍රමාණය, POS, channel manager, hardware සහ hosting add-ons මිල ගණන් දෙන්නේ '
    'HotelMate කණ්ඩායමයි. ඕනෑම දෙකකට sign කරන්න කලින් දැනට තියෙන campaign අවසාන date එක සහ rate '
    'card එක WhatsApp එකෙන් අහන්න.',
    'les frais d’installation sont offerts uniquement pendant la campagne et 39 $ US/mois couvre les 10 '
    'premières chambres. Les chambres au-delà de 10, la caisse, le channel manager, le matériel et '
    'l’hébergement sont chiffrés séparément par l’équipe HotelMate. Demandez sur WhatsApp la date de fin '
    'de campagne et le tarif en vigueur avant de signer quoi que ce soit.')}</div>
</section>
"""


def fit_block():
    cards = ''
    for c in COVERS:
        cards += ('<div class="card"><h3>🏨 ' + T(c['t_en'], c['t_si'], c['t_fr'])
                  + '</h3><p>' + T(c['n_en'], c['n_si'], c['n_fr']) + '</p></div>')
    return f"""
<section id="fit">
<div class="eyebrow">{T('What it covers', 'ආවරණය වන දේ', 'Ce que cela couvre')}</div>
<h2>{T('What a PMS Like HotelMate Handles', 'HotelMate වැනි PMS එකක් බලන දේ',
        'Ce qu’un PMS comme HotelMate prend en charge')}</h2>
<p class="lead">{T('A general view of the category. The exact modules, your rate plan and the '
                   'integrations you need are confirmed with the HotelMate team during the final demo. '
                   'Nothing here promises results: no revenue guarantee and no occupancy guarantee is '
                   'made by Ceyteq or HotelMate in this campaign.',
                   'මේ category එක ගැන සාමාන්‍ය දසුනක්. Exact modules, ඔබේ rate plan එක සහ ඕන '
                   'integrations තහවුරු වන්නේ final demo එකේදී HotelMate කණ්ඩායම සමඟයි. මෙතන කිසිම '
                   'ප්‍රතිඵලයක් පොරොන්දු වෙන්නේ නෑ: Ceyteq හෝ HotelMate විසින් revenue හෝ occupancy '
                   'guarantee එකක් මේ campaign එකේදී නිකුත් කරන්නේ නෑ.',
                   'Vue générale de la catégorie. Les modules exacts, votre grille tarifaire et vos '
                   'intégrations sont confirmés avec l’équipe HotelMate lors de la démo finale. Rien ici '
                   'ne promet de résultat : aucune garantie de revenus ni d’occupation n’est donnée par '
                   'Ceyteq ou HotelMate dans cette campagne.')}</p>
<div class="grid">{cards}</div>
</section>
"""


def led_block():
    """The optional Ceyteq service paired with the campaign page: LED screens
    and signage for the hotel. It is Ceyteq's own Print & Digital work,
    quoted per job — it is never bundled into the US$39/month HotelMate
    licence, and no price is invented here (site price-lock rule: quote on
    request). The dedicated WhatsApp button keeps the campaign number and
    rides the same UTM passthrough as every other wa.me link."""
    return f"""
<section id="led">
<div class="eyebrow">{T('Hotel extra', 'හෝටල් extra එක', 'Extra pour votre hôtel')}</div>
<h2>{T('Add LED Screens & Signage', 'LED Screens & Signage එකතු කරන්න',
       'Écrans LED & enseigne en plus')}</h2>
<p class="lead">{T('While you roll out HotelMate, Ceyteq can fit your lobby, reception or entrance '
                   'with LED screens and signage — today’s menus, offers and promotions, updated in '
                   'minutes. It is a Ceyteq Print & Digital service, quoted per job: sizes, mounting '
                   'and the content are confirmed on WhatsApp before any work starts.',
                   'HotelMate rollout කරන කාලයේ, Ceyteq වගේ lobby, reception හෝ entrance වලට LED '
                   'screens සහ signage එකතු කරන්න පුළුවන් — දැන් තියෙන menus, offers සහ promotions '
                   'minutes කිහිපයකින් update කරනවා. මේක Ceyteq Print & Digital service එකක් — quote '
                   'per job: sizes, mounting සහ content work පටන් ගන්නකලින් WhatsApp වල තහවුරු කරගන්න.',
                   'Pendant le déploiement de HotelMate, Ceyteq peut équiper votre hall, votre '
                   'réception ou votre entrée d’écrans LED et d’une enseigne — menus, offres et '
                   'promotions du jour, mis à jour en quelques minutes. C’est un service Ceyteq '
                   'Print & Digital, chiffré par projet : dimensions, fixation et contenu sont '
                   'confirmés sur WhatsApp avant tout travaux.')}</p>
<ul class="hm-extra">
<li>🖥️ <b>{T('Lobby & reception screens', 'lobby & reception screens',
            'Écrans hall & réception')}</b> — {T('today’s offers, events and notices',
            'දැන් තියෙන offers, events සහ notices',
            'offres du jour, événements et avis')}</li>
<li>🪧 <b>{T('Outdoor & entrance signage', 'outdoor & entrance signage',
            'Enseigne extérieure & entrée')}</b> — {T('your name, your menu, in light',
            'ඔබේ නම, ඔබේ menu එක — ආලෝකයෙන්',
            'votre nom, votre menu, en lumière')}</li>
<li>📋 <b>{T('Content you can change', 'change කරන්න පුළුවන් content එක',
            'Contenu modifiable')}</b> — {T('swap the picture or the words in minutes',
            'picture එක හෝ වචන minutes කිහිපයකින් මාරු කරන්න',
            'changez l’image ou le texte en quelques minutes')}</li>
<li>💬 <b>{T('Quote on request', 'quote on request', 'Devis sur demande')}</b> — {T(
            'sizes, mounting and content confirmed on WhatsApp',
            'sizes, mounting සහ content WhatsApp වල තහවුරු කරනවා',
            'dimensions, fixation et contenu confirmés sur WhatsApp')}</li>
</ul>
<div class="cta-row">
<a class="btn btn-wa" href="{wa_link(LED_TEXT)}" target="_blank" rel="noopener" data-utm
   aria-label="WhatsApp about HotelMate and LED screens — {WA_DISPLAY}">💬 {T(
            'WhatsApp about HotelMate + LED',
            'HotelMate + LED ගැන WhatsApp කරන්න',
            'WhatsApp pour HotelMate + LED')}</a>
<a class="btn btn-ghost" href="print.html">🖨️ {T('Ceyteq Print & Digital',
            'Ceyteq Print & Digital', 'Ceyteq Print & Digital')}</a>
</div>
</section>
"""


def how_block():
    steps = ''
    for i, s in enumerate(STEPS):
        steps += (f'<div class="step"><div class="n" aria-hidden="true">{i + 1}</div><div>'
                  f'<b>{T(s["t_en"], s["t_si"], s["t_fr"])}</b>'
                  f'<p>{T(s["n_en"], s["n_si"], s["n_fr"])}</p></div></div>')
    return f"""
<section id="how">
<div class="eyebrow">{T('The flow', 'ක්‍රමය', 'Le déroulé')}</div>
<h2>{T('Four Steps — WhatsApp to Live System', 'පියවර 4 — WhatsApp සිට live පද්ධතිය දක්වා',
        'Quatre étapes — du WhatsApp au système en service')}</h2>
<p class="lead">{T('Ceyteq runs the first two steps and schedules the third. The final demo and the '
                   'activation are completed with the HotelMate team, so nothing is promised on their '
                   'behalf.',
                   'පළමු පියවර දෙක Ceyteq කරනවා, තුන්වන පියවර schedule කරනවා. අවසාන demo එක සහ '
                   'activation සිදු වන්නේ HotelMate කණ්ඩායම සමඟයි — ඒ නිසා ඔවුන් වෙනුවෙන් කිසිවක් '
                   'පොරොන්දු වන්නේ නෑ.',
                   'Ceyteq traite les deux premières étapes et planifie la troisième. La démo finale et '
                   'la mise en service se font avec l’équipe HotelMate : rien n’est promis en son nom.')}</p>
<div class="steps">{steps}</div>
{disclose()}
<div class="cta-row" style="justify-content:flex-start">
{wa_button()}
</div>
</section>
"""


def follow_block():
    links = ''
    for name, icon, url in SOCIAL:
        links += (f'<a href="{url}" target="_blank" rel="noopener" '
                  f'aria-label="HotelMate on {name}">{icon} {name}</a>')
    return f"""
<section id="follow">
<div class="eyebrow">{T('HotelMate directly', 'HotelMate ගැනම', 'HotelMate en direct')}</div>
<h2>{T('Follow HotelMate, Talk to Ceyteq', 'HotelMate follow කරන්න, Ceyteq සමඟ කතා කරන්න',
        'Suivez HotelMate, parlez à Ceyteq')}</h2>
<p class="lead">{T('HotelMate publishes its own product content on Facebook, Instagram and TikTok. '
                   f'Sales coordination, your qualification call and the demo schedule stay with Ceyteq '
                   f'on {WA_DISPLAY}.',
                   'HotelMate ගැන product content ඔවුන්ගේම Facebook, Instagram සහ TikTok වල පළ වෙනවා. '
                   f'Sales coordination, qualification call එක සහ demo schedule එක Ceyteq සමඟයි — {WA_DISPLAY}.',
                   'HotelMate publie son propre contenu produit sur Facebook, Instagram et TikTok. La '
                   f'mise en relation commerciale, l’appel de qualification et le planning de la démo '
                   f'restent chez Ceyteq au {WA_DISPLAY}.')}</p>
<div class="social">{links}</div>
</section>
"""


def form_block():
    """WhatsApp-only enquiry. There is no backend call and nothing is stored:
    submitting composes ONE WhatsApp message and navigates the tab
    synchronously to the campaign number (see WA_FORM_JS). Blank optional
    fields are omitted from the message entirely."""
    options = ['Hotel', 'Resort', 'Villa', 'Guest house', 'Hostel', 'Other']
    opts = ''
    for o in options:
        sel = ' selected' if o == options[0] else ''
        opts += f'<option value="{o}"{sel}>{o}</option>'
    return f"""
<section id="enquiry">
<div class="eyebrow">{T('HotelMate enquiry', 'HotelMate විමසුම', 'Demande HotelMate')}</div>
<h2>{T('Or Send the Details on WhatsApp', 'නැත්නම් විස්තර WhatsApp වලට යවන්න', 'Ou envoyez les détails sur WhatsApp')}</h2>
<form class="enquiry" id="enquiryForm" onsubmit="return HMWA.send(event)"
      aria-label="HotelMate enquiry form">
<input id="eqName" required maxlength="120" placeholder="Your name / ඔබේ නම" autocomplete="name"
       aria-label="Your name">
<input id="eqContact" required maxlength="60" placeholder="WhatsApp or phone number / දුරකථන අංකය"
       autocomplete="tel" aria-label="WhatsApp or phone number">
<input id="eqEmail" type="email" maxlength="160" placeholder="Email (optional) / ඊමේල්" aria-label="Email, optional">
<select id="eqType" aria-label="Property type">{opts}</select>
<input id="eqRooms" type="number" min="1" max="9999" inputmode="numeric"
       placeholder="Number of rooms (optional) / කාමර ගණන" aria-label="Number of rooms, optional">
<textarea id="eqMsg" required maxlength="2000" rows="5"
          placeholder="Tell us about your property / ඔබේ property එක ගැන කියන්න"
          aria-label="About your property"></textarea>
<button class="btn btn-wa" type="submit" id="eqBtn">{T('Send on WhatsApp', 'WhatsApp වලට යවන්න', 'Envoyer sur WhatsApp')}</button>
<div class="form-note" id="eqNote">{T('Your details will be sent to Ceyteq on WhatsApp. A campaign representative will reply.',
                                      'ඔබේ විස්තර Ceyteq වෙත WhatsApp හරහා යවනු ලැබේ. campaign representative කෙනෙකු පිළිතුරු දෙනවා.',
                                      'Vos détails seront envoyés à Ceyteq sur WhatsApp. Un représentant de campagne vous répondra.')}</div>
</form>
</section>
"""


def closing_block():
    return f"""
<section id="start">
<div class="hm-band">
<div class="kick">★ {T('CAMPAIGN PERIOD ONLY', 'campaign කාලය සඳහා පමණයි', 'DURANT LA CAMPAGNE SEULEMENT')} ★</div>
<div class="ah">{mark()}
<span>{T('Start with one WhatsApp message', 'එක WhatsApp msg එකකින් පටන් ගන්න',
          'Commencez par un message WhatsApp')}</span></div>
<p>{T('Tell us your property and your room count. Ceyteq qualifies the lead and hands the demo over to '
       'the HotelMate team.',
       'ඔබේ property එක සහ කාමර ගණන කියන්න. Ceyteq lead එක qualify කරලා demo එක HotelMate කණ්ඩායමට '
       'භාර දෙනවා.',
       'Indiquez votre établissement et votre nombre de chambres. Ceyteq qualifie la demande et confie '
       'la démo à l’équipe HotelMate.')}</p>
<p class="hm-terms">{T('Campaign terms: setup fee FREE for the campaign period; US$39/month for the '
                             'first 10 rooms.',
                             'Campaign කොන්දේසි: setup ගාස්තුව campaign කාලය සඳහා නොමිලේ; පළමු කාමර 10 '
                             'සඳහා මාසයට US$39.',
                             'Conditions de campagne : frais d’installation OFFERTS pendant la campagne ; '
                             '39 $ US/mois pour les 10 premières chambres.')}</p>
<div class="cta-row">
{wa_button()}
{explore_button('btn btn-ghost')}
<a class="btn btn-ghost" href="contact.html">📩 {T('Ceyteq contact page', 'Ceyteq සම්බන්ධ පිටුව',
                                                     'Page contact Ceyteq')}</a>
</div>
{disclose()}
</div>
</section>
"""


def hotelmate_page():
    """Body of /hotelmate.html — the HotelMate campaign landing page."""
    return (hero_block() + offer_block() + fit_block() + led_block() + how_block()
            + follow_block() + form_block() + closing_block())
