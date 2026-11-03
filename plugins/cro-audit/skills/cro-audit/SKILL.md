---
name: cro-audit
description: "Conversion-rate audit for a Shopify page or store that needs no analytics or heatmap integration (no Clarity, GA or Shopify connector). Runs five evidence streams: an expert heuristic review of the live page (CTA hierarchy, value and price visibility, trust, form and booking friction), page speed and Core Web Vitals, a mobile pass at phone width, funnel math from numbers the person pastes or exports, and voice-of-customer from an existing REVIEW-MINING.md. Labels every finding by evidence type (heuristic, measured, reported, customer voice) so expert judgement is never passed off as behavioural data, ranks fixes by impact and effort, and lists the open questions that only behavioural data can answer. Read-only. Use for \"CRO audit\", \"why isn't this converting\", \"conversion review\", \"heuristic review\", \"what should we test\", \"audit the funnel\", \"is the site fast enough\", or when a store has no analytics yet and wants a first evidence base. Not for fixing the page (use page-edit-content or page-edit-design), a general page gap analysis (page-audit), tagging and consent (analytics-audit) or accessibility scoring (accessibility-audit)."
---

# CRO audit

Find what is most likely costing a page or store conversions, using only what can be observed
or measured today, with no tool connections. Read-only and brand-agnostic.

```
1. Intake -> 2. Heuristic review -> 3. Speed -> 4. Mobile pass ->
5. Funnel math (only from numbers given) -> 6. Customer voice (only if it exists) ->
7. Rank and write CRO-AUDIT.md -> 8. Hand off
```

## Who this is for

A store owner, marketer or Site Editor who wants to know what to fix first and what to test,
not a developer. Plain language, explain a term once, narrate before acting.

## Rules

- **Read-only.** Never edit a theme or store, and never enter data into the live site (no test
  bookings, no test orders, no form submits). The only file you write is `CRO-AUDIT.md`.
- **No integrations required.** Work from the public page, public tools and numbers the person
  gives you. Never ask the person to connect an analytics tool, and never type a password or
  token for them.
- **Label every finding by evidence type**, and never blur them:
  - `[Heuristic]` expert judgement against a named principle. Legitimate evidence, but not
    behavioural: say "this is a likely friction point", never "this loses X% of sales".
  - `[Measured]` a number you measured (speed, tap target size, field count, word count).
  - `[Reported]` a number the person supplied (funnel counts, conversion rate). Say where it
    came from and the date range; you did not verify it.
  - `[Customer voice]` quoted or counted from an existing `REVIEW-MINING.md`.
- **No invented numbers.** No benchmark, uplift percentage or "industry average" without a
  source and date you can name. Default to none. Never predict a lift.
- **Findings vs. test ideas.** A finding is observed. A test idea is a hypothesis; mark it as
  such and say what data would confirm it.
- **Small samples are small.** Flag any rate built on fewer than a few hundred sessions or
  fewer than about 30 conversions as directional only (`references/funnel-math.md`).
- **Hard limits win.** If the person says something must not change (price display, a
  required form field, a legal line), keep it out of the recommendations and say so.
- **Don't rule on claims.** Unsourced claims are reported as "no source on the page" and sent
  to the `fact-check` skill, not judged here.

## 1. Intake

Ask at most four questions, multiple choice where possible, always allowing "not sure". If
unanswered, state the assumption and continue.

1. **What is being audited?** A page URL (homepage, product, collection, landing, booking) or
   the whole store's main path.
2. **What counts as a conversion?** Purchase, booking or consultation request, lead form,
   email signup, other. This sets the one primary action every check is measured against.
3. **Who is the typical visitor and where do they come from?** (new or returning; search,
   social, email, ads, in person.) "Not sure" is fine.
4. **What evidence do you already have?** Numbers from Shopify Analytics or anywhere else
   (sessions, product views, add to cart, checkout, orders, or sessions to bookings), and
   whether a `REVIEW-MINING.md` exists. Say none is fine: skip streams 5 and 6.

Brand context: read `BRAND.md` if present (brand name, what is sold, claim limits) using
brand-capture's lookup order; if missing, continue and say claims can't be checked against
brand rules. If `CRO-AUDIT.md` already exists, read it first: this is a re-audit that updates
it (`references/report-template.md`).

## 2. Heuristic review

Load the real page at desktop (1440x900) and at 375x812 using whichever browser tool is
available (built-in browser first). Scroll slowly so lazy content loads; do not interact with
forms beyond looking. If no browser is available, work from the fetched HTML and say the
review is partial and which checks you could not do.

Run `references/heuristics-checklist.md` for the page's type. Record each failed or at-risk
check as a `[Heuristic]` finding naming the principle (Nielsen Norman heuristic, Baymard-style
checkout or form friction, or plain CRO practice) and quoting what you saw. Passed checks are
listed in one line, not padded out.

## 3. Page speed

Run `scripts/pagespeed.py <url>` for mobile and desktop (public PageSpeed Insights; the shared
no-key quota is often used up, so a free API key via `--key` or `PSI_API_KEY` makes it reliable). Record LCP, INP or TBT, CLS and the top
opportunities as `[Measured]`. If the script can't reach the API or the quota is used up, use the
Lighthouse CLI if installed, else say speed was not measured and give the person the PageSpeed
Insights link to read it themselves. Report lab and field (real-user) data
separately and say which is which; field data may be absent for low-traffic pages.

Name an owner for each fix (this theme, an installed app, images and media, store settings,
a third-party embed). Don't promise a conversion gain from a faster page.

## 4. Mobile pass

At 375 wide, check `references/mobile-checklist.md`: tap target size and spacing, text
truncation, horizontal scroll, carousel and gallery usability one-handed, sticky or hidden
primary CTA, popups and banners that cover content, form input types, and whether the primary
action is reachable without hunting. Record as `[Measured]` where you measured a size and
`[Heuristic]` otherwise.

## 5. Funnel math

Only when the person gave numbers. Run
`scripts/funnel.py --steps "Sessions=12000,Product views=5400,Add to cart=640,Checkout=310,Orders=140"`
(or `--csv file`), following `references/funnel-math.md`. It returns step conversion, drop-off
and the largest leak. Tag everything `[Reported]`, state the date range and source the person
gave, and apply the small-sample rule. A leak points to where to look, not why: pair it with
the heuristic findings for that step.

If the person has no numbers, say which three they can read off Shopify Analytics in a minute
(sessions, add to cart or booking starts, orders) and move on. Do not ask them to export
anything or connect anything.

## 6. Customer voice

If `REVIEW-MINING.md` exists, read its top pain points and praise themes and tie each to the
page element it speaks to. Tag `[Customer voice]` with the mention count it reports. If it
doesn't exist, mention once that the `review-miner` skill produces it from a review export;
do not run it from here.

## 7. Rank and write

Score each finding for impact (how many visitors it touches, how close to the conversion) and
effort (who can fix it and how fast), then rank with `references/report-template.md`. Write
`CRO-AUDIT.md` in the project root (or the folder the person names) and give a short readout:
the top five, one line each, with the evidence tag.

End with **Open questions for behavioural data**: what a session recording, scroll map or
funnel report would answer that this audit cannot (for example "do visitors reach the booking
form at all?"), so adding tools later has a purpose. These are questions, not findings.

## 8. Hand off

Offer to apply the rows they pick: copy, images and links go to `page-edit-content`, layout,
order and style to `page-edit-design`, new sections to `page-create`, claims to `fact-check`.
Do not apply them from this skill.
