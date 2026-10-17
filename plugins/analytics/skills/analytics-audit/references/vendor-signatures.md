# Vendor signatures

How to recognise each common tool in a page, what it is for, how it gets consent, and how early it really needs to load. Use it to label inventory rows and to fill the load policy. Hosts change; when a request does not match, label it by its host and look it up.

Load timing key: **early** = in the head, before or at first paint (still async) · **load** = async at page load, after consent · **defer** = after load, on idle, or on first interaction · **event** = only on the page or action it measures · **study** = only while an active study needs it.

| Tool | Category | Script hosts | Collect endpoints | Globals | Cookies | Consent mechanism | Load timing |
|---|---|---|---|---|---|---|---|
| Google Tag Manager | Tag manager | `www.googletagmanager.com/gtm.js` | (none itself) | `google_tag_manager`, `dataLayer` | | Consent mode inside tags | early |
| Google tag / GA4 | Analytics | `www.googletagmanager.com/gtag/js?id=G-` | `*/g/collect`, `analytics.google.com`, first-party server endpoints (`/g/collect` on the client's domain) | `gtag`, `dataLayer` | `_ga`, `_ga_<stream>` | Consent mode v2 | early (captures landing page and campaign) |
| GA4 signals | Analytics (demographics) | | `stats.g.doubleclick.net/g/collect` | | | Consent mode | with GA4; not an event |
| Google Ads | Advertising | `gtag/js?id=AW-` | `googleadservices.com/pagead/conversion`, `google.com/ccm/collect`, `googleads.g.doubleclick.net/pagead/viewthroughconversion` | `gtag` | `_gcl_au`, `_gcl_aw` | Consent mode v2 (`ad_storage`, `ad_user_data`, `ad_personalization`) | conversion linker early; conversions on event |
| Merchant Center | Advertising | via Google & YouTube app | `merchant-center-analytics.goog` | | | Consent mode | with Google tag |
| Meta pixel | Advertising | `connect.facebook.net/*/fbevents.js` | `www.facebook.com/tr` | `fbq` (`fbq.getState().pixels`) | `_fbp`, `_fbc` | `fbq('consent', 'revoke'/'grant')`, Shopify gate | load (captures `fbclid`) |
| Meta CAPI | Advertising, server | | server to `graph.facebook.com` | | | Must mirror the browser choice; dedup on `event_id` + `event_name` | server |
| Meta CAPI parameter builder | Advertising helper | script `meta-capi-param-builder-clientjs` (`clientParamBuilder.bundle.js`, from a CDN or bundled; also loaded by the Meta GTM template) | none itself | `clientParamBuilder` | works with `_fbp`, `_fbc` | follows the Meta pixel's consent | load, with the pixel. Signals a server-side Meta path: check event ids (FC-03, FC-32) |
| TikTok pixel | Advertising | `analytics.tiktok.com/i18n/pixel` | `analytics.tiktok.com/api/v2/pixel` | `ttq` (`ttq._i`) | `_ttp` | `ttq.holdConsent/grantConsent/revokeConsent`, Shopify gate | load |
| Pinterest tag | Advertising | `s.pinimg.com/ct/core.js` | `ct.pinterest.com` | `pintrk` | `_pin_unauth`, `_derived_epik` | Shopify gate or CMP | load |
| Snap pixel | Advertising | `sc-static.net/scevent.min.js` | `tr.snapchat.com` | `snaptr` | `_scid` | CMP | load |
| Reddit pixel | Advertising | `www.redditstatic.com/ads/pixel.js` | `alb.reddit.com/rp.gif` | `rdt` | `_rdt_uuid` | CMP | load |
| Microsoft UET | Advertising | `bat.bing.com/bat.js` | `bat.bing.com/action` | `uetq` | `_uetsid`, `_uetvid` | UET consent mode (`ad_storage`) | load |
| LinkedIn Insight | Advertising | `snap.licdn.com` | `px.ads.linkedin.com` | `_linkedin_partner_id`, `lintrk` | `li_*` | CMP | load |
| AdRoll | Advertising | `s.adroll.com` | `d.adroll.com` | `adroll` | `__adroll_fpc`, `__ar_v4` | CMP | load |
| Microsoft Clarity | Heatmap and replay | `www.clarity.ms/tag/<id>`, `scripts.clarity.ms` | `*.clarity.ms/collect` | `clarity` | `_clck`, `_clsk` | ConsentV2 (`ad_Storage`, `analytics_Storage`), enforced for EEA, UK, CH since 2025-10-31 | study |
| Hotjar | Heatmap and replay | `static.hotjar.com` | `*.hotjar.com`, `*.hotjar.io` | `hj`, `_hjSettings` (`hjid` is the site ID) | `_hj*` | CMP | study |
| Hotjar on Contentsquare | Heatmap and replay | `static.hj.contentsquare.net` | `t.contentsquare.net`, `*.contentsquare.net` | `hj`, `_hjSettings`, `_uxa` | `_cs_c`, `_cs_id`, `_cs_s` (and `_hj*`) | CMP | study; same tool as Hotjar, newer hosting |
| Lucky Orange | Heatmap and replay | `tools.luckyorange.com` | `*.luckyorange.com` | `LO`, `__lo_site_id` | `_lo_*` | CMP | study |
| Crazy Egg | Heatmap | `script.crazyegg.com` | | `CE2` | `_ce.*` | CMP | study |
| VWO | A/B testing | `dev.visualwebsiteoptimizer.com` | | `_vwo_code` | `_vwo_*`, `_vis_opt_*` | CMP | early only while a test runs, else remove |
| Optimizely | A/B testing | `cdn.optimizely.com` | `logx.optimizely.com` | `optimizely` | `optimizely*` | CMP | early only while a test runs |
| Triple Whale | Attribution (Shopify) | `*.config-security.com` (seen: `conf.`, `api.`), app block `triplewhale/triple_pixel_snippet` | `*.config-security.com` | `TriplePixel`, `TriplePixelData` | not recorded | CMP, Shopify gate for its pixel | load (reads click ids on landing) |
| Klaviyo | Email and SMS | `static.klaviyo.com`, `static-tracking.klaviyo.com` | `a.klaviyo.com` | `klaviyo`, `_learnq` | `__kla_id` | CMP, Shopify gate for its pixel | defer (forms after interaction or delay) |
| Attentive | SMS | `cdn.attn.tv` | `events.attentivemobile.com` | `__attentive` | `__attentive_*` | CMP | defer |
| CallRail | Call tracking | `cdn.callrail.com` | `js.callrail.com` | `CallTrk` | `calltrk_*` | CMP | defer to after DOM ready, only on pages with numbers |
| Chat (Gorgias, Intercom, Zendesk) | Support | `config.gorgias.chat`, `widget.intercom.io`, `static.zdassets.com` | | `GorgiasChat`, `Intercom`, `zE` | various | CMP (functional) | defer: facade, load on click or after idle |
| Reviews (Judge.me, Yotpo, Okendo, Stamped) | Social proof | `cdn.judge.me`, `staticw2.yotpo.com`, `cdn.okendo.io` | | | | usually functional | event: only on templates showing reviews, lazy near the widget |
| Affiliate (ShareASale/Awin, Impact) | Attribution | `static.shareasale.com`, `www.dwin1.com`, `d.impactradius-event.com` | | | `shareasaleShopifySSCID`, `awc` | CMP, Shopify gate | load on landing (click id), conversion on purchase |
| accessiBe | Accessibility overlay (not tracking) | `acsbapp.com` | | `acsbJS` | | usually none | defer. Not analytics, but a third party on every page: list it with an owner like any tag |
| Zenoti | Booking engine (spas, salons, clinics) | its web store on a client subdomain or `*.zenoti.com`, paths like `/webstoreNew/` | none itself (the client's tags fire on its pages) | `dataLayer` | | the vendor's page; the client's consent tool usually absent there | pushes gtag-style commands into the page's `dataLayer` (`checkout`, `purchase` with `eventModel.*`, prefixed events such as `ws2-*`); may run its own container next to the client's (FC-29). Its push shape is a vendor contract for the dependency register |
| Shopify web pixels | Platform | `*/wpm@*/` (web pixels manager), sandbox iframes `web-pixel-*` | per pixel | `Shopify.analytics` | `_shopify_y`, `_shopify_s`, `_tracking_consent` | Customer Privacy API | managed by Shopify (workers and iframes) |
| Consent tools | CMP | Shopify banner (`#shopify-pc__banner`), OneTrust (`cdn.cookielaw.org`), Cookiebot (`consent.cookiebot.com`), Usercentrics, Didomi, CookieYes, Termly, Pandectes, Consentmo, PieEye | | `OneTrust`, `Cookiebot`, `__tcfapi`, `__gpp` | `_tracking_consent`, `OptanonConsent`, `CookieConsent` | n/a | earliest: must run before any tag |
