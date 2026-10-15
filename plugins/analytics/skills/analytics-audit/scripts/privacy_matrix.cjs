#!/usr/bin/env node
// privacy_matrix.cjs: visit pages in several privacy states and record what tracking fires.
//
// For each state it opens a fresh browser profile, applies the state, walks the
// pages (and optional journey steps), then saves a HAR (every request, with POST
// bodies) and the page_inventory.js result. Decode the HARs with decode_hits.py.
//
// States:
//   fresh    first visit, no banner interaction
//   accept   click the banner's accept button, then continue
//   reject   click the banner's reject button, then continue
//   gpc      Global Privacy Control on (Sec-GPC header + navigator.globalPrivacyControl)
//   blocked  common tracker domains blocked, like an ad blocker
//
// Usage (Playwright must be installed where Node can find it, e.g. `npm i playwright`
// in a scratch folder, or NODE_PATH pointing at a node_modules that has it):
//   node privacy_matrix.cjs --url https://store.example.com/ --out ./matrix
//   node privacy_matrix.cjs --url https://a/ --url https://a/products/x --states fresh,accept,reject,gpc
//   node privacy_matrix.cjs --url https://a/ --accept "#my-accept" --reject "#my-reject"
//   node privacy_matrix.cjs --url https://a/ --steps journey.json --proxy http://eu-proxy:8080
//
// journey.json: [{"goto": "/products/x"}, {"click": "button[name=add]"}, {"wait": 2000}, {"goto": "/cart"}]
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
  else if (a === '--proxy') { opt.proxy = v; i++; }
  else if (a === '--wait') { opt.wait = Number(v); i++; }
  else if (a === '--headed') { opt.headed = true; }
}
if (!opt.urls.length) { console.error('Give at least one --url'); process.exit(2); }

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

const inventory = fs.readFileSync(path.join(__dirname, 'page_inventory.js'), 'utf8');

async function clickFirst(page, selectors) {
  for (const sel of selectors) {
    try {
      const el = page.locator(sel).first();
      if (await el.isVisible({ timeout: 800 })) { await el.click({ timeout: 2000 }); return sel; }
    } catch (e) { /* try next */ }
  }
  return null;
}

async function runState(browser, state) {
  const dir = path.join(opt.out, state);
  fs.mkdirSync(dir, { recursive: true });
  const ctxOpts = { recordHar: { path: path.join(dir, 'capture.har'), content: 'omit' }, viewport: { width: 1366, height: 900 } };
  if (state === 'gpc') ctxOpts.extraHTTPHeaders = { 'Sec-GPC': '1' };
  const context = await browser.newContext(ctxOpts);
  if (state === 'gpc') await context.addInitScript(() => Object.defineProperty(Navigator.prototype, 'globalPrivacyControl', { get: () => true }));
  if (state === 'blocked') await context.route(BLOCK, r => r.abort());
  const page = await context.newPage();
  const log = { state, startedAt: new Date().toISOString(), pages: [], banner: null };
  for (const [i, url] of opt.urls.entries()) {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(opt.wait);
    if (i === 0 && (state === 'accept' || state === 'reject')) {
      const list = state === 'accept' ? (opt.accept ? [opt.accept] : ACCEPT) : (opt.reject ? [opt.reject] : REJECT);
      log.banner = await clickFirst(page, list) || 'no banner button found';
      await page.waitForTimeout(2500);
      await page.reload({ waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(opt.wait);
    }
    const inv = await page.evaluate(inventory).catch(e => ({ error: String(e) }));
    log.pages.push({ url, inventory: inv });
  }
  for (const step of opt.steps || []) {
    if (step.goto) await page.goto(new URL(step.goto, opt.urls[0]).href, { waitUntil: 'domcontentloaded' });
    if (step.click) await page.locator(step.click).first().click({ timeout: 5000 }).catch(e => log.pages.push({ step, error: String(e) }));
    if (step.fill) await page.locator(step.fill[0]).fill(step.fill[1]).catch(() => {});
    await page.waitForTimeout(step.wait || 2500);
    if (step.inventory) log.pages.push({ step, inventory: await page.evaluate(inventory).catch(e => ({ error: String(e) })) });
  }
  await context.close(); // flushes the HAR
  fs.writeFileSync(path.join(dir, 'inventory.json'), JSON.stringify(log, null, 2));
  return { state, banner: log.banner, har: path.join(dir, 'capture.har') };
}

(async () => {
  const launch = { headless: !opt.headed };
  if (opt.proxy) launch.proxy = { server: opt.proxy };
  const browser = await chromium.launch(launch);
  const results = [];
  for (const s of opt.states) {
    let b = browser;
    if (s === 'blocked') {
      const rules = BLOCK_HOSTS.map(h => `MAP ${h} ~NOTFOUND`).join(', ');
      b = await chromium.launch({ ...launch, args: [`--host-resolver-rules=${rules}`] });
    }
    try { results.push(await runState(b, s)); }
    catch (e) { results.push({ state: s, error: String(e) }); }
    if (b !== browser) await b.close();
  }
  await browser.close();
  fs.writeFileSync(path.join(opt.out, 'summary.json'), JSON.stringify(results, null, 2));
  for (const r of results) console.log(`${r.state}: ${r.error ? 'ERROR ' + r.error : 'banner=' + (r.banner || 'n/a') + '  har=' + r.har}`);
  console.log('Next: python decode_hits.py <state>/capture.har for each state.');
})();
