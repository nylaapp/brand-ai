# Privacy-state test matrix

Tags behave differently depending on what the visitor chose, where they are and what their browser blocks. A setup that works for a consenting visitor in one country can double count, leak or go silent for everyone else. Every full audit and every fix that touches tags runs this matrix for the core events.

This is a measurement check, not legal advice. Report what fires; leave "is this compliant" to the client's counsel.

## 1. States

| State | How to produce it | What it tells you |
|---|---|---|
| `fresh` | New browser profile, no banner interaction | Defaults before any choice: what fires on landing |
| `accept` | Click "accept all" in the banner | The full setup |
| `reject` | Click "reject all" | Whether rejection is honoured (cookieless pings only, or nothing) |
| `partial` | Analytics yes, marketing no (banner preferences) | Category mapping (analytics vs ads) |
| `withdraw` | Accept, then reopen preferences and reject | Whether a change of mind takes effect on the next page |
| `gpc` | `Sec-GPC: 1` header and `navigator.globalPrivacyControl = true` | Opt-out signal in US states that require it; Shopify sets sale of data to no |
| `blocked` | Ad and tracker domains blocked | What a blocker user leaves behind (server-side paths keep working). Context, not a bug |

`scripts/privacy_matrix.cjs` produces fresh, accept, reject, gpc and blocked automatically. Per state it saves `hits.har` (every collection request, tagged with scenario, step and sending frame), a full HAR per scenario under `har/`, and `inventory.json` (inventory results, dataLayer snapshots, clicks, stopped navigations, redirects). Partial and withdraw need the banner's preferences UI: do them in a browser by hand or add steps. If the banner's buttons are not found, pass `--accept` and `--reject` selectors; if there is no banner, say so (that is itself a finding in consent-required regions).

### Dry capture (default for live sites)

`--dry` answers every collection request locally with an empty HTTP 204 and logs it in full: method, URL, body, the frame that sent it and the journey step. The audit sees exactly what each tag would have sent, and the client's GA4, ad accounts, Shopify analytics and other tools receive no test page views, clicks or conversions. Pages and scripts still load from the site, so tags behave normally.

- Covered endpoints: GA4 (Google's and first-party `/g/collect`), Google mirrors, Merchant Center, Google Ads and remarketing, Floodlight, Meta, TikTok (including the Shopify app's `/api/v2/shopify_pixel`), Clarity, Microsoft UET, Pinterest, Reddit, Snapchat, LinkedIn, X, Shopify's own analytics (monorail), Triple Whale, Klaviyo client events, Contentsquare and Hotjar, CallRail sessions. Add a server-side tagging path or any other endpoint with `--dry-extra <regex>`. Live-session websockets (Hotjar, Contentsquare, Clarity) are held locally when Playwright supports it.
- Requests are fulfilled, not aborted: an aborted request loses its POST body, and batched GA4, TikTok and Shopify hits travel in POST bodies.
- The run prints a warning if any collection request reached the network; `decode_hits.py` repeats it. Investigate before using the capture.
- Run without `--dry` only to confirm the receiving side (GA4 DebugView, Meta Test Events) during an agreed test window, with the owner's OK.

### Journeys

`--scenarios journeys.json` lists named scenarios; each gets a fresh browser profile per state, and an optional `"states"` list limits where it runs. Every step has a `label`, which `hits.har` and `decode_hits.py --by-step` use, so each hit can be traced to the step that caused it. Steps: `goto`, `click` (with optional `text`), `fill` (test values only), `wait`, `inventory`, `dataLayer`.

