# BRAND.md template (schema 1.1)

Copy this layout exactly. Other skills and `scripts/validate_brand.py` find information by these front-matter keys
and `##` headings, so keep every key and every heading, in this order, even when a section is short. Replace each
`<…>` with content and delete the guidance in *italics*.

**Voice lives in its own file.** BRAND.md's **Voice** section is only a pointer plus the three words; the detail
(how it sounds, signature phrases, do / don't pairs, words to avoid) goes in `BRAND-VOICE.md` next to BRAND.md, laid
out as in `voice-template.md`. Terminology and Claim limits stay here, because they are naming and compliance rules.

**Origin labels** (on any line that isn't plainly sourced): `(from site)`, `(repo)`, `(client)`, `(inferred)`,
`(suggested)`. A line labelled `(client)` was confirmed by the customer and must never be overwritten by a scan.

**Unknowns** use one form only, with a stable id that also appears in `BRAND-QUESTIONS.md`:
`[[CLIENT TO CONFIRM: Q-07 | the question the client must answer]]`. Never write a bare `[[CLIENT TO CONFIRM]]`.

**Budget:** aim for 150 to 220 lines. The validator warns above 220 lines or 3,500 words and fails above 300 lines
or 5,000 words. Deep research, site fixes and copied procedures never go in this file (see "What stays out").

The front matter is flat `key: value` lines (no nesting, no quotes) so any tool can read it without a YAML library.
Lists are comma-separated. Dates are `YYYY-MM-DD`.

---

```markdown
---
brand_md_schema: 1.1
brand: <the default name to use in copy, exactly as the brand writes it>
legal_name: <legal entity if published, else [[CLIENT TO CONFIRM: Q-01 | legal entity name]]>
parent_brand: <parent company or group, or blank>
site: <https://public-site-that-was-scanned>
store: <shop.myshopify.com, or blank>
other_domains: <booking or checkout domains that belong to the brand, comma-separated, or blank>
platform: <shopify (online store) | shopify (headless) | wordpress | ... from the scan>
category: <plain words, e.g. medical spa group and skincare retail>
markets: <ISO country codes, e.g. US>
language: <e.g. en-US>
currency: <e.g. USD>
regulated: <no | yes: <categories>>
design_doc: <design.md | none>
voice_doc: BRAND-VOICE.md
competitors_doc: COMPETITORS.md
search_console_property: <property, or blank>
brand_approver: <name and role from setup question 3, or [[CLIENT TO CONFIRM: Q-.. | who approves things to make sure they're on brand]]>
status: <draft | approved>
revision: <1, 2, 3 ... +1 on every write>
approved_by: <name and role of the client approver, blank while draft>
approved_on: <YYYY-MM-DD, blank while draft>
captured: <YYYY-MM-DD of the first capture>
last_updated: <YYYY-MM-DD of the latest write>
captured_by: brand-capture 1.2.0
---

# <Brand> brand file

> **Source of truth for <Brand>'s brand facts.** Every skill and agent reads this file instead of asking about the
> brand or re-researching it, and answers questions about the brand from it. Only the brand-capture skill writes it,
> and only when the customer asks (see Change log). To request a change, or to report something this file doesn't
> cover, add a line to `BRAND-REQUESTS.md`; don't edit this file. Live data (prices, stock, rankings, competitors'
> latest posts) is always checked fresh. Status `draft` means facts marked (inferred) or pending are assumptions
> until the client approves them.

## Quick reference
*At most 15 lines. The summary an agent reads first; every line must agree with the sections below.*
- **We are:** <one-liner>
- **Call us:** <default name>; see Brand architecture for other names
- **Sounds like:** <three words> (full voice guide: BRAND-VOICE.md)
- **Never say:** <the 3 to 5 most important banned claims or words; the client's own answers first>
- **On-brand approver:** <brand_approver>
- **Regulated:** <no | yes: categories; approved disclaimers in Claim limits>
- **Visual system:** <design.md, or "see Visual identity">
- **Open items:** <n pending, ids Q-..>

## Identity
- **One-liner:** <Brand> is a <what> that <does what> for <whom>.
- **Tagline:** "<verbatim>" (from site)
- **Positioning:** <1 to 2 sentences, quoting the site where possible>
- **What sets us apart:** <2 to 4 bullets, each traceable to a source>
- **Proof points:** <years, customers served, awards, press; each with its source URL; conflicting numbers stay out
  until confirmed>
- **Locations / reach:** <count and regions; the per-location names are in Brand architecture>

## Brand architecture
*Every name the business trades under, and when to use each. One BRAND.md per client storefront; sub-brands live here.*

| Name | Type | Use it for | Don't use it for | Status |
|---|---|---|---|---|
| <AYA Skin> | <parent company> | <corporate news, careers> | <consumer copy> | <(from site)> |

**Locations** *(only for multi-location businesses)*

| Location | Name used in copy | SEO business name | Region | Source |
|---|---|---|---|---|
| <Buckhead> | <AYA Medical Spa Buckhead> | <AYA Medical Spa Buckhead> | <Atlanta> | <url or repo file> |

## Story
- **Founding idea:** <why the brand exists, in its own words, quoted with source>
- **Mission:** "<verbatim>" (<url>)
- **Values:** <bulleted, verbatim where the site states them>
- **People:** <founders or leaders named publicly, with role; blank if none are named>

## Audience
*(inferred unless the site or client states it)*
- **Primary customers:** <who>
- **What they want / their problems:** <...>
- **What they worry about or ask:** <from FAQ, reviews shown on site, post topics>

## Catalog
- **What they sell:** <categories, collections, services>
- **Size and prices:** <n products; price range and median; per main type; "check live prices before quoting">
- **Hero products:** <3 to 6, with URLs>
- **Third-party brands stocked:** <if any>
- **Topics the brand can credibly own:** <5 to 12 topic clusters, used for topic-fit checks>

## Voice
*A pointer, at most 8 lines (the validator fails longer). The detail goes in BRAND-VOICE.md.*
Full specification: BRAND-VOICE.md (it wins on any question of tone; Terminology and Claim limits below still win on names and claims). Summary that agrees with it:
- **In three words:** <adjective, adjective, adjective>
- **In BRAND-VOICE.md:** how it sounds, signature phrases, do / don't pairs, words and habits to avoid

## Terminology
| Use | Instead of | Note |
|---|---|---|
| <wrinkle relaxers> | <Botox (as a generic word)> | <Botox® is a trademark; name the product only when it is the product> |
| <Beauty Bank®> | <Beauty Bank> | <registered mark, keep ®> |

## Visual identity
*Brand-capture writes design.md next to this file, so normally: "Full specification: design.md (it wins on any visual
value)." plus a 3 to 5 line summary that agrees with it (palette in one line, the type pairing, the rounding rule,
the imagery rule). Only when design.md could not be made, list:*
- **Palette:** <hex, role> list
- **Typography:** <family, role> list; flag TRIAL licences
- **Imagery:** <photo style, subjects, treatment>
- **Logo:** <URL or repo path>

## Blog
- **Blogs:** <handle or path, article count> list; default blog for new posts: <handle>
- **Rhythm:** <newest post date; rough posting frequency. Never list individual posts here>
- **Typical post:** <word range of the body (not counting the disclaimer); headings; images; byline; tags; CTA>
- **Byline:** <default author line>
- **Standard disclaimer:** see Claim limits → Required disclaimers (one approved text, never two copies)
- **Procedures:** <name the repo skill or workflow that governs publishing, e.g. `aya-add-blog-post`; do not copy its
  rules here>

## Claim limits
- **Regulated category:** <none | which, and why>
- **Approved claims:** *claims the client approved, with source*
  - "<claim>" (client, <date>) or (from site, pending Q-..)
- **Never say (client):** <the client's answer to setup question 4, verbatim, or "nothing named">
- **Not allowed:** <absolutes, superlatives, unsupported results, vendor claims not to reuse>
- **Required disclaimers:** <verbatim approved text or "pending Q-.."; say where each one is used>
- **Rules:** <do / don't lines for the category; only the categories the scan found>
- **Sign-off:** <brand_approver; plus who signs off regulated claims, only if the brand is regulated and it's
  someone else>

## Competitors
*The client's top 2 or 3, as named. Light research only: site, feed, overlap, one line each.*

| Brand | Website | Blog feed | Overlap | Notes | Source |
|---|---|---|---|---|---|
| <name> | <url> | <feed or blank> | <shared markets, locations or marketplaces> | <one line> | <client / suggested> |

- **Where we stand:** <2 to 4 lines on how the brand differs; no deep benchmark here>
- **Deep research:** COMPETITORS.md, written by the competitor-research skill (dated; run it if the file is missing)

## Inspiration brands
*The client's 2 or 3 non-competitive brands they admire, any industry.*

| Brand | Website | What to learn (style only, never copy) | Source |
|---|---|---|---|
| <name> | <url> | <tone, layout, storytelling> | <client / suggested> |

## Channels
- **Social:** <platform: url> list
- **Search Console property:** <value, or blank>

## Author
- **Default byline:** <the byline on existing posts; if none, the brand name>
- **Bio:** <from site, or "none published">

## Sources
| Section | Source | Fingerprint | Last checked |
|---|---|---|---|
| Identity, Story | <urls> | <first 8 chars of sha256 per page> | <YYYY-MM-DD> |
| Voice (detail in BRAND-VOICE.md) | <urls read for voice> | <first 8 chars of sha256 per page> | <YYYY-MM-DD> |

## Change log
| Rev | Date | Mode | Requested by | Sections | Summary |
|---|---|---|---|---|---|
| 1 | <YYYY-MM-DD> | new | <client name or "agency for client", with reference> | all | <first capture, including BRAND-VOICE.md> |
```

Any later change to BRAND-VOICE.md also adds a row here (Sections: Voice) and raises `revision`, so the one revision
number other skills cite still moves whenever the voice does.

## What stays out of BRAND.md

| Content | Where it goes instead |
|---|---|
| Problems on the client's site (wrong addresses, outdated pages, inconsistent numbers) | The run report and `BRAND-QUESTIONS.md`; BRAND.md keeps only the confirmed value |
| Procedures from the client repo (markup rules, publishing steps) | Stay in the repo skill or workflow; BRAND.md names it under Blog → Procedures |
| Deep competitor research, pricing comparisons, content benchmarks | `COMPETITORS.md`, written by the competitor-research skill (dated research, re-run more often than BRAND.md) |
| Lists of blog posts, the brand's or competitors' | Nowhere: skills read the live blog or feed when they need posts |
| Live data (prices, stock, rankings, competitors' latest posts) | Checked fresh by the skill that needs it |
| Voice detail: how it sounds, signature phrases, do / don't pairs, words to avoid | `BRAND-VOICE.md` (layout in `voice-template.md`); BRAND.md keeps only the pointer and the three words |
| Follow-up questions and the client's answers | `BRAND-QUESTIONS.md`; BRAND.md keeps only the answered value, labelled `(client)` |
| Change requests from skills or people | `BRAND-REQUESTS.md` (append-only) |
