---
name: page-content-studio
description: >-
  The front door for Shopify page work. Use when a request spans several jobs ("improve the
  homepage and apply the top fixes", "audit it and fix what matters", "change the headline and
  restyle the section"), when it isn't clear which job is wanted, or when someone only wants an
  existing change checked on the rendered page, pushed to a draft theme, or reverted. It decides the
  job and hands it to the right skill: page-audit (find where a page falls short, read-only),
  page-create (something new: a page, a section, a section type), page-edit-content (change the
  words, images or links of something that exists) or page-edit-design (change the layout, order,
  spacing, colour or style of something that exists), and chains them in order. For a request that
  clearly names one job, those skills trigger directly. Brand-agnostic, built for the Site Editor.
  Not for blog posts (use shopify-blog-writer or shopify-blog-rewrite) and not for accessibility
  audits (use accessibility-audit).
---

# Page content studio

The front door. It does no page editing itself: it works out which job a request is, hands it to the
skill that owns it, and chains the jobs in order when a request needs more than one. The shared
delivery steps (baseline, verify, ship to a draft, revert, QA log) live here in `references/`, and the
three editing skills run them themselves. Brand-agnostic; brand facts come from the brand files, never
invented.

## The skills

| Skill | Job | Writes to a theme? |
|---|---|---|
| `page-audit` | Find where a page falls short against what its type should do; rank fixes with owners; keep `PAGE-AUDIT.md` | No, read-only |
| `page-create` | Make something **new**: a page, a section on a page, or a new section type | Local working copy, then a draft theme |
| `page-edit-content` | Change what something that **exists says or shows**: words, images, links, alt text, SEO fields | Local working copy, then a draft theme |
| `page-edit-design` | Change how something that **exists looks or is arranged**: layout, order, spacing, colour, type, styles, responsive behaviour | Local working copy, then a draft theme |

Each editing skill ends with the same steps, defined once in this folder: capture a baseline, verify
on the rendered page, push only the touched files to a draft theme and pull them back as proof, and
stop at the go-live gate.

## Which job is this?

| The person says... | Hand to |
|---|---|
| "Improve the homepage", "what's wrong with this page", "what should we fix" | `page-audit` |
| "Build a page for X", "add a testimonials section", "make a new section for team members" | `page-create` |
| "Change the headline", "fix the typo", "swap this image", "make the button go to X" | `page-edit-content` |
| "Move this section up", "make the hero shorter on mobile", "change the colours", "restyle the button" | `page-edit-design` |
| "Do row HOME-02" | Read the row; its type decides: words, images or links go to `page-edit-content`; layout, order or style to `page-edit-design`; something new to `page-create` |
| One request that is both content and design | Do the content first, then the design, each as its own change with its own baseline and check |
| Only wants an existing change checked | Run `references/verify.md` here; no edits |
| Only wants an existing change pushed to the draft | Run `references/ship-to-draft.md` here (it needs a passed verification) |
| "Undo that", "revert the draft" | Run `references/revert-mode.md` here |
| Unclear | Ask one short question: "Do you already know what you want changed, or should I review the page first?" |

**The line between content and design.** A section reorder is design. A button's label is content and
its style is design. Swapping an image is content; changing its size, crop or position is design. Adding
a new section, or a new page, is create, even when it only reuses an existing section type.

Invoke the chosen skill with the Skill tool, passing the page, the theme (draft or preview) and anything
already known. Don't answer its questions for the person.

## The chain

```
page-audit  ->  (the person picks rows)  ->  page-create | page-edit-content | page-edit-design
                                                         |
                                       baseline -> edit working copy -> verify -> ship to draft
                                                         |
                                               go live only on an explicit, recorded yes
```

1. **Audit** when the person hasn't decided what to change. It writes `PAGE-AUDIT.md` with ranked rows;
   nothing is edited until the person picks rows.
2. **Create or edit** the picked rows this theme owns, one skill at a time, each as its own change.
3. **Verify and ship** run inside each editing skill; a failed check goes back to the edit and nothing
   ships.

Run one step at a time and tell the person where they are and what comes next. If they only want one
step, stop after it.

## Rules that hold for every step

- **Draft or preview only.** Nothing reaches the live theme without an explicit yes in chat that names
  the theme, recorded in the change pack and the QA entry (`references/ship-to-draft.md`).
- **Only verified changes are pushed, and only the touched files.** No bare pushes.
- **Only picked rows are acted on.** A recommendation nobody chose stays an open row.
- **Never type a password or credential** for the person; blocked access is reported and handed back.
- **Brand facts come from the brand files** (`BRAND.md`, `BRAND-VOICE.md`, `design.md`), never from
  memory. Missing brand files block new copy, not structural changes.
- **Hard limits win.** Tracked booking links, regulated wording, brand look: what the person said must
  not change overrides every recommendation.
- **Plain language for the Site Editor**: someone on the marketing, content or operations side who
  describes what a visitor sees, not where it lives in the theme.

## Shared files

| Where | What |
|---|---|
| `references/baseline-and-change-pack.md` | What to capture before any edit, and the one-file record carried through a change |
| `references/verify.md` | The checks that prove a change on the rendered page |
| `references/ship-to-draft.md` | Pushing to a draft, pull-back proof, the log, the go-live gate |
| `references/revert-mode.md` | Restoring a draft to its baseline and proving it |
| `references/qa-entry-format.md` | The QA log entry |
| `../page-audit/references/` | Intake and goal questions, the page-type playbook, observation recipes, the `PAGE-AUDIT.md` format |

Each skill points to the files it needs, so any of them can be used on its own.

## Checklist before finishing

- [ ] The job was identified and handed to the owning skill, not done here (verify, ship and revert
      requests excepted)
- [ ] A mixed request was split into one change per skill, content before design
- [ ] The person knows where they are in the chain and what comes next
- [ ] Nothing was pushed except verified files to a draft; the live theme was not touched
- [ ] No credential was typed or passed on
