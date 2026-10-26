---
name: page-content-studio
description: >-
  The front door for Shopify page work. Use when a request spans several jobs ("improve the
  homepage and apply the top fixes", "take this page from audit to a draft I can review", "do the
  whole thing") or when it isn't clear which job is wanted. It decides the job and hands it to the
  right skill: page-audit (find where a page falls short, read-only), page-update (change something
  that exists), page-build (build a new page), page-verify (check a change on the rendered page) or
  page-ship (push to a draft, go-live gate, revert), and chains them in order. For a request that
  clearly names one job, those skills trigger directly. Brand-agnostic, built for the Site Editor.
  Not for blog posts (use shopify-blog-writer or shopify-blog-rewrite) and not for accessibility
  audits (use accessibility-audit).
---

# Page content studio

The front door. It does no page work itself: it works out which job a request is, hands it to the
skill that owns it, and chains the jobs in order when a request needs more than one. Brand-agnostic;
brand facts come from the brand files, never invented.

## The skills

| Skill | Job | Writes to a theme? |
|---|---|---|
| `page-audit` | Find where a page falls short against what its type should do; rank fixes with owners; keep `PAGE-AUDIT.md` | No, read-only |
| `page-update` | Change something that already exists, the narrowest safe way | Local working copy only |
| `page-build` | Build a new page from sections, planned from what its type needs | Local working copy only |
| `page-verify` | Prove a change on the rendered page: it exists, nothing else moved, nothing broke | No, read-only |
| `page-ship` | Push the verified files to a draft theme, prove they landed, log, hold the go-live gate, revert | **The only one that pushes** |

## Which job is this?

| The person says... | Hand to |
|---|---|
| "Improve the homepage", "what's wrong with this page", "what should we fix", "is this page any good" | `page-audit` |
| Names a change: "swap the hero image", "move pricing above the FAQ", "do row HOME-02" | `page-update` |
| "Build a page for X", "recreate this page from the live site" | `page-build` |
| "Did anything else move?", "check the draft", "is this safe to ship" | `page-verify` |
| "Push it to the draft", "go live", "revert the draft", "undo those changes" | `page-ship` |
| Several of the above, or "audit it and fix what matters" | Chain them (below) |
| Unclear | Ask one short question: "Do you already know what you want changed, or should I review the page first?" |

Invoke the chosen skill with the Skill tool, passing the page, the theme (draft or preview) and
anything already known. Don't answer its questions for the person.

## The chain

```
page-audit  ->  (the person picks rows)  ->  page-update or page-build  ->  page-verify  ->  page-ship
                                                      ^                          |
                                                      +---- a check failed ------+
```

1. **Audit** when the person hasn't decided what to change. It writes `PAGE-AUDIT.md` with ranked
   rows. Nothing is edited until the person picks rows.
2. **Update or build** on the picked rows that this theme owns, in a local working copy, after
   capturing a baseline and starting a change pack.
3. **Verify** on the rendered page against that baseline. A failure goes back to step 2 with the
   failing check; nothing ships.
4. **Ship** to a draft or preview theme. Going live is a separate, explicit step.

Run one step at a time and tell the person where they are in the chain and what comes next. If they
only want one step, stop after it.

## Rules that hold for every step

- **Draft or preview only.** Nothing reaches the live theme without an explicit yes in chat that
  names the theme, recorded by `page-ship`.
- **Only `page-ship` pushes.** `page-update` and `page-build` edit a local working copy;
  `page-audit` and `page-verify` change nothing.
- **Only picked rows are acted on.** A recommendation nobody chose stays an open row.
- **Never type a password or credential** for the person; blocked access is reported and handed back.
- **Brand facts come from the brand files** (`BRAND.md`, `BRAND-VOICE.md`, `design.md`), never from
  memory. Missing brand files block new copy, not structural changes.
- **Hard limits win.** Tracked booking links, regulated wording, brand look: what the person said
  must not change overrides every recommendation.
- **Plain language for the Site Editor**: someone on the marketing, content or operations side
  who describes what a visitor sees, not where it lives in the theme.

## Shared files

- Intake, playbook, recipes and the audit file format live in `page-audit/references/`.
- The baseline and change pack format live in `page-verify/references/`.
- The QA log format and revert mode live in `page-ship/references/`.

Each skill points to the files it needs, so any of them can be used on its own.

## Checklist before finishing

- [ ] The job was identified and handed to the owning skill, not done here
- [ ] The person knows which step of the chain they are in and what comes next
- [ ] Nothing was pushed except by `page-ship`; the live theme was not touched
- [ ] No credential was typed or passed on
