# REVIEW-MINING.md template (schema 1.0)

Keep the front-matter keys and the `##` headings in this order. Replace each
`<...>` and delete the guidance in *italics*. Flat `key: value` front matter;
dates `YYYY-MM-DD`.

Unlike `COMPETITORS.md`, this file is **not fully replaced** on each run: the
Pain-point taxonomy and Run history tables carry forward and grow, so the file
shows a trend over time, not just a snapshot. Everything else (Summary, the
reasoning tables, quotes) is rewritten fresh each run from the current data.

---

```markdown
---
review_mining_schema: 1.0
brand: <brand or store name>
brand_md_revision: <the BRAND.md revision this run read, or "none (no BRAND.md found)">
source: <Judge.me / Yotpo / Loox / Stamped / other, as given>
last_run: <YYYY-MM-DD>
runs_completed: <N>
reviews_analyzed_this_run: <N>
reviews_analyzed_total: <N, cumulative across runs>
taxonomy_version: <N, bump only when a category is added, merged, or retired>
next_review: <YYYY-MM-DD, about 3 months later>
analyzed_by: cro-review-mining 1.0
---

# <Brand>: review mining (<YYYY-MM-DD>)

> Mined from <N> customer reviews exported from <source>, covering <date range>.
> This is what customers are saying, not brand facts: brand facts live in
> BRAND.md. Re-run the cro-review-mining skill with a fresh export to update it.

## Summary
*3 to 6 bullets a store owner would act on this week.*
- <the single biggest pain point, with its mention count and trend>
- <the single biggest "why they love it" reason>
- <anything that moved notably since the last run>

## Pain-point taxonomy
*Persistent across runs — see clustering-guide.md §4. New rows get a "first seen"
date; existing rows keep their name and only their counts and trend change.*

| Category | First seen | Mentions (this run) | Mentions (prior run) | Trend | What it is |
|---|---|---|---|---|---|
| <name> | <date> | <n> | <n or "—" if new> | <up / down / stable / new / resolved> | <one line> |

## Root cause, impact, and success metric (top pain points)
*The top 3 to 6 categories by mention count, reasoned through per
clustering-guide.md §3. Only the categories with enough signal to say something
real — don't force a row for a category you can't say anything useful about.*

| Pain point | Root cause | User impact | Success metric (baseline → target) |
|---|---|---|---|
| <category> | <structural reason, inferred from the pattern> | <concrete business consequence> | <measurable, with today's baseline from this data> |

## What customers love
*Same clustering method, run on 4 and 5-star reviews (clustering-guide.md §5).*

| Reason | Mentions | Example quote |
|---|---|---|
| <reason> | <n> | "<verbatim quote>" — <redacted reviewer>, <date> |

## A/B test ideas
*Top 3 to 5 pain points, one idea each (clustering-guide.md §6).*

| Pain point | Test idea | Hypothesis | Psychological lever | Metrics to watch |
|---|---|---|---|---|
| <category> | <specific, buildable change> | <falsifiable belief being tested> | <named mechanism> | <specific, instrumentable metrics> |

## Flagged for review
*Anything found in a review that shouldn't be reused as-is: regulated/medical
claims, quality claims that contradict marketing, anything needing a human look
before it's quoted anywhere customer-facing (clustering-guide.md §8). Leave this
section out entirely if nothing was flagged.*

## Not covered
*Languages excluded, how large a sample was read vs. the full export if
stratified, reviews dropped as spam or unusable, anything the data couldn't
settle.*

## Run history
*One row per run, oldest first. Never remove a row.*

| Date | Reviews this run | Reviews total | Categories added | Notable shifts |
|---|---|---|---|---|
| <YYYY-MM-DD> | <n> | <n> | <names, or "none"> | <one line, or "first run"> |

## Sources
| Input | Reviews | Date range | Seen on |
|---|---|---|---|
| <filename or "pasted text"> | <n rows in file> | <range> | <YYYY-MM-DD> |
```
