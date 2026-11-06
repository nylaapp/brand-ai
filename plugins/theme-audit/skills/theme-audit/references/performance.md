# Performance (speed) lane

There is **no 100 target** here. Apps, outside scripts and the store's own images usually cost
the most, and the theme can't fix them. The goal is: every speed problem the theme owns is fixed
or explained, and every cost the theme doesn't own is named with its owner and its measured cost.

Performance fixes are the one place this skill may change *how* a page loads (which image loads
first, when a script runs). They must never change *what the visitor sees* once the page has
loaded. Section 4 is how that is proven.

## 1. Where to measure (three sources, in this order)

### 1a. Field data: real visitors (live site, read-only)

Google's Chrome UX Report holds 28 days of real-visitor speed for busy pages. It is the number
Google uses, and the only source for INP (how fast the page reacts to a tap). Read it for the
**live** page address; reading the live site changes nothing.

```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=<url-encoded live url>&strategy=mobile&category=PERFORMANCE" \
  -o <scratch>/psi-<handle>-mobile.json
```

Read `loadingExperience.metrics` (this page) and, when it is missing, `originLoadingExperience.metrics`
(the whole site; say so). Report the 75th percentile and category of `LARGEST_CONTENTFUL_PAINT_MS`,
`CUMULATIVE_LAYOUT_SHIFT_SCORE` (divide by 100), `INTERACTION_TO_NEXT_PAINT` and
`FIRST_CONTENTFUL_PAINT_MS`. Repeat with `strategy=desktop`.

- No field data (a small or new store): say "not enough real-visitor data yet" and rely on 1b.
- HTTP 429 (the shared free quota is used up): open
  `https://pagespeed.web.dev/analysis?url=<url-encoded live url>` in the browser and read the
  "Discover what your real users are experiencing" section instead. Never ask for an API key in chat.
- Field data takes 28 days to reflect a change. Say that in the report; don't promise a field
  improvement from a lab number.

### 1b. Lab data on the draft theme's preview (the before and after)

The local dev server is slow and uncached, so its speed numbers don't reflect the real site. Score
speed on the draft's preview address, which Shopify serves from its real servers:

`https://<store>.myshopify.com/<path>?preview_theme_id=<draft theme id>`

Run the same address on the live theme too (drop `preview_theme_id`) for a reference: before any
fix, the draft (a copy of live) should score within the run-to-run spread of live. A big gap means
the draft isn't a fair copy; say so before going on.

Shopify's preview bar adds a small, constant cost. It is the same before and after, so the
comparison holds; never chase it.

**Password-protected store:** Lighthouse can't get past the password page. Score speed on the local
dev server instead and label every speed number "local, for before-and-after comparison only, not
the real speed". Field data (1a) still works if the live site is open.

### 1c. Runs

Speed scores move between runs. For every page and form factor:

- **3 runs**, one after another, with nothing else heavy running on the computer.
- If the performance spread (`performance_spread` in the summary) is wider than 10 points, add 2
  more runs (5 in all).
- Report the **median** and the spread, never a single run.

Use the full-suite command from `SKILL.md` step 3a with the preview address (every category, JSON and
HTML saved), so the speed runs and the other scores come from the same runs. When only speed is
being re-measured after a fix, `--only-categories=performance` is enough:

```bash
for i in 1 2 3; do
  npx lighthouse "<preview url>" --output=json --output-path=<scratch>/perf-<handle>-mobile-$i.json \
    --only-categories=performance --chrome-flags="--headless=new" --quiet
done
node <skill>/scripts/lh_summary.mjs <scratch>/perf-<handle>-mobile-*.json > <scratch>/perf-<handle>-mobile.summary.json
```

Desktop: add `--preset=desktop` and name the files `-desktop-`. If the summary shows the wait for
the server (`server-response-time`, or "Time to first byte" in `lcp_breakdown`) is a large part of
the delay, add the Theme Inspector (`liquid-profile.md`): Lighthouse says the server is slow, the
Theme Inspector says which theme files made it so.

Good thresholds, for the plain-language readout: LCP (main content shown) 2.5 s or less, CLS
(layout jumping) 0.1 or less, TBT (page frozen while loading, lab only) 200 ms or less, INP (reacts
to a tap, field only) 200 ms or less.

## 2. Find who owns each cost

From the summary, read `lcp_element` (what the main content is) and `lcp_breakdown` (where its time
goes), `failing.performance` (sorted by the biggest saving) and `third_party` (cost per outside
company: size and main-thread time, the time it keeps the page busy). Put every finding in exactly one
bucket:

| Owner | How to tell | What the skill does |
|---|---|---|
| **This theme** | the file, class or tag is in the theme's own files (search for it) | fix it (section 3) |
| **An app** | the script or element comes from an app: an app embed or app block in `settings_data.json` or a template, a `/apps/` or `cdn.shopify.com/extensions/` address, or an entity in `third_party` matching an installed app | report its cost (KB, main-thread ms) and the owner: the app's settings, its support, or removing it in the store admin. Never disable or remove it. |
| **Outside script added by hand** | a vendor script (chat, reviews, tracking) pasted into a theme file | treat as theme-owned only for adding `defer` or `async`, and only when the vendor's own docs allow it; otherwise report it |
| **Store content** | a huge uploaded image or video, many products on one page, a heavy rich-text embed | report it with the exact file and size; the fix is in the store admin (for example re-upload a smaller image) |
| **Shopify** | `content_for_header`, Shopify's own analytics, checkout or preview-bar scripts, `cdn.shopify.com/shopifycloud/` | skip with evidence; no one can fix these in the theme |

