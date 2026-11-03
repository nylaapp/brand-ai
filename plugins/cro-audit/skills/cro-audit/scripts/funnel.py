#!/usr/bin/env python3
"""Funnel math from supplied numbers. No network, no integrations.

  funnel.py --steps "Sessions=12000,Product views=5400,Add to cart=640,Orders=140"
  funnel.py --csv funnel.csv          # two columns: step,count (header optional)

Prints a markdown table plus the largest leaks and sanity flags. Stdlib only.
"""
import argparse, csv, sys

def parse_steps(s):
    out = []
    for part in s.split(","):
        if "=" not in part:
            sys.exit(f"bad step '{part}': use Name=count")
        n, c = part.rsplit("=", 1)
        out.append((n.strip(), num(c)))
    return out

def num(x):
    try:
        return float(str(x).replace(",", "").replace(" ", ""))
    except ValueError:
        sys.exit(f"not a number: {x!r}")

def read_csv(path):
    rows = []
    with open(path, newline="") as f:
        for r in csv.reader(f):
            if len(r) < 2 or not r[0].strip():
                continue
            try:
                rows.append((r[0].strip(), num(r[1])))
            except SystemExit:
                if rows:  # a non-numeric row after data is a real error
                    raise
    return rows

def pct(a, b):
    return "n/a" if not b else f"{a / b * 100:.1f}%"

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--steps")
    g.add_argument("--csv")
    a = ap.parse_args()
    steps = parse_steps(a.steps) if a.steps else read_csv(a.csv)
    if len(steps) < 2:
        sys.exit("need at least two steps")

    print("| Step | Count | Step conversion | Lost here | Of first step |")
    print("|---|---:|---:|---:|---:|")
    flags, leaks = [], []
    first = steps[0][1]
    for i, (n, c) in enumerate(steps):
        if i == 0:
            print(f"| {n} | {c:,.0f} | | | 100% |")
            continue
        prev = steps[i - 1][1]
        lost = max(prev - c, 0)
        print(f"| {n} | {c:,.0f} | {pct(c, prev)} | {lost:,.0f} | {pct(c, first)} |")
        if c > prev:
            flags.append(f"'{n}' ({c:,.0f}) is larger than '{steps[i-1][0]}' ({prev:,.0f}): different counting method or date range?")
        if c == 0:
            flags.append(f"'{n}' is zero: tracking gap or a broken step?")
        if prev:
            leaks.append((c / prev, lost, n, steps[i - 1][0]))

    print(f"\nOverall: {pct(steps[-1][1], first)} ({steps[-1][1]:,.0f} of {first:,.0f}).")
    if leaks:
        low = min(leaks)
        big = max(leaks, key=lambda x: x[1])
        print(f"Lowest step conversion: {low[3]} -> {low[2]} at {low[0]*100:.1f}%.")
        print(f"Most people lost: {big[3]} -> {big[2]} ({big[1]:,.0f}).")
    if first < 300:
        flags.append(f"first step is {first:,.0f}: directional only, too few for a rate.")
    small = [n for n, c in steps[1:] if 0 < c < 30]
    if small:
        flags.append("fewer than ~30 events at: " + ", ".join(small) + ": directional only.")
    for f in flags:
        print(f"FLAG: {f}")

if __name__ == "__main__":
    main()
