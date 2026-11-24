---
name: page-create
description: >-
  Create something new on a Shopify theme: a new page (landing page, campaign page, service or
  treatment page, region or location page), a new section added to an existing page, or a new
  section type built to the theme's own rules. Starts from a short brief (goal, traffic source,
  offer, the reader's doubts, proof), researches the brand's inspiration brands, its competitors and
  the current design trends of notable brands in similar industries (what works, what doesn't, what
  is a fad), scores two or three page options for conversion, brand fit, UX, speed and build cost,
  and recommends the best. Plans it from what its page type needs (the playbook's must-haves, primary
  action in the first screen), takes each section from the theme's existing pool first and
  recommends a new section only when a proven pattern needs one, shows a plain-language plan for a
  yes, then builds it (in a local working
  copy with the Shopify CLI, or, without the CLI, directly on the staging theme through the Shopify
  connector when it can change themes), verifies it on the rendered page including the theme
  editor's controls, and sends only the new and touched files to the theme the person chose (always
  the staging theme, never the live theme). Can recreate a page from a live reference URL by capturing
  measured values, never from a text-only fetch.
  Brand-agnostic, written for the Site Editor. Use for "build a page for X", "make a landing page
  for the new treatment", "create a region page", "add a testimonials section to the homepage",
  "build a new section for team members", "recreate this page from the live site". Not for changing
  words, images or links on something that exists (use page-edit-content), changing layout or style
  of something that exists (page-edit-design), open-ended "improve this page" (page-audit), blog
  posts (blog-generator) or accessibility, speed and theme-code audits (theme-audit).
---

# Page create

Make something **new**: a page, a section on a page, or a new kind of section. It is planned from
what that kind of page needs, built from existing pieces first, and made in a local working copy.
The skill proves the result on the rendered page and puts only the new and touched files on the
store's staging theme (never the live theme). The live theme is never edited: work goes to the staging theme, created as "<live theme name> staging" if there isn't one.

It works one of two ways, chosen by the setup check: with the Shopify CLI and a local working copy
(the default), or, when the CLI isn't installed and the Shopify connector can change themes, through
that connector (`../page-studio/references/connector-route.md`). The rules and the safety are the
same; the steps below say where the connector route differs.

```
0. Setup check -> 1. Context -> 2. Understand what is being created -> 2b. Brief ->
3. Reference or research -> 4. Options and plan (approval) -> 5. Capture the baseline ->
6. Build in the working copy -> 7. Verify, then look, score, fix once -> 8. Ship to the theme -> 9. Hand back
```

`references/page-quality.md` holds the brief, the research and trend scan, the option scoring, where each section
comes from, and the conversion, UX and visual rules every new page is scored against. Read it at step 2b.

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

## Ground rules (every run)

These come before every step below. The full text is `references/ground-rules.md`; where it and a step below disagree, the
stricter rule wins.

- **Brand files first (required: BRAND.md, BRAND-VOICE.md and design.md).** Read them before any work and follow them: words follow
  BRAND-VOICE.md and stay inside BRAND.md's claim limits; visuals use design.md's values. If one is missing or
  belongs to another store, stop and ask once: create it now (brand-capture, voice-builder or styles-builder,
  `references/ground-rules.md` section 1) or tell me where it is. Never work from memory or the live site instead, and
  never carry on without it. With no person present, stop and report what is missing.
- **Staging only.** Every change goes to the store's staging theme (an unpublished theme whose name contains
  "staging"), and to the `staging` branch when the theme is in a git repository. If none is remembered, settle
  it before the first change, offering to create "<live theme name> staging" (`../page-studio/references/theme-target.md` sections 3
  and 4). Never edit, push to or commit for the live theme.
- **Live only when the person asks.** Never suggest, offer or schedule publishing. Only when the person asks in
  their own words in this chat, run the go-live gate (`references/ground-rules.md` section 3; `../page-studio/references/theme-target.md` section 7):
  checks first, then two confirmations, the second typed. End every change with the preview link and "Your live
  store has not changed."

## Rules

