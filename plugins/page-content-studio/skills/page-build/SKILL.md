---
name: page-build
description: >-
  Build a new Shopify page from sections: a landing page, campaign page, service or treatment page,
  region or location page, or a new homepage section. Plans the page from what its page type
  needs (the playbook's must-haves, primary action in the first screen), reuses existing sections
  before building anything new, shows a plain-language plan for a yes, then builds the template in a
  local working copy of the theme. Can recreate a page from a live reference URL by capturing
  measured values, never from a text-only fetch. Brand-agnostic, written for the Site Editor. Use for
  "build a page for X", "make a landing page for the new treatment", "create a region page",
  "recreate this page from the live site". Edits the working copy only; it never pushes. Not for
  changing something on an existing page (use page-update), open-ended "improve this page"
  (page-audit), checking (page-verify), pushing or going live (page-ship), or blog posts
  (shopify-blog-writer).
---

# Page build

Build a new page from the theme's own sections, planned from what that kind of page needs, in a
**local working copy**. It never pushes: `page-verify` checks the result and `page-ship` pushes it.

```
1. Context -> 2. Understand the page -> 3. Reference or playbook ->
4. Plan the regions (approval) -> 5. Capture the baseline -> 6. Build the template ->
7. Hand to page-verify, then page-ship
```

## Rules

- **Working copy only.** Never push, publish or edit the live theme. Pushing belongs to
  `page-ship`.
- **Reuse first.** For every region choose, in order: an existing section that fits; the same
  section with one small new setting; a native base-theme section or block; a new section only when
  the layout is genuinely different. One section per visual region; blocks are for repeated items
  inside a region.
- **Get a yes on the plan before building.**
- **No hardcoded colours, fonts or text** that a setting could hold. Check every number against
  the schema's min and max, since a bad value can reject the whole push.
- **Leave image pickers blank** if rights aren't confirmed, and never link to a reference site's own
  CDN. A new font needs a licence check with the person first; never swap in a lookalike silently.
- **Don't invent brand facts or claims.** Copy comes from the brand files or the person; with
  neither, wait for brand-capture. Placeholder text must be obviously a placeholder.
- **Never recreate a reference page from a text-only fetch.** A capture without computed values and
  images isn't a capture. Don't say "matches the reference" without a measured parity table.
- **Never type a password or credential** for the person.

## Who this is for

A Site Editor on the marketing, content or operations side. Plain language, explain a term once,
narrate before acting, flag trade-offs in plain terms, and explain draft versus live the first time
it comes up: nothing visitors see changes until they say go.

## 1. Context

Follow section 1 of `../page-audit/references/intake.md`: resolve the brand files and `design.md`,
handle a partial set, and read the store repo's own rules (`AGENTS.md` or `CLAUDE.md`). With no
brand files, structure can be planned but copy waits for brand-capture. Visual values come from
`design.md`, else the store repo's visual spec or the theme's settings; never invent a hex, font,
size or radius.

## 2. Understand the page

- **What is the page called, and what URL handle should it have?** Check it doesn't clash with an
  existing template or page.
- **What type of page is it, and what is it for?** Use `../page-audit/references/intake.md`
  sections 2 and 3 (page type, business type, the goal and who it is for, limits).
- **Is there a reference** to match (a live URL, inspiration, existing brand pages), or is it from
  scratch?
- **Which theme?** A draft or preview; record id and role. Get a working copy (pull the draft
  theme first, per the store repo's workflow, so admin-side edits aren't lost).

## 3. Reference or playbook

**With a reference URL:** capture desktop and mobile widths, scrolling slowly so lazy content
loads; list every section top to bottom including ones with no text; read computed values
(container, padding, gaps, font, size, weight, colours, radius) rather than eyeballing them; and
capture hover, focus and disabled states of buttons and links. If no rendered view is possible, say
plainly it's blocked and name what failed; don't guess.

**Without one:** start from the playbook section for this page type
(`../page-audit/references/page-type-playbook.md`). Its must-have checks decide which regions the
page needs and in what order, with the primary action in the first screen. Take copy facts from the
brand files and visual values from `design.md`.

## 4. Plan the regions

For each region choose from the reuse order in the rules. Show the person a plain-language table:
region, which section it will use, whether it needs a new setting or a new section, and why. If a
new section type is needed, say so explicitly and follow the store repo's rules for adding one
(naming, anatomy, scoping, where styles go); a dedicated section-building skill may replace this
step later. Get a yes before building.

## 5. Capture the baseline

Before the first edit, start the change pack as set out in
`../page-verify/references/baseline-and-change-pack.md`. For a new page the baseline is the list of
existing templates plus the site-wide numbers (a few existing pages' section inventory, total
height and the `theme check` count), so the new page can be shown not to disturb anything.

## 6. Build the template

In the working copy: add the template, add every section, and list all section ids in the right
order. Fill settings with real, approved values; leave image pickers blank where rights are
unconfirmed; keep every number inside the schema's range. Add CSS only if the existing sections
truly can't do it, following the store repo's cascade, scoping and breakpoint rules. Run
`theme check`; the count must not be higher than the baseline's. Record the intended structure and
the files touched in sections 3 and 4 of the change pack.

## 7. Hand on

Tell the person the page exists in the working copy only, that nothing is pushed or live, and what
they still need to supply or do themselves (images, copy, creating the page in admin and choosing
the template). Next: `page-verify` checks the render, including the theme editor's add, remove,
reorder and duplicate controls, then `page-ship` pushes to the draft theme. Never claim the page
"matches" a reference without a measured parity table.

## Checklist before finishing

- [ ] Page name, handle and type settled; no template clash
- [ ] Plan built from the reference's measured values or the playbook's must-haves
- [ ] Existing sections reused first; any new section type called out and approved
- [ ] Plan table agreed before building
- [ ] Baseline and change pack started before the first edit
- [ ] No hardcoded colours, fonts or text; numbers inside schema ranges; images blank where unconfirmed
- [ ] `theme check` count not higher; nothing pushed; live theme untouched; no credential typed
- [ ] The person knows what they still must supply, and that verify and ship come next
