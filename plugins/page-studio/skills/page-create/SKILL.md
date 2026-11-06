---
name: page-create
description: >-
  Create something new on a Shopify theme: a new page (landing page, campaign page, service or
  treatment page, region or location page), a new section added to an existing page, or a new
  section type built to the theme's own rules. Plans it from what its page type needs (the
  playbook's must-haves, primary action in the first screen), reuses existing sections before
  building anything new, shows a plain-language plan for a yes, then builds it (in a local working
  copy with the Shopify CLI, or, without the CLI, directly on the draft through the Shopify
  connector when it can change themes), verifies it on the rendered page including the theme
  editor's controls, and sends only the new and touched files to the theme the person chose (always
  a draft, never the live theme). Can recreate a page from a live reference URL by capturing
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
theme the person chose (always a draft, never the live theme). The live theme is never edited: work goes to a draft theme, created if there isn't one.

It works one of two ways, chosen by the setup check: with the Shopify CLI and a local working copy
(the default), or, when the CLI isn't installed and the Shopify connector can change themes, through
that connector (`../page-studio/references/connector-route.md`). The rules and the safety are the
same; the steps below say where the connector route differs.

```
0. Setup check -> 1. Context -> 2. Understand what is being created -> 3. Reference or playbook ->
4. Plan (approval) -> 5. Capture the baseline -> 6. Build in the working copy ->
7. Verify -> 8. Ship to the theme -> 9. Hand back
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

## Rules

- **Working copy first, on the theme the person chose.** Never push from the working copy except
  through the ship step (connector route: no copy of the whole theme; build in `work/` and write
  nothing except through the ship step). The theme is asked once and remembered (`theme-target.md`); it is always a draft or unpublished theme, never the live theme (if there is none, `theme-target.md` asks for one or creates one) (`theme-target.md`, `ship-to-draft.md`).
- **The connector route changes the order, not the rules.** With no Shopify CLI, nothing can be
  rendered before the files are written, so the rendered checks run on the private draft right after
  the write (the live theme is never touched), and `theme check` can't run. Say both in the plan and
  get the person's agreement once. The calls and guards are in
  `../page-studio/references/connector-route.md`.
- **Reuse first.** For every region choose, in order: an existing section that fits; the same section
  with one small new setting; a native base-theme section or block; a new section only when the layout
  is genuinely different. One section per visual region; blocks are for repeated items inside a region.
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
narrate before acting, flag trade-offs in plain terms, and explain draft versus live the first time
it comes up: on a draft, nothing visitors see changes until they say go; these skills never edit the live theme, because edits there show to visitors at once.

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
conversation or remembered in `THEME-TARGET.md` and say so in one line, or settle one with that file (an existing draft, or a new draft copy; never the live theme) and remember it for every other skill. Don't ask again unless the
person names a different theme. If the person names the live theme, that file applies: it is refused and a draft is used.

Follow section 1 of `../page-audit/references/intake.md`: resolve the brand files and `design.md`,
handle a partial set, and read the store repo's own rules (`AGENTS.md` or `CLAUDE.md`), including how
sections and blocks are named, structured, scoped and registered. With no brand files, structure can be
planned but copy waits for brand-capture. Visual values come from `design.md`, else the store repo's
visual spec or the theme's settings; never invent a hex, font, size or radius.

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

## 3. Reference or playbook

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

**Without one:** start from the playbook section for this page type
(`../page-audit/references/page-type-playbook.md`). Its must-have checks decide which regions the page
or section needs and in what order, with the primary action in the first screen. Take copy facts from
the brand files and visual values from `design.md`.

## 4. Plan

For each region choose from the reuse order in the rules. Show the person a plain-language table:
region, which section it will use, whether it needs a new setting or a new section, and why. When
recreating a reference, add what the reference does there and every place the brand guidelines replace
the reference's value (step 3). Get a
yes before building. The plan names the draft theme (name and id) it will be built on.

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
Never say a page "matches" a reference without a measured parity table. **Connector route:** step 8
comes first (the pre-write checks, then the write to the draft), and this step runs on the draft
right after it. Nothing renders before the write; a failed check means the draft is not ready, so
fix it or revert.

## 8. Ship to the chosen theme

Run `../page-studio/references/ship-to-draft.md`: check nobody edited the touched files
since the baseline, push only the new and touched files to the chosen theme, pull them back as
proof, re-check the preview, write the QA entry
(`../page-studio/references/qa-entry-format.md`), and set any audit rows to `done`. Connector route: the calls are in `connector-route.md`, and the proof is a read-back, not a pull-back. Never push to the live theme. Publishing a draft is done by the person in the store admin; say where (`ship-to-draft.md` section 8). To undo, use
`../page-studio/references/revert-mode.md`.

## 9. Hand back

Give a short, plain summary: what now exists and where it can be seen on the draft, what was verified
with the numbers, and what the person still has to supply or do (images, final copy, creating the page
in the store admin and choosing the template, publishing). Say whether it is on the draft only or live.
On the connector route, say that the code checker (`theme check`) could not run.

## Checklist before finishing

- [ ] Setup check passed (or already passed this conversation); anything missing was explained and fixed step by step
- [ ] Page, section or section type settled; name and handle checked for clashes
- [ ] Plan built from the reference's measured values or the playbook's must-haves
- [ ] Existing sections reused first; any new section type called out, approved and built to the repo's rules
- [ ] Plan table agreed before building
- [ ] Baseline captured before the first edit; change pack started
- [ ] No hardcoded colours, fonts or text; numbers inside schema ranges; images blank where unconfirmed; placeholders obvious
- [ ] Verified at desktop and mobile including the editor controls; nothing existing moved
- [ ] Theme settled once (remembered or asked); pushed only to it, only the new and touched files, pulled back
      (connector route: read back) identical; never the live theme
- [ ] Connector route only: route and its two differences (checked on the draft after the write; no `theme check`) said in the plan and agreed
- [ ] No credential typed; the person knows what they still must supply
