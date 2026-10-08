#!/usr/bin/env python3
"""Point a project's agent instructions and skills at BRAND.md, so every tool reads the same brand facts.

Standard library only. Works the same for Claude Code (CLAUDE.md, .claude/skills), Codex and other AGENTS.md
tools (AGENTS.md, .agents/skills), Cowork folders and plain repos. Usage:

    python link_brand.py <project-root>                 # dry run: list what would change, change nothing
    python link_brand.py <project-root> --apply all     # add or refresh the link everywhere it was proposed
    python link_brand.py <project-root> --apply AGENTS.md .claude/skills/x/SKILL.md
    python link_brand.py <project-root> --remove        # take every link out again

The link is a short marked block, so running it twice changes nothing and --remove undoes it exactly.
Only files inside the project are touched; installed skills elsewhere on the machine are never edited.
"""
import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

START, END = "<!-- brand-capture:link -->", "<!-- /brand-capture:link -->"
BLOCK = re.compile(re.escape(START) + r".*?" + re.escape(END) + r"[ \t]*(?:\r?\n)?", re.S)
SKILL_GLOBS = [".claude/skills/*/SKILL.md", ".agents/skills/*/SKILL.md", "skills/*/SKILL.md",
               ".claude/commands/*.md", ".claude/agents/*.md"]
AGENT_FILES = ["AGENTS.md", "CLAUDE.md"]
OWN_FILES = {"brand.md", "brand-voice.md", "brand-questions.md", "brand-requests.md", "competitors.md", "readme.md", "changelog.md",
             "license.md", "contributing.md", "code_of_conduct.md", "security.md"}
OWN_SKILLS = {"brand-capture", "competitor-research"}
SKIP_DIRS = {".git", "node_modules", "vendor", "dist", "build", ".venv", "venv", "__pycache__", ".next", ".cache"}
# Words that show a file guides writing customer-facing words; one point per distinct word found.
COPY_WORDS = ["brand", "voice", "tone of voice", "copywriting", "blog", "article", "product description",
              "seo", "meta description", "alt text", "headline", "tagline", "caption", "email", "newsletter",
              "social media", "marketing", "customer-facing", "claims", "disclaimer", "wording", "landing page",
              "faq", "testimonial", "review"]
SKILL_MIN, DOC_MIN = 3, 5


def block_text(newline="\n"):
    lines = [START,
             "> **Brand facts live in `BRAND.md`** (project root, else the central brand directory `$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`). Read it before writing anything "
             "customers will see: names, voice, terminology, claim limits, competitors and inspiration brands all "
             "come from there (deeper competitor research, when it exists, is in `COMPETITORS.md`). Don't ask the "
             "user about the brand and don't re-research it. To change something in it, add a line to "
             "`BRAND-REQUESTS.md` instead of editing it.",
             END, ""]
    return newline.join(lines)


def score(text):
    low = text.lower()
    return sorted({w for w in COPY_WORDS if re.search(r"(?<![a-z])" + re.escape(w) + r"(?![a-z])", low)})


def insert_at(text):
    """Index after the front matter and the first heading (or after the front matter alone)."""
    pos = 0
    m = re.match(r"---\r?\n.*?\r?\n---[ \t]*\r?\n", text, re.S)
    if m:
        pos = m.end()
    rest = text[pos:]
    lead = re.match(r"(?:[ \t]*\r?\n)*", rest).end()
    h = re.match(r"#[^\n]*\n", rest[lead:])
    if h:
        pos += lead + h.end()
    return pos


def with_block(text):
    newline = "\r\n" if "\r\n" in text else "\n"
    block = block_text(newline)
    if START in text:
        return BLOCK.sub(lambda _: block, text, count=1)
    pos = insert_at(text)
    before, after = text[:pos], text[pos:]
    if before and not before.endswith("\n"):
        before += newline
    if before and not before.endswith(newline * 2):
        before += newline
    return before + block + (newline if after and not after.startswith(("\n", "\r\n")) else "") + after


def without_block(text):
    newline = "\r\n" if "\r\n" in text else "\n"
    out = BLOCK.sub("", text)
    return re.sub("(" + re.escape(newline) + "){3,}", newline * 2, out)


def read(path):
    return path.read_bytes().decode("utf-8", errors="replace")


