#!/usr/bin/env node
// privacy_matrix.cjs: walk pages and journeys in several privacy states and record what tracking fires.
//
// Each scenario runs in a fresh browser profile per state. The state is applied, the steps
// are walked, and three things are saved under <out>/<state>/:
//   hits.har            every collection request (the COLLECT list below), tagged with the
//                       scenario, the step that was running and the frame that sent it.
//                       Decode it with decode_hits.py (--by-step, --by-source).
//   har/<scenario>.har  the full Playwright HAR of that scenario (every request).
//   inventory.json      per step: page_inventory.js results, dataLayer snapshots, what a
//                       click hit, navigations stopped, pop-ups, redirects, errors.
//
// States:
//   fresh    first visit, no banner interaction
//   accept   click the banner's accept button, then continue
//   reject   click the banner's reject button, then continue
//   gpc      Global Privacy Control on (Sec-GPC header + navigator.globalPrivacyControl)
//   blocked  common tracker domains blocked, like an ad blocker
//
// --dry (recommended on live sites): collection requests never leave the machine. Each one
// is answered locally with HTTP 204 and logged in full (method, URL, body, frame, step), so
// the audit sees exactly what would have been sent without adding test page views, clicks
// or conversions to the client's analytics and ad accounts. Requests are fulfilled, not
// aborted: an aborted request loses its POST body, and batched GA4, TikTok and Shopify hits
// travel in POST bodies. Page loads (HTML, scripts, images) still reach the site. Without
// --dry the hits are real; use that only to confirm the receiving side (GA4 DebugView, Meta
// Test Events) with the owner's OK. --dry-extra <regex> adds endpoints the list misses (a
// server-side tagging path on the client's own domain, say).
//
// Visitor profile: the automation flag is hidden by default (navigator.webdriver false,
// --disable-blink-features=AutomationControlled, a normal Chrome user agent), because some
// pixels (Meta's) send nothing to a browser that says it is automated. --webdriver-visible
// turns this off.
//
// Usage (Playwright must be installed where Node can find it, e.g. `npm i playwright`
// in a scratch folder, or NODE_PATH pointing at a node_modules that has it):
//   node privacy_matrix.cjs --dry --url https://store.example.com/ --out ./matrix
//   node privacy_matrix.cjs --dry --scenarios journeys.json --states fresh,gpc,blocked --out ./matrix
//   node privacy_matrix.cjs --dry --url https://a/ --accept "#my-accept" --reject "#my-reject"
//   node privacy_matrix.cjs --dry --url https://a/ --steps journey.json --proxy http://eu-proxy:8080
//
// journeys.json: a list of scenarios, each in its own fresh profile; "states" (optional)
// limits the states a scenario runs in.
//   [{"name": "home", "steps": [
//      {"label": "home", "goto": "https://store.example.com/", "inventory": true, "dataLayer": true},
//      {"label": "header book now", "click": "header a", "text": "book now", "dataLayer": true},
//      {"label": "booking page", "goto": "https://book.example.com/start", "wait": 9000}]},
//    {"name": "product", "states": ["fresh", "gpc"], "steps": [...]}]
// --steps journey.json: a plain list of steps run after the --url pages, in the same profile.
// Step keys: label, goto (absolute, or relative to the current page), click (CSS selector,
// plus "text" to match the visible text), fill ([selector, value], test values only), wait
// (ms after the step), inventory (scroll once, then page_inventory.js), dataLayer (event
// names and keys only, never values).
//
// Clicks are dispatched on the element from inside the page (element.click()), so overlays,
// sticky bars and pop-ups cannot swallow them. When the element is a link, its navigation is
// answered locally with 204 so the page stays put; the click event itself is untouched, so
// tag-manager link listeners (including link-click triggers with "Check validation") see a
// normal click. The would-be destination is recorded; test it with its own goto step.
// "navigate": true lets the link navigate. "stop": "prevent" stops it with a capture-phase
// preventDefault instead (also proven, but it hides the click from triggers that check
// validation). Buttons and other elements are never stopped, so an add to cart works.
//
// Region: the store decides by IP. Use --proxy with a proxy in the region you need, or
// report that region as not tested. Never put real customer data in a journey.
// Read-only toward the site except the clicks you script; never complete a real purchase
// or booking without the owner's explicit OK.
'use strict';
const fs = require('fs');
const path = require('path');

