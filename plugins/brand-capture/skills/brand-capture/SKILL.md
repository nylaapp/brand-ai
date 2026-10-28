---
name: brand-capture
description: >-
  One-time brand setup for a new client. Always asks first whether the brand has an existing store
  or website and an existing brand book (or other brand documents) to work from, and which draft
  theme to save the brand files in. Scans the brand's public website (About, story, mission and
  values pages, careers and news, locations, products with prices, types and colors, site colors and
  fonts, blog style, social links, disclaimers) and reads any brand book it is given, asks four
  short setup questions (top competitors, non-competitive inspiration brands, who approves things to
  make sure they're on brand, anything never to say or claim), then writes BRAND.md (the single
  source of truth for brand identity that every other skill reads) and BRAND-VOICE.md (how the brand
  sounds, kept in its own file), design.md (the brand's visual system as measured values: palette,
  type, spacing, corners, components, imagery), a readable BRAND.html copy for the client, and at
  most four follow-up questions, all saved in the chosen draft theme's folder so later customization
  and every other skill find them there. Finally points the project's agent files and skills at
  BRAND.md. Works for any kind of store or business, in Claude Code, Cowork, Claude projects, Codex
  and ChatGPT. Use when the user says "capture the brand", "set up the brand file", "create
  BRAND.md", "onboard a new client", "brand setup", or applies a client's answers to brand
  questions; and whenever another skill needs BRAND.md and it doesn't exist.
---

# Brand capture

Build `BRAND.md` once, at a client's setup, so no skill ever asks about the brand again. The brand's own material is
the source: its website, and any brand book it already has. Read them, don't interview the client. Always ask first
what exists (a site or store, a brand book) and which draft theme the files are saved in, and in the same message the
four things neither can say. What the reading can't settle becomes at most four follow-up questions. Every file is
saved in the draft theme's folder, so the brand files sit with the theme that later customization works on.

```
0. Locate → 1. Ask what to work from and where to save, then four setup questions
→ 2. Scan the site, read the brand book → 3. Read and judge
→ 4. Write BRAND.md, BRAND-VOICE.md, design.md + questions
→ 5. Validate → 6. Client copy (BRAND.html) → 7. Link the project → 8. Report
```

## Effort (read before starting)

Single use and high value: it runs once per client, and every other skill relies on the result.

**Model and effort:**
- **Use:** Claude Opus 5.5 at the highest effort available (xhigh or max).
- **Minimum for an acceptable result:** Claude Opus 5.5 at high effort. Below that, don't run it.
- **If you're running below the recommended setting** (Opus 5.5 at high, or another model), say so in the first
  message and in the report's "Run" line. Ask the reviewer to check the address, store and claim conflicts by
  hand: those are what lower settings miss first.

| | Typical store | Large or complex site |
|---|---|---|
| Working time, start to report (not counting waits for answers) | 10 to 20 minutes | 20 to 40 minutes |
| Of which the scan script | about 1 minute | 1 to 2 minutes |
| Web requests | 40 to 80 | 60 to 150 |
| Working context | about 80,000 tokens | about 150,000 tokens |
| Budget, Opus 5.5 at high or above | about USD 3 to 4 | about USD 4 to 6 |

Measured on Anna Sheffield (691 products, two stores, 10 known conflicts on the site) on 2026-10-05, same site and
same answers:

| Setting | Time | Cost (estimate) | Conflicts caught |
|---|---|---|---|
| Opus 5.5, xhigh | 36 min, including waits for answers and about 20 pages read by hand (before the scanner fixes) | about USD 3.60 | 10 of 10 |
| Opus 5.5, high | 10 min | about USD 3.20 | 8 of 10: missed a homepage still sending walk-ins to an old address, and the treated-stones disclosure |
| Sonnet 5.5, high | 6 min | about USD 1.50 | 8 of 10: missed treated stones and the gemstone-lore wording rule. Not recommended |

All three wrote a usable, category-correct file with 4 sensible questions; the difference is how many conflicts
reach the client. Cost is an estimate from token counts at API list prices, not a bill; on a Claude Pro plan,
expect a noticeable share of one 5-hour window. Stop and tell the person if the working time passes 40 minutes or
the cost passes USD 10: something is looping. Never run two captures in the same folder at once: they overwrite
each other's files.

