# Where tags live, by platform

The same destination can be wired from several places at once, and each place sees different things. An audit inventories every install point separately; a fix chooses one path per destination.

## Shopify (Online Store 2.0, checkout extensibility)

Facts checked 2026-10-15 against Shopify and Google documentation unless marked observed.

### Install points

| Install point | Where to look | Sees | Cannot see | Scope |
|---|---|---|---|---|
| Theme code | `layout/theme.liquid` (head and before `</body>`), `snippets/`, `sections/`, `assets/*.js` | Storefront DOM: clicks, link text, forms, scroll | Checkout, thank-you, order status | Per theme: lost when another theme is published |
| App embeds and app blocks | Rendered page source: `<!-- BEGIN app block: shopify://apps/<app>/blocks/<block>/... -->` comments (embeds and blocks placed in sections). Theme editor > App embeds. `config/settings_data.json` > `current.blocks` only to confirm: repo copies are often stale or ignored by git | Storefront DOM | Checkout | Per theme |
| ScriptTags | Rendered page source: the `asyncLoad` function's `urls` list (legacy ScriptTag API, added by apps) | Storefront DOM | Checkout | Store-wide: every theme, survive theme changes and app embed toggles |
| App pixels | Settings > Customer events > App pixels | Shopify standard events, including checkout and purchase; consent-gated by Shopify | DOM (strict sandbox, web worker) | Store-wide, every theme including previews |
| Custom pixels | Settings > Customer events > Custom pixels | Standard events plus custom events the theme publishes with `Shopify.analytics.publish()` | DOM (lax sandbox, iframe); its cookies do not reach the main page | Store-wide |
| Tag manager | A container loaded from theme code (sees the DOM) or from a custom pixel (sandboxed) | Depends on where it is loaded | From a custom pixel: no click, scroll, visibility or form triggers, no Preview mode | As its loader |
| Server-side | Order webhooks, a server-side GTM container, or an app (Elevar, Littledata, Stape, Analyzify) | Orders even when the browser is blocked | Browser context unless passed | Store-wide |
| Legacy (gone) | `checkout.liquid`, Settings > Checkout > Additional scripts, Online Store preferences GA field | Nothing now | | Deadlines passed: Plus 2025-08-28, non-Plus 2026-08-26; preferences GA converted to a custom pixel 2025-02-02 |

### Facts that drive decisions

