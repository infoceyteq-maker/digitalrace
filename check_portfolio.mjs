/* check_portfolio.mjs — boots the Ceyteq backend, publishes a client project through
 * the same /api/admin/portfolio endpoint the admin form uses, then loads
 * portfolio.html in jsdom and asserts the Client Work section paints it.
 *   node check_portfolio.mjs
 */
import { JSDOM, VirtualConsole } from 'jsdom';
import { spawn, execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import http from 'node:http';

/* The check runs its OWN server against a throwaway data dir, so it can never
 * touch the developer's or the production data/ceyteq.db. */
const PORT = 8317;
const BASE = `http://127.0.0.1:${PORT}`;
const DATA = fs.mkdtempSync(path.join(os.tmpdir(), 'ceyteq-portfolio-check-'));
const ENV = { ...process.env, CEYTEQ_DATA_DIR: DATA, PYTHONUNBUFFERED: '1' };
const results = [];
const ok = (m) => { results.push(['PASS', m]); console.log('  ✓', m); };
const bad = (m) => { results.push(['FAIL', m]); console.log('  ✗', m); };

const req = (path, { method = 'GET', body, cookie } = {}) => new Promise((resolve, reject) => {
  const data = body ? JSON.stringify(body) : null;
  const r = http.request(BASE + path, {
    method,
    headers: { 'Content-Type': 'application/json', ...(cookie ? { Cookie: cookie } : {}), ...(data ? { 'Content-Length': Buffer.byteLength(data) } : {}) },
  }, res => {
    let out = '';
    res.on('data', c => out += c);
    res.on('end', () => resolve({ status: res.statusCode, body: out, headers: res.headers }));
  });
  r.on('error', reject);
  if (data) r.write(data);
  r.end();
});

const ROOT = new URL('.', import.meta.url).pathname;
execFileSync('python3', ['server.py', '--init', '--admin-password', 'ceytec@2026'], { cwd: ROOT, env: ENV, stdio: 'ignore' });
const server = spawn('python3', ['server.py', '--host', '127.0.0.1', '--port', String(PORT)],
  { cwd: ROOT, env: ENV, stdio: ['ignore', 'ignore', 'pipe'] });

try {
  // wait for /api/health
  for (let i = 0; i < 60; i++) {
    try { if ((await req('/api/health')).status === 200) break; } catch { /* not up yet */ }
    await new Promise(r => setTimeout(r, 250));
  }

  // ---------------------------------------------------------- 1. the admin form
  const login = await req('/api/login', { method: 'POST', body: { username: 'admin', password: 'ceytec@2026' } });
  let cookie = (login.headers['set-cookie'] || [''])[0].split(';')[0];   // same jar the browser below uses
  if (login.status !== 200) bad('admin login failed (' + login.status + ') — run: python3 server.py --init --admin-password ceytec@2026');
  else ok('admin login works');

  JSON.parse((await req('/api/portfolio')).body).total === 0
    ? ok('starts from an empty throwaway database') : bad('temp database was not empty — check CEYTEQ_DATA_DIR handling');

  const entry = {
    client_name: 'Amara Tea Estate',
    project_title: 'Brand refresh, website and tour booking',
    area: 'Nuwara Eliya',
    category: 'Export & Import',
    services: ['Website', 'Designing', 'Photography'],
    summary: 'Packaging refresh, an export catalogue and a booking flow for estate tours.',
    media_links: 'assets/logo.jpg\nhttps://example.com/photo.png',
    folder_url: 'https://drive.google.com/drive/folders/test',
    website_url: 'https://example.com',
    logo_url: 'assets/logo-transparent.png',
    tags: ['Branding', 'Catalogue', 'Booking'],
    featured: 1, visible: 1,
  };
  const created = await req('/api/admin/portfolio', { method: 'POST', body: entry, cookie });
  created.status === 201 ? ok('admin form saved the entry (POST /api/admin/portfolio)') : bad('create failed: ' + created.status + ' ' + created.body);
  const id = JSON.parse(created.body || '{}').id;

  await req('/api/admin/portfolio', { method: 'POST', body: { client_name: 'Spice Garden Hotel', category: 'Hospitality', services: ['Website', 'Ads & Promotion'], media_links: 'assets/logo.jpg', visible: 1 }, cookie });

  const feed = await req('/api/portfolio');
  const payload = JSON.parse(feed.body);
  payload.items.length === 2 ? ok('/api/portfolio returns both entries') : bad('feed items = ' + payload.items.length);
  payload.items[0].client === 'Amara Tea Estate' ? ok('featured entry is first') : bad('featured order wrong');
  Array.isArray(payload.items[0].services) && payload.items[0].services.length === 3 ? ok('service models come back as a list') : bad('services not parsed');
  (feed.body.includes('http://') || !feed.body.includes('javascript:')) ? ok('no javascript: link survives') : bad('raw link leaked');
  const hidden = await req('/api/admin/portfolio/' + id, { method: 'PATCH', body: { visible: 0 }, cookie });
  hidden.status === 200 && (await req('/api/portfolio')).body.includes('Spice Garden') && !(await req('/api/portfolio')).body.includes('Amara')
    ? ok('hide in admin removes it from the public page') : bad('visibility toggle did not work');
  await req('/api/admin/portfolio/' + id, { method: 'PATCH', body: { visible: 1 }, cookie });

  const dirty = await req('/api/admin/portfolio', { method: 'POST', cookie, body: {
    client_name: 'Bad Links', media_links: 'javascript:alert(1)\n../../etc/passwd\nhttps://cdn.example.com/a.jpg\nnot-a-real-file.png',
    website_url: 'javascript:alert(1)', folder_url: 'data:text/html,<script>1</script>' } });
  const dirtyItem = JSON.parse((await req('/api/portfolio?q=Bad%20Links')).body).items[0];
  dirtyItem && dirtyItem.media.length === 1 && dirtyItem.media[0] === 'https://cdn.example.com/a.jpg'
    && !dirtyItem.website && !dirtyItem.folder
    ? ok('bad media/link values are dropped by the API') : bad('sanitiser let through: ' + JSON.stringify(dirtyItem && { m: dirtyItem.media, w: dirtyItem.website, f: dirtyItem.folder }));
  await req('/api/admin/portfolio/' + JSON.parse(dirty.body).id, { method: 'DELETE', cookie });

  const searched = JSON.parse((await req('/api/portfolio?q=nuwara')).body);
  searched.count === 1 && searched.items[0].client === 'Amara Tea Estate' ? ok('server-side search finds it by area') : bad('q=nuwara → ' + searched.count);
  const filtered = JSON.parse((await req('/api/portfolio?category=Hospitality')).body);
  filtered.count === 1 ? ok('category filter works server-side') : bad('category filter → ' + filtered.count);

  // ---------------------------------------------------------- 2. the public page
  const page = await req('/portfolio.html');
  const dom = new JSDOM(page.body, {
    url: BASE + '/portfolio.html',
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),               // keep the log readable
    beforeParse(w) {
      w.fetch = (u, o) => fetch(new URL(u, BASE).href, o);   // jsdom ships no fetch
      w.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
      w.matchMedia = w.matchMedia || (q => ({ matches: false, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }));
      w.Element.prototype.scrollIntoView = function () {};
      w.HTMLElement.prototype.focus = function () {};
    },
  });
  const w = dom.window;
  const html = () => w.document.getElementById('pf-results').innerHTML;
  for (let i = 0; i < 30 && !w.document.querySelector('.pf-card'); i++) await new Promise(r => setTimeout(r, 200));

  const cards = w.document.querySelectorAll('.pf-card');
  cards.length === 2 ? ok('portfolio.html paints 2 client cards') : bad('cards = ' + cards.length + ' :: ' + html().slice(0, 200));
  const first = cards[0];
  first && first.querySelector('h3').textContent.includes('Brand refresh') ? ok('card headline is the project title') : bad('headline wrong: ' + (first && first.querySelector('h3')?.textContent));
  first && first.querySelector('.pf-cat').textContent.trim() === 'Export & Import' ? ok('business category badge shows') : bad('category badge: ' + first?.querySelector('.pf-cat')?.textContent);
  first && first.querySelector('.pf-cover img') ? ok('cover image taken from the first media link') : bad('no cover image');
  first && first.querySelectorAll('.pf-tags li').length === 3 ? ok('service tags render as chips') : bad('tags = ' + first?.querySelectorAll('.pf-tags li').length);
  first && first.querySelector('.pf-star') ? ok('featured entry shows the ★ ribbon') : bad('featured ribbon missing');
  first && /Media \(2\)/.test(first.textContent) ? ok('media button counts the 2 uploads') : bad('media button: ' + first?.querySelectorAll('.pf-actions button')[0]?.textContent);
  first && first.innerHTML.includes('drive.google.com/drive/folders/test') ? ok('folder link button present') : bad('folder link missing');
  first && /wa\.me\/94788607143\?text=/.test(first.innerHTML) ? ok('WhatsApp quote button prefilled from the project') : bad('quote link missing');

  const chips = [...w.document.querySelectorAll('#pf-chips button')].map(b => b.textContent.replace(/\s+/g, ' ').trim());
  chips.length === 3 && chips[0] === 'All clients 2' ? ok('category chips: ' + chips.join(' | ')) : bad('chips = ' + JSON.stringify(chips));

  // search bar filters live
  const search = w.document.getElementById('pf-search');
  search.value = 'spice';
  search.dispatchEvent(new w.Event('input', { bubbles: true }));
  w.document.querySelectorAll('.pf-card').length === 1 ? ok('search bar narrows to 1 card') : bad('search left ' + w.document.querySelectorAll('.pf-card').length + ' cards');
  search.value = 'zzzz';
  search.dispatchEvent(new w.Event('input', { bubbles: true }));
  /No client project matches/.test(html()) ? ok('empty search shows the friendly no-match note') : bad('no-match state missing');
  w.document.getElementById('pf-clear').dispatchEvent(new w.Event('click', { bubbles: true }));
  w.document.querySelectorAll('.pf-card').length === 2 ? ok('clear button restores the list') : bad('clear failed');

  // service button re-groups by service model
  w.document.querySelector('.pf-view button[data-view="service"]').dispatchEvent(new w.Event('click', { bubbles: true }));
  const groups = [...w.document.querySelectorAll('#pf-results .pf-group .subcategory-title')].map(h => h.textContent.replace(/\s+/g, ' ').trim());
  groups.some(g => /Website \(2\)/.test(g)) ? ok('service button groups by service model: ' + groups.join(' | ')) : bad('service groups = ' + JSON.stringify(groups));
  w.document.querySelector('.pf-view button[data-view="client"]').dispatchEvent(new w.Event('click', { bubbles: true }));

  // client logo strip + counter
  const logos = w.document.querySelectorAll('#pf-track .pf-logo');
  logos.length === 4 ? ok('client logo strip animates (2 clients × 2 copies)') : bad('logo tiles = ' + logos.length);
  w.document.getElementById('pf-logos').hidden === false ? ok('logo strip is shown once entries exist') : bad('logo strip hidden');
  logos[0].dispatchEvent(new w.Event('click', { bubbles: true }));
  w.document.querySelectorAll('.pf-card').length === 1 ? ok('clicking a client logo filters the grid') : bad('logo filter failed');
  w.pfReset();
  for (let i = 0; i < 40 && w.document.getElementById('pf-stat').textContent !== '2'; i++) await new Promise(r => setTimeout(r, 50));
  w.document.getElementById('pf-stat').textContent === '2' ? ok('stats band gains a live “Client Projects Published” number') : bad('pf-stat = ' + w.document.getElementById('pf-stat').textContent);

  // media viewer
  w.document.querySelector('.pf-card .pf-actions button').dispatchEvent(new w.Event('click', { bubbles: true }));
  const modal = w.document.getElementById('pf-modal');
  modal.hidden === false ? ok('media viewer opens') : bad('modal did not open');
  w.document.querySelectorAll('#pf-modal-body figure').length === 2 ? ok('viewer shows both media items') : bad('viewer figures = ' + w.document.querySelectorAll('#pf-modal-body figure').length);
  w.document.dispatchEvent(new w.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  modal.hidden === true ? ok('Escape closes the viewer') : bad('escape close failed');

  // ------------------------------------------------------------ 3. admin + nav
  const admin = await req('/admin.html');
  const a = new JSDOM(admin.body).window.document;
  a.getElementById('tab-portfolio') ? ok('admin has the Portfolio tab') : bad('admin tab missing');
  const labels = [...a.querySelectorAll('#pfServices label input')].map(i => i.value);
  labels.length === 11 && labels[0] === 'Website' ? ok('form has the 11 service models') : bad('service chips = ' + JSON.stringify(labels));
  const cats = [...a.querySelectorAll('#pfCategory option')].map(o => o.value).filter(Boolean);
  cats.length === 11 && cats[0] === 'IT & Digital' ? ok('select has the 11 business categories') : bad('categories = ' + JSON.stringify(cats));
  ['pfClient', 'pfArea', 'pfCategory', 'pfSummary', 'pfMedia', 'pfFolder', 'pfTags', 'pfFiles', 'pfSaveBtn'].every(i => a.getElementById(i))
    ? ok('every field of the brief exists in the form') : bad('a form field is missing');
  a.getElementById('pfForm').getAttribute('onsubmit') === 'return savePortfolio(event)' ? ok('form wired to savePortfolio()') : bad('form not wired');
  // the form itself: log in, switch tab, fill it in, press Save
  const adminPage = await req('/admin.html');
  const adom = new JSDOM(adminPage.body, {
    url: BASE + '/admin.html',
    runScripts: 'dangerously',
    pretendToBeVisual: true,
    virtualConsole: new VirtualConsole(),
    beforeParse(w2) {
      // the admin panel is cookie-authenticated, so hand its fetch the same session cookie
      w2.fetch = async (u, o) => {
        const res = await fetch(new URL(u, BASE).href, { ...o, headers: { ...(o && o.headers || {}), ...(cookie ? { Cookie: cookie } : {}) } });
        const set = typeof res.headers.getSetCookie === 'function' ? res.headers.getSetCookie() : [];
        if (set.length) cookie = set.map(c => c.split(';')[0]).join('; ');
        return res;
      };
      w2.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
      w2.matchMedia = w2.matchMedia || (q => ({ matches: false, media: q, addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} }));
      w2.Element.prototype.scrollIntoView = function () {};
      w2.confirm = () => true;
      w2.alert = () => {};
    },
  });
  const A = adom.window, ad = A.document;
  await new Promise(r => setTimeout(r, 250));
  ad.getElementById('auser').value = 'admin';
  ad.getElementById('apass').value = 'ceytec@2026';
  A.doLogin();
  for (let i = 0; i < 40 && ad.getElementById('dashBox').style.display !== 'block'; i++) await new Promise(r => setTimeout(r, 100));
  ad.getElementById('dashBox').style.display === 'block' ? ok('admin login through the panel works') : bad('dashboard never showed');
  A.showTab('portfolio');
  for (let i = 0; i < 40 && ad.querySelector('#pfTable tbody tr td').textContent.includes('Amara'); i++) { A.loadPortfolio(); await new Promise(r => setTimeout(r, 150)); }
  ad.getElementById('tab-portfolio').style.display === 'block' ? ok('Portfolio Upload tab opens') : bad('tab did not open');
  // upload one cover image, exactly like the admin would
  try {
    const png = new A.File([new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])], 'amara-cover.png', { type: 'image/png' });
    Object.defineProperty(ad.getElementById('pfFiles'), 'files', { value: [png], configurable: true });
    A.pfUploadFiles();
    for (let i = 0; i < 40 && !ad.getElementById('pfMedia').value.includes('uploads/amara-cover.png'); i++) await new Promise(r => setTimeout(r, 100));
    ad.getElementById('pfMedia').value.includes('uploads/amara-cover') ? ok('image upload lands in the media list as uploads/…') : bad('upload did not fill the media box: ' + ad.getElementById('pfMedia').value);
  } catch (e) { bad('file upload step threw: ' + e.message); }
  // a client logo can be uploaded instead of linked
  try {
    const logo = new A.File([new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])], 'kandy-tea-logo.png', { type: 'image/png' });
    Object.defineProperty(ad.getElementById('pfLogoFile'), 'files', { value: [logo], configurable: true });
    A.pfUploadLogo();
    for (let i = 0; i < 40 && !ad.getElementById('pfLogo').value.startsWith('uploads/'); i++) await new Promise(r => setTimeout(r, 100));
    ad.getElementById('pfLogo').value.startsWith('uploads/kandy-tea-logo') ? ok('logo upload fills the logo field with uploads/…') : bad('logo field = ' + ad.getElementById('pfLogo').value);
  } catch (e) { bad('logo upload step threw: ' + e.message); }
  // fill the fields of the brief
  A.savePortfolio(new A.Event('submit'));      // Client Name is the only required field
  await new Promise(r => setTimeout(r, 250));
  /is required/.test(ad.getElementById('pfNote').textContent) ? ok('form refuses a save without a Client Name') : bad('validation note = ' + ad.getElementById('pfNote').textContent);
  ad.getElementById('pfClient').value = 'Kandy Tea Room';
  ad.getElementById('pfProject').value = 'Cafe website, menu and Google profile';
  ad.getElementById('pfArea').value = 'Kandy Road, Matale';
  ad.getElementById('pfCategory').value = 'Food & Beverage';
  [...ad.querySelectorAll('#pfServices input')].filter(i => ['Website', 'Printing'].includes(i.value)).forEach(i => { i.checked = true; A.pfChip(i); });
  ad.getElementById('pfSummary').value = 'Cafe website, menu printing and a Google Business refresh.';
  ad.getElementById('pfFolder').value = 'https://drive.google.com/drive/folders/cafe-pack';
  ad.getElementById('pfTags').value = 'Menu design, GBP, Photography';
  ad.getElementById('pfFeatured').checked = false;
  A.savePortfolio(new A.Event('submit'));
  for (let i = 0; i < 40 && !/live on the Portfolio page/.test(ad.getElementById('pfNote').textContent); i++) await new Promise(r => setTimeout(r, 100));
  /live on the Portfolio page/.test(ad.getElementById('pfNote').textContent) ? ok('form save publishes the entry') : bad('save note = ' + ad.getElementById('pfNote').textContent);
  for (let i = 0; i < 30 && ad.querySelectorAll('#pfTable tbody tr').length < 3; i++) { A.loadPortfolio(); await new Promise(r => setTimeout(r, 100)); }
  // the published card must show the uploaded logo
  const live = new JSDOM(page.body, {
    url: BASE + '/portfolio.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
    beforeParse(w5) {
      w5.fetch = (u, o) => fetch(new URL(u, BASE).href, o);
      w5.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
      w5.matchMedia = () => ({ matches: false, media: '', addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
      w5.Element.prototype.scrollIntoView = function () {};
    },
  });
  for (let i = 0; i < 30 && !live.window.document.querySelector('.pf-card .pf-client img'); i++) await new Promise(r => setTimeout(r, 100));
  const logoImg = live.window.document.querySelector('.pf-card .pf-client img');
  logoImg && /^(uploads|assets)\//.test(logoImg.getAttribute('src') || '')
    ? ok('card shows the client logo next to the name') : bad('card logo missing: ' + (logoImg && logoImg.getAttribute('src')));

  ad.querySelectorAll('#pfTable tbody tr').length === 3 ? ok('admin table lists all 3 entries') : bad('admin rows = ' + ad.querySelectorAll('#pfTable tbody tr').length);
  const feedAfterForm = JSON.parse((await req('/api/portfolio')).body);
  feedAfterForm.total === 3 ? ok('the same 3 entries are on the public feed') : bad('feed total = ' + feedAfterForm.total);
  const cafe = feedAfterForm.items.find(i => i.client === 'Kandy Tea Room');
  const uploaded = cafe && cafe.media[0] && cafe.media[0].startsWith('uploads/');
  uploaded && (await req('/' + cafe.media[0])).status === 200 ? ok('uploaded cover is served from uploads/') : bad('uploaded media not reachable: ' + (cafe && cafe.media[0]));
  cafe && String(cafe.logo).startsWith('uploads/') ? ok('the uploaded logo is stored and served') : bad('stored logo = ' + (cafe && cafe.logo));
  cafe && cafe.services.join('|') === 'Website|Printing' && cafe.media.length === 1 && cafe.tags.length === 3
    ? ok('what was ticked/typed in the form is what the page receives') : bad('stored entry = ' + JSON.stringify(cafe));
  ad.getElementById('pfNote').innerHTML = '';
  A.pfEdit(cafe.id);
  ad.getElementById('pfClient').value === 'Kandy Tea Room' && [...ad.querySelectorAll('#pfServices input:checked')].length === 2 && ad.getElementById('pfCategory').value === 'Food & Beverage'
    ? ok('edit loads the saved entry back into the form') : bad('edit did not repopulate');
  const hiddenRow = ad.querySelector('#pfTable tbody tr:last-child');
  if (hiddenRow.querySelector('button.mini')) A.pfPatch(cafe.id, { visible: 0 });
  for (let i = 0; i < 30 && JSON.parse((await req('/api/portfolio')).body).total !== 2; i++) await new Promise(r => setTimeout(r, 100));
  JSON.parse((await req('/api/portfolio')).body).total === 2 ? ok('hide button in the table takes it off the public page') : bad('hide failed');
  A.pfPatch(cafe.id, { visible: 1 });
  await new Promise(r => setTimeout(r, 300));

  const contact = (await req('/contact.html')).body;
  /<div class="staffbar">[\s\S]{0,1500}?href="admin\.html"/.test(contact) ? ok('Contact page leads with the Admin button') : bad('contact admin button missing');
  const nav = (await req('/index.html')).body;
  nav.includes('portfolio.html') ? ok('shared nav still links Portfolio') : bad('nav lost Portfolio');
  // new styles must stay scoped: client grid on portfolio.html only, form CSS in admin.html only
  const homeCss = nav.includes('.pf-card') || nav.includes('.pffields');
  homeCss ? bad('portfolio/admin CSS leaked into the home page') : ok('home page CSS untouched by this feature');
  const adminCss = (await req('/admin.html')).body;
  adminCss.includes('.pffields input:not([type=file]):not([type=checkbox])') && adminCss.includes('.pfchecks input{')
    ? ok('admin form CSS ships with admin.html (and leaves tick boxes native)') : bad('admin form CSS missing');

  // ------------------------------------------------------------ 4. empty + offline states
  const del = await req('/api/admin/portfolio/' + id, { method: 'DELETE', cookie });
  const rest = JSON.parse((await req('/api/admin/portfolio', { cookie })).body);
  for (const row of rest) await req('/api/admin/portfolio/' + row.id, { method: 'DELETE', cookie });
  del.status === 200 && JSON.parse((await req('/api/portfolio')).body).total === 0
    ? ok('delete takes the entry off the page (and the test dir is thrown away)') : bad('delete failed');

  const emptyDom = new JSDOM(page.body, {
    url: BASE + '/portfolio.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
    beforeParse(w3) {
      w3.fetch = (u, o) => fetch(new URL(u, BASE).href, o);
      w3.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
      w3.matchMedia = () => ({ matches: false, media: '', addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
      w3.Element.prototype.scrollIntoView = function () {};
    },
  });
  for (let i = 0; i < 30 && !/No client projects published yet/.test(emptyDom.window.document.getElementById('pf-results').innerHTML); i++) await new Promise(r => setTimeout(r, 100));
  const ed = emptyDom.window.document;
  /No client projects published yet/.test(ed.getElementById('pf-results').innerHTML)
    ? ok('empty database shows the “publish from the admin” note, not a broken grid') : bad('empty state missing: ' + ed.getElementById('pf-results').innerHTML.slice(0, 160));
  ed.getElementById('pf-toolbar').hidden && ed.getElementById('pf-logos').hidden ? ok('search bar and logo strip stay hidden with nothing to browse') : bad('toolbar shown with no data');

  const offlineDom = new JSDOM(page.body, {
    url: 'http://127.0.0.1:9/portfolio.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: new VirtualConsole(),
    beforeParse(w4) {
      w4.fetch = () => Promise.reject(new Error('offline'));   // static hosting: no api at all
      w4.IntersectionObserver = class { observe() {} unobserve() {} disconnect() {} };
      w4.matchMedia = () => ({ matches: false, media: '', addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {} });
      w4.Element.prototype.scrollIntoView = function () {};
    },
  });
  for (let i = 0; i < 30 && !/is not answering/.test(offlineDom.window.document.getElementById('pf-results').innerHTML); i++) await new Promise(r => setTimeout(r, 100));
  /is not answering/.test(offlineDom.window.document.getElementById('pf-results').innerHTML)
    ? ok('static hosting (no backend) degrades to an explainer, no JS error') : bad('offline state missing');
  // the rest of the page still works without the API
  offlineDom.window.document.querySelectorAll('.pf-card').length === 0 && offlineDom.window.document.querySelector('#service-panels').children.length === 5
    ? ok('the 100-service catalogue above still renders (5 tabs)') : bad('service tabs broke');
} catch (e) {
  bad('exception: ' + (e && e.stack || e));
} finally {
  server.kill();
  fs.rmSync(DATA, { recursive: true, force: true });
}

const failed = results.filter(r => r[0] === 'FAIL').length;
console.log('\n' + (failed ? failed + ' problem(s)' : 'all front-end checks passed'));
process.exit(failed ? 1 : 0);
