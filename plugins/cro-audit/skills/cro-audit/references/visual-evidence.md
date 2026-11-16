# Visual evidence: show the problem, then the fix

Show every important finding on a picture of the real page, with numbered boxes on the exact elements,
and the numbered changes beside it. A reader who sees the problem believes it. A reader who only
reads a description has to take it on trust.

## 1. What gets a picture

- Every row in "Fix these first" and every stage block in the funnel report (`funnel-stages.md`).
- Device-specific findings get the device they happen on. A phone problem gets a phone picture.
- First-visit behaviour (a popup, a cookie banner) gets a picture at the moment it happens. For example,
  use `--wait 7` for a popup that opens at 6 seconds. Also take a picture without it, to show what it
  covers.
- Findings with no visible element (a duplicate tag, a slow file) get none. Use a number instead.

## 2. Take the picture

Use `scripts/evidence_shot.py`, best source first:

1. **`--capture <url>`** (needs Chrome or Chromium on the computer):
   - It opens the page in a fresh, private profile as a phone (390 × 844) or a desktop (1440 × 900).
   - It waits, then scrolls to the section with wheel events, like a visitor.
   - It boxes elements by CSS selector (`--mark-el "1=<selector>"`). Get selectors from the page in
     the browser you're auditing with. Shopify section wrappers have stable ids
     (`#shopify-section-…`).
   - It prints which theme the page showed. If the role isn't `main` and the person didn't ask for a
     draft, add `?preview_theme_id=<live id>` to the URL.
2. **`--image <file>`**: a screenshot the person sends, or one your browser tool saved, with
   `--css-width` set to the page width it was taken at. Place boxes with `--box "1:x,y,w,h"` in CSS
   pixels, measured at that width.
3. **`--lighthouse <report.json>`**: the full-page screenshot inside the Lighthouse report from the
   speed check. It is often taken mid-load (a popup's grey backdrop, images not yet loaded). Use it
   only when nothing else works, and say so in the caption.

No browser and no screenshot at all: describe the element and its position in words, and say pictures
weren't possible.

## 3. Rules

- **Read-only.** Loading and scrolling only. Never click, type, submit or answer the cookie banner to
  get a picture. If a popup must be gone, take the picture before it opens (a shorter `--wait`).
- **The live theme**, unless the person asked about a draft. The caption says which.
- **No personal data in a picture.** Don't capture a signed-in account, an order or a filled form. Crop
  out anything personal that appears.
- **One idea per picture.** Crop to the section (`--selector`), not the whole page. Use at most four
  boxes, numbered in reading order. The numbers match the "What to change" list beside the picture.
- **Caption:** `<finding ID> · <device> · <where or when>`, for example "CRO-02 · phone · 8 s after
  load".
- **Before and after.** For copy or layout changes, a "Next" picture can show the proposed version only
  once it exists on a draft theme (made by `page-edit-content` or `page-edit-design`). Never mock up
  the client's page by editing it. Describe the change in words until then.

## 4. Where the files go

- Save the pictures in `cro-evidence/` beside `CRO-AUDIT.md`, named `<finding id>-<device>.svg`
  (stage blocks: `stage-<n>-<device>.svg`). `--capture` also keeps the PNG beside it, for decks and
  documents that don't take SVG.
- In `CRO-AUDIT.md`, place a picture with `![CRO-02 · phone · 8 s after load](cro-evidence/cro-02-phone.svg)`,
  followed by the numbered list.
- Re-audits take new pictures, and the old ones are kept with the run date in the name, so changes can
  be compared.

## 5. A deck or shareable page, only when asked

The Markdown file and the chat readout are the default. Make a deck or a web page only when the person
asks, for example because a client needs it. It takes far more effort and usage than the readout.

Build it from the same content, one slide or panel per block:

1. **Cover:** the brand, the page or store audited, and the date.
2. **What we looked at:** the data, devices and window, and what wasn't available.
3. **Funnel summary:** the stage table with coloured verdicts.
4. **One slide per stage:** the grid on the left, the insight bullets on the right. Follow it with one
   slide per finding: the picture on the left and the numbered changes on the right.
5. **Worth testing:** each test with its feasibility.
6. **Next steps and what wasn't checked.**

Use the host's slides tool if there is one (for example a Slides artifact or the pptx skill).
Otherwise, use a single HTML page with the same sections. Use the PNG versions of the pictures where
SVG isn't supported.
