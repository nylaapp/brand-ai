#!/usr/bin/env python3
"""Build a campaign landing-page template whose parts swap with one switch.

Reads the theme's own sections, takes a small spec, and writes templates/page.campaign-<slug>.json
(plain JSON) with one ACTIVE section per region and, under it, the ready alternates switched off
("disabled": true). In the theme editor the owner swaps a part with the eye icon; through Claude,
"swap the hero for the video one" flips two flags. Prints the swap map to paste into the plan.

Usage:
  python build_template.py --theme <theme-folder> --slug black-friday --spec spec.json [--dry-run]
  python build_template.py --theme <theme-folder> --slug black-friday --list      # sections you can use
  python build_template.py --theme <theme-folder> --swap hero_b --slug black-friday   # swap by id

spec.json:
{
  "regions": [
    {"region": "hero", "label": "Hero",
     "options": [
       {"id": "hero_a", "type": "hero-image", "settings": {"heading": "35% off Cousin Walk"}},
       {"id": "hero_b", "type": "hero-video", "settings": {"heading": "35% off Cousin Walk"}}
     ]},
    {"region": "products", "label": "Products",
     "options": [{"id": "products_a", "type": "featured-collection", "settings": {}}]}
  ]
}
The first option of a region is on. Each section starts from its first preset in the theme (so a hero keeps its
heading and button blocks); put copy in "blocks": {"text_1": {"type": "text", "settings": {"text": "..."}}}
(block ids matching the preset's replace its copy), add a "label" ("video hero") for the swap map, or
"preset": false to start empty. Block types and their settings are checked against blocks/ and the schema.

Checks before writing: every type exists in sections/, every setting id is in that section's schema,
numbers sit inside min/max/step, ids are unique. Exits 2 with the reason on a bad spec. Standard
library only. Never touches the live theme: point --theme at a preview copy.
"""
import argparse
import json
import os
import re
import sys


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(2)


def schema_of(theme, stype):
    path = os.path.join(theme, "sections", stype + ".liquid")
    if not os.path.isfile(path):
        return None
    text = open(path, encoding="utf-8").read()
    m = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(1))
    except ValueError:
        return {}


def block_schema(theme, schema, btype):
    """Settings of a block type: the theme's blocks/<type>.liquid, else declared inline in the section."""
    path = os.path.join(theme, "blocks", btype + ".liquid")
    if os.path.isfile(path):
        text = open(path, encoding="utf-8").read()
        m = re.search(r"\{%-?\s*schema\s*-?%\}(.*?)\{%-?\s*endschema\s*-?%\}", text, re.S)
        try:
            return json.loads(m.group(1)) if m else {}
        except ValueError:
            return {}
    for b in schema.get("blocks", []):
        if b.get("type") == btype and "settings" in b:
            return b
    return None


def block_allowed(schema, btype):
    allowed = [b.get("type") for b in schema.get("blocks", [])]
    return not allowed or btype in allowed or "@theme" in allowed or btype.startswith("_")


def settings_by_id(schema):
    return {s["id"]: s for s in schema.get("settings", []) if "id" in s}


def check_setting(sid, value, defn, where):
    if defn is None:
        fail(f"{where}: setting '{sid}' is not in the section's schema")
    if isinstance(value, (int, float)) and not isinstance(value, bool) and defn.get("type") in ("range", "number"):
        lo, hi, st = defn.get("min"), defn.get("max"), defn.get("step", 1)
        if lo is not None and value < lo or hi is not None and value > hi:
            fail(f"{where}: '{sid}' = {value} is outside {lo} to {hi}")
        if lo is not None and st and defn.get("type") == "range" and (value - lo) % st:
            fail(f"{where}: '{sid}' = {value} is not on the step {st} (from {lo})")
    if defn.get("type") == "select":
        allowed = [o.get("value") for o in defn.get("options", [])]
        if allowed and value not in allowed:
            fail(f"{where}: '{sid}' = {value!r} is not one of {allowed}")


def list_sections(theme):
    d = os.path.join(theme, "sections")
    if not os.path.isdir(d):
        fail(f"no sections/ folder in {theme}")
    for f in sorted(os.listdir(d)):
        if f.endswith(".liquid"):
            sch = schema_of(theme, f[:-7])
            name = sch.get("name", "") if sch else ""
            ids = ", ".join(list(settings_by_id(sch))[:8]) if sch else ""
            print(f"{f[:-7]:32} {name:28} {ids}")


def swap(path, target):
    data = json.load(open(path, encoding="utf-8"))
    secs = data["sections"]
    if target not in secs:
        fail(f"no section '{target}' in {path}")
    region = target.rsplit("_", 1)[0]  # ids are <region>_<letter>: hero_a, hero_b
    group = [k for k in secs if k.rsplit("_", 1)[0] == region]
    for k in group:
        if k == target:
            secs[k].pop("disabled", None)
        else:
            secs[k]["disabled"] = True
    json.dump(data, open(path, "w", encoding="utf-8"), indent=2)
    print(f"on: {target}   off: {', '.join(k for k in group if k != target)}")


