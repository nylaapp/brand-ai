---
name: page-audit
description: "Audit a Shopify page against what its page type should do, for any store: find where it falls short and rank what to fix, from evidence. Asks what the page is for (book, sell, promote, build trust, inform, fix), checks the rendered page at desktop and mobile against a graded playbook for its type (homepage, landing, collection, product, about, contact, FAQ, policy, location, service), measures what it can, names who owns each fix (this theme, store admin, store settings, a third-party app, an off-site page), and writes a ranked, client-ready report plus a living PAGE-AUDIT.md. Use for \"what should we improve on the homepage\", \"audit the about page\", \"where does this page fall short\", \"review this landing page\", \"is this page effective\", \"what is missing on this page\". Read-only: never edits a theme or store. Not for making a change or building a page (use page-content-studio), blog posts (shopify-blog-writer), a full accessibility audit (accessibility-audit) or analytics and tagging (analytics-audit)."
---

# Page audit

Find where a page falls short of what its type should do, and say what to do about it, from
what was actually observed. Read-only and brand-agnostic. Brand facts come from `BRAND.md`
and `BRAND-VOICE.md` (see `references/intake.md`), never invented.

```
1. Intake: brand/theme context, page and type, goal questions ->
2. Observe the rendered page -> 3. Gap analysis against the playbook ->
4. Measure -> 5. Qualitative evidence -> 6. Pair, score, name owners ->
7. Write PAGE-AUDIT.md and the readout -> 8. Hand off the rows they pick
```

## Who this is for

