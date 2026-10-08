#!/usr/bin/env python3
"""Check that BRAND.md follows the brand-capture schema before it is saved or committed.

Standard library only. Usage:

    python validate_brand.py BRAND.md [--evidence <scratch>/evidence] [--questions BRAND-QUESTIONS.md]

Exit codes: 0 valid (warnings allowed), 1 errors found, 2 file missing or unreadable, 3 older schema
(rebuild it with a new brand-capture run). Errors block saving; warnings go in the run report.
Quotes are checked against the evidence only on lines that cite the site ("(from site)" or a URL);
lines labelled (client...), (repo...) or (example) are skipped.

When BRAND.md names a `voice_doc` (BRAND-VOICE.md), that file sits next to BRAND.md and is validated too: the
Voice section in BRAND.md must then be a short pointer. Without `voice_doc` the older layout (Voice written out
inside BRAND.md) still passes, with a warning.
"""
import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SCHEMA = "1.1"
REQUIRED_KEYS = ["brand_md_schema", "brand", "legal_name", "parent_brand", "site", "store", "other_domains",
                 "platform", "category", "markets", "language", "currency", "regulated", "design_doc",
                 "competitors_doc", "search_console_property", "brand_approver", "status", "revision", "approved_by", "approved_on", "captured",
                 "last_updated", "captured_by"]
MUST_HAVE_VALUE = ["brand_md_schema", "brand", "site", "platform", "category", "markets", "language",
                   "currency", "regulated", "design_doc", "status", "revision", "captured", "last_updated",
                   "captured_by"]
HEADINGS = ["Quick reference", "Identity", "Brand architecture", "Story", "Audience", "Catalog", "Voice",
            "Terminology", "Visual identity", "Blog", "Claim limits", "Competitors", "Inspiration brands",
            "Channels", "Author", "Sources", "Change log"]
NO_PENDING_WHEN_APPROVED = ["Brand architecture", "Claim limits"]
VOICE_KEYS = ["brand", "parent_doc", "status", "revision", "last_updated", "source"]
VOICE_HEADINGS = ["In three words", "How it sounds", "Signature phrases", "Do / don't",
                  "Words and habits to avoid", "Rules that stay in BRAND.md", "Change log"]
VOICE_FILE = re.compile(r"[A-Za-z0-9._-]+\.md")   # a plain file name next to BRAND.md, never a path
VOICE_POINTER_MAX = 8                              # non-empty lines allowed in BRAND.md's Voice when voice_doc is set
VOICE_LINES_WARN, VOICE_LINES_FAIL, VOICE_WORDS_WARN, VOICE_WORDS_FAIL = 90, 140, 1200, 2000
DO_DONT = re.compile(r"^\s*-\s*Do:.*Don't:", re.M)
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PLACEHOLDER_ANY = re.compile(r"\[\[CLIENT TO CONFIRM[^\]]*\]\]")
PLACEHOLDER_OK = re.compile(r"\[\[CLIENT TO CONFIRM: (Q-\d{2,3}) \| [^\]]{5,}\]\]")
HTML_OK = r"/?(?:a|b|i|u|p|br|em|strong|small|sup|sub|span|div|ul|ol|li|img|figure|figcaption|h[1-6])\b"
TEMPLATE_LEFTOVER = re.compile(r"<(?!https?://|mailto:|" + HTML_OK + r")[A-Za-z0-9][^<>\n]{2,}>"
                               r"|^\*[A-Z][^*\n]+\*$", re.M)
QUOTE = re.compile(r"[\"\u201c]([^\"\u201c\u201d\n]{12,400})[\"\u201d]")
SOURCED = re.compile(r"\(from site|https?://")          # lines whose quotes must match the evidence
NOT_FROM_SITE = re.compile(r"\((client|repo|example)\b")  # quotes that never come from a web page
LINES_WARN, LINES_FAIL, WORDS_WARN, WORDS_FAIL = 220, 300, 3500, 5000
MAX_SENT = 4  # follow-up questions sent to the client; the rest wait under '## Held for later'
POST_URL = re.compile(r"https?://[^\s)|>]+/(?:blogs?|news|journal|articles?)/[^\s)|>/]+/[^\s)|>]+")