Measure an app's real cost only by reading: the `third_party` table, or the request list in the
browser. Don't switch apps off to test them.

## 3. Theme fixes, chosen deliberately

Lighthouse renames its audits between versions (the summary records the version). Names below are
Lighthouse 13's, with older names in brackets; match by meaning. Most findings list the exact
elements or files, so the first job is always: is that element or file in this theme?

| Finding | Safe fix | Do not |
|---|---|---|
| Main image is lazy-loaded or not prioritised (`lcp-discovery-insight` shows a "not met" line; older `lcp-lazy-loaded`, `prioritize-lcp-image`) | `loading="eager"` and `fetchpriority="high"` on that image, only in the first section on the page (for example `{% if section.index == 1 %}`) | eager-load every image |
| Main image found late (`lcp-discovery-insight` "discoverable" not met; a long "Resource load delay" in `lcp_breakdown`) | preload it with `image_tag: preload: true` (or `preload_tag`), one or two preloads at most | preload many files |
| Main image waits on something else (a long "Element render delay" in `lcp_breakdown`, often a slideshow or fade-in script) | report with the numbers; usually a script or animation that holds the first slide back, which is a design decision: ask | remove the animation |
| Images below the first screen load at once (a long list of images in `network-requests` or a high `total-byte-weight`; older `offscreen-images`) | `loading="lazy"`, for sections after the first one or two | lazy-load anything in the first screen |
| Images without width and height (`cls-culprits-insight`, `unsized-images`, Theme Check `ImgWidthAndHeight`), causing layout shift | add `width` and `height` from the image's own size, or use `image_tag`, which adds them; the displayed box must stay the same size | change the image's shown size or crop |
| Images larger than shown (`image-delivery-insight`; older `uses-responsive-images`, `modern-image-formats`) | `image_url: width:` with `image_tag: widths: ..., sizes: ...`, so the browser picks a fitting size; the largest offered width must cover the shown width at 2x. A `sizes` value that doesn't match the real layout (for example `100vw` for an image shown at a third of the screen) is the usual cause. | lower quality, or offer widths smaller than the shown size (blurry) |
| Theme file blocks the page (`render-blocking-insight`; older `render-blocking-resources`; Theme Check `ParserBlockingScript`) | scripts: add `defer`, after checking no inline script on the page uses that script's code straight away (search the theme for the globals it defines). Stylesheets: report; making CSS non-blocking risks a flash of unstyled page | `defer` or `async` on a script you haven't traced; reorder scripts; load the theme's main stylesheet late |
| Missing or unused early connection (`network-dependency-tree-insight`; older `uses-rel-preconnect`; Theme Check `CdnPreconnect`) | add or remove the `preconnect` line for the host the page really uses | preconnect to hosts the page doesn't use |
| Web font hides text while loading (`font-display-insight`; older `font-display`) | `font_display: 'swap'` in the `font_face` filter. This shows the fallback font for a moment, which is a visible change while loading: ask first | change the font |
| Big theme JavaScript or CSS (`unused-javascript`, `unused-css-rules`, `legacy-javascript-insight`, `duplicated-javascript-insight`, `dom-size-insight`, Theme Check `AssetSize*`) | for theme files, report it as a developer task with the sizes; splitting files is a rebuild, not a safe fix. For outside files, it goes in the owner table | delete code that looks unused |
| Files not cached long (`cache-insight`) | almost always outside scripts or Shopify's servers: owner table | |
| File hosted outside Shopify (Theme Check `RemoteAsset`) | report it; moving it to the theme's own files needs the person's yes (and the file's licence must allow it) | move it silently |

Never, for speed: remove or turn off an app, an app embed or an app block; remove or reorder
sections; swap a video for an image; change an image's crop or art direction; change any words.
Each of those is the store owner's decision. Put it in the report as a suggestion with its cost.

## 4. Prove nothing visible changed

For every page with a speed fix, before and after, at mobile (390 px wide) and desktop (1440 px):

1. Load the page, scroll to the bottom and back (so lazy images load), wait for the network to go quiet.
2. Take a full-page screenshot, and record the position and size
   (`getBoundingClientRect()`) of the header, the LCP element and the first three sections.
3. Compare. Positions and sizes must match; the screenshots must look the same. A difference means
   the fix changed the page: undo it or ask.
4. Check the page still works: open the menu, open the cart, pick a product option, and read the
   console for new errors. A script given `defer` that breaks any of these is undone.
5. For responsive images, confirm on the page that each changed image's `naturalWidth` is at least
   its shown width times the screen's pixel ratio (not blurry).

## 5. Re-measure and report

Repeat 1b with the same number of runs, same address, same form factors. A change is real only
when the new median is outside the baseline's spread; otherwise report "no measurable change" for
that page. Report per page: the score and LCP, CLS and TBT before and after (median and spread),
field data as it stands today with the 28-day note, what was fixed, and the costs the theme
doesn't own, largest first, each with its owner.
