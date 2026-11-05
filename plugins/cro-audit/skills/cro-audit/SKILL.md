---
name: cro-audit
description: "Conversion-rate (CRO) audit for a Shopify page or store, run as a quick first pass or as the full research suite CRO agencies use, with no analytics or heatmap integration required. Streams: technical and speed, expert heuristic review, competitive review, web analytics analysis (read-only Shopify Analytics through the Shopify CLI when it is authorised, otherwise numbers the person supplies, with a data-validity check and segment cuts), behavioural review of heatmaps and session recordings the person supplies, voice of customer (reviews, support text, surveys) and user testing (it writes the survey questions and test scripts and analyses the results; it does not collect them). Labels every finding by evidence type and confidence, sorts each issue into a bucket (just do it, instrument, investigate, test, hypothesize), scores with ICE or PIE, and plans the experiments with hypotheses, metrics, sample size and duration, plus an A/B result checker with a sample-ratio check. Strictly read-only: it never changes a store's settings, setup, theme, content or apps, even when its access would allow it. Use for \"CRO audit\", \"conversion audit\", \"full CRO audit\", \"why isn't this converting\", \"heuristic review\", \"what should we test\", \"analyse our funnel\", \"plan an A/B test\", \"how many visitors do we need for a test\", \"read these A/B results\", or \"is the site fast enough\". Not for fixing the page (use page-edit-content, page-edit-design or page-create), a general page gap analysis (page-audit), tagging and consent (analytics-audit) or accessibility scoring (accessibility-audit)."
---

# CRO audit

Find what is most likely costing a page or store conversions, say how sure we are, and turn it into a
ranked plan: fixes to make now, tracking to add, things to investigate, and experiments worth running.
Read-only and brand-agnostic. Works with no tool connections; behavioural data is supplied by the
person when they have it.

```
1. Intake and mode -> 2. Technical -> 3. Heuristic + competitive ->
4. Analytics (supplied) -> 5. Behavioural (supplied) -> 6. Voice of customer + surveys ->
7. User testing -> 8. Synthesis, prioritise, plan experiments -> 9. Write CRO-AUDIT.md -> 10. Hand off
```

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

## Who this is for

A store owner, marketer or Site Editor who wants to know what to fix first and what to test, not a
developer. Plain language, explain a term once, narrate before acting.

## Two modes

- **Quick audit** (about an hour): stages 1, 2, 3 and 8 to 10, plus 4 and 6 only for numbers and
  files the person already has. Needs nothing from the person. Gives likely friction and measured
  problems, a ranked list, and the questions behavioural data would answer.
- **Full audit** (the research suite): every stage. Stages 4 to 7 need data or sessions the person
  provides; the skill tells them exactly what to bring (`references/research-suite.md`). A stream
  with no data yet is written up as "prepared, awaiting data" with its instrument attached, not
  skipped silently.

Ask which mode in the intake. If unsure, run the quick audit and offer the full one.

## Rules

- **Store access is read-only, always.** Whatever access you have (the Shopify CLI, a connector, the
  admin, a signed-in browser), only read and pull data. Never create, change or delete anything on the
  store: no settings, themes, content, products, files, apps, discounts, tags, pixels or permissions,
  even when the access scope would allow it (a `write_*` scope is never used). With the Shopify CLI run
  queries only, through `scripts/shopifyql.py`, and never pass `--allow-mutations`. Never run
  `shopify store auth` or change what a connection may do: granting access is the person's step.
- **Don't act as a visitor who changes anything.** No test bookings, orders, sign-ups or form submits.
  Don't accept or decline the cookie banner. A popup may be closed with its own close button to see the
  page behind it; nothing else on the page is clicked except links being followed to read them.
- **The only files you write** are `CRO-AUDIT.md` and, if asked, instruments (survey questions, test
  scripts) beside it.
- **No integrations required.** Work from the public page, public tools, read-only access the person
  already set up (such as an authorised Shopify CLI) and what the person gives you. Never ask them to
  connect a new tool, and never type a password or token for them. Behavioural
  tools (a heatmap, recordings, a survey tool) are places the person may already have data, never a
  requirement.
- **Label every finding by evidence type**, and never blur them:
  - `[Heuristic]` expert judgement against a named principle; fast, but not behavioural. Say "likely
    friction", never "loses X% of sales".
  - `[Measured]` a number you measured (speed, tap size, field count, request weight).
  - `[Reported]` an analytics number: supplied by the person, or pulled read-only from the store's own
    analytics (Shopify via the CLI). Give the source, the query window and the validity checks it passed.
  - `[Behavioural]` what visitors did, from heatmaps, scroll maps or recordings the person supplied.
    Give the sample ("9 of 24 mobile recordings").
  - `[Customer voice]` text customers wrote already (reviews, tickets), counted.
  - `[Survey]` answers to questions asked for this audit.
  - `[Test]` what participants did in user testing; give how many people.
