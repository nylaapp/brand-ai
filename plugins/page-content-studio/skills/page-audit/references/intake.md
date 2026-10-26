# Intake: context, page, goal

What to settle before auditing or changing a page. This file is the single source for brand
and theme context, page and page-type resolution, and the guided goal questions. `page-audit`
runs all three sections; `page-update`, `page-build` and `page-verify` point here for section 1
and 2 and for the goal check in section 3.

Keep it light: plain language, multiple choice where possible (use the interactive question
tool when available, otherwise a numbered list answerable with a number), no more than four
questions per round, and always allow "not sure" and "something else". If the person doesn't
answer, say which answers you are assuming and continue; never block on a question.

## 1. Brand and theme context

Brand facts (name, spelling, voice, claim limits, inspirations) come from `BRAND.md` and
`BRAND-VOICE.md`, resolved with the lookup order in brand-capture's
`references/brand-context.md` (project root, user local environment, central brand
directory, then memory and connected knowledge). Record each file's path, tier and revision.

- **Found:** this is the source for every brand fact. Never copy a brand name, colour, claim
  or proper noun from memory; read it from the file each time.
- **Not found:** an audit can still run, because it only observes and reports. Say plainly
  that claims can't be checked against brand rules and that new or rewritten copy should wait
  for brand-capture (about 10 to 25 minutes, once per store). A change with no new copy
  (reordering sections, a settings toggle) can proceed without `BRAND.md` if the person
  would rather not wait.

Resolve each file separately and handle a partial set explicitly:

| `BRAND.md` | `BRAND-VOICE.md` | What to do |
|---|---|---|
| found | found | Normal path. |
| found | missing | Structure, settings and existing-copy work proceed. For new or rewritten copy use only the voice facts inside `BRAND.md`, say voice guidance is missing, and offer brand-capture. |
| missing | found | Treat as missing: voice without claim limits and naming rules isn't enough for brand-facing copy. Offer brand-capture. |
| missing | missing | As "Not found" above. |

**Visual spec.** `BRAND.md`'s `design_doc` key points to `design.md` (lowercase, written by
brand-capture): palette, type, spacing, corners and component values. When it exists it is
the source for every visual value and wins over `BRAND.md` on visual values (`BRAND.md` still
wins on names, voice and claims). Values marked `(from site)` are measured; treat
`(inferred)` ones as unconfirmed and flag them. With no `design.md`, fall back to the store
repo's own visual spec or the theme's settings and say which you used. Never invent a hex,
font, size or radius to fill a gap.

**Theme rules.** Theme-engineering rules (where changes go, naming, file ownership, section
conventions, verification gates) live in the store's own repo, usually `AGENTS.md` or
`CLAUDE.md` at its root. Read it fully, and any workflow file it points to. If it's missing,
ask the person's engineering contact where the rules live, or proceed carefully and say which
gates you can't confirm.

**Other evidence files**, if present: `REVIEW-MINING.md` (what customers praise or struggle
with), `COMPETITORS.md`, and an existing `PAGE-AUDIT.md` (see `audit-file.md`).

## 2. Which page, and what type

- **Which page, in their words?** A URL they can paste, or a description ("the homepage",
  "a new page for the Botox treatment"). Resolve it to an actual template; don't assume
  `index` means the homepage, check.
- **What type of page is it?** Homepage, landing page, collection, product, about, contact,
  FAQ or help, policy, location, or service/treatment page. Resolve it from the template and
  the page's job.
- **What kind of business?** Catalog store, appointment or service business, or both. Some
  playbook checks apply to only one.
- **New or existing?** If they're not sure, it is settled by checking the store; never ask
  them to know the difference between a template and a section.
- **Which theme?** Name the exact theme id you will observe. Confirm it is the one meant,
  and that it is a draft or preview rather than the live theme unless they say otherwise.

## 3. Guided goal questions: what is the page for?

Most "improve this page" requests are really "help this page do a job". Find the job first,
then recommend against it. If the person names a specific change with a clear purpose
("swap the hero photo for the new one"), ask only a one-line goal check and move on.

