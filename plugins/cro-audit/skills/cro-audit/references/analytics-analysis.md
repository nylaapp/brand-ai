# Web analytics analysis (stream 4)

Input is the store's own analytics read through the Shopify CLI (read-only), or whatever the person can
export or read off their analytics (Shopify Analytics, GA4, any tool) as numbers, CSVs or screenshots.
Everything here is `[Reported]`: name the source, the date range and the segment. Never ask the person
to connect a new tool.

## 0. Getting the numbers through the Shopify CLI (read-only)

`scripts/shopifyql.py` runs ShopifyQL with `shopify store execute`, queries only. It refuses anything
that looks like a write and never passes `--allow-mutations`.

1. `--check` shows the shop, the connection's scopes and whether analytics is ready. Analytics needs
   `read_reports` (and Shopify's protected customer data level for reports); sales by channel needs
   `read_orders`. A `write_*` scope on the connection is never used.
2. If access is missing, the person decides whether to grant it and runs the command themselves, for
   example `shopify store auth -s <shop>.myshopify.com --scopes <their current scopes>,read_reports,read_orders`.
   Don't run it, and don't suggest dropping their existing scopes. If they'd rather not, use exports.
3. `--preset check-data` first (sessions per day), then `--preset all` on the clean window.

Fields that work in the `sessions` dataset: `sessions`, `sessions_with_cart_additions`,
`sessions_that_reached_checkout`, `sessions_that_completed_checkout`, `conversion_rate`, `bounce_rate`,
`average_session_duration`, `pageviews_per_session`; group by `session_device_type`,
`landing_page_path`, `referrer_source`, `referrer_name`; filter with `WHERE`; `TIMESERIES day|week`. In
`sales`: `orders`, `gross_sales`, `net_sales`, grouped by `sales_channel`. Shopify's sessions data reports
entry (landing) pages, not every page viewed, so drop-off on a later page needs recordings or GA4.

## 1. Validate the data first

Before reading any rate, check the numbers can be trusted. Report the result in the audit.

| Check | How | If it fails |
|---|---|---|
| Orders match | Compare orders (or booking requests) in the store admin with transactions in analytics for the same dates | A gap over a few percent means lost or double tracking: say so, send to `analytics-audit` |
| No duplicate firing | One purchase event per order; one pageview per page | Duplicates inflate conversion; fix first |
| Consent effect | A cookie banner can hide a share of visitors from analytics | Rates are of tracked visitors only: say so |
| Bots and internal traffic | Rows with no device type and near-100% bounce; spikes of zero-engagement sessions; the team's and agency's own visits (often desktop, "direct", higher bounce, especially around a launch) | Leave bot rows out; say internal traffic can't be filtered if it can't |
| Date range | At least two full weeks, ideally four or more, with no big promotion unless it is the subject | Note seasonality and promotions |
| Step changes | Sessions per day: a jump or collapse from one day to the next (a new storefront, theme or tracking change) | Use only the window after the change; earlier data isn't comparable |
| Orders by channel | Orders by sales channel against completed checkouts: subscription renewals (for example Recharge), other storefronts, draft orders and POS aren't website conversions | Count only website checkouts as website conversions; say what the rest are |
| Where the conversion happens | Bookings or leads completed on another system (a booking site, a form tool) never appear in the store's analytics | Say the main conversion is unmeasured here; instrument it before any test |
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