| File | Read at |
|---|---|
| `references/discovery.md` | Steps 2 and 3: where facts live, the reading checklist, reading a brand book, conflicts, choosing the 4 questions, claim rules by category, competitors |
| `references/brand-home.md` | Steps 0, 1 and 7: asking for the draft theme, finding and writing its folder, `BRAND-HOME.md`, moving existing files |
| `references/theme-target.md` | Step 1: choosing and remembering the theme (the same file the theme skills use; sections 1 to 4 and 6 apply here) |
| `references/brand-context.md` | Step 0: the lookup order for files that already exist |
| `references/brand-template.md` | Step 4: the exact layout of BRAND.md (other skills depend on its headings) |
| `references/voice-template.md` | Step 4: the exact layout of BRAND-VOICE.md (the validator checks its headings) |
| `references/design-template.md` | Step 4: the layout of design.md, and where its values come from |
| `references/client-questions.md` | Step 4: the layout of BRAND-QUESTIONS.md, with worked examples |
| `references/report-template.md` | Step 8 |
| `references/brand-contract.md` | When someone asks how other skills should use BRAND.md |
| `scripts/scrape_site.py` | Step 2: the scan (Python 3 standard library, no installs) |
| `scripts/validate_brand.py` | Step 5 |
| `scripts/brand_html.py` | Step 6 |
| `scripts/link_brand.py` | Step 7 |
| `scripts/brand_section.py` | Prints one section or key, for skills that read BRAND.md; for Voice it also prints BRAND-VOICE.md |

## Rules

- **It's for any business.** Never ask a question or write a rule that only fits one category unless the scan
  found that category. A jewellery store gets no medical questions; a clinic gets no materials questions.
- **BRAND.md and BRAND-VOICE.md are identity only**, and only this skill writes them, only when the client asks.
  Site problems, post lists, procedures and deep competitor research live elsewhere (template: "What stays out").
- **Voice has one home.** The detail (how it sounds, signature phrases, do / don't pairs, words to avoid) is written
  in BRAND-VOICE.md only; BRAND.md's Voice section is a pointer plus the three words. Terminology and Claim limits
  stay in BRAND.md: they are naming and compliance rules, not tone.
- **Always ask what to work from.** Step 1 asks whether the brand has an existing store or site and an existing brand
  book, on every new capture and every add-design run, even when the request already names a site, the repo has one,
  or another skill called you. A brand book that is given is read and used; a site that looks like enough is never a
  reason to skip the question.
- **Always ask where the files go.** Step 1 also asks which draft theme the brand files are saved in, on every new
  capture (a remembered draft is offered first). Everything is written in that theme's folder, at its root: not in the
  theme's own folders, never in `assets/` (public), and nothing is pushed to the store. Without a draft theme, say so
  and use the central brand directory (`references/brand-home.md`).
- **Setup needs a person.** If no one can answer the setup questions (an unattended or scheduled run), don't
  start: say that brand-capture needs a person present, and stop.
- **Competitors and inspirations come from the client.** Never research or suggest other brands unless the
  person explicitly asks you to suggest.
- **Facts come from sources.** Quote mission, values and founding-story language verbatim (short quotes) with the page
  URL or document name, only from text saved in the evidence folder (page text, or a text copy of the brand book).
  Anything you conclude is labelled `(inferred)`; anything a brand book states is labelled `(from brand book)`.
- **Never invent** founders, dates, awards, prices, results, certifications or names. When two sources disagree (two
  pages, or the site and the brand book), write neither: it becomes a Q-id (`discovery.md` §3a).
- **A `(client)` line is never overwritten by a scan.** Client answers outrank the site.
- **Don't duplicate other docs.** design.md owns visual values; repo skills own procedures. BRAND.md links them.
- **design.md is measured, not imagined.** Every value comes from the live site, the scan or the theme settings, or
  from the brand book (labelled `(from brand book)`: stated, not measured), or is labelled `(inferred)` or left out.
  Never invent a hex, size, radius or hover state to fill a table. An existing design.md (the client's or the repo's)
  is never overwritten: it is the source, and BRAND.md points to it.
- **Read only on the web.** Public pages, robots.txt honoured, fixed caps. Never sign in, never submit forms.
  Follow the host repo's own device and browser rules.
- **Scratch stays out of the repo.** The scan JSON and the evidence folder go to a temp or scratch folder.

## Step 0: Locate

1. **Site URL (a first guess only):** from the request; else from the repo (README, theme config, a design doc).
   Step 1 always asks the person to confirm it, so it is never taken as settled.
2. **Look for existing files first**, following `references/brand-context.md` (project root, user local environment,
   central brand directory and the folder its `BRAND-HOME.md` names, then memory, CLAUDE.md and connected knowledge).
   **Where the files go:** the folder of the draft theme the person chooses in Step 1 (question C;
   `references/brand-home.md`): BRAND.md, BRAND-VOICE.md, BRAND-QUESTIONS.md, BRAND-REQUESTS.md and BRAND.html in
   uppercase, and design.md (lowercase, as other docs already refer to it), all at that folder's root. Nothing is
   written until the theme is settled. If the folder already has a `design.md` (any case), it is the visual source:
   don't generate another (Step 4). Files found in the central directory or another folder are moved in only on the
   person's yes (`brand-home.md` section 7). With no draft theme (no Shopify store, no draft yet) or no filesystem (a
   chat), `brand-home.md` section 6 says where they go.
