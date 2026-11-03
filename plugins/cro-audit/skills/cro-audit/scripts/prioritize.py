#!/usr/bin/env python3
"""Rank test ideas and fixes with ICE or PIE scoring. Stdlib only.

  prioritize.py ideas.json                 # ICE (default)
  prioritize.py ideas.json --method pie
  prioritize.py ideas.json --evidence-confidence

Input is a JSON list. Each idea: {"id":"CRO-01","title":"...","impact":8,"ease":7,"confidence":6,
"evidence":["Heuristic","Measured","Customer voice"]}. PIE uses "potential","importance","ease"
instead of impact and confidence. Scores run 1 to 10.

ICE = average of impact, confidence and ease. PIE = average of potential, importance and ease.
--evidence-confidence ignores any hand-given confidence and sets it from how many DIFFERENT
kinds of evidence back the idea: 1 kind = 3 (5 if that kind is "Measured": the problem is certain,
only its effect isn't), 2 kinds = 6, 3 or more = 8, and 9 only if the idea lists "Behavioural" or
"Experiment" among them. This keeps a guess from outranking a finding that
several independent sources agree on. It is a default rule, not a law: override it when you can say why.
"""
import argparse, json, sys

def conf_from_evidence(ev):
    kinds = {e.strip().lower() for e in ev}
    n = len(kinds)
    if n == 0:
        return 2
    c = (5 if kinds == {"measured"} else 3) if n == 1 else 6 if n == 2 else 8
    if {"behavioural", "behavioral", "experiment"} & kinds and n >= 3:
        c = 9
    return c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--method", choices=["ice", "pie"], default="ice")
    ap.add_argument("--evidence-confidence", action="store_true")
    a = ap.parse_args()
    ideas = json.load(open(a.file))
    keys = ("impact", "confidence", "ease") if a.method == "ice" else ("potential", "importance", "ease")
    rows = []
    for i in ideas:
        sc = {k: i.get(k) for k in keys}
        if a.method == "ice" and a.evidence_confidence:
            sc["confidence"] = conf_from_evidence(i.get("evidence", []))
        missing = [k for k, v in sc.items() if v is None]
        if missing:
            sys.exit(f"{i.get('id','?')}: missing {', '.join(missing)}")
        for k, v in sc.items():
            if not 1 <= float(v) <= 10:
                sys.exit(f"{i.get('id','?')}: {k} must be 1 to 10")
        score = sum(float(v) for v in sc.values()) / 3
        rows.append((score, i, sc))
    rows.sort(key=lambda r: (-r[0], -float(r[2]["ease"])))
    head = " | ".join(k.capitalize() for k in keys)
    print(f"| Rank | ID | Idea | {head} | {a.method.upper()} | Evidence |")
    print("|---|---|---|" + "---|" * len(keys) + "---|---|")
    for n, (s, i, sc) in enumerate(rows, 1):
        vals = " | ".join(str(sc[k]) for k in keys)
        print(f"| {n} | {i.get('id','')} | {i.get('title','')} | {vals} | {s:.1f} | {', '.join(i.get('evidence', []))} |")

if __name__ == "__main__":
    main()
