# Action plan: prioritise, then get approval

The audit says what is wrong. The action plan says what we will change, in what order, who does it, how we will know it worked and how we undo it. Nothing is changed until the plan, or the batch being worked on, is approved.

## 1. Order

Work in this order, because later steps depend on earlier ones:

1. **Decisions that block everything:** one path per destination, the confirmed tracking plan, who owns the tag manager. A fix made before these are settled often gets undone.
2. **Consent foundations:** defaults before any tag, the banner talking to the platform (Shopify Customer Privacy API), vendor gating. Fixing events first and consent later means testing everything twice.
3. **S1 findings** (Tier 1 events wrong or missing, legal exposure).
4. **S2 findings** (Tier 2, attribution, deduplication).
5. **Quick hygiene** that reduces risk (dead tags that could fire, leftovers that send data).
6. **S3 and S4** (settings, hygiene, cost). Cost work goes to `analytics-cleanup`.

Within a level, prefer the change with the least risk and the quickest test. Group changes that are tested together, but never group changes owned by different people into one approval.

## 2. Plan table

| # | Findings | Change (exact) | System | Who | Effort | Risk | Test | Rollback | Approval |
|---|---|---|---|---|---|---|---|---|---|
| 1 | F-3 (FC-01) | Disconnect custom pixel "GA4 old" that duplicates the Google & YouTube app | Shopify Customer events | store owner (or us with OK) | 10 min | Low: app covers the same events | privacy matrix accept state, `page_view` once and `purchase` once | Reconnect the pixel | store owner |

Columns:
- **Change (exact):** the object and the edit, specific enough that someone else could do it ("GTM trigger 54: Click URL contains `booking.example.com` instead of `booking.old-example.com`").
- **System:** theme or site code, app embed, Shopify Customer events, Shopify Customer privacy, GTM web container, server container, GA4 admin, Ads, Meta, third-party vendor.
- **Who:** the person who makes the change. We make site-code changes; tag manager and account changes are made by their owner unless they explicitly hand it to us.
- **Risk:** what could break and how many core events it touches. Store-wide changes with no staging (Shopify pixels and privacy settings, GTM publish) are at least medium.
- **Test:** the states and events from the privacy matrix that prove it, plus any receiving-side check.
- **Rollback:** the concrete undo, prepared before the change (see fix playbook P12).

## 3. Asking for approval

Show the plan in plain words first ("1. Remove the second copy of Google Analytics so page views stop counting twice"), then the table. Ask for approval per item or per batch, and record who approved what and when in ANALYTICS.md section 10.

Changes that always need a named approver, never a general "go ahead":
- anything that publishes (a GTM version, a live theme, a pixel connect or disconnect on a live store),
- consent banner settings, regions or category mappings (client and, if they have one, their counsel),
- deleting anything (prefer pause or disconnect first, delete after a quiet period),
- test purchases, bookings or form submissions on the live site,
- anything in an ad account (conversion actions, primary vs secondary, attribution settings).

## 4. Questions that block items

If an item depends on an answer (which booking host is current, which value definition), it waits. Put the question in ANALYTICS.md section 9 with the item number it blocks, and move on to items that are not blocked. A good question names the exact object, what breaks if the answer is wrong, and who should answer.
