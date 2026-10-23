---
name: page-content-studio
description: Create a new Shopify page (homepage section, landing page, campaign/service/region page) or update something that already exists on one -- copy, an image, a section's settings, a section's layout, or which sections appear and in what order -- all in one skill. Brand-agnostic, built for the Site Editor: the marketing/content/ops person who asks for page changes but isn't necessarily a developer. Use whenever the user says "update the homepage", "make a landing page for X", "change this section", "fix the copy on", "swap the image on", "move this section up/down", "build a page for X", "recreate this page from the live site", or points at a live/preview URL and describes something to change or build -- or asks what on a page should be improved, or says what they want a page to achieve. Not for blog posts (use shopify-blog-writer/shopify-blog-rewrite) and not for accessibility audits (use accessibility-audit).
---

# Page content studio

One skill for the whole page journey: figure out whether the request is a brand-new
page or a change to one that already exists, then carry it out -- without handing off
to a different skill partway through. Brand-agnostic; brand facts come from `BRAND.md`
and `BRAND-VOICE.md` (see Step 0), never invented and never hardcoded here.

```
0. Locate brand context -> 1. Understand the request in plain terms ->
1a. Guided goal questions (what is the page for?) ->
1b. (If they haven't decided what to change) Diagnose and recommend ->
2. Resolve the real target -> 3. Find or plan what controls it ->
4. Build or change it -> 5. Verify live -> 6. Push to draft, log, report
```

## Who this is for: the Site Editor

The person asking is usually a **Site Editor** -- someone on the client's marketing,
content, or operations side, responsible for how the live site looks and reads, but not
necessarily a developer. They describe what a *visitor* sees ("the homepage photo is
outdated," "we need a landing page for the new treatment," "move the pricing above the
FAQ"), not where it lives in the theme.

That changes how this skill is used, not just what it does:

- **Plain language by default.** Say "section" or "template" and explain it in one short
  clause the first time ("the hero -- the big banner at the top"). Don't drop into file
  paths or schema terms unless the Site Editor is clearly comfortable with them.
- **You translate the request into the technical target** (Steps 1-3) -- they describe
  what they see; you find or plan what controls it.
- **Narrate before acting**, in a sentence they'd understand ("I'll swap the homepage
  hero image and leave everything else as-is").
- **Flag trade-offs in plain terms.** "This section is also used on your contact page --
  changing it there too, or just here?" beats describing it as shared-section reuse.
- **Explain draft vs. live the first time it comes up**: "this updates the
  draft/preview first; nothing visitors see changes until you say go."

## Why this is one skill, not two

Creating a new page and updating an existing one share almost everything that matters --
reading the same brand and theme-engineering facts, reusing sections before building new
ones, verifying against the live render instead of the source, never pushing live without
sign-off. Splitting them into separate skills mostly duplicated that shared discipline
and left the genuinely hard part -- deciding which job a request actually is -- unowned by
either one. Step 2 below is what used to be a hand-off between two skills; here it's just
the fork in the road partway through a single pass.

## Step 0: Locate brand and theme context

Brand facts (name, spelling, voice, claim limits, inspirations) come from `BRAND.md` and
`BRAND-VOICE.md`, resolved with the lookup order in brand-capture's
`references/brand-context.md` (project root, user local environment, central brand
directory, then memory/connected knowledge). This skill depends on brand-capture, so:

- **Found:** note the file's path/tier and revision; this is the source for every brand
  fact used below. Never copy a brand name, color, claim, or proper noun into a plan from
  memory -- read it from the file each time.
- **Not found:** stop and offer to run brand-capture first (about 10-25 minutes, once per
  store) -- this skill shouldn't write brand-facing copy without it. An exception: a pure
  structural change with no new copy (reordering sections, a settings toggle) can proceed
  without BRAND.md if the Site Editor would rather not wait; say so plainly and flag that
  anything copy-related should wait for brand-capture to run.

Resolve each file separately, as brand-capture's lookup does, and handle a partial set
explicitly rather than treating it as all-or-nothing:

| `BRAND.md` | `BRAND-VOICE.md` | What to do |
|---|---|---|
| found | found | Normal path. |
| found | missing | Structure, settings and existing-copy edits proceed. For new or rewritten copy, use only the voice facts inside `BRAND.md`, say plainly that voice guidance is missing, and offer brand-capture to fill it. |
| missing | found | Treat as missing: voice without claim limits and naming rules is not enough for brand-facing copy. Offer brand-capture; the structural-change exception above still applies. |
| missing | missing | As "Not found" above. |

**Visual spec.** `BRAND.md`'s `design_doc` key points to `design.md` (lowercase, written by
brand-capture) -- the brand's palette, type, spacing, corners and component values. When
it exists, it is the source for every visual value in Step 3b and wins over BRAND.md on
visual values (BRAND.md still wins on names, voice and claims). Use values marked
`(from site)` as measured; treat `(inferred)` ones as unconfirmed and flag them rather than
building on them silently. If there is no `design.md`, fall back to the store repo's own
visual spec or the theme's settings, and say which one you used. Never invent a hex,
font, size or radius to fill a gap.

