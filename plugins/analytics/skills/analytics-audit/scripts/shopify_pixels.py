#!/usr/bin/env python3
"""List the web pixels a Shopify storefront loads, from its public page source.

Every Shopify storefront page embeds the Web Pixels Manager setup with a
`webPixelsConfigList`: one entry per connected pixel (app pixels and custom
pixels), with its type, sandbox, consent purposes and configuration. The
configuration usually holds the destination IDs (GA4, Google Ads, Merchant
Center, Meta pixel, TikTok code, and so on). This is observed behaviour,
not a documented Shopify API, so treat the result as a fast first pass and
confirm in Settings > Customer events when you have admin access. Custom
pixel code is not in the page source; only its existence and settings are.

The script also lists, from the same source:
- tag IDs that appear in the page outside the pixel list (theme code, app
  embeds, a GTM snippet), so a destination wired twice shows up;
- pixel destination IDs that also sit INSIDE a GTM container on the page (it
  reads each container's public gtm.js), the most common second path;
- ScriptTags (the `asyncLoad` URL list; store-wide, they survive theme changes)
  and app blocks and embeds (`BEGIN app block` comments; they change with the theme);
- the theme that served the page. A `?preview_theme_id=` URL fetched without a
  browser session gets the PUBLISHED theme: the script warns when the served
  theme differs. Pixels and ScriptTags are store-wide, so they are still right;
  theme code IDs and app blocks are the published theme's. Previews need the
  browser inventory (page_inventory.js).

Usage:
  python shopify_pixels.py https://store.example.com/            # fetch and list
  python shopify_pixels.py saved-page.html --json                 # from a saved file
  python shopify_pixels.py URL1 URL2 --out pixels.md
  python shopify_pixels.py URL --gtm GTM-XXXXXXX                  # a container injected at runtime (not in the source)
  python shopify_pixels.py URL --no-gtm                           # skip the gtm.js reads

Standard library only. Fetches with a desktop browser user agent; does not
log in, submit anything or follow links beyond redirects.
"""
import argparse
import json
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

# Recognise the vendor from configuration keys (stable) before app ids (observed only).
CONFIG_SIGNATURES = [
    (lambda c: "google_tag_ids" in c, "Google & YouTube app"),
    (lambda c: c.get("pixel_type") == "facebook_pixel" or "pixel_id" in c and "facebook" in json.dumps(c), "Meta (Facebook & Instagram app)"),
    (lambda c: "pixelCode" in c, "TikTok"),
    (lambda c: "redditPixelId" in c, "Reddit"),
    (lambda c: "snapPixelId" in c or "snap_pixel_id" in c, "Snapchat"),
    (lambda c: "config_url" in c and "elevar" in str(c.get("config_url")), "Elevar"),
    (lambda c: "shareasale" in json.dumps(c), "ShareASale / Awin"),
    (lambda c: "webPixelName" in c, None),  # use the name it declares
    (lambda c: "klaviyo" in json.dumps(c).lower(), "Klaviyo"),
    (lambda c: "pinterest" in json.dumps(c).lower(), "Pinterest"),
]
OBSERVED_APP_IDS = {  # seen on live stores; use only when config gives no hint
    "1780363": "Google & YouTube app",
    "2329312": "Meta (Facebook & Instagram app)",
    "683015": "Judge.me",
    "4929191": "ShareASale / Awin",
    "123074": "Klaviyo",
    "3009811": "Pinterest",
    "4383523": "TikTok",
    "2509311": "Elevar",
    "shopify-pixel": "Shopify (built-in)",
}
ID_PATTERNS = {
    "google": re.compile(r"\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|MC-[A-Z0-9]{6,12}|DC-\d{6,10}|GTM-[A-Z0-9]{5,9})\b"),
}
RAW_ID_KEYS = ("pixel_id", "pixelCode", "redditPixelId", "tagID", "accountID", "projectId")
THEME_RE = re.compile(r"Shopify\.theme\s*=\s*(\{[^}]*\})")
PREVIEW_RE = re.compile(r"[?&]preview_theme_id=(\d+)")
ASYNC_LOAD_RE = re.compile(r"function asyncLoad\(\)\s*\{.*?var urls\s*=\s*(\[.*?\]);", re.S)
APP_BLOCK_RE = re.compile(r"BEGIN app block: shopify://apps/([^/\s]+)/blocks/([^/\s]+)")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.geturl(), resp.read().decode("utf-8", errors="ignore")