def main():
    ap = argparse.ArgumentParser(description="Build a swappable campaign landing-page template.")
    ap.add_argument("--theme", required=True, help="theme folder (a preview copy, never the live theme)")
    ap.add_argument("--slug", help="campaign slug, e.g. black-friday")
    ap.add_argument("--spec", help="JSON spec of regions and options")
    ap.add_argument("--list", action="store_true", help="list the theme's sections and exit")
    ap.add_argument("--swap", metavar="ID", help="turn this alternate on and its region's others off")
    ap.add_argument("--dry-run", action="store_true", help="validate and print, write nothing")
    a = ap.parse_args()

    if a.list:
        return list_sections(a.theme)
    if not a.slug:
        fail("give --slug")
    out = os.path.join(a.theme, "templates", f"page.campaign-{a.slug}.json")
    if a.swap:
        return swap(out, a.swap)
    if not a.spec:
        fail("give --spec (or --list, or --swap)")
    spec = json.load(open(a.spec, encoding="utf-8"))

    sections, order, seen, rows = {}, [], set(), []
    for reg in spec.get("regions", []):
        opts = reg.get("options") or []
        if not opts:
            fail(f"region '{reg.get('region')}' has no options")
        for i, o in enumerate(opts):
            sid, stype = o.get("id"), o.get("type")
            where = f"{reg.get('region')}/{sid}"
            if not sid or not re.fullmatch(r"[a-z0-9]+(_[a-z0-9]+)*_[a-z]", sid):
                fail(f"{where}: give each option an id like hero_a (region, underscore, a letter)")
            if sid in seen:
                fail(f"{where}: duplicate id")
            seen.add(sid)
            sch = schema_of(a.theme, stype or "")
            if sch is None:
                fail(f"{where}: the theme has no section '{stype}' (try --list)")
            defs = settings_by_id(sch)
            for k, v in (o.get("settings") or {}).items():
                check_setting(k, v, defs.get(k), where)
            # Start from the section's first preset (its blocks, e.g. a hero's heading and button), then
            # overlay the spec; "preset": false starts empty.
            presets = sch.get("presets") or []
            base = presets[0] if presets and o.get("preset", True) else {}
            sec = {"type": stype, "settings": {**(base.get("settings") or {}), **(o.get("settings") or {})}}
            blocks = {**(base.get("blocks") or {}), **(o.get("blocks") or {})}
            if blocks:
                for bid, b in blocks.items():
                    bt = b.get("type", "")
                    if not block_allowed(sch, bt):
                        fail(f"{where}: block '{bid}' of type '{bt}' is not allowed in '{stype}'")
                    bs = block_schema(a.theme, sch, bt)
                    if bs is None:
                        fail(f"{where}: block '{bid}': the theme has no block type '{bt}'")
                    if bid in (o.get("blocks") or {}):
                        bdefs = settings_by_id(bs)
                        for k, v in (b.get("settings") or {}).items():
                            check_setting(k, v, bdefs.get(k), f"{where}/{bid}")
                sec["blocks"] = blocks
                sec["block_order"] = o.get("block_order") or (base.get("block_order") if not o.get("blocks")
                                                              else list(blocks)) or list(blocks)
            if i > 0:
                sec["disabled"] = True
            sections[sid] = sec
            order.append(sid)
        label = reg.get("label") or reg["region"].title()
        names = {o["id"]: o.get("label") or o["id"] for o in opts}
        on, off = opts[0]["id"], [o["id"] for o in opts[1:]]
        rows.append((label, on, off, names))

    template = {"sections": sections, "order": order}
    print("| Part | On now | Alternates (off) | To swap |\n|---|---|---|---|")
    for label, on, off, names in rows:
        how = (f"Editor: eye icon on `{on}` and the alternate. Or say \"swap the {label.lower()} to the "
               f"{names[off[0]]}\"" if off else "Nothing to swap: one option")
        print(f"| {label} | {names[on]} (`{on}`) | "
              f"{', '.join(names[x] + ' (`' + x + '`)' for x in off) or 'none'} | {how} |")
    # Preset text is the theme's own placeholder ("t:html_defaults..." keys render as stock copy).
    stock = []
    for sid, sec in sections.items():
        for k, v in sec["settings"].items():
            if isinstance(v, str) and v.startswith("t:"):
                stock.append(f"{sid} {k}")
        for bid, b in (sec.get("blocks") or {}).items():
            for k, v in (b.get("settings") or {}).items():
                if isinstance(v, str) and v.startswith("t:"):
                    stock.append(f"{sid}/{bid} {k}")
    if stock:
        print("\nStill the theme's placeholder text (write your own or remove the block): " + "; ".join(stock))
    if a.dry_run:
        print("\n(dry run: nothing written)")
        return
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        print(f"note: replacing {out}", file=sys.stderr)
    json.dump(template, open(out, "w", encoding="utf-8"), indent=2)
    print(f"\nWrote {out}")


if __name__ == "__main__":
    main()