- **Desktop and mobile, always.** Every check of how something looks (a page, section, draft, style or screenshot) is done at both desktop (1440x900) and mobile (375x812), never one alone. Name the viewport beside each visual result. If one can't be loaded, mark that check "Can't tell" and say so; never assume one view from the other.
- **Working copy first, on the staging theme.** Never push from the working copy except
  through the ship step (connector route: no copy of the whole theme; build in `work/` and write
  nothing except through the ship step). The staging theme is settled once and remembered (`theme-target.md` sections 3 and 5); it is always an unpublished theme, never the live theme (if there is none, `theme-target.md` section 3 offers to create one) (`theme-target.md`, `ship-to-draft.md`).
- **The connector route changes the order, not the rules.** With no Shopify CLI, nothing can be
  rendered before the files are written, so the rendered checks run on the private staging theme right after
  the write (the live theme is never touched), and `theme check` can't run. Say both in the plan and
  get the person's agreement once. The calls and guards are in
  `../page-studio/references/connector-route.md`.
- **Reuse first, build when it pays.** For every region choose, in order: an existing section that fits; the same
  section with one small new setting; a native base-theme section or block; a new section when the layout is
  genuinely different, or when the research shows a pattern that works and no existing section can produce it
  (`references/page-quality.md` section 4). Say in the plan which one each region uses and why. One section per
  visual region; blocks are for repeated items inside a region.
- **Built to convert, not only to exist.** Every new page meets the conversion, UX and visual rules in
  `references/page-quality.md` sections 5 to 7 and is scored against them before it ships.
- **Get a yes on the plan before building.**
- **No hardcoded colours, fonts or text** that a setting could hold. Check every number against the
  schema's min and max, since a bad value can reject the whole push.
- **Leave image pickers blank** if rights aren't confirmed, and never link to a reference site's own
  CDN. A new font needs a licence check with the person first; never swap in a lookalike silently.
- **Don't invent brand facts or claims.** Copy comes from the brand files or the person; with neither,
  wait for brand-capture. Placeholder text must be obviously a placeholder, such as "[Clinician name]".
- **Never recreate a reference page from a text-only fetch.** A capture without computed values and
  images isn't a capture. Don't say "matches the reference" without a measured parity table.
- **Recreating a reference: its layout, the brand's design.** Unless the person says otherwise, follow
  "Recreating a page from a reference" in step 3: copy the reference's structure and layout, build a new
  section when no existing one nearly matches, and take every visual value from `design.md` and the
  theme settings already established. Where the reference conflicts with the brand guidelines (spacing,
  sizes, radius, type, colour), the brand guidelines win.
- **Never delete or rename** an existing section or block file, and never edit a shared base-theme file
  without checking every usage.
- **Never type a password or credential** for the person.
- **Hard limits win.** What the person said must not change overrides the request.

## Who this is for

A Site Editor on the marketing, content or operations side. Plain language, explain a term once,
narrate before acting, flag trade-offs in plain terms, and explain staging versus live the first time
it comes up: on the staging theme, nothing visitors see changes, and nothing goes live unless the person asks for it; these skills never edit the live theme, because edits there show to visitors at once.

## 0. Setup check

Before anything else, run `../page-studio/references/setup-check.md` for this skill's column: a
browser, the page address, brand files, a way to reach the theme (Node.js and the Shopify CLI signed
in to the store, or, when the CLI isn't ready, the Shopify connector with permission to change
themes: the check picks the route, and the CLI wins when both are ready) and a folder for the work
files. Assume the person isn't technical: check silently yourself, then walk
them through anything missing one step at a time, in plain words, and re-check after each step.
Skip it if it already passed in this conversation (for example, `page-studio` ran it before handing
off). Nothing else starts until the required items pass.

## 1. Context

**Theme first.** Before anything else, settle which theme this runs on, with
`../page-studio/references/theme-target.md`: use the theme already chosen in this
conversation or remembered in `THEME-TARGET.md` and say so in one line, or settle one with that file's section 3 (an existing staging theme, or a new "<live theme name> staging"; never the live theme) and remember it for every other skill. When the theme is in a git repository, settle the `staging` branch too (section 4). Don't ask again unless the
person names a different theme. If the person names the live theme, that file applies: it is refused and the staging theme is used.

