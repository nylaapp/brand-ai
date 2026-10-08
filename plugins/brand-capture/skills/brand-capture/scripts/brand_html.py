#!/usr/bin/env python3
"""Render BRAND.md as one self-contained HTML page the client can read, share and print.

Standard library only. Usage:

    python brand_html.py BRAND.md [--questions BRAND-QUESTIONS.md] [--out BRAND.html]

The page drops what only agents need (the source-of-truth notice, fingerprints, technical front-matter keys),
shows the questions sent to the client first while the file is a draft, and turns origin labels and
[[CLIENT TO CONFIRM]] placeholders into readable tags. Everything from BRAND.md is escaped: it is data.

When BRAND.md names a voice_doc (BRAND-VOICE.md) next to it, the page shows that file's content under Voice, so
the client still reads the whole voice in one place.
"""
import argparse
import html
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Only what the client recognises. Internal pointers (design_doc, competitors_doc, search_console_property,
# captured_by) stay out: the client never receives those files.
GLANCE = [("site", "Website"), ("category", "Category"), ("markets", "Markets"), ("language", "Language"),
          ("currency", "Currency"), ("regulated", "Regulated"), ("brand_approver", "On-brand approver")]
HIDE_SECTIONS = {"Sources"}
HIDE_VOICE_SECTIONS = {"Rules that stay in BRAND.md", "Change log"}   # notes for agents, not for the client
VOICE_FILE = re.compile(r"[A-Za-z0-9._-]+\.md")
LABELS = {"from site": "from your site", "client": "from you", "repo": "from our files", "inferred": "our reading",
          "suggested": "our suggestion", "example": "example"}
LABEL = re.compile(r"\((from site|client|repo|inferred|suggested|example)([^()]*)\)")
CONFIRM = re.compile(r"\[\[CLIENT TO CONFIRM: (Q-\d{2,3}) \| ([^\]]+)\]\]")
MD_LINK = re.compile(r"\[([^\]\n]+)\]\((https?://[^)\s]+)\)")
AUTOLINK = re.compile(r"(?<![\w\"'=/>])(https?://[^\s)<|]+[^\s)<|.,;:])")
CODE = re.compile(r"`([^`\n]+)`")

CSS = """
:root { --ink:#1f1f1f; --muted:#5a5a60; --line:#dedad2; --soft:#f5f3ee; --accent:#8a6d3b; --confirm:#fbe7c6;
  --tag:#ebe7df; --bg:#ffffff; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --ink:#ece9e3; --muted:#b4b0a8;
  --line:#3a3833; --soft:#24221f; --accent:#d8b779; --confirm:#5a4520; --tag:#33302b; --bg:#171614; } }
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.55 system-ui, -apple-system, "Segoe UI",
  Roboto, Arial, sans-serif; }
main { max-width: 860px; margin: 0 auto; padding: 32px 16px 64px; }
header.top { border-bottom: 2px solid var(--ink); padding-bottom: 16px; margin-bottom: 24px; }
.eyebrow { font-size: 13px; letter-spacing: .08em; text-transform: uppercase; color: var(--muted); margin: 0; }
h1 { font-size: clamp(28px, 6vw, 40px); line-height: 1.15; margin: 6px 0 10px; letter-spacing: -.01em; }
h2 { font-size: 22px; margin: 36px 0 10px; padding-top: 14px; border-top: 1px solid var(--line); }
h3 { font-size: 17px; margin: 22px 0 6px; }
p { margin: 8px 0; }
ul, ol { padding-left: 22px; margin: 8px 0; }
li { margin: 4px 0; }
a { color: inherit; text-decoration-color: var(--accent); text-underline-offset: 3px; overflow-wrap: anywhere; }
code { font-family: ui-monospace, Consolas, monospace; font-size: .9em; background: var(--soft); padding: 1px 4px;
  border-radius: 4px; overflow-wrap: anywhere; }
.status { display: inline-block; font-size: 14px; font-weight: 600; padding: 4px 10px; border-radius: 999px;
  background: var(--confirm); color: var(--ink); }
.status.ok { background: var(--tag); }
.meta { color: var(--muted); font-size: 14px; margin: 8px 0 0; }
.intro { background: var(--soft); border-radius: 8px; padding: 14px 16px; margin: 0 0 8px; }
.glance { width: 100%; border-collapse: collapse; margin: 8px 0; }
.scroll { overflow-x: auto; margin: 10px 0; }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { text-align: left; vertical-align: top; padding: 8px 10px; border-bottom: 1px solid var(--line); }
th { font-weight: 600; background: var(--soft); }
.glance th { width: 34%; background: none; color: var(--muted); font-weight: 500; }
.tag { display: inline-block; font-size: 12px; line-height: 1.5; padding: 0 7px; border-radius: 999px;
  background: var(--tag); color: var(--muted); white-space: nowrap; vertical-align: 1px; }
.confirm { background: var(--confirm); border-radius: 4px; padding: 1px 5px; box-decoration-break: clone;
  -webkit-box-decoration-break: clone; }
.questions { border: 2px solid var(--accent); border-radius: 10px; padding: 6px 18px 12px; margin: 24px 0; }
.questions h2 { border: 0; margin-top: 10px; padding-top: 0; }
.q { margin: 14px 0; }
.q .id { font-weight: 700; color: var(--accent); }
footer { margin-top: 48px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line);
  padding-top: 12px; }
@media print { body { font-size: 11pt; } main { max-width: none; padding: 0; } h2 { break-after: avoid; }
  tr, .q { break-inside: avoid; } a { text-decoration: none; } }
"""


def split_front(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    front = {}
    for line in m.group(1).splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, v = line.split(":", 1)
            front[k.strip()] = v.strip()
    return front, text[m.end():]


def inline(text):
    """Escape first, then add code, links, emphasis, origin tags and to-confirm highlights."""
    stash = []

    def keep(fragment):
        stash.append(fragment)
        return f"\x00{len(stash) - 1}\x00"

    text = CODE.sub(lambda m: keep("<code>" + html.escape(m.group(1)) + "</code>"), text)
    text = CONFIRM.sub(lambda m: keep(f'<span class="confirm"><strong>To confirm ({m.group(1)}):</strong> '
                                      f"{html.escape(m.group(2).strip())}</span>"), text)
    text = MD_LINK.sub(lambda m: keep(f'<a href="{html.escape(m.group(2))}">{html.escape(m.group(1))}</a>'), text)
    text = AUTOLINK.sub(lambda m: keep(f'<a href="{html.escape(m.group(1))}">{html.escape(m.group(1))}</a>'), text)
    text = LABEL.sub(lambda m: keep(f'<span class="tag">{LABELS[m.group(1)]}{html.escape(m.group(2))}</span>'), text)
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", text)
    for _ in range(3):  # stashed fragments can contain other stashed fragments
        text = re.sub(r"\x00(\d+)\x00", lambda m: stash[int(m.group(1))], text)
    return text


def cells_of(row):
    """Split a table row on |, except inside [[...]] placeholders (they contain a | themselves)."""
    cells, buf, depth, i = [], [], 0, 0
    row = row.strip().strip("|")
    while i < len(row):
        if row.startswith("[[", i):
            depth, i = depth + 1, i + 2
            buf.append("[[")
            continue
        if row.startswith("]]", i) and depth:
            depth, i = depth - 1, i + 2
            buf.append("]]")
            continue
        ch = row[i]
        if ch == "|" and not depth and (i == 0 or row[i - 1] != "\\"):
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
        i += 1
    cells.append("".join(buf).strip())
    return cells


def table(rows):
    cells = [cells_of(r) for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r":?-{2,}:?", c) for c in r if c)]
    if not cells:
        return ""
    head, body = cells[0], cells[1:]
    out = ['<div class="scroll"><table><thead><tr>'
           + "".join(f'<th scope="col">{inline(c)}</th>' for c in head) + "</tr></thead><tbody>"]
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def blocks(md):
    """Markdown subset used by BRAND.md: headings, nested lists, tables, quotes, paragraphs."""
    lines = md.split("\n")
    out, stack, i = [], [], 0

    def close(level=-1):
        while stack and stack[-1][1] > level:
            out.append(f"</li></{stack.pop()[0]}>")

    while i < len(lines):
        line, s = lines[i], lines[i].strip()
        if not s or s.startswith("<!--"):
            i += 1
            continue
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            level, kind = len(m.group(1).expandtabs(2)) // 2, "ol" if m.group(2)[0].isdigit() else "ul"
            if stack and stack[-1][1] >= level:
                close(level)
            if stack and stack[-1][1] == level:
                out.append(f"</li><li>{inline(m.group(3))}")
            else:
                out.append(f"<{kind}><li>{inline(m.group(3))}")
                stack.append((kind, level))
            i += 1
            continue
        if s.startswith("|"):
            if not line.startswith((" ", "\t")):
                close()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
            continue
        if line.startswith((" ", "\t")) and stack:
            out.append(f" {inline(s)}")
            i += 1
            continue
        close()
        if s.startswith("### "):
            out.append(f"<h3>{inline(s[4:])}</h3>")
        elif s.startswith("## "):
            out.append(f"<h2>{inline(s[3:])}</h2>")
        elif s.startswith("# "):
            pass  # the page header carries the title
        elif s.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + "".join(f"<p>{inline(q)}</p>" for q in quote if q) + "</blockquote>")
            continue
        else:
            para = [s]
            while i + 1 < len(lines):
                nxt = lines[i + 1].strip()
                if not nxt or re.match(r"^([-*]|\d+\.)\s+|^[#>|]|^<!--", nxt):
                    break
                para.append(nxt)
                i += 1
            out.append(f"<p>{inline(' '.join(para))}</p>")
        i += 1
    close()
    return "\n".join(out)


