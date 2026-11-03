# Web analytics analysis (stream 4)

Input is whatever the person can export or read off their analytics (Shopify Analytics, GA4, or any
tool) as numbers, CSVs or screenshots. Everything here is `[Reported]`: name the tool, the date
range and the segment, and say you did not verify it. Never ask the person to connect anything.

## 1. Validate the data first

Before reading any rate, check the numbers can be trusted. Report the result in the audit.

| Check | How | If it fails |
|---|---|---|
| Orders match | Compare orders (or booking requests) in the store admin with transactions in analytics for the same dates | A gap over a few percent means lost or double tracking: say so, send to `analytics-audit` |
| No duplicate firing | One purchase event per order; one pageview per page | Duplicates inflate conversion; fix first |
| Consent effect | A cookie banner can hide a share of visitors from analytics | Rates are of tracked visitors only: say so |
| Bots and internal traffic | Spikes of sessions with zero engagement; the team's own visits | Filter or note them |
| Date range | At least two full weeks, ideally four or more, with no big promotion unless it is the subject | Note seasonality and promotions |
| Same definitions | "Session", "user", "conversion" mean the same in every table | State the definitions used |

## 2. The reports to ask for

Ask for as many as the person can give, in this order. Don't block on a missing one.

1. **Overall funnel** (sessions to product or booking-page views to add-to-cart or form start to
   checkout or submit to order). Run `scripts/funnel.py`.
2. **The same funnel by device** (mobile, desktop, tablet). A mobile gap is the commonest big finding.
3. **By traffic source** (organic, paid, social, email, direct). Different intent converts differently.
4. **New vs returning visitors.**
5. **Landing pages**: the top entry pages with entrances, engagement and conversion. Which entry pages
   lose people?
6. **Checkout or booking steps**: drop-off at each step, and the payment or form errors if reported.
7. **Product or service level**: views, add-to-cart rate and purchase rate per item. Which popular
   items convert poorly?
8. **Site search**: the top searches, searches with no results, and how searchers convert.
9. **Order value and repeat rate** (average order value, share of repeat customers) when the goal is
   revenue, not only orders.
10. **Pages visited before conversion** (the path), if available.

## 3. Reading it

- Find the **largest leak by segment**, not overall: the step and the segment where the most
  people are lost and where the rate is lowest. They are often different; report both.
- **Compare a segment with another segment of the same store**, not with a made-up benchmark.
- **Sample sizes.** Apply the small-sample rule from `funnel-math.md` to each segment: a segment of a
  few dozen sessions gives a lead, not a rate.
- **Pair every leak with a cause to look for** from the other streams (the heuristic findings for
  that step, recordings of that page, review and survey themes). A leak with no cause yet becomes an
  "Investigate" item (`prioritization.md`).
- **Trends over averages.** A step that fell last month points to a change (a theme edit, an app, a
  campaign); a step that has always been low points to a design problem.

## 4. What to write down

A table per segment with the funnel from `funnel.py`; the validity checks and their results; the
largest leak(s) by segment; and the open questions the numbers can't answer.