- **Clicks** are dispatched on the element from inside the page, so cookie bars, chat widgets and pop-ups cannot swallow them. A link's navigation is answered locally with 204, so the page stays and its listeners keep running: the click event is not cancelled, so tag-manager link-click triggers (including those with "Check validation") see a normal click. The destination is recorded. `"navigate": true` follows the link; `"stop": "prevent"` stops it with a capture-phase `preventDefault` instead, which hides the click from triggers that check validation. Buttons are never stopped.
- **Destinations get their own step.** Test a booking or checkout landing with an explicit `goto` to the URL the CTA points to. A landing that ends elsewhere is recorded as `redirectedFrom` (see FC-35).
- **Visitor profile.** The browser hides the automation flag (`navigator.webdriver` false, a normal Chrome user agent), because some pixels (Meta's) send nothing to a browser that says it is automated. `--webdriver-visible` turns this off; say in the method section which profile was used.

### Which install point sent a hit

`decode_hits.py hits.har --by-source` attributes each hit from what the request shows: the sending frame (top page, Shopify custom pixel sandbox, Shopify app pixel sandbox, other iframe, service worker), the GA4 endpoint (Google's, or a first-party one such as a server container), the `z8<number>` marker in the `gtm` parameter of Google hits (a tag in that GTM container fired it; no marker means the Google tag's own events or a gtag call from an app or code), Meta event ids (`sh-` is Shopify's Meta app; other prefixes come from the theme, a tag manager or code) and TikTok's Shopify endpoint. It then lists every event a destination got from more than one source in the same step: the evidence for FC-01, FC-33 and FC-34. These are observed conventions, not vendor documentation: confirm a surprising attribution with the container, the pixel list or the app settings. Copies sent to `www.google.com/g/collect` and `stats.g.doubleclick.net` (Google's ads and signals measurement) and to `merchant-center-analytics.goog` are listed separately, never as GA4 events.

## 2. Regions

The store decides what to show by the visitor's IP. Test each region type the store serves:

| Region type | Example | Expect |
|---|---|---|
| Consent required | EEA, UK, Switzerland | Banner; marketing and analytics off until accepted; Google defaults denied (`gcs=G100`), cookieless pings at most |
| Opt-out | California and the other GPC states | Usually no banner; tracking on; a "Your privacy choices" link; GPC turns off sale and sharing |
| Neither | Most other places | Tracking on by default (`gcs=G111` or no gcs) |

How to be "in" a region: a proxy or VPN exit in that region (`privacy_matrix.cjs --proxy`), a remote test location, or a person there. On Shopify, `Shopify.customerPrivacy.getRegion()` (shown by `page_inventory.js`) says which region the store thinks you are in: always record it. If a region cannot be produced, write "not tested" for it; never infer it from another region.

## 3. Expectations to check per state

For each core event (from ANALYTICS.md section 1) and each state, record per destination: sent once, sent twice, not sent, or sent cookieless.

| Signal | Where to read it | Expected when consent is denied |
|---|---|---|
| Google consent state | `gcs` and `gcd` on Google requests (`decode_hits.py`); `googleConsentState` in the inventory | `gcs=G100`; `gcd` letters `p` or `q` (denied). Advanced consent mode still sends cookieless pings; basic sends nothing |
| Google cookies | `_ga`, `_ga_*`, `_gcl_*` in cookie names | absent |
| Meta | requests to `facebook.com/tr`; `_fbp`, `_fbc` cookies | none, unless the client deliberately runs Meta in limited mode |
| TikTok, Pinterest, Snap, Reddit, UET | their collect endpoints; their cookies | none |
| Clarity | `clarity.ms/collect`; `_clck`, `_clsk` | EEA, UK, CH: no cookies without ConsentV2 granted (enforced since 2025-10-31) |
| Shopify pixels | `Shopify.customerPrivacy` allowed flags; pixel purposes | pixels needing Analytics or Marketing do not run; with GPC or sale opt-out, pixels marked as data sale do not run |
| Server-side | the server endpoint or platform logs | must respect the same choice; a browser check alone cannot prove it, so list it as "not verified from the browser" |

Accept state: every core event reaches every destination it should, exactly once, with the right parameters (`transaction_id`, `value`, `currency`, items; Meta `event_id` shared between pixel and CAPI).

## 4. Running it safely

- **Test traffic pollutes the client's data.** On live sites run the matrix with `--dry` (section 1), so no test hit reaches any account; page loads still reach the site. Without it, prefer a preview theme or staging, keep runs short, use GA4's internal-traffic or debug parameters if the client has them, and tell the client when and from where you tested.
- **Never place a real order or booking** without the owner's explicit OK for that specific test. Use the platform's test mode (Shopify Bogus Gateway on a development store, a 100 percent discount code the owner creates and then deletes, a booking engine's test location) and note the test order number in section 8 so it can be excluded or refunded.
- **Never type real customer data** into forms. Use obvious test values (`test+analytics@<client domain>` only if the client provides it).
- Never sign in for the person, never accept terms on their behalf, never change the banner's settings to make a test pass.

## 5. Recording

Write the result table into ANALYTICS.md section 8: date, states, regions, regions not tested, dry or live capture, the visitor profile, and per event and state the outcome with its source (which install point sent it). Attach nothing personal. Keep the HARs in the session's scratch folder, not in the repo (they contain cookies and IP-derived data).
