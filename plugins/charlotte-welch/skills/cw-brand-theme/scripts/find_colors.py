#!/usr/bin/env python3
"""List every hex colour a Shopify theme's settings and JSON templates use, with its JSON path.

  python find_colors.py <theme-folder> [--palette "#152E38,#111B18,#c93d0d,#ffffff"] [--json]

Reads config/settings_data.json (the `current` settings), templates/*.json and sections/*.json. Marks colours not in
the palette (case-insensitive; also flags gradients containing off-palette stops). Standard library only.
"""
import json
import re
import sys
from pathlib import Path

HEX = re.compile(r"#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
COMMENT = re.compile(r"^\s*/\*.*?\*/", re.S)


def load(p: Path):
    text = p.read_text(encoding="utf-8-sig")
    return json.loads(COMMENT.sub("", text, count=1))


def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, f"{path}.{k}" if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", out)
    elif isinstance(node, str):
        for m in HEX.findall(node):
            out.append((path, m, node if len(node) < 120 else node[:117] + "..."))


def norm(h):
    h = h.lower().lstrip("#")
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    root = Path(argv[0])
    palette = set()
    if "--palette" in argv:
        palette = {norm(x.strip()) for x in argv[argv.index("--palette") + 1].split(",") if x.strip()}
    as_json = "--json" in argv
    files = [root / "config" / "settings_data.json"] + sorted((root / "templates").glob("*.json")) + sorted((root / "sections").glob("*.json"))
    rows = []
    for f in files:
        if not f.is_file():
            continue
        data = load(f)
        if f.name == "settings_data.json" and isinstance(data.get("current"), dict):
            data = {"current": data["current"]}
        found = []
        walk(data, "", found)
        rel = f.relative_to(root).as_posix()
        for path, color, raw in found:
            rows.append({"file": rel, "path": path, "color": norm(color), "raw": raw,
                         "in_palette": (norm(color) in palette) if palette else None})
    if as_json:
        print(json.dumps(rows, indent=1))
        return
    off = 0
    for r in rows:
        mark = "" if r["in_palette"] is None else ("  " if r["in_palette"] else "! ")
        off += 1 if r["in_palette"] is False else 0
        print(f"{mark}{r['color']}  {r['file']} :: {r['path']}")
    if palette:
        print(f"\n{len(rows)} colour uses, {off} off-palette (marked !)")
        counts = {}
        for r in rows:
            if r["in_palette"] is False:
                counts[r["color"]] = counts.get(r["color"], 0) + 1
        for c, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f"  {c}  x{n}")


if __name__ == "__main__":
    main(sys.argv[1:])
