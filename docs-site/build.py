#!/usr/bin/env python3
"""Build docs-site/dist/index.html from content.json, the marketplace and SKILL.md files.
Read-only on the rest of the repo."""
import json, pathlib, re, sys

here = pathlib.Path(__file__).resolve().parent
repo = here.parent
content = json.loads((here / "content.json").read_text())
market = json.loads((repo / ".claude-plugin" / "marketplace.json").read_text())
versions = {p["name"]: p.get("version", "") for p in market["plugins"]}
descs = {p["name"]: p.get("description", "") for p in market["plugins"]}

for p in content["plugins"]:
    if p["name"] not in versions:
        sys.exit(f"{p['name']} is not in marketplace.json")
    p["version"] = versions[p["name"]]
    p["install"] = f"/plugin install {p['name']}@brand-ai"
    p["listing"] = descs[p["name"]]
    # sanity: every named sub-skill exists on disk
    for s in p.get("skills", []):
        if not (repo / "plugins" / p["name"] / "skills" / s["name"] / "SKILL.md").exists():
            sys.exit(f"missing SKILL.md for {s['name']}")
missing = set(versions) - {p["name"] for p in content["plugins"]}
if missing:
    print("warning: in marketplace but not documented:", ", ".join(sorted(missing)))

tpl = (here / "template.html").read_text()
html = tpl.replace("/*DATA*/null", json.dumps(content, ensure_ascii=False).replace("</", "<\\/"))
out = here / "dist"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(html)
print("wrote", out / "index.html", len(html), "bytes")
# keep the copy bundled with the brand-docs plugin in sync, so Claude can open it offline
bundled = repo / "plugins" / "brand-docs" / "skills" / "brand-docs" / "assets"
bundled.mkdir(parents=True, exist_ok=True)
(bundled / "index.html").write_text(html)
print("wrote", bundled / "index.html")
