#!/usr/bin/env node
// Summarise one or more Lighthouse JSON reports of the SAME page and form factor.
// Usage: node lh_summary.mjs run1.json [run2.json ...] > summary.json
// No dependencies. Prints JSON: median category scores (0-100), the spread of the performance
// score, median core metrics, and every failing audit with its elements, taken from the run whose
// performance score is the median (or the first run when performance wasn't scored).
import { readFileSync } from 'node:fs';

const files = process.argv.slice(2);
if (!files.length) {
  console.error('usage: node lh_summary.mjs run1.json [run2.json ...]');
  process.exit(1);
}
const runs = files.map((f) => JSON.parse(readFileSync(f, 'utf8')));

const median = (xs) => {
  const v = xs.filter((x) => typeof x === 'number').sort((a, b) => a - b);
  if (!v.length) return null;
  const m = Math.floor(v.length / 2);
  return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2;
};
const pct = (s) => (typeof s === 'number' ? Math.round(s * 100) : null);
// Every category the report has: performance, accessibility, best-practices and seo, plus any newer
// ones (Lighthouse 13.6 adds 'agentic-browsing').
const CATS = [...new Set(runs.flatMap((r) => Object.keys(r.categories || {})))];
const METRICS = {
  lcp_ms: 'largest-contentful-paint',
  fcp_ms: 'first-contentful-paint',
  tbt_ms: 'total-blocking-time',
  cls: 'cumulative-layout-shift',
  speed_index_ms: 'speed-index',
  total_bytes: 'total-byte-weight',
};

// Representative run: median performance score, so its findings match the reported number.
const perfScores = runs.map((r) => r.categories?.performance?.score ?? null);
let rep = runs[0];
if (perfScores.every((s) => typeof s === 'number')) {
  const order = runs.map((r, i) => i).sort((a, b) => perfScores[a] - perfScores[b]);
  rep = runs[order[Math.floor((order.length - 1) / 2)]];
}

const SKIP_MODES = new Set(['notApplicable', 'manual', 'informative', 'error']);
const trimItem = (it) => {
  const out = {};
  const node = it.node || (it.type === 'node' ? it : null);
  if (node) {
    out.selector = node.selector;
    out.label = node.nodeLabel;
    out.snippet = node.snippet;
    if (node.explanation) out.explanation = node.explanation;
  }
  if (!node && it.subpart) { out.part = it.label || it.subpart; out.ms = Math.round(it.duration || 0); }
  for (const k of ['url', 'entity', 'wastedBytes', 'wastedMs', 'totalBytes', 'transferSize', 'blockingTime', 'mainThreadTime', 'score', 'source', 'description']) {
    if (it[k] !== undefined && typeof it[k] !== 'object') out[k] = it[k];
    else if (k === 'entity' && it.entity?.text) out.entity = it.entity.text;
    else if (k === 'source' && it.source?.url) out.source = `${it.source.url}:${it.source.line ?? ''}`;
  }
  return out;
};
const itemsOf = (audit) => {
  const d = audit.details || {};
  let items = d.items || [];
  // some audits (Lighthouse 12+ insights) nest tables, nodes and checklists inside a list
  if (d.type === 'list') {
    items = items.flatMap((x) => {
      if (x.type === 'node') return [x];
      if (x.type === 'checklist') return Object.values(x.items || {}).filter((c) => c.value === false).map((c) => ({ description: `not met: ${c.label}` }));
      return Array.isArray(x.items) ? x.items : [];
    });
  }
  return items.slice(0, 10).map(trimItem);
};

