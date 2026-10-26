# Observation recipes

How to observe a rendered page so the playbook's checks are marked from evidence and every
run measures the same way. Run these in the browser on the real page (a draft theme preview
is fine), at desktop (1440x900) and mobile (375x812). Record each number with its source,
date and device.

## Protocol

1. **Set a real viewport first.** A browser pane can report a 0x0 viewport, which makes
   full-screen sections balloon to thousands of pixels. Resize explicitly, then check
   `innerWidth` and `innerHeight` are not zero before measuring anything.
2. **Confirm what you are looking at.** A preview parameter can be dropped by a redirect,
   leaving you on the live theme. After loading, read the theme id the page reports (on
   Shopify, `Shopify.theme.id`) and compare it with the theme you were asked to test.
3. **Load fresh, then scroll slowly to the bottom and back to the top.** Lazy images report
   a natural width of 0 until they are near the viewport; don't judge image size before
   scrolling. Re-load per viewport rather than only resizing, so layout and overlays rerun.
4. **Note overlays at 1 s and about 15 s** after load: consent banners, sign-up modals,
   chat widgets. Record size, position and what they cover in the first screen.
5. **Measure, don't eyeball:** positions and heights from `getBoundingClientRect()`,
   copy from `innerText`, links from `href`.
6. **Say what you could not observe.** Missing data is "Can't tell", never a failed check.

## When access or data is blocked

| Blocker | What to do |
|---|---|
| Storefront is password protected | Don't type a password on the person's behalf. Ask them to enter it in the browser or lift it; or offer a local preview from the theme CLI. Meanwhile read theme files only and mark render checks "Can't tell". |
| Admin or store is not signed in | Ask the person to sign in themselves; use the CLI or connector where it is already authenticated. |
| Analytics connector points at a different store | Check the connected store's domain first (shop info); if it is not the page's store, say so and ask for an export instead. |
| PageSpeed or Lighthouse quota exceeded | Say so, retry later, or ask for a shared report; mark speed "Can't tell". Never estimate scores. |
| Third-party tool or destination page is off-site | Observe it read-only (status, visible dates, terms) and report it as an off-site finding. |

## Snippets

Each runs in the page context and returns JSON. Adjust selectors to the theme.

**Section inventory (position, height, first words)**

```js
[...document.querySelectorAll('#MainContent > .shopify-section')].map(s => {
  const r = s.getBoundingClientRect();
  return { id: s.id.split('__').pop(), top: Math.round(r.top + scrollY),
           h: Math.round(r.height), text: s.innerText.replace(/\s+/g, ' ').trim().slice(0, 70) };
});
```

**Headings and h1 count**

```js
({ h1: [...document.querySelectorAll('h1')].map(h => h.textContent.trim()),
   outline: [...document.querySelectorAll('main h1,main h2,main h3')]
     .map(h => h.tagName + ':' + h.textContent.trim().slice(0, 40)) });
```

**Link map by destination (shows how far each action is from the goal)**

```js
[...document.querySelectorAll('a[href]')].map(a => ({
  label: a.textContent.trim().replace(/\s+/g, ' ').slice(0, 30),
  to: a.host + a.pathname,
  top: Math.round(a.getBoundingClientRect().top + scrollY),
  section: (a.closest('.shopify-section') || {id: '?'}).id.split('__').pop() }))
  .filter(l => l.label);
```

Group by `to`, count distinct labels per destination, and record the first position of the
link that reaches the primary action. Follow the path one page at a time to count clicks.

**Overlays covering the first screen**

```js
[...document.querySelectorAll('body *')].filter(e => {
  const cs = getComputedStyle(e), r = e.getBoundingClientRect();
  return cs.position === 'fixed' && r.width > 200 && r.height > 100 && cs.display !== 'none'
    && cs.visibility !== 'hidden' && +cs.opacity > 0.1 && r.bottom > 0 && r.top < innerHeight;
}).map(e => ({ id: (e.id || e.className).toString().slice(0, 40),
  w: Math.round(e.getBoundingClientRect().width), h: Math.round(e.getBoundingClientRect().height),
  top: Math.round(e.getBoundingClientRect().top), text: e.innerText.replace(/\s+/g, ' ').slice(0, 60) }));
```

Compare each overlay's rectangle with the primary button's rectangle.

**Tap targets under the playbook thresholds**

```js
[...document.querySelectorAll('main a, main button')].map(e => ({ e, r: e.getBoundingClientRect() }))
  .filter(o => o.r.width > 0 && o.r.height > 0 && o.r.height < 44 && o.e.textContent.trim())
  .map(o => ({ text: o.e.textContent.trim().slice(0, 24), h: Math.round(o.r.height), w: Math.round(o.r.width) }));
```

WCAG 2.2 AA minimum is 24x24 CSS px (with spacing, inline and equivalent exceptions);
44 to 48 px is common advice (grade B). Report which threshold a target misses.

**Images: size versus display, and alt text**

```js
[...document.querySelectorAll('main img')].map(i => ({
  alt: i.alt.slice(0, 40), noAltAttr: !i.hasAttribute('alt'),
  natural: i.naturalWidth, shown: Math.round(i.getBoundingClientRect().width) }));
```

Only trust `natural` after the slow scroll in the protocol. Flag images shown more than
about 1.2x their natural width.

**Carousel autoplay**: read the scroll position of the track, wait about 7 seconds
without interacting, read it again; unchanged means no autoplay on that carousel.

**Claims scan (numbers, superlatives, regulated wording)**

```js
(document.querySelector('main').innerText
  .match(/[^.\n]*(\d[\d,]+ (patients|customers|clients|reviews)|award|proven|clinically|best|#1|certified)[^.\n]*/gi) || [])
  .map(x => x.trim().slice(0, 90));
```

Each hit is checked against the brand files; with none, it is a "no source on the page"
note and goes to a fact-check, not a verdict.

**Off-site destination check (offer or booking pages)**: fetch the page read-only, record
the status code and any visible dates, prices and terms, and compare them with what the
linking page promises.

## What to record

For each playbook check: ID, status, the observation (number, position or quote), viewport,
and date. The gap report quotes these, so a reader can reproduce any row.
