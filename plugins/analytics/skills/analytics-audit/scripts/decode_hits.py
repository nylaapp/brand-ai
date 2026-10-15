#!/usr/bin/env python3
"""Decode the tracking hits in a network capture and flag duplicates.

Input is a HAR file (DevTools > Network > Save all as HAR, or a Playwright
`record_har_path`) or a plain text file with one request URL per line.
Output is one row per event that left the browser (requests the HAR records
as blocked or failed are counted separately): vendor, account, event
name, page, transaction or event id, value, and the consent state Google
sent with it. Then it lists likely duplicates and a consent summary.

Usage:
  python decode_hits.py capture.har                    # markdown table
  python decode_hits.py capture.har --json
  python decode_hits.py capture.har --vendor GA4 --event purchase
  python decode_hits.py urls.txt --window 3            # duplicate window in seconds

Decodes GA4 (including batched POST bodies), Google Ads, Meta pixel, TikTok,
Microsoft UET, Pinterest, Reddit, Snapchat and Clarity. Google's `gcs` is
decoded from its documented-by-practice values; the `gcd` letters use the
community decoding (Google does not publish it), so the raw value is kept.
Standard library only. The capture is read locally and never sent anywhere.
"""
import argparse
import json
import re
import sys
from datetime import datetime
from urllib.parse import urlsplit, parse_qsl

GCS = {"G100": "ads denied, analytics denied", "G101": "ads denied, analytics granted",
       "G110": "ads granted, analytics denied", "G111": "ads granted, analytics granted",
       "G1--": "consent mode not required"}
GCD_LETTERS = {  # community decoding, unofficial
    "l": "not set", "p": "denied (default, no update)", "q": "denied (default and update)",
    "r": "granted on update (default denied)", "t": "granted (default, no update)",
    "v": "granted (default and update)", "m": "denied on update (no default)",
    "n": "granted on update (no default)", "u": "denied on update (default granted)",
}
GCD_ORDER = ["ad_storage", "analytics_storage", "ad_user_data", "ad_personalization"]

VENDORS = [
    ("GA4 signals", re.compile(r"stats\.g\.doubleclick\.net/g/collect")),
    ("GA4", re.compile(r"/g/collect|google-analytics\.com/.*collect\?v=2|/collect\?v=2")),
    ("Google Ads", re.compile(r"googleadservices\.com/pagead/conversion|google\.[a-z.]+/pagead/1p-conversion|googleads\.g\.doubleclick\.net/pagead/viewthroughconversion|google\.[a-z.]+/ccm/collect")),
    ("Google Ads remarketing", re.compile(r"google\.[a-z.]+/rmkt/collect|/pagead/1p-user-list")),
    ("Meta", re.compile(r"facebook\.com/tr")),
    ("TikTok", re.compile(r"analytics\.tiktok\.com/api/v\d/(pixel|track)")),
    ("Microsoft UET", re.compile(r"bat\.bing\.(com|net)/action")),
    ("Pinterest", re.compile(r"ct\.pinterest\.com/(v3|user)")),
    ("Reddit", re.compile(r"alb\.reddit\.com/rp\.gif|/rp\.gif\?")),
    ("Snapchat", re.compile(r"tr\.snapchat\.com/p|tr-shadow\.snapchat")),
    ("Clarity", re.compile(r"\.clarity\.ms/collect")),
]


def decode_gcd(gcd):
    if not gcd or len(gcd) < 9:
        return {}
    letters = [gcd[i] for i in (2, 4, 6, 8)]
    return {sig: GCD_LETTERS.get(ch, f"unknown '{ch}'") for sig, ch in zip(GCD_ORDER, letters)}


def load_requests(path):
    text = open(path, encoding="utf-8", errors="ignore").read()
    reqs = []
    try:
        har = json.loads(text)
        for e in har["log"]["entries"]:
            r = e.get("request", {})
            body = (r.get("postData") or {}).get("text", "")
            reqs.append({"url": r.get("url", ""), "method": r.get("method", "GET"), "body": body,
                         "time": e.get("startedDateTime"), "status": (e.get("response") or {}).get("status")})
    except (ValueError, KeyError, TypeError):
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("http"):
                reqs.append({"url": line, "method": "GET", "body": "", "time": None, "status": None})
    return reqs


