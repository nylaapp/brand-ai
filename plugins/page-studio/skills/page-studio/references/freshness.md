# Freshness: suggest a refresh, not only fixes

Shared by `page-audit`, `page-edit-content` and `page-edit-design`. A page can pass every check
and still look and read tired. This step looks for that and proposes a refresh: new content, a new
layout, or both. It is always a **suggestion**: nothing changes until the person picks it.

## When to run it

- `page-audit`: always, after the gap analysis (step 6b). Fixes and refresh ideas go in separate
  groups.
- `page-edit-content` and `page-edit-design`: once, after the request is understood. Fix what was
  asked first. Then offer the refresh ideas for the same page or section in a short list. If the
  person said "only this change", offer once, in one line, and move on.

## What to look at (both desktop and mobile)

| Area | Signs it is stale | Refresh to suggest |
|---|---|---|
| Hero and first screen | Generic promise, dated or stock image, a season, year or offer that has passed, more than one competing action | New angle or proof in the headline; a different hero layout (split, full-bleed, video, product-led); one clear action |
| Section order | Same order since launch; proof or the main action sits low; a long run of the same layout | Move proof or booking or buying up; break the run with a different layout type |
| Repeated layouts | Three or more sections that are the same card grid or the same image-left text-right | Swap one for a different pattern: tabs, comparison table, timeline, carousel, logo wall, before and after, FAQ accordion |
| Content | Old offers, old prices or dates, claims with no proof, text walls, no customer voice, no current reviews | New offer or story; short proof blocks; real customer quotes or numbers; shorter copy |
| Imagery | Mixed photo styles, low resolution, no people or product in use, no mobile crop | A consistent set; new photos or crops; icons or illustration where photos are missing |
| Mobile | A desktop layout squeezed down; long stacks; small tap targets; hidden proof | A mobile-first layout for that section; horizontal swipe rows; sticky action bar |
| Against the field | `COMPETITORS.md`, the brand's inspiration sites or the page-type playbook show a pattern this page lacks | Name the pattern and the source. Copy the idea, never the words or images |

## Rules

- **Look at both desktop (1440x900) and mobile (375x812).** Name the viewport for each point.
  A refresh must work at both.
- **Evidence, not taste.** Each idea names what was seen (the section, the date or text that is
  old, the repeated layout, the competitor pattern) and why a visitor would notice. No idea
  without an observation.
- **Brand first.** Ideas stay inside `BRAND.md`, `BRAND-VOICE.md` and `design.md`. Use only
  tokens, fonts and colours that exist there. Anything that would change the brand look is
  labelled "needs a brand decision".
- **Content ideas are drafts.** Never invent facts, prices, results, reviews or claims. Mark any
  figure or claim as "needs source" and send regulated or numeric claims to `fact-check`.
- **Limits win.** Respect what the person said must not change (tracked links, regulated wording).
- **Small, medium, large.** Offer at least one small option (setting, reorder, new image or
  headline) so a refresh is possible without a rebuild. Give a large option (new section type or
  full relayout) only where the page clearly needs it.
- **Keep it short.** About three ideas per page, ranked by closeness to the page's main action.
  The rest go in one line as "also noticed".

## Idea format

| Field | Content |
|---|---|
| What to change | One plain sentence: the section and the new content or layout |
| Why it feels dated | What was seen, at which viewport |
| What the visitor gets | The benefit in plain words |
| Desktop and mobile | One line each: how it looks at each width |
| Size | S, M or L, as in `page-audit/references/audit-file.md` |
| Needs | Owner and next skill: `page-edit-content` for words, images, links; `page-edit-design` for layout, order, style; `page-create` for a new section or page; a fact-check or a brand decision if flagged |

Show a rough before and after in words, or a simple sketch, so a non-technical person can picture
it. Never present an idea as a finding.