def extract_list(html):
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
                return json.loads(html[j:k + 1])
    return None


def parse_config(raw):
    try:
        cfg = json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        return {}
    if isinstance(cfg.get("config"), str):  # Google app nests a JSON string
        try:
            cfg = {**cfg, **json.loads(cfg["config"])}
        except ValueError:
            pass
    return cfg if isinstance(cfg, dict) else {}


def vendor(p, cfg):
    for test, name in CONFIG_SIGNATURES:
        try:
            if test(cfg):
                return name or cfg.get("webPixelName")
        except Exception:
            continue
    api = str(p.get("apiClientId") or "")
    if api in OBSERVED_APP_IDS:
        return OBSERVED_APP_IDS[api]
    if p.get("type") == "CUSTOM":
        return "Custom pixel (code not in page source)"
    return f"unknown app {api}" if api else "unknown"


def destination_ids(cfg):
    text = json.dumps(cfg)
    ids = set(ID_PATTERNS["google"].findall(text))
    for key in RAW_ID_KEYS:
        if cfg.get(key):
            ids.add(f"{key}={cfg[key]}")
    return sorted(ids)


def raw_ids(row):
    """Destination IDs without the `key=` label, for matching against other install points."""
    return {x.split("=", 1)[-1] for x in row["destination_ids"]}


def served_theme(html):
    m = THEME_RE.search(html)
    if not m:
        return None
    try:
        t = json.loads(m.group(1))
    except ValueError:
        return {"raw": m.group(1)[:120]}
    return {k: t.get(k) for k in ("name", "id", "role", "schema_name", "schema_version")}


def script_tags(html):
    m = ASYNC_LOAD_RE.search(html)
    if not m:
        return []
    try:
        urls = json.loads(m.group(1))
    except ValueError:
        return []
    return sorted({u.split("?")[0] for u in urls if isinstance(u, str)})


def app_blocks(html):
    return sorted({f"{a}/{b}" for a, b in APP_BLOCK_RE.findall(html)})


def gtm_overlap(containers, pixel_ids):
    """Which pixel destination IDs also sit inside each GTM container (public gtm.js)."""
    out = {}
    for c in sorted(containers):
        try:
            _, js = fetch(f"https://www.googletagmanager.com/gtm.js?id={c}")
        except Exception as exc:  # report and continue
            out[c] = {"error": str(exc)}
            continue
        i = js.find('"resource"')
        body = js[i:js.find('"runtime"', i)] if i >= 0 else js
        m = re.search(r'"version"\s*:\s*"(\d+)"', body)
        found = sorted(x for x in pixel_ids if x and (x in body or (x.startswith("AW-") and x[3:] in body)))
        out[c] = {"version": m.group(1) if m else None, "ids_also_in_pixels": found}
    return out


def analyse(source, html, final_url=None, extra_gtm=(), read_gtm=True):
    lst = extract_list(html)
    rows = []
    if lst:
        for p in lst:
            cfg = parse_config(p.get("configuration"))
            rows.append({
                "id": p.get("id"),
                "vendor": vendor(p, cfg),
                "type": p.get("type"),
                "sandbox": p.get("runtimeContext"),
                "consent_purposes": p.get("privacyPurposes", []),
                "data_sharing": p.get("dataSharingState"),
                "app_id": p.get("apiClientId"),
                "destination_ids": destination_ids(cfg),
                "google_events": sorted({e.get("type") for e in cfg.get("gtag_events", []) if isinstance(e, dict)}),
            })
    # IDs elsewhere in the page (theme code, app embeds, GTM snippet)
    i = html.find("webPixelsConfigList")
    page_wo_pixels = html if i < 0 else html[:i] + html[i + 20000:]
    page_ids = sorted(set(ID_PATTERNS["google"].findall(page_wo_pixels)))
    pixel_ids = {x for r in rows for x in raw_ids(r)}
    twice = sorted(set(page_ids) & pixel_ids)
    theme = served_theme(html)
    warning = None
    want = PREVIEW_RE.search(source) or PREVIEW_RE.search(final_url or "")
    if want and (not theme or str(theme.get("id")) != want.group(1)):
        warning = (f"Asked for preview theme {want.group(1)} but the page was served by "
                   f"{(theme or {}).get('name')} (id {(theme or {}).get('id')}, role {(theme or {}).get('role')}): "
                   "a preview needs a browser session. Pixels and ScriptTags below are store-wide and still valid; "
                   "theme code IDs and app blocks are the served theme's. Use page_inventory.js in a browser for the preview.")
    containers = {i for i in page_ids if i.startswith("GTM-")} | set(extra_gtm or [])
    overlap = gtm_overlap(containers, pixel_ids) if read_gtm and lst and containers else {}
    return {"source": source, "final_url": final_url, "is_shopify": lst is not None, "theme": theme,
            "preview_warning": warning, "pixels": rows, "ids_outside_pixels": page_ids, "ids_in_both": twice,
            "gtm_containers": overlap, "script_tags": script_tags(html), "app_blocks": app_blocks(html)}


