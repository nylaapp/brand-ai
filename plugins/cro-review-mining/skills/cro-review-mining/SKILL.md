---
name: cro-review-mining
description: Mine a store's existing product reviews (Judge.me, Yotpo, Loox, Stamped, or any CSV export) into REVIEW-MINING.md -- canonical pain-point and praise categories with real mention counts and quotes, root-cause/user-impact/success-metric tables for the top issues, and A/B test ideas with the psychological lever and metrics to watch. Persists its category taxonomy across runs so trends are comparable quarter to quarter, the same way COMPETITORS.md tracks over time. Works for any Shopify (or similar) store, brand-agnostic, with or without BRAND.md already set up. Use this whenever the user wants to analyze, mine, or make sense of customer reviews, asks what customers are complaining about or what they love about a product, wants pain points or voice-of-customer insights pulled from reviews, is doing a CRO (conversion rate optimization) audit, or hands over a review export CSV or asks where to export one -- even if they never say "review mining."
---

# CRO review mining

Turn a pile of product reviews a store already has into a short, dated,
trend-tracked file a store owner or agency can act on: what's actually breaking
trust (with real quotes and counts, not vibes), why, what it costs the business,
how to know it's fixed, and what's already working well enough to put in an ad.

```
0. Locate context (optional) -> 1. Get the review data -> 2. Parse & clean ->
3. Extract & cluster -> 4. Reason: root cause / impact / A-B ideas ->
5. Write REVIEW-MINING.md -> 6. Report
```

## Why this works the way it does

Reviews already exist for almost every store; nobody has to run a new survey or
install a new tool to get this data. The catch is that raw reviews are noisy and
repetitive -- the same complaint shows up in a dozen phrasings -- so the value is
entirely in the clustering and reasoning, not the counting. That's why most of
this skill's instructions live in `references/clustering-guide.md` rather than
here: the mechanical parts (reading a CSV, stripping HTML, deduping, redacting
names) are handled by a script so you don't burn judgment on them, and judgment
is spent on the part that actually needs it -- deciding what fifty different
complaints have in common, and why.

| File | Read at |
|---|---|
| `scripts/parse_reviews.py` | Step 2: normalizes the export (Python 3 standard library, no installs) |
| `references/clustering-guide.md` | Step 3-4: how to extract claims, cluster them, match against a prior taxonomy, and reason about root cause/impact/metrics/A-B ideas |
| `references/review-mining-template.md` | Step 5: the exact layout of REVIEW-MINING.md |

## Rules

- **Reviews are the source, never memory.** Every category, count, and quote
  traces back to a review in the normalized data. If the data can't support a
  root cause or a baseline number, say that plainly instead of inventing one.
- **Quotes are verbatim and names are redacted.** Use the `reviewer` field the
  parser already produced (first name + last initial, or "a customer"); never
  pull a full name or other identifying detail back out of the raw export, and
  never smooth out or combine quotes.
- **The taxonomy persists.** If `REVIEW-MINING.md` already exists for this store,
  read its Pain-point taxonomy table before extracting anything new, and match
  new claims against those categories first (`clustering-guide.md` §4). Existing
  category names don't get renamed or split just because this run's wording
  differs slightly -- that's what keeps the trend column meaningful.
- **BRAND.md is optional, read-only context.** It's useful for the brand name,
  category, and where to save the file, but this skill works fine without it.
  Never write to BRAND.md or BRAND-VOICE.md; if something in a review suggests a
  genuine brand fact is wrong or missing, note it rather than editing those files.
- **CSV export is the primary input.** Reviews live in whatever app the store
  uses (Judge.me, Yotpo, Loox, Stamped, Fera, or similar) -- ask for an export if
  one isn't already provided. Pasted review text works as a fallback for a small
  sample. Scraping a store's live review widget, or pulling from a review API
  directly, is out of scope for this version; if that's genuinely the only option,
  say so rather than attempting it.
