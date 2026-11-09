#!/usr/bin/env python3
"""Funnel stage report: each stage's rate for every segment, against a target or the store's own average.
No network, no integrations. Stdlib only.

  stages.py --csv stages.csv
  stages.py --csv stages.csv --targets "Viewed a product=50-70,Added to cart=12-18" --targets-source "Agency targets, 2026"

The CSV (from `shopifyql.py --preset stages --stages-out stages.csv`, or written by hand from any analytics):
  Segment,Value,Visits,Viewed a product,Added to cart,Reached checkout,Purchased
  All,All visits,8000,2400,310,190,120
  Device,mobile,5200,1450,160,95,55
Columns after Value are the stages, top to bottom; name them for the store (for a booking business:
Visits,Viewed a treatment,Clicked Book,Booked). A blank cell or "-" means "not measured". Lines starting
with # are notes. The first row must be the whole store (Segment "All").

For each stage it prints the overall rate with a 95% range, the visits lost, and a verdict against the
target when one is given; then a grid by segment. Without targets a segment is compared with the store's
own rate for that stage, and called higher or lower only when its 95% range doesn't include it.
"""
import argparse, csv, math, sys

def wilson(k, n, z=1.96):
    if not n:
        return None, None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)

def num(x):
    x = (x or "").strip().replace(",", "")
    if x in ("", "-", "n/a"):
        return None
    try:
        return float(x)
    except ValueError:
        sys.exit(f"not a number: {x!r}")

def pct(x, d=1):
    return "n/a" if x is None else f"{x * 100:.{d}f}%"

def parse_targets(s):
    out = {}
    for part in (s or "").split(","):
        if not part.strip():
            continue
        if "=" not in part or "-" not in part.split("=", 1)[1]:
            sys.exit(f"bad target '{part}': use Stage name=low-high, in percent")
        name, rng = part.split("=", 1)
        lo, hi = rng.replace("%", "").split("-", 1)
        out[name.strip().lower()] = (float(lo) / 100, float(hi) / 100)
    return out

def read(path):
    with open(path, newline="") as f:
        rows = [r for r in csv.reader(f) if r and not r[0].lstrip().startswith("#")]
    if len(rows) < 2:
        sys.exit("the CSV needs a header and at least the All row")
    head = rows[0]
    if len(head) < 4:
        sys.exit("the CSV needs Segment, Value and at least two stages")
    stages = [h.strip() for h in head[2:]]
    data = [(r[0].strip(), r[1].strip(), [num(c) for c in (r[2:] + [""] * len(stages))[:len(stages)]]) for r in rows[1:]]
    if data[0][0].lower() != "all":
        sys.exit("the first data row must be the whole store (Segment 'All')")
    return stages, data

def verdict_vs_target(k, n, rng):
    lo, hi = rng
    p = k / n
    a, b = wilson(k, n)
    if p < lo:
        return "Below target" + ("" if b < lo else " (not sure)")
    if p > hi:
        return "Above target" + ("" if a > hi else " (not sure)")
    return "In target"

def segment_note(k, n, ref, rng, minimum):
    if n < minimum:
        return "too few to judge"
    a, b = wilson(k, n)
    if rng:
        lo, hi = rng
        if b < lo:
            return "below target"
        if a > hi:
            return "above target"
        p = k / n
        if lo <= p <= hi:
            return "in target"
        return "near target (not sure)"
    if ref is None:
        return ""
    if b < ref:
        return "lower than the store"
    if a > ref:
        return "higher than the store"
    return "about the same"

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--targets", help='target ranges in percent: "Stage name=low-high,..."')
    ap.add_argument("--targets-source", help="where the targets come from (required with --targets)")
    ap.add_argument("--min", type=int, default=100, help="smallest base for a segment rate (default 100 visits)")
    ap.add_argument("--top", type=int, default=6, help="segment values shown per segment (default 6)")
    a = ap.parse_args()
    targets = parse_targets(a.targets)
    if targets and not a.targets_source:
        sys.exit("say where the targets come from with --targets-source (the person, an agency, or a named study and date)")
    stages, data = read(a.csv)
    unknown = [t for t in targets if t not in [s.lower() for s in stages[1:]]]
    if unknown:
        sys.exit(f"targets for unknown stages: {', '.join(unknown)}; stages are {', '.join(stages[1:])}")

    overall = data[0][2]
    print("## Funnel by stage\n")
    print(f"Reference: {'targets from ' + a.targets_source if targets else 'the store against itself (no targets given)'}. "
          f"Rates under {a.min} visits are shown but not judged.\n")
    print("| Stage | Rate | 95% range | Target | Visits lost | Verdict |")
    print("|---|---|---|---|---|---|")
    lost, below = [], []
    for i in range(1, len(stages)):
        name, k, n = stages[i], overall[i], overall[i - 1]
        label = f"{stages[i - 1]} → {name}"
        rng = targets.get(name.lower())
        tgt = f"{rng[0] * 100:g} to {rng[1] * 100:g}%" if rng else "none"
        if k is None or n is None:
            print(f"| {label} | not measured | | {tgt} | | Not measured: add tracking for this step |")
            continue
        if not n:
            print(f"| {label} | n/a | | {tgt} | | No visits reached the step before |")
            continue
        lo, hi = wilson(k, n)
        flag = " (count higher than the step before: different counting, read with care)" if k > n else ""
        if n < a.min:
            v = "Too few to judge"
        elif rng:
            v = verdict_vs_target(k, n, rng)
            if k / n < rng[0]:
                below.append(((rng[0] - k / n) / rng[0], label))
        else:
            v = "No target: compare segments below"
        lost.append((n - k, label))
        print(f"| {label} | {pct(k / n)} | {pct(lo)} to {pct(hi)} | {tgt} | {max(0, int(n - k)):,} | {v}{flag} |")
    print()
    if lost:
        m = max(lost)
        print(f"- Most visits lost: {m[1]} ({int(m[0]):,}).")
    if below:
        b = max(below)
        print(f"- Furthest below target: {b[1]} ({b[0] * 100:.0f}% under the low end).")
    print("- The stage to work on is decided with the other evidence, not by these numbers alone.\n")

    segs = []
    for seg, val, counts in data[1:]:
        if seg not in segs:
            segs.append(seg)
    for i in range(1, len(stages)):
        name = stages[i]
        k0, n0 = overall[i], overall[i - 1]
        if k0 is None or n0 is None:
            continue
        ref = (k0 / n0) if n0 else None
        rng = targets.get(name.lower())
        print(f"### {stages[i - 1]} → {name}\n")
        print(f"Store: {pct(ref)} of {int(n0):,}" + (f"; target {rng[0] * 100:g} to {rng[1] * 100:g}%" if rng else "") + ".\n")
        print("| Segment | Value | Rate | Base | Compared with " + ("target" if rng else "the store") + " |")
        print("|---|---|---|---|---|")
        for seg in segs:
            shown = 0
            for s, val, counts in data[1:]:
                if s != seg or shown >= a.top:
                    continue
                k, n = counts[i], counts[i - 1]
                if k is None or n is None:
                    print(f"| {seg} | {val} | not measured | | |")
                elif not n:
                    print(f"| {seg} | {val} | n/a | 0 | |")
                else:
                    print(f"| {seg} | {val} | {pct(k / n)} | {int(n):,} | {segment_note(k, n, ref, rng, a.min)} |")
                shown += 1
        print()

if __name__ == "__main__":
    main()
