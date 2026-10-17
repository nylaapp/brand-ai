// page_inventory.js: read-only inventory of the tracking on the current page.
// Paste into the DevTools console or a browser tool's "execute JavaScript" action;
// it evaluates to a promise of one JSON object. Scroll once and wait 3 to 5 s first:
// some sites load tools only after the first scroll or click.
// Reads, never changes: script hosts, vendor globals and IDs (per project for
// Clarity, Hotjar, TikTok), GTM containers, dataLayer events, gtag and consent
// commands, Google consent state, CMP, GPC, Shopify theme and role (a preview is
// not the published theme), pixels, ScriptTags, app blocks and embeds, Customer
// Privacy, cookie NAMES (never values), tracking requests already sent (URL only).
// To list IDs reached by two paths it GETs each GTM container's public gtm.js
// and the page's own HTML (no scripts run; inline code as the server sent it).
// Summary mode (about 1 to 2 KB instead of 5 to 10): run
// `window.PAGE_INVENTORY_MODE = 'summary';` first. Many pages in one tab: run
// `window.PAGE_INVENTORY_KEEP = true;` before the first paste and the script keeps
// itself in window.name; on later pages of the same site run `(0, eval)(window.name)`
// instead of pasting again (paste again if it is gone or eval is blocked; end with
// `window.name = ''`). Undocumented internals (google_tag_data.ics, fbq.getState,
// ttq._i): a missing field means "could not read".
(function pageInventory() {
  try { if (window.PAGE_INVENTORY_KEEP) window.name = '(' + pageInventory.toString() + ')()'; } catch (e) { /* keep going */ }
  return (async () => {
  const MODE = window.PAGE_INVENTORY_MODE === 'summary' ? 'summary' : 'full';
  const out = { url: location.href, host: location.hostname, at: new Date().toISOString(), mode: MODE };
  const safe = (fn, fallback = null) => { try { const v = fn(); return v === undefined ? fallback : v; } catch (e) { return fallback; } };
  const uniq = a => [...new Set(a.filter(Boolean))];
  const GOOGLE_ID = /\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|MC-[A-Z0-9]{6,12}|DC-\d{6,10})\b/g;
  const TIKTOK_CODE = /^C[A-Z0-9]{15,}$/;
  const OBSERVED_APPS = { 683015: 'Judge.me', 4929191: 'ShareASale / Awin', 123074: 'Klaviyo', 3009811: 'Pinterest', 2509311: 'Elevar', 'shopify-pixel': 'Shopify (built-in)' };

  // Every script URL the page has: script tags plus loaded resources (catches scripts removed after loading)
  const scriptSrcs = [...document.scripts].map(s => s.src).filter(Boolean);
  const resourceUrls = safe(() => performance.getEntriesByType('resource').map(e => e.name), []);
  const allUrls = uniq([...scriptSrcs, ...resourceUrls]);
  const idsFrom = re => uniq(allUrls.map(u => { const m = u.match(re); return m && m.slice(1).find(Boolean); }));

  // 1. Script hosts
  const hosts = {};
  for (const src of scriptSrcs) {
    const h = safe(() => new URL(src, location.href).host, 'invalid');
    hosts[h] = (hosts[h] || 0) + 1;
  }
  out.scriptHosts = Object.fromEntries(Object.entries(hosts).sort((a, b) => b[1] - a[1]));
  out.inlineScripts = [...document.scripts].filter(s => !s.src).length;

  // 2. Vendors by global, with IDs per project where the page exposes them
  const ttqKeys = safe(() => Object.keys(window.ttq._i || {}), []);
  const tiktok = uniq([...ttqKeys.filter(k => TIKTOK_CODE.test(k)), ...idsFrom(/analytics\.tiktok\.com\/.*[?&]sdkid=(C[A-Z0-9]+)/)]);
  const clarity = idsFrom(/clarity\.ms\/tag\/([a-z0-9]+)/);
  const hotjar = uniq([String(safe(() => window._hjSettings.hjid) || ''), ...idsFrom(/(?:hotjar|csq)-(\d{5,9})\.js|[?&]hjid=(\d{5,9})/)]);
  const vendors = {
    'Google Tag Manager / gtag': () => window.google_tag_manager && Object.keys(window.google_tag_manager).filter(k => /^(GTM|G|GT|AW|DC)-/.test(k)),
    'Meta pixel': () => window.fbq && (safe(() => window.fbq.getState().pixels.map(p => p.id)) || true),
    'TikTok pixel': () => (window.ttq || tiktok.length) && (tiktok.length ? tiktok : true),
    'TikTok (other ttq keys, not pixel codes)': () => ttqKeys.filter(k => !TIKTOK_CODE.test(k)),
    'Microsoft UET': () => window.uetq && true,
    'Microsoft Clarity': () => (window.clarity || clarity.length) && (clarity.length ? clarity : true),
    'Hotjar': () => (window.hj || hotjar.length) && (hotjar.length ? hotjar : true),
    'Contentsquare': () => (window._uxa || window.CS_CONF) && true,
    'Lucky Orange': () => (window.LO || window.__lo_site_id) && (window.__lo_site_id || true),
    'Pinterest': () => window.pintrk && true,
    'Snapchat': () => window.snaptr && true,
    'Reddit': () => window.rdt && true,
    'LinkedIn Insight': () => window._linkedin_partner_id || (window.lintrk && true),
    'X (Twitter)': () => window.twq && true,
    'Klaviyo': () => (window.klaviyo || window._learnq) && true,
    'Attentive': () => window.__attentive && true,
    'Triple Whale': () => (window.TriplePixel || window.TriplePixelData) && true,
    'Segment': () => window.analytics && window.analytics.initialize && true,
    'Heap': () => window.heap && (window.heap.appid || true),
    'Mixpanel': () => window.mixpanel && true,
    'VWO': () => window._vwo_code && (window._vwo_acc_id || true),
    'Optimizely': () => window.optimizely && true,
    'CallRail': () => (window.CallTrk || window.CallTrkSwap) && true,
    'Intercom': () => window.Intercom && true,
    'Gorgias chat': () => (window.GorgiasChat || window.gorgiasChat) && true,
    'Zendesk': () => window.zE && true,
    'Elevar': () => window.ElevarDataLayer && true,
    'accessiBe (not tracking; third-party script)': () => window.acsbJS && true,
  };
  out.vendors = {};
  for (const [name, test] of Object.entries(vendors)) {
    const v = safe(test);
    if (v && !(Array.isArray(v) && v.length === 0)) out.vendors[name] = v;
  }

  // 3. dataLayer: event names, gtag commands (who they address) and consent commands
  const dl = Array.isArray(window.dataLayer) ? window.dataLayer : [];
  const events = {};
  const consent = [];
  const gtagTargets = {};
  for (const e of dl) {
    if (e && typeof e === 'object' && !Array.isArray(e) && e.event) events[e.event] = (events[e.event] || 0) + 1;
    const arr = e && typeof e === 'object' && e.length !== undefined ? Array.from(e) : null;
    if (!arr) continue;
    if (arr[0] === 'consent') consent.push({ command: arr[1], state: arr[2] });
    if (arr[0] === 'event') events['gtag:' + arr[1]] = (events['gtag:' + arr[1]] || 0) + 1;
    const targets = arr[0] === 'config' ? [arr[1]] : arr[0] === 'event' && arr[2] && arr[2].send_to ? [].concat(arr[2].send_to) : [];
    for (const t of targets) if (typeof t === 'string') (gtagTargets[t] = gtagTargets[t] || []).push(arr[0] === 'config' ? 'config' : 'event:' + arr[1]);
  }
  out.dataLayer = { present: Array.isArray(window.dataLayer), length: dl.length, events, consentCommands: consent,
    gtagTargets: Object.fromEntries(Object.entries(gtagTargets).map(([k, v]) => [k, uniq(v)])) };

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

  // 6. Shopify: theme (role tells a preview from the published theme), pixels, ScriptTags, app blocks, Customer Privacy
  const html = document.documentElement.outerHTML;
  let pixelJson = null;
  if (window.Shopify) {
    const theme = safe(() => window.Shopify.theme && { name: window.Shopify.theme.name, id: window.Shopify.theme.id, role: window.Shopify.theme.role, schema: window.Shopify.theme.schema_name });
    out.shopify = { shop: safe(() => window.Shopify.shop), theme,
      themeIsPreview: theme ? theme.role !== 'main' : 'unknown' };
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
      pixelJson = html.slice(start, end + 1);
      out.shopify.pixels = safe(() => JSON.parse(pixelJson).map(p => {
        const cfg = safe(() => JSON.parse(p.configuration || '{}'), {}) || {};
        const raw = [cfg.pixel_id, cfg.pixelCode, cfg.redditPixelId, cfg.tagID, cfg.accountID].filter(Boolean).map(String);
        const vendor = cfg.google_tag_ids || /google_tag_ids/.test(p.configuration || '') ? 'Google & YouTube app'
          : cfg.pixel_id ? 'Meta app' : cfg.pixelCode ? 'TikTok app' : p.type === 'CUSTOM' ? 'custom pixel'
          : OBSERVED_APPS[p.apiClientId] || 'app ' + p.apiClientId;
        return { vendor, type: p.type, sandbox: p.runtimeContext, app: p.apiClientId, purposes: p.privacyPurposes,
          ids: uniq([...((p.configuration || '').match(GOOGLE_ID) || []), ...raw]) };
      }), 'could not parse');
    }
    // ScriptTags: the asyncLoad URL list Shopify renders (store-wide; they survive theme changes)
    const loader = [...document.scripts].find(s => !s.src && /function asyncLoad\(\)/.test(s.textContent));
    out.shopify.scriptTags = loader ? safe(() => uniq(JSON.parse(loader.textContent.match(/var urls\s*=\s*(\[[\s\S]*?\]);/)[1]).map(u => u.split('?')[0])), 'could not parse') : [];
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
  // App blocks and embeds (Shopify themes mark them with comments; they change with the theme)
  const appBlocks = uniq((html.match(/BEGIN app block: shopify:\/\/apps\/[^/\s]+\/blocks\/[^/\s]+/g) || []).map(s => s.replace('BEGIN app block: shopify://apps/', '').replace('/blocks/', '/')));
  if (out.shopify || appBlocks.length) (out.shopify = out.shopify || {}).appEmbeds = appBlocks;

  // 7. Cookie names by vendor (values are never read out)
  const cookieOwners = [
    [/^_ga($|_)/, 'Google Analytics'], [/^_gcl_/, 'Google Ads'], [/^_gid$/, 'Google Analytics'], [/^FPID|^FPLC|^FPGSID/, 'Google first-party (server-side)'],
    [/^_fbp$|^_fbc$/, 'Meta'], [/^_ttp$|^ttcsid|^_tt_enable_cookie$/, 'TikTok'], [/^_clck$|^_clsk$/, 'Microsoft Clarity'], [/^_uet/, 'Microsoft UET'],
    [/^_hj/, 'Hotjar'], [/^_cs_(c|id|s)$/, 'Contentsquare (incl. Hotjar on Contentsquare)'], [/^_pin_|^_derived_epik/, 'Pinterest'], [/^_scid|^_sctr/, 'Snapchat'], [/^_rdt_/, 'Reddit'],
    [/^__kla_id$/, 'Klaviyo'], [/^_shopify_|^_tracking_consent$|^_cmp_a$|^_landing_page|^_orig_referrer|^_y$|^_s$/, 'Shopify'],
    [/^OptanonConsent|^OptanonAlertBoxClosed/, 'OneTrust'], [/^CookieConsent$/, 'Cookiebot'], [/^calltrk/, 'CallRail'], [/^_vwo|^_vis_opt/, 'VWO'],
  ];
  const cookies = {};
  for (const name of document.cookie.split(';').map(c => c.split('=')[0].trim()).filter(Boolean)) {
    const owner = (cookieOwners.find(([re]) => re.test(name)) || [null, 'other'])[1];
    (cookies[owner] = cookies[owner] || []).push(name);
  }
  out.cookieNames = cookies;

  // 8. Tracking requests already sent (URL only). Order matters: GA4 signals before GA4.
  const endpoints = [
    [/stats\.g\.doubleclick\.net\/g\/collect/, 'GA4 signals (demographics, not an event)'],
    [/\/g\/(s\/)?collect|\/collect\?v=2/, 'GA4'],
    [/googleads\.g\.doubleclick\.net|googleadservices\.com|\/pagead\/|google\.[a-z.]+\/(ccm|rmkt)\/|ad\.doubleclick\.net\/ccm\//, 'Google Ads'],
    [/facebook\.com\/tr/, 'Meta'], [/analytics\.tiktok\.com\/api/, 'TikTok'], [/clarity\.ms\/collect/, 'Clarity'],
    [/bat\.bing\.com\/action/, 'Microsoft UET'], [/ct\.pinterest\.com/, 'Pinterest'], [/tr\.snapchat\.com/, 'Snapchat'],
    [/alb\.reddit\.com/, 'Reddit'], [/\/monorail\/|produce_batch/, 'Shopify'], [/hotjar\.(com|io)|hj\.contentsquare\.net/, 'Hotjar'],
    [/contentsquare\.net/, 'Contentsquare'], [/config-security\.com/, 'Triple Whale'],
  ];
  const hits = [];
  for (const name of resourceUrls) {
    const match = endpoints.find(([re]) => re.test(name));
    if (!match) continue;
    const u = safe(() => new URL(name));
    const q = u ? u.searchParams : new URLSearchParams();
    hits.push({ vendor: match[1], host: u && u.host, en: q.get('en') || q.get('ev') || q.get('event') || null,
      tid: q.get('tid') || q.get('id') || null, gcs: q.get('gcs'), gcd: q.get('gcd'), npa: q.get('npa'), dma: q.get('dma') });
  }
  out.trackingRequests = hits;

  // 9. Same destination reached by more than one path. A GTM container is read from its public gtm.js.
  const paths = {};
  const addPath = (id, path) => { if (id) (paths[id] = paths[id] || new Set()).add(path); };
  for (const p of (out.shopify && Array.isArray(out.shopify.pixels) ? out.shopify.pixels : [])) for (const id of p.ids) addPath(id, `Shopify pixel: ${p.vendor} (${p.sandbox})`);
  const known = uniq([...Object.keys(paths), ...(Array.isArray(out.vendors['Meta pixel']) ? out.vendors['Meta pixel'] : []), ...tiktok,
    ...Object.keys(window.google_tag_manager || {}).filter(k => /^(G|GT|AW|DC)-/.test(k)), ...Object.keys(gtagTargets)]);
  const containers = uniq([...Object.keys(window.google_tag_manager || {}).filter(k => /^GTM-/.test(k)), ...idsFrom(/googletagmanager\.com\/gtm\.js\?id=(GTM-[A-Z0-9]+)/)]);
  out.gtmContainers = {};
  for (const c of containers) {
    const js = await fetch('https://www.googletagmanager.com/gtm.js?id=' + c, { credentials: 'omit' }).then(r => r.text()).catch(e => null);
    if (!js) { out.gtmContainers[c] = 'could not read gtm.js (blocked or offline); use gtm_public_rules.py --ids'; continue; }
    const body = js.slice(Math.max(0, js.indexOf('"resource"')), js.indexOf('"runtime"') > 0 ? js.indexOf('"runtime"') : js.length);
    const inside = uniq([...(body.match(GOOGLE_ID) || []), ...known.filter(id => body.includes(id) || (id.startsWith('AW-') && body.includes(id.slice(3))))]);
    out.gtmContainers[c] = { version: (body.match(/"version"\s*:\s*"(\d+)"/) || [])[1] || null, ids: inside };
    for (const id of inside) addPath(id, `GTM ${c}`);
  }
  // Inline code as the server sent it (a tag manager injects its Custom HTML into the live DOM, so the DOM would double count it)
  const served = await fetch(location.href, { credentials: 'include' }).then(r => r.text()).catch(e => null);
  const inline = (served ? served.match(/<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?<\/script>/gi) || [] : [...document.scripts].filter(s => !s.src).map(s => s.textContent))
    .filter(t => !t.includes('webPixelsConfigList')).join('\n');
  const inlineLabel = served ? 'inline code in the served page (theme, app embed or snippet)' : 'inline code in the live DOM (may include tag-manager code)';
  for (const id of uniq([...(inline.match(GOOGLE_ID) || []), ...known.filter(id => inline.includes(id))])) addPath(id, inlineLabel);
  // gtag commands only count as their own path when no OPEN pixel (which runs in the page and writes them) holds the ID
  const openPixelIds = new Set((out.shopify && Array.isArray(out.shopify.pixels) ? out.shopify.pixels : []).filter(p => p.sandbox === 'OPEN').flatMap(p => p.ids));
  for (const id of Object.keys(gtagTargets)) if (!openPixelIds.has(id)) addPath(id, 'gtag commands in window.dataLayer (site code or a vendor script)');
  out.sameIdTwoPaths = Object.entries(paths).filter(([, s]) => s.size > 1).map(([id, s]) => ({ id, paths: [...s] }));
  out.note = 'Resource timing shows request URLs only, and only from this frame: sandboxed Shopify pixels (STRICT, LAX) and batched or POST hits need a HAR (privacy_matrix.cjs, decode_hits.py). sameIdTwoPaths lists candidates: confirm in a HAR which path actually sends each event.';

  if (MODE === 'summary') {
    const count = {};
    for (const h of hits) { const c = (count[h.vendor] = count[h.vendor] || { n: 0, events: [] }); c.n++; if (h.en && !c.events.includes(h.en)) c.events.push(h.en); }
    const sh = out.shopify;
    return { url: out.url, at: out.at, mode: MODE, vendors: out.vendors, gtmContainers: out.gtmContainers,
      dataLayerEvents: Object.keys(events), gtagTargets: out.dataLayer.gtagTargets,
      consent: { cmp: Object.keys(out.consentTools), gpc: out.gpc, googleDefaultCommands: consent.length,
        google: out.googleConsentState && Object.fromEntries(Object.entries(out.googleConsentState).map(([k, v]) => [k, v.update !== undefined ? v.update : v.default])) },
      shopify: sh && { theme: sh.theme, themeIsPreview: sh.themeIsPreview,
        pixels: Array.isArray(sh.pixels) ? sh.pixels.map(p => `${p.vendor} ${p.sandbox} ${p.ids.join(' ')}`.trim()) : sh.pixels,
        scriptTagHosts: Array.isArray(sh.scriptTags) ? uniq(sh.scriptTags.map(u => safe(() => new URL(u).host))) : sh.scriptTags,
        appEmbeds: sh.appEmbeds,
        privacy: sh.customerPrivacy && typeof sh.customerPrivacy === 'object' ? { region: sh.customerPrivacy.region, analytics: sh.customerPrivacy.analyticsAllowed, marketing: sh.customerPrivacy.marketingAllowed, saleOfData: sh.customerPrivacy.saleOfDataAllowed, choice: sh.customerPrivacy.visitorChoice } : sh.customerPrivacy },
      sameIdTwoPaths: out.sameIdTwoPaths, requests: count,
      cookieOwners: Object.fromEntries(Object.entries(cookies).map(([k, v]) => [k, v.length])) };
  }
  return out;
  })();
})();