- **Confidence on every finding** (`references/prioritization.md` section 3): High when two or more
  different kinds of evidence agree, Medium for one strong source, Low for a single opinion.
- **Triangulate.** Analytics find where; behavioural, voice and test evidence find why. Never explain
  a leak from analytics alone, and never present a heuristic finding as data about visitors.
- **No invented numbers.** No benchmark, uplift or "industry average" without a source and date you can
  name. Never predict a lift. Check scripts' results; don't round a verdict up.
- **Small samples are leads.** Apply `references/funnel-math.md` to every rate, and treat recordings,
  surveys and tests as explanations, not rates.
- **Findings vs. test ideas.** A finding is observed. A test idea is a hypothesis; mark it and say what
  would confirm it.
- **Honest about what you can't do.** You can't recruit participants, send surveys, or run an
  experiment. Say so, prepare the instrument and analyse what comes back.
- **Hard limits win.** If the person says something must not change (price display, a required field,
  a legal line), keep it out of the recommendations and say so.
- **Don't rule on claims.** Unsourced claims are reported as "no source on the page" and sent to the
  `fact-check` skill.
- **Run it well.** This is judgement-heavy work: use the strongest model available and high effort for
  the audit and synthesis. Cheaper settings are fine for re-running a script or one check.

## 1. Intake and mode

Ask at most four questions per round, multiple choice where possible, always allowing "not sure". If
unanswered, state the assumption and continue.

1. **Mode:** quick or full.
2. **What is being audited?** A page URL (homepage, product, collection, landing, booking) or the main
   path of the store.
3. **What counts as a conversion, and which is the one primary action?** (purchase, booking or
   consultation request, lead, signup.) Plus the **segments that matter** (mobile vs desktop,
   new vs returning, paid vs organic, location), if known.
4. **What evidence exists?** Analytics numbers or exports, whether the Shopify CLI is authorised for
   the store (check it yourself with `scripts/shopifyql.py --store <shop>.myshopify.com --check`),
   heatmaps or recordings, reviews or a `REVIEW-MINING.md`, support text, past A/B tests, and where the
   conversion happens (on the store, or on another system such as a booking site). "None" is fine.