let chromium;
try { ({ chromium } = require('playwright')); } catch (e) {
  console.error('Playwright not found. Run `npm i playwright` in a scratch folder and run this script from there, or set NODE_PATH.');
  process.exit(2);
}

const args = process.argv.slice(2);
const opt = { urls: [], states: ['fresh', 'accept', 'reject', 'gpc'], out: './privacy-matrix', wait: 6000 };
for (let i = 0; i < args.length; i++) {
  const a = args[i], v = args[i + 1];
  if (a === '--url') { opt.urls.push(v); i++; }
  else if (a === '--states') { opt.states = v.split(','); i++; }
  else if (a === '--out') { opt.out = v; i++; }
  else if (a === '--accept') { opt.accept = v; i++; }
  else if (a === '--reject') { opt.reject = v; i++; }
  else if (a === '--steps') { opt.steps = JSON.parse(fs.readFileSync(v, 'utf8')); i++; }
  else if (a === '--scenarios') { opt.scenarios = JSON.parse(fs.readFileSync(v, 'utf8')); i++; }
  else if (a === '--proxy') { opt.proxy = v; i++; }
  else if (a === '--wait') { opt.wait = Number(v); i++; }
  else if (a === '--dry') { opt.dry = true; }
  else if (a === '--dry-extra') { opt.dryExtra = v; i++; }
  else if (a === '--summary') { opt.summary = true; }
  else if (a === '--webdriver-visible') { opt.webdriverVisible = true; }
  else if (a === '--headed') { opt.headed = true; }
  else { console.error(`Unknown option ${a}`); process.exit(2); }
}
// A --steps file written as a list of scenarios is treated as --scenarios.
if (Array.isArray(opt.steps) && opt.steps.length && opt.steps.every(s => s && Array.isArray(s.steps))) {
  opt.scenarios = [...(opt.scenarios || []), ...opt.steps];
  delete opt.steps;
}
if (!opt.urls.length && !opt.scenarios && !opt.steps) { console.error('Give at least one --url, or a --scenarios file'); process.exit(2); }

// Best-known banner buttons. Confirm on the site; pass --accept/--reject when they differ.
const ACCEPT = [
  '#shopify-pc__banner__btn-accept', '#onetrust-accept-btn-handler',
  '#CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll', '#CybotCookiebotDialogBodyButtonAccept',
  '.cky-btn-accept', '#didomi-notice-agree-button', '[data-testid="uc-accept-all-button"]',
  'button:has-text("Accept all")', 'button:has-text("Accept")', 'button:has-text("Allow all")',
];
const REJECT = [
  '#shopify-pc__banner__btn-decline', '#onetrust-reject-all-handler',
  '#CybotCookiebotDialogBodyButtonDecline', '.cky-btn-reject', '#didomi-notice-disagree-button',
  '[data-testid="uc-deny-all-button"]', 'button:has-text("Reject all")', 'button:has-text("Decline")',
  'button:has-text("Reject")',
];
const BLOCK = /googletagmanager\.com|google-analytics\.com|\/g\/collect|doubleclick\.net|googleadservices\.com|connect\.facebook\.net|facebook\.com\/tr|analytics\.tiktok\.com|clarity\.ms|bat\.bing\.com|hotjar|ct\.pinterest\.com|snapchat\.com|redditstatic\.com|alb\.reddit\.com|klaviyo\.com|luckyorange|crazyegg/;
// The blocked state also refuses these hosts at DNS level, so requests from any frame or
// worker (Shopify app pixels run in web workers) fail the way a DNS blocklist makes them fail.
const BLOCK_HOSTS = ['*.googletagmanager.com', '*.google-analytics.com', 'analytics.google.com', '*.doubleclick.net',
  '*.googleadservices.com', 'connect.facebook.net', 'www.facebook.com', 'analytics.tiktok.com', '*.clarity.ms',
  'bat.bing.com', '*.hotjar.com', '*.hotjar.io', 'ct.pinterest.com', 's.pinimg.com', 'tr.snapchat.com', 'sc-static.net',
  'www.redditstatic.com', 'alb.reddit.com', 'static.klaviyo.com', 'static-tracking.klaviyo.com', '*.luckyorange.com',
  '*.luckyorange.net', 'script.crazyegg.com'];

