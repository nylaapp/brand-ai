#!/usr/bin/env python3
"""Measure how much of a rewrite is still the source's wording, and compare it to a rewrite tier's limits.

    python3 overlap_check.py <source.(md|txt|html)> <rewrite.(md|txt|html)> --tier <match|reword|restructure|reimagine> [--json]

Python 3 standard library only. Exit 0 = within the tier's limits, 1 = over a limit, 2 = unreadable input.
This is a wording check, not legal clearance: it can't see copied structure, ideas or images.
"""
import argparse, html, json, re, sys
from pathlib import Path

# (max shared 5-word phrases as % of the rewrite, longest shared run in words, max verbatim sentences, max shared headings)
LIMITS = {
    "match":       (None, None, None, None),   # reported, never failed: own or client content
    "reword":      (12.0, 10, 2, None),
    "restructure": (5.0, 7, 0, 1),
    "reimagine":   (2.0, 5, 0, 0),
}
STOP = re.compile(r"[^\w\s'’-]", re.U)


def text_of(path):
    raw = Path(path).read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?m)^URL:.*$", " ", raw)
    heads = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"(?is)<h[1-6][^>]*>(.*?)</h[1-6]>", raw)]
    heads += [h.strip("# ").strip() for h in re.findall(r"(?m)^#{1,6}\s+(.+)$", raw)]
    raw = re.sub(r"<[^>]+>", " ", raw)
    raw = html.unescape(raw)
    raw = re.sub(r"[*_`>#|]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or " ", raw)
    return raw, [h for h in heads if h]


def words(t):
    return STOP.sub(" ", t.lower().replace("’", "'")).split()


def sentences(t):
    return [s for s in re.split(r"(?<=[.!?])\s+|\n+", t) if len(words(s)) >= 6]


def grams(w, n):
    return [tuple(w[i:i + n]) for i in range(len(w) - n + 1)]


def longest_run(a, b):
    """Longest common run of words (dynamic programming over the rewrite's words)."""
    best, prev = 0, {}
    pos = {}
    for j, w in enumerate(b):
        pos.setdefault(w, []).append(j)
    for w in a:
        cur = {}
        for j in pos.get(w, ()):
            cur[j] = prev.get(j - 1, 0) + 1
            best = max(best, cur[j])
        prev = cur
    return best


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("source"); ap.add_argument("rewrite")
    ap.add_argument("--tier", choices=list(LIMITS), default="reword")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        st, sh = text_of(a.source); rt, rh = text_of(a.rewrite)
    except OSError as e:
        print(f"cannot read input: {e}", file=sys.stderr); return 2
    sw, rw = words(st), words(rt)
    if len(rw) < 50 or len(sw) < 50:
        print("one of the texts is too short to compare", file=sys.stderr); return 2
    sg = set(grams(sw, 5)); rg = grams(rw, 5)
    shared = sum(1 for g in rg if g in sg)
    pct = 100.0 * shared / max(1, len(rg))
    run = longest_run(sw, rw)
    ss = {" ".join(words(s)) for s in sentences(st)}
    verbatim = [s for s in sentences(rt) if " ".join(words(s)) in ss]
    sheads = {" ".join(words(h)) for h in sh}
    same_heads = [h for h in rh if " ".join(words(h)) in sheads]
    lim = LIMITS[a.tier]
    problems = []
    if lim[0] is not None and pct > lim[0]: problems.append(f"shared 5-word phrases {pct:.1f}% (limit {lim[0]}%)")
    if lim[1] is not None and run > lim[1]: problems.append(f"longest shared run {run} words (limit {lim[1]})")
    if lim[2] is not None and len(verbatim) > lim[2]: problems.append(f"{len(verbatim)} verbatim sentences (limit {lim[2]})")
    if lim[3] is not None and len(same_heads) > lim[3]: problems.append(f"{len(same_heads)} headings kept from the source (limit {lim[3]})")
    out = {"tier": a.tier, "source_words": len(sw), "rewrite_words": len(rw), "shared_5gram_pct": round(pct, 1),
           "longest_shared_run_words": run, "verbatim_sentences": verbatim[:10], "verbatim_sentence_count": len(verbatim),
           "shared_headings": same_heads, "over_limit": problems, "pass": not problems,
           "note": "wording check only; not legal clearance, and blind to copied structure, ideas and images"}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"tier {a.tier}: {out['shared_5gram_pct']}% shared 5-word phrases · longest shared run {run} words · "
              f"{len(verbatim)} verbatim sentences · {len(same_heads)} shared headings")
        for s in verbatim[:5]: print(f"  verbatim: {s[:140]}")
        print("PASS" if not problems else "OVER: " + "; ".join(problems))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