3. **Mode:**
   - **new:** no BRAND.md yet. Full run; it writes BRAND.md, BRAND-VOICE.md and design.md.
   - **add-design:** BRAND.md exists but no design.md does (`design_doc: none`, or the key is missing). Run Step 1's
     sources question, and its draft theme question if the files aren't already in a draft theme's folder (not
     the four setup questions), then Steps 2, 3 (visual part only), 4 (design.md), 5 and 6, then
     set `design_doc: design.md` in BRAND.md, replace its Visual identity with the pointer and summary, add a Visual
     identity row to Sources, bump `revision` and add a Change log row (Mode `add-design`, Sections: Visual identity,
     Sources). Nothing else in BRAND.md changes.
   - **apply-answers:** BRAND.md exists and the client's answers to BRAND-QUESTIONS.md (or the setup questions)
     have arrived. Change only the answered lines, label them `(client, <date>)`, mark each question
     `Answered <date>: <answer> (from <who>)`, bump `revision`, add a Change log row, and re-run Steps 5 to 6.
     A voice line goes in BRAND-VOICE.md: bump that file's `revision` and Change log too, and add a Voice row to
     BRAND.md's Change log so BRAND.md's revision moves with it. A visual answer goes in design.md the same way
     (its own revision and Change log, plus a Visual identity row in BRAND.md's).
     Set `status: approved` with `approved_by` and `approved_on` only when the approver says the file is right.
     Open lines in `BRAND-REQUESTS.md` are not answers: leave them alone unless the client's message confirms one;
     then apply it like an answer and mark the line `done <date>`. Unconfirmed requests can go to the client as
     questions in the next round.
   - **BRAND.md exists and the request is anything else:** don't rewrite it. A change of direction (a rebrand, a
     new name) is a new capture: rename the old file `BRAND-<YYYY-MM-DD>.md` and run **new**. Other change
     requests go to `BRAND-REQUESTS.md`, and are applied in an apply-answers run only once the client confirms
     them. (Verify, refresh and upgrade modes come in a later version.)
   - **split-voice:** BRAND.md exists from before BRAND-VOICE.md did (no `voice_doc` in its front matter, Voice
     written out in full; the scan's `repo.brand_md.voice_doc` is empty) and the client or reviewer asks for the
     voice to be separated. Move, don't rewrite: create BRAND-VOICE.md from `references/voice-template.md` with the
     Voice lines carried over word for word (origin labels with them) and the "Rules that stay in BRAND.md" section
     filled in; replace BRAND.md's Voice with the pointer and the three words; add `voice_doc: BRAND-VOICE.md` to
     the front matter and `(full voice guide: BRAND-VOICE.md)` to the Quick reference line; add a Voice row to
     Sources; bump `revision` and add a Change log row (Mode `split-voice`, Sections: Voice, Quick reference,
     Sources). Confirm every moved line appears unchanged in BRAND-VOICE.md, then run Steps 5 to 6. Nothing is
     researched or reworded.

## Step 1: Ask what to work from and where to save, then the four setup questions

**Sources and the draft theme: always asked, first.** Ask on every new capture (add-design asks A and B, and C only
when the files aren't already in a draft theme's folder), before anything is read, even when the request names a site,
the repo has one, or another skill called you (then relay it to the person). A site that looks like enough is no
reason to skip A and B: a brand book often holds what a site can't (the mission as the brand wrote it, a voice guide,
logo rules, the exact palette) and settles conflicts the site leaves open. C settles where every file this run writes
will live, so nothing is written before it is answered (`references/brand-home.md`).