// Collection endpoints: what --dry answers locally and what hits.har records. Scripts and
// configuration files are not in the list, so every tool loads and behaves as for a visitor.
const COLLECT_PARTS = [
  String.raw`/g/(s/)?collect`,                                // GA4, first-party GA4 endpoints, Google mirrors
  String.raw`/collect\?v=2`,                                  // GA4 protocol on other paths (Merchant Center, server-side tagging)
  String.raw`google-analytics\.com/(j/|r/)?collect`,          // Universal Analytics leftovers
  String.raw`/ccm/(s/)?collect`,                              // Google Ads and Google tag measurement
  String.raw`/pagead/(viewthroughconversion|conversion|1p-conversion|1p-user-list|landing)`,
  String.raw`/rmkt/collect`,                                  // Google Ads remarketing
  String.raw`googletagmanager\.com/td(\?|$)`,                 // Google tag diagnostics
  String.raw`merchant-center-analytics\.goog`,                // Merchant Center (Google & YouTube app)
  String.raw`doubleclick\.net/activity`,                      // Floodlight
  String.raw`facebook\.com/tr(/|\?|$)|facebook\.com/privacy_sandbox/`, // Meta pixel
  String.raw`analytics\.tiktok\.com/api/`,                    // TikTok, including the Shopify app's /api/v2/shopify_pixel
  String.raw`\.clarity\.ms/collect`,
  String.raw`//bat\.bing\.(com|net)/action`,                  // Microsoft UET
  String.raw`//ct\.pinterest\.com/(v3|user)`,
  String.raw`//alb\.reddit\.com/rp\.gif`,
  String.raw`//tr(-shadow)?\.snapchat\.com/(p(\?|/|$)|cm/|v\d/)`, // Snapchat (not its /config script)
  String.raw`//px\.ads\.linkedin\.com/`,
  String.raw`//(analytics\.twitter\.com|t\.co)/i/adsct`,
  String.raw`/monorail/|monorail-edge\.shopifysvc\.com|/produce_batch`, // Shopify's own analytics
  String.raw`config-security\.com`,                           // Triple Whale
  String.raw`//a\.klaviyo\.com/(client/|onsite/track|api/(track|identify))`,
  String.raw`contentsquare\.net/.*(collect|events|i\?)`,     // Contentsquare and Hotjar on Contentsquare
  String.raw`//in\.hotjar\.com/|\.hotjar\.io/`,
  String.raw`callrail\.com/[^?]*swap_session`,                // CallRail visitor sessions
];
const COLLECT = new RegExp(COLLECT_PARTS.join('|') + (opt.dryExtra ? '|' + opt.dryExtra : ''));
const WS_COLLECT = /hotjar\.(com|io)|contentsquare\.net|clarity\.ms/; // live-session sockets

const inventoryCode = fs.readFileSync(path.join(__dirname, 'page_inventory.js'), 'utf8');

const hostOf = u => { try { return new URL(u).hostname; } catch (e) { return ''; } };
const hostBlocked = h => BLOCK_HOSTS.some(p => p.startsWith('*.') ? h.endsWith(p.slice(1)) : h === p);
const safeName = s => String(s).replace(/[^\w.-]+/g, '_').slice(0, 60) || 'scenario';

