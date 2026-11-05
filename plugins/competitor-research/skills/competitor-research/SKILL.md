---
name: competitor-research
description: Deep research on the client's top 3 competitors, named in BRAND.md, written to COMPETITORS.md next to it. Competitors only; inspiration brands are asked and studied by brand-capture. Compares where each competitor operates against the client (shared cities, neighbourhoods, channels or marketplaces), what it sells and at what prices, its pricing model (flat prices, packages, bundles, memberships, subscriptions), offers and referral programs, how often it publishes content and who writes it, and how it positions itself. Ends with concrete openings for the client. Dated research, re-run every few months; never changes BRAND.md. Saved in the folder of the draft theme that holds the brand files, and asks which draft theme when none is remembered; copied to the team's shared copy too when one was chosen. Works for any kind of business, in Claude Code, Cowork, Claude projects, Codex and ChatGPT. Use when the user says "research the competitors", "competitor analysis", "build COMPETITORS.md", "how do we compare", "refresh the competitor research", or when brand-capture offers it after setup.
---

# Competitor research

Turn the client's top 3 competitors (named in BRAND.md) into `COMPETITORS.md`: what each one does, where it
overlaps the client, how it prices and promotes, how it publishes, and what that means for the client. Competitors
only: inspiration brands are asked for and studied by brand-capture, and live in BRAND.md. BRAND.md says who the brand is; COMPETITORS.md says what the market around it looks like this quarter.

```
0. Read BRAND.md, settle the draft theme → 1. Confirm the top 3 and plan → 2. Research each competitor
→ 3. Compare and find openings → 4. Write COMPETITORS.md → 5. Report
```

## How to reply (every message)

These rules apply to every message this skill writes to the person, in Claude or in any other AI app.
They take priority over any other tone guidance in this skill or its reference files.
They cover messages to the person only. Content written for the brand (posts, page copy, product
text) follows the brand's own voice from `BRAND-VOICE.md`.

- **Short and direct.** Start with the answer or the next action. Say only what the person needs to
  know, decide or do next. No long introductions, recaps or repeated warnings. Put long detail in the
  saved file, not in the chat.
- **No technical knowledge assumed, including of Shopify.** Avoid technical terms (for example theme
  files, CLI, API, metafields, JSON, schema, cron). If one is needed, explain it in a few plain words
  the first time.
- **Step-by-step for anything the person must do.** When they need to set up, sign in, click, export or
  install something, give numbered steps, one action per step. Name the exact button or menu, and say
  what they should see when it worked.
- **Simple English.** Short sentences, common words, one idea per sentence. No idioms, figures of
  speech, jokes or slang.
- **Formal and professional.** Polite and neutral. No exclamation marks, emoji or hype words.
- **Not intimidating.** Do not list everything that could go wrong. When something fails, say what
  happened and what to do next.

## Effort (read before starting)

Occasional and high value: run it on the strongest model available, at high effort.

| | 2 competitors | 3 competitors |
|---|---|---|
| Time, start to report | 6 to 10 minutes | 8 to 14 minutes |
| Of which scans (about 1 minute per competitor) | 2 minutes | 3 minutes |
| Web requests | 100 to 180 | 150 to 260 |
| Budget on the strongest model | about USD 1.50 | about USD 2.50 |

Estimated from the AYA run on 2026-10-02 (2 competitors and 2 inspiration brands at the time), with the inspiration
share removed. Cost is an estimate from token counts at API list prices, not a bill. Stop and
tell the person if a run passes 30 minutes or USD 10. Re-run every 3 months, or before a strategy meeting; prices and
offers go stale within weeks.

| File | Read at |
|---|---|
| `references/research-guide.md` | Steps 1 to 3: what to compare for each kind of business, where to find it, how to judge it |
| `references/competitors-template.md` | Step 4: the layout of COMPETITORS.md |
| brand-capture `references/brand-home.md` and `references/theme-target.md` | Steps 0b and 4: asking for the draft theme, finding its folder, moving existing brand files, the optional shared copy (brand-capture is a dependency of this plugin) |

## Rules

- **Top 3 competitors only.** Research the first 3 brands in BRAND.md's Competitors table, in the order listed.
  If it lists more, say in one line which 3 you are using. Never research inspiration brands here: brand-capture
  owns them. Never add or suggest competitors unless the person explicitly asks; if they do, label them `(suggested)`.
- **One question at most.** Ask only when BRAND.md names no competitors (Step 1). Never ask about inspiration brands.
- **BRAND.md is read only.** Facts about the client come from BRAND.md, never re-researched. If BRAND.md is
  missing, stop and offer brand-capture first. If something in it looks wrong, add a line to `BRAND-REQUESTS.md`.
- **Everything is dated and sourced.** Every price, offer and count carries the page URL and the date seen.
  COMPETITORS.md is research, not a source of truth: label inferences `(inferred)`.
- **Summaries, not post lists.** For content, record cadence (posts in the last 90 days), typical length,
  authorship and the topics they cover. Never list individual posts.
- **Never copy.** Quote competitors' wording only to show positioning or claims, briefly.
- **It saves in a draft theme's folder.** COMPETITORS.md goes next to BRAND.md, in the folder of a draft theme the
  person chose, so later customization and every other skill find it with the brand files. Step 0b settles which theme
  before anything is researched. It's written at the folder's root, never inside the theme's own folders and never in
  `assets/` (public), and nothing is pushed to the store.
- **A shared copy is only a copy.** If the person chose one in brand-capture, COMPETITORS.md is added to it after
  it is saved here. The draft theme's folder stays the source of truth, and the local file wins if the two differ.
  This skill never asks for a shared copy itself and never copies BRAND-QUESTIONS.md or BRAND-REQUESTS.md
  (`brand-home.md` section 8).
