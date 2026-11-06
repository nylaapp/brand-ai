---
name: theme-audit
description: "Audit a Shopify theme's pages with the full Lighthouse suite from the command line (speed and performance, accessibility, best practices and SEO, mobile and desktop, several runs, with the HTML reports saved), plus Shopify's Theme Inspector (how long the theme's Liquid code takes on the server) and Shopify's own Theme Check on the theme code, and present the result as a plain-language readout (headline, scorecard, fix these first) the way the CRO audit does; name who owns every problem (this theme, an app, store content or Shopify); propose minimal fixes for what the theme owns; and after approval apply them on a draft theme, prove nothing visible changed, and re-score. Accessibility is fixed to 1.00; speed is measured as a median of several runs with real-visitor data where it exists, with no 100 target. Use whenever the user says \"run Lighthouse\", \"score this page\", \"audit the theme\", \"theme check\", \"why is the site slow\", \"page speed\", \"performance score\", \"Core Web Vitals\", \"LCP\", \"CLS\", \"best practices\", \"accessibility audit\", \"check accessibility on the product page\", \"get this to 100%\", \"fix the a11y score\", or asks to improve any Lighthouse score on a page template, even if they don't say Lighthouse. Can run one lane alone (for example accessibility only), and can run read-only on a live page with no fixes. Never removes apps, changes words or moves layout; works only on a draft theme (asked once, remembered, or created from the live theme) and never edits the live theme. Not for content and page-type gaps (page-studio's page-audit), conversion audits (cro-audit) or deep blog SEO (seo-audit)."
---

# Theme audit (Lighthouse, Theme Check, classify, fix, re-score)

## How to reply (every message)

These rules apply to every message this skill writes to the person, in Claude or in any other AI app.
They take priority over any other tone guidance in this skill or its reference files.
They cover messages to the person only. Content written for the brand (posts, page copy, product
text) follows the brand's own voice from `BRAND-VOICE.md`.

- **Short and direct.** Start with the answer or the next action. Say only what the person needs to
  know, decide or do next. No long introductions, recaps or repeated warnings. Put long detail in the
  saved file, not in the chat.
- **No technical knowledge assumed, including of Shopify.** Avoid technical terms (for example theme
  files, CLI, API, metafields, JSON, schema, cron). If one is needed, explain it in a few plain words
  the first time.
- **Step-by-step for anything the person must do.** When they need to set up, sign in, click, export or
  install something, give numbered steps, one action per step. Name the exact button or menu, and say
  what they should see when it worked.
- **Simple English.** Short sentences, common words, one idea per sentence. No idioms, figures of
  speech, jokes or slang.
- **Formal and professional.** Polite and neutral. No exclamation marks, emoji or hype words.
- **Not intimidating.** Do not list everything that could go wrong. When something fails, say what
  happened and what to do next.

## Two modes