def parse_time(t):
    if not t:
        return None
    try:
        return datetime.fromisoformat(t.replace("Z", "+00:00"))
    except ValueError:
        return None


def events_from(req):
    url = req["url"]
    vendor = next((name for name, rx in VENDORS if rx.search(url)), None)
    if not vendor:
        return []
    parts = urlsplit(url)
    q = dict(parse_qsl(parts.query, keep_blank_values=True))
    base = {"vendor": vendor, "host": parts.netloc, "url": url, "time": req["time"], "status": req["status"],
            "gcs": q.get("gcs"), "gcd": q.get("gcd")}
    out = []
    if vendor == "GA4":
        lines = [ln for ln in (req["body"] or "").splitlines() if ln.strip()] or [""]
        for ln in lines:
            p = {**q, **dict(parse_qsl(ln, keep_blank_values=True))}
            out.append({**base, "account": p.get("tid"), "event": p.get("en"), "page": p.get("dl"),
                        "txn": p.get("ep.transaction_id"), "value": p.get("epn.value") or p.get("ep.value"),
                        "currency": p.get("cu") or p.get("ep.currency"), "event_id": p.get("ep.event_id"),
                        "items": sum(1 for k in p if re.fullmatch(r"pr\d+", k)) or None})
    elif vendor.startswith("Google Ads"):
        m = re.search(r"/(?:conversion|1p-conversion|viewthroughconversion|1p-user-list|collect)/(\d+)", parts.path)
        out.append({**base, "account": q.get("tid") or (f"AW-{m.group(1)}" if m else None),
                    "event": q.get("en") or (f"conversion:{q.get('label')}" if q.get("label") else "remarketing" if "rmkt" in url or "user-list" in url else None),
                    "page": q.get("url") or q.get("dl"), "txn": q.get("oid") or q.get("transaction_id"),
                    "value": q.get("value"), "currency": q.get("currency_code"), "event_id": None, "items": None})
    elif vendor == "Meta":
        p = {**q, **dict(parse_qsl(req["body"] or "", keep_blank_values=True))}
        out.append({**base, "account": p.get("id"), "event": p.get("ev"), "page": p.get("dl"),
                    "txn": p.get("cd[order_id]") or p.get("cd[transaction_id]"), "value": p.get("cd[value]"),
                    "currency": p.get("cd[currency]"), "event_id": p.get("eid"), "items": None})
    elif vendor == "TikTok":
        try:
            b = json.loads(req["body"] or "{}")
        except ValueError:
            b = {}
        ctx = b.get("context", {}) if isinstance(b, dict) else {}
        props = b.get("properties", {}) if isinstance(b, dict) else {}
        out.append({**base, "account": (ctx.get("pixel") or {}).get("code"), "event": b.get("event"),
                    "page": (ctx.get("page") or {}).get("url"), "txn": props.get("order_id"),
                    "value": props.get("value"), "currency": props.get("currency"), "event_id": b.get("event_id"), "items": None})
    else:
        p = {**q, **dict(parse_qsl(req["body"] or "", keep_blank_values=True))}
        out.append({**base, "account": p.get("ti") or p.get("tid") or p.get("id") or p.get("pid"),
                    "event": p.get("evt") or p.get("event") or p.get("ea") or p.get("e"),
                    "page": p.get("p") or p.get("url") or p.get("u"), "txn": p.get("order_id") or p.get("oid"),
                    "value": p.get("gv") or p.get("value"), "currency": p.get("gc") or p.get("currency"), "event_id": p.get("eid"), "items": None})
    return out


NOT_EVENTS = {None, "", "gtag.config", "remarketing"}
SKIP_DUP_VENDORS = {"Google Ads remarketing", "GA4 signals", "Clarity"}
HIGH = re.compile(r"purchase|conversion|checkout|lead|schedule|book|sign_?up|subscribe|add_to_cart|addtocart", re.I)


def endpoint(r):
    """Host plus path with numbers removed: one logical event often hits several endpoints."""
    return r.get("host", "") + re.sub(r"\d+", "#", urlsplit(r.get("url", "")).path)


