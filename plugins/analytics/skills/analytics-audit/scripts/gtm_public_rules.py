#!/usr/bin/env python3
"""Map every tag in a live GTM container to its firing conditions, from the public gtm.js.

Every visitor downloads the published container as gtm.js. Its compiled
"resource" block holds the tags, the variables and the rules that fire or
block them, so it shows what the LIVE container does even when the container
export is missing or older than the live version:

- tag type and tag number (the same numbers as `tagId` in an export),
- paused tags, event names and destination IDs (GA4, Google Ads, Meta,
  TikTok, Clarity, Hotjar, hosts loaded by Custom HTML),
- the conditions each tag fires and is blocked on: dataLayer events and keys,
  page URLs, paths and hostnames, click text and URL (CTA wording, booking
  hosts, regexes), listener triggers by trigger number.

Tag, trigger and variable NAMES are not in gtm.js; numbers are. Paused tags
keep their conditions but lose their settings. The compiled format is
undocumented: treat the result as strong evidence of what is live, and confirm
details with an export when you can get one.

Usage:
  python gtm_public_rules.py GTM-XXXXXXX                 # fetch the live container
  python gtm_public_rules.py GTM-XXXXXXX --ids           # destination IDs only (multi-path check)
  python gtm_public_rules.py saved-gtm.js --json         # from a saved file, machine-readable
  python gtm_public_rules.py GTM-XXXXXXX --out rules.md

Standard library only. Reads one public file; no sign-in, nothing is changed.
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
GOOGLE_ID_RE = re.compile(r"\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|DC-\d{6,10}|UA-\d{4,10}-\d{1,4})\b")
# GTM minifies Custom HTML (`fbq("init", ...)` can become `a("init", ...)`), so match the call shape.
META_INIT_RE = re.compile(r"['\"]init['\"]\s*,\s*['\"](\d{10,20})['\"]")
TIKTOK_RE = re.compile(r"\.load\(\s*['\"](C[A-Z0-9]{15,25})['\"]")
CLARITY_RE = re.compile(r"clarity\.ms/tag/([a-z0-9]{8,12})|['\"]clarity['\"]\s*,\s*['\"]script['\"]\s*,\s*['\"]([a-z0-9]{8,12})['\"]")
HOTJAR_RE = re.compile(r"hjid\s*:\s*(\d{5,9})")
HOST_RE = re.compile(r"(?:https?:)?//([a-z0-9-]+(?:\.[a-z0-9-]+)+\.[a-z]{2,})(?=[/'\"?:])", re.I)
REDIRECT_RE = re.compile(r"\blocation(?:\.(?:href|pathname|search|host|hostname|protocol|port))?\s*=(?!=)|\blocation\.(?:replace|assign)\s*\(")
PUSH_RE = re.compile(r"dataLayer\.push\(\s*\{[^}]*?['\"]?event['\"]?\s*:\s*['\"]([^'\"]+)['\"]")

TAG_TYPES = {
    "__googtag": "Google tag", "__gaawe": "GA4 event", "__gaawc": "GA4 config (legacy)",
    "__awct": "Google Ads conversion", "__sp": "Google Ads remarketing", "__gclidw": "Conversion linker",
    "__awcc": "Google Ads calls from website", "__awud": "Google Ads user-provided data",
    "__flc": "Floodlight counter", "__fls": "Floodlight sales", "__ua": "Universal Analytics (retired 2024)",
    "__html": "Custom HTML", "__img": "Custom image", "__baut": "Microsoft UET", "__bzi": "LinkedIn Insight",
    "__hjtc": "Hotjar", "__cegg": "Crazy Egg", "__pntr": "Pinterest", "__twitter_website_tag": "X (Twitter)",
}
LISTENERS = {
    "__lcl": "just links click", "__cl": "all elements click", "__fsl": "form submission",
    "__hl": "history change", "__sdl": "scroll depth", "__evl": "element visibility",
    "__tl": "timer", "__ytl": "YouTube video", "__jel": "JavaScript error",
}
EVENTS = {
    "gtm.js": "page view", "gtm.dom": "DOM ready", "gtm.load": "window loaded", "gtm.init": "initialization",
    "gtm.init_consent": "consent initialization", "gtm.click": "all elements click",
    "gtm.linkClick": "just links click", "gtm.formSubmit": "form submission", "gtm.historyChange": "history change",
    "gtm.historyChange-v2": "history change", "gtm.elementVisibility": "element visibility",
    "gtm.scrollDepth": "scroll depth", "gtm.timer": "timer", "gtm.video": "YouTube video",
}
OPS = {"_eq": "equals", "_cn": "contains", "_re": "matches regex", "_sw": "starts with", "_ew": "ends with",
       "_css": "matches CSS selector", "_lt": "<", "_le": "<=", "_gt": ">", "_ge": ">="}
URL_PARTS = {"URL": "Page URL", "PATH": "Page Path", "HOST": "Page Hostname", "QUERY": "Page Query",
             "FRAGMENT": "Page Fragment", "PROTOCOL": "Page Protocol", "PORT": "Page Port",
             "IS_OUTBOUND": "URL is outbound", "EXTENSION": "File extension"}
# Built-in variables that compile to dataLayer reads
GTM_KEYS = {"gtm.elementUrl": "Click/Form URL", "gtm.element": "Click/Form Element", "gtm.elementClasses": "Click/Form Classes",
            "gtm.elementId": "Click/Form ID", "gtm.elementTarget": "Click/Form Target", "gtm.uniqueEventId": "Event ID (per page)",
            "gtm.newUrl": "New History URL", "gtm.oldUrl": "Old History URL", "gtm.historyChangeSource": "History Source",
            "gtm.scrollThreshold": "Scroll Depth Threshold", "gtm.visibleRatio": "Percent Visible", "gtm.errorMessage": "Error Message"}
AEV_PARTS = {"TEXT": "Click/Form Text", "URL": "Click/Form URL", "ELEMENT": "Click/Form Element",
             "CLASSES": "Click/Form Classes", "ID": "Click/Form ID", "TARGET": "Click/Form Target",
             "TAG_NAME": "Click/Form Tag name", "ATTRIBUTE": "Click/Form attribute"}
VENDOR_HOSTS = [("connect.facebook.net", "Meta pixel"), ("analytics.tiktok.com", "TikTok"),
                ("clarity.ms", "Microsoft Clarity"), ("hotjar", "Hotjar"), ("bat.bing.com", "Microsoft UET"),
                ("s.pinimg.com", "Pinterest"), ("sc-static.net", "Snapchat"), ("redditstatic.com", "Reddit"),
                ("snap.licdn.com", "LinkedIn"), ("klaviyo", "Klaviyo"), ("callrail", "CallRail")]


def fetch(source):
    if re.fullmatch(r"GTM-[A-Z0-9]{4,10}", source, re.I):
        source = f"https://www.googletagmanager.com/gtm.js?id={source.upper()}"
    req = urllib.request.Request(source, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return source, resp.read().decode("utf-8", errors="ignore")


def extract(src):
    """Return the object that holds "resource" in a compiled gtm.js."""
    i = src.find('"resource"')
    if i < 0:
        sys.exit("no compiled \"resource\" block found: not a gtm.js file, or the format changed")
    start = src.rindex("{", 0, i)
    depth, in_str, esc = 0, False, False
    for k in range(start, len(src)):
        c = src[k]
        if in_str:
            if esc:
                esc = False
            elif c == "\\":
                esc = True
            elif c == '"':
                in_str = False
        elif c == '"':
            in_str = True
        elif c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(src[start:k + 1])
    sys.exit("could not find the end of the \"resource\" block")


class Container:
    def __init__(self, top):
        r = top["resource"]
        self.version = r.get("version")
        self.macros, self.tags = r.get("macros", []), r.get("tags", [])
        self.preds, self.rules = r.get("predicates", []), r.get("rules", [])
        self.template_vendor = {}
        for item in top.get("runtime", []) or []:  # custom templates: guess the vendor from the hosts they load
            if isinstance(item, list) and len(item) > 1 and isinstance(item[1], str) and item[1].startswith("__cvt"):
                code = json.dumps(item)
                self.template_vendor[item[1]] = next((v for h, v in VENDOR_HOSTS if h in code), None)

    # --- values
    def macro(self, n):
        m = self.macros[n] if 0 <= n < len(self.macros) else {}
        f = m.get("function", "?")
        if f == "__e":
            return "Event"
        if f == "__u":
            label = URL_PARTS.get(m.get("vtp_component") or "URL", m.get("vtp_component"))
            if m.get("vtp_queryKey"):
                label = f"Page Query {m['vtp_queryKey']}"
            if m.get("vtp_customUrlSource"):
                label += f" of {self.value(m['vtp_customUrlSource'])}"
            return label
        if f == "__aev":
            label = AEV_PARTS.get(m.get("vtp_varType"), f"auto-event {m.get('vtp_varType')}")
            return label + (f" [{m['vtp_attribute']}]" if m.get("vtp_attribute") else "")
        if f == "__v":
            name = m.get("vtp_name")
            return f"{GTM_KEYS[name]} ({name})" if name in GTM_KEYS else f"dataLayer.{name}"
        if f == "__c":
            return f"const \"{self.value(m.get('vtp_value'))}\""
        if f == "__k":
            return f"cookie {m.get('vtp_name')}"
        if f == "__j":
            return f"window.{m.get('vtp_name')}"
        if f == "__d":
            return f"DOM {m.get('vtp_elementSelector') or m.get('vtp_elementId')}"
        if f == "__f":
            return "Referrer"
        if f == "__smm":
            return f"lookup table #{n} on {self.value(m.get('vtp_input'))}"
        if f == "__remm":
            return f"regex table #{n} on {self.value(m.get('vtp_input'))}"
        names = {"__jsm": "custom JS", "__cid": "Container ID", "__ctv": "Container Version", "__r": "Random Number",
                 "__dbg": "Debug Mode", "__awec": "user-provided data", "__gtes": "event settings",
                 "__gtcs": "config settings", "__vis": "visibility"}
        return f"{names.get(f, f)} #{n}"

    def const(self, v):
        """Resolve a constant variable to its value; leave other values as rendered text."""
        if isinstance(v, list) and len(v) == 2 and v[0] == "macro" and isinstance(v[1], int):
            m = self.macros[v[1]] if v[1] < len(self.macros) else {}
            if m.get("function") == "__c":
                return self.const(m.get("vtp_value"))
        return self.value(v)

    def value(self, v):
        if isinstance(v, list) and v:
            kind = v[0]
            if kind == "macro":
                return "{{" + self.macro(v[1]) + "}}"
            if kind == "template":  # a string built from parts; constants are inlined
                return "".join(self.const(x) for x in v[1:])
            if kind == "escape":
                return self.value(v[1])
            if kind == "list":
                return "[" + ", ".join(self.value(x) for x in v[1:]) + "]"
            if kind == "map":
                return "{" + ", ".join(f"{self.value(v[i])}: {self.value(v[i + 1])}" for i in range(1, len(v) - 1, 2)) + "}"
            return json.dumps(v)
        return "" if v is None else str(v)

    def html(self, t):
        h = t.get("vtp_html")
        text = self.value(h) if isinstance(h, list) else (h or "")
        if text.startswith('"'):
            try:
                text = json.loads(text)
            except ValueError:
                pass
        return text

    # --- conditions
    def pred(self, n):
        p = self.preds[n]
        a0, a1 = p.get("arg0"), p.get("arg1")
        left = self.value(a0)
        if left == "{{dataLayer.gtm.triggers}}" and isinstance(a1, str):
            ids = re.findall(r"\d+_(\d+)", a1)  # "(^$|((^|,)<container>_<trigger>($|,)))"
            return f"listener for trigger {', '.join(ids)}"
        text = f"{left} {OPS.get(p.get('function'), p.get('function'))} \"{self.value(a1)}\""
        if p.get("ignore_case"):
            text += " (ignore case)"
        if left == "{{Event}}" and a1 in EVENTS:
            text += f" ({EVENTS[a1]})"
        return text

    def conditions(self):
        fires, blocks = {}, {}
        for rule in self.rules:
            conds = []
            for part in rule:
                if part[0] == "if":
                    conds += [self.pred(p) for p in part[1:]]
                elif part[0] == "unless":
                    conds += ["NOT " + self.pred(p) for p in part[1:]]
            conds.sort(key=lambda c: not c.startswith("{{Event}}"))  # the event first, then its filters
            for part in rule:
                if part[0] == "add":
                    for t in part[1:]:
                        fires.setdefault(t, []).append(conds)
                elif part[0] == "block":
                    for t in part[1:]:
                        blocks.setdefault(t, []).append(conds)
        return fires, blocks

    # --- tags
    def describe(self, t):
        f = t.get("function", "")
        details, ids, hosts = [], set(), set()
        if f == "__paused":
            orig = t.get("vtp_originalTagType", "?")
            label = f"PAUSED {TAG_TYPES.get('__' + orig, 'template ' + orig if orig.startswith('cvt') else orig)}"
        elif f in LISTENERS:
            trig = str(t.get("vtp_uniqueTriggerId", "")).split("_")[-1]
            label = f"listener: {LISTENERS[f]}" + (f" (trigger {trig})" if trig else "")
        elif f.startswith("__cvt"):
            label = f"template {f[2:]}" + (f" ({self.template_vendor[f]})" if self.template_vendor.get(f) else "")
        else:
            label = TAG_TYPES.get(f, f)
        if f == "__googtag":
            ids.add(self.const(t.get("vtp_tagId")))
            table = t.get("vtp_configSettingsTable")
            if isinstance(table, list):  # ["list", ["map", "parameter", k, "parameterValue", v], ...]
                for row in table[1:]:
                    kv = dict(zip(row[1::2], row[2::2])) if isinstance(row, list) else {}
                    if kv.get("parameter"):
                        details.append(f"{kv['parameter']}={self.const(kv.get('parameterValue'))}")
        if f == "__gaawe":
            details.append(f"event={self.value(t.get('vtp_eventName'))}")
            if t.get("vtp_measurementIdOverride"):
                ids.add(self.const(t["vtp_measurementIdOverride"]))
        if f in ("__awct", "__sp", "__awcc", "__awud") and t.get("vtp_conversionId"):
            cid = self.const(t["vtp_conversionId"])
            ids.add(cid if cid.startswith("AW-") else f"AW-{cid}")
            if t.get("vtp_conversionLabel"):
                details.append(f"label={self.const(t['vtp_conversionLabel'])}")
        if f == "__ua":
            details.append(t.get("vtp_trackType", "").replace("TRACK_", "").lower() or "ua")
            for key in ("vtp_eventCategory", "vtp_eventAction"):
                if t.get(key):
                    details.append(f"{key[10:].lower()}={self.value(t[key])}")
        if f.startswith("__cvt"):
            name = t.get("vtp_customEventName") if t.get("vtp_eventName") == "custom" else (
                t.get("vtp_standardEventName") or t.get("vtp_eventName"))
            if name:
                details.append(f"event={self.value(name)}")
            for key in ("vtp_pixelId", "vtp_pixel_code", "vtp_pixelCode", "vtp_tagId"):
                if t.get(key):
                    for part in re.split(r"[,\s]+", self.const(t[key])):
                        if part:
                            ids.add(part)
            if t.get("vtp_eventId"):
                details.append(f"event_id={self.value(t['vtp_eventId'])}")
        if f == "__html":
            code = self.html(t)
            ids.update(GOOGLE_ID_RE.findall(code))
            if "fbevents" in code or "fbq" in code:
                ids.update(META_INIT_RE.findall(code))
            if "tiktok" in code.lower():
                ids.update(TIKTOK_RE.findall(code))
            ids.update(a or b for a, b in CLARITY_RE.findall(code))
            ids.update(f"hjid {x}" for x in HOTJAR_RE.findall(code))
            hosts.update(h.lower() for h in HOST_RE.findall(code))
            hints = [v for k, v in (("fbevents", "Meta"), ("tiktok", "TikTok"), ("clarity", "Clarity"), ("callrail", "CallRail"),
                                    ("hotjar", "Hotjar"), ("replaceState", "rewrites the URL"), ("document.cookie", "cookies"))
                     if k.lower() in code.lower()]
            if REDIRECT_RE.search(code):
                hints.append("REDIRECTS")
            hints += [f"pushes {e}" for e in sorted(set(PUSH_RE.findall(code)))]
            if not hints and not hosts:
                hints.append(re.sub(r"\s+", " ", re.sub(r"<script[^>]*>", "", code))[:60].strip())
            details.append("; ".join(hints))
            if hosts:
                details.append("loads " + ", ".join(sorted(hosts)))
        for key in ("once_per_load", "priority"):
            if t.get(key):
                details.append(key.replace("_", " ") + ("" if t[key] is True else f" {t[key]}"))
        for key in ("setup_tags", "teardown_tags", "consent"):
            if key in t:
                details.append(f"{key}={self.value(t[key])}")
        ids.discard("")
        return {"tag_id": t.get("tag_id"), "type": label, "function": f, "paused": f == "__paused",
                "listener": f in LISTENERS, "details": [d for d in details if d], "ids": sorted(ids), "hosts": sorted(hosts)}

    def summary(self):
        fires, blocks = self.conditions()
        rows = []
        for i, t in enumerate(self.tags):
            row = self.describe(t)
            row["fires"] = fires.get(i, [])
            row["blocked"] = blocks.get(i, [])
            rows.append(row)
        rows.sort(key=lambda r: (r["listener"], int(r["tag_id"]) if str(r["tag_id"]).isdigit() else 0))
        ids = {"google": set(), "meta_pixel": set(), "tiktok": set(), "other": set()}
        for r in rows:
            for x in r["ids"]:
                if GOOGLE_ID_RE.fullmatch(x):
                    ids["google"].add(x)
                elif re.fullmatch(r"\d{10,20}", x):
                    ids["meta_pixel"].add(x)
                elif re.fullmatch(r"C[A-Z0-9]{15,25}", x):
                    ids["tiktok"].add(x)
                else:
                    ids["other"].add(x)
        consts = {self.const(m.get("vtp_value")) for m in self.macros if m.get("function") == "__c"}
        ids["google"].update(x for x in consts if GOOGLE_ID_RE.fullmatch(x))
        return {"version": self.version, "tags": rows, "ids": {k: sorted(v) for k, v in ids.items()},
                "hosts": sorted({h for r in rows for h in r["hosts"]})}


def to_markdown(s, source, fetched):
    rows = s["tags"]
    live = [r for r in rows if not r["paused"] and not r["listener"]]
    saved = fetched == "a saved copy"
    out = [f"# {source}: {'' if saved else 'live '}version {s['version']}", "",
           f"Read from {'a saved gtm.js' if saved else 'the public gtm.js on ' + fetched}. {len(rows)} compiled tags: {len(live)} live, "
           f"{sum(r['paused'] for r in rows)} paused, {sum(r['listener'] for r in rows)} listeners (auto-created for click, form "
           "and visibility triggers). Tag numbers match `tagId` in a container export; names are not in gtm.js.", "",
           "## Destination IDs", ""]
    labels = {"google": "Google", "meta_pixel": "Meta pixel", "tiktok": "TikTok", "other": "Other (Clarity, Hotjar, ...)"}
    for k, label in labels.items():
        out.append(f"- {label}: {', '.join(s['ids'][k]) or 'none found'}")
    out.append(f"- Hosts loaded by Custom HTML: {', '.join(s['hosts']) or 'none'}")
    out += ["", "## Tags and when they fire", ""]

    def cond_lines(sets, word):
        if not sets:
            return []
        lines = []
        for i, conds in enumerate(sets):
            lines.append(f"    {word if i == 0 else 'or':<8} " + (" AND ".join(conds) if conds else "(always)"))
        return lines

    for r in rows:
        if r["listener"]:
            continue
        head = f"[{r['tag_id']}] {r['type']}"
        if r["ids"]:
            head += "  " + ", ".join(r["ids"])
        if r["details"]:
            head += "  (" + "; ".join(r["details"]) + ")"
        out.append(head)
        out += cond_lines(r["fires"], "would fire" if r["paused"] else "fires") or [
            "    no rule: fired only through tag sequencing, or never"]
        out += cond_lines(r["blocked"], "blocked")
    listeners = [r for r in rows if r["listener"]]
    if listeners:
        out += ["", "## Listeners", ""]
        for r in listeners:
            out.append(f"[{r['tag_id']}] {r['type']}" + ("  when " + " | ".join(" AND ".join(c) for c in r["fires"]) if r["fires"] else ""))
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="GTM-XXXXXXX (fetches the live gtm.js), a gtm.js URL, or a saved gtm.js file")
    ap.add_argument("--ids", action="store_true", help="print only the destination IDs")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out")
    a = ap.parse_args()
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if re.match(r"https?://", a.source) or re.fullmatch(r"GTM-[A-Z0-9]{4,10}", a.source, re.I):
        url, src = fetch(a.source)
        m = re.search(r"id=(GTM-[A-Z0-9]+)", url, re.I)
        label = m.group(1).upper() if m else url
    else:
        src = open(a.source, encoding="utf-8", errors="ignore").read()
        m = re.search(r"\b(GTM-[A-Z0-9]{4,10})\b", src)
        label = (m.group(1) if m else a.source) + " (saved file)"
        fetched = "a saved copy"
    s = Container(extract(src)).summary()
    if a.json:
        text = json.dumps({"source": label, "fetched": fetched, **s}, indent=2)
    elif a.ids:
        text = f"{label} version {s['version']} ({fetched})\n" + "".join(
            f"{k}: {', '.join(v) or '-'}\n" for k, v in s["ids"].items())
    else:
        text = to_markdown(s, label, fetched)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