**Round 1: the page's job**

1. **What should this page mainly do for your visitors?**
   - Get people to book or enquire (appointments, consultations, quotes)
   - Sell products (add to cart, buy)
   - Promote an offer, launch or campaign
   - Build trust (reviews, credentials, results, who you are)
   - Inform or answer questions (education, SEO, support)
   - Fix something that looks broken, outdated or off-brand
   - Not sure yet
2. **Who is it mostly for?** New visitors from search or ads / returning customers / people
   on phones from social / not sure. Phone-first changes the advice: say so.
3. **How much change are you open to?** Small tweak to one part / refresh a few sections /
   rebuild the page. This sets the effort ceiling.
4. **What must not change?** Claims or regulated wording, tracked booking or checkout links,
   brand rules, anything they list. These become hard limits.

**Round 2: goal-specific follow-ups.** Ask the follow-up questions for the chosen goal and
the page-type questions in the playbook ("Follow-up questions by page type"). Then use the
matching row's checks as the starting evidence list. The playbook's goal table ("Which checks
matter most for each goal") says which check IDs to weigh first. The "typical
recommendations" are candidates to test against the page, never findings.

| Goal | Follow-up questions | What to check first | Typical recommendations (candidates only) |
|---|---|---|---|
| Book or enquire | Which single action counts (form, call, booking link)? Is there a booking link that analytics already tracks? | Where the first booking action sits on mobile and desktop, clicks to book, whether the booking path matches the tracked one, form or link friction | Move one clear booking action into the first screen, repeat it after proof, shorten the path to book, remove competing off-site actions from the top |
| Sell products | Which products or collection matter most? Is the problem traffic, add-to-cart, or checkout? | Product and collection sections' position, price and review visibility, add-to-cart reachability on mobile, empty or sold-out items showing | Feature best sellers earlier, show ratings and prices on cards, add a clear shop path, reduce sections between hero and products |
| Promote an offer or launch | What is the offer, its dates and terms? Where should it lead? | Offer visible in the first screen, dates and terms present and current, link target works | One lead banner with the offer, one clear destination, expiry and terms, remove stale promos |
| Build trust | What proof exists (reviews, counts, credentials, before/after, press)? Which claims are allowed? | Review count and rating shown, quotes sourced, unsourced numbers, credentials visible, photo proof | Show rating plus count, attribute quotes, source or soften unsourced claims (offer content-fact-check), put real proof near the main action |
| Inform or answer questions | What questions do visitors ask? What should they do after reading? | Heading structure, answer-first copy, FAQ presence, internal links, page speed, search impressions if available | Answer-first intro, scannable headings, FAQ block, next-step link, fix heading levels |
| Fix what looks wrong | What exactly looks wrong, and on which device? Is there a reference for what right looks like? | Reproduce on the render at desktop and mobile, compare against `design.md`, check the section's settings before touching code | Settings-level fix first, then scoped CSS, only then section code; list anything else as "flagged, not done" |
| Not sure yet | Ask Round 1 question 2, then offer the two nearest goals with a one-line example each | Run the full measurement | Rank across all goals and show which goal each candidate serves |

**Using the answers**

- Write them back in two lines ("Goal: book consultations. Audience: phone users from search.
  Open to: refresh a few sections. Must not change: tracked booking links") and get a yes
  before measuring. If there's no answer, state the assumption instead.
- Weigh impact by closeness to the **primary action** for the chosen goal, and tag each
  recommendation **on-goal** or **off-goal**. Off-goal rows are listed last as "worth
  knowing", never ranked above on-goal ones.
- Hard limits from question 4 override every recommendation: if a candidate would break one,
  say so in the row instead of dropping it silently.
- If the answers conflict with the evidence (they say "sell products" but the page has no
  product section), say so plainly and ask which to follow.
- Keep the answers; they go in section 1 of `PAGE-AUDIT.md` and in the QA log's `goal:` line.