def candidates(root):
    """Every file that should carry the link, with why. Agent files always; skills and docs by content."""
    found, seen = [], set()

    def add(path, kind, reason, create=False):
        rel = path.relative_to(root).as_posix()
        if rel not in seen:
            seen.add(rel)
            found.append({"path": rel, "kind": kind, "reason": reason, "create": create})

    agents = root / "AGENTS.md"
    claude = root / "CLAUDE.md"
    if agents.is_file():
        add(agents, "agent instructions", "read by Codex and other AGENTS.md tools at the start of every session")
    if claude.is_file():
        if agents.is_file() and re.search(r"^@AGENTS\.md\s*$", read(claude), re.M):
            pass  # CLAUDE.md imports AGENTS.md, so the AGENTS.md link already reaches Claude Code
        else:
            add(claude, "agent instructions", "read by Claude Code and Cowork at the start of every session")
    if not agents.is_file() and not claude.is_file():
        add(agents, "agent instructions", "new file: Codex and other tools read it every session", create=True)
        add(claude, "agent instructions", "new file: imports AGENTS.md so Claude Code reads the same rules",
            create=True)

    for pattern in SKILL_GLOBS:
        for path in sorted(root.glob(pattern)):
            parts = path.relative_to(root).parts
            if path.parent.name in OWN_SKILLS or any(p in SKIP_DIRS for p in parts):
                continue
            words = score(read(path))
            if len(words) >= SKILL_MIN:
                add(path, "skill", "writes or checks customer-facing words: " + ", ".join(words[:6]))

    for path in sorted(root.rglob("*.md")):
        rel_parts = path.relative_to(root).parts
        if len(rel_parts) > 3 or any(p in SKIP_DIRS or p.startswith(".") for p in rel_parts[:-1]):
            continue
        if path.name.lower() in OWN_FILES or path.name in AGENT_FILES or path.name == "SKILL.md":
            continue
        if re.search(r"(^|[-_ ])(qa|log|logs|report|reports|notes|history)([-_ ]|$)", path.stem, re.I):
            continue  # records of past work, not instructions
        if path.relative_to(root).as_posix() in seen:
            continue
        text = read(path)
        if not re.search(r"\b(always|never|must|should|step \d|workflow|checklist)\b", text, re.I):
            continue  # notes and data files, not instructions
        words = score(text)
        if len(words) >= DOC_MIN:
            add(path, "workflow doc", "instructions that involve customer-facing words: " + ", ".join(words[:6]))
    return found


def status_of(root, item):
    path = root / item["path"]
    if item["create"]:
        return "would create"
    text = read(path)
    if START in text:
        current = BLOCK.search(text)
        newline = "\r\n" if "\r\n" in text else "\n"
        return "linked" if current and current.group(0).rstrip() == block_text(newline).rstrip() else "outdated link"
    if "brand.md" in text.lower():
        return "mentions BRAND.md"
    return "would add"


def apply(root, item):
    path = root / item["path"]
    if item["create"]:
        if path.name == "CLAUDE.md":
            path.write_text("@AGENTS.md\n", encoding="utf-8", newline="")
        else:
            path.write_text("# Agent instructions\n\n" + block_text(), encoding="utf-8", newline="")
        return "created"
    text = read(path)
    new = with_block(text)
    if new == text:
        return "unchanged"
    path.write_bytes(new.encode("utf-8"))
    return "linked"


def main():
    ap = argparse.ArgumentParser(description="Point a project's agent files and skills at BRAND.md")
    ap.add_argument("root", help="project root (where BRAND.md lives)")
    ap.add_argument("--apply", nargs="+", metavar="PATH", help="'all', or the proposed paths to link")
    ap.add_argument("--remove", action="store_true", help="remove every BRAND.md link block")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a folder", file=sys.stderr)
        return 2

    if a.remove:
        done = []
        for path in sorted(root.rglob("*.md")):
            if any(p in SKIP_DIRS for p in path.relative_to(root).parts):
                continue
            text = read(path)
            if START in text:
                path.write_bytes(without_block(text).encode("utf-8"))
                done.append(path.relative_to(root).as_posix())
        print(json.dumps({"removed": done}, indent=2) if a.json else
              "\n".join(["removed: " + d for d in done]) or "no links found")
        return 0

    items = candidates(root)
    for item in items:
        item["status"] = status_of(root, item)
    if a.apply:
        wanted = {p.replace("\\", "/") for p in a.apply}
        unknown = wanted - {"all"} - {i["path"] for i in items}
        if unknown:
            print("error: not proposed by the dry run: " + ", ".join(sorted(unknown)), file=sys.stderr)
            return 1
        for item in items:
            if item["path"] in wanted or ("all" in wanted and item["status"] != "mentions BRAND.md"):
                item["status"] = apply(root, item)
    if a.json:
        print(json.dumps({"root": str(root), "brand_md": (root / "BRAND.md").is_file(), "files": items}, indent=2))
    else:
        if not (root / "BRAND.md").is_file():
            print("note: no BRAND.md in this folder yet")
        for item in items:
            print(f"{item['status']:<18} {item['path']}  ({item['kind']}: {item['reason']})")
        if not a.apply:
            print("dry run: nothing changed. Re-run with --apply all, or --apply <paths>.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
