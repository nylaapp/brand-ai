# Detecting triggers

Contents: 0. Lookback window · 1. Store events · 2. Search Console · 3. Voice of customer · 4. Competitors · 5. Market trends · 6. Occasions · 7. AI citation spot-check · 8. Periodic · 9. Sources-checked log

Every family is optional. Run a family only if the profile enables it and the data exists. Record each one's status (ok, no data, not configured or error) for the run report. A missing source is never a reason to guess.

---

## 0. Lookback window

`since` = the date of the last *successful* run in `ledger.runs`, or 7 days ago if the ledger is empty. Every "new since" check uses `since`, not "yesterday", so a missed scheduled run is caught up automatically.

## 1. Store events (Shopify connector)

Follow the connector's GraphQL workflow (check `graphql_schema`, then `validate_graphql_codeblocks`, then run). The queries below are starting points; the schema is the source of truth. All of these are **read-only** and safe in any mode.

**Existing articles, including hidden drafts.** Fetch these first; they're the dedupe baseline and the `--existing` file for the scorer.
```graphql
query { articles(first: 250, sortKey: UPDATED_AT, reverse: true) {
  nodes { id title handle tags createdAt publishedAt isPublished blog { handle } } } }
```
Save them as `runs/<date>-existing-articles.json` in the form `[{title, handle, tags, created_at, published}]`, where `published = isPublished`. Paginate if there are 250 or more.

**New products and collections since `since`.**
```graphql
query { products(first: 50, query: "created_at:>=<since> status:active") {
  nodes { id title handle productType tags createdAt totalInventory onlineStoreUrl } } }
query { collections(first: 50, query: "updated_at:>=<since>") { nodes { id title handle updatedAt } } }
```
- Each new active product → `store_new_product`. A launch-adjacent or deep-dive post only makes sense for hero products. Business value is 5 for a new product in a core category and 2–3 for a minor variant or accessory. Group several products launched together into one candidate ("Meet the fall collection").
- A new collection → `store_new_collection`, often a buying guide for the collection's theme.

**Restocks.** Compare against `ledger.snapshots.out_of_stock` (product IDs with `totalInventory <= 0` last run). A product in the old snapshot that now has stock → `store_restock`. Refresh the snapshot every run. On the first run, just create the snapshot and emit nothing.

**Rising products and conversion gaps** (analytics; skip if the tool errors). Use `run-analytics-query` with ShopifyQL, for example net sales by product for the last 30 days against the previous 30:
```
FROM sales SHOW net_sales BY product_title SINCE -30d UNTIL today COMPARE TO previous_period ORDER BY net_sales DESC LIMIT 20
```
A product up at least 50% with meaningful volume → `store_rising_product` (buying guide, usage or styling post). If sessions-by-product data is available, high views with a low conversion rate → `store_conversion_gap` (a comparison or FAQ post that answers objections). ShopifyQL syntax varies by API version; if a query fails, note it in the log and move on.

**Dry runs with a snapshot.** If `store-snapshot.json` is provided, read `shop`, `products`, `collections`, `articles` and `analytics` from it instead of querying. It may also carry `competitor_feeds` (per domain, a list of `{title, url, published}`) in place of fetching feeds. Use whatever keys are present.

## 2. Search Console (`inputs/gsc/`)

The user exports **Search results → Export (CSV)** from Search Console, ideally in **Compare** mode (last 28 days vs. previous 28 days), and unzips it into `inputs/gsc/`. Keep the export's folder name: it ends in the export date (`…-Performance-on-Search-2026-09-28/`), which the script uses to judge freshness. Without a date in the name, it falls back to the file's modified time. Then run:

```bash
python scripts/gsc_signals.py --dir inputs/gsc --existing runs/<date>-existing-articles.json \
  --min-impressions <thresholds.gsc_striking_min_impressions> --decay-pct <thresholds.gsc_decay_drop_pct> \
  --max-age-days <sources.search_console.max_age_days> --today <date>
```

- `striking_distance` with `suggested_action: new` → a `gsc_striking` candidate. With a matching article, it becomes a refresh/optimize candidate for that article.
- `ctr_gap` → a small refresh (title and meta only). Mention these in the report, but give them urgency 2 unless impressions are large.
- `decay` → a `gsc_decay` refresh candidate with the page's handle as `refresh_target`.
- `stale_files` → don't use them. Add "export fresh Search Console data" to *Needs your attention*.

