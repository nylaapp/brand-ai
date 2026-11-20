#!/usr/bin/env python3
"""Read a Shopify theme folder and say what state its styling is in.

  python theme_state.py detect <theme-folder> [--design design.md]
  python theme_state.py gaps   <theme-folder> [--design design.md]

detect  -> verdict: "completed" (styles-builder already ran; the gap count then says whether anything needs
           refining), "fresh" (styling is still the theme's own
           defaults), "established" (a brand look is already set) or "ambiguous", with the evidence.
gaps    -> only for an established theme: what falls short, found by measuring, never by taste:
           contrast below 4.5:1, more font families than the brand names, line heights outside a
           readable range, uneven section padding, colours off the brand palette or near-duplicates,
           hardcoded fonts and colours in section code.

Read-only. Standard library only. Reads config/settings_schema.json, config/settings_data.json,
templates/*.json, sections/, snippets/, assets/. Exit 2 on a folder that is not a theme.
"""
import argparse
import glob
import json
import os
import re
import sys

HEX = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")
MARK = "styles-builder"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def load_json(path):
    """Theme JSON often starts with a /* ... */ header the editor writes."""
    try:
        text = open(path, encoding="utf-8").read()
    except OSError:
        return None
    text = re.sub(r"^\s*/\*.*?\*/", "", text, flags=re.S)
    try:
        return json.loads(text)
    except ValueError:
        return None


def norm(h):
    h = h.lower()
    return "#" + "".join(c * 2 for c in h[1:]) if len(h) == 4 else h