def find_duplicates(rows, window):
    """Same vendor, account, event and transaction id (or page) at the same endpoint within the window."""
    dups = []
    seen = {}
    for r in rows:
        if r["vendor"] in SKIP_DUP_VENDORS or r.get("event") in NOT_EVENTS:
            continue
        key = (r["vendor"], r.get("account"), r["event"], r.get("txn") or r.get("page"), endpoint(r))
        t = parse_time(r.get("time"))
        for prev in seen.get(key, []):
            pt = parse_time(prev.get("time"))
            if t is None or pt is None or abs((t - pt).total_seconds()) <= window:
                dups.append((key[:4], prev.get("time"), r.get("time"), "high" if HIGH.search(r["event"]) else "check"))
        seen.setdefault(key, []).append(r)
    return dups


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capture", help="HAR file or text file of URLs")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--vendor", help="only this vendor (GA4, Meta, Google Ads, TikTok, ...)")
    ap.add_argument("--event", help="only this event name")
    ap.add_argument("--window", type=float, default=3.0, help="seconds within which a repeat counts as a duplicate (default 3)")
    a = ap.parse_args()
    all_rows = [ev for req in load_requests(a.capture) for ev in events_from(req)]
    # A HAR also records requests that never left (blocked, DNS refused, aborted): status -1 or 0.
    failed = [r for r in all_rows if r.get("status") is not None and int(r["status"]) <= 0]
    rows = [r for r in all_rows if not (r.get("status") is not None and int(r["status"]) <= 0)]
    if a.vendor:
        rows = [r for r in rows if r["vendor"].lower().startswith(a.vendor.lower())]
    if a.event:
        rows = [r for r in rows if (r.get("event") or "").lower() == a.event.lower()]
    dups = find_duplicates(rows, a.window)
    consent = {}
    for r in rows:
        if r.get("gcs") or r.get("gcd"):
            consent.setdefault((r.get("gcs"), r.get("gcd")), 0)
            consent[(r.get("gcs"), r.get("gcd"))] += 1
    sys.stdout.reconfigure(encoding="utf-8")
    if a.json:
        for r in rows + failed:
            r.pop("url", None)
        print(json.dumps({"events": rows, "blocked_or_failed": failed, "duplicates": [list(d) for d in dups],
                          "consent": [{"gcs": k[0], "gcs_meaning": GCS.get(k[0]), "gcd": k[1], "gcd_decoded": decode_gcd(k[1]), "hits": v} for k, v in consent.items()]}, indent=2, default=str))
        return
    print(f"# Tracking hits in {a.capture}\n")
    note = f", {len(failed)} more attempted but blocked or failed (not counted)" if failed else ""
    print(f"{len(rows)} events sent{note}.\n")
    print("| # | Time | Vendor | Account | Event | Page | Txn / event id | Value | gcs |")
    print("|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        page = (r.get("page") or "")[:60]
        ident = " / ".join(x for x in (r.get("txn"), r.get("event_id")) if x)
        value = f"{r.get('value') or ''} {r.get('currency') or ''}".strip()
        t = (r.get("time") or "")[11:23]
        print(f"| {i} | {t} | {r['vendor']} | {r.get('account') or ''} | {r.get('event') or ''} | {page} | {ident} | {value} | {r.get('gcs') or ''} |")
    print("\n## Possible duplicates\n")
    if not dups:
        print(f"None within {a.window}s (same vendor, account, event and transaction id or page).")
    for (vendor, acct, ev, where), t1, t2, level in dups:
        print(f"- [{level}] {vendor} {acct} `{ev}` on {where}: at {t1} and {t2}")
    print("\n## Consent state sent to Google\n")
    if not consent:
        print("No gcs/gcd parameters found (no Google hits, or consent mode not in use).")
    for (gcs, gcd), n in consent.items():
        decoded = ", ".join(f"{k}: {v}" for k, v in decode_gcd(gcd).items())
        print(f"- {n} hits with gcs={gcs or 'none'} ({GCS.get(gcs, 'no gcs sent' if not gcs else 'unknown')}), gcd={gcd} ({decoded or 'not decoded'})")
    print("\ngcd letters use community decoding; confirm odd values in Tag Assistant.")


if __name__ == "__main__":
    main()
