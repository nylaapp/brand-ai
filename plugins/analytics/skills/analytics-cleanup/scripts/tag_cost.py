#!/usr/bin/env python3
"""Measure what tags cost a page, the zero-based way, with the Lighthouse CLI.

Runs Lighthouse (performance only) several times per configuration and takes
the median, because single runs vary:

  all-on    the page as visitors get it
  all-off   every tag group blocked (the zero baseline)
  +GROUP    all-off plus one group allowed back   (--mode addback, default)
  -GROUP    all-on minus one group                 (--mode removal)

Tags are blocked in the browser, not removed from the site, so nothing on the
store changes and store-wide installs (Shopify app pixels, GTM) can be
benchmarked on a preview or the live URL alike. Groups are blocked with
Lighthouse URL patterns: each host becomes `*://host/*`, and a group can add
path patterns (useful for first-party or server-side endpoints).

Usage:
  python tag_cost.py https://store.example.com/ --runs 5 --out cost.md
  python tag_cost.py URL --groups my-groups.json --mode removal
  python tag_cost.py URL --only google,meta,heatmaps --runs 3
  python tag_cost.py URL --list-groups

my-groups.json: {"server-side GA4": {"patterns": ["*data.example.com/g/collect*"], "hosts": []}}
Custom groups are added to the built-in ones (same name replaces).

Needs Node (npx downloads Lighthouse on first use) and Chrome. Lab numbers on
one machine: compare configurations with each other, not with field data.
Lab has no INP; Total Blocking Time and main-thread time are the proxies.
"""
import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile

GROUPS = {
    "google": {"hosts": ["www.googletagmanager.com", "googletagmanager.com", "www.google-analytics.com", "analytics.google.com",
                         "stats.g.doubleclick.net", "googleads.g.doubleclick.net", "ad.doubleclick.net", "www.googleadservices.com",
                         "td.doubleclick.net"],
               "patterns": ["*/g/collect*", "*/gtag/js*", "*/gtm.js*"]},
    "meta": {"hosts": ["connect.facebook.net"], "patterns": ["*facebook.com/tr*"]},
    "tiktok": {"hosts": ["analytics.tiktok.com"], "patterns": []},
    "microsoft": {"hosts": ["bat.bing.com", "www.clarity.ms", "scripts.clarity.ms", "c.clarity.ms", "u.clarity.ms", "q.clarity.ms"], "patterns": []},
    "heatmaps": {"hosts": ["static.hotjar.com", "script.hotjar.com", "vars.hotjar.com", "tools.luckyorange.com", "script.crazyegg.com"],
                 "patterns": ["*hotjar*", "*luckyorange*", "*crazyegg*"]},
    "pinterest": {"hosts": ["s.pinimg.com", "ct.pinterest.com"], "patterns": []},
    "snap": {"hosts": ["sc-static.net", "tr.snapchat.com"], "patterns": []},
    "reddit": {"hosts": ["www.redditstatic.com", "alb.reddit.com"], "patterns": []},
    "klaviyo": {"hosts": ["static.klaviyo.com", "static-tracking.klaviyo.com", "a.klaviyo.com", "fast.a.klaviyo.com"], "patterns": []},
    "attentive": {"hosts": ["cdn.attn.tv", "events.attentivemobile.com"], "patterns": []},
    "callrail": {"hosts": ["cdn.callrail.com", "js.callrail.com"], "patterns": []},
    "ab-testing": {"hosts": ["dev.visualwebsiteoptimizer.com", "cdn.optimizely.com", "logx.optimizely.com"], "patterns": []},
    "chat": {"hosts": ["config.gorgias.chat", "client-builder.production.gorgias.io", "widget.intercom.io", "js.intercomcdn.com",
                       "static.zdassets.com", "ekr.zdassets.com"], "patterns": []},
    "reviews": {"hosts": ["cdn.judge.me", "cache.judge.me", "staticw2.yotpo.com", "cdn-widgetsrepository.yotpo.com", "cdn.okendo.io",
                          "cdn1.stamped.io"], "patterns": []},
    "affiliate": {"hosts": ["static.shareasale.com", "www.dwin1.com", "d.impactradius-event.com"], "patterns": []},
    "adroll": {"hosts": ["s.adroll.com", "d.adroll.com", "assets1.adroll.com"], "patterns": []},
    "shopify-pixels": {"hosts": [], "patterns": ["*/wpm@*", "*web-pixels-manager*", "*/web-pixel-*"]},
}


