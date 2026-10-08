#!/usr/bin/env python3
"""Turn Google Search Console CSV exports into blog-opportunity signals.

Usage:
  python gsc_signals.py --dir inputs/gsc [--existing existing-articles.json]
      [--min-impressions 100] [--decay-pct 25] [--max-age-days 35] [--today YYYY-MM-DD]

Expects the standard Performance export (Search results → Export → CSV / Google Sheets):
  Queries.csv : Top queries, Clicks, Impressions, CTR, Position
  Pages.csv   : Top pages, Clicks, Impressions, CTR, Position
A "Compare" export (e.g. last 28 days vs previous 28 days) adds prefixed columns such as
"Last 28 days Clicks" / "Previous 28 days Clicks"; that's what the decay check needs.
Other file names work as long as the first column header contains "quer" or "page".

Outputs JSON with:
  striking_distance : queries ranking 8–20 with enough impressions (new post, or optimize a matching one)
  ctr_gap           : queries ranking top 5 with CTR < 2% (title/meta refresh of the matching post)
  decay             : blog pages whose clicks dropped by ≥ decay-pct (refresh)
  stale_files       : exports older than max-age-days (ignored; ask the user for a fresh export)
"""
import argparse
import csv
import datetime as dt
import glob
import json
import os
import re

STOP = set("a an the and or for of to in on with your my our how what which why best vs is are do does can at by from guide".split())


def toks(s):
    out = set()
    for w in re.findall(r"[a-z0-9]+", (s or "").lower().replace("-", " ")):
        if w in STOP:
            continue
        if len(w) > 3 and w.endswith("s") and not w.endswith("ss"):
            w = w[:-1]
        out.add(w)
    return out


def num(v):
    v = (v or "").strip().replace(",", "").replace("%", "")
    try:
        return float(v)
    except ValueError:
        return 0.0


def split_cols(header):
    """Return {prefix: {metric: col}} where prefix '' is a non-compare export."""
    groups = {}
    for col in header[1:]:
        m = re.match(r"^(.*?)(Clicks|Impressions|CTR|Position)$", col.strip(), re.I)
        if not m:
            continue
        prefix = m.group(1).strip()
        groups.setdefault(prefix, {})[m.group(2).lower()] = col
    return groups


def pick_periods(groups):
    if "" in groups:
        return groups[""], None
    keys = list(groups)
    cur = next((k for k in keys if re.search(r"last|current|this", k, re.I)), keys[0] if keys else None)
    prev = next((k for k in keys if re.search(r"previous|prior|last year", k, re.I) and k != cur), None)
    if prev is None and len(keys) > 1:
        prev = [k for k in keys if k != cur][0]
    return groups.get(cur, {}), groups.get(prev) if prev else None


def match_article(q, existing):
    qt = toks(q)
    best, best_j = None, 0
    for a in existing:
        tt, ht = toks(a.get("title", "")), toks(a.get("handle", ""))
        if not qt or not (tt or ht):
            continue
        j = len(qt & tt) / len(qt | tt) if tt else 0
        if ht and qt <= ht:
            j = max(j, 0.99)
        if j > best_j:
            best, best_j = a, j
    return (best.get("handle"), round(best_j, 2)) if best and best_j >= 0.67 else (None, round(best_j, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--existing", default=None)
    ap.add_argument("--min-impressions", type=float, default=100)
    ap.add_argument("--decay-pct", type=float, default=25)
    ap.add_argument("--max-age-days", type=int, default=35)
    ap.add_argument("--today", default=dt.date.today().isoformat())
    a = ap.parse_args()
    today = dt.date.fromisoformat(a.today)
    existing = []
    if a.existing and os.path.exists(a.existing):
        existing = json.load(open(a.existing))

    res = {"striking_distance": [], "ctr_gap": [], "decay": [], "stale_files": [], "files_read": []}
    for path in sorted(glob.glob(os.path.join(a.dir, "**", "*.csv"), recursive=True)):
        # Export date: a YYYY-MM-DD in the file or folder name wins (GSC zips are named
        # "<site>-Performance-on-Search-YYYY-MM-DD"); otherwise fall back to file mtime.
        m = re.findall(r"(20\d\d-\d\d-\d\d)", os.path.relpath(path, a.dir))
        exported = dt.date.fromisoformat(m[-1]) if m else dt.date.fromtimestamp(os.path.getmtime(path))
        age = (today - exported).days
        if age > a.max_age_days:
            res["stale_files"].append({"file": path, "age_days": age})
            continue
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.reader(f))
        if not rows:
            continue
        header = rows[0]
        kind = "query" if "quer" in header[0].lower() else "page" if "page" in header[0].lower() else None
        if not kind:
            continue
        cur, prev = pick_periods(split_cols(header))
        idx = {h: i for i, h in enumerate(header)}
        res["files_read"].append({"file": path, "kind": kind, "compare": prev is not None, "rows": len(rows) - 1})
        for r in rows[1:]:
            if not r:
                continue
            key = r[0]
            g = lambda col: num(r[idx[col]]) if col and col in idx and idx[col] < len(r) else 0.0
            clicks, imp = g(cur.get("clicks")), g(cur.get("impressions"))
            ctr, pos = g(cur.get("ctr")), g(cur.get("position"))
            if kind == "query":
                handle, sim = match_article(key, existing)
                if 8 <= pos <= 20 and imp >= a.min_impressions:
                    res["striking_distance"].append({"query": key, "impressions": imp, "clicks": clicks,
                                                     "position": pos, "matching_article": handle, "similarity": sim,
                                                     "suggested_action": "refresh" if handle else "new"})
                elif 0 < pos <= 5 and imp >= a.min_impressions and ctr < 2:
                    res["ctr_gap"].append({"query": key, "impressions": imp, "ctr_pct": ctr, "position": pos,
                                           "matching_article": handle, "suggested_action": "refresh (title/meta)"})
            elif kind == "page" and prev and "/blogs/" in key:
                pc = g(prev.get("clicks"))
                if pc >= 10:
                    drop = (pc - clicks) / pc * 100
                    if drop >= a.decay_pct:
                        res["decay"].append({"page": key, "clicks_now": clicks, "clicks_before": pc,
                                             "drop_pct": round(drop, 1),
                                             "position_now": pos, "position_before": g(prev.get("position")),
                                             "suggested_action": "refresh"})
    res["striking_distance"].sort(key=lambda x: -x["impressions"])
    res["decay"].sort(key=lambda x: -x["drop_pct"])
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
