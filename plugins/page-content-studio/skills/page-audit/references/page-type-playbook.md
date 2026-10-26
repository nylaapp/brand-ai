# Page-type playbook

What each kind of ecommerce page is for, what a good one contains, and the checks the skill
uses to say where a page falls short. Load the section for the page's type (resolved in `intake.md`) and the
"Every page" checks. Used by `page-audit` (gap analysis) and by `page-build` when
planning a new page.

**Evidence grades.** Every check carries one. Never present a B or H check as research.

| Grade | Meaning | How to word it |
|---|---|---|
| **A** | Published research or a standard: Baymard Institute, Nielsen Norman Group (NN/g), Google (web.dev), W3C WCAG | "Research shows..." and name the source |
| **B** | Practitioner or vendor guidance. Plausible and widely repeated, but no controlled study found | "Common practice..." and say it is unverified |
| **H** | House heuristic from audits of real pages. No external source | "A rule of thumb we use..." |

Numbers in this file are what the cited source reported at the time; the survey year is
given where known. Quote them with their source and date, never as universal facts.

**Status values** for every check: **Pass**, **Partial**, **Missing**, **Can't tell**
(couldn't observe it). "Can't tell" is never a shortfall.

## How to run a gap analysis

1. Resolve the page type and the business type (catalog store, appointment/service
   business, or both). Some checks only apply to one (marked).
2. Observe the real rendered page at desktop and mobile; mark each check's status from what
   you saw, with the number, quote or position that supports it.
3. A shortfall is a check marked Missing or Partial. Rank shortfalls by: closeness to the
   page's primary action and the goal from the intake questions, then evidence grade (A before B before H),
   then effort. List at most about five; park the rest as "also noticed".
4. Label each row **finding** (observed, with an A-grade check or a measured number) or
   **suggestion** (B/H-grade, or inferred). Hard limits from the intake questions override any fix.
5. A page can pass every check and still underperform; the checklist finds common
   problems, it does not prove impact. Say so, and pair with analytics when available.

Gap report row format:

| # | Check | Status | What was observed | Why it matters (source, grade) | Fix | Effort | On-goal? |
|---|---|---|---|---|---|---|---|

## Every page

| ID | Check | How to verify | Grade |
|---|---|---|---|
| U1 | The first screen says what this is, who it is for and what to do next | Read the first viewport on desktop and mobile | A (NN/g: one-sentence statement of what the company does) |
| U2 | One primary action is easy to spot; each clickable element is one clear hit area with an obvious destination | List links and buttons in the first two screens; compare label to target | A (Baymard homepage study, 2021: 43% of sites unclear) |
| U3 | Upfront disclosure: contact details, prices and fees, shipping and returns are visible, not buried | Look for them from this page without a form or sign-up | A (NN/g trustworthiness factors; Baymard checkout survey, updated 2025: extra costs 40%, total cost not visible 12%, return policy 13% of abandoners) |
| U4 | Real, in-context photography rather than generic stock art | Read alt text and look at the images; flag generic subjects | A (NN/g, Baymard) |
| U5 | No overlay or pop-up covers the first screen or the main button | Load fresh on mobile and desktop; note any modal, cookie or promo overlay and what it covers | A (Baymard: users often mistake pop-ups for spam) |
| U6 | Speed: LCP 2.5 s or less, INP 200 ms or less, CLS 0.1 or less, judged at the 75th percentile, mobile and desktop separately | PageSpeed / field data; if unavailable, say can't tell | A (Google web.dev) |
| U7 | Accessibility basics: one h1, no skipped heading levels, alt text, contrast, keyboard use; pointer targets at least 24x24 CSS px unless spacing or inline exceptions apply | DOM check plus `theme check`; targets by measurement | A (WCAG 2.2 SC 2.5.8, level AA). Larger targets (44-48 px) are common advice: B |
| U8 | Mobile parity: the same primary action is reachable in the first screens; no auto-rotating carousel on mobile | Measure positions at 375 px; check carousel autoplay | A (Baymard) |
| U9 | Independent proof exists and matches: third-party reviews and listings agree with the page | Compare claims with review sites | A (NN/g: users cross-check outside sources) |
| U10 | Claims that are regulated or numeric (results, "award-winning", patient counts, "proven") have a source on the page or in the brand files | Read copy against `BRAND.md`; run content-fact-check | H (compliance; for health and wellness content treat as a must-check) |
| U11 | No dead space: no full-screen block with neither copy nor an action between sections | Section heights from the inventory | H |
| U12 | Tracked links and tagging are unchanged by any edit | Compare booking and checkout links before and after | H (check the store repo's analytics rules) |

## Homepage

**Purpose.** The front door and anchor: tell new and returning visitors what the business
offers and send them to the right next step. Many visitors land elsewhere first, so it must
also orient someone arriving from search or social. (Baymard; NN/g)

**Primary action.** Catalog store: start browsing (category, search, best sellers).
Appointment business: book or enquire. Name it from the intake goal.

| ID | Check | Applies | Grade |
|---|---|---|---|
| HP1 | A one-sentence statement of what the business does or sells in the first screen | all | A (NN/g) |
| HP2 | Clear starting points for the one to four main tasks visitors come to do | all | A (NN/g) |
| HP3 | Breadth is visible: for catalogs, at least about 40% of product types are shown or linked; popular subcategories are promoted directly | catalog | A (Baymard homepage study, 2021; 6% of sites fell short, 62% did not help reach a specific category) |
| HP3s | For service businesses: each main service line is reachable from the homepage in one click | service | B |
| HP4 | Search is prominent | catalog | A (Baymard: 22% of sites not prominent) |
| HP5 | Carousels, if any, rotate slowly, pause on hover and stop after interaction; static sections are often as good | all | A (Baymard: about 36% of sites use one, about 75% of those wrongly) |
| HP6 | Promotions are restrained: they must not overwhelm category content, and offers do not compete above the fold | all | A (Baymard: ad-like content hurt 59% of sites). Competing offers: B |
| HP7 | Original photography and design, not template placeholders | all | A (Baymard: 19% lacked it) |
| HP8 | Best or newest real items are shown (best sellers, new arrivals, featured treatments) | all | A (NN/g) |
| HP9 | "About" and corporate information are in one clearly labelled place | all | A (NN/g) |
| HP10 | Proof sits near the main action: rating and count, credentials, real reviews | all | B for placement; A that third-party proof matters (NN/g) |
| HP11 | Offer terms and dates on the page, or one tap away, and current | promo | A (NN/g upfront disclosure) |
| HP12 | Same primary action label and destination across repeated buttons; avoid six wordings for one destination | all | H |
| HP13 | The primary action is in the first screen on mobile, not only in the header | all | B |

**Typical fixes by effort.** S: reorder sections, change a button link or label,
demote a second h1, set an overlay delay. M: add a proof row, a service or category grid,
rework the hero. L: new section type, new page structure.

## Landing page (campaign, offer, ad destination)

**Purpose.** One job for one audience, usually arriving from an ad, email or social post.
**Primary action.** One, repeated if the page is long.

Research note: no controlled studies were found for landing pages; most guidance is
practitioner opinion (B). Treat conversion lift figures you see elsewhere as unverified.

| ID | Check | Grade |
|---|---|---|
| LP1 | The headline matches the promise that brought the visitor (ad or link text) | B |
| LP2 | One primary action, repeated rather than competing; distracting navigation trimmed | B |
| LP3 | Headline, benefit and the action are in the first screen | B |
| LP4 | Proof near the action: rating, testimonial, credentials, press | B (A that proof from independent sources is trusted more: NN/g) |
| LP5 | Offer terms, price, dates and exclusions are visible and current; expired offers removed | A (NN/g upfront disclosure) |
| LP6 | Forms ask only what is needed (3 to 5 fields is the NN/g guideline for contact forms) | A |
| LP7 | Loads fast on mobile (U6) and has no blocking overlay (U5) | A |
| LP8 | Every claim has a source or is softened (U10) | H |

## Collection page (category or product listing)

**Purpose.** Help a shopper narrow a set to the right few products. Shopify calls the
filterable grid a collection page; Baymard calls it a product listing page.
**Primary action.** Open a product or add to cart. Evidence: Baymard (Aug 2026 article; 80%
of tested sites had serious product-list issues).

| ID | Check | Grade |
|---|---|---|
| CP1 | Filters show result counts, allow multi-select within a group, and include category-specific attributes | A |
| CP2 | Applied filters appear as removable chips (28% of sites don't) | A |
| CP3 | Mobile uses a sticky filter button that opens a drawer | A |
| CP4 | Cards show price and key attributes so shoppers can decide without opening the page; every item has a thumbnail | A |
| CP5 | Variants such as colours are consolidated into one card with swatches | A |
| CP6 | "Load more" is preferred to endless scroll; returning from a product restores the position | A |
| CP7 | Sort is available and defaults sensibly | B (no evidence found) |
| CP8 | Empty or sold-out items are not given prime positions | H |

## Product page

**Purpose.** Give a buyer enough confidence to add to cart: what it is, what it looks like,
what it costs in total, when it arrives, and what happens if it is wrong.
**Primary action.** Add to cart. Evidence: Baymard's product-page research (110+ guidelines;
about half of 344 benchmarked sites rated mediocre or worse). Most detail is paywalled, so
rows below are the topics Baymard covers plus widely repeated practice.

| ID | Check | Grade |
|---|---|---|
| PD1 | Multiple image types (context, detail, scale) with a usable gallery and zoom | A (topic); counts: B |
| PD2 | Price, variants, quantity and the add-to-cart button sit together and are clear, including out-of-stock states | A (topic) |
| PD3 | Shipping cost, delivery estimate and returns are visible near the buy section; the true total is not a surprise later | A (Baymard checkout survey: extra costs 40%, slow delivery 20%, return policy 13%) |
| PD4 | Reviews with a rating summary and filtering; Q&A if buyers ask questions | A (topic); lift figures: B |
| PD5 | Description and specifications are scannable, in plain language | A (topic) |
| PD6 | Sticky add-to-cart on mobile | B (lift figures reported by vendors are unsourced) |
| PD7 | Cross-sells are relevant and do not bury the main action | A (topic) |

## About page

**Purpose.** Let a sceptical visitor judge whether this business is credible. NN/g found
visitors use it to check purpose, values, history, location and how to make contact.
**Primary action.** Move on with more confidence: browse, book, or contact.

| ID | Check | Grade |
|---|---|---|
| AB1 | A clear explanation of what the business does and why it exists, in the first screen | A (NN/g) |
| AB2 | Concrete facts rather than hollow superlatives (years, locations, credentials, numbers with sources) | A (NN/g) |
| AB3 | Real people: named team or founders, real photos, credentials where relevant | A (NN/g: real photos of people help); for clinics, licence and training stated: B |
| AB4 | Mission, values and history are present and specific | A (NN/g) |
| AB5 | Testimonials are balanced and attributed, and match what third-party sites say | A (NN/g) |
| AB6 | Location and contact details are on or one click from the page | A (NN/g) |
| AB7 | A next step that fits the goal (book, shop, contact), without a wall of identical buttons | B |
| AB8 | Superlative or regulated claims have a source (U10) | H |

## Contact page

**Purpose.** Make it easy and low-risk to reach a person. **Primary action.** Send a
message or pick a contact method. Evidence: NN/g contact-page guidelines; Shopify guidance.

| ID | Check | Grade |
|---|---|---|
| CT1 | A phone number and email are shown; a form is offered alongside, not instead | A (NN/g) |
| CT2 | The page is linked from the main navigation or footer on every page and found within seconds | A (NN/g, Shopify) |
| CT3 | Forms stay short (3 to 5 fields), need no account, and use the right input types on mobile | A |
| CT4 | Phone numbers are tappable on mobile; hours and address (with map and parking for physical sites) are shown | A (NN/g address; Shopify) |
| CT5 | Availability and expected response time are stated per channel, and a confirmation follows submission | A (NN/g, Shopify) |
| CT6 | Chat is an option, never the only method; social channels shown only if staffed | A (NN/g) |
| CT7 | A link to FAQs or a help centre for quick answers | B |
| CT8 | Every listed channel actually works (test form, link, phone tap) | H |

## FAQ and help pages

**Purpose.** Answer the questions that block a decision or reduce support requests.
Research note: NN/g and Baymard material was not retrievable for this type; guidance below
is practitioner opinion (B).

| ID | Check | Grade |
|---|---|---|
| FQ1 | The most decision-critical answers (shipping, returns, pricing) also appear where shoppers expect them, not only in an FAQ | B (supported by NN/g upfront disclosure: A) |
| FQ2 | Questions are grouped by topic, closely related ones merged, answers lead with the answer | B |
| FQ3 | Answers link onward to the product, booking or policy page | B |
| FQ4 | The FAQ is reachable from the main navigation or footer | B |

## Policy pages (shipping, returns, privacy, terms)

**Purpose.** Remove fear of a bad outcome. **Primary action.** None; they must be findable
and understandable. Evidence: NN/g upfront disclosure; Baymard checkout survey.

| ID | Check | Grade |
|---|---|---|
| PL1 | Shipping and return policies are linked from product, cart and footer | A |
| PL2 | Plain-language summary first, details after; cost and timing stated | A |
| PL3 | Dates, prices and promotion terms in policy text are current | H |

## Location page (businesses with physical sites)

**Purpose.** Convert a local searcher into a visit or booking. Practitioner guidance (B).

| ID | Check | Grade |
|---|---|---|
| LC1 | The booking action for this location is in the first screen | B |
| LC2 | Address, hours, phone, map, parking and nearby area are present and correct | A for address and hours (NN/g, Shopify); parking and local detail: B |
| LC3 | Content is specific to this site, not duplicated across locations | B |
| LC4 | Local proof: reviews for this site, team at this site | B |
| LC5 | Booking takes about three clicks or fewer from the page | B |

## Service or treatment page (appointment businesses)

**Purpose.** Explain one service well enough to book it. Practitioner guidance (B); the
claim checks are compliance, not marketing.

| ID | Check | Grade |
|---|---|---|
| SV1 | One page per service, with what it is, who it is for, what to expect, downtime and price or range if possible | B |
| SV2 | Provider names and credentials stated plainly, linked to the services they perform | B |
| SV3 | Results imagery uses consented real cases with accurate alt text | B; consent and claims: H, treat as must-check |
| SV4 | Questions answered on the page; booking action repeated after proof | B |
| SV5 | Medical or result claims have a source or are softened (U10) | H |

## Cart (when a theme controls it)

Evidence: Baymard checkout survey. CA1: total cost including shipping and tax is visible
before checkout (A). CA2: no account required (18% of abandoners cited it) (A). CA3: the
checkout form is short; Baymard's ideal is about 12 to 14 form elements (A).

## Which checks matter most for each goal

From the intake goal, weigh these checks first when ranking shortfalls. Other shortfalls
are still reported, tagged off-goal, and listed last.

| Goal | Check IDs to weigh first |
|---|---|
| Get bookings or enquiries | U1, U2, U5, U8, U12, HP2, HP10, HP12, HP13, LC1, LC5, SV2, SV4, CT1 to CT5 |
| Sell products | U3, HP3, HP4, HP8, CP1 to CP6, PD1 to PD5, CA1 to CA3, PL1 |
| Promote an offer or launch | U3, U5, HP6, HP11, HP12, LP1 to LP5 |
| Build trust | U4, U9, U10, HP10, AB1 to AB6, SV2, SV3, U3 |
| Inform or answer questions | U1, U6, U7, FQ1 to FQ4, PL1 to PL2 |
| Fix something broken or outdated | The checks that match the described problem, plus U7 and U11 |

## Follow-up questions by page type (intake round 2)

Ask two or three, as multiple choice with "not sure". The answers decide which checks
apply and which fixes are safe.

| Page type | Ask |
|---|---|
| Homepage | The one action that counts most (name its link). Which offers are active right now, and which one leads? Catalog, service, or both? |
| Landing page | Where does the traffic come from, and what does that ad or link promise? Offer dates and terms? Which single action ends the page? |
| Collection | Which filters do shoppers use most? Default sort? Are sold-out items hidden? |
| Product | Shipping cost and delivery estimate, and the return policy, in facts the page can state. Which reviews are real and linkable? |
| About | Who can be named, and which credentials can be shown? Which claims have a source? Is there real photography of people? |
| Contact | Which channels are staffed, their hours, and the real response time? Is there a phone number to show? |
| FAQ or help | Which questions come up most often, and from which source? Where do shoppers expect the answer? |
| Location | Address, hours, parking, local team, and the booking link for this site |
| Service or treatment | Provider names and credentials, price or range, downtime, and which result claims are allowed |

## Where each fix lives

A shortfall is reported even when this theme cannot fix it. Tag each row with the owner so
the Site Editor knows who acts; only theme rows can be picked for editing here.

| Owner | Examples | What the skill does |
|---|---|---|
| This theme (templates, sections, CSS) | Section order, button link or label in a section setting, heading level, a new section | Can plan and edit on the draft theme |
| Store admin content | Pages, products, navigation menus, metafields, policies | Point to the exact place in admin and the wording to change; do not edit unless the person asks |
| Store settings | Consent banner behaviour, checkout, taxes and shipping, analytics | Report with the measured effect; the person or their admin changes it |
| Third-party app or script | Pop-ups, review widgets, chat, booking widgets | Report with what it covers or breaks; the app's owner changes it |
| Off-site destination | An offer page, booking site or partner page on another domain | Report what was observed (status, dates, terms); the owner of that site changes it |

## Typical fixes for common shortfalls

Candidates only; confirm each against the observed page and the limits from intake.

| Shortfall | Typical fix | Usual effort |
|---|---|---|
| U1 / HP1: first screen doesn't say what the business does | Add one plain sentence to the hero eyebrow or subheading; needs brand-approved wording | S to M |
| U2 / HP13: the primary action isn't in the first screen | Move the existing booking or buy section up, or give the hero a second button to the existing link | S (reorder) to M |
| U5: an overlay covers the first screen or main button | Delay or shrink the overlay, or reposition it; usually a store setting or app | S, other owner |
| U7: second h1, skipped heading levels | Change the section's heading-level setting | S |
| U7: small tap targets | Add padding with matching negative margin so layout holds | S |
| U10: unsourced numbers or superlatives | Source them, soften them, or remove them; run content-fact-check first | S |
| U11: dead full-screen band | Remove it from the section list, add an action to it, or replace its image | S to M |
| HP6: two offers compete above the fold | Decide which leads; the other moves lower or becomes secondary | S, needs a business decision |
| HP10: proof sits far from the action | Move a rating, count or short quote next to the main button | S to M |
| HP11 / LP5: offer terms missing or stale | Add a visible terms link and correct or remove stale dates, including on the destination page | S, often another owner |
| HP12: many labels for one destination | Standardise on the tracked wording already in use | S, check analytics rules first |
| AB3: no named people | New team section with real names, photos and credentials from the business | M, needs content |
| CP2 / CP3: no applied-filter chips or mobile filter button | Theme filter settings or a small section change | M |
| CT5: no stated response time | Add one line near the form | S |

## Sources

- Baymard Institute, homepage UX benchmark (2021): https://baymard.com/blog/ecommerce-homepage-ux
- Baymard Institute, cart abandonment reasons (updated 2025): https://baymard.com/lists/cart-abandonment-rate
- Baymard Institute, product listing pages (Aug 2026): https://baymard.com/blog/product-listing-page-plp-ux
- Baymard Institute, product page research topics: https://baymard.com/product-page
- NN/g, top 10 homepage guidelines: https://www.nngroup.com/articles/top-ten-guidelines-for-homepage-usability/
- NN/g, contact-us page guidelines: https://www.nngroup.com/articles/contact-us-pages/
- NN/g, trustworthiness in web design: https://www.nngroup.com/articles/trustworthy-design/
- NN/g, About Us information research: https://www.nngroup.com/articles/about-us-information-on-websites/
- Shopify, contact us page guidance: https://www.shopify.com/blog/contact-us-page
- Google web.dev, Core Web Vitals: https://web.dev/articles/vitals
- W3C, WCAG 2.2 SC 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- Grade B material (landing page, FAQ, med spa, mobile conversion tactics) came from
  practitioner and vendor blogs found in October 2026 searches; none is cited as research.
  Re-verify before quoting any figure from them.

Refresh this file every six months or when a source updates; record the date in the commit.