- **Google does not support Google tags inside a custom pixel** and recommends the Google & YouTube app for sitewide Google measurement. GTM cannot be configured through that app. (support.google.com/tagmanager/answer/16031492 and /15642481)
- **A container in theme code never sees checkout.** Checkout and purchase events come from pixels or a server-side path.
- **Pixels are consent-gated by Shopify:** new pixels require Analytics and Marketing permission and count as data sale by default; GPC is honoured automatically in opt-out regions. A third-party banner must write choices through the Customer Privacy API (`setTrackingConsent`) or pixels never fire.
- **The page source lists every pixel** (observed on live stores, undocumented): `webPixelsConfigList` gives type, sandbox (`STRICT`, `LAX`, `OPEN`), app id, consent purposes and configuration with destination IDs. `scripts/shopify_pixels.py` parses it. Custom pixel code itself is not in the page source; read it in the admin.
- **Observed sandbox `OPEN`** for the Google & YouTube app and the Meta app on every store checked, with the Google app declaring no consent purposes (it relies on Google consent mode instead of Shopify's gate).
- **Theme switches change tracking.** Theme code and app embeds go with the theme; pixels and ScriptTags stay. Before publishing a new theme, diff the old theme's tracking code against the new one.
- **Previews and browser state (observed).** A `?preview_theme_id=` URL fetched without a browser session (a script, a crawler) returns the published theme; the preview id can even be dropped by the redirect to the primary domain. In a browser, opening a preview sets a cookie that keeps serving the unpublished theme on the live domain until it expires or is cleared, so a used browser profile can audit the wrong theme without noticing. `window.Shopify.theme.role` is `main` for the published theme and `unpublished` for a preview: check it on every page.
- **Purchase value change around 2025-04-22:** Shopify fixed `subtotalPrice` on the new Thank you page to subtract order-level discounts, so reported values dropped for stores with order discounts. Expected, not a bug.
- **Customer account pages** load pixels only with a connected custom subdomain, and only send `page_viewed`.
- **Shopify's own analytics** (monorail, trekkie) always runs and is not a third-party tag.
- **Testing a custom pixel:** Settings > Customer events > the pixel > Test opens the store with the Pixel Helper (one custom pixel at a time; "awaiting consent" means the visitor has not consented).

### Shopify pitfalls to check every time

1. Same GA4 or Ads ID in the Google & YouTube app and in GTM or theme code (double page views, double purchases).
2. Meta pixel in the Facebook & Instagram app and in GTM or theme code without shared `event_id`.
3. GTM in a custom pixel expected to fire click or form triggers.
4. Old theme snippets from uninstalled apps still loading scripts.
5. A third-party consent banner that never calls `setTrackingConsent` (pixels silent after "Accept").
6. Thank-you page tracking that lived in Additional scripts and silently stopped.
7. Theme-level `dataLayer` events from a previous platform (Magento, a custom site) that GTM still waits for, including the base page view itself (FC-30).
8. The same GA4 or Meta ID in an app pixel and inside the GTM container the theme loads: `shopify_pixels.py` and the inventory's `sameIdTwoPaths` read the container's public `gtm.js` to catch it.
9. ScriptTags from apps nobody remembers installing: they load on every theme and survive a theme switch.
10. The Google & YouTube app and a theme GTM container sharing `window.dataLayer`: the app's `gtag('event', 'page_view')` and ecommerce events trigger the container's tags too, so destinations get two hits and the container depends on the app (FC-33).
11. A full GTM container inside a custom pixel: its Google tag and base tags send from the sandbox iframe, with the sandbox URL as the page address, on every page and on checkout (FC-34).

**Telling the paths apart in a capture.** App pixels send from workers owned by the page, so their hits show the top page as frame; custom pixels send from an iframe on the store's own host at `/web-pixels@.../custom/...`. The Google & YouTube app's GA4 hits go to Google's endpoint without a GTM marker; the Meta app's event ids start with `sh-`; the TikTok app posts to `/api/v2/shopify_pixel`. `decode_hits.py --by-source` applies these rules.

## WordPress and WooCommerce

| Install point | Where to look |
|---|---|
| Theme files | `header.php`, `footer.php`, `functions.php` (`wp_head` / `wp_footer` hooks) |
| Plugins | Site Kit by Google, GTM4WP, WooCommerce Google Analytics, PixelYourSite, Meta for WooCommerce, CMP plugins (Complianz, CookieYes, Cookiebot) |
| Snippet plugins | WPCode / Insert Headers and Footers, Code Snippets |
| Tag manager | GTM via plugin or snippet; check for two (plugin plus hardcoded) |
| Server-side | WooCommerce order hooks, CAPI plugins |

Checkout is on the same domain and in the DOM, so a theme-level container sees it. Double installs from a plugin plus a snippet are the most common duplicate.

## Custom sites and headless storefronts

- Look in the base layout or document template, the framework's script component (Next.js `next/script`, Nuxt head config), and any analytics wrapper module.
- Single-page apps need `page_view` on route change (history change trigger or manual events); check it is not sent twice (automatic plus manual).
- Headless Shopify (Hydrogen or custom): use Hydrogen's analytics and consent handling, or the Customer Privacy API with the headless parameters; checkout must share the root domain for consent cookies to carry.
- **Hybrid stores** run a headless or custom front end on the main domain and the Shopify theme on another host (the platform domain, a checkout subdomain, or a theme being rebuilt to replace the front end). Each host has its own install points: the front end's loader and tag manager, and on the Shopify host the theme, embeds, ScriptTags and pixels. Inventory the page list on every host, and say which host each finding applies to. A front end that injects every tag at runtime shows no tags in its static source: use the browser inventory there.
- **Script loaders** (a site's own loader or a tag service) often delay tools until the first interaction or a timer. Interact before the inventory, and list what the loader adds as its own install point.

## Other platforms

Squarespace (Settings > Advanced > Code injection; built-in GA field), Wix (Marketing integrations; custom code in Settings), BigCommerce (Script Manager, Data Solutions), Webflow (Project settings > Custom code). Same method: list every install point, find each ID once, check checkout separately.

## Third-party domains in the journey

Booking engines, payment pages, donation forms, scheduling tools and separate checkout domains break sessions and are where conversions often happen.

- Confirm who loads tags there (the vendor's setting, a container, nothing) and which events they push (`purchase`, custom names).
- A vendor page can run its own container next to the client's. Two containers on one page share the default `dataLayer`, so the vendor's gtag `event` commands can reach the client's Google tags and the client's pushes reach the vendor's (FC-29). Run `gtm_public_rules.py` on each container to see what it does.
- Generic entry URLs (a booking engine's or checkout's start page with nothing selected) can fire "started" tags and then redirect the visitor away (FC-35). Visit each URL that calls to action point to with its own journey step.
- Cross-domain: the linker domain list (GTM conversion linker and the GA4 data stream's "Configure your domains") must include every hop; `_gl` must survive redirects.
- Unwanted referrals: payment gateways and booking hosts listed so they do not steal the session source.
- The dataLayer contract with that vendor (event name, keys, value fields) belongs in the dependency register like any theme dependency.
