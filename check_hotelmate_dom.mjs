#!/usr/bin/env node
/**
 * CEYTEQ HotelMate DOM check — WhatsApp-only lead handoff (jsdom).
 *
 *     npm i jsdom
 *     node check_hotelmate_dom.mjs
 *
 * Runs 52 checks against the BUILT hotelmate.html (run build_site.py first).
 * jsdom cannot leave the document, so navigation is verified two ways:
 *   1. submit is captured through the page's own seam (window.HMWA.go — the
 *      exact function send() calls), proving WHERE the form hands off to;
 *   2. HMWA.go is then restored and called with a same-document URL, proving
 *      it performs a real synchronous location navigation.
 * Prints SKIP (exit 0) when jsdom is not installed.
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const ROOT = dirname(fileURLToPath(import.meta.url));

let JSDOM, VirtualConsole;
try {
  ({ JSDOM, VirtualConsole } = await import('jsdom'));
} catch {
  console.log('SKIP — jsdom is not installed. Run:  npm i jsdom  — then re-run this check.');
  process.exit(0);
}

const HTML = readFileSync(join(ROOT, 'hotelmate.html'), 'utf8');
const ORIGIN = 'https://ceyteq-check.test';
const CONFIRM = 'Your details will be sent to Ceyteq on WhatsApp. A campaign representative will reply.';
const BASE = 'https://wa.me/94768607143?text=';
const COUNT = 52;

let passed = 0, failed = 0;
const ok = (name, cond) => {
  if (cond) { passed++; console.log('  \u2713 ' + name); }
  else { failed++; console.log('  \u2717 ' + name); }
};

// quiet console — jsdom CSS chit-chat is irrelevant here
const quiet = () => new VirtualConsole();
quiet().on('jsdomError', () => {});

function loadDom(url) {
  return new JSDOM(HTML, { url, runScripts: 'dangerously', virtualConsole: quiet() });
}
function captureNav(w) {
  const nav = [];
  const real = w.HMWA.go;
  w.HMWA.go = (url) => { nav.push(String(url)); };
  nav.restore = () => { w.HMWA.go = real; };
  return nav;
}
function submit(form) {
  const w = form.ownerDocument.defaultView;
  const ev = new w.Event('submit', { bubbles: true, cancelable: true });
  form.dispatchEvent(ev);
  return ev;
}
const dec = (url) => decodeURIComponent(String(url).split('?text=')[1] || '');
const lns = (url) => dec(url).split('\n');
const fill = (d, id, v) => { d.getElementById(id).value = v; };

// ---------------------------------------------------------- A: plain URL --
console.log('\n--- A. clean URL: one message, fixed order, blank fields omitted ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html');
  const w = dom.window, d = w.document;
  ok('window.HMWA API is defined', !!w.HMWA && typeof w.HMWA.send === 'function');
  ok('campaign number is 94768607143', !!w.HMWA && w.HMWA.number === '94768607143');
  ok('base is https://wa.me/94768607143?text= (HTTPS, campaign number only)',
     !!w.HMWA && w.HMWA.base === BASE);
  ok('form #enquiryForm exists', !!d.getElementById('enquiryForm'));
  ok('field #eqName exists', !!d.getElementById('eqName'));
  ok('field #eqContact exists', !!d.getElementById('eqContact'));
  ok('field #eqEmail exists', !!d.getElementById('eqEmail'));
  ok('field #eqType exists', !!d.getElementById('eqType'));
  ok('field #eqRooms exists', !!d.getElementById('eqRooms'));
  ok('field #eqMsg exists', !!d.getElementById('eqMsg'));
  ok('confirmation line is exactly right',
     d.querySelector('#eqNote .lang-en').textContent === CONFIRM);
  ok('submit button #eqBtn exists', !!d.getElementById('eqBtn'));
  ok('property type defaults to Hotel', d.getElementById('eqType').value === 'Hotel');

  let opens = 0, fetches = 0, xhr = 0;
  w.open = () => { opens++; };
  w.fetch = () => { fetches++; };
  if (typeof w.XMLHttpRequest === 'function') {
    const X = w.XMLHttpRequest;
    w.XMLHttpRequest = function () { xhr++; return new X(); };
  }
  const nav = captureNav(w);
  fill(d, 'eqName', 'Niroshan Perera');
  fill(d, 'eqContact', '077 123 4567');
  fill(d, 'eqMsg', 'Hello, I run a small hotel in Kandy.');
  const ev = submit(d.getElementById('enquiryForm'));

  ok('submitting composes exactly ONE WhatsApp handoff, synchronously', nav.length === 1);
  ok('the submit default is prevented (no form POST, no reload)', ev.defaultPrevented === true);
  ok('URL starts https://wa.me/94768607143?text=', (nav[0] || '').startsWith(BASE));
  ok('line 1 is the name', lns(nav[0])[0] === 'Name: Niroshan Perera');
  ok('line 2 is the contact', lns(nav[0])[1] === 'Contact: 077 123 4567');
  ok('blank email is omitted entirely', !dec(nav[0]).includes('Email:'));
  ok('line 3 is the property type', lns(nav[0])[2] === 'Property type: Hotel');
  ok('blank rooms is omitted entirely', !dec(nav[0]).includes('Rooms:'));
  ok('the message is the last line — 4 lines exactly, nothing else',
     lns(nav[0]).length === 4 && lns(nav[0])[3] === 'Hello, I run a small hotel in Kandy.');
  ok('no utm_ lines without campaign parameters in the page URL', !dec(nav[0]).includes('utm_'));
  ok('window.open is never called', opens === 0);
  ok('fetch is never called', fetches === 0);
  ok('XMLHttpRequest is never created', xhr === 0);

  const dom2 = loadDom(ORIGIN + '/hotelmate.html#fresh');
  dom2.window.HMWA.go(ORIGIN + '/hotelmate.html#wa-handoff');
  ok('go() performs a real synchronous location navigation', dom2.window.location.hash === '#wa-handoff');
}

// ------------------------------------------------ B: optional fields set --
console.log('\n--- B. filled optional fields land in the right slots ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html');
  const w = dom.window, d = w.document;
  const nav = captureNav(w);
  fill(d, 'eqName', 'Kumari Silva');
  fill(d, 'eqContact', '071 999 8888');
  fill(d, 'eqEmail', 'owner@villa.lk');
  fill(d, 'eqType', 'Villa');
  fill(d, 'eqRooms', '12');
  fill(d, 'eqMsg', 'Villa with sea view, unawatuna.');
  submit(d.getElementById('enquiryForm'));
  const t = dec(nav[0]);
  ok('filled email is included', t.includes('Email: owner@villa.lk'));
  ok('email sits after contact and before property type',
     t.indexOf('Contact: 071 999 8888') < t.indexOf('Email: owner@villa.lk') &&
     t.indexOf('Email: owner@villa.lk') < t.indexOf('Property type:'));
  ok('filled rooms is included', t.includes('Rooms: 12'));
  ok('rooms sits after property type',
     t.indexOf('Property type:') < t.indexOf('Rooms: 12'));
  ok('the message follows rooms',
     t.indexOf('Rooms: 12') < t.indexOf('Villa with sea view, unawatuna.'));
  ok('property type reflects the selected value', t.includes('Property type: Villa'));
  ok('still exactly one handoff per submit', nav.length === 1);
}

// ------------------------------------------------------- C: campaign UTMs --
console.log('\n--- C. utm parameters ride along in the required order ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html?utm_source=fb-ads&utm_medium=cpc' +
                      '&utm_campaign=hotelmate_sep&utm_content=banner1&gclid=XYZ999&utm_term=hotels');
  const w = dom.window, d = w.document;
  const nav = captureNav(w);
  fill(d, 'eqName', 'Test Name');
  fill(d, 'eqContact', '077 000 0000');
  fill(d, 'eqMsg', 'Please book a demo.');
  submit(d.getElementById('enquiryForm'));
  const t = dec(nav[0]);
  ok('utm_source rides along', t.includes('utm_source: fb-ads'));
  ok('utm_medium rides along', t.includes('utm_medium: cpc'));
  ok('utm_campaign rides along', t.includes('utm_campaign: hotelmate_sep'));
  ok('utm_content rides along', t.includes('utm_content: banner1'));
  ok('strict order: source, medium, campaign, content',
     t.indexOf('utm_source: fb-ads') < t.indexOf('utm_medium: cpc') &&
     t.indexOf('utm_medium: cpc') < t.indexOf('utm_campaign: hotelmate_sep') &&
     t.indexOf('utm_campaign: hotelmate_sep') < t.indexOf('utm_content: banner1'));
  ok('UTM lines come after the message',
     t.indexOf('Please book a demo.') < t.indexOf('utm_source: fb-ads'));
  ok('non-listed trackers (gclid, utm_term) are NOT added to the message',
     !t.includes('gclid') && !t.includes('utm_term'));
}

// ---------------------------------------------------- D: fitLines, ASCII --
console.log('\n--- D. fitLines guard: long English message ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html');
  const w = dom.window, d = w.document;
  const nav = captureNav(w);
  fill(d, 'eqName', 'Long Message Tester');
  fill(d, 'eqContact', '077 111 1111');
  fill(d, 'eqMsg', 'A'.repeat(1500));
  submit(d.getElementById('enquiryForm'));
  ok('long English message keeps the URL under ~1900 chars', (nav[0] || '').length <= 1900);
  ok('fixed fields survive the guard',
     (nav[0] || '').startsWith(BASE) && dec(nav[0]).startsWith('Name: Long Message Tester\nContact: 077 111 1111'));
  ok('the campaign number never changes under the guard', (nav[0] || '').startsWith(BASE));
}

// -------------------------------------------------- E: fitLines, Sinhala --
console.log('\n--- E. fitLines guard: Sinhala text (about 9 URI chars per letter) ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html?utm_source=fb&utm_medium=cpc&utm_campaign=hm&utm_content=ad1');
  const w = dom.window, d = w.document;
  const nav = captureNav(w);
  fill(d, 'eqName', 'සිංහල නම ටෙස්ට්');
  fill(d, 'eqContact', '077 222 2222');
  fill(d, 'eqMsg', 'ආයුබෝවන් හෝටල්. '.repeat(150));
  submit(d.getElementById('enquiryForm'));
  ok('long Sinhala message keeps the URL under ~1900 chars', (nav[0] || '').length <= 1900);
  ok('the URL still decodes cleanly and starts with the name',
     dec(nav[0]).startsWith('Name: සිංහල නම ටෙස්ට්\nContact: 077 222 2222'));

  const dom2 = loadDom(ORIGIN + '/hotelmate.html?utm_source=fb&utm_medium=cpc&utm_campaign=hm&utm_content=ad1');
  const w2 = dom2.window, d2 = dom2.window.document;
  const nav2 = captureNav(w2);
  fill(d2, 'eqName', 'Test');
  fill(d2, 'eqContact', '077 333 3333');
  fill(d2, 'eqMsg', 'ආයුබෝවන්. '.repeat(10));
  submit(d2.getElementById('enquiryForm'));
  ok('moderate Sinhala + UTM fit together (UTM lines survive the guard)',
     (nav2[0] || '').length <= 1900 && dec(nav2[0]).includes('utm_content: ad1'));

  const dom3 = loadDom(ORIGIN + '/hotelmate.html');
  const w3 = dom3.window, d3 = dom3.window.document;
  const nav3 = captureNav(w3);
  fill(d3, 'eqName', 'අ'.repeat(120));
  fill(d3, 'eqContact', '077 444 4444');
  fill(d3, 'eqMsg', 'ය'.repeat(800));
  submit(d3.getElementById('enquiryForm'));
  ok('a huge Sinhala name plus long message still cannot overflow the guard',
     (nav3[0] || '').length <= 1900);

  const dom4 = loadDom(ORIGIN + '/hotelmate.html');
  const d4 = dom4.window.document;
  const nav4 = captureNav(dom4.window);
  fill(d4, 'eqName', 'Multi Line');
  fill(d4, 'eqContact', '077 555 5555');
  fill(d4, 'eqMsg', 'Line one\nLine two\nLine three');
  submit(d4.getElementById('enquiryForm'));
  ok('multi-line message keeps its line breaks in the WhatsApp text',
     dec(nav4[0]).includes('Line one\nLine two\nLine three'));
}

// ---------------------------------------------------------- F: validation --
console.log('\n--- F. validation and encoding hygiene ---');
{
  const dom = loadDom(ORIGIN + '/hotelmate.html');
  const w = dom.window, d = w.document;
  const nav = captureNav(w);
  fill(d, 'eqName', 'Test');
  fill(d, 'eqContact', '077 666 6666');
  fill(d, 'eqMsg', '   ');
  submit(d.getElementById('enquiryForm'));
  ok('whitespace-only message is rejected — no handoff at all', nav.length === 0);

  const dom2 = loadDom(ORIGIN + '/hotelmate.html');
  const d2 = dom2.window.document;
  const nav2 = captureNav(dom2.window);
  fill(d2, 'eqName', 'Test');
  fill(d2, 'eqContact', '');
  fill(d2, 'eqMsg', 'Hello there');
  submit(d2.getElementById('enquiryForm'));
  ok('missing contact is rejected, the error note shows, still no handoff',
     nav2.length === 0 && d2.getElementById('eqNote').className.includes('form-err'));

  const dom3 = loadDom(ORIGIN + '/hotelmate.html');
  const d3 = dom3.window.document;
  const nav3 = captureNav(dom3.window);
  fill(d3, 'eqName', 'Encode Check');
  fill(d3, 'eqContact', '077 777 7777');
  fill(d3, 'eqMsg', 'spaces  and\nnewlines & symbols ?#=');
  submit(d3.getElementById('enquiryForm'));
  ok('the handoff URL is fully encoded (no raw spaces, newlines or bare &?#)',
     nav3.length === 1 && !/[ \n]/.test(nav3[0].split('?text=')[1]) &&
     !/[&?#]/.test(nav3[0].split('?text=')[1]));
}

// ---------------------------------------------------------------- summary --
if (passed + failed !== COUNT) {
  console.log(`\n!! check harness error: expected ${COUNT} checks, ran ${passed + failed}`);
  process.exit(2);
}
console.log(`\n${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
