# Load timing: when each tag should load

Some tags have to load immediately; most do not. Loading a tag later than needed loses data; loading it earlier than needed costs every visitor speed for nothing. Decide per tag, write the rule in the load policy, and implement it in the place the tag lives.

## 1. What must load early, and why

| Tag | Why early | How early |
|---|---|---|
| Consent defaults and the banner or CMP | Every other tag reads its state; defaults must exist before any tag runs | First in the head (GTM: Consent Initialization trigger) |
| Tag manager container | It carries the rules for everything else | Head, async |
| Analytics base (GA4 config, page view) | Captures the landing page, referrer and campaign parameters; a visitor who leaves in two seconds still counts | Head, async; after consent defaults |
| Ad click-id capture (Google conversion linker, Meta base for `fbclid`, affiliate landing scripts) | The click id is only in the landing URL | At load, async |
| A/B test that changes what is above the fold | Changing content after paint causes flicker and layout shift | Early, only while a test runs; prefer server-side or edge testing |

Everything else can wait.

## 2. What can wait

| Tag | Rule |
|---|---|
| Conversion tags (purchase, lead, booking) | Fire on the event only; never load the vendor's library on every page just to be ready |
| Ad base pixels beyond click capture (audiences) | Async at load or after load; through a Shopify app pixel (sandboxed) where available |
| Heatmaps and session replay | On demand, during a study only; then after load or on idle |
| Chat widgets | A facade (a button that looks like the widget) that loads the real script on click, or after idle on pages where chat matters |
| Review widgets | Only on templates that show reviews; lazy-load near the widget |
| Email and SMS popups | After a delay, scroll depth or exit intent; never in the first seconds |
| Call tracking number swap | After DOM ready, only on pages that show numbers |
| Social embeds and video | Facade until clicked |

## 3. How to implement, by install point

| Install point | Tools |
|---|---|
| Theme code | Liquid template conditions (`{% if template.name == 'product' %}`); `defer`; inject after `load` or on first interaction (`pointerdown`, `keydown`, `scroll`, with a timeout fallback); `requestIdleCallback` |
| App embeds | Disable on themes or templates where not needed; ask the app vendor for a lighter mode |
| Shopify pixels | Already sandboxed (app pixels in web workers, custom pixels in iframes) and gated by consent; prefer them over theme scripts for anything that only needs standard events |
| GTM | Triggers on Window Loaded, a custom `idle` or `first_interaction` event pushed by the site, page-path conditions, or the specific event; tag sequencing for dependencies; consent checks per tag |
| Server-side | Moves work off the browser for conversions and audiences; still needs consent mirrored and deduplication |

Rules:
- **Delay never breaks a conversion.** A conversion tag that depends on a delayed library must queue its event (most vendor snippets queue calls before the library arrives) or be sent server-side.
- **Do not delay what captures the landing.** Campaign parameters and click ids must be read on the first page.
- **Test after every change:** accept-state events once each, and a HAR showing the tag loads when the rule says.
- **Write the rule** in the load policy (ANALYTICS.md section 7): "Hotjar: on demand, study 'PDP drop-off' until 2026-11-30, 25 percent sample, after load".
