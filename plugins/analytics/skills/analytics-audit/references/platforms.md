# Where tags live, by platform

The same destination can be wired from several places at once, and each place sees different things. An audit inventories every install point separately; a fix chooses one path per destination.

## Shopify (Online Store 2.0, checkout extensibility)

Facts checked 2026-10-15 against Shopify and Google documentation unless marked observed.

### Install points

| Install point | Where to look | Sees | Cannot see | Scope |
|---|---|---|---|---|
| Theme code | `layout/theme.liquid` (head and before `</body>`), `snippets/`, `sections/`, `assets/*.js` | Storefront DOM: clicks, link text, forms, scroll | Checkout, thank-you, order status | Per theme: lost when another theme is published |
| App embeds | Theme editor > App embeds; `config/settings_data.json` > `current.blocks` (type `shopify://apps/...`, `disabled` flag) | Storefront DOM | Checkout | Per theme |
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
- **Theme switches change tracking.** Theme code and app embeds go with the theme; pixels stay. Before publishing a new theme, diff the old theme's tracking code against the new one.
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
7. Theme-level `dataLayer` events from a previous platform (Magento, a custom site) that GTM still waits for.

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

## Other platforms

Squarespace (Settings > Advanced > Code injection; built-in GA field), Wix (Marketing integrations; custom code in Settings), BigCommerce (Script Manager, Data Solutions), Webflow (Project settings > Custom code). Same method: list every install point, find each ID once, check checkout separately.

## Third-party domains in the journey

Booking engines, payment pages, donation forms, scheduling tools and separate checkout domains break sessions and are where conversions often happen.

- Confirm who loads tags there (the vendor's setting, a container, nothing) and which events they push (`purchase`, custom names).
- Cross-domain: the linker domain list (GTM conversion linker and the GA4 data stream's "Configure your domains") must include every hop; `_gl` must survive redirects.
- Unwanted referrals: payment gateways and booking hosts listed so they do not steal the session source.
- The dataLayer contract with that vendor (event name, keys, value fields) belongs in the dependency register like any theme dependency.