If a site URL is already known (Step 0), you may start Step 2's scan on it in the background while you ask (in Claude
Code, run it as a background command): a question tool usually waits for the answer, so a scan started after asking
would sit idle. If the answer names a different site, drop that scan and run it again on the right one. Likewise, if
the store is known (the repo's theme config, a connected store), list its themes now (`references/theme-target.md`
section 2) so C can offer them; if they can't be listed, ask for the draft's name or id. Then ask, in one message,
with your environment's question tool if it has one:

> Before I start on **<brand or site>**, what can I work from, and where should the brand files go?
> **A. Does the brand have an existing store or website?** *(If a URL is known:)* I found <url> (<where>): is that
> the right one, and are there others I should read, such as another store, a marketplace page or social profiles?
> *(Otherwise:)* Please send the link or links. "Not yet" is a fine answer.
> **B. Is there an existing brand book I can use?** Brand guidelines, a style or voice guide, a logo or press kit, a
> messaging or pitch deck, a Google Doc or Figma export: anything already written about the brand. Send the file or a
> link, or paste the text. "Not yet" is a fine answer.
> **C. Which draft theme should the brand files be saved in?** They are kept in that theme's folder on your computer,
> next to its code, so later customization and every other skill finds them there. Nothing is sent to your store.
> *(If themes were listed:)* Your draft themes are <name (id)>, <name (id)>: which one? *(If a draft was used before:)*
> Same draft as before, <name>? *(Otherwise:)* Please give the store's .myshopify.com address and the draft theme's
> name, and the folder where its files are (I'll use this folder if it is the theme). "No draft yet" is a fine answer.
>
> And four quick questions:
> 1. **Who are your top 2 or 3 competitors?** Names or websites.
> 2. **Who are 2 or 3 brands you admire that don't compete with you?** Any industry: for tone, look, or how they talk to customers.
> 3. **Who in your company needs to approve things to make sure they're on brand?** Name and role. "Nobody yet" is a fine answer.
> 4. **Is there anything we should never say or claim about your brand or products?** Words, claims or topics. "Nothing" is fine.

(An add-design run asks only A and B, and C only when the files aren't already in a draft theme's folder.) Then act on
the answers to A, B and C:

| Answer | What to do |
|---|---|
| A site or store | It is the site for Step 2. The first is `site` in BRAND.md; others go in `other_domains` or the report |
| A brand book | Read it in Step 2 (`discovery.md` §2b) before judging anything. If it can't be opened (a private link, an unsupported format), say what failed and ask for another form; don't skip it |
| No brand book | Carry on from the site. The report says "no brand book provided" so the reviewer can ask the client again; a book that arrives later goes through `BRAND-REQUESTS.md` (Step 0) |
| No site yet, but a brand book | Skip the scan, set `site: none`, and capture from the book (`discovery.md` §2b) |
| Neither a site nor any document | There is nothing to capture from. Say so, ask for at least one site, document or set of social profiles, and stop until it arrives. Never write BRAND.md from memory |
| A or B left unanswered | Go on with the known site, if any, and put "sources not confirmed" in the report. With no known site, treat it as "Neither" |
| A draft theme (and its folder) | Settle the folder (`brand-home.md` §2); every file this run writes goes there. Remember the theme in `THEME-TARGET.md` and write `BRAND-HOME.md` (§4). If brand files already exist elsewhere, offer once to move them in (§7) |
| No draft yet, not a Shopify store, or C left unanswered | Don't create a theme. Carry on and save in the central brand directory (`brand-home.md` §6), or wait while they duplicate one in Admin if they prefer. The report says "no draft theme yet" |

Questions 1 to 4 are not asked in an add-design run. Unanswered or skipped ones become the first follow-up questions
(they count toward the 4). If the person answers on behalf of the client (an agency kickoff), record who in the Change
log.

## Step 2: Scan the site and read the brand book

With a site, run the scan below. With a brand book, also read it (2b, after the scan). With no site, skip the scan.

```bash
python3 scripts/scrape_site.py <site-url> --out <scratch>/brand-scrape.json --repo <theme-folder>
```

(`python` on Windows, where `python3` usually isn't installed. Omit `--repo` with no theme folder.) It saves every
page it reads as text under `<scratch>/evidence/`, records failures under `errors` instead of stopping, and covers:
story, careers, news, FAQ and contact pages; up to three location or store pages; custom and appointment pages;
financing, loyalty, returns and shipping pages; the terms page; the site's title, description and footer text
(`site-meta-and-footer.txt`, where legal names usually are); claim wording from product descriptions
(`product-claims.txt`); the full catalog on Shopify online stores (a sample elsewhere); colors and fonts; blogs and a
measured sample of posts; social links, structured data, regulated-category signals and disclaimers; and brand docs
already in the repo.

**Pages the reading checklist needs that the scan didn't pick:** run the scan again with `--extra-url <url>` for
each one (repeatable; about a minute), so their text is saved as evidence. Quotes may only come from saved pages.

**If the script can't read the site:** exit code 2 means the home page couldn't be fetched (no network, or the
site refuses scripts with HTTP 401 or 403); exit code 3 means it got a bot check ("verifying your browser") instead
of the page. Sandboxes that block network (Codex's default, ChatGPT, Claude chat): ask once to allow network for
this command. Otherwise read the site with your browser tool if you have one (it gets past most bot checks; never
solve a CAPTCHA or click through a challenge), else your web fetch tool, following `discovery.md` §2. Save each
page you read that way as a text file in the evidence folder, first line `URL: <url>`, so quotes can be checked.
If nothing works and there is no brand book either, stop and say what failed. Never write BRAND.md from memory.

### 2b. Read the brand book

Follow `references/discovery.md` §2b: read each document in full, save a text copy of it in the evidence folder (first
line `FILE: <name or link>`), and take its mission, values, voice, naming, palette, type and claim rules, each
labelled `(from brand book)`. Do this before Step 3, so any disagreement with the site shows up as a conflict.

## Step 3: Read and judge (no more questions)

Read `references/discovery.md` and complete its §2a reading checklist (and §2b, for a brand book). Where the book and
the site disagree, that is a conflict (§3a). Then fill each part of the template:
story in the brand's own words; voice with real examples (for BRAND-VOICE.md); names and brand architecture from every source;
catalog topics and price bands; claim limits for the categories the scan found, with the site's disclaimers
verbatim and the client's "never say" answer first; visual identity (or a pointer to design.md).

**Competitors and inspirations: light research only** (`discovery.md` §6): site, feed, one line and overlap for
each brand the client named, about a minute each. Deep research (pricing, offers, content cadence) is the
competitor-research skill's job; BRAND.md only points to `COMPETITORS.md` (front matter `competitors_doc`), which that skill writes.

## Step 4: Write BRAND.md, BRAND-VOICE.md, design.md and BRAND-QUESTIONS.md

- **BRAND.md:** follow `references/brand-template.md` exactly: same front-matter keys and `##` headings, in
  order. Status `draft`, revision 1. Aim for 150 to 220 lines; every line should earn its place. Its Voice section is
  only the pointer and the three words.
- **BRAND-VOICE.md:** next to BRAND.md, following `references/voice-template.md` exactly. Same status as BRAND.md,
  revision 1, 40 to 70 lines. `voice_doc: BRAND-VOICE.md` in BRAND.md's front matter is what links the two.
- **design.md:** next to BRAND.md, following `references/design-template.md`. Same status as BRAND.md, revision 1.
  **Skip it if a design.md already exists** in the theme folder, the project or the central folder: set `design_doc`
  to it and write Visual identity as a pointer plus a 3 to 5 line summary that agrees with it. Otherwise measure
  first: with a browser tool, read computed values from the live site at 1440 and 390 (headings, body, nav, buttons
  and their hover states, inputs, images, section padding, container width); add the scan's `visual` block and the
  theme's colour and font settings. With no browser tool, use the scan and CSS only, say so in `measured:`, and label
  guesses `(inferred)`. Take a brand book's stated palette, type and logo rules as `(from brand book)` and say in
  `measured:` that they are stated, not measured; where the live site measures differently, record both and ask. With
  no site, everything in design.md is stated, not measured. Set `design_doc: design.md` in BRAND.md, whose Visual
  identity is the pointer plus the summary. Font families named TRIAL or DEMO get a ⚠️ in Assets and a question in
  BRAND-QUESTIONS.md.
- **BRAND-QUESTIONS.md:** follow `references/client-questions.md`. **At most 4 questions for the client**,
  chosen with `discovery.md` §3b; every other open item goes under "Held for later" for the reviewer.

## Step 5: Validate

```bash
python3 scripts/validate_brand.py BRAND.md --evidence <scratch>/evidence --questions BRAND-QUESTIONS.md
```

It checks BRAND.md and, through `voice_doc`, BRAND-VOICE.md. Check design.md by hand: the front-matter keys match
the template, every value is measured or labelled, and BRAND.md's Visual identity summary agrees with it. Exit 0 is required before saving (warnings go in the
report). Fix and re-run on errors. Always pass
`--evidence`: a quote it can't find in the saved pages is unverified, so save that page (`--extra-url`) or drop
the quote, and report any warning that remains.

## Step 6: Client copy

```bash
python3 scripts/brand_html.py BRAND.md --questions BRAND-QUESTIONS.md
```

Writes `BRAND.html` next to BRAND.md: one self-contained page the client can open in any browser, share or print
to PDF. While in draft it opens with the questions for them. It includes the content of BRAND-VOICE.md under Voice,
so the client reads the whole voice in one place. design.md is shared as the file itself (it is a reference for
designers and developers, not for sign-off). Re-run it after every change to BRAND.md or BRAND-VOICE.md.

## Step 7: Link the project to BRAND.md

```bash
python3 scripts/link_brand.py <theme-folder>              # dry run: lists what it would change
python3 scripts/link_brand.py <theme-folder> --apply all  # after the person says yes
```

It adds one short marked pointer to the theme folder's agent files (AGENTS.md for Codex and similar tools, CLAUDE.md
for Claude Code, unless CLAUDE.md already imports AGENTS.md) and to every skill or workflow doc in it that writes
customer-facing words. Show the dry-run list, drop anything that doesn't write copy, and ask once: "Link these N files
to BRAND.md?" Apply only what they approve. It never edits skills installed outside the project, and `--remove` undoes
it exactly. In a Shopify theme repo, root-level files such as AGENTS.md and CLAUDE.md are not part of the theme, so
theme pushes never send them to the store. Where the project lives decides the rest:

| Where you run | BRAND.md lives | Also do |
|---|---|---|
| Claude Code, Codex (a repo) | the draft theme's folder (the repo root when the theme is checked out as a repo) | Suggest committing BRAND.md, BRAND-VOICE.md, design.md and the links (don't commit unless asked; BRAND-QUESTIONS.md and COMPETITORS.md are internal, `brand-home.md` section 3) |
| Cowork (a project with a local folder) | the draft theme's folder (the project's folder when the theme is connected as it) | Ask the person to paste into the project's Instructions: "Brand facts live in BRAND.md in the draft theme's folder (its voice is in BRAND-VOICE.md and its look in design.md, next to it); read them before writing anything customers will see." |
| Claude or ChatGPT project, or a plain chat (no folder) | handed over for download | Ask the person to save BRAND.md, BRAND-VOICE.md and design.md in the root of the draft theme's folder (`brand-home.md` section 6), add them to the project's files, and paste the same instruction line into the project instructions |

## Step 8: Report

Follow `references/report-template.md`: what it worked from (the site, the brand book, or that none was available),
which draft theme and folder the files were saved in (or that there was no draft theme yet), where everything was
saved, the 3 or 4 most useful findings, the questions sent and held, what the agency (not the client) should fix, what
was linked, and the run time. End by offering the competitor-research skill for COMPETITORS.md, which saves next to
BRAND.md.

When another skill called this one, return to it as soon as BRAND.md is validated, with one line on what's still to
confirm and the draft theme and folder you settled.
