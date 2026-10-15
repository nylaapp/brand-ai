# Tracking plan: deciding what to measure

The tracking plan is section 1 of ANALYTICS.md. It answers: what does this business count as success, which events prove it, which destination needs each one, and where each one comes from. Everything else (tests, guardrails, the load policy) hangs off it, so agree it with the client before fixing anything.

## 1. Start from the business model

| Model | Tier 1 | Tier 2 | Tier 3 |
|---|---|---|---|
| Online store | `purchase` | `begin_checkout`, `add_payment_info`, subscribe | `view_item`, `add_to_cart`, `view_cart`, `search`, `view_item_list` |
| Appointments or bookings | booking completed (often on a third-party booking domain) | click-out to booking, `begin_checkout` in the booking flow, phone call click, contact form | service page view, location page view |
| Lead generation | qualified lead (form success, booked call) | form start, phone or email click, chat started | key content views, pricing page view |
| Subscription or membership | `purchase` of the first period, `sign_up` | trial start | plan page views |
| Content or media | subscription or registration | newsletter sign-up | engaged reading, video progress |

Mixed businesses (a clinic with a shop) have more than one Tier 1 row. Tier 4 is always base measurement: page views, sessions, click-id capture.

## 2. Name events per destination

Use each platform's standard names so built-in reports and bidding work:

| Business event | GA4 | Google Ads (conversion action) | Meta | TikTok |
|---|---|---|---|---|
| Purchase | `purchase` | Purchase (primary) | `Purchase` | `CompletePayment` or `Purchase`* |
| Begin checkout | `begin_checkout` | Begin checkout (secondary) | `InitiateCheckout` | `InitiateCheckout` |
| Add to cart | `add_to_cart` | (usually not a conversion) | `AddToCart` | `AddToCart` |
| View item | `view_item` | | `ViewContent` | `ViewContent` |
| Lead | `generate_lead` | Submit lead form | `Lead` | `SubmitForm` |
| Booking | `purchase` (with value) or a custom event | Book appointment | `Schedule` | `SubmitForm` or a custom event* |
| Phone click | `click` with link domain or a custom `phone_click` | Phone call lead | `Contact` | `Contact` |
| Sign up | `sign_up` | Sign-up | `CompleteRegistration` | `CompleteRegistration` |

\* TikTok's standard event list changes; check it in Events Manager before choosing. The same goes for any less common name on any platform. Custom GA4 names are lowercase snake_case, at most 40 characters, never containing personal data.

## 3. Parameters that make events useful

- **Purchases:** `transaction_id` (the order number, unique), `value`, `currency`, `items` (id, name, price, quantity). One agreed value definition across destinations (with or without tax, shipping, discounts); write it in section 1.
- **Browser plus server copies:** one `event_id` per event, shared by both paths, for Meta and TikTok deduplication.
- **Leads and bookings:** a stable id if the system provides one, the location or service when relevant, and nothing personal in analytics parameters. Enhanced conversions or advanced matching (hashed email or phone) only through the platform's supported feature and only with consent.

## 4. Where each event comes from

For every event, write its origin, because that decides who can break it:

- the platform (Shopify standard events through a pixel, WooCommerce hooks),
- the site's markup (a link click, text, URL: these go into the dependency register),
- a dataLayer push in site code (needs an agreed name and schema),
- a third-party domain (booking engine, payment page: the vendor's push is a contract),
- a server (webhook, CAPI, server-side container).

## 5. Choose the destinations deliberately

Only send an event where someone uses it: a GA4 report someone reads, an Ads conversion used for bidding or reporting, a Meta optimisation event. Every extra destination is cost (page weight, consent scope, maintenance). The load policy (cleanup skill) starts from this table.

## 6. Review with the client

Show the table in plain words ("When someone books, we tell GA4, Google Ads and Meta, with the booking value"). Ask them to confirm the Tier 1 rows and the value definition. Mark the plan `confirmed YYYY-MM-DD by <name>` in section 1; until then it is a draft and tests are provisional.