Usually a Site Editor on the client's marketing, content or operations side: responsible for
how the site looks and reads, not necessarily a developer. They describe what a visitor sees,
not where it lives in the theme. Use plain language, explain a term once ("the hero, the big
banner at the top"), narrate before acting, and flag trade-offs in plain terms ("this section
is also on your contact page").

## Rules

- **Read-only.** Never write to a theme or a store. You may pull theme files into a scratch
  folder, load pages and fetch public destinations. The only file you write is `PAGE-AUDIT.md`
  (and a readout the person asks for).
- **Never type a password, token or other credential** for the person, and don't enter test
  values into their live pages. If access is blocked, follow the blocked-access table in
  `references/observation-recipes.md`.
- **Evidence over taste.** Mark a playbook check failed only from what you observed. Say the
  grade when you cite a check: research is named as research with its source; grade B and H
  checks are "common practice" or "a rule of thumb", never research. Never quote a figure
  without its source and date.
- **Findings and suggestions are different.** A **finding** is observed and tied to an A-grade
  check or a measured number. Everything else is a **suggestion**.
- **Hard limits win.** What the person said must not change overrides every recommendation;
  say so in the row instead of dropping it.
- **Don't invent brand facts, claims or numbers.** Unsourced claims on a page are reported as
  "no source on the page", then sent to a fact-check, not ruled on.
- **No promises about results.** A page can pass every check and still underperform, and a
  failed check doesn't prove lost sales. Say so, and pair with analytics when available.

## 1. Intake

Follow `references/intake.md`: brand and theme context, which page and what type, and the
guided goal questions with the round-2 follow-ups. Echo the answers back in two lines. If
`PAGE-AUDIT.md` already exists (rules in `references/audit-file.md`), read it first: this is
a re-audit that updates it.

If the person doesn't answer, state the assumption you are using and continue.

## 2. Observe

Load the real page at desktop (1440x900) and mobile (375x812) following
`references/observation-recipes.md`: a real viewport, the theme id confirmed, a slow scroll for
lazy content, overlays noted at 1 s and about 15 s. List the sections top to bottom in plain
terms. A blocked page is not a failed page: mark those checks "Can't tell" and say what you
need.

## 3. Gap analysis against the playbook

Open `references/page-type-playbook.md`: the "Every page" checks plus the section for this
page type. Mark each check **Pass**, **Partial**, **Missing** or **Can't tell**, recording the
number, quote or position that supports it and the viewport. Missing and Partial are the
page's shortfalls; "Can't tell" never is. Apply only the checks that fit the business type.

## 4. Measure

Run what can be run, ask for what can't, and record each number with source, date and device.
Never estimate a number you could have measured. A missing source lowers confidence; it
doesn't block the audit.

| Run it yourself (when available) | Ask the person to export or share |
|---|---|
| Page speed and accessibility scores on mobile and desktop (PageSpeed or Lighthouse) | Conversion rate, bounce or exit rate and CTA clicks for this page, by device (Shopify analytics or GA4); the Shopify connector's analytics query can pull some directly if it is connected to this store |
| Section inventory with positions and heights | Scroll depth and per-section clicks (heatmap), session recordings |
| Theme check count for the page's template | Search Console impressions, clicks and position |
| Baseline accessibility (one h1, alt text, contrast, tap targets) | On-site survey or support themes |
| Copy and claims read against the brand files | |

## 5. Qualitative evidence

Read `REVIEW-MINING.md` (what customers praise or struggle with) and `COMPETITORS.md` if they
exist, and do a visitor walkthrough at both widths: what the first screen says, whether there
is one clear action, trust cues, friction.

## 6. Pair, score, name owners

A measured problem becomes a recommendation only when a qualitative reason explains it (for
example mobile conversion at half of desktop, plus a booking button below three screens of
text). A failed playbook check is that reason when its grade is A, and a weaker one when B or
H. Name the owner of each fix using the playbook's "Where each fix lives". A shortfall the
theme can't fix is still reported, tagged `handed-off`, with who acts and what to ask them.

Score each row: **impact** high, medium or low from closeness to the page's primary action and
how many visitors reach it ("unknown" with no traffic data); **effort** S, M or L as defined in
`references/audit-file.md`. Rank by impact over effort, weighted toward the goal's primary
action, tagged **on-goal** or **off-goal** (off-goal last). Keep about five rows and list the
rest as "also noticed".

## 7. Write the file and the readout

1. Create or update `PAGE-AUDIT.md` following `references/audit-file.md` and
   `references/audit-template.md`: brief, observation log, gap report, recommendations with
   stable IDs and `open` status, hand-offs, questions, changelog.
2. Give the readout in the order set in `references/audit-template.md`: assumptions, counts,
   the top rows, what couldn't be observed, a recommendation, and where the file is.

## 8. Hand off

Ask which rows to act on. Do nothing until they pick. Set picked rows to `picked`, parked
ones to `parked`. For each picked row, name the number that should move and when to re-check
it (typically two to four weeks of traffic), say this audit can't prove impact on its own, and
suggest an A/B test where traffic allows.

Then point to the next skill:

| Picked row | Next |
|---|---|
| A change on this theme (reorder, setting, section, copy) | `page-content-studio`, which reads the row from `PAGE-AUDIT.md` |
| Brand files missing, or copy needs brand approval | `brand-capture` |
| Unsourced, numeric or regulated claims | `content-fact-check` |
| Accessibility depth beyond the baseline | `accessibility-audit` |
| Tracking, consent or tagging problems | `analytics-audit` |
| Store settings, an app, or an off-site page | The owner named in the row; give them the observation and what to change |

## Checklist before finishing

- [ ] Goal, audience, change appetite and limits recorded, with assumptions marked
- [ ] Theme id confirmed and viewports noted; blocked checks marked "Can't tell"
- [ ] Every shortfall has an observation behind it; no check failed from guesswork
- [ ] Grades stated; no grade B or H item presented as research; figures have source and date
- [ ] Rows have owners; theme-owned rows are separated from handed-off ones
- [ ] `PAGE-AUDIT.md` created or updated, IDs stable, no secrets in it
- [ ] Nothing was written to a theme or store; no credential was typed
- [ ] The readout says what wasn't observed and what the person should decide