function visitorUserAgent(version) {
  const major = String(version).split('.')[0];
  const os = process.platform === 'darwin' ? 'Macintosh; Intel Mac OS X 10_15_7'
    : process.platform === 'win32' ? 'Windows NT 10.0; Win64; x64' : 'X11; Linux x86_64';
  return `Mozilla/5.0 (${os}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/${major}.0.0.0 Safari/537.36`;
}

// Which frame sent a request: the top page, a Shopify pixel sandbox, another iframe, or a
// service worker (request.frame() throws for service-worker requests).
function frameInfo(req) {
  let f;
  try { f = req.frame(); } catch (e) {
    let sw = false; try { sw = !!(req.serviceWorker && req.serviceWorker()); } catch (x) { /* older Playwright */ }
    return { kind: sw ? 'service-worker' : 'no-frame', url: '' };
  }
  if (!f) return { kind: 'no-frame', url: '' };
  let url = '', top = false;
  try { url = f.url() || ''; } catch (e) { /* detached */ }
  try { top = f.parentFrame() === null; } catch (e) { /* detached */ }
  const kind = top ? 'top'
    : /\/web-pixels@[^/]*\/cust/.test(url) ? 'shopify-custom-pixel'
    : /\/web-pixels@/.test(url) ? 'shopify-app-pixel'
    : 'iframe';
  return { kind, url: url.slice(0, 200) };
}

function bodyOf(req) {
  let buf = null;
  try { buf = req.postDataBuffer(); } catch (e) { /* no body */ }
  if (!buf || !buf.length) return { text: '' };
  const text = buf.toString('utf8');
  // Compressed or binary bodies (Clarity, some replay tools) are kept as a size only.
  if (text.includes('�') || /[\x00-\x08\x0E-\x1F]/.test(text)) return { text: '', binaryBytes: buf.length };
  return { text };
}

function hitEntry(method, url, m, status, dry, failure) {
  const e = { startedDateTime: m.time, request: { method, url, postData: { text: m.body.text } }, response: { status },
    _scenario: m.scenario, _step: m.step, _frame: m.frame.url, _frameKind: m.frame.kind, _dry: dry };
  if (m.body.binaryBytes) e._binaryBytes = m.body.binaryBytes;
  if (failure) e._failure = failure;
  return e;
}

// gtag commands and dataLayer pushes, with keys only (consent commands keep their values).
const DATALAYER_SNAPSHOT = () => (window.dataLayer || []).map(e => {
  try {
    if (e && typeof e === 'object' && typeof e.length === 'number' && !Array.isArray(e)) {
      const a = Array.from(e), p = a[2] && typeof a[2] === 'object' ? a[2] : null;
      return { gtag: [a[0], typeof a[1] === 'string' ? a[1] : typeof a[1]],
        [a[0] === 'consent' ? 'values' : 'keys']: p ? (a[0] === 'consent' ? p : Object.keys(p).slice(0, 15)) : undefined };
    }
    return { event: e && e.event, keys: e && typeof e === 'object' ? Object.keys(e).slice(0, 15) : [] };
  } catch (x) { return '?'; }
});

async function clickFirst(page, selectors) {
  for (const sel of selectors) {
    try {
      const el = page.locator(sel).first();
      if (await el.isVisible({ timeout: 800 })) { await el.click({ timeout: 2000 }); return sel; }
    } catch (e) { /* try next */ }
  }
  return null;
}

async function runInventory(page) {
  try {
    // A real wheel scroll first: some sites load tools only after the first interaction.
    await page.mouse.wheel(0, 900); await page.waitForTimeout(1200);
    await page.mouse.wheel(0, -900); await page.waitForTimeout(3500);
    if (opt.summary) await page.evaluate(() => { window.PAGE_INVENTORY_MODE = 'summary'; });
    return await page.evaluate(inventoryCode);
  } catch (e) { return { error: String(e).slice(0, 300) }; }
}

