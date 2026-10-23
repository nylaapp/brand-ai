#!/usr/bin/env python3
"""Take a no-login snapshot of a site's tracking setup and compare it with the last one.

For each URL it reads the public page source (no JavaScript runs) and records:
script hosts, tag IDs (GA4, Google Ads, GTM, Merchant Center), the Shopify
theme and pixel list when the site is on Shopify, and, for every GTM container
found, the live published version from the public gtm.js. Snapshots are saved
as dated JSON files; each run reports what changed since the previous one.

A changed GTM version, a new or removed pixel, a new script host, a theme
switch or a changed tag ID means the dependency register in ANALYTICS.md may
be out of date: review it (analytics-guardrails, build mode).

Usage:
  python drift_snapshot.py https://store.example.com/ https://store.example.com/products/x --dir analytics-snapshots/store
  python drift_snapshot.py URL --dir DIR --gtm GTM-XXXXXXX     # also check a container not in the page source
  python drift_snapshot.py --compare old.json new.json

Standard library only. Reads public pages; no sign-in, no clicks, no forms.
Pages that render tags with JavaScript only (a GTM container adding scripts)
show those scripts in a browser inventory, not here, so script hosts are
reported as "(static source only)"; the GTM version check covers changes
inside the container. A Shopify `?preview_theme_id=` URL fetched without a
browser session is served by the published theme: the run warns instead of
filing it under the wrong theme.
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
ID_RE = re.compile(r"\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|MC-[A-Z0-9]{6,12}|GTM-[A-Z0-9]{5,9})\b")
SRC_RE = re.compile(r"<script[^>]+src=[\"']([^\"']+)[\"']", re.I)
THEME_RE = re.compile(r"Shopify\.theme\s*=\s*(\{[^}]*\})")
PREVIEW_RE = re.compile(r"[?&]preview_theme_id=(\d+)")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.geturl(), resp.read().decode("utf-8", errors="ignore")


def pixel_list(html):
    i = html.find("webPixelsConfigList")
    if i < 0:
        return None
    j = html.find("[", i)
    depth, in_str, esc = 0, False, False
    for k in range(j, len(html)):
        c = html[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                try:
                    raw = json.loads(html[j:k + 1])
                except ValueError:
                    return None
                return sorted(
                    f"{p.get('type')}|{p.get('apiClientId') or 'custom'}|{','.join(p.get('privacyPurposes') or [])}|"
                    f"{','.join(sorted(set(ID_RE.findall(p.get('configuration') or ''))))}"
                    for p in raw)
    return None


def gtm_version(container):
    try:
        _, js = fetch(f"https://www.googletagmanager.com/gtm.js?id={container}")
    except Exception as exc:
        return {"error": str(exc)}
    m = re.search(r'"version"\s*:\s*"(\d+)"', js)
    return {"version": m.group(1) if m else None, "ids": sorted(set(ID_RE.findall(js)) - {container})}


def snapshot(urls, extra_gtm):
    snap = {"taken_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "pages": {}, "gtm": {}}
    containers = set(extra_gtm or [])
    for url in urls:
        try:
            final, html = fetch(url)
        except Exception as exc:
            snap["pages"][url] = {"error": str(exc)}
            continue
        hosts = set()
        for src in SRC_RE.findall(html):
            m = re.match(r"(?:https?:)?//([^/]+)", src)
            if m:
                hosts.add(m.group(1).lower())
        ids = sorted(set(ID_RE.findall(html)))
        containers.update(i for i in ids if i.startswith("GTM-"))
        theme, theme_id = None, None
        tm = THEME_RE.search(html)
        if tm:
            try:
                t = json.loads(tm.group(1))
                theme_id = str(t.get("id"))
                theme = f"{t.get('name')} (id {t.get('id')}, {t.get('schema_name')} {t.get('schema_version')})"
            except ValueError:
                theme = tm.group(1)[:120]
        page = {"final_url": final, "script_hosts": sorted(hosts), "ids": ids,
                "shopify_theme": theme, "pixels": pixel_list(html)}
        # Without a browser session a preview URL is served by the PUBLISHED theme; say so instead of filing it silently.
        want = PREVIEW_RE.search(url)
        if want and theme_id != want.group(1):
            page["preview_warning"] = (f"asked for preview theme {want.group(1)}, served by {theme or 'no Shopify theme'}: "
                                       "theme code here is the published theme's (pixels are store-wide); "
                                       "check the preview with a browser inventory")
        snap["pages"][url] = page
    for c in sorted(containers):
        snap["gtm"][c] = gtm_version(c)
    return snap


def compare(old, new):
    changes = []
    for c in sorted(set(old.get("gtm", {})) | set(new.get("gtm", {}))):
        a, b = old.get("gtm", {}).get(c, {}), new.get("gtm", {}).get(c, {})
        if not a:
            changes.append(f"GTM {c}: newly seen (version {b.get('version')})")
        elif not b:
            changes.append(f"GTM {c}: no longer seen (was version {a.get('version')})")
        elif a.get("version") != b.get("version"):
            changes.append(f"GTM {c}: version {a.get('version')} -> {b.get('version')} (container republished; export it and diff)")
        if a and b and a.get("ids") != b.get("ids"):
            changes.append(f"GTM {c}: IDs inside changed {a.get('ids')} -> {b.get('ids')}")
    for url in sorted(set(old.get("pages", {})) | set(new.get("pages", {}))):
        a, b = old.get("pages", {}).get(url, {}), new.get("pages", {}).get(url, {})
        if not a or not b:
            changes.append(f"{url}: only in {'new' if b else 'old'} snapshot")
            continue
        for key, label in (("script_hosts", "script hosts"), ("ids", "tag IDs"), ("pixels", "Shopify pixels")):
            sa, sb = set(a.get(key) or []), set(b.get(key) or [])
            if sb - sa:
                changes.append(f"{url}: {label} added: {', '.join(sorted(sb - sa))}")
            if sa - sb:
                changes.append(f"{url}: {label} removed: {', '.join(sorted(sa - sb))}")
        if a.get("shopify_theme") != b.get("shopify_theme"):
            changes.append(f"{url}: live theme changed: {a.get('shopify_theme')} -> {b.get('shopify_theme')}")
    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--dir", help="folder for dated snapshots (compared with the newest one there)")
    ap.add_argument("--gtm", action="append", help="extra GTM container ID to check")
    ap.add_argument("--compare", nargs=2, metavar=("OLD", "NEW"))
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if a.compare:
        old, new = (json.load(open(p, encoding="utf-8")) for p in a.compare)
        changes = compare(old, new)
    else:
        if not a.urls:
            ap.error("give URLs, or --compare OLD NEW")
        new = snapshot(a.urls, a.gtm)
        changes = None
        if a.dir:
            os.makedirs(a.dir, exist_ok=True)
            previous = sorted(glob.glob(os.path.join(a.dir, "snapshot-*.json")))
            path = os.path.join(a.dir, f"snapshot-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json")
            with open(path, "w", encoding="utf-8") as fh:
                json.dump(new, fh, indent=2)
            print(f"saved {path}")
            if previous:
                old = json.load(open(previous[-1], encoding="utf-8"))
                print(f"compared with {previous[-1]} ({old.get('taken_at')})")
                changes = compare(old, new)
            else:
                print("first snapshot in this folder: nothing to compare yet")
        for c, info in new["gtm"].items():
            print(f"GTM {c}: live version {info.get('version')}")
        for url, p in new["pages"].items():
            if "error" in p:
                print(f"{url}: ERROR {p['error']}")
            else:
                # Static source only: tags a tag manager or loader injects at runtime are not counted here.
                print(f"{url}: {len(p['script_hosts'])} script hosts (static source only), IDs {', '.join(p['ids']) or 'none'}, "
                      f"{'theme ' + p['shopify_theme'] if p['shopify_theme'] else 'not Shopify'}, "
                      f"{len(p['pixels']) if p['pixels'] is not None else 0} pixels")
                if p.get("preview_warning"):
                    print(f"  WARNING: {p['preview_warning']}")
    if changes is not None:
        if changes:
            print("\nDRIFT:")
            for c in changes:
                print(f"- {c}")
            print("\nReview the dependency register in ANALYTICS.md for anything listed above.")
        else:
            print("\nNo drift since the previous snapshot.")


if __name__ == "__main__":
    main()
