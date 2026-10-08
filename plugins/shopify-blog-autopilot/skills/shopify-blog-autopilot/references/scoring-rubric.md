# Scoring rubric and guardrails

Contents: 1. Candidate schema · 2. Factor anchors · 3. Score formula · 4. Guardrails · 5. Worked examples

The rubric answers one question: **is this post worth one of this week's limited slots?** Review time is the real constraint. Two great drafts a week that get published beat seven that sit unreviewed.

---

*The worked examples in this file (and in `handoff.md`) use a fictional sock brand for illustration. They say nothing about your brand's industry, market or currency.*

## 1. Candidate schema

```json
{
  "id": "gsc-<keyword>",
  "trigger": "gsc_striking",
  "triggers": ["gsc_striking", "store_new_product"],
  "title_idea": "<Working title idea for the keyword>",
  "primary_keyword": "<keyword>",
  "secondary_keywords": ["<variant 1>", "<variant 2>"],
  "cluster": "<cluster>",
  "intent": "commercial",
  "post_type": "buying guide",
  "action": "new",
  "refresh_target": null,
  "evidence": [
    {"source": "gsc", "detail": "1,240 impressions, avg position 11.4, 18 clicks (last 28 days)"},
    {"source": "shopify", "detail": "New product '<Product A>' created 2026-09-27", "url": "https://<store>/products/<product-a>"}
  ],
  "products": ["<product-a>"],
  "deadline": null,
  "factors": {"demand": 4, "business_value": 5, "winnability": 4, "uniqueness": 3, "urgency": 3}
}
```

- `trigger` is the primary trigger. `triggers` lists every trigger merged into this candidate.
- **Trigger ids:** `store_new_product`, `store_new_collection`, `store_restock`, `store_rising_product`, `store_conversion_gap`, `gsc_striking`, `gsc_decay`, `gsc_gap`, `voc`, `competitor`, `trend`, `occasion`, `ai_citation_gap`, `periodic`, `manual`.
- **`intent`** is one of `informational`, `commercial`, `transactional`, `post_purchase` or `brand`.
- **`action`** is `new` or `refresh`. The script may convert `new` to `refresh` when an older article already targets the keyword.
- **`deadline`** is the publish-by date: for occasions, the occasion date minus 14 days; for launches, the launch date. Use null when there's no deadline.
- **`id`** should be stable across runs: `<trigger>-<keyword-slug>`. A stable id lets a backlog item be updated instead of duplicated.

## 2. Factor anchors (1–5)

Score from the evidence in front of you. If you can't point to evidence for a 4 or 5, it's a 3 or lower.

| Factor | 1 | 3 | 5 |
|---|---|---|---|
| **demand**: do people search for or ask about this? | No visible demand | PAA or autocomplete present, some forum threads, or GSC impressions near the threshold | GSC impressions well above the threshold, or strong PAA, forum and autocomplete presence, or a recurring question from customers |
| **business_value**: does it sell or support what the brand sells? | Unrelated to the catalog (auto-skipped) | Adjacent category, indirect link to products | Directly features core or bestselling products, or a new launch |
| **winnability**: can this store rank or get cited? | SERP dominated by huge publishers or marketplaces with deep content | Mixed SERP, some small brands and forums rank | Weak or outdated results, forums ranking, or already on page 2 in GSC |
| **uniqueness**: can the brand add something others can't? | Pure commodity info | Brand perspective, but no first-party data | First-party data, testing, maker process, or the brand's own product specifics |
| **urgency**: does it lose value if it waits? | Evergreen, no time pressure | Moderate: a trend building, or a competitor just published | Occasion window open, launch this week, or a fast-rising trend |

Use the occasion script's `suggested_urgency` for occasion candidates. A decay refresh usually has urgency 3–4, because traffic is leaking every week it waits.

## 3. Score formula (implemented in `scripts/score_opportunities.py`)

```
weighted = 0.25·demand + 0.25·business_value + 0.20·winnability + 0.15·uniqueness + 0.15·urgency   (1–5)
score    = (weighted − 1) / 4 × 100                                                                  (0–100)
+5 per extra independent source family (store, search, voc, competitor, trend, occasion), max +10
+5 if the intent is more than 10 points below its content_mix target over the last 90 days (needs ≥3 recent posts)
```

Rough feel: all 3s = 50 (backlog). All 4s = 75 (write). A 3.6 average ≈ 65 (the default write threshold).

Decision bands (from the profile): `score ≥ thresholds.write` → write, `≥ thresholds.backlog` → backlog, otherwise skip.

## 4. Guardrails (applied in this order)

1. **Excluded topic:** any `brand.excluded_topics` entry appears in the keyword, title or cluster → skip.
2. **No brand fit:** `business_value = 1` → skip. Traffic that can't convert isn't worth a slot.
3. **Deadline passed** → skip.
4. **Already covered by autopilot:** a ledger topic in the last 180 days matches the keyword → skip.
5. **Existing store article matches the keyword** (hidden drafts included):
   - a hidden draft → skip (a draft is already waiting for review)
   - published less than 90 days ago → skip (cannibalization risk, too soon to refresh)
   - published 90+ days ago → convert to **refresh** of that article
6. **Cluster cooldown:** an autopilot post in the same cluster within `cluster_cooldown_days` → backlog. This is overridden when the candidate's deadline falls before the cooldown ends plus 7 days, so a seasonal deadline isn't missed.
7. **Rank and limit:** deadlines within 45 days first, then the nearest deadline, then score. Take up to `max_posts_per_run`, never more than the weekly remainder. The rest go to backlog as "weekly cap reached" or "per-run limit".
8. **Periodic rule:** if nothing was written, a slot is free and the last autopilot post was at least `periodic.max_gap_days` ago, promote the best backlog item scoring at least `thresholds.periodic_min`.

Backlog items older than `backlog_expiry_days` are dropped. Evidence goes stale, and if the signal still exists it will be rediscovered with fresh numbers.

## 5. Worked examples

**A. New product plus a striking-distance query (write).** "<Product A>" launched two days ago. GSC shows "<keyword>" at position 11 with 1,240 impressions, and no article targets it. Factors 4/5/4/3/3 → weighted 3.95 → 73.8, +5 multi-signal (store + search) → 78.8 → **write**.

**B. The same topic, but a post from last month exists (skip).** `/blogs/<blog>/<existing-post-handle>` was published 35 days ago → skip: "covered recently, cannibalization risk". If it were 200 days old, it would become a **refresh** instead.

**C. Holiday gift guide during a cooldown (write, override).** Today is 2026-09-29, and the holiday gifting window is open (publish by Dec 11). An autopilot post in the "gifts" cluster went out 10 days ago, so the cooldown runs to Oct 10. The deadline is not before the cooldown end plus 7 days, so the cooldown holds → **backlog** until Oct 10. It will score high on the next run after that and still make its deadline. (Had the deadline been Oct 12, the override would apply.)

**D. A competitor post in an adjacent category (backlog or skip).** A competitor posts about a topic in a category the brand doesn't sell. Business value 2, demand 4, winnability 2, uniqueness 2, urgency 2 → 2.5 → 37.5 → **skip**.

**E. A quiet fortnight (periodic).** Nothing crossed 65 today. The last autopilot post was 15 days ago, and the top backlog item scores 58 (≥ 55) → **promoted** by the periodic rule.