- **Read only on the web.** Public pages, robots.txt honoured. Never sign in, book, add to cart or submit forms.
  Follow the host repo's device and browser rules.
- **It's for any business.** Compare what matters for the client's kind of business (`research-guide.md` §1); a
  clinic is compared on locations and treatment prices, an online store on catalog, price bands and shipping.

## Step 0: Read BRAND.md

Find it with the lookup order in brand-capture `references/brand-context.md` (project root, user local environment,
central brand directory and the folder its `BRAND-HOME.md` names, then memory and connected knowledge); don't ask
first.

From BRAND.md take: `brand`, `site`, `category`, `markets`, `currency`, `regulated`; Identity (positioning, proof
points, locations or reach); Brand architecture (locations); Catalog (what they sell, price bands, topics);
Competitors (names, sites, feeds, overlap; the first 3). Note its `revision` for the header.
If a COMPETITORS.md already exists, read it: the new run replaces it, and the report says what changed.

## Step 0b: Which draft theme?

COMPETITORS.md is saved in the folder of a draft theme, next to BRAND.md. Follow brand-capture
`references/brand-home.md` (sections 1, 2 and 7) and `references/theme-target.md`:

1. **A draft theme is remembered** (this conversation, `THEME-TARGET.md` next to BRAND.md, or the folder
   `BRAND-HOME.md` names): say one line ("Saving COMPETITORS.md in the draft theme <name>, folder <path>."), check the
   folder still exists, and go on. The person can name another draft at any time.
2. **None is remembered** (BRAND.md was found in the central brand directory or in a folder that isn't a theme's): ask
   once, before researching, which draft theme to save in (drafts only; "no draft yet" is an answer) and the folder
   where its files are. If no local folder exists for the project yet, `brand-home.md` section 2 first asks the
   person to create one. Then offer to copy the existing brand files in unchanged (`brand-home.md` section 7), and save
   COMPETITORS.md next to wherever BRAND.md ends up.
3. **No draft yet, not a Shopify store, or no file system:** `brand-home.md` section 6.

## Step 1: Confirm the top 3 and plan

**The top 3.** Take the first 3 competitors from BRAND.md and name them in one line ("Researching <A>, <B> and <C>.").
If BRAND.md names none, ask once, in plain words:

> **Who are your top 3 competitors?** Names or websites. Fewer is fine.

Use the answer for this run, and add a line to `BRAND-REQUESTS.md` so brand-capture adds them to BRAND.md (BRAND.md
stays read only here). If the person can't name any, stop: this skill doesn't pick competitors on its own unless the
person asks for suggestions.

**The plan.** Pick the client's business type in `research-guide.md` §1 and list the comparison rows that apply. Tell
the person in one line what you'll compare and roughly how long it takes, then start. Ask nothing else beyond the
draft theme in Step 0b.

## Step 2: Research each competitor

For each of the top 3 competitors:

1. **Scan it** if the brand-capture plugin is installed (find its script with
   `find ~/.claude -name scrape_site.py -path '*brand-capture*' 2>/dev/null | head -1`, or use the sibling skills folder):
   ```bash
   python3 <path-to>/scrape_site.py <competitor-site> --out <scratch>/<slug>.json --evidence <scratch>/<slug>-evidence --max-posts 8
   ```
   (`python` on Windows.) Give every brand its own `--evidence` folder: scans that share one overwrite each
   other's files. Exit code 2 (site refuses scripts) or 3 (bot check instead of the page) is common on big brands.
   It returns products and prices (complete on Shopify stores), story, locations, offer and terms pages, blogs
   with post counts and dates, social links and disclaimers, in a minute or two. If the script isn't there, can't
   reach the network, or the site blocks it, read the site with your browser tool (the main fallback: it gets past
   most bot checks; never solve a CAPTCHA or click through a challenge), else your web fetch tool, with the
   checklist in `research-guide.md` §2.
2. **Read** what the scan can't judge: the homepage and main story page for positioning; pricing, membership and
   offers pages; the locations index; two recent posts for length and authorship (`research-guide.md` §2).
3. **Record** each finding with its URL and today's date as you go.

## Step 3: Compare and find openings

Build the side-by-side table, then write the openings: topics, offers, places or channels where the client is
stronger, or where nobody serves the customer well, each tied to evidence (`research-guide.md` §3). Separate
what is measured (a price, a count) from what is judged (`(inferred)`).

## Step 4: Write COMPETITORS.md

Follow `references/competitors-template.md`. Save it in the draft theme's folder, next to BRAND.md (Step 0b), at the
folder's root: never inside the theme's own folders, and never in `assets/`, which is public. If BRAND.md stays
somewhere else (the person said no to moving it), save next to BRAND.md. Aim for 120 to 250 lines. Keep the client's
facts as BRAND.md states them; don't restate BRAND.md sections.

**Shared copy, after it is saved:** read `shared_copy` in `BRAND-HOME.md`. If it is `drive`, `repo` or `both`, add or
update COMPETITORS.md in those places (`brand-home.md` section 8), saying in one line what was updated. If the key is
absent, don't ask: the shared copy is offered by brand-capture, and a person who wants one now can ask for it.

## Step 5: Report

About ten lines: where COMPETITORS.md was saved (the draft theme and its folder), where its shared copy is (or that
none was chosen), the three most useful findings, the openings, anything you couldn't read (blocked pages,
client-rendered prices), the run time and model, and the suggested next review date. If you found something BRAND.md
should hold (a competitor's site moved, a new location of the client's), list it as a BRAND-REQUESTS.md line instead
of changing BRAND.md.