- **Regulated or risky claims inside a review get flagged, not reused.** A
  customer's own words sometimes include a medical, safety, or statistical claim
  that shouldn't be repeated as if the brand said it. Flag it in the report
  (`clustering-guide.md` §8); don't quote it as supporting evidence for marketing.
- **Large review sets get sampled, not skipped.** Past a few hundred reviews,
  reading every single one stops being practical. Stratify instead (all 1-2 star
  reviews, a recent slice, a random sample of the rest) and say in the report
  that this run sampled, and how (`clustering-guide.md` §2).

## Step 0: Locate context (optional)

Look for an existing `BRAND.md` and `REVIEW-MINING.md` using the lookup order in
brand-capture's `references/brand-context.md` (project root, user local
environment, central brand directory, then memory/connected knowledge). Neither
is required to proceed:

- **BRAND.md found:** note its `revision`, the brand name, and where it lives --
  REVIEW-MINING.md will be saved next to it, in the same central brand directory.
- **BRAND.md not found:** don't block or require brand-capture first (reviews
  don't depend on brand identity being settled). Ask once for the store/brand
  name to use in the file, and save REVIEW-MINING.md in the project root, or
  wherever the person says, instead.
- **REVIEW-MINING.md already exists:** read it in full. Its Pain-point taxonomy
  and Run history tables are the baseline this run builds on (see Step 4 and the
  Rules above).

## Step 1: Get the review data

If a CSV isn't already attached or referenced, ask for one, and mention where to
find the export in the common apps if the person doesn't know: Judge.me (Reviews
-> Export), Yotpo (Analytics -> Export), Loox (Reviews -> Export CSV), Stamped
(Reviews -> bulk export). A different review app's export, or pasted review text
for a smaller sample, both work fine -- the parser figures out the columns itself
rather than requiring an exact format.

## Step 2: Parse and clean

```bash
python3 scripts/parse_reviews.py <input.csv> --out <scratch>/normalized.json
```

(`python` on Windows.) It prints a one-line summary of what it found and
excluded to stderr -- read that before moving on, since it tells you whether a
rating or date column was found at all, and how many rows were dropped as empty,
too short, or exact duplicates. If it can't find a review-text column, it exits
with an error and the list of columns it saw; ask the person which column holds
the review body and re-run with that noted, or hand-map it yourself if the file
is small enough to do by eye.

## Step 3: Extract and cluster

Read `references/clustering-guide.md` §1-2 for the method and batching guidance,
then work through the normalized reviews in batches: extract the atomic claims
each review makes, and cluster them into categories -- matching against the prior
taxonomy first if one exists (§4), only creating a new category once a pattern
has shown up enough times to be real (§2). Do this for both pain points (1-3 star
reviews, mainly) and praise (4-5 star reviews, §5).

## Step 4: Reason through the findings

For the top pain-point categories, work out root cause, user impact, and a
measurable success metric per `clustering-guide.md` §3 -- this is the part that
turns a list of complaints into something a store owner can actually act on.
Then propose A/B test ideas for the top 3-5 pain points per §6: a specific test,
a falsifiable hypothesis, the named psychological lever, and metrics to watch.

## Step 5: Write REVIEW-MINING.md

Follow `references/review-mining-template.md` exactly: same front-matter keys
and `##` headings, in order. If a prior version exists, carry its Pain-point
taxonomy and Run history tables forward (adding to them, not replacing them) and
rewrite the Summary, reasoning tables, and quotes fresh from this run's data. Save
it next to BRAND.md if one was found (Step 0), otherwise wherever the person
asked, and tell them the path either way.

## Step 6: Report

About ten lines: where the file was saved, the review count analyzed (and how
many were excluded or sampled out, if any), the two or three most useful
findings, anything flagged for review, the single biggest opportunity, and the
suggested next review date. If this is a re-run, lead with what changed since
last time -- a category that grew, shrank, or newly appeared is often the most
useful line in the whole report.