- **Audit only (read-only).** The person wants scores and findings ("audit the homepage", "why is the
  site slow"). Nothing is edited or pushed, so **no draft theme is needed yet**: run the lanes against
  the live page and the live theme, which only reads. End with the readout and offer the fixes.
- **Audit and fix.** The person wants the problems fixed ("get this to 100%", "fix the speed
  issues"), or says yes to the offer after an audit. Settle the draft theme (below), then go through
  every step.

Say which mode this is in one line. When unclear, start in audit-only mode.

## Effort (read before starting)

About 30 to 60 minutes per page template for all lanes, mostly waiting on Lighthouse runs (speed
needs several runs per form factor). Accessibility alone is about 15 to 40 minutes. Estimates, not
yet measured. Stop and tell the person if a pass passes 2 hours.

**Goal: better scores and a healthier theme without moving anything a visitor or the store owner
can see.** The owner judges "did anything change" by eye, so this is a trust contract: why each
rule below exists is to keep that trust.

If the project has its own instructions file (for example `AGENTS.md` or `CLAUDE.md`) with safety
rules or invariants, read it first and follow it; it outranks this skill.

**Setup check first.** Before anything else, run `references/setup-check.md` for the `theme-audit`
column: a browser, the page address, Node.js, the Shopify CLI signed in to the store, Google
Chrome, Lighthouse and a folder for the theme copy. Assume the person isn't technical: check
silently yourself, then walk them through anything missing one step at a time, in plain words, and
re-check after each step. Skip it if it already passed in this conversation. Nothing else starts
until every required item passes.

**Theme first (audit and fix mode; in audit-only mode, wait until the person asks for fixes).** Before step 1, settle which theme this run is for, following
`references/theme-target.md`: use the theme the person already chose in this conversation or
recorded in `THEME-TARGET.md` and say so in one line, or settle a draft: ask whether one already
exists or create one, never the live theme (the project's theme config may default to the live
theme, so don't use that default) and remember the answer for every other skill. Don't ask again
unless the person names a different theme. The local dev server previews the working copy; the
draft's preview address is where speed is measured; the chosen theme is where approved fixes are
pushed in step 8.

## The lanes

| Lane | Measured on | Target | Guide |
|---|---|---|---|
| Accessibility | Lighthouse, full suite | 1.00 on every page, both form factors | `references/accessibility.md`, `references/contrast.md` |
| Speed (performance) | Lighthouse, full suite, median of 3 to 5 runs; real-visitor data from the live site | every theme-owned cost fixed or explained; no 100 target | `references/performance.md` |
| Best practices | Lighthouse, full suite | every theme-owned finding fixed | `references/best-practices-seo.md` |
| SEO (quick check) | Lighthouse, full suite; crawlability on live | every theme-owned finding fixed; deeper SEO goes to `seo-audit` | `references/best-practices-seo.md` |
| Server speed (Theme Inspector) | `shopify theme profile`, one page, 3 runs | the slowest theme files named; nothing to fix blindly | `references/liquid-profile.md` |
| Theme Check | the theme copy, whole theme, once | nothing broken in pages in scope; never a new offense | `references/theme-check.md` |

"Lighthouse, full suite" means every category in every run, on phone and desktop, saved as JSON for
the numbers and HTML for the person. Lighthouse 13 has four main scores (performance,
accessibility, best practices, SEO); version 13.6 adds a fifth, **agentic browsing** (can AI
assistants read and use the site: a clean accessibility tree, a valid `llms.txt`, WebMCP), which Google
marks as still under development. Report it as an extra row, never in the headline, and with that
caveat. Lighthouse no longer has a progressive-web-app score. Read the category list from the report
rather than assuming it; the summary does.

**Scope.** Run every lane unless the person asked for fewer ("accessibility audit", "just the
speed", "only theme check"): then run only those, and say in one line which lanes run. In fix mode,
Theme Check always runs as the safety net (section 0), even when its findings aren't in scope. A
lane that can't run (for example the Theme Inspector when the Shopify CLI isn't signed in to the
store, or Theme Check when there is no theme copy yet) is marked "not run" with the reason, never
skipped silently.

## 0. Non-negotiables

- **Nothing a visitor can see changes.** Accessibility, best-practices and SEO fixes are additive: an
  `aria-*` attribute, a `role`, a visually-hidden label, a guard around a blank or broken dynamic
  value, a missing `<head>` tag, or a minimum contrast nudge. Speed fixes may change *how* the page
  loads (which image loads first, when a theme script runs, image sizes offered), never what the
  loaded page looks like; `references/performance.md` section 4 is the proof. Never move, resize,
  reword or restyle. If a real fix needs a visible change, stop and ask; don't reinterpret "no
  changes" to permit it.
- **Never remove, turn off or reconfigure an app**, app embed or app block, and never edit store
  content (products, pages, images, descriptions). Report their cost and owner; the store owner
  decides.
- **Push only to a draft theme, never the live theme.** Pushing means that theme by id.
  `--allow-live` is never used, and neither is `--publish` (which makes a draft the live theme): the
  person publishes in the store admin (`references/theme-target.md` section 5).
- **Don't edit shared, vendor or base theme files** (global stylesheets, the theme's core scripts,
  shared colour-scheme tokens). If it's unavoidable, keep the edit minimal, mark it with a comment
  saying what and why, and log it.
- **Theme Check may only get better.** Take a clean baseline first (`references/theme-check.md`);
  don't trust a remembered number. After every edit, `new_offenses` must be empty.
  `--auto-correct` is never used.
- **Verify every fix on the rendered page**, never from the code alone. Reading
  `document.querySelector(...).getAttribute('role')` on the running page is verification; "I added
  the role" is not.
- **Report speed as a median with its spread**, never a single run, and never call a change real
  when it's inside the run-to-run spread.
- **Reading the live site is fine; changing it is not.** Field data and the live reference runs only
  read.
- Never enter credentials or 2FA codes in a browser, and never ask for an API key in chat. The person
  signs in themselves.

## 1. Resolve a real 200 URL per template

Lighthouse won't audit non-200 responses. For each page template:

1. Look for a Shopify Page that uses the template (read-only GraphQL): `query { pages(first: 50) { nodes { handle title templateSuffix } } }`, and paginate past 50 so no page is missed.
2. Confirm it is published: `query { page(id: "gid://shopify/Page/...") { handle templateSuffix isPublished } }`. `isPublished: false` is why it returns 404.
3. If it is unpublished, publish it only if every other requested page already follows that pattern. Publishing is a real store write: state it plainly in the summary and get the person's OK first.
4. If no Page exists at all, stop and tell the person (it's a content decision).
5. Confirm the status: `curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:9292/pages/<handle>"`. Product, collection and home templates use their normal routes (pick a real, published product or collection).

## 2. Theme Check baseline (whole theme, once)

Pull the chosen draft into the working folder if it isn't there yet, then run Theme Check and its
summary (`references/theme-check.md` section 1). Keep the baseline file: every later comparison
uses it. Audit-only mode with no theme copy: pulling the live theme to a scratch folder is a read, so
it is allowed for this check only (`shopify theme pull --theme <live id> --path <scratch>`, never
with `--live` as a push target); say so in one line.

## 3. Baseline: Lighthouse full suite, Theme Inspector, real-visitor data

Save every report in the session's scratch folder (`<scratch>` below); `<skill>` is this skill's
own folder. `npx lighthouse` installs itself on first use.

### 3a. Lighthouse, full suite, on the live page (read-only; this is what visitors get)

Every run covers all four categories and saves both formats. Three runs per form factor, one after
another, nothing else heavy running on the computer; five when the speed spread is wider than 10
points. The HTML report is for the person to open; the JSON is for the numbers.

```bash
for i in 1 2 3; do
  npx lighthouse "<live url>" --output=json --output=html --output-path=<scratch>/home-mobile-$i \
    --chrome-flags="--headless=new" --quiet
  npx lighthouse "<live url>" --preset=desktop --output=json --output=html --output-path=<scratch>/home-desktop-$i \
    --chrome-flags="--headless=new" --quiet
done
node <skill>/scripts/lh_summary.mjs <scratch>/home-mobile-*.report.json > <scratch>/home-mobile.summary.json
node <skill>/scripts/lh_summary.mjs <scratch>/home-desktop-*.report.json > <scratch>/home-desktop.summary.json
```

(If a Lighthouse version writes `home-mobile-1.json` instead of `.report.json`, use that name.) The
summary gives median scores for all four categories, the speed spread, core speed metrics, the
main-content element, cost per outside company, and every failing audit with its elements.

A store with a password page can't be scored this way; say so, run on the local dev server instead,
and label every speed number "local, for before-and-after comparison only".

### 3b. Fix mode only: checking fixes on the working copy

Accessibility, best practices and SEO don't move between runs, so after edits one run per form
factor on the local dev server is enough (`shopify theme dev`, usually `http://127.0.0.1:9292`, not
the preview domain, which injects Shopify's preview-bar iframe):

```bash
npx lighthouse "<local url>" --output=json --output-path=<scratch>/lab-<handle>-mobile-1.json \
  --only-categories=accessibility,best-practices,seo --chrome-flags="--headless=new" --quiet
npx lighthouse "<local url>" --output=json --output-path=<scratch>/lab-<handle>-desktop-1.json \
  --only-categories=accessibility,best-practices,seo --preset=desktop --chrome-flags="--headless=new" --quiet
```

Speed after a fix is measured on the draft's preview address with several runs
(`references/performance.md` section 1b), never on the dev server.

### 3c. Theme Inspector: how long the theme's own code takes on the server

Shopify's Theme Inspector shows where the server spends time running the theme's Liquid code. The
command line version, `shopify theme profile`, needs the Shopify CLI signed in to the store with
theme access (setup check rows E and F). It only reads. Always name the theme by id, never rely on
the default. Follow `references/liquid-profile.md`: three profiles of the page, summarised with
`scripts/liquid_profile_summary.mjs`. If the CLI isn't signed in to the store, mark this lane "not
run" and say what is needed.

### 3d. Real-visitor data (live page, read-only)

`references/performance.md` section 1a.

## 4. Classify every finding

Each finding goes in exactly one bucket, with a reason, using its lane's guide:

- **Fix**: the theme owns it and a safe fix exists in the guide's table.
- **Skip, with evidence**: owned by an app, store content, Shopify, or outside the theme. Name the
  owner and, for speed, the measured cost.
- **Ask**: the only real fix changes something visible, touches a vendor file, or needs a store
  write.

## 5. Present the plan and WAIT for approval

Show a table: page, lane, finding, element or file, bucket (fix, skip or ask), exact edit (file,
before to after), and reason. List skipped items with their evidence and owner, largest speed cost
first. Make no edits until the person says go; these files render on live pages once published. If
the chosen theme is the live theme, stop: use or create a draft (`references/theme-target.md`).

## 6. Apply fixes, verify each on the page

Apply each approved edit in the working copy and read back the running page (attribute values,
computed colours, `loading` and `fetchpriority`, image sizes offered). After each edit, run Theme
Check and compare it with the baseline (`references/theme-check.md` section 3). For speed fixes,
run the visual and working-page proof in `references/performance.md` section 4.

## 7. Re-run and confirm

- Accessibility: repeat 3a. Every page and form factor must score `1.0`; if not, return to step 4
  for what remains. Then prove nothing moved (`references/accessibility.md` section 3).
- Best practices and SEO: repeat 3a. Every finding marked "fix" must be gone.
- Speed: the after numbers come from the draft's preview address, so they need the push in step 8.
  On the local dev server, only check that each fix is in place.
- Server speed: re-run the Theme Inspector (`references/liquid-profile.md`) on the draft after the push.
- Theme Check: `new_offenses` empty; `fixed_offenses` matches the plan.

## 8. Push, verify, re-check deployed (only after the person approves pushing)

1. Theme Check matches the plan against the baseline (no new offenses).
2. Re-read the chosen theme's role: if it is live, stop (never push to it) and use or create a draft.
   Then `shopify theme push --theme <chosen theme id> --only <exact touched files>`, never with
   `--allow-live`. Never a bare push: the branch may carry unrelated work in progress.
3. `shopify theme pull` the same files to a scratch folder and `diff` them: they must be
   byte-identical to local. That is the proof, not the CLI's "success" message.
4. Speed: repeat `references/performance.md` section 1b on the draft's preview address, same runs,
   and compare medians (section 5 there).
5. Accessibility, best practices and SEO on the deployed preview: say plainly that this is the
   Lighthouse command-line tool, not the Chrome extension. Expect lower scores than local (the
   preview bar, outside scripts). Don't reopen step 4 to chase the gap, but confirm every new finding
   lands in a skip bucket with evidence rather than assuming it's outside noise.

## 9. Report and log

Write the plain-language readout in chat and at the top of `THEME-AUDIT.md` as **Read this first**,
following `references/readout.md` (headline, scorecard, fix these first, quick wins, what isn't the
theme's to fix, what I couldn't check). Put the full record in the rest of `THEME-AUDIT.md`,
following `references/report-template.md`, and give the person the HTML reports' folder. Write "not
run" for anything not run. The readout is what the person reads; never paste the file.

## Checklist

- [ ] Setup check passed (or already passed this conversation); anything missing was explained and fixed step by step
- [ ] Mode stated (audit only, or audit and fix); in fix mode the theme settled once (remembered or asked), a draft, never the live theme
- [ ] Lanes in scope stated in one line
- [ ] Real, published, 200 URL for every page
- [ ] Theme Check baseline taken from a clean run
- [ ] Lighthouse full suite (every category in the report) on phone and desktop, 3 to 5 runs each, JSON and HTML saved; median and spread
- [ ] Theme Inspector profiled 3 times (or marked "not run" with the reason)
- [ ] Real-visitor data read (or "not enough data yet")
- [ ] Every finding classified fix, skip or ask, with a reason and an owner
- [ ] Plan approved before any edit
- [ ] No app, app embed or store content changed
- [ ] Every fix verified on the rendered page; speed fixes passed the visual and working-page proof
- [ ] Contrast verified on the live composited page
- [ ] Theme Check: no new offenses after every edit
- [ ] Accessibility 1.0 on every page, both form factors, locally
- [ ] Pushed only to the draft, with `--only` touched files; pulled and diffed identical
- [ ] Speed re-measured on the draft preview; changes inside the spread reported as "no measurable change"
- [ ] Deployed-domain gaps traced to confirmed non-theme causes
- [ ] Readout written in plain words (`references/readout.md`) in chat and at the top of `THEME-AUDIT.md`; QA log pointer added if the project keeps one
