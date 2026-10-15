#!/usr/bin/env python3
"""Summarise a Google Tag Manager container export, or diff two of them.

Reads the JSON that GTM's Admin > Export Container produces (a published
version or a workspace). Standard library only. Read-only: it never changes
the export or talks to Google.

Usage:
  python gtm_export_summary.py EXPORT.json                 # markdown summary
  python gtm_export_summary.py EXPORT.json --json          # machine-readable
  python gtm_export_summary.py EXPORT.json --out notes.md
  python gtm_export_summary.py --diff OLD.json NEW.json    # what changed

The summary has five parts: container facts, destinations (IDs found),
tags, site dependencies (what the container needs from the website: link
text, URLs, hostnames, form behaviour, dataLayer events and keys, DOM
selectors, cookies, globals) and health flags (paused tags, orphan
triggers, unused variables, duplicate Google tags, missing consent
settings, Universal Analytics leftovers, unstable event ids, risky Custom
HTML). The site dependencies are the raw material for the dependency
register in ANALYTICS.md.
"""
import argparse
import json
import re
import sys

TAG_TYPES = {
    "googtag": "Google tag (GA4 / Ads config)",
    "gaawc": "GA4 configuration (legacy)",
    "gaawe": "GA4 event",
    "awct": "Google Ads conversion",
    "sp": "Google Ads remarketing",
    "gclidw": "Conversion linker",
    "awcc": "Google Ads calls from website",
    "awud": "Google Ads user-provided data",
    "flc": "Floodlight counter",
    "fls": "Floodlight sales",
    "ua": "Universal Analytics (retired 2024)",
    "html": "Custom HTML",
    "img": "Custom image",
    "baut": "Microsoft Advertising UET",
    "bzi": "LinkedIn Insight",
    "hjtc": "Hotjar",
    "twitter_website_tag": "X (Twitter) website tag",
    "cegg": "Crazy Egg",
    "pntr": "Pinterest",
}

TRIGGER_TYPES = {
    "PAGEVIEW": "Page view",
    "DOM_READY": "DOM ready",
    "WINDOW_LOADED": "Window loaded",
    "INIT": "Initialization",
    "CONSENT_INIT": "Consent initialization",
    "CUSTOM_EVENT": "Custom event",
    "CLICK": "All elements click",
    "LINK_CLICK": "Just links click",
    "FORM_SUBMISSION": "Form submission",
    "HISTORY_CHANGE": "History change",
    "ELEMENT_VISIBILITY": "Element visibility",
    "SCROLL_DEPTH": "Scroll depth",
    "TIMER": "Timer",
    "YOU_TUBE_VIDEO": "YouTube video",
    "JS_ERROR": "JavaScript error",
    "TRIGGER_GROUP": "Trigger group",
}

VARIABLE_TYPES = {
    "v": "Data layer variable",
    "jsm": "Custom JavaScript",
    "c": "Constant",
    "u": "URL",
    "k": "1st-party cookie",
    "j": "JavaScript variable",
    "d": "DOM element",
    "e": "Custom event",
    "f": "HTTP referrer",
    "aev": "Auto-event variable",
    "smm": "Lookup table",
    "remm": "RegEx table",
    "awec": "User-provided data",
    "gtes": "Google tag event settings",
    "gtcs": "Google tag config settings",
    "gas": "GA settings (Universal Analytics)",
    "vis": "Element visibility",
    "r": "Random number",
    "cid": "Container ID",
    "ctv": "Container version",
    "dbg": "Debug mode",
}

# Built-in variables that read the page, and what the site must keep stable
SITE_BUILTINS = {
    "Click Text": "visible text of the clicked element",
    "Click URL": "href of the clicked link",
    "Click Element": "the clicked DOM element",
    "Click Classes": "CSS classes of the clicked element",
    "Click ID": "id of the clicked element",
    "Click Target": "target attribute of the clicked link",
    "Form ID": "id of the submitted form",
    "Form Classes": "CSS classes of the submitted form",
    "Form Text": "text of the submitted form",
    "Form URL": "action URL of the submitted form",
    "Form Element": "the submitted form element",
    "Form Target": "target of the submitted form",
    "Page URL": "full page URL",
    "Page Path": "page path",
    "Page Hostname": "hostname the site is served on",
    "Referrer": "referring URL",
}

BUILTIN_TRIGGERS = {
    "2147479553": "All Pages (built-in)",
    "2147479573": "Initialization - All Pages (built-in)",
    "2147479572": "Consent Initialization - All Pages (built-in)",
}