Group near-duplicate queries ("<keyword>", "best <keyword> for <use>") into one candidate and sum their impressions.

If the user keeps a Google Sheet instead of CSVs and a Google Drive connector is available, read the sheet and save it as CSV into `inputs/gsc/` first.

## 3. Voice of customer (`inputs/reviews/`, `inputs/helpdesk/`)

Review apps (Judge.me, Yotpo, Okendo, Loox) and helpdesks (Gorgias, Zendesk, Shopify Inbox) all export CSV. Column names vary, so find the free-text column (body, content, message, review), the date column and the product column.

1. Keep rows within `since − 30 days` so there's enough volume to see patterns.
2. Cluster the text into themes: questions ("does it run small?"), confusion ("how do I wash…"), objections ("too expensive vs…") and praise that reveals a use case.
3. A theme with at least `thresholds.voc_min_mentions` → a `voc` candidate. Put the mention count and two or three short paraphrased examples in the evidence. Don't copy customer names; quotes need permission before they appear in a post.
4. Typical outputs: fit or size guide, care guide, troubleshooting post, or a "who it's for" comparison.

Uniqueness is usually 4–5 for these, because the brand's own customer questions are first-party insight.

## 4. Competitors (profile `sources.competitors.list`)

For each competitor, fetch the `feed`. Shopify blogs expose `/blogs/<handle>.atom`; otherwise use `/sitemap.xml` → `sitemap_blogs_*.xml`, or an RSS feed. Find posts published since `since`.

- Keep only posts in the brand's `categories`. Anything else is noise.
- Check whether the brand already covers the topic (existing articles). If it does and the competitor post is clearly better or newer, consider a refresh.
- An uncovered topic → a `competitor` candidate, with urgency 3. Don't copy their angle; the brief should say how to do better (the gap).
- Ranking changes can't be tracked without a paid rank tracker. If the profile lists `tracked_questions`, a monthly web-search spot-check is the free approximation (section 7).

If a feed can't be fetched, log it and continue. Don't try to work around the site's restrictions.

## 5. Market trends (web search)

For each category and seed term, search for recent news, launches and "trend" coverage, and check forums (Reddit, niche communities) for rising questions. A trend counts only with at least `thresholds.trend_min_evidence` independent sources from the last 30 days. One viral post isn't a trend.

- Emit a `trend` candidate with the sources in the evidence. Demand is rarely above 3 without GSC or volume data. Urgency is 4–5 if the topic is time-sensitive.
- Don't invent volumes. "Rising" should be backed by dated sources.

## 6. Occasions

```bash
python scripts/occasions.py --profile brand-profile.yaml --today <date> --json
```

For each occasion with status `open` (or `late`, for transactional or gift posts):

1. Decide whether it fits the brand. An occasion only matters if the catalog has a real angle; a hiking-sock brand has one for holiday gifting, but not for Singles' Day unless it sells in those markets.
2. Check for last year's post on the same occasion (existing articles). If one exists, make it a **refresh** at the same URL rather than a new post, so it keeps its accumulated authority.
3. Emit an `occasion` candidate with `deadline = publish_by` and `urgency = suggested_urgency`.

See `occasions.md` for how the calendar and lead times work.

## 7. AI citation spot-check (optional, monthly)

If the profile lists `tracked_questions` and the last check was 28 or more days ago (`ledger.snapshots.ai_check_date`), web-search each question and note whether the brand's domain appears, which sites are cited, and whether there's an AI Overview. A question where competitors appear and the brand doesn't, and the brand has a credible angle → an `ai_citation_gap` candidate with an answer-first, FAQ-heavy brief. Report this honestly as an approximation: web search results aren't the same as what ChatGPT or Perplexity answer.

## 8. Periodic

No detection needed. The scorer's periodic rule handles it using the ledger. You just make sure the backlog carries forward.

## 9. Sources-checked log

End Step 2 with a line per family for the run report, for example:
```
store: ok (2 new products, 0 restocks, analytics unavailable)
search_console: stale (Queries.csv 41 days old) → skipped
reviews: ok (212 rows, 2 themes ≥ 3 mentions)
helpdesk: not configured
competitors: ok (3 feeds, 1 relevant new post); 1 feed error (competitor.example 403)
trends: ok (no qualifying trend)
occasions: ok (holiday_gifting open, bfcm open)
```