def sections(body):
    """Split the body into (heading, text) pairs; text before the first ## is the preamble."""
    parts, current, buf = [], None, []
    for line in body.split("\n"):
        if line.startswith("## "):
            parts.append((current, "\n".join(buf)))
            current, buf = line[3:].strip(), []
        else:
            buf.append(line)
    parts.append((current, "\n".join(buf)))
    return parts


def sent_questions(qtext):
    """The questions still waiting for the client: entries before '## Held for later' that have no
    'Answered <date>' line yet, as (id, title, detail)."""
    sent = re.split(r"^## Held for later", qtext, maxsplit=1, flags=re.M)[0]
    found = []
    for m in re.finditer(r"^\*\*(Q-\d{2,3})\s*[·:.-]\s*(.+?)\*\*\s*\n(.*?)(?=^\*\*Q-\d|^## |\Z)", sent, re.M | re.S):
        if re.search(r"^\s*(?:[-*>]\s*)?\**Answered\b", m.group(3), re.M | re.I):
            continue
        found.append((m.group(1), m.group(2).strip(), m.group(3).strip()))
    return found


def voice_section(voice_text):
    """The Voice section of the page, built from BRAND-VOICE.md, and that file's revision."""
    front, body = split_front(voice_text.replace("\r\n", "\n").lstrip("﻿"))
    inner = "".join(f"<h3>{inline(h)}</h3>{blocks(c)}" for h, c in sections(body)
                    if h is not None and h not in HIDE_VOICE_SECTIONS)
    return f"<section><h2>Voice</h2>{inner}</section>", front.get("revision", "")


