#!/usr/bin/env node
// Summarise `shopify theme check -o json` output, and optionally compare it with a baseline.
// Usage: node theme_check_summary.mjs current.json [baseline.json] > summary.json
// No dependencies. Groups offenses by check and severity, flags the checks that affect page
// speed, and (with a baseline) lists offenses that are new or gone. Paths are made relative to
// the theme folder so runs in different folders compare cleanly.
import { readFileSync } from 'node:fs';

const [cur, base] = process.argv.slice(2);
if (!cur) {
  console.error('usage: node theme_check_summary.mjs current.json [baseline.json]');
  process.exit(1);
}

// Theme Check checks whose offenses slow pages down or shift layout.
const SPEED = new Set([
  'AssetPreload', 'AssetSizeAppBlockCSS', 'AssetSizeAppBlockJavaScript', 'AssetSizeCSS',
  'AssetSizeCSSStylesheetTag', 'AssetSizeJavaScript', 'CdnPreconnect', 'DeprecateBgsizes',
  'DeprecateLazysizes', 'ImgLazyLoading', 'ImgWidthAndHeight', 'LiquidComplexity',
  'LiquidNestingDepth', 'PaginationSize', 'ParserBlockingJavaScript', 'ParserBlockingScript',
  'RemoteAsset', 'StaticStylesheetAndJavascriptTags',
]);
// Checks that mean something is broken, whatever the score.
const BROKEN = new Set([
  'JSONSyntaxError', 'LiquidSyntaxError', 'LiquidHTMLSyntaxError', 'MissingAsset', 'MissingTemplate',
  'MissingRenderSnippetArguments', 'RequiredLayoutThemeObject', 'UnknownFilter', 'UndefinedObject',
  'ValidSchema', 'ValidJSON', 'JSONMissingBlock', 'JSONMissingSection', 'TranslationKeyExists',
  'UnclosedHTMLElement',
]);

const load = (f) => {
  const raw = readFileSync(f, 'utf8');
  const start = raw.indexOf('['); // the CLI may print a banner before the JSON
  return JSON.parse(raw.slice(start));
};
const rel = (p) => {
  const m = p.match(/(?:^|\/)((?:assets|blocks|config|layout|locales|sections|snippets|templates)\/.+)$/);
  return m ? m[1] : p;
};
const flatten = (files) => files.flatMap((f) => (f.offenses || []).map((o) => ({
  file: rel(f.path), check: o.check, severity: o.severity,
  line: (o.start_row ?? 0) + 1, message: o.message,
})));
const key = (o) => `${o.file}|${o.check}|${o.message}`;

const now = flatten(load(cur));
const bySeverity = {};
const byCheck = {};
for (const o of now) {
  bySeverity[o.severity] = (bySeverity[o.severity] || 0) + 1;
  const c = (byCheck[o.check] ||= { check: o.check, severity: o.severity, count: 0, speed: SPEED.has(o.check), broken: BROKEN.has(o.check), files: new Set(), sample: [] });
  c.count++;
  c.files.add(o.file);
  if (c.sample.length < 5) c.sample.push(`${o.file}:${o.line} ${o.message}`);
}
const checks = Object.values(byCheck)
  .map((c) => ({ ...c, files: [...c.files].slice(0, 20), file_count: c.files.size }))
  .sort((a, b) => (b.broken - a.broken) || (b.speed - a.speed) || (b.count - a.count));

const out = {
  total: now.length,
  by_severity: bySeverity,
  speed_offenses: now.filter((o) => SPEED.has(o.check)).length,
  broken_offenses: now.filter((o) => BROKEN.has(o.check)).length,
  checks,
};

if (base) {
  const before = flatten(load(base));
  // Compare as multisets: the same message can appear more than once in a file.
  const count = (xs) => xs.reduce((m, o) => m.set(key(o), (m.get(key(o)) || 0) + 1), new Map());
  const b = count(before), n = count(now);
  const diff = (x, y) => [...x].filter(([k, v]) => v > (y.get(k) || 0)).map(([k, v]) => {
    const [file, check, message] = k.split('|');
    return { file, check, message, extra: v - (y.get(k) || 0) };
  });
  out.baseline_total = before.length;
  out.new_offenses = diff(n, b); // must be empty after a fix pass
  out.fixed_offenses = diff(b, n);
}
console.log(JSON.stringify(out, null, 2));
