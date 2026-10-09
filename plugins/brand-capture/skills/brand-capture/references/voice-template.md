# BRAND-VOICE.md template

BRAND-VOICE.md holds how the brand sounds: the part of the brand file that writers act on, and the part that changes
most often. It sits next to BRAND.md; BRAND.md's `voice_doc` key and its Voice section point to it. Copy this layout
exactly: `scripts/validate_brand.py` checks the front-matter keys and the `##` headings, in this order. Replace each
`<…>` with content and delete the guidance in *italics*.

**What goes here, and what doesn't.** Tone only: how the brand sounds and what it avoids saying. Naming and
compliance rules stay in BRAND.md because other skills read them on their own: **Terminology** (which names and
spellings to use), **Claim limits** (what can never be promised or said, disclaimers, the client's never-say list),
**Brand architecture** (which name goes where) and **Inspiration brands**. Where this file and BRAND.md disagree,
BRAND.md wins.

**Origin labels** are the same as in BRAND.md: `(from site)`, `(repo)`, `(client)`, `(inferred)`, `(suggested)`. A
`(client)` line is never overwritten by a scan. Unlike BRAND.md, this file holds **no** `[[CLIENT TO CONFIRM]]`
placeholders: an unknown is a question in BRAND.md and `BRAND-QUESTIONS.md`, and the voice line waits (is left out)
until it is answered. The validator fails a placeholder here.

**Budget:** aim for 40 to 70 lines. The validator warns above 90 lines or 1,200 words and fails above 140 lines or
2,000 words. Never copy from the site at length: short verbatim quotes only, each from a saved page.

**Status and revision** follow BRAND.md: `draft` until the client approves both files together, and `revision`
goes up by one on every write, with a row in this file's Change log (and a row in BRAND.md's Change log, Sections:
Voice).

The front matter is flat `key: value` lines (no nesting, no quotes). Dates are `YYYY-MM-DD`.

---

```markdown
---
voice_md_schema: 1.0
brand: <same as BRAND.md `brand`>
parent_doc: BRAND.md
brand_md_revision: <the BRAND.md `revision` this file was last checked against>
status: <draft | approved, same as BRAND.md>
revision: <1, 2, 3 ... +1 on every write>
captured: <YYYY-MM-DD of the first capture>
last_updated: <YYYY-MM-DD of the latest write>
source: <where it came from, e.g. "brand-capture 1.2.0 scan of https://example.com" or "moved from the Voice section of BRAND.md rev 1">
captured_by: brand-capture 1.2.0
---

# <Brand> brand voice

> **How <Brand> sounds in customer-facing copy.** <Where this came from, one sentence.> `BRAND.md` still owns names,
> Terminology and Claim limits, and wins where they conflict with anything on this page. Status `draft`: lines marked
> (inferred) are assumptions until the client approves them. To request a change, add a line to `BRAND-REQUESTS.md`.

## In three words
<adjective, adjective, adjective> *three a copywriter can act on ("plain, confident, warm"), never vague ones
("premium, quality")*

## How it sounds
- <sentence length and headline length>
- <point of view: we / you, and how often>
- <formality and technical depth; how clinical or technical words are used>
- <how it handles reassurance, humour, urgency>

## Signature phrases
"<verbatim>", "<verbatim>", "<verbatim>" (from site) *two to five, each quoted exactly from a saved page*

## Do / don't
*3 to 5 pairs, one line each, every side with a short real example rewritten in the brand's voice. A writer acts
on examples, not adjectives.*
- Do: <...> e.g. "<example>" · Don't: <...> e.g. "<example>"

## Words and habits to avoid
<words, claims-by-tone and habits the brand steers away from; each from evidence (words competitors use that the
brand never does, tone it clearly avoids) or labelled (inferred). When the site has two registers, say which one new
writing follows.>

## Rules that stay in BRAND.md
Word choice that is a naming or compliance rule, not a matter of tone, is kept in `BRAND.md`:
- **Terminology:** <one line on what it covers for this brand>
- **Claim limits:** <one line: what can never be promised or said, the approved disclaimers, the client's never-say list>
- **Brand architecture:** <one line: which brand name to use on which page>
- **Inspiration brands:** <one line: style references only, never to copy; name the one that bears on voice, if any>

## Change log
| Rev | Date | Requested by | Summary |
|---|---|---|---|
| 1 | <YYYY-MM-DD> | <client name or "agency for client", with reference> | <first capture, or moved out of BRAND.md rev N> |
```
