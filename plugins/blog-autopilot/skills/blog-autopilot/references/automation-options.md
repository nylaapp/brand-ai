# Faster-than-daily events (optional, free)

The default, a **daily polling scan**, needs no setup and catches every store event within about 24 hours. For SEO that's plenty: a post drafted today versus tomorrow makes no ranking difference, and every draft waits for human review anyway. Recommend these upgrades only when the user asks for faster reaction or for events polling can't see.

Ordered from least to most friction. All are free or open source.

## Option 1 — Shopify Flow → product tags (free, built in, no accounts)

Shopify Flow is a free Shopify app. It can tag a product when something happens; the next scan sees the tag.

- Example workflow: **Trigger** "Product added to store" (or "Inventory quantity changed" where the quantity went from 0 to more than 0) → **Action** "Add product tags": `autopilot-event-launch` / `autopilot-event-restock`.
- The scan then also queries `products(query: "tag:autopilot-event-*")`, treats each as a store-event candidate, and removes the tag afterwards (a product update, so only in non-dry runs).
- Many review apps (Judge.me, Yotpo and others) ship their own Flow triggers ("review created"). A condition like "rating ≤ 3" can tag the product `autopilot-event-review-issue`.
- Limits: it only works for product-attached events, and it's still picked up at the next scan. It's more reliable than polling for restocks, since there's no snapshot diff to miss.

## Option 2 — Shopify Flow → Google Sheet event log (free)

Flow's Google Sheets connector ("Add row to spreadsheet") appends one row per event from any trigger, such as orders, customers, reviews or low stock. Columns: `timestamp, event, object_id, detail`.

- The scan reads the sheet through a Google Drive connector if one is connected, or the user exports it to `inputs/events/` as CSV.
- Good for events that aren't attached to a product (a spike in orders from a new region, customer tags).
- Flow can only append rows, so the scan tracks the last row processed in `ledger.snapshots.events_last_row`.

## Option 3 — Instant, self-hosted (open source; only if truly needed)

For true real-time reaction, use **n8n** (self-hosted community edition) or **Activepieces** (open source). Either can receive Shopify webhooks (`products/create`, `inventory_levels/update`) on a server the user runs.

- This is real friction: a server or always-on computer, a public URL for the webhook, and a way to start Claude, which means the paid Claude API (so it isn't free end to end).
- A lighter middle ground: the webhook flow writes events to the Google Sheet from Option 2, and the daily scan stays as is. You get instant logging with the same review cadence.
- Note: Shopify Flow's own "Send HTTP request" action is only on Grow, Advanced and Plus plans, so on Basic plans an external webhook receiver is the only path to instant events.

## What not to do

- Don't use paid middleware (Zapier or Make paid tiers) by default; the user asked for free or open-source tools.
- Don't let any event pipeline publish directly. Every path ends in the same scorer, cap and hidden draft.
