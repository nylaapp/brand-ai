# Funnel math

Input is numbers the person supplies, as ordered steps from top to bottom (for example
Sessions, Product views, Add to cart, Checkout, Orders; or Sessions, Booking page views,
Form starts, Submissions). Everything here is `[Reported]`: say the source, the date range and
that you did not verify it.

## What `scripts/funnel.py` returns

- **Step conversion**: step N divided by step N-1.
- **Overall conversion**: last step divided by first.
- **Drop-off** at each step (people lost).
- **Largest leak**: the step with the lowest step conversion, and the step where the most
  people are lost. They are often different; report both.
- **Sanity flags**: a step larger than the one before it (usually a different counting method
  or date range), a zero step, and small samples.

## Reading it

- A leak shows where to look, not why. Pair it with the heuristic findings for that stage.
- Compare against a target only when it has a source: the person's or agency's own targets, or a
  published benchmark you looked up, with its publisher, date and definition
  (`funnel-stages.md` section 3). Otherwise compare the store with itself: segment against segment,
  or this period against the last. `scripts/stages.py` does both.
- Different tools count differently (sessions vs. users, orders vs. checkouts started). If
  steps come from different tools, say so.
- Mix of device or traffic source hides the picture. If the person can read the same numbers
  for mobile and desktop, run the script twice and compare.

## Small samples

Directional only when the first step is under a few hundred, or any step has fewer than about
30 events. Say "directional: too few to rely on a rate" and prefer counts to percentages. Do
not call a difference between two small rates real. Name the minimum more data needed before
a test could be read, or say to collect more.

## Never

Predict a lift, project revenue from a rate, or call a change "significant" without a test.
