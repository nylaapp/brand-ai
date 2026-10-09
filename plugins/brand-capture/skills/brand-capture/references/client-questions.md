# Template: BRAND-QUESTIONS.md (written next to BRAND.md)

Two parts: the questions sent to the client (**at most 4**) and the items held back for the reviewer. The
validator counts the `**Q-..` entries above `## Held for later` and fails above 4; `brand_html.py` shows only
those in the client copy.

Rules for the agent:
- One entry per open item in BRAND.md, same id (`Q-01`, `Q-02` ...). Ids are never reused.
- Pick the 4 with `references/discovery.md` §3b: claims needing proof or permission, then facts that disagree,
  then names, then unsourced proof points. Merge items one answer settles.
- Setup questions 3 and 4 (approver, never say) were asked at the start. If the client skipped them, they
  are the first two questions here and count toward the 4.
- Offer choices whenever the evidence allows (A/B/C plus "other"). Quote both sides of a conflict with where each
  appears. Plain language: no file names, section names or ids in the question text itself.
- Everything else goes under "Held for later" with its evidence, for the reviewer. It is never sent as a list.
- The front matter is flat `key: value` lines like BRAND.md's. Keep `questions_sent` and `questions_held` equal to the
  entries in each part, and move `brand_md_revision` whenever BRAND.md's revision moves.
- When an answer arrives, mark the entry `Answered <date>: <answer> (from <who>)`; never delete entries.

---

```markdown
---
questions_md_schema: 1.0
brand: <same as BRAND.md `brand`>
brand_md_revision: <the BRAND.md `revision` these questions belong to>
generated: <YYYY-MM-DD>
questions_sent: <number of questions for the client, 0 to 4>
questions_held: <number under "Held for later">
captured_by: brand-capture 1.2.0
---

# <Brand>: brand file questions (<YYYY-MM-DD>)

## Questions for <Brand>

We've drafted your brand file: the one reference every tool we use reads before writing anything for you.
These points only you can settle. Reply in any form (for example "Q-03: B"). Anything you leave blank stays
marked as unconfirmed, and our tools won't present it as fact.

**Q-01 · <question>**
<one line of context, with where we saw it>
A) <option>  B) <option>  C) Other: ____

**Q-02 · <question>**
...

## Held for later (not sent to the client)

For whoever reviews BRAND.md. Each stays a `[[CLIENT TO CONFIRM]]` line in BRAND.md until it's answered.

**Q-05 · <item>**
<evidence and why it waited>
```

---

## Worked examples

**AYA Medical Spa** (medical spa group, 12 locations, several trading names; scan of 2026-10-01). Sent:

| Id | Question | Why it made the 4 |
|---|---|---|
| Q-01 | Your blog disclaimer says "locations across Atlanta and Dallas", but you also have New York and Florida clinics. May we update it to all four regions? | Legal text that every new post copies |
| Q-02 | Your site says "over 25 years", but a 2018 post celebrates "15 Years of Skincare Excellence". Which is right today? | A proof point copy repeats often |
| Q-03 | Location pages call AYA "NYC's leading medical spa" and "one of the best medspas in Atlanta". Keep each with a source, soften, or remove? | Superlative claims |
| Q-04 | Which name should copy use by default: "AYA Medical Spa" or "AYA Skin"? And are the three New York practice names right? | Names: half the clinics trade under another name |

Held for later: the awards behind "award-winning", ÉLAN's co-founder surname (Pirkl or Cronk), the "Georgia and
Texas" line on the Locations page, the Dallas street number, the founding story, the Search Console property, the
Saans TRIAL font licence. The last three are not brand questions for the client at all: the report lists them
for the agency.

**A jewellery store** (illustration of what the same rules produce for a non-regulated brand). Sent:

| Id | Question |
|---|---|
| Q-01 | Product pages say "conflict-free diamonds". What certification or supplier statement backs it, or should we stop using it? |
| Q-02 | One collection is "solid 14k gold" on one page and "gold vermeil" on another. Which is right? |
| Q-03 | Your FAQ promises a "lifetime warranty", your returns policy says "1 year". Which applies? |
| Q-04 | Earrings are described as "hypoallergenic". Is that true for every metal you use? |

Held for later: whether every piece is "handmade" (copy can say "handmade" only where the product page does).
No medical, clinician or regulator questions: the scan found no such claims.