def to_markdown(res):
    out = [f"## {res['source']}" + (f" (served from {res['final_url']})" if res.get("final_url") and res["final_url"] != res["source"] else ""), ""]
    if not res["is_shopify"]:
        out.append("No `webPixelsConfigList` found: not a Shopify storefront page, or the page was blocked or redirected.")
        return "\n".join(out) + "\n"
    t = res.get("theme") or {}
    if t:
        out += [f"Served by theme \"{t.get('name')}\" (id {t.get('id')}, role {t.get('role')}, {t.get('schema_name')} {t.get('schema_version')})", ""]
    if res.get("preview_warning"):
        out += [f"**Warning: {res['preview_warning']}**", ""]
    out += ["| Vendor | Type | Sandbox | Waits for consent | Data sharing | Destination IDs | Google events |", "|---|---|---|---|---|---|---|"]
    for r in res["pixels"]:
        purposes = ", ".join(r["consent_purposes"]) or "none declared"
        out.append(f"| {r['vendor']} | {r['type']} | {r['sandbox']} | {purposes} | {r['data_sharing'] or '-'} | {', '.join(r['destination_ids']) or '-'} | {', '.join(r['google_events']) or '-'} |")
    out += ["", f"Tag IDs elsewhere in the page source: {', '.join(res['ids_outside_pixels']) or 'none'}"]
    if res["ids_in_both"]:
        out.append(f"**Same ID in a pixel and in page code: {', '.join(res['ids_in_both'])}. Check for double counting.**")
    for c, info in (res.get("gtm_containers") or {}).items():
        if "error" in info:
            out.append(f"GTM {c}: could not read gtm.js ({info['error']})")
        elif info["ids_also_in_pixels"]:
            out.append(f"**Same ID in a pixel and inside GTM {c} (live version {info['version']}): "
                       f"{', '.join(info['ids_also_in_pixels'])}. Second path: check which install point owns each event.**")
        else:
            out.append(f"GTM {c} (live version {info['version']}): no pixel destination ID inside it.")
    out.append(f"ScriptTags (store-wide, survive theme changes): {', '.join(res.get('script_tags') or []) or 'none'}")
    out.append(f"App blocks and embeds in this theme: {', '.join(res.get('app_blocks') or []) or 'none'}")
    custom = sum(1 for r in res["pixels"] if r["type"] == "CUSTOM" and r["app_id"] != "shopify-pixel")
    out.append(f"Custom pixels: {custom} (read their code in Settings > Customer events).")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="storefront URLs or saved .html files")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    ap.add_argument("--gtm", action="append", default=[], help="also compare with this GTM container (repeatable)")
    ap.add_argument("--no-gtm", action="store_true", help="do not read GTM containers' public gtm.js")
    a = ap.parse_args()
    results = []
    for src in a.sources:
        try:
            if re.match(r"https?://", src):
                final, html = fetch(src)
            else:
                final, html = None, open(src, encoding="utf-8", errors="ignore").read()
            results.append(analyse(src, html, final, a.gtm, not a.no_gtm))
        except Exception as exc:  # report and continue with the next source
            results.append({"source": src, "error": str(exc), "is_shopify": False, "pixels": [], "ids_outside_pixels": [], "ids_in_both": []})
    if a.json:
        text = json.dumps(results, indent=2)
    else:
        text = "\n".join(to_markdown(r) if "error" not in r else f"## {r['source']}\n\nError: {r['error']}\n" for r in results)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