async function runClick(ctx, page, st, rec) {
  rec.clicked = await page.evaluate(({ sel, text }) => {
    const norm = s => (s || '').replace(/\s+/g, ' ').trim().toLowerCase();
    let els = [...document.querySelectorAll(sel)];
    if (text) els = els.filter(e => norm(e.innerText || e.textContent).includes(norm(text)));
    const el = els.find(e => e.getClientRects().length && (e.offsetWidth || e.offsetHeight)) || els[0];
    window.__auditClickTarget = el || null;
    if (!el) return null;
    const link = el.closest('a[href]');
    return { tag: el.tagName.toLowerCase(), text: norm(el.innerText || el.textContent).slice(0, 80),
      href: link ? link.href : null, target: (link && link.target) || null, visible: !!el.getClientRects().length, matches: els.length };
  }, { sel: st.click, text: st.text || null });
  if (!rec.clicked) { rec.error = `nothing matches ${st.click}${st.text ? ` with text "${st.text}"` : ''}`; return; }
  const isLink = !!rec.clicked.href && !/^(tel|mailto|sms|javascript):/i.test(rec.clicked.href);
  const mode = !isLink || st.navigate ? 'none' : st.stop === 'prevent' ? 'prevent' : 'local';
  if (isLink) rec.navigation = mode === 'none' ? 'followed' : mode === 'prevent' ? 'stopped (preventDefault)' : 'stopped (answered 204)';
  let stopRoute = null;
  if (mode === 'local') {
    // Any top-level navigation during this step (the link, a JavaScript redirect it triggers,
    // a new tab) gets an empty 204: the browser stays on the current page.
    stopRoute = async route => {
      const req = route.request();
      let top = false;
      if (req.isNavigationRequest()) {
        // A new tab's first navigation has no frame yet, and request.frame() throws.
        try { top = req.frame().parentFrame() === null; } catch (e) { top = req.resourceType() === 'document'; }
      }
      if (!top) return route.fallback();
      (rec.stoppedNavigations = rec.stoppedNavigations || []).push(req.url());
      return route.fulfill({ status: 204, body: '' });
    };
    await ctx.route('**/*', stopRoute);
  }
  const popups = [];
  const onPage = p => popups.push(p);
  ctx.on('page', onPage);
  try {
    await page.evaluate(prevent => {
      const el = window.__auditClickTarget;
      if (prevent && !window.__auditPreventNav) {
        window.__auditPreventNav = true;
        window.addEventListener('click', e => { if (e.target.closest && e.target.closest('a[href]')) e.preventDefault(); }, true);
      }
      el.scrollIntoView({ block: 'center' });
      el.click();
    }, mode === 'prevent');
  } catch (e) { rec.note = 'page changed during the click: ' + String(e).slice(0, 120); }
  await page.waitForTimeout(st.wait || 4000);
  ctx.off('page', onPage);
  if (stopRoute) await ctx.unroute('**/*', stopRoute);
  if (popups.length) rec.popups = popups.length;
  for (const p of popups) await p.close().catch(() => {});
  rec.url = page.url();
}

function stepLabel(st, i) {
  if (st.goto) return `goto ${st.goto}`;
  if (st.click) return `click ${st.click}${st.text ? ` "${st.text}"` : ''}`;
  if (st.fill) return `fill ${st.fill[0]}`;
  return `step ${i + 1}`;
}

