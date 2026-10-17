# Findings catalog

The problems that come up again and again, with how to prove each one and the usual fixes. Reference the catalog code in ANALYTICS.md findings (`F-7 (FC-01)`) so the fix playbook and the cleanup rules can find it. Default severity is a starting point; raise it when a Tier 1 event is affected.

Severity: **S1** Tier 1 event wrong or missing, or a legal exposure · **S2** Tier 2 or attribution wrong · **S3** data quality or hygiene · **S4** cost or cosmetic.

## Duplicates and identity

**FC-01 Same destination installed twice** (S1 if purchases, else S2)
- Symptom: page views or purchases about double; GA4 above the platform; two `page_view` hits per page.
- Detect: the same ID in two install points (`shopify_pixels.py` "Same ID in a pixel and in page code" or "inside GTM", the inventory's `sameIdTwoPaths`, `gtm_export_summary.py` "same Google tag configured twice", `gtm_public_rules.py --ids` compared with the pixel list); two hits with the same event and page in `decode_hits.py`. A second path can be hidden today by another bug (for example the container's page view never fires, FC-30): report it anyway, because fixing the other bug turns the double count on.
- Fix: choose one path per destination (on Shopify, the Google & YouTube app for Google, the Meta app for Meta, unless there is a reason not to); remove or pause the other; re-test.

**FC-02 Purchase without a unique transaction id, or re-fired on reload** (S1)
- Detect: GA4 data check 1 (transaction counted twice); reload the thank-you page in a test and watch for a second `purchase`.
- Fix: pass the order number as `transaction_id`; fire on the platform's purchase event, not on a thank-you URL view.