def render(brand_text, questions_text=None, voice_text=None):
    text = brand_text.replace("\r\n", "\n").lstrip("﻿")
    front, body = split_front(text)
    name = front.get("brand") or "Brand"
    status = front.get("status", "draft")
    if status == "approved":
        badge = (f'<span class="status ok">Approved by {html.escape(front.get("approved_by", ""))} on '
                 f'{html.escape(front.get("approved_on", ""))}</span>')
    else:
        badge = '<span class="status">Draft for your review</span>'
    meta = (f'Revision {html.escape(front.get("revision", "1"))} · last updated '
            f'{html.escape(front.get("last_updated", ""))}')
    glance = "".join(f'<tr><th scope="row">{label}</th><td>{inline(front[key])}</td></tr>'
                     for key, label in GLANCE if front.get(key) and front[key] != "none")
    parts = [f'<header class="top"><p class="eyebrow">Brand file</p><h1>{html.escape(name)}</h1>{badge}'
             f'<p class="meta">{meta}</p></header>',
             f'<p class="intro">This is the one reference every tool we use reads before writing anything for '
             f'{html.escape(name)}: who you are, how you sound, what you sell and what we must never claim. '
             f'Tags show where each line comes from: <span class="tag">from your site</span> '
             f'<span class="tag">from you</span> <span class="tag">our reading</span>. '
             f'<span class="confirm">Highlighted lines</span> wait for your confirmation; until then our tools '
             f'treat them as unconfirmed.</p>']
    if glance:
        parts.append(f'<table class="glance"><tbody>{glance}</tbody></table>')
    if questions_text and status != "approved":
        qs = sent_questions(questions_text.replace("\r\n", "\n"))
        if qs:
            items = "".join(f'<div class="q"><p><span class="id">{qid}</span> <strong>{inline(title)}</strong></p>'
                            f'{blocks(detail)}</div>' for qid, title, detail in qs)
            parts.append(f'<section class="questions" aria-labelledby="qs"><h2 id="qs">'
                         f'{len(qs)} question{"s" if len(qs) != 1 else ""} for you</h2>{items}</section>')
    voice_rev = ""
    for heading, content in sections(body):
        if heading is None or heading in HIDE_SECTIONS:
            continue  # the preamble is the agents' notice; Sources are fingerprints for agents
        if heading == "Voice" and voice_text:
            voice_html, voice_rev = voice_section(voice_text)
            parts.append(voice_html)
            continue
        parts.append(f"<section><h2>{inline(heading)}</h2>{blocks(content)}</section>")
    source = f'BRAND.md, revision {html.escape(front.get("revision", "1"))}'
    if voice_rev:
        source += f' and BRAND-VOICE.md, revision {html.escape(voice_rev)}'
    parts.append(f'<footer>Generated from {source}. '
                 f'To change anything, tell us; we update the file and send you a new copy.</footer>')
    lang = html.escape((front.get("language") or "en").split(",")[0].strip() or "en")
    return (f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{html.escape(name)} brand file</title><style>{CSS}</style></head>'
            f'<body><main>{"".join(parts)}</main></body></html>\n')


def main():
    ap = argparse.ArgumentParser(description="Render BRAND.md as a readable HTML page for the client")
    ap.add_argument("file")
    ap.add_argument("--questions", help="BRAND-QUESTIONS.md; its sent questions are shown first while in draft")
    ap.add_argument("--out", help="output path (default: BRAND.html next to BRAND.md)")
    a = ap.parse_args()
    src = Path(a.file)
    if not src.is_file():
        print(f"error: {src} not found", file=sys.stderr)
        return 2
    qtext = None
    if a.questions:
        qpath = Path(a.questions)
        if not qpath.is_file():
            print(f"error: {qpath} not found", file=sys.stderr)
            return 2
        qtext = qpath.read_text(encoding="utf-8", errors="replace")
    out = Path(a.out) if a.out else src.with_name("BRAND.html")
    brand_text = src.read_text(encoding="utf-8", errors="replace")
    voice_name = split_front(brand_text.replace("\r\n", "\n"))[0].get("voice_doc", "")
    vtext = None
    if VOICE_FILE.fullmatch(voice_name) and src.with_name(voice_name).is_file():
        vtext = src.with_name(voice_name).read_text(encoding="utf-8", errors="replace")
    out.write_text(render(brand_text, qtext, vtext), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
