// Run in a pagespeed.web.dev tab with the javascript tool. Edit TARGET (and API_KEY if the user has one).
// This is a top-level-await snippet: the LAST line is the value returned.
const TARGET = 'REPLACE_WITH_POST_URL';
const API_KEY = ''; // optional free Google API key; without one the shared daily quota is often used up (HTTP 429)
const out = {};
for (const strategy of ['mobile', 'desktop']) {
  const api = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=' + encodeURIComponent(TARGET) +
    '&strategy=' + strategy + '&category=PERFORMANCE&category=ACCESSIBILITY&category=BEST_PRACTICES&category=SEO' +
    (API_KEY ? '&key=' + API_KEY : '');
  try {
    const r = await fetch(api);
    if (!r.ok) { out[strategy] = { error: 'HTTP ' + r.status }; continue; }
    const j = await r.json();
    const c = j.lighthouseResult.categories, a = j.lighthouseResult.audits;
    out[strategy] = {
      performance: Math.round(c.performance.score * 100),
      accessibility: Math.round(c.accessibility.score * 100),
      best_practices: Math.round(c['best-practices'].score * 100),
      seo: Math.round(c.seo.score * 100),
      lcp: a['largest-contentful-paint']?.displayValue,
      tbt: a['total-blocking-time']?.displayValue,
      cls: a['cumulative-layout-shift']?.displayValue,
      field_data: j.loadingExperience?.overall_category || 'none yet',
    };
  } catch (e) { out[strategy] = { error: String(e) }; }
}
out
