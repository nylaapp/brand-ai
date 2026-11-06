# Report: THEME-AUDIT.md and the chat readout

## Where it goes

`THEME-AUDIT.md` in the theme copy's folder, at its root beside the brand files (never inside
`assets/`, which is public). Each run adds a new dated entry at the top; older entries stay below.
If the project also keeps a QA log (for example `design-qa.md`), add a three-line pointer there.
Write "not run" for anything that wasn't run, never a guess.

## Entry template

```markdown
## <YYYY-MM-DD>: <pages in scope>, theme "<theme name>" (<theme id>, <live or draft>)

### Read this first

<the readout, exactly as written in chat: `readout.md`>

### How this was measured

Scope: <lanes run, and any "not run" with the reason>. Mode: <audit only or audit and fix>.
Lighthouse <version> from the command line, not the Chrome extension, full suite (performance,
accessibility, best practices, SEO), <n> runs per form factor, median reported. Reports: <folder
with the HTML and JSON files, one per run>. Server timing: `shopify theme profile`, <n> runs.

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

### Server timing (Theme Inspector)

Total Liquid time in the profile: <median ms> (<heavy / OK / light>); real wait for the server from
Lighthouse: <ms>. Profiles: <files>.

| Theme file | Kind | Own time | With what it renders | Times rendered | Share of total |
|---|---|---|---|---|---|

Costliest lines: `<file:line>` (<tag>, <ms>, <runs> runs). Anything an app owns: <name, ms>.

### Theme code check

Offenses: <before> -> <after>. Broken: <n> -> <n>. Speed: <n> -> <n>. Style findings: <n>, left as they are.

| Check | What it means | Count | Files | Status |
|---|---|---|---|---|

### All findings

Every finding with an ID (TA-01, TA-02...), in rank order, with the evidence behind it.

| ID | Lane | Finding | Evidence (audit, element, file:line, number) | Owner | Bucket | Effort | How we know |
|---|---|---|---|---|---|---|---|

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

## Chat readout

Follow `readout.md` (headline, what I looked at, scorecard, speed in plain words, fix these first,
quick wins, not the theme's to fix, what I couldn't check, close). The same text is **Read this
first** at the top of the entry.
