#!/usr/bin/env python3
"""How many visitors an A/B test needs, and roughly how long it takes. Stdlib only, no network.

  sample_size.py --baseline 0.03 --mde 0.10 --daily-visitors 1200
  sample_size.py --baseline 0.03 --mde-abs 0.003 --variants 3 --power 0.8 --alpha 0.05

--baseline      current conversion rate of the thing being measured (0.03 = 3%).
--mde           smallest RELATIVE change worth detecting (0.10 = 10% better than baseline).
--mde-abs       the same as an absolute change in rate (0.003 = +0.3 points). Use one of the two.
--variants      total arms including control (default 2). More than 2 applies a Bonferroni
                correction (alpha divided by the number of variant-vs-control comparisons).
--daily-visitors  visitors per day entering the test (all arms together), to estimate duration.
Two-sided test on a difference in proportions. The answer is a planning number, not a promise.
"""
import argparse, math, sys
from statistics import NormalDist

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", type=float, required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--mde", type=float)
    g.add_argument("--mde-abs", type=float)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.80)
    ap.add_argument("--variants", type=int, default=2)
    ap.add_argument("--daily-visitors", type=float)
    a = ap.parse_args()
    if not 0 < a.baseline < 1:
        sys.exit("--baseline must be a rate between 0 and 1, e.g. 0.03")
    p1 = a.baseline
    p2 = p1 * (1 + a.mde) if a.mde is not None else p1 + a.mde_abs
    if not 0 < p2 < 1 or p2 == p1:
        sys.exit("the target rate must be between 0 and 1 and differ from the baseline")
    comps = max(a.variants - 1, 1)
    alpha = a.alpha / comps
    z_a = NormalDist().inv_cdf(1 - alpha / 2)
    z_b = NormalDist().inv_cdf(a.power)
    pbar = (p1 + p2) / 2
    n = ((z_a * math.sqrt(2 * pbar * (1 - pbar)) + z_b * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / (p2 - p1) ** 2
    n = math.ceil(n)
    total = n * a.variants
    print(f"Baseline {p1*100:.2f}% -> target {p2*100:.2f}% ({(p2/p1-1)*100:+.1f}% relative, {(p2-p1)*100:+.2f} points)")
    print(f"alpha {a.alpha} (two-sided){' / Bonferroni '+str(comps)+' = '+format(alpha,'.4f') if comps>1 else ''}, power {a.power:.0%}, {a.variants} arms")
    print(f"Visitors needed per arm: {n:,}   total: {total:,}")
    print(f"Conversions expected per arm at baseline: about {round(n*p1):,}")
    if a.daily_visitors:
        days = math.ceil(total / a.daily_visitors)
        weeks = max(math.ceil(days / 7), 1)
        print(f"At {a.daily_visitors:,.0f} visitors a day: about {days} days; run whole weeks, so plan {weeks} week(s) ({weeks*7} days).")
        if days < 14:
            print("NOTE: under two weeks. Still run at least two full weekly cycles so weekday/weekend mix is covered.")
        if days > 56:
            print("WARNING: over eight weeks. The effect is probably too small to test here; test a bigger change, a higher-traffic page, or a metric closer to the click.")
    if n * p1 < 100:
        print("WARNING: under about 100 conversions per arm. Results will be noisy even if the maths says it is enough.")

if __name__ == "__main__":
    main()
