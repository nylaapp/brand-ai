#!/usr/bin/env python3
"""Decode the tracking hits in a network capture and flag duplicates.

Input is a HAR file (DevTools > Network > Save all as HAR, a Playwright
`record_har_path`, or the hits.har that privacy_matrix.cjs writes) or a plain
text file with one request URL per line. Output is one row per event that left
the browser (requests the HAR records as blocked or failed are counted
separately): vendor, account, event name, page, transaction or event id,
value, and the consent state Google sent with it. Then it lists likely
duplicates and a consent summary.

Usage:
  python decode_hits.py capture.har                    # markdown table
  python decode_hits.py hits.har --by-step             # what each journey step sent
  python decode_hits.py hits.har --by-source           # which install point sent each hit
  python decode_hits.py capture.har --json
  python decode_hits.py capture.har --vendor GA4 --event purchase
  python decode_hits.py urls.txt --window 3            # duplicate window in seconds

hits.har (privacy_matrix.cjs) carries the scenario, step and sending frame of
each request; in a dry run, status 204 means "answered locally, would have
been sent". With an inventory.json next to it, --by-step also shows what each
click hit, navigations stopped and redirects, and steps that sent nothing.

Decodes GA4 (including batched POST bodies), Google Ads, Meta pixel, TikTok
(including the Shopify app's /api/v2/shopify_pixel), Microsoft UET,
Pinterest, Reddit, Snapchat and Clarity. Google mirrors (www.google.com/g/collect,
stats.g.doubleclick.net) and Merchant Center (merchant-center-analytics.goog)
are labelled as such and not counted as GA4 events.

--by-source names the install point behind each hit from what the request
shows (observed conventions, not vendor documentation): the sending frame (top
page, Shopify custom or app pixel sandbox, other iframe), the GA4 endpoint
(Google's or first-party), the `z8<number>` marker in the `gtm` parameter of
Google hits (a tag in that GTM container fired it; the number is the
container's internal id, the one in its tagmanager.google.com URL), Meta event
ids (`sh-` is Shopify's Meta app) and TikTok's Shopify endpoint. It then lists
every event a destination received from more than one source in the same step.

Google's `gcs` is decoded from its documented-by-practice values; the `gcd`
letters use the community decoding (Google does not publish it), so the raw
value is kept. Standard library only. The capture is read locally and never
sent anywhere.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
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

# Order matters: the first match wins, so mirrors and Merchant Center come before GA4.
VENDORS = [
    ("Merchant Center", re.compile(r"merchant-center-analytics\.goog")),
    ("Google mirror", re.compile(r"stats\.g\.doubleclick\.net/g/collect|www\.google\.[a-z.]+/g/collect")),
    ("Google Ads", re.compile(r"googleadservices\.com/pagead/conversion|google\.[a-z.]+/pagead/1p-conversion|googleads\.g\.doubleclick\.net/pagead/viewthroughconversion|google\.[a-z.]+/ccm/collect|ad\.doubleclick\.net/ccm/(s/)?collect")),
    ("Google Ads remarketing", re.compile(r"google\.[a-z.]+/rmkt/collect|/pagead/1p-user-list")),
    ("GA4", re.compile(r"/g/(s/)?collect|google-analytics\.com/.*collect\?v=2|/collect\?v=2")),
    ("Meta", re.compile(r"facebook\.com/tr([/?]|$)")),
    ("TikTok signals", re.compile(r"analytics\.tiktok\.com/api/v\d/pixel/(act|inter)")),
    ("TikTok", re.compile(r"analytics\.tiktok\.com/api/v\d/(pixel|track|shopify_pixel)")),
    ("Microsoft UET", re.compile(r"bat\.bing\.(com|net)/action")),
    ("Pinterest", re.compile(r"ct\.pinterest\.com/(v3|user)")),
    ("Reddit", re.compile(r"alb\.reddit\.com/rp\.gif|/rp\.gif\?")),
    ("Snapchat", re.compile(r"tr\.snapchat\.com/p|tr-shadow\.snapchat")),
    ("Clarity", re.compile(r"\.clarity\.ms/collect")),
]
GA_FORMAT = {"GA4", "Google mirror", "Merchant Center"}
GOOGLE_FAMILY = GA_FORMAT | {"Google Ads", "Google Ads remarketing"}
# Copies, automatic signals and session data: listed, never counted as events or duplicates.
NON_EVENT_VENDORS = {"Google mirror", "Merchant Center", "Google Ads remarketing", "TikTok signals", "Clarity"}
GOOGLE_HOSTED = re.compile(r"(^|\.)(google-analytics\.com|analytics\.google\.com)$")
SANDBOX_PAGE = re.compile(r"/web-pixels@|/wpm@|/sandbox/")


def decode_gcd(gcd):
    if not gcd or len(gcd) < 9:
        return {}
    letters = [gcd[i] for i in (2, 4, 6, 8)]
    return {sig: GCD_LETTERS.get(ch, f"unknown '{ch}'") for sig, ch in zip(GCD_ORDER, letters)}


def frame_kind(e):
    """Frame kind from hits.har; older dry captures only kept the frame URL."""
    if e.get("_frameKind"):
        return e["_frameKind"]
    f = e.get("_frame")
    if not f:
        return None
    if re.search(r"/web-pixels@[^/]*/cust", f):
        return "shopify-custom-pixel"
    if "/web-pixels@" in f:
        return "shopify-app-pixel"
    return f if f in ("service-worker", "no-frame") else "page"


def load_capture(path):
    """Requests plus what the file says about itself (hits.har mode, labelled steps)."""
    text = open(path, encoding="utf-8", errors="ignore").read()
    reqs, meta = [], {"mode": None, "labelled": False}
    try:
        har = json.loads(text)
        meta["mode"] = har["log"].get("_mode")
        for e in har["log"]["entries"]:
            r = e.get("request", {})
            body = (r.get("postData") or {}).get("text", "")
            reqs.append({"url": r.get("url", ""), "method": r.get("method", "GET"), "body": body,
                         "time": e.get("startedDateTime"), "status": (e.get("response") or {}).get("status"),
                         "scenario": e.get("_scenario"), "step": e.get("_step"), "frame": e.get("_frame"),
                         "frame_kind": frame_kind(e), "dry": e.get("_dry")})
            if "_step" in e:
                meta["labelled"] = True
    except (ValueError, KeyError, TypeError, AttributeError):
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("http"):
                reqs.append({"url": line, "method": "GET", "body": "", "time": None, "status": None})
    return reqs, meta


def load_requests(path):
    return load_capture(path)[0]


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
    base = {"vendor": vendor, "host": parts.netloc, "url": url, "time": req.get("time"), "status": req.get("status"),
            "gcs": q.get("gcs"), "gcd": q.get("gcd"), "gtm": q.get("gtm"),
            "scenario": req.get("scenario"), "step": req.get("step"), "frame_kind": req.get("frame_kind"), "dry": req.get("dry")}
    body = req.get("body") or ""
    out = []
    if vendor in GA_FORMAT:
        lines = [ln for ln in body.splitlines() if ln.strip()] or [""]
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
        p = {**q, **dict(parse_qsl(body, keep_blank_values=True))}
        out.append({**base, "account": p.get("id"), "event": p.get("ev"), "page": p.get("dl"),
                    "txn": p.get("cd[order_id]") or p.get("cd[transaction_id]"), "value": p.get("cd[value]"),
                    "currency": p.get("cd[currency]"), "event_id": p.get("eid"), "items": None, "agent": p.get("a")})
    elif vendor.startswith("TikTok"):
        try:
            b = json.loads(body or "{}")
        except ValueError:
            b = {}
        b = b if isinstance(b, dict) else {}
        ctx = b.get("context") or {}
        props = b.get("properties") or {}
        out.append({**base, "account": (ctx.get("pixel") or {}).get("code"), "event": b.get("event") or b.get("action"),
                    "page": (ctx.get("page") or {}).get("url"), "txn": props.get("order_id"),
                    "value": props.get("value"), "currency": props.get("currency"), "event_id": b.get("event_id") or None,
                    "items": None, "shopify_app": "/shopify_pixel" in parts.path or b.get("partner") == "Shopify"})
    else:
        p = {**q, **dict(parse_qsl(body, keep_blank_values=True))}
        out.append({**base, "account": p.get("ti") or p.get("tid") or p.get("id") or p.get("pid"),
                    "event": p.get("evt") or p.get("event") or p.get("ea") or p.get("e"),
                    "page": p.get("p") or p.get("url") or p.get("u"), "txn": p.get("order_id") or p.get("oid"),
                    "value": p.get("gv") or p.get("value"), "currency": p.get("gc") or p.get("currency"), "event_id": p.get("eid"), "items": None})
    return out


def eid_prefix(eid):
    m = re.match(r"^([A-Za-z]{1,12}[-_.])", eid)
    return m.group(1) if m else ("numeric" if eid.isdigit() else "unprefixed")


def source_of(r):
    """The install point a hit points to, from the request alone."""
    v, parts = r["vendor"], []
    if v in GOOGLE_FAMILY:
        m = re.search(r"z8(\d+)", r.get("gtm") or "")
        parts.append(f"tag in GTM container #{m.group(1)}" if m else "Google tag, no GTM marker")
        if v == "GA4":
            host = r.get("host") or ""
            parts.append("Google endpoint" if GOOGLE_HOSTED.search(host) else f"first-party endpoint {host}")
    elif v == "Meta":
        eid = r.get("event_id") or ""
        if eid.startswith("sh-"):
            parts.append("Shopify Meta app (event id sh-)")
        elif eid:
            parts.append(f"Meta pixel, event id {eid_prefix(eid)}")
        else:
            parts.append("Meta pixel, no event id")
    elif v.startswith("TikTok"):
        parts.append("Shopify TikTok app" if r.get("shopify_app") else "TikTok pixel on the page or in a tag manager")
    else:
        parts.append(r.get("host") or "?")
    return "; ".join(parts)


def where_sent(r):
    return f"{r['source']} [{r.get('frame_kind') or 'frame unknown'}]"


NOT_EVENTS = {None, "", "gtag.config", "remarketing"}
HIGH = re.compile(r"purchase|conversion|checkout|lead|schedule|book|sign_?up|subscribe|add_to_cart|addtocart", re.I)


def is_event(r):
    return r["vendor"] not in NON_EVENT_VENDORS and r.get("event") not in NOT_EVENTS


def endpoint(r):
    """Host plus path with numbers removed: one logical event often hits several endpoints."""
    return r.get("host", "") + re.sub(r"\d+", "#", urlsplit(r.get("url", "")).path)


def find_duplicates(rows, window):
    """Same vendor, account, event and transaction id (or page) at the same endpoint within the window."""
    dups = []
    seen = {}
    for r in rows:
        if not is_event(r):
            continue
        key = (r["vendor"], r.get("account"), r["event"], r.get("txn") or r.get("page"), endpoint(r))
        t = parse_time(r.get("time"))
        for prev in seen.get(key, []):
            pt = parse_time(prev.get("time"))
            if t is None or pt is None or abs((t - pt).total_seconds()) <= window:
                dups.append((key[:4], prev.get("time"), r.get("time"), "high" if HIGH.search(r["event"]) else "check"))
        seen.setdefault(key, []).append(r)
    return dups


def multi_source(rows):
    """Events a destination got from more than one install point in the same step (or on the same page)."""
    by = defaultdict(lambda: defaultdict(set))
    for r in rows:
        if not is_event(r):
            continue
        place = ("step", r.get("scenario"), r["step"]) if r.get("step") else ("page", (r.get("page") or "").split("?")[0].split("#")[0])
        by[(r["vendor"], r.get("account"), r["event"])][place].add(where_sent(r))
    out = []
    for (vendor, acct, ev), places in by.items():
        hit = {p: s for p, s in places.items() if len(s) > 1}
        if hit:
            first = next(iter(hit))
            out.append({"vendor": vendor, "account": acct, "event": ev, "places": len(hit),
                        "place_kind": first[0], "example": " | ".join(str(x) for x in first[1:] if x),
                        "sources": sorted(set().union(*hit.values()))})
    return sorted(out, key=lambda d: (-d["places"], d["vendor"], d["event"] or ""))


def counts(rows):
    c = Counter(r.get("event") or "?" for r in rows)
    return ", ".join(f"{ev} {n}" for ev, n in c.most_common())


def load_steps(capture_path):
    """inventory.json next to a hits.har: step order and notes (click target, stopped navigation, redirect)."""
    path = os.path.join(os.path.dirname(os.path.abspath(capture_path)), "inventory.json")
    try:
        inv = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    steps = []
    for sc in inv.get("scenarios") or []:
        for s in sc.get("steps") or []:
            notes = []
            c = s.get("clicked")
            if c:
                notes.append(f"clicked {c.get('tag')} \"{c.get('text')}\"" + (f" ({c.get('href')})" if c.get("href") else ""))
            if s.get("navigation"):
                notes.append(f"navigation {s['navigation']}")
            if s.get("redirectedFrom"):
                notes.append(f"landed on {s.get('url')}, redirected from {s['redirectedFrom']}")
            if s.get("error"):
                notes.append(f"error: {s['error'][:120]}")
            steps.append(((sc.get("scenario"), s.get("label")), "; ".join(notes)))
    return steps


def print_by_step(rows, capture_path):
    groups = defaultdict(list)
    order = []
    for r in rows:
        k = (r.get("scenario"), r.get("step"))
        if k not in groups:
            order.append(k)
        groups[k].append(r)
    steps = load_steps(capture_path)
    notes = {}
    if steps:
        known = [k for k, _ in steps]
        notes = dict(steps)
        order = known + [k for k in order if k not in notes]
    print("## What each step sent\n")
    for k in order:
        sc, st = k
        print(f"### {sc or '-'} | {st or '-'}\n")
        if notes.get(k):
            print(f"_{notes[k]}_\n")
        evs = groups.get(k, [])
        if not evs:
            print("- no collection requests\n")
            continue
        c = Counter()
        for r in evs:
            if is_event(r):
                c[(r["vendor"], r.get("account") or "", r.get("event") or "?", where_sent(r))] += 1
            else:
                c[(r["vendor"], r.get("account") or "", "(not events)", "")] += 1
        for (vendor, acct, ev, src), n in sorted(c.items()):
            print(f"- {n}x {vendor} {acct} `{ev}`" + (f" from {src}" if src else ""))
        print()


def print_by_source(rows, multi):
    print("## Hits by install point\n")
    groups = defaultdict(list)
    for r in rows:
        if is_event(r):
            groups[(r["vendor"], r.get("account") or "", r["source"], r.get("frame_kind") or "?")].append(r)
    print("| Vendor | Account | Source | Frame | Events |")
    print("|---|---|---|---|---|")
    for (vendor, acct, src, frame), evs in sorted(groups.items()):
        agents = sorted({r.get("agent") for r in evs if r.get("agent")})
        extra = f" (agent {', '.join(agents)})" if agents else ""
        print(f"| {vendor} | {acct} | {src}{extra} | {frame} | {counts(evs)} |")
    other = Counter((r["vendor"], r.get("account") or "", r["source"], r.get("frame_kind") or "?") for r in rows if not is_event(r))
    if other:
        print("\nNot counted as events (mirrors, Merchant Center, remarketing, automatic signals, session data, hits without an event name):\n")
        for (vendor, acct, src, frame), n in sorted(other.items()):
            print(f"- {n}x {vendor} {acct} from {src} [{frame}]")
    print("\nMeta's `a` agent names the first library that set up the shared `fbq`, so two installs can show the same agent; the event id prefix is the better signal.")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("capture", help="HAR file (hits.har from privacy_matrix.cjs, or any HAR) or text file of URLs")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--vendor", help="only this vendor (GA4, Meta, Google Ads, TikTok, ...)")
    ap.add_argument("--event", help="only this event name")
    ap.add_argument("--scenario", help="only this scenario (hits.har)")
    ap.add_argument("--by-step", action="store_true", help="group by journey step (hits.har)")
    ap.add_argument("--by-source", action="store_true", help="attribute each hit to an install point")
    ap.add_argument("--window", type=float, default=3.0, help="seconds within which a repeat counts as a duplicate (default 3)")
    a = ap.parse_args()
    reqs, meta = load_capture(a.capture)
    if a.scenario:
        reqs = [r for r in reqs if r.get("scenario") == a.scenario]
    all_rows = [ev for req in reqs for ev in events_from(req)]
    for r in all_rows:
        r["source"] = source_of(r)
    # A HAR also records requests that never left (blocked, DNS refused, aborted): status -1 or 0.
    failed = [r for r in all_rows if r.get("status") is not None and int(r["status"]) <= 0]
    rows = [r for r in all_rows if not (r.get("status") is not None and int(r["status"]) <= 0)]
    if a.vendor:
        rows = [r for r in rows if r["vendor"].lower().startswith(a.vendor.lower())]
    if a.event:
        rows = [r for r in rows if (r.get("event") or "").lower() == a.event.lower()]
    dups = find_duplicates(rows, a.window)
    multi = multi_source(rows)
    sandbox = Counter((r["vendor"], r.get("account"), r.get("event")) for r in rows if is_event(r) and SANDBOX_PAGE.search(r.get("page") or ""))
    undecoded = Counter()
    if meta["labelled"]:
        for q in reqs:
            if not any(rx.search(q["url"]) for _, rx in VENDORS):
                p = urlsplit(q["url"])
                undecoded[p.netloc + re.sub(r"[0-9a-f]{8,}|\d{3,}", "#", p.path)[:50]] += 1
    dry_local = sum(1 for q in reqs if q.get("dry"))
    leaked = sum(1 for q in reqs if q.get("dry") is False and (q.get("status") or 0) > 0) if meta["mode"] == "dry" else 0
    consent = {}
    for r in rows:
        if r.get("gcs") or r.get("gcd"):
            consent.setdefault((r.get("gcs"), r.get("gcd")), 0)
            consent[(r.get("gcs"), r.get("gcd"))] += 1
    sys.stdout.reconfigure(encoding="utf-8")
    if a.json:
        for r in rows + failed:
            r.pop("url", None)
        print(json.dumps({"mode": meta["mode"], "events": rows, "blocked_or_failed": failed, "duplicates": [list(d) for d in dups],
                          "multi_source": multi, "sandbox_page_address": [{"vendor": k[0], "account": k[1], "event": k[2], "hits": v} for k, v in sandbox.items()],
                          "not_decoded": dict(undecoded), "dry_answered_locally": dry_local, "dry_reached_network": leaked,
                          "consent": [{"gcs": k[0], "gcs_meaning": GCS.get(k[0]), "gcd": k[1], "gcd_decoded": decode_gcd(k[1]), "hits": v} for k, v in consent.items()]}, indent=2, default=str))
        return
    print(f"# Tracking hits in {a.capture}\n")
    note = f", {len(failed)} more attempted but blocked or failed (not counted)" if failed else ""
    print(f"{len(rows)} hits sent{note}.")
    if meta["mode"] == "dry" or dry_local:
        print(f"Dry capture: {dry_local} collection requests were answered locally (status 204 means they would have been sent); none of them reached an account.")
    if leaked:
        print(f"WARNING: {leaked} collection requests reached the network during the dry run (`_dry` false, status above 0).")
    print()
    if a.by_step:
        print_by_step(rows, a.capture)
    if a.by_source:
        print_by_source(rows, multi)
    if not a.by_step and not a.by_source:
        has_step = any(r.get("step") for r in rows)
        print("| # | Time | " + ("Step | " if has_step else "") + "Vendor | Account | Event | Page | Txn / event id | Value | gcs |")
        print("|---|---|" + ("---|" if has_step else "") + "---|---|---|---|---|---|---|")
        for i, r in enumerate(rows, 1):
            page = (r.get("page") or "")[:60]
            ident = " / ".join(x for x in (r.get("txn"), r.get("event_id")) if x)
            value = f"{r.get('value') or ''} {r.get('currency') or ''}".strip()
            t = (r.get("time") or "")[11:23]
            step = f"{r.get('scenario') or ''}: {r.get('step') or ''} | " if has_step else ""
            print(f"| {i} | {t} | {step}{r['vendor']} | {r.get('account') or ''} | {r.get('event') or ''} | {page} | {ident} | {value} | {r.get('gcs') or ''} |")
        print("\nMirrors, Merchant Center, remarketing and automatic signals are listed but never counted as events or duplicates.")
    print("\n## Same event from more than one source\n")
    if not multi:
        print("None: every event reached each destination from one install point" + (" per step." if meta["labelled"] else " per page."))
    for m in multi:
        where = f"{m['places']} step(s), e.g. {m['example']}" if m["place_kind"] == "step" else f"{m['places']} page(s), e.g. {m['example']}"
        print(f"- {m['vendor']} {m['account'] or ''} `{m['event']}` in {where}. Sources: " + "; ".join(f"({s})" for s in m["sources"]))
    if multi:
        print("\nTwo sources for one event usually means two install paths (FC-01), or one path triggering another through a shared dataLayer (FC-33). Confirm before calling it a double count.")
    if sandbox:
        print("\n## Hits whose page address is a sandbox URL\n")
        for (vendor, acct, ev), n in sandbox.most_common():
            print(f"- {n}x {vendor} {acct or ''} `{ev}`")
        print("\nA tag running inside a Shopify pixel sandbox reports the sandbox as the page (FC-34).")
    print("\n## Possible duplicates\n")
    if not dups:
        print(f"None within {a.window}s (same vendor, account, event and transaction id or page).")
    for (vendor, acct, ev, where), t1, t2, level in dups:
        print(f"- [{level}] {vendor} {acct} `{ev}` on {where}: at {t1} and {t2}")
    if undecoded:
        print("\n## Collection requests not decoded\n")
        for k, n in undecoded.most_common(20):
            print(f"- {n}x {k}")
    print("\n## Consent state sent to Google\n")
    if not consent:
        print("No gcs/gcd parameters found (no Google hits, or consent mode not in use).")
    for (gcs, gcd), n in consent.items():
        decoded = ", ".join(f"{k}: {v}" for k, v in decode_gcd(gcd).items())
        print(f"- {n} hits with gcs={gcs or 'none'} ({GCS.get(gcs, 'no gcs sent' if not gcs else 'unknown')}), gcd={gcd} ({decoded or 'not decoded'})")
    print("\ngcd letters use community decoding; confirm odd values in Tag Assistant.")


if __name__ == "__main__":
    main()