**FC-03 Browser and server events without a shared event id** (S2)
- Detect: Meta Events Manager deduplication warnings (person's screenshot); in the HAR, Meta `eid` absent or different from what the server sends.
- Fix: one `event_id` per event, generated once and passed to both paths; the order id for purchases.

**FC-04 Event id regenerated on every read** (S2)
- Detect: `gtm_export_summary.py` "unstable value" flag (Custom JS with `Math.random` or time).
- Fix: generate once per event (dataLayer key set at push time, or a template that caches per event).

**FC-32 Event id that repeats across pages or visitors** (S2)
- Symptom: browser and server copies pair up, but the platform merges unrelated events or reports low deduplicated counts.
- Detect: event ids built from a per-page counter, such as `evt_{{gtm.uniqueEventId}}` or a variable that reads `gtm.uniqueEventId` alone (in an export; `gtm_public_rules.py` shows it as `Event ID (per page) (gtm.uniqueEventId)`). The counter restarts on every page, so `evt_12` exists for every visitor; dedup windows then match events that are not the same.
- Fix: an id unique per event (a random id generated once at push time and reused by both paths, or the order or booking id for conversions); keep it stable between the pixel and the server copy.

## Platform and install point

**FC-05 Tag manager in a Shopify custom pixel expected to see the page** (S2)
- Detect: GTM loaded from a custom pixel while the container has click, link-click, form, scroll or visibility triggers.
- Fix: load GTM from the theme for storefront interactions, or publish those interactions from the theme with `Shopify.analytics.publish()`; keep checkout events in pixels. Note Google does not support Google tags in custom pixels.

**FC-06 Checkout or thank-you tracking lost** (S1)
- Detect: tags that lived in `checkout.liquid` or Additional scripts (old exports, old notes); no `purchase` reaching a destination in a test order.
- Fix: move to an app pixel (preferred) or custom pixel subscribed to `checkout_completed`; verify with a test order.

**FC-07 Trigger depends on a site detail that changed** (S1 or S2)
- Detect: dependency register rows with status broken: old booking host in a Click URL filter, CTA text that no longer exists, a page path or hostname rule that no longer matches.
- Fix: update the trigger (analytics owner) or restore the site detail (site owner); add the row to the rules so it does not happen again.

**FC-08 Trigger waits for a dataLayer event nobody pushes** (S2)
- Detect: custom-event triggers whose event never appears in the inventory's dataLayer events on the relevant pages (common after a platform migration).
- Fix: rebuild on events the platform provides (Shopify standard events in a pixel), or agree and add the push; retire the dead trigger.

**FC-30 Base page views tied to a previous platform's dataLayer event** (S1 when conversions or audiences depend on page views, else S2)
- The sharpest FC-08 case: the main page view (GA4 `page_view`, Meta PageView, often helper tags such as campaign-cookie writers) fires on a custom event such as `page_view` that the old site pushed, instead of on the built-in page view. The Google tag usually has `send_page_view` off. On the new platform or theme nothing fires and nothing errors.
- Detect: in the export or `gtm_public_rules.py`, page-view tags whose firing rule is `{{Event}} equals "<custom name>"` rather than `gtm.js`, and a Google tag with `send_page_view=false`; the inventory's dataLayer events on the new site lack that name. Check every host: the old site may still push it while the new theme or preview does not.
- Fix: decide the page-view path first (FC-01: a platform app may already send page views), then either retrigger the tags on the built-in page view or add one agreed push per page; verify one `page_view` per page in a HAR.

**FC-29 Two containers sharing one dataLayer** (S3, S2 if conversions are affected)
- Typical on third-party pages (booking engines, payment or donation pages) where the vendor loads its own container next to the client's. Both read the default `window.dataLayer`, so the vendor's gtag `event` commands and custom events reach the client's Google tags and triggers (unplanned events, possible double conversions), and the client's pushes reach the vendor's container.
- Detect: two `GTM-` keys in the inventory's GTM list or `gtmContainers` on one page; `gtagTargets` addressing IDs the client does not own, or vendor event names (often prefixed) in the client's GA4; `gtm_public_rules.py` on each container shows what each one listens to.
- Fix: find the second container's owner; ask the vendor to use its own dataLayer name, or filter the client's triggers to the events it should act on; record the vendor contract in the dependency register.

**FC-31 Site script intercepts link clicks and navigates in JavaScript** (S2)
- A site-wide script (a redirect helper, a booking-flow router, a page-transition library) cancels the native click and changes `location` itself. Link-click triggers with "Check validation" on skip clicks whose default action was prevented (`preventDefault`), `stopPropagation` hides the click from tag-manager listeners altogether, and a fast JavaScript navigation can leave the page before tags send; out-click and CTA conversions undercount. Rewriting the URL on click (for example an old host to a new one) also changes what Click URL conditions see.
- Detect: in site code, click listeners on `a` elements that call `preventDefault` and then set `location`; in a test, the link-click trigger does not fire in GTM Preview while the page navigates.
- Fix: let the link navigate natively and do the rewrite in the `href` itself, or push an agreed dataLayer event before navigating and trigger on it; add the interception to the dependency register.

**FC-18 Tracking tied to a theme that is about to change** (S2)
- Detect: hardcoded tags in the live theme that the new theme lacks, or the reverse (`drift_snapshot.py` shows the live theme; diff theme code before publishing).
- Fix: decide per tag before the switch; pixels and server paths survive theme changes, theme code does not.

**FC-17 Leftover code from uninstalled apps** (S4, S3 if it sends data)
- Detect: script hosts or snippets for apps no longer installed; app embeds still enabled for removed apps.
- Fix: remove the snippet and its render tag, or disable the embed, in a duplicate theme first.

## Consent and privacy

**FC-09 Third-party banner not synced to Shopify** (S1)
- Detect: after Accept, `Shopify.customerPrivacy.currentVisitorConsent()` still empty or "no"; Pixel Helper says "awaiting consent".
- Fix: the CMP's Shopify integration or a `setTrackingConsent` call on the visitor's choice.

**FC-10 Consent defaults missing or late** (S1 in consent-required regions)
- Detect: Google hits before the default command; `gcs` absent; `G111` on first load from an EEA session.
- Fix: default command (with `region` where needed) before any tag; `wait_for_update` for a slow banner.

**FC-11 Non-Google vendors ignore the choice** (S1)
- Detect: Meta, TikTok, Clarity or others firing in the `reject` state.
- Fix: gate them through the CMP or Shopify pixel permissions; Clarity ConsentV2.

**FC-12 GPC ignored where required** (S1 where applicable)
- Detect: `gpc` state still sends marketing pixels marked as data sale in an opt-out region.
- Fix: honour GPC in the CMP; on Shopify mark sale-of-data pixels correctly.

**FC-21 Personal data sent to analytics** (S1)
- Detect: GA4 data check 9; emails or phone numbers in URLs, event parameters or page titles in the HAR.
- Fix: strip at the source (forms using GET, thank-you URLs with emails); redact in the tag; request data deletion if already collected.

**FC-22 Ad pixels on pages that reveal health conditions** (S1, regulated categories only)
- Only when BRAND.md or the site shows a health, medical or wellness business. Detect: marketing pixels on condition or treatment pages, appointment flows. Fix: client's counsel decides; options include excluding those pages or limiting data. Never give a legal verdict.

## Attribution and configuration

**FC-13 Cross-domain broken** (S2)
- Detect: `_gl` missing on arrival at the booking or checkout domain; different `_ga` client ids; own domain as a referral.
- Fix: linker domains in GTM and GA4 domain settings; keep `_gl` through redirects.

**FC-14 Gateways or booking hosts stealing sessions** (S2)
- Detect: GA4 data check 4. Fix: unwanted referrals list.

**FC-15 GA4 settings left at defaults** (S3)
- Detect: settings checklist. Fix: retention 14 months, internal traffic filter active, key events cleaned, custom definitions registered.

**FC-19 Lead tracking on an unreliable signal** (S2)
- Detect: form-submission triggers filtered on click text, thank-you URL rules where the form shows success in place.
- Fix: fire on a real success signal (success event, redirect to a stable thank-you URL, platform form event).

**FC-20 Page changes not tracked, or tracked twice** (S2)
- Detect: single-page navigation without `page_view`, or enhanced measurement history events plus manual events.
- Fix: one source of page views on route change.

**FC-27 Value means different things per destination** (S2)
- Detect: GA4 reads one field, Ads another (subtotal vs total, with or without tax, shipping, discounts).
- Fix: agree one definition per business and use it everywhere; document it in section 1.

**FC-28 Currency missing or wrong** (S2)
- Detect: purchases without `currency`, or a fixed default that is wrong for some markets. Fix: pass the order currency.

## Hygiene and cost

**FC-16 Orphan, paused or dead container items** (S4)
- Detect: `gtm_export_summary.py` health flags: paused tags, triggers without tags, unused variables, Universal Analytics leftovers.
- Fix: confirm intent with the owner, then delete in a new container version with a clear description.

**FC-23 Tags nobody owns** (S3)
- Detect: no one can say what question the tag answers or who reads its data. Fix: owner or removal (cleanup).

**FC-24 Heavy tags on every page** (S4, S3 if it hurts Core Web Vitals)
- Detect: `tag_cost.py` and Lighthouse third-party table. Fix: load policy (defer, template conditions, on interaction).

**FC-25 A/B testing tool loaded with no running test** (S4)
- Detect: VWO, Optimizely or similar present; the person confirms no active experiment. Fix: remove until the next test.

**FC-26 More than one heatmap or replay tool** (S4, S3 for privacy)
- Detect: two or more of Clarity, Hotjar, Lucky Orange, Crazy Egg. Fix: one at a time, only during a study.