const failing = {};
for (const cat of CATS) {
  const c = rep.categories?.[cat];
  if (!c) continue;
  const list = [];
  for (const ref of c.auditRefs) {
    const a = rep.audits[ref.id];
    if (!a || SKIP_MODES.has(a.scoreDisplayMode) || a.score === null) continue;
    if (cat === 'performance') {
      if (ref.group === 'metrics') continue; // reported under metrics
      const savings = a.metricSavings || {};
      const hasSavings = Object.values(savings).some((v) => v > 0);
      if (a.score >= 0.9 && !hasSavings) continue;
      list.push({
        id: a.id, title: a.title, score: a.score, group: ref.group || null,
        display: a.displayValue || null, metric_savings: a.metricSavings || null,
        items: itemsOf(a),
      });
    } else {
      if (ref.weight <= 0 || a.score >= 1) continue;
      list.push({ id: a.id, title: a.title, score: a.score, weight: ref.weight, items: itemsOf(a) });
    }
  }
  if (cat === 'performance') {
    list.sort((x, y) => (Math.max(0, ...Object.values(y.metric_savings || {})) - Math.max(0, ...Object.values(x.metric_savings || {}))));
  } else {
    list.sort((x, y) => y.weight - x.weight);
  }
  failing[cat] = list;
}

// Third-party cost, for naming who owns a speed problem (theme vs app vs outside script).
// Lighthouse 13 calls it third-parties-insight; older versions third-party-summary.
const tpAudit = rep.audits['third-parties-insight'] || rep.audits['third-party-summary'];
const tp = (tpAudit?.details?.items || [])
  .slice()
  .sort((a, b) => (b.mainThreadTime || 0) - (a.mainThreadTime || 0) || (b.transferSize || 0) - (a.transferSize || 0));
const third_party = tp.slice(0, 15).map((x) => ({
  entity: typeof x.entity === 'string' ? x.entity : x.entity?.text,
  transfer_kb: Math.round((x.transferSize || 0) / 1024),
  blocking_ms: x.blockingTime === undefined ? null : Math.round(x.blockingTime),
  main_thread_ms: Math.round(x.mainThreadTime || 0),
  urls: (x.subItems?.items || []).slice(0, 5).map((s) => s.url),
}));

// The main-content (LCP) element: in an insight (Lighthouse 12+) or the older element audit.
const findNode = (audit) => {
  const walk = (x) => {
    if (!x || typeof x !== 'object') return null;
    if (x.type === 'node' && x.selector) return x;
    if (x.node?.selector) return x.node;
    for (const v of Array.isArray(x) ? x : Object.values(x)) { const n = walk(v); if (n) return n; }
    return null;
  };
  return walk(audit?.details);
};
const lcpNode = ['lcp-breakdown-insight', 'lcp-discovery-insight', 'largest-contentful-paint-element']
  .map((id) => findNode(rep.audits[id])).find(Boolean) || null;
const lcpParts = (rep.audits['lcp-breakdown-insight']?.details?.items || [])
  .flatMap((x) => (x.type === 'table' ? x.items : []))
  .map((p) => ({ part: p.label || p.subpart, ms: Math.round(p.duration || 0) }));

const out = {
  url: rep.finalDisplayedUrl || rep.finalUrl || rep.requestedUrl,
  form_factor: rep.configSettings?.formFactor,
  lighthouse: rep.lighthouseVersion,
  runs: runs.length,
  scores: Object.fromEntries(CATS.map((c) => [c, median(runs.map((r) => pct(r.categories?.[c]?.score)))])),
  performance_spread: perfScores.every((s) => typeof s === 'number')
    ? { min: pct(Math.min(...perfScores)), max: pct(Math.max(...perfScores)) } : null,
  metrics: Object.fromEntries(Object.entries(METRICS).map(([k, id]) => {
    const m = median(runs.map((r) => r.audits?.[id]?.numericValue));
    return [k, m === null ? null : (k === 'cls' ? Math.round(m * 1000) / 1000 : Math.round(m))];
  })),
  lcp_element: lcpNode ? { selector: lcpNode.selector, label: lcpNode.nodeLabel, snippet: lcpNode.snippet } : null,
  lcp_breakdown: lcpParts,
  third_party,
  failing,
  run_warnings: rep.runWarnings || [],
};
console.log(JSON.stringify(out, null, 2));