Follow section 1 of `../page-audit/references/intake.md`: resolve the brand files and `design.md`,
handle a partial set, and read the store repo's own rules (`AGENTS.md` or `CLAUDE.md`), including how
sections and blocks are named, structured, scoped and registered. If a required brand file is
missing, stop and ask once (create it now, or tell me where it is; `references/ground-rules.md`
section 1); nothing is planned without it. Visual values come from `design.md` and the theme settings
set from it; never invent a hex, font, size or radius.

## 2. Understand what is being created

- **A new page, a section on an existing page, or a new section type?** Each follows the same flow; the
  plan and the checks differ.
- **Name and URL handle** (for a page); check it doesn't clash with an existing template or page.
- **What type of page is it and what is it for?** Use `../page-audit/references/intake.md` sections 2 and
  3 (page type, business type, the goal and who it is for, limits).
- **Is there a reference** to match (a live URL, inspiration, existing brand pages), or is it from
  scratch?
- **Which theme?** Settled in step 1; record its id and role. Get a working copy (pull the theme first,
  per the store repo's workflow, so admin-side edits aren't lost). Connector route: no whole-theme
  pull; read only the files this work touches or copies from, through the connector
  (`connector-route.md` sections 2 and 4). With no local store repo its rules aren't available:
  copy the closest sibling section and say which gates you can't confirm.

**From an audit.** If the request is a row ID or points at a `PAGE-AUDIT.md` (rules in
`../page-audit/references/audit-file.md`), read the rows marked `picked` that call for something new and
are owned by this theme. Work only on those and carry each row's baseline number.

## 2b. Brief

For a new page, settle the brief in `references/page-quality.md` section 1: the goal, the traffic source and its
promise, the offer, the reader and their doubts (from BRAND-VOICE.md's Who we're talking to), and the proof the page
can show. Take each one from the brand files and the request first, and ask only what is missing, one question at a
time. For a single new section, the goal and the reader are enough. The brief decides what the research looks for
and what the page is scored on.

## 3. Reference or research

**With a reference URL:** capture desktop and mobile widths, scrolling slowly so lazy content loads;
list every section top to bottom including ones with no text; read computed values (container, padding,
gaps, font, size, weight, colours, radius) rather than eyeballing them; and capture hover, focus and
disabled states of buttons and links. If no rendered view is possible, say plainly it's blocked and name
what failed; don't guess.

**Recreating a page from a reference.** These rules apply unless the person gives other instructions
for this page; when they do, theirs win and the plan says which rule they replaced.

1. **Copy the layout, not the look.** Match the reference's structure: the order and number of bands,
   what each band holds, columns and card count, which side media sits on, what is centred, and what
   slides or stacks. Never copy its words, images, logo or typefaces.
2. **Existing section first, new section when needed.** Use an existing section (or the same section
   with one new setting) when it nearly matches the band's layout. When none nearly matches (a
   different arrangement, a component the theme lacks, a card with parts no block can produce), plan a
   new section following "If a new section type is needed" in step 4. Don't force a band into a
   section that changes its layout.
3. **Always the brand's design system.** Every colour, font, type size, spacing, radius, border,
   shadow and state comes from `design.md` and the theme settings already set from it (styles-builder),
   including its `(proposed)` values. The reference's own values are measured only to understand the
   layout and to explain the differences.
4. **The brand guidelines win every conflict.** Where the reference's spacing, sizes, radius, type,
   colours or proportions differ from the brand guidelines, use the brand's value: for example the
   brand's section padding instead of the reference's gaps, the brand's H2 instead of the reference's
   heading size, the brand's pill buttons instead of square ones. Record each one in the parity table as
   an intended difference with the brand rule it follows, so it isn't counted as a mismatch.

**Without one (no Figma file, mockup or link): research first, always.** Don't design from
the playbook alone. The full method is `references/page-quality.md` section 2; in short:

1. **Choose five to eight live pages:** at least two inspiration brands (BRAND.md → Inspiration brands and
   BRAND-VOICE.md → Tone references), at least one competitor (`COMPETITORS.md` or BRAND.md → Competitors),
   and two or three **trend leaders**: notable brands in the same or a neighbouring industry, praised now
   for their design, preferably redesigned in the last 18 months. Prefer pages that do the same job as this
   page. Record each URL and the date you looked.
2. **Read each at desktop and mobile** with `site-reader` first (the browser only for what it can't do, after
   checking the window really resized), scrolling so lazy content loads
   (the capture rules above apply). If a page can't be rendered, say so and pick another. Never describe a
   page from memory or a snippet.
3. **Study three lenses** and write them down: *content* (what the first screen says, how offer, proof and
   objections are ordered, how things are named and priced, button labels, length); *layout* (section
   order and count, hero type, how backgrounds alternate, grid columns, density, the mobile first screen);
   *design system and branding* (their fonts, palette, spacing, corners, buttons and imagery, read to
   understand why the page feels as it does), then the store's own `design.md` and theme settings, noting
   where they agree or differ. For each page also note **what works and what doesn't** (clarity, proof,
   speed, mobile), and across all of them which repeated patterns are **durable trends** and which are
   **fads** (`page-quality.md` sections 2.2 and 2.3). Borrow durable ones only.
4. **Decide and record.** Put a Reference study table (brand, URL, date, source type, what we borrow, what
   we leave and why), a one-line design basis and the durable trends used in the plan. The "Recreating a page from a reference" rules above then apply to
   what you borrow: structure and patterns yes, words, images, logos and typefaces never, and the store's
   design system wins every conflict. Show the person two or three borrowed patterns with a link each
   before building.
5. **Then the playbook** for this page type (`../page-audit/references/page-type-playbook.md`): its
   must-have checks decide which regions the page needs and that the primary action sits in the first
   screen. Copy facts come from the brand files and visual values from `design.md`.

If nothing similar can be read, say the design basis is the brand files and the playbook only, and flag it.

## 4. Options and plan

**Options first (new pages).** Build two or three page options from the design basis, each a different
section order, not three wordings of one layout. Score each for conversion, brand fit, UX, speed and build
cost, and recommend the best (`references/page-quality.md` section 3). Show them with the recommendation
first; the person's pick wins. Copy for the chosen option is written with `copywriter` when it is installed
(`page-quality.md` section 5, rule 8).

For each region choose from the reuse order in the rules. Show the person a plain-language table:
region, which section it will use (existing as is, one new setting, base-theme, or a recommended new
section), and why. A recommended new section names the pattern, the reference page that shows it and what
the page gains (`page-quality.md` section 4). When
recreating a reference, add what the reference does there and every place the brand guidelines replace
the reference's value (step 3). Get a
yes before building. The plan names the staging theme (name and id) it will be built on.

**If a new section type is needed**, plan it explicitly and follow the store repo's rules for adding one:

- Check existing sections first; copy the structure and pattern of the closest sibling.
- Name and place the files as the repo requires; make it appear in the theme editor's "add section"
  list (a preset, in most themes).
- Every merchant-editable value is a setting with a sensible default: no hardcoded colours, fonts or
  copy. Include a colour-scheme setting so it inherits the store's palette.
- Images carry width, height, lazy loading and alt text; placeholders are obviously placeholders.
- Styles are scoped in the repo's preferred way and go where the repo says; JavaScript only if needed
  and in the repo's pattern.
- Record anything that touches a shared base file in the repo's register of base-file changes.

## 5. Capture the baseline

Before the first edit, start the change pack as set out in
`../page-studio/references/baseline-and-change-pack.md`. For a **new page** the baseline is the
list of existing templates plus the site-wide numbers (a few existing pages' section inventory, total
height and the `theme check` count), so the new page can be shown not to disturb anything. For a
**section added to an existing page**, capture that page's full baseline first, as for any edit.
Connector route: record `theme check` as "Can't tell", and save the theme manifest and each file
you will touch as `baseline/` (`baseline-and-change-pack.md`).

## 6. Build in the working copy