async function runScenario(browser, state, sc, hits, ua) {
  const dir = path.join(opt.out, state);
  fs.mkdirSync(path.join(dir, 'har'), { recursive: true });
  const ctxOpts = { recordHar: { path: path.join(dir, 'har', `${sc.name}.har`), content: 'omit' }, viewport: { width: 1366, height: 900 } };
  if (ua) ctxOpts.userAgent = ua;
  if (state === 'gpc') ctxOpts.extraHTTPHeaders = { 'Sec-GPC': '1' };
  const ctx = await browser.newContext(ctxOpts);
  if (!opt.webdriverVisible) await ctx.addInitScript(() => Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false }));
  if (state === 'gpc') await ctx.addInitScript(() => Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true }));
  if (state === 'blocked') await ctx.route(BLOCK, r => r.abort('blockedbyclient'));

  const run = { scenario: sc.name, step: 'start' };
  const answeredLocally = new WeakSet();
  if (opt.dry) {
    await ctx.route(COLLECT, route => {
      const url = route.request().url();
      // In the blocked state, a blocked host must fail as it would with a blocker, not look sent.
      if (state === 'blocked' && (BLOCK.test(url) || hostBlocked(hostOf(url)))) return route.fallback();
      answeredLocally.add(route.request());
      return route.fulfill({ status: 204, body: '' });
    });
    if (ctx.routeWebSocket) {
      await ctx.routeWebSocket(WS_COLLECT, ws => {
        // Never connected to the server: the page's socket talks to nothing.
        hits.push(hitEntry('WEBSOCKET', ws.url(), { time: new Date().toISOString(), scenario: run.scenario, step: run.step,
          frame: { kind: 'unknown', url: '' }, body: { text: '' } }, 204, true));
      });
    }
  }

  // Record every collection request with the step and frame that caused it.
  const pending = new Map(), tasks = [];
  ctx.on('request', req => {
    if (!COLLECT.test(req.url())) return;
    pending.set(req, { time: new Date().toISOString(), scenario: run.scenario, step: run.step, frame: frameInfo(req), body: bodyOf(req) });
  });
  const finish = async (req, failure) => {
    const m = pending.get(req);
    if (!m) return;
    pending.delete(req);
    // Chromium reports beacons as failed (net::ERR_ABORTED) once their response arrives, so
    // the status comes from the response when there is one, not from the event.
    let status = 0;
    try { const r = await req.response(); status = r ? r.status() : 0; } catch (e) { /* closed */ }
    const local = answeredLocally.has(req);
    if (local) status = 204;
    hits.push(hitEntry(req.method(), req.url(), m, status, local, status > 0 ? undefined : failure));
  };
  ctx.on('requestfinished', req => tasks.push(finish(req)));
  ctx.on('requestfailed', req => tasks.push(finish(req, (req.failure() || {}).errorText || 'failed')));

  const log = { scenario: sc.name, steps: [] };
  const page = await ctx.newPage();
  let bannerDone = false;
  for (const [i, st] of sc.steps.entries()) {
    run.step = st.label || stepLabel(st, i);
    const rec = { label: run.step };
    try {
      if (st.goto) {
        const base = /^https?:/.test(page.url()) ? page.url() : opt.urls[0];
        const target = new URL(st.goto, base).href;
        await page.goto(target, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(st.wait || opt.wait);
        if (!bannerDone && (state === 'accept' || state === 'reject')) {
          bannerDone = true;
          const list = state === 'accept' ? (opt.accept ? [opt.accept] : ACCEPT) : (opt.reject ? [opt.reject] : REJECT);
          rec.banner = await clickFirst(page, list) || 'no banner button found';
          await page.waitForTimeout(2500);
          await page.reload({ waitUntil: 'domcontentloaded' });
          await page.waitForTimeout(opt.wait);
        }
        rec.url = page.url();
        // A landing that ends somewhere else (a JavaScript or HTTP redirect) is worth knowing.
        if (rec.url.split(/[?#]/)[0] !== target.split(/[?#]/)[0]) rec.redirectedFrom = target;
      }
      if (st.click) await runClick(ctx, page, st, rec);
      if (st.fill) { await page.locator(st.fill[0]).first().fill(String(st.fill[1])); await page.waitForTimeout(st.wait || 1000); }
      if (!st.goto && !st.click && !st.fill && st.wait) await page.waitForTimeout(st.wait);
      if (st.inventory) rec.inventory = await runInventory(page);
      if (st.dataLayer) rec.dataLayer = await page.evaluate(DATALAYER_SNAPSHOT).catch(e => ({ error: String(e).slice(0, 200) }));
    } catch (e) { rec.error = String(e).slice(0, 300); }
    log.steps.push(rec);
  }
  run.step = 'end';
  await page.waitForTimeout(1500); // let the last beacons leave
  await Promise.allSettled(tasks);
  await ctx.close(); // flushes the HAR
  await Promise.allSettled(tasks);
  for (const [req, m] of pending) hits.push(hitEntry(req.method(), req.url(), m, 0, answeredLocally.has(req), 'still in flight when the scenario ended'));
  return log;
}

(async () => {
  const baseArgs = opt.webdriverVisible ? [] : ['--disable-blink-features=AutomationControlled'];
  const launch = { headless: !opt.headed, args: baseArgs };
  if (opt.proxy) launch.proxy = { server: opt.proxy };
  const browser = await chromium.launch(launch);
  const ua = opt.webdriverVisible ? null : visitorUserAgent(browser.version());
  const scenarios = [];
  if (opt.urls.length || opt.steps) {
    scenarios.push({ name: 'pages', steps: [...opt.urls.map(u => ({ goto: u, inventory: true, label: u })), ...(opt.steps || [])] });
  }
  for (const sc of opt.scenarios || []) scenarios.push(sc);
  const seen = new Set();
  for (const sc of scenarios) {
    let n = safeName(sc.name), k = 2;
    while (seen.has(n)) n = `${safeName(sc.name)}-${k++}`;
    seen.add(n); sc.name = n;
  }
  if (!opt.dry) console.log('Live mode: every hit reaches the site\'s analytics and ad accounts. Use --dry on live sites.');
  const results = [];
  for (const state of opt.states) {
    let b = browser;
    if (state === 'blocked') {
      const rules = BLOCK_HOSTS.map(h => `MAP ${h} ~NOTFOUND`).join(', ');
      b = await chromium.launch({ ...launch, args: [...baseArgs, `--host-resolver-rules=${rules}`] });
    }
    const dir = path.join(opt.out, state);
    fs.mkdirSync(dir, { recursive: true });
    const hits = [], logs = [];
    try {
      for (const sc of scenarios) {
        if (Array.isArray(sc.states) && !sc.states.includes(state)) continue;
        logs.push(await runScenario(b, state, sc, hits, ua));
      }
      hits.sort((x, y) => String(x.startedDateTime).localeCompare(String(y.startedDateTime)));
      const har = { log: { version: '1.2', creator: { name: 'privacy_matrix.cjs', version: '0.3.0' }, _mode: opt.dry ? 'dry' : 'live', _state: state, entries: hits } };
      fs.writeFileSync(path.join(dir, 'hits.har'), JSON.stringify(har));
      fs.writeFileSync(path.join(dir, 'inventory.json'), JSON.stringify({ state, mode: har.log._mode, startedAt: new Date().toISOString(), scenarios: logs }, null, 2));
      const sent = hits.filter(h => h.response.status > 0);
      const banners = logs.flatMap(l => l.steps.filter(s => s.banner).map(s => s.banner));
      results.push({ state, scenarios: logs.length, hits: hits.length, answeredLocally: hits.filter(h => h._dry).length,
        reachedNetwork: sent.filter(h => !h._dry).length, banner: banners[0] || null, hitsHar: path.join(dir, 'hits.har') });
    } catch (e) { results.push({ state, error: String(e) }); }
    if (b !== browser) await b.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(opt.out, 'summary.json'), JSON.stringify(results, null, 2));
  for (const r of results) {
    if (r.error) { console.log(`${r.state}: ERROR ${r.error}`); continue; }
    const how = opt.dry ? `${r.answeredLocally} answered locally` : `${r.reachedNetwork} reached the network`;
    console.log(`${r.state}: ${r.scenarios} scenarios, ${r.hits} collection requests (${how})${r.banner ? ', banner=' + r.banner : ''} -> ${r.hitsHar}`);
    if (opt.dry && r.reachedNetwork) console.log(`  WARNING: ${r.reachedNetwork} collection requests reached the network in a dry run (entries with "_dry": false and a status above 0).`);
  }
  console.log('Next: python decode_hits.py <state>/hits.har --by-step (what each step sent) and --by-source (which install point sent it).');
})();
