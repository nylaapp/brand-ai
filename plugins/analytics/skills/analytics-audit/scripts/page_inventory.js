// page_inventory.js: read-only inventory of the tracking on the current page.
//
// Run it in the page itself: paste into the DevTools console, or pass the file
// contents to a browser tool's "execute JavaScript" action. It evaluates to a
// promise of one JSON object (most browser tools await it; in the console use
// `await` on the result or read the printed object).
//
// It reads, never changes: script hosts, known vendor globals and IDs, GTM
// containers, dataLayer event names and consent commands, Google's current
// consent state, the consent banner / CMP in use, Shopify's pixel list and
// Customer Privacy state, GPC, cookie NAMES (never values) and the tracking
// requests the page has already sent (URL only; POST bodies need a network
// capture, see decode_hits.py).
//
// Internal objects it peeks at (google_tag_data.ics, fbq.getState, ttq._i)
// are undocumented; a missing field means "could not read", not "absent".
(async () => {
  const out = { url: location.href, host: location.hostname, at: new Date().toISOString() };
  const safe = (fn, fallback = null) => { try { const v = fn(); return v === undefined ? fallback : v; } catch (e) { return fallback; } };

  // 1. Script hosts
  const hosts = {};
  for (const s of document.scripts) {
    if (!s.src) continue;
    const h = safe(() => new URL(s.src, location.href).host, 'invalid');
    hosts[h] = (hosts[h] || 0) + 1;
  }
  out.scriptHosts = Object.fromEntries(Object.entries(hosts).sort((a, b) => b[1] - a[1]));
  out.inlineScripts = [...document.scripts].filter(s => !s.src).length;

  // 2. Vendors by global
  const vendors = {
    'Google Tag Manager / gtag': () => window.google_tag_manager && Object.keys(window.google_tag_manager).filter(k => /^(GTM|G|GT|AW|DC)-/.test(k)),
    'Meta pixel': () => window.fbq && (safe(() => window.fbq.getState().pixels.map(p => p.id)) || true),
    'TikTok pixel': () => window.ttq && (safe(() => Object.keys(window.ttq._i || {})) || true),
    'Microsoft UET': () => window.uetq && true,
    'Microsoft Clarity': () => window.clarity && true,
    'Hotjar': () => window.hj && (safe(() => window._hjSettings.hjid) || true),
    'Lucky Orange': () => (window.LO || window.__lo_site_id) && (window.__lo_site_id || true),
    'Pinterest': () => window.pintrk && true,
    'Snapchat': () => window.snaptr && true,
    'Reddit': () => window.rdt && true,
    'LinkedIn Insight': () => window._linkedin_partner_id || (window.lintrk && true),
    'X (Twitter)': () => window.twq && true,
    'Klaviyo': () => (window.klaviyo || window._learnq) && true,
    'Attentive': () => window.__attentive && true,
    'Segment': () => window.analytics && window.analytics.initialize && true,
    'Heap': () => window.heap && (window.heap.appid || true),
    'Mixpanel': () => window.mixpanel && true,
    'VWO': () => window._vwo_code && true,
    'Optimizely': () => window.optimizely && true,
    'CallRail': () => (window.CallTrk || window.CallTrkSwap) && true,
    'Intercom': () => window.Intercom && true,
    'Gorgias chat': () => (window.GorgiasChat || window.gorgiasChat) && true,
    'Zendesk': () => window.zE && true,
    'Elevar': () => window.ElevarDataLayer && true,
  };
  out.vendors = {};
  for (const [name, test] of Object.entries(vendors)) {
    const v = safe(test);
    if (v && !(Array.isArray(v) && v.length === 0)) out.vendors[name] = v;
  }

  // 3. dataLayer: event names and consent commands
  const dl = Array.isArray(window.dataLayer) ? window.dataLayer : [];
  const events = {};
  const consent = [];
  for (const e of dl) {
    if (e && typeof e === 'object' && !Array.isArray(e) && e.event) events[e.event] = (events[e.event] || 0) + 1;
    const arr = e && typeof e === 'object' && e.length !== undefined ? Array.from(e) : null;
    if (arr && arr[0] === 'consent') consent.push({ command: arr[1], state: arr[2] });
    if (arr && arr[0] === 'event') events['gtag:' + arr[1]] = (events['gtag:' + arr[1]] || 0) + 1;
  }
  out.dataLayer = { present: Array.isArray(window.dataLayer), length: dl.length, events, consentCommands: consent };

  // 4. Google's live consent state (internal, undocumented)
  out.googleConsentState = safe(() => {
    const entries = window.google_tag_data.ics.entries;
    const r = {};
    for (const k of Object.keys(entries)) r[k] = { default: entries[k].default, update: entries[k].update };
    return r;
  });

  // 5. Consent banner / CMP and privacy signals
  const cmps = {
    'Shopify banner': () => document.querySelector('#shopify-pc__banner, [id^="shopify-pc__"]') && true,
    'OneTrust': () => window.OneTrust && (window.OptanonActiveGroups || true),
    'Cookiebot': () => window.Cookiebot && (safe(() => window.Cookiebot.consent) || true),
    'Usercentrics': () => (window.UC_UI || window.__ucCmp) && true,
    'Didomi': () => window.Didomi && true,
    'CookieYes': () => (window.getCkyConsent && safe(() => window.getCkyConsent())) || (window.cookieyes && true),
    'Termly': () => window.Termly && true,
    'Complianz': () => window.complianz && true,
    'Pandectes': () => (window.Pandectes || document.querySelector('[class*="pandectes"]')) && true,
    'Consentmo': () => (window.isenseGDPR || document.querySelector('[id*="consentmo"], [class*="isense"]')) && true,
    'IAB TCF API': () => typeof window.__tcfapi === 'function',
    'IAB GPP API': () => typeof window.__gpp === 'function',
  };
  out.consentTools = {};
  for (const [name, test] of Object.entries(cmps)) { const v = safe(test); if (v) out.consentTools[name] = v; }
  out.gpc = safe(() => navigator.globalPrivacyControl, 'not exposed');

  // 6. Shopify: theme, pixel list, Customer Privacy API
  if (window.Shopify) {
    out.shopify = { shop: safe(() => window.Shopify.shop), theme: safe(() => window.Shopify.theme && { name: window.Shopify.theme.name, id: window.Shopify.theme.id, role: window.Shopify.theme.role, schema: window.Shopify.theme.schema_name }) };
    const html = document.documentElement.outerHTML;
    const i = html.indexOf('webPixelsConfigList');
    if (i >= 0) {
      const start = html.indexOf('[', i);
      let depth = 0, inStr = false, esc = false, end = -1;
      for (let k = start; k < html.length; k++) {
        const c = html[k];
        if (inStr) { if (esc) esc = false; else if (c === '\\') esc = true; else if (c === '"') inStr = false; }
        else if (c === '"') inStr = true;
        else if (c === '[') depth++;
        else if (c === ']') { depth--; if (depth === 0) { end = k; break; } }
      }
      out.shopify.pixels = safe(() => JSON.parse(html.slice(start, end + 1)).map(p => ({
        type: p.type, sandbox: p.runtimeContext, app: p.apiClientId, purposes: p.privacyPurposes,
        ids: [...new Set((p.configuration || '').match(/\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|MC-[A-Z0-9]{6,12})\b/g) || [])],
      })), 'could not parse');
    }
    out.shopify.customerPrivacy = await new Promise(resolve => {
      const read = () => {
        const cp = window.Shopify.customerPrivacy;
        if (!cp) return resolve('not loaded');
        resolve({
          region: safe(() => cp.getRegion()),
          bannerRegion: safe(() => cp.shouldShowBanner()),
          saleOfDataRegion: safe(() => cp.saleOfDataRegion()),
          analyticsAllowed: safe(() => cp.analyticsProcessingAllowed()),
          marketingAllowed: safe(() => cp.marketingAllowed()),
          preferencesAllowed: safe(() => cp.preferencesProcessingAllowed()),
          saleOfDataAllowed: safe(() => cp.saleOfDataAllowed()),
          visitorChoice: safe(() => cp.currentVisitorConsent()),
        });
      };
      if (window.Shopify.customerPrivacy) return read();
      if (typeof window.Shopify.loadFeatures !== 'function') return resolve('API not available');
      const timer = setTimeout(() => resolve('timed out loading API'), 4000);
      window.Shopify.loadFeatures([{ name: 'consent-tracking-api', version: '0.1' }], err => { clearTimeout(timer); if (err) resolve('load error'); else read(); });
    });
  }

  // 7. Cookie names by vendor (values are never read out)
  const cookieOwners = [
    [/^_ga($|_)/, 'Google Analytics'], [/^_gcl_/, 'Google Ads'], [/^_gid$/, 'Google Analytics'], [/^FPID|^FPLC/, 'Google first-party (server-side)'],
    [/^_fbp$|^_fbc$/, 'Meta'], [/^_ttp$|^ttcsid/, 'TikTok'], [/^_clck$|^_clsk$/, 'Microsoft Clarity'], [/^_uet/, 'Microsoft UET'],
    [/^_hj/, 'Hotjar'], [/^_pin_|^_derived_epik/, 'Pinterest'], [/^_scid|^_sctr/, 'Snapchat'], [/^_rdt_/, 'Reddit'],
    [/^__kla_id$/, 'Klaviyo'], [/^_shopify_|^_tracking_consent$|^_cmp_a$|^_landing_page|^_orig_referrer|^_y$|^_s$/, 'Shopify'],
    [/^OptanonConsent|^OptanonAlertBoxClosed/, 'OneTrust'], [/^CookieConsent$/, 'Cookiebot'], [/^calltrk/, 'CallRail'], [/^_vwo|^_vis_opt/, 'VWO'],
  ];
  const cookies = {};
  for (const name of document.cookie.split(';').map(c => c.split('=')[0].trim()).filter(Boolean)) {
    const owner = (cookieOwners.find(([re]) => re.test(name)) || [null, 'other'])[1];
    (cookies[owner] = cookies[owner] || []).push(name);
  }
  out.cookieNames = cookies;

  // 8. Tracking requests already sent (URL only)
  const endpoints = [
    [/\/g\/collect|\/collect\?v=2/, 'GA4'], [/googleads\.g\.doubleclick\.net|\/pagead\/|google\.[a-z.]+\/(ccm|rmkt)\//, 'Google Ads'],
    [/facebook\.com\/tr/, 'Meta'], [/analytics\.tiktok\.com\/api/, 'TikTok'], [/clarity\.ms\/collect/, 'Clarity'],
    [/bat\.bing\.com\/action/, 'Microsoft UET'], [/ct\.pinterest\.com/, 'Pinterest'], [/tr\.snapchat\.com/, 'Snapchat'],
    [/alb\.reddit\.com/, 'Reddit'], [/\/monorail\/|produce_batch/, 'Shopify'], [/hotjar\.(com|io)/, 'Hotjar'],
  ];
  const hits = [];
  for (const e of performance.getEntriesByType('resource')) {
    const match = endpoints.find(([re]) => re.test(e.name));
    if (!match) continue;
    const u = safe(() => new URL(e.name));
    const q = u ? u.searchParams : new URLSearchParams();
    hits.push({ vendor: match[1], host: u && u.host, en: q.get('en') || q.get('ev') || q.get('event') || null,
      tid: q.get('tid') || q.get('id') || null, gcs: q.get('gcs'), gcd: q.get('gcd'), npa: q.get('npa'), dma: q.get('dma') });
  }
  out.trackingRequests = hits;
  out.note = 'Resource timing shows request URLs only. Batched GA4 events and POST bodies need a HAR or network capture.';
  return out;
})();
