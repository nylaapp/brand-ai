#!/usr/bin/env python3
"""Read a finished (or running) A/B test from visitor and conversion counts. Stdlib only.

  ab_result.py --control 10000,300 --variant 10050,342
  ab_result.py --control 10000,300 --variant 10050,342 --split 0.5

Reports rates, relative lift, a two-sided two-proportion z-test, a 95% interval on the
difference, and a sample ratio mismatch (SRM) check on the visitor split. If SRM fails the test
is invalid: fix the assignment before reading any lift. This does not correct for peeking: read
the test once, at the planned sample size (see references/experiment-design.md).
"""
import argparse, math, sys
from statistics import NormalDist

def pair(s):
    try:
        v, c = s.split(",")
        v, c = int(v), int(c)
    except ValueError:
        sys.exit(f"bad value '{s}': use visitors,conversions (for example 10000,300)")
    if c > v or v <= 0:
        sys.exit(f"'{s}': conversions cannot exceed visitors")
    return v, c

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--control", required=True)
    ap.add_argument("--variant", required=True)
    ap.add_argument("--split", type=float, default=0.5, help="planned share of traffic to control (default 0.5)")
    a = ap.parse_args()
    n1, x1 = pair(a.control)
    n2, x2 = pair(a.variant)
    p1, p2 = x1 / n1, x2 / n2
    nd = NormalDist()
    pp = (x1 + x2) / (n1 + n2)
    se0 = math.sqrt(pp * (1 - pp) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se0 if se0 else 0.0
    p = 2 * (1 - nd.cdf(abs(z)))
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    lo, hi = (p2 - p1) - 1.96 * se, (p2 - p1) + 1.96 * se
    tot = n1 + n2
    e1, e2 = tot * a.split, tot * (1 - a.split)
    chi = (n1 - e1) ** 2 / e1 + (n2 - e2) ** 2 / e2
    srm_p = math.erfc(math.sqrt(chi / 2))  # chi-square, 1 degree of freedom
    print(f"Control: {x1:,}/{n1:,} = {p1*100:.2f}%   Variant: {x2:,}/{n2:,} = {p2*100:.2f}%")
    print(f"Difference: {(p2-p1)*100:+.2f} points ({(p2/p1-1)*100 if p1 else float('nan'):+.1f}% relative), 95% interval {lo*100:+.2f} to {hi*100:+.2f} points")
    print(f"z = {z:.2f}, p = {p:.4f} (two-sided)")
    print(f"Split check: expected {a.split:.0%}/{1-a.split:.0%}, saw {n1/tot:.1%}/{n2/tot:.1%}, SRM p = {srm_p:.4f}")
    if srm_p < 0.001:
        print("INVALID: sample ratio mismatch. The groups were not split as planned, so the result cannot be trusted. Find the assignment or tracking bug first. No reading is given.")
        return
    if min(x1, x2) < 100:
        print("FLAG: under about 100 conversions in an arm. Directional only.")
    if p < 0.05 and lo * hi > 0:
        print("Reading: the interval excludes zero. A real difference is likely, but check it was read at the planned sample size and against the guardrail metrics.")
    else:
        print("Reading: no reliable difference seen. That is not proof the change does nothing; the test may be too small to see it.")

if __name__ == "__main__":
    main()