Separately, theme-engineering rules (where changes go, naming, file ownership, section
conventions, verification gates) live in that specific store's own repo -- usually
`AGENTS.md` or `CLAUDE.md` at its root, not in this marketplace repo. Read it fully, and
any workflow file it points to. If it's missing, ask the Site Editor's engineering contact
where the rules live, or proceed carefully and say plainly which gates you can't confirm
without it.

## Step 1: Understand the request in plain terms

Ask (short, plain-language, multiple-choice where possible) until these are answered --
the Site Editor is describing what they *see*, not where it lives:

- **What is the page for, and do they already know what to change?** Run Step 1a (guided
  goal questions) whenever the ask is open-ended or the goal isn't obvious. If they name
  a specific change with a clear purpose ("swap the hero photo for the new one"), ask
  only the one-line goal check in Step 1a and carry on. If they're unsure what to change,
  Step 1a leads into Step 1b -- don't wait for them to decide, and don't guess.
- **Which page, in their words?** A URL they can paste, or a description ("the
  homepage," "a new page for the Botox treatment"). You resolve this to an actual
  template -- don't assume `index` means the homepage; check.
- **New or existing?** If they're not sure, Step 2 settles it. Don't ask them to know the
  difference between a template and a section.
- **What should stay exactly the same?** Default assumption unless told otherwise:
  everything else on the page stays visually identical. If satisfying the request would
  touch something they didn't mention, stop and ask in plain terms ("doing this would
  also change X on your contact page -- okay?") rather than quietly widening it.
- **Is there a reference** (a live URL to match, inspiration, or existing brand pages to
  stay consistent with), or is this from scratch / described verbally?
- **How urgent is this?** (e.g., a live typo right now) -- still go through draft staging
  and verification even under time pressure; say so if asked to skip it, and explain the
  risk of skipping rather than just refusing.

## Step 1a: Guided goal questions -- ask what the page is for

Most "improve this page" requests are really "help this page do a job". Find the job
first, then recommend against it. Offer a few short multiple-choice questions (use the
interactive question tool when available; otherwise a numbered list they can answer with
a number). Plain language, one round at a time, no more than four questions per round.
Always allow "not sure" and "something else".

**Round 1 -- the page's job**

1. **What should this page mainly do for your visitors?**
   - Get people to book or enquire (appointments, consultations, quotes)
   - Sell products (add to cart, buy)
   - Promote an offer, launch or campaign
   - Build trust (reviews, credentials, results, who you are)
   - Inform or answer questions (education, SEO, support)
   - Fix something that looks broken, outdated or off-brand
   - Not sure yet
2. **Who is it mostly for?** New visitors from search or ads / returning customers /
   people on phones from social / not sure. Phone-first changes the advice: say so.
3. **How much change are you open to?** Small tweak to one part / refresh a few
   sections / rebuild the page. This sets the effort ceiling in Step 1b.
4. **What must not change?** Claims or regulated wording, tracked booking or checkout
   links, brand rules, anything the Site Editor lists. These become hard limits.

**Round 2 -- goal-specific follow-ups.** Ask the follow-up questions for the chosen goal,
then use the matching row's checks and typical recommendations as the starting evidence
list for Step 1b. Never present the "typical recommendations" as findings; they are
candidates to test against what is actually measured on this page.

| Goal | Follow-up questions | What to check first | Typical recommendations (candidates only) |
|---|---|---|---|
| Book or enquire | Which single action counts (form, call, booking link)? Is there a booking link that analytics already tracks? | Where the first booking action sits on mobile and desktop, number of clicks to book, whether the booking path matches the tracked one, form or link friction | Move one clear booking action into the first screen, repeat it after proof sections, shorten the path to book, remove competing off-site CTAs from the top |
| Sell products | Which products or collection matter most? Is the problem traffic, add-to-cart, or checkout? | Product and collection sections' position, price and review visibility, add-to-cart reachability on mobile, empty or sold-out items showing | Feature best sellers earlier, show ratings and prices on cards, add a clear shop path, reduce sections between hero and products |
| Promote an offer or launch | What is the offer, its dates and terms? Where should it lead? | Offer visible in the first screen, dates and terms present, link target works, urgency stated honestly | One lead banner with the offer, one clear destination, expiry date and terms, remove stale promos |
| Build trust | What proof exists (reviews, counts, credentials, before/after, press)? Which claims are allowed? | Review count and rating shown, quotes sourced, unsourced numbers, credentials visible, photo proof | Show rating plus count, attribute quotes, source or soften unsourced claims (offer content-fact-check), add real proof near the main action |
| Inform or answer questions | What questions do visitors ask? What should they do after reading? | Heading structure, answer-first copy, FAQ presence, internal links, page speed, search impressions if available | Answer-first intro, scannable headings, FAQ block, next-step link, fix heading levels |
| Fix what looks wrong | What exactly looks wrong, and on which device? Is there a reference of what right looks like? | Reproduce on the render at desktop and mobile, compare against `design.md`, check the section's settings before touching code | Settings-level fix first, then scoped CSS, only then section code; list anything else noticed as "flagged, not done" |
| Not sure yet | Ask Round 1 question 2, then offer the two nearest goals with a one-line example each | Run Step 1b's full measurement | Rank across all goals and show which goal each candidate serves |

**Using the answers**

- Write the answers back in two lines ("Goal: book consultations. Audience: phone users
  from search. Open to: refresh a few sections. Must not change: tracked booking links")
  and get a yes before measuring.
- In Step 1b, weigh impact by how close a candidate is to the **primary action** for the
  chosen goal, and tag each row **on-goal** or **off-goal**. Off-goal rows are listed
  last as "worth knowing", never ranked above on-goal ones.
- Hard limits from question 4 override every recommendation: if a candidate would break
  one, say so in the row instead of dropping it silently.
- If the answers conflict with the evidence (they say "sell products" but the page has no
  product section), say so plainly and ask which to follow.
- Keep the answers for the QA log (`goal:` line).

## Step 1b: Help them decide what to change (only when they haven't)

The Site Editor shouldn't have to know which part of a page to touch. When they haven't
decided, find the candidates yourself and recommend -- from evidence, never from taste.

1. Load the page (live render or `shopify theme dev`, desktop and mobile) and list its
   sections top to bottom in plain terms.
2. **Measure it.** Run what can be run, ask for what can't, and record every number with
   its source, date and device. Never estimate a number you could have measured.

   | Run it yourself (when available) | Ask the Site Editor to export or share |
   |---|---|
   | Page speed and accessibility score on mobile and desktop (PageSpeed / Lighthouse, accessibility-audit) | Conversion rate, bounce/exit rate and CTA clicks for this page, by device (Shopify analytics or GA4) -- the Shopify connector's analytics query can pull some of this directly |
   | Section inventory with each section's position and height on the live render | Scroll depth and per-section clicks (heatmap tool), session recordings |
   | Theme check count for the page's template | Search Console impressions, clicks and position for the page |
   | Baseline accessibility checks (one h1, alt text, contrast, tap targets) | Any on-site survey or support/ticket themes |
   | Copy and claims read against `BRAND.md` / `BRAND-VOICE.md` / `design.md` | |

   If a source is unavailable, say so in one line and carry on with the rest; a missing
   number lowers confidence, it doesn't block the diagnosis.
3. **Read the qualitative evidence:** `REVIEW-MINING.md` (what customers praise or struggle
   with), `COMPETITORS.md` (what competitors' equivalent pages show or say that this one
   doesn't), and a visitor walkthrough at desktop and mobile -- what the first screen
   says, whether there is one clear action, trust cues, friction.
4. **Pair them, then score.** A measured problem becomes a recommendation only when a
   qualitative reason explains it (for example, mobile conversion at half of desktop plus
   a CTA that sits below three screens of text). Score each candidate:

   | # | Part of the page | What could improve | Numbers (source) | Why (qualitative) | Impact | Effort | On-goal? | Also affects other pages? |
   |---|---|---|---|---|---|---|---|---|

   Impact is high/medium/low from traffic x drop-off at that part of the page; effort is
   S/M/L using the Step 3a change types (setting value is S, new section is L). Rank by
   impact over effort (impact weighted toward the Step 1a goal's primary action, rows
   tagged on-goal or off-goal), keep it to about five rows, and label each row **finding**
   (measured and explained) or **suggestion** (judgement, missing numbers or no
   explanation) -- never present a suggestion as a finding.
5. Ask which rows to do. Do nothing until they pick. Each picked row becomes a normal
   request and continues from Step 2, carrying its baseline number forward; unpicked rows
   go in the QA log's "flagged, not done".
6. **Close the loop.** For each picked row, name the number that should move and when to
   re-check it (typically two to four weeks of traffic). This skill can't prove impact on
   its own; say so, and suggest an A/B test where traffic allows.

Keep this advisory: Step 1b never edits anything, and never widens a pick into extra
changes.

## Step 2: Resolve the real target -- this decides the path

1. Confirm whether the page already exists: check the Page in Admin (or the `templates/`
   folder for a template-level question) rather than trusting the name used in chat.
2. **Exists -> this is an update.** Go to Step 3a.
3. **Doesn't exist -> this is a new build.** Go to Step 3b.
4. If "update the live page" is the ask, confirm it's actually published -- an unpublished
   page can look fine locally and still 404 for a visitor.
5. Resolve a real local URL to test against (`shopify theme dev`, not the
   password-protected preview domain -- that domain injects its own preview-bar UI and is
   noisier signal).
6. If nothing matches what the Site Editor described, say so and ask for the actual URL or
   name rather than guessing the closest match.

## Step 3a: Updating an existing page -- find what controls it

A request like "update the headline on the homepage" could live in: a section's schema
default, a section's setting (set per-page), a locale file, or -- if it's
merchant-authored content like a product description -- nowhere in the theme at all.

1. Find which section renders that part of the page (walk the template's section list,
   matching visually against the live/dev render -- don't guess from the name).
2. Check whether a setting already exists for what's being asked. Reusing an existing
   setting beats adding a new one; adding a new setting beats touching markup/logic.
3. If the content is rendered from outside the theme (product description, metafield,
   Admin-authored data), say so plainly in terms the Site Editor can act on -- "that text
   comes from the product page in Admin, not this page's design; here's where to edit
   it" -- rather than editing Liquid that won't change what they see.
4. Check whether the same visual change is needed elsewhere (a section reused across
   several pages) -- flag this before changing it, not after.
5. Classify the change and pick the narrowest safe technique:

   | Kind of change | Safe technique | Avoid |
   |---|---|---|
   | Content (text, image, link, price) | Edit the value in the page's setting, or point to the theme editor/Admin if it's something the Site Editor can self-serve going forward | Hardcoding the new value into markup where a setting should hold it |
   | Settings (existing toggle/variant) | Change the setting value | Editing the section file to "just handle it in code" when a setting already exists |
   | Section code (no setting covers it) | Add the new setting + minimal markup to use it; match the pattern a sibling section already uses | Inventing a new pattern when the theme already has one |
   | Structure (add/remove/reorder) | Edit the page's section list only | Deleting a section/block file another page still references |
   | Visible beyond what was asked | Stop, name the trade-off in plain terms, ask | Silently "improving" something nearby |

Then go to Step 4.

## Step 3b: Building a new page -- plan it from sections, reuse first

1. Confirm the page name and URL handle; check it doesn't already clash with an existing
   template.
2. If there's a reference (a live URL): capture desktop and mobile widths, scroll slowly
   so lazy content loads, list every section top to bottom including ones with no text,
   read computed values (container, padding, gaps, font, size, weight, colors, radius) --
   don't eyeball them. Capture hover/focus/disabled states of buttons and links. If no
   rendered view is possible, say plainly it's blocked and name what failed; don't guess.
3. No reference: take copy facts from BRAND.md/BRAND-VOICE.md and visual values from
   `design.md` (Step 0), falling back to the store repo's own visual spec, and go to the
   next step.
4. For each region of the page, choose in this order: (1) an existing section that already
   fits, (2) the same section with one small new setting, (3) a native base-theme
   section/block, (4) a new section -- only when the layout is genuinely different. One
   section per visual region; blocks are for repeated items inside one region, not a
   substitute for separate sections.
5. Show the Site Editor a plain-language table: region, what it'll use, why. Get a yes
   before building.
6. Build the template: add every section, list all ids in the right order. No hardcoded
   colors, fonts, or text a setting could hold. Check every number against the schema's
   min/max -- a bad value can reject the whole push. Leave image pickers blank if rights
   aren't confirmed; never link to a reference site's own CDN.
7. CSS only if the existing sections truly can't do it, following the store repo's
   cascade/scoping/breakpoint rules. A new font needs a licence check with the Site Editor
   first -- never swap in a lookalike silently.

Then go to Step 4.

## Step 4: Verify -- live, not from the diff

Reading the source you just wrote is not verification; loading the actual rendered page
is.

1. Load the page in `shopify theme dev`. For an update, compare against what it looked
   like before (screenshot or saved HTML from before starting). For a new page, check
   both the fresh build and, if there's a reference, side-by-side against it.
2. Confirm the thing asked for actually changed/exists on the rendered page -- not just
   that the source now says what was intended.
3. Confirm nothing *else* visibly moved. For an update: everything else should be
   identical in position/size. For a new page: the theme editor's add/remove/reorder/
   duplicate controls work, each setting changes something visible, empty fields and very
   long headings don't break layout.
4. Check every breakpoint and color scheme the change could plausibly reach -- don't
   assume it's fine elsewhere just because it's fine on the one page tested.
5. Run (or re-run) `theme check` -- a build should show no new offenses; an update's count
   from before must be unchanged. A changed count means something broke; find it before
   continuing.
6. Accessibility baseline either way: one h1, no skipped heading levels, icon-only buttons
   have names, images have alt text, keyboard-only pass, contrast checked per color
   scheme. This is a baseline check, not the dedicated audit -- for a full Lighthouse pass,
   use the accessibility-audit skill instead of expanding this one.

## Step 5: Push, verify, log

1. Push only to the unpublished/draft/preview theme, scoped to the exact touched files --
   never a bare push that could carry unrelated WIP. Never push to the live theme without
   the Site Editor's explicit go-ahead, confirmed in chat.
2. Pull the same files back to a scratch path and diff -- that's the actual proof the push
   landed, not the CLI's success message.
3. Re-check on the deployed preview domain. Expect small differences from local (the
   preview-bar UI, third-party scripts) -- that's expected noise, not a sign the fix is
   wrong, but confirm rather than assume it on every gap.
4. Log an entry (`references/qa-entry-format.md`, or the store repo's own QA log format if
   it names one): what was asked, what controlled or composed it, what changed, what was
   verified, measured parity against a reference if there was one, and anything the Site
   Editor still needs to do themselves (upload a different image, fill in copy, publish
   the page in Admin and pick the template).
5. Final summary to the Site Editor, short, plain terms: what changed/was built and where
   it's now visible, what was checked, anything flagged but not done and why, and whether
   it's only on draft/preview or already live.

## Never

Do not invent a brand fact that isn't in BRAND.md/BRAND-VOICE.md. Do not widen a
content/settings fix into a code change when an existing setting would do. Do not touch a
shared base-theme file or token without checking every usage it affects. Do not delete or
rename a section/block file another page still references. Do not claim a visual check
passed without having loaded the live rendered page. Do not push to the live theme without
the Site Editor's explicit, chat-confirmed go-ahead. Do not recreate a reference page from
a text-only fetch -- a capture missing computed values and images isn't a capture. Do not
call something "matches the reference" without a measured parity table.