Also gather: what has already been changed or tested (so you don't re-recommend it), the platform and
installed apps, and any promotion running. Brand context: read `BRAND.md` if present (brand name,
what is sold, claim limits) using brand-capture's lookup order; if missing, continue and say claims
can't be checked against brand rules. If `CRO-AUDIT.md` exists, read it first: this is a re-audit that
updates it (`references/report-template.md`).

## 2. Technical

Load the real page at desktop (1440x900), at 1024 wide, and at 375x812 in the built-in browser (or
whichever tool is available). If no browser is available, work from fetched HTML and say the review is
partial.

- **Confirm which theme you are looking at.** A browser that has previewed a draft keeps showing it.
  Read `Shopify.theme.id` and `Shopify.theme.role` on the page; if the role isn't `main` and the person
  didn't ask for a draft, load `?preview_theme_id=<live theme id>` (or use a fresh browser profile) and
  check again. Say which theme was audited.
- **Scroll like a visitor.** Use real wheel or touch scrolling. Many themes override scripted scrolling
  (`window.scrollTo`), so a page that "won't scroll" from a script may scroll fine for people. Never
  conclude a scroll lock from scripted scrolling; measure `overflow` on `body` and `html` instead.
- **Overlays.** Record when each popup and banner appears (time after load), what it covers and its
  close-button size, then close a popup with its own close button to see the page. Leave the cookie
  banner unanswered. A popup you closed won't come back in the same browser, so measure first-visit
  behaviour on the first load of each device.
- **Follow the conversion path read-only.** Click through each step of the main action (for example
  Book, then choose a region, then a location) to count the steps and spot dead or looping links. Stop
  at the first page of an off-site system (a booking or checkout site) and don't enter anything.

- **Speed**: `scripts/pagespeed.py <url>` (a free key via `--key` or `PSI_API_KEY` avoids the shared
  quota). If it fails, run the Lighthouse CLI (`npx lighthouse`), else say speed was not measured.
  Record LCP, TBT or INP, CLS, page weight and the biggest items, lab and field separately. Name an
  owner for each fix. Lab and field numbers differ; a huge LCP caused by one heavy asset is likely
  inflated by the lab throttle, so say so.
- **Mobile pass**: `references/mobile-checklist.md`.
- **Console errors, broken links, missing images, layout that differs by browser or device**, if the
  tool reads them.
- **Which theme**: confirm the page is the live theme (read `Shopify.theme.id` and role) unless the
  person named a draft; say which was audited.

## 3. Heuristic and competitive review

- **Heuristics**: `references/heuristics-checklist.md` for the page type. Record each failed or at-risk
  check as `[Heuristic]` naming the principle and quoting what you saw. List passed checks in one line.
- **Competitive** (full mode, or quick if `COMPETITORS.md` exists): `references/competitor-benchmark.md`.

## 4. Web analytics (supplied numbers)

Follow `references/analytics-analysis.md`.

1. **Shopify CLI first, read-only.** Run `scripts/shopifyql.py --store <shop>.myshopify.com --check`.
   If it reports "Analytics: ready", pull the data with `--preset all --since <start> --until <end>`.
   If `read_reports` (or `read_orders`) is missing, or the CLI isn't authorised, stop there: tell the
   person what's missing and give them the `shopify store auth` command to run themselves if they want to
   grant it, or ask for the CSV exports instead. Never run that command for them.
2. **Validate before reading** (section 1 of the reference): look for step changes in sessions per day
   (a storefront switch or tracking break) and use only the clean window; reconcile orders by sales
   channel with completed checkouts (subscriptions, other storefronts, draft orders and POS aren't
   website conversions); drop bot rows (no device type, near-100% bounce); flag internal traffic; and
   say whether the main conversion even happens on the store.
3. **Read by segment:** the funnel by device with `scripts/funnel.py` (use `--csv` output), entry pages,
   sources by device, social networks and their entry pages, the homepage by device and source.

Tag everything `[Reported]` with the window and source. If there are no numbers at all, name the three
the person can read off their analytics in a minute (sessions, add-to-cart or booking starts, orders)
and move on. If a number can't be trusted, say so and route the question to `analytics-audit`.

## 5. Behavioural (supplied)

Follow `references/behavioral-review.md` for heatmaps, scroll maps and recordings the person brings
or notes they take from a short viewing plan you write. Tag `[Behavioural]` with sample counts. No data
yet: prepare the viewing plan and mark the stream "prepared, awaiting data".

## 6. Voice of customer and surveys

Follow `references/survey-playbook.md`. First use existing text: `REVIEW-MINING.md` (from the
`review-miner` skill), support tickets, chats, reviews. Then write the survey questions the audit still
needs and say how many answers to wait for. Tag `[Customer voice]` or `[Survey]`.

## 7. User testing

Follow `references/user-testing-playbook.md`: write the tasks and script from the conversion goal,
say who to recruit and how many, and analyse the notes or recordings the person brings with the
severity scale. Tag `[Test]`. No sessions yet: attach the script and mark "prepared, awaiting data".

## 8. Synthesis, prioritise, plan experiments

1. Merge the streams into one issue list. For each issue note every kind of evidence behind it.
2. Rate confidence and assign a bucket (`references/prioritization.md`): Just do it, Instrument,
   Investigate, Test or Hypothesize.
3. Score with `scripts/prioritize.py ideas.json --evidence-confidence` (write the JSON from the issue
   list) and rank. Present the list by bucket first, then score: a measured defect is a Just do it item
   whatever its score.
4. For each Test item write the experiment (`references/experiment-design.md`): hypothesis naming its
   evidence, primary and guardrail metrics, sample size and duration from `scripts/sample_size.py`, and
   feasibility at the page's traffic. If it can't be tested, say what to do instead.
5. If the person supplies results of a finished test, check them with `scripts/ab_result.py`, report
   the interval, and flag a failed split check as invalid.

## 9. Write CRO-AUDIT.md

Use `references/report-template.md` for the file. Then write the chat message with
`references/chat-readout.md`: a plain-language readout in a fixed order (headline, what I looked at,
what changed, a five-row "Fix these first" table, quick wins, what's worth testing, what the numbers
say, what I couldn't check, then the link and one next-step question). The file keeps the analyst
detail (evidence tags, buckets, scores); the chat translates it into plain words using the glossary in
that reference. Put the same readout at the top of the file as **Read this first**.

## 10. Hand off

Offer to apply the "Just do it" rows the person picks: copy, images and links go to
`page-edit-content`, layout, order and style to `page-edit-design`, new sections to `page-create`,
tracking to `analytics-setup`, claims to `fact-check`. Do not apply them from this skill. Theme changes
always go to a draft theme (those skills never edit the live theme).

## Files

| File | Use |
|---|---|
| `references/research-suite.md` | The streams, how they combine, what stays human |
| `references/heuristics-checklist.md`, `references/mobile-checklist.md` | Streams 1 and 2 |
| `references/competitor-benchmark.md` | Stream 3 |
| `references/analytics-analysis.md`, `references/funnel-math.md` | Stream 4 |
| `references/behavioral-review.md` | Stream 5 |
| `references/survey-playbook.md` | Stream 6 |
| `references/user-testing-playbook.md` | Stream 7 |
| `references/prioritization.md`, `references/experiment-design.md` | Stream 8 |
| `references/report-template.md` | The file you write |
| `references/chat-readout.md` | The chat message: layout, writing rules, glossary, example |
| `scripts/shopifyql.py` | Read-only Shopify Analytics through the Shopify CLI (access check, presets, refuses writes) |
| `scripts/pagespeed.py`, `funnel.py`, `sample_size.py`, `ab_result.py`, `prioritize.py` | Measurement and maths (stdlib only) |