Add the template (or the section) and every region; list all section ids in the right order. Fill
settings with real, approved values or obvious placeholders; leave image pickers blank where rights are
unconfirmed; keep every number inside the schema's range. Add CSS only if the existing sections truly
can't do it, following the repo's cascade, scoping and breakpoint rules. Run `theme check`; the count
must not be higher than the baseline's. Record the intended structure and the files touched in sections
3 and 4 of the change pack. Connector route: `theme check` can't run; build in `work/` and run the
pre-write checks in `verify.md` instead.

## 7. Verify

Run `../page-studio/references/verify.md` on the rendered page. For something new the checks
that matter most are: it exists and reads as planned (checks 1 and 5), the theme editor's add, remove,
reorder and duplicate controls work and empty fields and long headings don't break layout (check 10),
other breakpoints and colour schemes hold (check 6), values come from the spec (check 12), and nothing
that already existed moved (check 2). Any failure goes back to step 6; nothing ships on a failed check.
Then **look, score, fix once** (`references/page-quality.md` section 8): full-page captures at 375 and
1440 px, one line per check (first screen, one goal, doubts answered, proof at the button, terms, FAQs,
mobile, rhythm and type, no placeholders, media weight), fix what the page can, capture again, and list what
needs the person.
Never say a page "matches" a reference without a measured parity table. **Connector route:** step 8
comes first (the pre-write checks, then the write to the staging theme), and this step runs there
right after it. Nothing renders before the write; a failed check means the change is not ready, so
fix it or revert.

## 8. Ship to the staging theme

Run `../page-studio/references/ship-to-draft.md`: check nobody edited the touched files
since the baseline, push only the new and touched files to the staging theme (and commit them on the `staging` branch
when the theme is in a git repository), pull them back as
proof, re-check the preview, write the QA entry
(`../page-studio/references/qa-entry-format.md`), and set any audit rows to `done`. Connector route: the calls are in `connector-route.md`, and the proof is a read-back, not a pull-back. Never push to the live theme, and never suggest publishing; if the person asks to go live, follow `ship-to-draft.md` section 8. To undo, use
`../page-studio/references/revert-mode.md`.

## 9. Hand back

Give a short, plain summary: what now exists and where it can be seen on the staging theme, what was
verified with the numbers, the page score from step 7, and what the person still has to supply or do
(images, final copy, creating the page in the store admin and choosing the template). For a new page, add
the measurement list (`references/page-quality.md` section 9): a tagged link per traffic source, the
conversion event to watch, and what to compare after two to four weeks. On the connector route, say that the code
checker (`theme check`) could not run. End with the hand-over line (`theme-target.md` section 6):
"Done on the staging theme <name> (<id>). Preview: <link>. Your live store has not changed." Say
nothing about publishing unless the person asks.

## Checklist before finishing

- [ ] Setup check passed (or already passed this conversation); anything missing was explained and fixed step by step
- [ ] Page, section or section type settled; name and handle checked for clashes
- [ ] Brief settled (goal, traffic source, offer, reader's doubts, proof)
- [ ] Plan built from the reference's measured values, or (with no reference) from a Reference study of
      five to eight pages (inspiration brands, competitor, trend leaders) with what works, what doesn't and
      durable trends versus fads, plus the playbook's must-haves
- [ ] Two or three options scored (conversion, brand fit, UX, speed, build cost); recommendation shown first
- [ ] Existing sections reused first; any new section type called out with its reason, approved and built to the repo's rules
- [ ] Look, score, fix once done at 375 and 1440 px; measurement list in the hand-back
- [ ] Plan table agreed before building
- [ ] Baseline captured before the first edit; change pack started
- [ ] No hardcoded colours, fonts or text; numbers inside schema ranges; images blank where unconfirmed; placeholders obvious
- [ ] Verified at desktop and mobile including the editor controls; nothing existing moved
- [ ] Staging theme settled once (remembered or created); pushed only to it, only the new and touched files, pulled back
      (connector route: read back) identical; never the live theme
- [ ] Connector route only: route and its two differences (checked on the staging theme after the write; no `theme check`) said in the plan and agreed
- [ ] No credential typed; the person knows what they still must supply
