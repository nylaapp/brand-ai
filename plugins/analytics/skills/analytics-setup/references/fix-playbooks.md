# Fix playbooks

How to make the common fixes safely. Each playbook: when to use it, steps, how to verify, how to undo. Platform facts behind them are in the audit skill's `references/platforms.md`. Every fix ends with the verification it names and an ANALYTICS.md changelog line.

## P1. One path per destination

Use when a destination is installed in two places (FC-01), or before adding anything new.

On Shopify, the default choice is:

| Destination | Default path | Use another path when |
|---|---|---|
| GA4, Google Ads, Merchant Center | Google & YouTube app (covers storefront and checkout; the path Google supports) | The business needs storefront interactions the app does not send (link clicks, CTA clicks, scroll): add those from GTM in the theme, sending to the same measurement ID **without a second page_view** (a Google tag with `send_page_view` false, or event tags only), and prove one `page_view` per page in a HAR |
| Meta | Facebook & Instagram app (pixel plus CAPI with deduplication) | Custom events the app cannot send: add them through the same pixel ID with a shared `event_id` |
| TikTok, Pinterest, Snap, Reddit | The vendor's Shopify app pixel | No app exists: custom pixel |
| Heatmaps, chat, reviews, popups | Their app embed (per theme, can be switched off per theme) | |
| Tag manager | In theme code, only for storefront DOM interactions | Never as the only path for checkout events |

Elsewhere: one tag manager container, loaded once, with each Google tag configured once.

Steps: list each destination's current paths (audit inventory) · pick the keeper with the person · disable the others (P2) · verify. Verify: accept state, each page sends one `page_view` per destination; a test purchase sends one `purchase` per destination. Undo: re-enable what was disabled.

## P2. Remove a duplicate or dead install point

1. Back up: duplicate the theme (Shopify: Online Store > Themes > Duplicate) or commit the code; note the GTM version currently live; screenshot the pixel's settings.
2. Disable before deleting: disconnect a pixel, disable an app embed, pause a GTM tag, comment out or remove a theme snippet in the duplicate theme first.
3. Verify on a preview where possible; pixels and GTM have no preview on Shopify, so verify immediately after the live change.
4. After a quiet period (a week of normal data) delete for good, with the owner's OK.
Undo: reconnect, re-enable, republish the previous GTM version, restore the theme file.

## P3. Purchase tracking on Shopify

Use when purchases are missing or doubled (FC-02, FC-06).
- Prefer the destination's app pixel. For a custom pixel: subscribe to `checkout_completed`, send `transaction_id` = the order id (or name), `value` and `currency` from the event's checkout totals, items from line items, and an `event_id` derived from the order id so browser and server copies match.
- Never fire purchases from a thank-you URL rule or the order status page view: reloads repeat them.
Verify: test order with the owner's approved method; one purchase per destination, correct id and value; reload the thank-you page and confirm no second purchase. Undo: disconnect the pixel.

## P4. Storefront interactions that a pixel must see

Use when a sandboxed pixel or a GTM container in a custom pixel needs clicks or form success (FC-05).
- Publish from theme code: `Shopify.analytics.publish('<prefix>_cta_click', { label, href, location })` on the real interaction (listen for the native event; never `preventDefault` a link to do it).
- Subscribe in the custom pixel: `analytics.subscribe('<prefix>_cta_click', event => { ... })`.
- Use a client prefix for custom event names, document the name and fields in the dependency register, and keep personal data out.
Verify: the custom pixel's Test mode (Pixel Helper) shows the event; the destination receives it once. Undo: remove the publish call and the subscription.

## P5. Consent

Use for FC-09 to FC-12.
- **Shopify banner only** (no third-party tools outside Shopify's gate): set regions in Settings > Customer privacy; check each pixel's permission and data-sale settings.
- **Third-party CMP:** use its Shopify integration, or call `Shopify.customerPrivacy.setTrackingConsent({analytics, marketing, preferences, sale_of_data?}, callback)` on the visitor's choice. Never write Shopify's cookies directly.
- **Google consent mode in theme or GTM:** `gtag('consent', 'default', {...denied..., region: [...]})` before any tag (GTM: a Consent Initialization trigger), then `update` from the CMP. Map Shopify `analytics` to `analytics_storage`; `marketing` to `ad_storage`, `ad_user_data`, `ad_personalization`. Consider `url_passthrough` and `ads_data_redaction` where ads storage is denied.
- **Other vendors:** gate in the CMP or via Shopify pixel permissions; Clarity needs ConsentV2 for EEA, UK and CH.
- Banner text, regions and category choices are the client's legal decision: propose, never decide.
Verify: full privacy matrix for every core event. Undo: previous banner settings (screenshot them first) and previous container version.

## P6. Changing a GTM container

1. Work in a new workspace named for the change. Never edit the default workspace someone else is using.
2. Make the change; name things clearly; add a note in the tag or trigger with the finding ID.
3. Preview with Tag Assistant on the affected pages and states; save the HAR.
4. The container owner publishes with a version name and description that cite the finding IDs. We publish only if the owner explicitly asks us to, for that version.
5. Export the published version, run `../analytics-audit/scripts/gtm_export_summary.py --diff old.json new.json` (path from this skill's folder), and update the dependency register.
Undo: publish the previous version (GTM Versions > the previous one > Publish).

## P7. Cross-domain and referrals

Linker domains in GTM's conversion linker and in GA4 (data stream > Configure tag settings > Configure your domains) list every hop; payment and booking hosts go in unwanted referrals. Verify: follow a link to the other domain and confirm `_gl` arrives and the `_ga` client id matches on both sides. Undo: restore the previous lists (copy them first).

## P8. Lead and booking signals

Fire on success, not on submit or click text: a success event from the form or booking tool, a redirect to a stable thank-you URL, or the platform's form event. If the success signal lives on a third-party domain, agree the event name and fields with that vendor and record them as a dependency. Verify: one successful test submission with test data, one event per destination. Undo: re-enable the old trigger.

## P9. Adding a dataLayer push to site code

Only when a needed signal cannot come from the platform. Agree the event name (client prefix), the fields and their types with the analytics owner first; add the row to the dependency register and a rule that protects it; push on the real interaction; keep personal data out. Verify in the inventory's dataLayer events and in Preview. Undo: remove the push.

## P10. A trigger that waits for a stale site detail

Decide which side changes: update the trigger (host, text, path) or restore the site detail. Prefer conditions that survive copy edits (link host and path over link text; a data attribute the site keeps stable over CSS classes). Record the new dependency. Verify in Preview or a HAR. Undo: previous version.

## P11. Browser and server deduplication

One `event_id` generated once per event (order id for purchases), passed to the browser pixel and the server event; same event name on both sides. Verify in Meta Events Manager (deduplication and event match quality; person's screenshot) and in the HAR (`eid`). Undo: previous version.

## P12. Rollback kit, prepared before every change

| Changed | Prepare before | Undo |
|---|---|---|
| Theme code | Duplicate theme or commit | Republish the previous theme or revert the file |
| App embed | Note its on/off state per theme | Toggle back |
| Shopify pixel | Screenshot settings and permissions | Reconnect or restore settings |
| Customer privacy settings | Screenshot every panel | Restore by hand |
| GTM | Note the live version number; export it | Publish the previous version |
| GA4 admin | Screenshot the setting | Restore by hand |
| Ad platform | Screenshot conversion settings | Restore by hand (the owner) |

Annotate the date of every change that affects numbers (GA4 annotations if available, otherwise ANALYTICS.md changelog) so later readers do not mistake a fix for a trend.