def lighthouse(url, block_patterns, block_hosts, outdir, tag, form_factor):
    path = os.path.join(outdir, f"{tag}.json")
    patterns = list(block_patterns) + [f"*://{h}/*" for h in sorted(set(block_hosts))]
    cmd = ["npx", "--yes", "lighthouse", url, "--only-categories=performance", "--output=json",
           f"--output-path={path}", "--quiet", "--chrome-flags=--headless=new"]
    if form_factor == "desktop":
        cmd.append("--preset=desktop")
    for p in patterns:
        cmd.append(f"--blocked-url-patterns={p}")
    res = subprocess.run(cmd, capture_output=True, text=True, shell=(os.name == "nt"))
    if res.returncode != 0 or not os.path.exists(path):
        raise RuntimeError(f"lighthouse failed for {tag}: {res.stderr[-500:]}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def metrics(lhr):
    a = lhr["audits"]
    num = lambda k: (a.get(k) or {}).get("numericValue")
    reqs = len(((a.get("network-requests") or {}).get("details") or {}).get("items", []))
    third = []
    # Lighthouse 12 and earlier: "third-party-summary"; Lighthouse 13: "third-parties-insight"
    tp = a.get("third-party-summary") or a.get("third-parties-insight") or {}
    for it in (tp.get("details") or {}).get("items", []):
        ent = it.get("entity")
        name = ent.get("text") if isinstance(ent, dict) else ent
        third.append({"entity": name, "transfer_kb": (it.get("transferSize") or 0) / 1024,
                      "main_thread_ms": it.get("mainThreadTime") or 0, "blocking_ms": it.get("blockingTime") or 0})
    return {"score": (lhr["categories"]["performance"].get("score") or 0) * 100, "lcp_ms": num("largest-contentful-paint"),
            "tbt_ms": num("total-blocking-time"), "cls": num("cumulative-layout-shift"), "fcp_ms": num("first-contentful-paint"),
            "main_thread_ms": num("mainthread-work-breakdown"), "bytes_kb": (num("total-byte-weight") or 0) / 1024,
            "requests": reqs, "third_party": third}


def median_of(runs):
    keys = ["score", "lcp_ms", "tbt_ms", "cls", "fcp_ms", "main_thread_ms", "bytes_kb", "requests"]
    out = {}
    for k in keys:
        vals = [r[k] for r in runs if r.get(k) is not None]
        out[k] = statistics.median(vals) if vals else None
    return out


def fmt(v, nd=0):
    return "-" if v is None else (f"{v:.{nd}f}" if nd else f"{v:,.0f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?")
    ap.add_argument("--runs", type=int, default=5, help="Lighthouse runs per configuration (median; default 5)")
    ap.add_argument("--mode", choices=["addback", "removal"], default="addback")
    ap.add_argument("--groups", help="JSON file with extra or replacement groups")
    ap.add_argument("--only", help="comma-separated group names to test (default: all groups)")
    ap.add_argument("--form-factor", choices=["mobile", "desktop"], default="mobile")
    ap.add_argument("--out", help="write the markdown report here")
    ap.add_argument("--keep", help="folder to keep raw Lighthouse JSON (default: temp folder)")
    ap.add_argument("--list-groups", action="store_true")
    a = ap.parse_args()
    groups = dict(GROUPS)
    if a.groups:
        with open(a.groups, encoding="utf-8") as fh:
            for name, g in json.load(fh).items():
                groups[name] = {"hosts": g.get("hosts", []), "patterns": g.get("patterns", [])}
    if a.list_groups:
        for name, g in groups.items():
            print(f"{name}: hosts={', '.join(g['hosts']) or '-'}; patterns={', '.join(g['patterns']) or '-'}")
        return
    if not a.url:
        ap.error("give a URL")
    names = [n.strip() for n in a.only.split(",")] if a.only else list(groups)
    unknown = [n for n in names if n not in groups]
    if unknown:
        ap.error(f"unknown groups: {', '.join(unknown)} (see --list-groups)")
    outdir = a.keep or tempfile.mkdtemp(prefix="tagcost-")
    os.makedirs(outdir, exist_ok=True)
    all_p = [p for n in names for p in groups[n]["patterns"]]
    all_h = [h for n in names for h in groups[n]["hosts"]]

    configs = [("all-on", [], []), ("all-off", all_p, all_h)]
    for n in names:
        if a.mode == "addback":
            configs.append((f"+{n}", [p for m in names if m != n for p in groups[m]["patterns"]],
                            [h for m in names if m != n for h in groups[m]["hosts"] if h not in groups[n]["hosts"]]))
        else:
            configs.append((f"-{n}", groups[n]["patterns"], groups[n]["hosts"]))

    results, third = {}, {}
    for label, pats, hosts in configs:
        runs = []
        for i in range(a.runs):
            print(f"{label} run {i + 1}/{a.runs}", file=sys.stderr)
            safe_label = label.replace("+", "plus-").replace("-", "minus-", 1) if label[0] in "+-" else label
            lhr = lighthouse(a.url, pats, hosts, outdir, f"{safe_label}-{i + 1}", a.form_factor)
            m = metrics(lhr)
            runs.append(m)
            if label == "all-on":
                for t in m["third_party"]:
                    third.setdefault(t["entity"], []).append(t)
        results[label] = median_of(runs)

    base = results["all-off" if a.mode == "addback" else "all-on"]
    lines = [f"# Tag cost: {a.url}", "",
             f"Lighthouse performance, {a.form_factor}, median of {a.runs} runs per row, mode {a.mode}. Raw reports: `{outdir}`.", "",
             "| Configuration | Score | LCP ms | TBT ms | Main thread ms | KB | Requests | TBT vs " + ("all-off" if a.mode == "addback" else "all-on") + " |",
             "|---|---|---|---|---|---|---|---|"]
    for label, _, _ in configs:
        r = results[label]
        delta = None if r["tbt_ms"] is None or base["tbt_ms"] is None else r["tbt_ms"] - base["tbt_ms"]
        lines.append(f"| {label} | {fmt(r['score'])} | {fmt(r['lcp_ms'])} | {fmt(r['tbt_ms'])} | {fmt(r['main_thread_ms'])} | {fmt(r['bytes_kb'])} | {fmt(r['requests'])} | {('+' if delta and delta > 0 else '') + fmt(delta) if delta is not None else '-'} |")
    lines += ["", "## Third parties on the full page (Lighthouse third-party summary, median)", "",
              "| Entity | KB | Main thread ms | Blocking ms |", "|---|---|---|---|"]
    rows = []
    for ent, items in third.items():
        rows.append((ent, statistics.median(i["transfer_kb"] for i in items), statistics.median(i["main_thread_ms"] for i in items),
                     statistics.median(i["blocking_ms"] for i in items)))
    for ent, kb, mt, bl in sorted(rows, key=lambda r: -r[2]):
        lines.append(f"| {ent} | {kb:,.0f} | {mt:,.0f} | {bl:,.0f} |")
    lines += ["", "Lab data from one machine and network. Use it to rank tags against each other; confirm real-user impact with field data (CrUX / PageSpeed Insights) after changes ship."]
    text = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