def norm(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def split(text):
    """Return (front-matter dict, body, errors)."""
    if text.startswith("\ufeff"):
        return {}, text, ["file starts with a byte-order mark (BOM): save it as UTF-8 without BOM"]
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text, ["no front matter: the file must start with a --- block"]
    front = {}
    errors = []
    for n, line in enumerate(m.group(1).splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line.startswith((" ", "\t", "-")):
            errors.append(f"front matter line {n} is not a flat `key: value` line: {line.strip()[:60]}")
            continue
        key, value = line.split(":", 1)
        front[key.strip()] = value.strip()
    return front, text[m.end():], errors


def sections(body):
    """Map each `## ` heading to its text, in order."""
    out, order, current = {}, [], None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            order.append(current)
            out[current] = []
        elif current:
            out[current].append(line)
    return order, {k: "\n".join(v) for k, v in out.items()}


def corpus_of(evidence):
    """All saved page text, normalised, so quotes can be looked up in it."""
    return " ".join(norm(p.read_text(encoding="utf-8", errors="replace"))
                    for p in Path(evidence).rglob("*") if p.is_file() and p.suffix in (".txt", ".md", ".json"))


def quote_warnings(body, corpus, label=""):
    """Warnings for quotes on site-cited lines that the saved pages don't contain."""
    out = []
    for line in body.splitlines():
        if not SOURCED.search(line) or NOT_FROM_SITE.search(line):
            continue
        for m in QUOTE.finditer(line):
            if norm(m.group(1)) not in corpus:
                out.append(f"{label}quote not found in the evidence: \"{m.group(1)[:60]}\"")
    return out


def validate_voice(path, brand_front, corpus=None):
    """Check BRAND-VOICE.md (the file BRAND.md's voice_doc names). Returns (errors, warnings, info)."""
    errors, warnings = [], []
    raw = path.read_bytes()
    if b"\r\n" in raw:
        warnings.append(f"CRLF line endings: save with LF (add `{path.name} text eol=lf` to .gitattributes)")
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    front, body, errs = split(text)
    errors += errs
    info = {"file": path.name, "revision": front.get("revision"), "status": front.get("status"),
            "lines": text.count("\n") + 1, "words": len(re.findall(r"\S+", body))}
    if errs and not front:
        return errors, warnings, info

    for key in VOICE_KEYS:
        if key not in front:
            errors.append(f"front matter key missing: {key}")
        elif not front[key]:
            errors.append(f"front matter key has no value: {key}")
    if front.get("parent_doc") and front["parent_doc"] != "BRAND.md":
        errors.append(f"parent_doc must be BRAND.md, got {front['parent_doc']}")
    if front.get("status") and front["status"] not in ("draft", "approved"):
        errors.append("status must be draft or approved")
    elif front.get("status") and front["status"] != brand_front.get("status"):
        warnings.append(f"status is {front['status']} but BRAND.md is {brand_front.get('status')}: "
                        f"approve both together")
    if front.get("brand") and brand_front.get("brand") and front["brand"] != brand_front["brand"]:
        warnings.append(f"brand is '{front['brand']}' here but '{brand_front['brand']}' in BRAND.md")
    if front.get("last_updated") and not DATE.match(front["last_updated"]):
        errors.append(f"last_updated must be YYYY-MM-DD, got {front['last_updated']}")
    if front.get("revision") and not re.fullmatch(r"\d+", front["revision"]):
        errors.append("revision must be a whole number")

    order, secs = sections(body)
    if order != VOICE_HEADINGS:
        missing = [h for h in VOICE_HEADINGS if h not in order]
        extra = [h for h in order if h not in VOICE_HEADINGS]
        if missing:
            errors.append("missing sections: " + ", ".join(missing))
        if extra:
            errors.append("unknown sections (rename or remove): " + ", ".join(extra))
        if not missing and not extra:
            errors.append("sections are out of order; expected: " + ", ".join(VOICE_HEADINGS))

    if PLACEHOLDER_ANY.search(text):
        errors.append("no [[CLIENT TO CONFIRM]] placeholders in this file: open items live in BRAND.md and "
                      "BRAND-QUESTIONS.md; leave the line out until it is answered")
    no_code = re.sub(r"`[^`\n]*`", "", body)
    leftovers = [m.group(0) for m in TEMPLATE_LEFTOVER.finditer(no_code) if not m.group(0).startswith("<!--")]
    if leftovers:
        errors.append("template guidance left in the file: " + "; ".join(x[:40] for x in leftovers[:5]))

    if "Do / don't" in secs and len(DO_DONT.findall(secs["Do / don't"])) < 3:
        warnings.append("Do / don't has fewer than 3 pairs (each line: `- Do: ... e.g. \"...\" · Don't: ... e.g. \"...\"`)")

    log = secs.get("Change log", "")
    revs = re.findall(r"^\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", log, re.M)
    if not revs:
        errors.append("Change log has no rows")
    elif revs[-1][0] != front.get("revision"):
        errors.append(f"last Change log row is rev {revs[-1][0]} but front matter says revision {front.get('revision')}")
    elif revs[-1][1] != front.get("last_updated"):
        warnings.append("last Change log date differs from last_updated")

    lines, words = info["lines"], info["words"]
    if lines > VOICE_LINES_FAIL or words > VOICE_WORDS_FAIL:
        errors.append(f"too long: {lines} lines, {words} words (limit {VOICE_LINES_FAIL} lines, "
                      f"{VOICE_WORDS_FAIL} words)")
    elif lines > VOICE_LINES_WARN or words > VOICE_WORDS_WARN:
        warnings.append(f"long: {lines} lines, {words} words (target {VOICE_LINES_WARN} lines, "
                        f"{VOICE_WORDS_WARN} words)")
    if corpus is not None:
        warnings += quote_warnings(body, corpus)
    return errors, warnings, info


def validate(path, evidence=None, questions=None):
    errors, warnings = [], []
    raw = path.read_bytes()
    if b"\r\n" in raw:
        warnings.append("CRLF line endings: save with LF (add `BRAND.md text eol=lf` to .gitattributes)")
    text = raw.decode("utf-8", errors="replace").replace("\r\n", "\n")
    front, body, errs = split(text)
    errors += errs
    info = {"schema": front.get("brand_md_schema", "1.0" if front else None), "status": front.get("status"),
            "revision": front.get("revision"), "last_updated": front.get("last_updated"), "open_ids": [],
            "lines": text.count("\n") + 1, "words": len(re.findall(r"\S+", body)), "old_schema": False}
    if errs and not front:
        return errors, warnings, info

    schema = front.get("brand_md_schema")
    if not schema:
        info["old_schema"] = True
        return [f"schema 1.0 file (no brand_md_schema key): rebuild it with a new brand-capture run ({SCHEMA})"], \
            warnings, info
    if schema != SCHEMA:
        errors.append(f"brand_md_schema is {schema}, this validator checks {SCHEMA}")

    for key in REQUIRED_KEYS:
        if key not in front:
            errors.append(f"front matter key missing: {key}")
    for key in MUST_HAVE_VALUE:
        if key in front and not front[key]:
            errors.append(f"front matter key has no value: {key}")
    for key in ("captured", "last_updated", "approved_on"):
        if front.get(key) and not DATE.match(front[key]):
            errors.append(f"{key} must be YYYY-MM-DD, got {front[key]}")
    if front.get("status") not in ("draft", "approved"):
        errors.append("status must be draft or approved")
    if front.get("status") == "approved" and not (front.get("approved_by") and front.get("approved_on")):
        errors.append("status is approved but approved_by or approved_on is empty")
    if not re.fullmatch(r"\d+", front.get("revision", "")):
        errors.append("revision must be a whole number")

    order, secs = sections(body)
    if order != HEADINGS:
        missing = [h for h in HEADINGS if h not in order]
        extra = [h for h in order if h not in HEADINGS]
        if missing:
            errors.append("missing sections: " + ", ".join(missing))
        if extra:
            errors.append("unknown sections (rename or remove): " + ", ".join(extra))
        if not missing and not extra:
            errors.append("sections are out of order; expected: " + ", ".join(HEADINGS))

    corpus = corpus_of(evidence) if evidence else None
    voice_name = front.get("voice_doc", "")
    if voice_name and voice_name.lower() != "none":
        if not VOICE_FILE.fullmatch(voice_name):
            errors.append(f"voice_doc must be a plain file name next to BRAND.md (e.g. BRAND-VOICE.md), "
                          f"got {voice_name}")
        else:
            pointer = [l for l in secs.get("Voice", "").splitlines() if l.strip()]
            if voice_name not in "\n".join(pointer):
                errors.append(f"voice_doc is {voice_name} but the Voice section doesn't point to it")
            if len(pointer) > VOICE_POINTER_MAX:
                errors.append(f"Voice is {len(pointer)} lines: with voice_doc set it is a pointer plus a short "
                              f"summary (max {VOICE_POINTER_MAX}); move the detail into {voice_name}")
            voice_path = path.with_name(voice_name)
            if not voice_path.is_file():
                errors.append(f"voice_doc names {voice_name} but there is no such file next to BRAND.md")
            else:
                v_errors, v_warnings, v_info = validate_voice(voice_path, front, corpus)
                errors += [f"{voice_name}: {e}" for e in v_errors]
                warnings += [f"{voice_name}: {w}" for w in v_warnings]
                info["voice"] = v_info
    else:
        warnings.append("voice_doc is not set: Voice is written out inside BRAND.md (older layout). New captures "
                        "keep it in BRAND-VOICE.md; see the split-voice mode in SKILL.md")

    for key, value in front.items():
        if re.search(r"<[^<>]{3,}>", value):
            errors.append(f"front matter key {key} still holds template text: {value[:50]}")

    ids = []
    for m in PLACEHOLDER_ANY.finditer(text):  # front matter values can be placeholders too
        ok = PLACEHOLDER_OK.fullmatch(m.group(0))
        if not ok:
            errors.append(f"placeholder without id and question: {m.group(0)[:70]}")
        else:
            ids.append(ok.group(1))
    info["open_ids"] = sorted(set(ids))
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errors.append("placeholder ids used twice: " + ", ".join(dupes))
    if front.get("status") == "approved":
        for name in NO_PENDING_WHEN_APPROVED:
            if PLACEHOLDER_ANY.search(secs.get(name, "")):
                errors.append(f"status is approved but '{name}' still has open placeholders")
    if questions:
        qtext = questions.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
        asked = set(re.findall(r"\bQ-\d{2,3}\b", qtext))
        for i in sorted(set(ids) - asked):
            errors.append(f"{i} is open in BRAND.md but missing from {questions.name}")
        sent = re.split(r"^## Held for later", qtext, maxsplit=1, flags=re.M)[0]
        info["sent_ids"] = sorted(set(re.findall(r"^\*\*(Q-\d{2,3})\b", sent, re.M)))
        if len(info["sent_ids"]) > MAX_SENT:
            errors.append(f"{len(info['sent_ids'])} questions for the client (max {MAX_SENT}): move the rest "
                          f"under '## Held for later'")

    no_code = re.sub(r"`[^`\n]*`", "", body)  # inline code may legitimately show markup such as `<h2>`
    leftovers = [m.group(0) for m in TEMPLATE_LEFTOVER.finditer(no_code) if not m.group(0).startswith("<!--")]
    if leftovers:
        errors.append("template guidance left in the file: " + "; ".join(x[:40] for x in leftovers[:5]))

    log = secs.get("Change log", "")
    revs = re.findall(r"^\|\s*(\d+)\s*\|\s*(\d{4}-\d{2}-\d{2})\s*\|", log, re.M)
    if not revs:
        errors.append("Change log has no rows")
    elif revs[-1][0] != front.get("revision"):
        errors.append(f"last Change log row is rev {revs[-1][0]} but front matter says revision {front.get('revision')}")
    elif revs[-1][1] != front.get("last_updated"):
        warnings.append("last Change log date differs from last_updated")

    not_sources = "\n".join(v for k, v in secs.items() if k != "Sources")  # Sources may cite posts
    posts = sorted(set(POST_URL.findall(not_sources)))
    if len(posts) > 3:
        warnings.append(f"{len(posts)} links to individual blog posts: post lists don't belong in BRAND.md")

    quick = [l for l in secs.get("Quick reference", "").splitlines() if l.strip()]
    if len(quick) > 15:
        warnings.append(f"Quick reference has {len(quick)} lines (max 15)")

    lines, words = info["lines"], info["words"]
    if lines > LINES_FAIL or words > WORDS_FAIL:
        errors.append(f"too long: {lines} lines, {words} words (limit {LINES_FAIL} lines, {WORDS_FAIL} words)")
    elif lines > LINES_WARN or words > WORDS_WARN:
        warnings.append(f"long: {lines} lines, {words} words (target {LINES_WARN} lines, {WORDS_WARN} words)")

    if corpus is not None:
        warnings += quote_warnings(body, corpus)
    return errors, warnings, info


def main():
    ap = argparse.ArgumentParser(description="Validate BRAND.md against the brand-capture schema")
    ap.add_argument("file")
    ap.add_argument("--evidence", help="folder of page texts saved by scrape_site.py (checks verbatim quotes)")
    ap.add_argument("--questions", help="BRAND-QUESTIONS.md (checks every open id was asked)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    path = Path(a.file)
    if not path.is_file():
        print(f"error: {path} not found", file=sys.stderr)
        return 2
    questions = Path(a.questions) if a.questions else None
    errors, warnings, info = validate(path, a.evidence, questions)
    if a.json:
        print(json.dumps({"file": str(path), "errors": errors, "warnings": warnings, **info}, indent=2))
    else:
        for e in errors:
            print("ERROR  " + e)
        for w in warnings:
            print("WARN   " + w)
        print("OK" if not errors else f"{len(errors)} error(s)")
    if info["old_schema"]:
        return 3
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