def rgb(h):
    h = norm(h)
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def lum(c):
    def f(v):
        v /= 255
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (f(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = lum(rgb(a)), lum(rgb(b))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(rgb(a), rgb(b))) ** 0.5


def theme_files(theme):
    sch = load_json(os.path.join(theme, "config", "settings_schema.json"))
    dat = load_json(os.path.join(theme, "config", "settings_data.json"))
    if not isinstance(sch, list) or not isinstance(dat, dict):
        fail(f"{theme} does not look like a theme (no config/settings_schema.json and settings_data.json)")
    cur = dat.get("current", dat)
    if not isinstance(cur, dict):  # "current" can name a preset
        cur = (dat.get("presets") or {}).get(cur, {})
    return sch, cur


def schema_settings(sch):
    for grp in sch:
        for s in grp.get("settings", []) if isinstance(grp, dict) else []:
            if isinstance(s, dict) and s.get("id"):
                yield s


STYLE_ID = re.compile(r"color|font|size|line_height|letter|radius|padding|spacing|gap|width|shadow|case|weight|"
                      r"palette|scheme", re.I)


def design_hexes(path):
    if not path or not os.path.isfile(path):
        return set()
    text = open(path, encoding="utf-8").read()
    return {norm(h) for h in re.findall(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b", text)}


def design_marker(paths):
    for p in paths:
        if p and os.path.isfile(p):
            m = re.search(r"^styles_built:\s*(.+)$", open(p, encoding="utf-8").read(), re.M)
            if m:
                return p, m.group(1).strip()
    return None, None


def find_design(theme, given):
    if given:
        return given
    for d in (theme, os.path.dirname(os.path.abspath(theme))):
        for n in ("design.md", "DESIGN.md"):
            if os.path.isfile(os.path.join(d, n)):
                return os.path.join(d, n)
    return None


def css_marker(theme):
    hits = []
    for p in glob.glob(os.path.join(theme, "assets", "*.css")) + glob.glob(os.path.join(theme, "assets", "*.liquid")):
        try:
            head = open(p, encoding="utf-8", errors="ignore").read(4000)
        except OSError:
            continue
        if MARK in head.lower() and "completed" in head.lower():
            hits.append(os.path.basename(p))
    return hits


def brand_css(theme):
    return [os.path.basename(p) for p in glob.glob(os.path.join(theme, "assets", "brand*"))
            + glob.glob(os.path.join(theme, "snippets", "brand*"))]


def custom_css_count(theme, cur):
    n = 0
    for k, v in cur.items():
        if "css" in k.lower() and isinstance(v, str) and v.strip():
            n += 1
    for p in glob.glob(os.path.join(theme, "templates", "*.json")) + glob.glob(os.path.join(theme, "sections", "*.json")):
        d = load_json(p) or {}
        for sec in (d.get("sections") or {}).values():
            for k, v in (sec.get("settings") or {}).items():
                if "css" in k.lower() and isinstance(v, str) and v.strip():
                    n += 1
    return n


def detect(theme, design_arg):
    sch, cur = theme_files(theme)
    design = find_design(theme, design_arg)
    total = changed = 0
    examples = []
    for s in schema_settings(sch):
        if not STYLE_ID.search(s["id"]) or s.get("type") in ("checkbox", "header", "paragraph", "image_picker"):
            continue
        if "default" not in s:
            continue
        total += 1
        v = cur.get(s["id"], s["default"])
        if v != s["default"]:
            changed += 1
            if len(examples) < 6:
                examples.append(f"{s['id']}: {s['default']!r} -> {v!r}")
    pct = round(100 * changed / total) if total else 0
    marker_file, marker = design_marker([design, os.path.join(theme, "design.md")])
    css_marks = css_marker(theme)
    bcss, ccss = brand_css(theme), custom_css_count(theme, cur)
    if marker or css_marks:
        verdict = "completed"
    elif pct < 10 and not bcss and ccss == 0:
        verdict = "fresh"
    elif pct >= 25 or bcss or ccss:
        verdict = "established"
    else:
        verdict = "ambiguous"
    out = {
        "verdict": verdict,
        "styling_settings_with_defaults": total,
        "changed_from_default": changed,
        "changed_percent": pct,
        "examples": examples,
        "brand_files_in_theme": bcss,
        "custom_css_settings_filled": ccss,
        "run_marker": {"design_md": marker, "file": marker_file, "css_files": css_marks},
        "design_md": design,
    }
    if verdict in ("completed", "established"):
        n = gap_count(gaps(theme, design_arg))
        out["gaps_found"] = n
        out["next"] = ("nothing to refine: built and consistent, change nothing" if n == 0 else
                       "show the gap table and ask which rows to fix") if verdict == "completed" else \
                      "established look: show the gap table and ask which rows to fix"
    elif verdict == "fresh":
        out["next"] = "not built yet: build everything"
    else:
        out["next"] = "ask one question: build everything or fill gaps only"
    print(json.dumps(out, indent=2))
    return out


def pairs_in(d, path=""):
    """Yield (label, background, text) from any dict holding both roles as hex strings."""
    if not isinstance(d, dict):
        return
    hexes = {k: norm(v) for k, v in d.items() if isinstance(v, str) and HEX.match(v)}
    for k, bg in hexes.items():
        m = re.match(r"^(.*?)(background(?:_color)?)$", k)
        if not m:
            continue
        pre = m.group(1)
        for tk in ("text", "text_color", "label", "foreground", "foreground_color"):
            if pre + tk in hexes:
                yield f"{path}{pre}{{background,{tk}}}".strip("."), bg, hexes[pre + tk]
    for k, v in d.items():
        if isinstance(v, dict):
            yield from pairs_in(v, f"{path}{k}.")


def gaps(theme, design_arg):
    sch, cur = theme_files(theme)
    design = find_design(theme, design_arg)
    palette = design_hexes(design)
    found = {}

    # 1. contrast
    low = []
    for label, bg, fg in pairs_in(cur):
        r = ratio(bg, fg)
        if r < 4.5:
            low.append({"where": label, "ratio": round(r, 2), "background": bg, "text": fg,
                        "fails": "even large text" if r < 3 else "body text"})
    pb, pt = cur.get("page_background_color"), cur.get("page_text_color")
    if isinstance(pb, str) and isinstance(pt, str) and HEX.match(pb) and HEX.match(pt) and ratio(pb, pt) < 4.5:
        low.append({"where": "page background and page text", "ratio": round(ratio(pb, pt), 2)})
    found["contrast_below_4_5"] = low

    # 2. fonts
    fams = {}
    for k, v in cur.items():
        if "font" in k and isinstance(v, str) and re.match(r"^[a-z0-9_]+_[ni]\d$", v):
            fams.setdefault(re.sub(r"_[ni]\d$", "", v), []).append(k)
    found["font_families_in_settings"] = {f: ks for f, ks in fams.items()}
    found["font_family_count"] = len(fams)

    # 3. line height
    lh = []
    for k, v in cur.items():
        if "line_height" in k:
            try:
                x = float(v)
            except (TypeError, ValueError):
                continue
            body = "paragraph" in k or "body" in k
            lo, hi = (1.4, 1.8) if body else (1.0, 1.4)
            if x < lo or x > hi:
                lh.append({"setting": k, "value": x, "readable_range": f"{lo} to {hi}"})
    found["line_height_outside_range"] = lh

    # 4. section spacing
    pads = {}
    for p in glob.glob(os.path.join(theme, "templates", "*.json")):
        d = load_json(p) or {}
        for sid, sec in (d.get("sections") or {}).items():
            for k, v in (sec.get("settings") or {}).items():
                if k.startswith("padding-block") or k in ("section_padding_top", "section_padding_bottom"):
                    if isinstance(v, (int, float)):
                        pads.setdefault(k, {}).setdefault(v, []).append(f"{os.path.basename(p)}:{sid}")
    spacing = {}
    for k, vals in pads.items():
        if len(vals) > 4:
            common = max(vals, key=lambda x: len(vals[x]))
            spacing[k] = {"distinct_values": sorted(vals), "most_common": common,
                          "odd_ones": {str(v): ids[:4] for v, ids in vals.items() if v != common and len(ids) <= 2}}
    found["uneven_section_padding"] = spacing

    # 5. colours: off palette and near duplicates
    used = {}

    def walk(x, path):
        if isinstance(x, str) and HEX.match(x):
            used.setdefault(norm(x), []).append(path)
        elif isinstance(x, dict):
            for k, v in x.items():
                walk(v, f"{path}.{k}" if path else k)
    walk(cur, "")
    if palette:
        off = []
        for h, where in used.items():
            if h in palette or h in ("#ffffff", "#000000"):
                continue
            near = min(palette, key=lambda p: dist(h, p))
            off.append({"colour": h, "nearest_in_design_md": near, "distance": round(dist(h, near)),
                        "used_in": where[:3]})
        found["colours_not_in_design_md"] = sorted(off, key=lambda o: o["distance"])[:20]
    else:
        found["colours_not_in_design_md"] = "no design.md palette found to compare against"
    hs = sorted(used)
    dup = [{"a": a, "b": b, "distance": round(dist(a, b))} for i, a in enumerate(hs) for b in hs[i + 1:]
           if 0 < dist(a, b) < 14]
    found["near_duplicate_colours"] = dup[:15]

    # 6. hardcoded values in section code
    hard = []
    for p in glob.glob(os.path.join(theme, "sections", "*.liquid")) + glob.glob(os.path.join(theme, "snippets", "*.liquid")):
        if os.path.basename(p).startswith("brand"):
            continue  # the brand layer is where fonts and colours are meant to be written out
        text = open(p, encoding="utf-8", errors="ignore").read()
        text = re.sub(r"\{%-?\s*schema.*?endschema\s*-?%\}", "", text, flags=re.S)
        f = len(re.findall(r"font-family\s*:\s*(?!var\()[^;}]+", text))
        c = len(re.findall(r"(?<![\w&])#[0-9a-fA-F]{6}\b", text))
        if f or c > 3:
            hard.append({"file": os.path.relpath(p, theme), "hardcoded_font_families": f, "hardcoded_hex_colours": c})
    found["hardcoded_in_section_code"] = sorted(hard, key=lambda h: -(h["hardcoded_font_families"] * 5
                                                                       + h["hardcoded_hex_colours"]))[:12]
    return found


def gap_count(found):
    """Hard, measured gaps only. Uneven padding and hardcoded values in the starting theme's own code are
    review items: reported, never counted, because a stock theme has both and they are not the brand's fault."""
    n = len(found["contrast_below_4_5"]) + len(found["line_height_outside_range"]) + len(found["near_duplicate_colours"])
    cn = found["colours_not_in_design_md"]
    n += len(cn) if isinstance(cn, list) else 0
    n += 1 if found["font_family_count"] > 3 else 0
    return n


def main():
    ap = argparse.ArgumentParser(description="Detect a theme's styling state and find its gaps.")
    ap.add_argument("mode", choices=["detect", "gaps"])
    ap.add_argument("theme")
    ap.add_argument("--design", help="path to design.md (found next to or above the theme if omitted)")
    a = ap.parse_args()
    if not os.path.isdir(a.theme):
        fail(f"no folder {a.theme}")
    if a.mode == "gaps":
        print(json.dumps(gaps(a.theme, a.design), indent=2))
        return
    out = detect(a.theme, a.design)


if __name__ == "__main__":
    main()
