# Rewrite tiers: how far the source is changed

Four depths, from light to complete. The tier decides how much of the source's **wording and structure** survives.
It never changes the rules about **facts**: every claim in the output still traces to the source or to BRAND.md,
nothing first-party is invented, and claim limits still apply (SKILL.md, Step 3).

| Tier | Name | What changes | What stays | Use when | Overlap limits (`scripts/overlap_check.py`) |
|---|---|---|---|---|---|
| 1 | **Match** | Voice, terminology, placeholders, CTA, disclaimer. Sentences are kept unless they clash with the voice | Structure, headings, most sentences | The article is the store's own or its client's and only needs to sound on brand | Reported only, never failed |
| 2 | **Reword** (default) | Every sentence is rewritten in the brand's voice; headings reworded | Section order, the points made, examples | Own or permitted content that should read as the brand's own | Shared 5-word phrases ≤ 12%, longest shared run ≤ 10 words, ≤ 2 verbatim sentences |
| 3 | **Restructure** | New outline: sections reordered, merged or split, new headings, new opening and closing, examples and framing drawn from BRAND.md | The facts and the points, in a new order | Permitted third-party material (a partner, supplier or franchise source) that must not read like the original | ≤ 5%, run ≤ 7, 0 verbatim sentences, ≤ 1 shared heading |
| 4 | **Reimagine** | Everything but the facts: new title, angle, outline and wording. The source is treated as research notes and the post is written fresh in the brand's voice | Only the verifiable facts and figures (never ownable), cited to their primary source | Material that must be clearly distinct from its source; the safest tier | ≤ 2%, run ≤ 5, 0 verbatim sentences, 0 shared headings |

## What each tier means in practice

**1 Match.** Pass 2 of Step 3 as written: open like the brand, match sentence length, swap terms, rewrite the CTA.
Keep the author's sentences wherever they already fit.

**2 Reword.** No sentence is carried over untouched. Change the opening and closing, vary how each point is
introduced, and replace the source's examples' phrasing (the examples themselves stay). Headings are reworded, not
reordered.

**3 Restructure.** Do Pass 1 (map the source) then build a **new outline before writing**: group the points by what
the reader needs first, not by the source's order; give each section a new job-based heading; write a new
introduction and close from BRAND.md's patterns. Keep one summary line of the source's argument; drop its pacing,
transitions and signature turns of phrase. Say in the report which sections were merged, split or moved.

**4 Reimagine.** Do not rewrite sentences at all. Extract a fact sheet from the source (claims, figures, steps,
definitions), each marked with where it came from. Close the source. Then write the post from the fact sheet and
BRAND.md: new title and angle (a different search intent if the store's keywords call for it), new outline, the
brand's own examples from Catalog and Identity. Statistics, studies and regulatory statements are cited to their
**primary source** (found and checked via `content-fact-check`), not to the source article, and a figure you cannot
trace to a primary source is dropped. Do not add claims the source did not make. A post at this tier is a new
article that uses the source's facts, so the report says "derived from <url>" for the record.

## Choosing a tier

- Ask once in Step 1, with the four names and the one-line "use when", unless the person already named one. Say the
  default if they don't mind: **Reword**.
- **Own or client content, light touch:** Match. **Own content that should read as the brand's:** Reword.
- **Anything from a different company, even with permission:** Restructure or Reimagine, never lower. The ownership
  gate in "Source from a URL" still applies first: no tier makes it acceptable to copy a competitor's article.
- A person asking for "a lower overlap" or "so it can't be flagged" moves up one tier, and is told that a tier lowers
  wording overlap, it does not make copying permitted.
- **Batches** use one tier for the whole run, stated in the batch summary.
- Images are not affected by the tier: they follow "Source images" (SKILL.md).

## The overlap check

Run after the rewrite, before the quality gate:

```bash
python3 scripts/overlap_check.py <run folder>/source.md <run folder>/<handle>.html --tier <tier>
```

It reports the share of the rewrite made of 5-word phrases also in the source, the longest run of shared words, the
verbatim sentences and the headings kept. Over the tier's limits: rewrite the flagged sentences (it prints them) and
re-run, up to three times; if it still fails, say so in the report instead of passing it. Match is reported only.
Python 3 standard library, no installs; on Windows use `python`. **It is a wording check, not legal clearance:** it
can't see copied structure, ideas or images, and a pass does not replace permission to reuse the source.