GOOGLE_ID_RE = re.compile(r"\b(G-[A-Z0-9]{6,12}|GT-[A-Z0-9]{6,10}|AW-\d{6,12}|DC-\d{6,10}|GTM-[A-Z0-9]{5,9}|UA-\d{4,10}-\d{1,4})\b")
META_INIT_RE = re.compile(r"fbq\(\s*['\"]init['\"]\s*,\s*['\"](\d{10,20})['\"]")
TIKTOK_RE = re.compile(r"ttq\.load\(\s*['\"]([A-Z0-9]{15,25})['\"]")
CLARITY_RE = re.compile(r"clarity\.ms/tag/['\"]?\+?\s*['\"]?([a-z0-9]{8,12})|clarity['\"]\s*,\s*['\"]script['\"]\s*,\s*['\"]([a-z0-9]{8,12})['\"]")
SRC_RE = re.compile(r"(?:src\s*=\s*['\"]|\.src\s*=\s*['\"]|['\"])(https?:)?//([a-z0-9.-]+\.[a-z]{2,})(/[^'\"\s]*)?", re.I)


def load(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    cv = data.get("containerVersion") or data
    if "tag" not in cv and "container" not in cv:
        sys.exit(f"{path}: not a GTM container export (no containerVersion.tag)")
    return data, cv


def params(obj):
    """Flatten a GTM parameter list into {key: value}; lists and maps stay as JSON."""
    out = {}
    for p in obj.get("parameter", []) or []:
        key = p.get("key")
        if key is None:
            continue
        if "value" in p:
            out[key] = p["value"]
        elif "list" in p:
            out[key] = p["list"]
        elif "map" in p:
            out[key] = p["map"]
    return out


def template_names(cv):
    names = {}
    cid = cv.get("containerId") or (cv.get("container") or {}).get("containerId", "")
    for t in cv.get("customTemplate", []) or []:
        tid = t.get("templateId")
        names[f"cvt_{cid}_{tid}"] = t.get("name")
        gal = (t.get("galleryReference") or {}).get("galleryTemplateId")
        if gal:
            names[f"cvt_{gal}"] = t.get("name")
    return names


def tag_type_label(t, tmpl):
    typ = t.get("type", "")
    if typ in TAG_TYPES:
        return TAG_TYPES[typ]
    if typ.startswith("cvt_"):
        return f"Template: {tmpl.get(typ, typ)}"
    return typ


def condition_text(cond, var_index):
    p = {x.get("key"): x.get("value") for x in cond.get("parameter", [])}
    arg0, arg1 = p.get("arg0", ""), p.get("arg1", "")
    neg = " NOT" if str(p.get("negate", "")).lower() == "true" else ""
    case = " (ignore case)" if str(p.get("ignore_case", "")).lower() == "true" else ""
    return f"{arg0}{neg} {cond.get('type', '')} '{arg1}'{case}", arg0, arg1


def var_name(ref):
    m = re.fullmatch(r"\{\{(.+?)\}\}", (ref or "").strip())
    return m.group(1) if m else None


def summarise(cv):
    tmpl = template_names(cv)
    tags = cv.get("tag", []) or []
    triggers = cv.get("trigger", []) or []
    variables = cv.get("variable", []) or []
    trig_by_id = {t["triggerId"]: t for t in triggers}
    var_by_name = {v["name"]: v for v in variables}
    blob = json.dumps(cv)

    def trigger_label(tid):
        if tid in trig_by_id:
            return trig_by_id[tid].get("name")
        return BUILTIN_TRIGGERS.get(tid, f"built-in {tid}")

    def resolve(value):
        """Replace a {{Constant}} reference with its value; keep anything else."""
        vn = var_name(str(value))
        if vn and vn in var_by_name and var_by_name[vn].get("type") == "c":
            return params(var_by_name[vn]).get("value", value)
        return value

    # --- tags
    tag_rows = []
    used_triggers = set()
    for t in tags:
        fire = t.get("firingTriggerId", []) or []
        block = t.get("blockingTriggerId", []) or []
        used_triggers.update(fire)
        used_triggers.update(block)
        cs = t.get("consentSettings") or {}
        consent = cs.get("consentStatus", "NOT_SET")
        if consent == "NEEDED":
            types = [x.get("value") for x in ((cs.get("consentType") or {}).get("list") or [])]
            consent = "NEEDED: " + ",".join(filter(None, types))
        p = params(t)
        ids = sorted(set(GOOGLE_ID_RE.findall(json.dumps(t))))
        tag_rows.append({
            "id": t.get("tagId"),
            "name": t.get("name"),
            "type": tag_type_label(t, tmpl),
            "raw_type": t.get("type"),
            "paused": bool(t.get("paused")),
            "firing": [trigger_label(x) for x in fire],
            "blocking": [trigger_label(x) for x in block],
            "consent": consent,
            "ids": ids,
            "event_name": p.get("standardEventName") or p.get("eventName"),
            "sequenced": bool(t.get("setupTag") or t.get("teardownTag")),
        })

    # triggers referenced from trigger groups count as used
    for tr in triggers:
        if tr.get("type") == "TRIGGER_GROUP":
            for item in params(tr).get("triggerIds", []) or []:
                if isinstance(item, dict) and item.get("value"):
                    used_triggers.add(item["value"])

    # --- destinations
    destinations = {"google": sorted(set(GOOGLE_ID_RE.findall(blob)))}
    html_text = " ".join(str(params(t).get("html", "")) for t in tags if t.get("type") == "html")
    def template_ids(word):
        found = set()
        for t in tags:
            label = tag_type_label(t, tmpl).lower()
            if word in label and params(t).get("pixelId"):
                for part in re.split(r"[,\s]+", str(resolve(params(t)["pixelId"]))):
                    if part:
                        found.add(part)
        return found
    destinations["meta_pixel"] = sorted(set(META_INIT_RE.findall(html_text)) | template_ids("meta") | template_ids("facebook"))
    destinations["tiktok"] = sorted(set(TIKTOK_RE.findall(html_text)) | template_ids("tiktok"))
    clarity = set()
    for a, b in CLARITY_RE.findall(html_text):
        clarity.add(a or b)
    destinations["clarity"] = sorted(clarity)
    html_domains = {}
    for t in tags:
        if t.get("type") != "html":
            continue
        doms = sorted({m[1].lower() for m in SRC_RE.findall(str(params(t).get("html", "")))})
        html_domains[t.get("name")] = doms
    destinations["custom_html_domains"] = html_domains

    # --- site dependencies
    deps = []

    def add_dep(kind, what, detail, trig, users):
        deps.append({"kind": kind, "what": what, "detail": detail, "trigger": trig, "used_by": users})

    users_of = {}
    for row in tag_rows:
        for name in row["firing"]:
            users_of.setdefault(name, []).append(row["name"] + (" (paused)" if row["paused"] else ""))

    for tr in triggers:
        name = tr.get("name")
        users = users_of.get(name, [])
        ttype = tr.get("type")
        if ttype == "LINK_CLICK":
            add_dep("markup", "Links must be real <a href> elements", "Just Links trigger only sees anchors", name, users)
        if ttype == "FORM_SUBMISSION":
            add_dep("forms", "Form must fire a native submit event", "intercepted or JS-only submits are invisible", name, users)
        if ttype == "ELEMENT_VISIBILITY":
            p = params(tr)
            sel = p.get("elementSelector") or p.get("elementId")
            add_dep("dom", f"Element must exist: {sel}", f"selection method {p.get('selectionMethod', '')}", name, users)
        if ttype == "HISTORY_CHANGE":
            add_dep("navigation", "Site changes URL with the History API", "single-page navigation", name, users)
        for cond in tr.get("customEventFilter", []) or []:
            text, arg0, arg1 = condition_text(cond, var_by_name)
            if arg0 == "{{_event}}":
                add_dep("dataLayer event", f"dataLayer.push({{event: '{arg1}'}})", f"custom event {cond.get('type')}", name, users)
        for key in ("filter", "autoEventFilter"):
            for cond in tr.get(key, []) or []:
                text, arg0, arg1 = condition_text(cond, var_by_name)
                vn = var_name(arg0)
                if vn in SITE_BUILTINS:
                    add_dep("page", f"{vn}: {SITE_BUILTINS[vn]}", text, name, users)
                elif vn and vn in var_by_name:
                    v = var_by_name[vn]
                    vp = params(v)
                    vt = v.get("type")
                    if vt == "v":
                        add_dep("dataLayer key", f"dataLayer key '{vp.get('name')}'", text, name, users)
                    elif vt == "d":
                        add_dep("dom", f"DOM element {vp.get('elementSelector') or vp.get('elementId')}", text, name, users)
                    elif vt == "k":
                        add_dep("cookie", f"cookie '{vp.get('name')}'", text, name, users)
                    elif vt == "j":
                        add_dep("global", f"window.{vp.get('name')}", text, name, users)
                    elif vt == "u":
                        add_dep("page", f"URL component {vp.get('component', 'URL')}", text, name, users)
                    elif vt == "jsm":
                        add_dep("custom js", f"Custom JS variable '{vn}'", text, name, users)

    # variables that read the page even when used outside triggers
    var_reads = []
    for v in variables:
        vp = params(v)
        vt = v.get("type")
        if vt == "v":
            var_reads.append(("dataLayer key", vp.get("name"), v["name"]))
        elif vt == "d":
            var_reads.append(("DOM element", vp.get("elementSelector") or vp.get("elementId"), v["name"]))
        elif vt == "k":
            var_reads.append(("cookie", vp.get("name"), v["name"]))
        elif vt == "j":
            var_reads.append(("JS global", vp.get("name"), v["name"]))

    # --- health flags
    flags = []
    for row in tag_rows:
        if row["paused"]:
            flags.append(("paused tag", row["name"], "paused tags still ship in the container; remove if no longer needed"))
        elif not row["firing"] and not row["sequenced"]:
            flags.append(("tag without trigger", row["name"], "never fires unless sequenced"))
        if row["raw_type"] == "ua" or any(i.startswith("UA-") for i in row["ids"]):
            flags.append(("Universal Analytics", row["name"], "UA stopped processing in 2024; dead weight"))
    for tr in triggers:
        if tr["triggerId"] not in used_triggers:
            flags.append(("trigger without tag", tr.get("name"), "unused; confirm intent or delete"))
    for v in variables:
        ref = "{{" + v["name"] + "}}"
        if blob.count(ref) == 0:
            flags.append(("unused variable", v["name"], VARIABLE_TYPES.get(v.get("type"), v.get("type"))))
        if v.get("type") == "jsm":
            code = str(params(v).get("javascript", ""))
            if re.search(r"Math\.random|Date\.now|new Date\(\)\.getTime", code):
                flags.append(("unstable value", v["name"], "Custom JS returns a new random/time value each read; as an event_id it breaks browser/server dedup"))
    google_cfg = {}
    for row in tag_rows:
        if row["raw_type"] in ("googtag", "gaawc") and not row["paused"]:
            t = next(x for x in tags if x.get("tagId") == row["id"])
            tid = params(t).get("tagId") or params(t).get("measurementId") or ""
            resolved = tid
            vn = var_name(tid)
            if vn and vn in var_by_name:
                resolved = params(var_by_name[vn]).get("value", tid)
            google_cfg.setdefault(resolved, []).append(f"{row['name']} [{', '.join(row['firing']) or 'no trigger'}]")
    for tid, rows in google_cfg.items():
        if len(rows) > 1:
            flags.append(("same Google tag configured twice", tid, "; ".join(rows) + " (check triggers do not overlap)"))
    not_set = sum(1 for r in tag_rows if r["consent"] == "NOT_SET")
    if not_set:
        flags.append(("consent settings", f"{not_set} of {len(tag_rows)} tags", "consentStatus NOT_SET (no additional consent check in GTM; fine only if consent mode or the CMP gates them)"))
    for t in tags:
        if t.get("type") != "html":
            continue
        code = str(params(t).get("html", ""))
        risky = [w for w, pat in (("document.write", r"document\.write"), ("eval", r"\beval\("),
                                   ("redirect", r"location\.(href|replace|assign)"), ("sync script", r"<script[^>]+src=(?![^>]*async)"))
                 if re.search(pat, code)]
        if risky:
            flags.append(("Custom HTML risk", t.get("name"), ", ".join(risky)))

    meta = {
        "publicId": (cv.get("container") or {}).get("publicId"),
        "container_name": (cv.get("container") or {}).get("name"),
        "version_id": cv.get("containerVersionId"),
        "version_name": cv.get("name"),
        "counts": {"tags": len(tags), "paused": sum(r["paused"] for r in tag_rows),
                   "triggers": len(triggers), "variables": len(variables),
                   "custom_templates": len(cv.get("customTemplate", []) or [])},
    }
    return {"meta": meta, "destinations": destinations, "tags": tag_rows,
            "dependencies": deps, "variable_reads": var_reads, "flags": flags}


def md_escape(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def to_markdown(s, export_time=None):
    m = s["meta"]
    out = [f"# GTM container {m['publicId']} \"{m['container_name']}\"", ""]
    out.append(f"Version {m['version_id'] if m['version_id'] not in (None, '0') else 'workspace'} \"{m['version_name'] or ''}\"" + (f", exported {export_time}" if export_time else ""))
    c = m["counts"]
    out.append(f"{c['tags']} tags ({c['paused']} paused), {c['triggers']} triggers, {c['variables']} variables, {c['custom_templates']} custom templates.")
    out += ["", "## Destinations", ""]
    d = s["destinations"]
    out.append(f"- Google IDs: {', '.join(d['google']) or 'none'}")
    out.append(f"- Meta pixel: {', '.join(d['meta_pixel']) or 'none found'}")
    out.append(f"- TikTok: {', '.join(d['tiktok']) or 'none found'}")
    out.append(f"- Clarity: {', '.join(d['clarity']) or 'none found'}")
    for name, doms in d["custom_html_domains"].items():
        if doms:
            out.append(f"- Custom HTML \"{name}\" loads from: {', '.join(doms)}")
    out += ["", "## Tags", "", "| ID | Name | Type | Status | Fires on | Consent | IDs / event |", "|---|---|---|---|---|---|---|"]
    for r in s["tags"]:
        status = "paused" if r["paused"] else "live"
        extra = ", ".join(r["ids"]) + (f" event={r['event_name']}" if r["event_name"] else "")
        out.append(f"| {r['id']} | {md_escape(r['name'])} | {md_escape(r['type'])} | {status} | {md_escape(', '.join(r['firing']) or '-')} | {r['consent']} | {md_escape(extra)} |")
    out += ["", "## Site dependencies (what the website must keep providing)", "",
            "| Kind | Dependency | Condition | Trigger | Used by |", "|---|---|---|---|---|"]
    for dep in s["dependencies"]:
        out.append(f"| {dep['kind']} | {md_escape(dep['what'])} | {md_escape(dep['detail'])} | {md_escape(dep['trigger'])} | {md_escape(', '.join(dep['used_by']) or 'no tag')} |")
    if s["variable_reads"]:
        out += ["", "Variables that read the page:", ""]
        for kind, what, name in s["variable_reads"]:
            out.append(f"- {kind} `{what}` (variable \"{name}\")")
    out += ["", "## Health flags", "", "| Flag | Item | Note |", "|---|---|---|"]
    for f, item, note in s["flags"]:
        out.append(f"| {f} | {md_escape(item)} | {md_escape(note)} |")
    return "\n".join(out) + "\n"


def index(cv):
    def strip(o):
        return {k: v for k, v in o.items() if k not in ("fingerprint", "accountId", "containerId", "path", "tagManagerUrl")}
    return {
        "tag": {t.get("name"): strip(t) for t in cv.get("tag", []) or []},
        "trigger": {t.get("name"): strip(t) for t in cv.get("trigger", []) or []},
        "variable": {t.get("name"): strip(t) for t in cv.get("variable", []) or []},
    }


def diff(old_path, new_path):
    od, ocv = load(old_path)
    nd, ncv = load(new_path)
    oi, ni = index(ocv), index(ncv)
    lines = [f"# GTM diff: v{ocv.get('containerVersionId') or 'workspace'} -> v{ncv.get('containerVersionId') or 'workspace'}", ""]
    lines.append(f"Old: {old_path} \"{ocv.get('name', '')}\" exported {od.get('exportTime', '?')}")
    lines.append(f"New: {new_path} \"{ncv.get('name', '')}\" exported {nd.get('exportTime', '?')}")
    total = 0
    for kind in ("tag", "trigger", "variable"):
        added = sorted(set(ni[kind]) - set(oi[kind]))
        removed = sorted(set(oi[kind]) - set(ni[kind]))
        changed = []
        for name in sorted(set(oi[kind]) & set(ni[kind])):
            a, b = oi[kind][name], ni[kind][name]
            if a != b:
                keys = sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))
                changed.append((name, keys))
        total += len(added) + len(removed) + len(changed)
        lines += ["", f"## {kind.title()}s: {len(added)} added, {len(removed)} removed, {len(changed)} changed", ""]
        for n in added:
            lines.append(f"- added: {n}")
        for n in removed:
            lines.append(f"- removed: {n}")
        for n, keys in changed:
            lines.append(f"- changed: {n} ({', '.join(keys)})")
    lines += ["", f"{total} differences. Re-check every dependency-register row whose trigger or tag is listed above."]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", nargs="?", help="GTM container export JSON")
    ap.add_argument("--json", action="store_true", help="print JSON instead of markdown")
    ap.add_argument("--out", help="write to this file instead of stdout")
    ap.add_argument("--diff", nargs=2, metavar=("OLD", "NEW"), help="compare two exports")
    a = ap.parse_args()
    if a.diff:
        text = diff(*a.diff)
    elif a.export:
        data, cv = load(a.export)
        s = summarise(cv)
        text = json.dumps(s, indent=2) if a.json else to_markdown(s, data.get("exportTime"))
    else:
        ap.error("give an export file or --diff OLD NEW")
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
