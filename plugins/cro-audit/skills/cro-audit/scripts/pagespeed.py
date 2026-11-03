#!/usr/bin/env python3
"""Fetch PageSpeed Insights results for a URL, mobile and desktop. Stdlib only.

  pagespeed.py https://example.com/ [--key API_KEY] [--strategy mobile|desktop|both]

Uses the public PageSpeed Insights API. The shared no-key quota is often used up; a free
API key (--key or the PSI_API_KEY environment variable) makes it reliable. Read-only: it only requests
the public report. Prints lab metrics, real-user (field) metrics when Google has them, and
the top opportunities. Exits 2 with a clear message if the network or API is unavailable.
"""
import argparse, json, os, shutil, subprocess, sys, urllib.parse, urllib.request, urllib.error

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

def run(url, strategy, key):
    q = {"url": url, "strategy": strategy, "category": "performance"}
    if key:
        q["key"] = key
    full = API + "?" + urllib.parse.urlencode(q)
    try:
        with urllib.request.urlopen(urllib.request.Request(full), timeout=120) as r:
            return json.load(r)
    except urllib.error.URLError as e:
        # python.org builds on macOS often lack CA certificates; curl uses the system store
        if "CERTIFICATE_VERIFY_FAILED" in str(e) and shutil.which("curl"):
            out = subprocess.run(["curl", "-sS", "--max-time", "120", full], capture_output=True, text=True)
            if out.returncode == 0 and out.stdout.strip():
                return json.loads(out.stdout)
        raise

def lab(lh):
    a = lh["audits"]
    pick = [("LCP", "largest-contentful-paint"), ("TBT", "total-blocking-time"),
            ("CLS", "cumulative-layout-shift"), ("FCP", "first-contentful-paint"),
            ("Speed Index", "speed-index")]
    return [(n, a[k]["displayValue"]) for n, k in pick if k in a and "displayValue" in a[k]]

def field(d):
    m = (d.get("loadingExperience") or {}).get("metrics") or {}
    names = {"LARGEST_CONTENTFUL_PAINT_MS": "LCP (ms)", "INTERACTION_TO_NEXT_PAINT": "INP (ms)",
             "CUMULATIVE_LAYOUT_SHIFT_SCORE": "CLS", "FIRST_CONTENTFUL_PAINT_MS": "FCP (ms)"}
    return [(names[k], v.get("percentile"), v.get("category")) for k, v in m.items() if k in names]

def opps(lh, n=6):
    rows = []
    for a in lh["audits"].values():
        if a.get("details", {}).get("type") == "opportunity" and a.get("score") is not None and a["score"] < 0.9:
            rows.append((a["details"].get("overallSavingsMs", 0), a["title"]))
    return sorted(rows, reverse=True)[:n]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--key", default=os.environ.get("PSI_API_KEY"))
    ap.add_argument("--strategy", default="both", choices=["mobile", "desktop", "both"])
    a = ap.parse_args()
    for s in (["mobile", "desktop"] if a.strategy == "both" else [a.strategy]):
        try:
            d = run(a.url, s, a.key)
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as e:
            print(f"Could not reach PageSpeed Insights ({e}). Try Lighthouse CLI or report speed as not measured.")
            sys.exit(2)
        if "lighthouseResult" not in d:
            msg = (d.get("error") or {}).get("message", "unexpected response")
            print(f"PageSpeed Insights returned an error: {msg}\nIf this is a quota limit, pass --key or set PSI_API_KEY, or use the Lighthouse CLI. Otherwise report speed as not measured.")
            sys.exit(2)
        lh = d["lighthouseResult"]
        score = lh["categories"]["performance"]["score"]
        print(f"\n## {s}: performance score {round(score * 100) if score is not None else 'n/a'} (lab)")
        print("Lab:", "; ".join(f"{n} {v}" for n, v in lab(lh)) or "none")
        f = field(d)
        print("Field (real users):", "; ".join(f"{n} {p} ({c})" for n, p, c in f) if f else "no field data for this URL")
        for ms, t in opps(lh):
            print(f"- {t} (~{ms/1000:.1f}s)")

if __name__ == "__main__":
    main()
