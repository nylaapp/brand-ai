# Deep cleanup: zero-based tag budgeting

Start from zero: assume no tag deserves to load until it proves what it answers and what it costs. Measure the page with every tag off, add tags back one group at a time, and keep only what pays for itself, loaded no earlier than it needs to be.

## 1. Every tag needs an owner and a question

Build the list from the audit inventory (one row per tool, not per request). For each tag, get from the client:

- **Owner:** the person who reads its data or uses it for ads.
- **Question it answers:** "which campaigns bring buyers", "where do visitors stop on the product page", "which retargeting audience". A tag without a question is a removal candidate.
- **Last used:** when someone last looked at its data or used it in a campaign.
- **Where it is needed:** all pages, some templates, checkout only, only during a study.

Write these into the load policy (ANALYTICS.md section 7) before measuring.

## 2. A safe benchmark environment

The benchmark blocks tags in the test browser; it never removes them from the store.

- `scripts/tag_cost.py` runs Lighthouse with URL patterns blocked: all-on, all-off, then each group added back (`--mode addback`) or each group removed (`--mode removal`). Median of at least 5 runs per row on the final pass; 3 is fine for a first look.
- This works on the live URL or a preview, and covers store-wide installs (Shopify app pixels, GTM) that a preview theme cannot switch off.
- Add client-specific groups with `--groups` (first-party or server-side endpoints, an unusual vendor).
- For theme code and app embeds you can also build a real all-off variant: an unpublished duplicate theme with them removed. Pixels and the tag manager stay on there, so combine it with blocking.
- Test pages: home, a top landing page for paid traffic, a product or service page, and cart. Mobile form factor first.
- Lab caveats: one machine and network, no real users, no INP in the lab (Total Blocking Time and main-thread time are the proxies). Use the numbers to rank tags against each other.

## 3. Measure

1. `all-on` and `all-off` on each test page. The gap is the total tag tax. If it is small (for example under 200 ms TBT and under 100 KB), say so: the deep cleanup is about hygiene and risk, not speed.
2. Add back in order of business importance, so the essentials are measured on a realistic base: consent tool, tag manager and analytics base, ad conversion tags, ad base pixels, email and SMS, call tracking, affiliate, chat, reviews, heatmaps, A/B testing.
3. Read the Lighthouse third-party table from the all-on runs for the per-vendor split (main-thread ms, KB).
4. Record cost per group in the load policy.

## 4. Decide, tag by tag

| Decision | When |
|---|---|
| **Keep, at load** | Answers a current question, is needed on landing (captures campaign data or click ids, or consent) |
| **Keep, deferred** | Needed, but not in the first seconds: after load, on idle, on first interaction |
| **Keep, only where used** | Needed on some templates only (reviews on product pages, call tracking where numbers are shown) |
| **On demand** | Needed only during a study or test: heatmaps and replay, A/B testing. Off by default; on with an end date |
| **Move** | Better from a sandboxed pixel (off the main thread) or server-side than from page code |
| **Remove** | No owner, no question, duplicated, or the client stopped using the tool |

Rules:
- **One heatmap or replay tool at a time**, only while a study with a question and an end date is running, sampled where the tool allows, consent-gated, and removed when the study ends.
- **Cost needs a reason.** A tag costing more than the rest of the analytics stack together needs a named owner and a question worth that cost, or a cheaper loading strategy.
- **Never trade a Tier 1 event for speed.** If a conversion tag is expensive, change how it loads; do not drop the conversion.

Present the decisions as a table (tag, owner, question, cost, decision, why) and get approval per tag. The client decides; we recommend.

## 5. Implement

Follow `load-timing.md` for each kept tag. Work in this order: removals (lowest risk, biggest certainty), template conditions, deferrals, on-demand switches, moves. Use the setup skill's playbooks for anything that touches a destination path (P1, P2, P6) and its rollback kit (P12). Re-verify Tier 1 and Tier 2 events in the accept state after each batch.

## 6. Re-measure and keep it

1. Re-run `tag_cost.py` all-on on the same pages, same settings: report before and after.
2. Field data after 28 days: PageSpeed Insights or CrUX for the origin and key URLs (INP, LCP), compared with the 28 days before. Say plainly if field data is too sparse to judge.
3. ANALYTICS.md section 7: every tag's decision, cost, loading rule and a review date (default: 6 months; studies: their end date).
4. Rule in section 6: no new tag without a load-policy row (owner, question, timing, cost measured).
