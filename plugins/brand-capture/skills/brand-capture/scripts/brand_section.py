#!/usr/bin/env python3
"""Print one section of BRAND.md (or its front matter) so a skill can read only what it needs.

    python brand_section.py BRAND.md "Claim limits"        # one section
    python brand_section.py BRAND.md --front markets      # one front-matter value
    python brand_section.py BRAND.md --list               # section names
    python brand_section.py BRAND-VOICE.md "How it sounds"   # works on any file with ## headings

"Voice" is special: when BRAND.md names a voice_doc (BRAND-VOICE.md) the Voice section is only a pointer, so
this prints the pointer and then the whole voice file, and callers get the real content in one call.

Standard library only. Exit 1 when the section or key is missing, so callers can react.
"""
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load(path):
    text = Path(path).read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    front, body = {}, text
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            for line in text[4:end].splitlines():
                if ":" in line and not line.lstrip().startswith("#"):
                    k, v = line.split(":", 1)
                    front[k.strip()] = v.strip()
            body = text[end + 5:]
    return front, body


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    front, body = load(argv[1])
    if argv[2] == "--front":
        value = front.get(argv[3]) if len(argv) > 3 else None
        if value is None:
            return 1
        print(value)
        return 0
    names, out, current = [], [], None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            names.append(current)
            if out:
                break
            if current.lower() == argv[2].lower():
                out.append(line)
            continue
        if out:
            out.append(line)
    if argv[2] == "--list":
        print("\n".join(names))
        return 0
    if not out:
        return 1
    print("\n".join(out).rstrip())
    if argv[2].lower() == "voice":
        voice = follow_voice(argv[1], front)
        if voice:
            print(voice)
    return 0


def follow_voice(brand_path, front):
    """The voice file's body, introduced by a one-line note, when BRAND.md's voice_doc points to one."""
    name = front.get("voice_doc", "")
    if not re.fullmatch(r"[A-Za-z0-9._-]+\.md", name):
        return ""
    path = Path(brand_path).with_name(name)
    if not path.is_file():
        print(f"warning: voice_doc names {name} but it isn't next to {Path(brand_path).name}", file=sys.stderr)
        return ""
    vfront, vbody = load(path)
    return f"\n(continued in {name}, rev {vfront.get('revision', '?')})\n\n" + vbody.strip()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
