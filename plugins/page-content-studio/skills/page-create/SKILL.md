---
name: page-create
description: >-
  Create something new on a Shopify theme: a new page (landing page, campaign page, service or
  treatment page, region or location page), a new section added to an existing page, or a new
  section type built to the theme's own rules. Plans it from what its page type needs (the
  playbook's must-haves, primary action in the first screen), reuses existing sections before
  building anything new, shows a plain-language plan for a yes, then builds it in a local working
  copy, verifies it on the rendered page including the theme editor's controls, and pushes only the
  new and touched files to a draft theme. Can recreate a page from a live reference URL by capturing
  measured values, never from a text-only fetch. Brand-agnostic, written for the Site Editor. Use for
  "build a page for X", "make a landing page for the new treatment", "create a region page", "add a
  testimonials section to the homepage", "build a new section for team members", "recreate this page
  from the live site". Not for changing words, images or links on something that exists (use
  page-edit-content), changing layout or style of something that exists (page-edit-design),
  open-ended "improve this page" (page-audit), blog posts (shopify-blog-writer) or accessibility audits
  (accessibility-audit).
---

# Page create

Make something **new**: a page, a section on a page, or a new kind of section. It is planned from what
that kind of page needs, built from existing pieces first, and made in a local working copy. The skill
proves the result on the rendered page and puts only the new and touched files on a draft theme. Going
live is a separate, explicit step.

```
1. Context -> 2. Understand what is being created -> 3. Reference or playbook ->
4. Plan (approval) -> 5. Capture the baseline -> 6. Build in the working copy ->
7. Verify -> 8. Ship to the draft -> 9. Hand back
```

## Rules

- **Working copy first, draft theme only.** Never push from the working copy except through the ship
  step, and never to the live theme without an explicit, recorded yes (`ship-to-draft.md`).
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
- **Never delete or rename** an existing section or block file, and never edit a shared base-theme file
  without checking every usage.
- **Never type a password or credential** for the person.
- **Hard limits win.** What the person said must not change overrides the request.

## Who this is for

A Site Editor on the marketing, content or operations side. Plain language, explain a term once,
narrate before acting, flag trade-offs in plain terms, and explain draft versus live the first time it
comes up: nothing visitors see changes until they say go.

## 1. Context

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
- **Which theme?** A draft or preview; record id and role. Get a working copy (pull the draft theme
  first, per the store repo's workflow, so admin-side edits aren't lost).

**From an audit.** If the request is a row ID or points at a `PAGE-AUDIT.md` (rules in
`../page-audit/references/audit-file.md`), read the rows marked `picked` that call for something new and
are owned by this theme. Work only on those and carry each row's baseline number.

## 3. Reference or playbook

**With a reference URL:** capture desktop and mobile widths, scrolling slowly so lazy content loads;
list every section top to bottom including ones with no text; read computed values (container, padding,
gaps, font, size, weight, colours, radius) rather than eyeballing them; and capture hover, focus and
disabled states of buttons and links. If no rendered view is possible, say plainly it's blocked and name
what failed; don't guess.

**Without one:** start from the playbook section for this page type
(`../page-audit/references/page-type-playbook.md`). Its must-have checks decide which regions the page
or section needs and in what order, with the primary action in the first screen. Take copy facts from
the brand files and visual values from `design.md`.

## 4. Plan

For each region choose from the reuse order in the rules. Show the person a plain-language table:
region, which section it will use, whether it needs a new setting or a new section, and why. Get a yes
before building.

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
`../page-content-studio/references/baseline-and-change-pack.md`. For a **new page** the baseline is the
list of existing templates plus the site-wide numbers (a few existing pages' section inventory, total
height and the `theme check` count), so the new page can be shown not to disturb anything. For a
**section added to an existing page**, capture that page's full baseline first, as for any edit.

## 6. Build in the working copy

Add the template (or the section) and every region; list all section ids in the right order. Fill
settings with real, approved values or obvious placeholders; leave image pickers blank where rights are
unconfirmed; keep every number inside the schema's range. Add CSS only if the existing sections truly
can't do it, following the repo's cascade, scoping and breakpoint rules. Run `theme check`; the count
must not be higher than the baseline's. Record the intended structure and the files touched in sections
3 and 4 of the change pack.

## 7. Verify

Run `../page-content-studio/references/verify.md` on the rendered page. For something new the checks
that matter most are: it exists and reads as planned (checks 1 and 5), the theme editor's add, remove,
reorder and duplicate controls work and empty fields and long headings don't break layout (check 10),
other breakpoints and colour schemes hold (check 6), values come from the spec (check 12), and nothing
that already existed moved (check 2). Any failure goes back to step 6; nothing ships on a failed check.
Never say a page "matches" a reference without a measured parity table.

## 8. Ship to the draft

Run `../page-content-studio/references/ship-to-draft.md`: check nobody edited the touched files since
the baseline, push only the new and touched files to the draft theme, pull them back as proof, re-check
the preview, write the QA entry (`../page-content-studio/references/qa-entry-format.md`), and set any
audit rows to `done`. Going live happens only if the person asks, and only with their explicit,
recorded yes. To undo, use `../page-content-studio/references/revert-mode.md`.

## 9. Hand back

Give a short, plain summary: what now exists and where it can be seen on the draft, what was verified
with the numbers, and what the person still has to supply or do (images, final copy, creating the page
in the store admin and choosing the template, publishing). Say whether it is on the draft only or live.

## Checklist before finishing

- [ ] Page, section or section type settled; name and handle checked for clashes
- [ ] Plan built from the reference's measured values or the playbook's must-haves
- [ ] Existing sections reused first; any new section type called out, approved and built to the repo's rules
- [ ] Plan table agreed before building
- [ ] Baseline captured before the first edit; change pack started
- [ ] No hardcoded colours, fonts or text; numbers inside schema ranges; images blank where unconfirmed; placeholders obvious
- [ ] Verified at desktop and mobile including the editor controls; nothing existing moved
- [ ] Pushed only to a draft, only the new and touched files, pulled back identical; nothing live without a recorded yes
- [ ] No credential typed; the person knows what they still must supply
