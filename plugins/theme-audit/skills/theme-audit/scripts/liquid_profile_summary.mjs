#!/usr/bin/env node
// Summarise the output of `shopify theme profile --json` (Shopify's Theme Inspector, a Speedscope
// file of how long the server spent running the theme's Liquid code for one page).
// Usage: node liquid_profile_summary.mjs profile.json [--top 12] > summary.json
// No dependencies. Prints JSON: total Liquid time, time per theme file (own time and with
// everything it renders), the slowest repeated pieces, and the most expensive single lines.
// Times are milliseconds. They include the profiler's own overhead, so use them to compare
// files with each other and runs before and after a fix, not as the real server time.
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const file = args.find((a) => !a.startsWith('--'));
const topIdx = args.indexOf('--top');
const TOP = topIdx >= 0 ? Number(args[topIdx + 1]) || 12 : 12;
if (!file) {
  console.error('usage: node liquid_profile_summary.mjs profile.json [--top 12]');
  process.exit(1);
}
const data = JSON.parse(readFileSync(file, 'utf8'));
const frames = data.shared.frames;
const ms = (ns) => Math.round((ns / 1e6) * 10) / 10;

const byFile = new Map(); // file -> { self, inclusive, renders }
const byLine = new Map(); // "file:line name" -> { self, count }
const bySnippet = new Map(); // file -> { total, count } for liquid_template frames (one per render)
const byFilter = new Map(); // filter name -> { self, count }
let total = 0;

const add = (map, key, init) => { let v = map.get(key); if (!v) { v = init(); map.set(key, v); } return v; };

for (const prof of data.profiles) {
  const unitToNs = prof.unit === 'microseconds' ? 1e3 : prof.unit === 'milliseconds' ? 1e6 : prof.unit === 'seconds' ? 1e9 : 1;
  total += (prof.endValue - prof.startValue) * unitToNs;
  const stack = []; // { frame, start, child, file, nested }
  const open = new Map(); // file -> how many renders of it are open right now
  for (const ev of prof.events) {
    const at = ev.at * unitToNs;
    if (ev.type === 'O') {
      const f = frames[ev.frame];
      const parentFile = stack.length ? stack[stack.length - 1].file : null;
      // A file rendered inside itself (a group inside a group) must not count its inner time twice.
      const isRender = f.name === 'liquid_template' && f.file;
      const nested = isRender && (open.get(f.file) || 0) > 0;
      if (isRender) open.set(f.file, (open.get(f.file) || 0) + 1);
      stack.push({ frame: f, start: at, child: 0, file: f.file || parentFile, nested });
    } else {
      const top = stack.pop();
      if (!top) continue;
      const incl = at - top.start;
      const self = Math.max(0, incl - top.child);
      if (stack.length) stack[stack.length - 1].child += incl;
      const f = top.frame;
      if (f.name === 'liquid_template' && f.file) open.set(f.file, open.get(f.file) - 1);
      const fileKey = top.file || '(page structure)';
      const rec = add(byFile, fileKey, () => ({ self: 0, inclusive: 0, renders: 0 }));
      rec.self += self;
      if (f.name === 'liquid_template') {
        rec.renders += 1;
        const s = add(bySnippet, fileKey, () => ({ total: 0, count: 0, max: 0 }));
        s.count += 1;
        if (!top.nested) { rec.inclusive += incl; s.total += incl; s.max = Math.max(s.max, incl); }
      }
      if (f.name.startsWith('filter:')) {
        const fl = add(byFilter, f.name.slice(7), () => ({ self: 0, count: 0 }));
        fl.self += self; fl.count += 1;
      } else if (f.file && f.line) {
        const l = add(byLine, `${f.file}:${f.line}`, () => ({ name: f.name, self: 0, count: 0 }));
        l.self += self; l.count += 1;
      }
    }
  }
}

const kind = (file) => (file.startsWith('sections/') ? 'section' : file.startsWith('snippets/') ? 'snippet'
  : file.startsWith('blocks/') ? 'block' : file.startsWith('templates/') ? 'template'
  : file.startsWith('layout/') ? 'layout' : 'other');

const files = [...byFile].map(([f, v]) => ({
  file: f, kind: kind(f), own_ms: ms(v.self), with_children_ms: ms(v.inclusive), renders: v.renders,
}));
const out = {
  total_liquid_ms: ms(total),
  note: 'Includes the profiler\'s own overhead; compare files with each other and before with after, not with real server time.',
  slowest_files_own_time: files.slice().sort((a, b) => b.own_ms - a.own_ms).slice(0, TOP),
  slowest_files_with_children: files.filter((f) => f.renders > 0 && f.kind !== 'layout' && f.kind !== 'template')
    .sort((a, b) => b.with_children_ms - a.with_children_ms).slice(0, TOP),
  repeated_pieces: [...bySnippet].filter(([, v]) => v.count >= 5)
    .map(([f, v]) => ({ file: f, kind: kind(f), renders: v.count, total_ms: ms(v.total), average_ms: ms(v.total / v.count), slowest_ms: ms(v.max) }))
    .sort((a, b) => b.total_ms - a.total_ms).slice(0, TOP),
  costliest_lines: [...byLine].map(([k, v]) => ({ where: k, tag: v.name, own_ms: ms(v.self), runs: v.count }))
    .sort((a, b) => b.own_ms - a.own_ms).slice(0, TOP),
  costliest_filters: [...byFilter].map(([k, v]) => ({ filter: k, own_ms: ms(v.self), runs: v.count }))
    .sort((a, b) => b.own_ms - a.own_ms).slice(0, 8),
};
console.log(JSON.stringify(out, null, 2));
