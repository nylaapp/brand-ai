# Report: THEME-AUDIT.md and the chat readout

## Where it goes

`THEME-AUDIT.md` in the theme copy's folder, at its root beside the brand files (never inside
`assets/`, which is public). Each run adds a new dated entry at the top; older entries stay below.
If the project also keeps a QA log (for example `design-qa.md`), add a three-line pointer there.
Write "not run" for anything that wasn't run, never a guess.

## Entry template

```markdown
## <YYYY-MM-DD>: <pages in scope>, theme "<theme name>" (<theme id>)

Scope: <lanes run>. Measured with the Lighthouse command-line tool <version>, not the Chrome
extension. Accessibility, best practices and SEO on the local preview; speed on the draft's
preview address, median of <n> runs (or: local only, because the store is password protected).

### Scores

| Page | Form | Speed | Accessibility | Best practices | SEO |
|---|---|---|---|---|---|
| <page> | Mobile | 41 -> 55 (spread 38-45) | 0.91 -> 1.00 | 0.78 -> 0.96 | 0.92 -> 1.00 |
| <page> | Desktop | ... | ... | ... | ... |

### Speed detail

| Page | Form | Main content shown (LCP) | Layout jumping (CLS) | Frozen while loading (TBT) | Real visitors (28 days) |
|---|---|---|---|---|---|
| <page> | Mobile | 4.8 s -> 3.1 s | 0.21 -> 0.02 | 610 ms -> 540 ms | LCP 3.9 s, CLS 0.08, INP 240 ms (or "not enough data yet") |

Real-visitor numbers take 28 days to show a change.

### Theme code check

Offenses: <before> -> <after>. Broken: <n> -> <n>. Speed: <n> -> <n>. Style findings: <n>, left as they are.

| Check | What it means | Count | Files | Status |
|---|---|---|---|---|

### Fixed

| Page | Lane | Finding | File | Change (before -> after) | Proof |
|---|---|---|---|---|---|

### Not fixed, and who owns it

Largest cost first.

| Finding | Cost | Owner | Suggested next step |
|---|---|---|---|
| <App name> script | 180 KB, 420 ms busy time | App | Check whether the app is still used; remove it in the store admin if not |
| Hero image is 4.1 MB | slows main content | Store content | Re-upload a smaller version (under 500 KB) |
| Shopify's own scripts | ... | Shopify | Nothing to do |

### Needs the store owner

<merchant content, unpublished pages, store writes made, app decisions>

### Push

Pushed <files> to "<theme name>" (<id>). Pulled back and compared: identical. (Or: not pushed.)
```

## Chat readout (short)

Plain words, no technical terms without a short explanation. In this order:

1. One line per page: the four scores before and after, mobile and desktop.
2. The single biggest cost the theme doesn't own, with its owner.
3. What was fixed, in one sentence per kind of fix.
4. What needs the store owner.
5. Where the full report is (`THEME-AUDIT.md`).
