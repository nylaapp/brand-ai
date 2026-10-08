---
name: competitor-research
description: Deep research on the competitors and inspiration brands a client named in BRAND.md, written to COMPETITORS.md next to it. Compares where each competitor operates against the client (shared cities, neighbourhoods, channels or marketplaces), what it sells and at what prices, its pricing model (flat prices, packages, bundles, memberships, subscriptions), offers and referral programs, how often it publishes content and who writes it, how it positions itself, and what each inspiration brand does well. Ends with concrete openings for the client. Dated research, re-run every few months; never changes BRAND.md. Works for any kind of business, in Claude Code, Cowork, Claude projects, Codex and ChatGPT. Use when the user says "research the competitors", "competitor analysis", "build COMPETITORS.md", "how do we compare", "refresh the competitor research", or when brand-capture offers it after setup.
---

# Competitor research

Turn the client's own list of competitors and inspiration brands (in BRAND.md) into `COMPETITORS.md`: what each one
does, where it overlaps the client, how it prices and promotes, how it publishes, and what that means for the
client. BRAND.md says who the brand is; COMPETITORS.md says what the market around it looks like this quarter.

```
0. Read BRAND.md → 1. Plan the comparison → 2. Research each brand → 3. Compare and find openings
→ 4. Write COMPETITORS.md → 5. Report
```

## Effort (read before starting)

Occasional and high value: run it on the strongest model available, at high effort.

| | 2 competitors + 2 inspirations | 3 competitors + 3 inspirations |
|---|---|---|
| Time, start to report | 8 to 12 minutes | 12 to 20 minutes |
| Of which scans (about 1 minute per brand) | 4 minutes | 6 minutes |
| Web requests | 150 to 250 | 220 to 380 |
| Budget on the strongest model | about USD 2 | about USD 4 |

Measured on AYA (2 competitors, 2 inspirations) on 2026-10-02: about 2 minutes of research and writing on top of
same-day scans, plus 4 page reads. Cost is an estimate from token counts at API list prices, not a bill. Stop and
tell the person if a run passes 30 minutes or USD 10. Re-run every 3 months, or before a strategy meeting; prices and
offers go stale within weeks.

| File | Read at |
|---|---|
| `references/research-guide.md` | Steps 1 to 3: what to compare for each kind of business, where to find it, how to judge it |
| `references/competitors-template.md` | Step 4: the layout of COMPETITORS.md |

## Rules

- **The list comes from BRAND.md.** Research only the brands in its Competitors and Inspiration brands tables.
  Never add or suggest others unless the person explicitly asks; if they do, label them `(suggested)`.
- **BRAND.md is read only.** Facts about the client come from BRAND.md, never re-researched. If BRAND.md is
  missing, stop and offer brand-capture first. If something in it looks wrong, add a line to `BRAND-REQUESTS.md`.
- **Everything is dated and sourced.** Every price, offer and count carries the page URL and the date seen.
  COMPETITORS.md is research, not a source of truth: label inferences `(inferred)`.
- **Summaries, not post lists.** For content, record cadence (posts in the last 90 days), typical length,
  authorship and the topics they cover. Never list individual posts.
- **Never copy.** Quote competitors' wording only to show positioning or claims, briefly. Inspiration notes
  describe patterns to learn from, never text to reuse.
- **Read only on the web.** Public pages, robots.txt honoured. Never sign in, book, add to cart or submit forms.
  Follow the host repo's device and browser rules.
- **It's for any business.** Compare what matters for the client's kind of business (`research-guide.md` §1); a
  clinic is compared on locations and treatment prices, an online store on catalog, price bands and shipping.

## Step 0: Read BRAND.md

Find it with the lookup order in brand-capture `references/brand-context.md` (project root, user local environment, central brand directory, then memory and connected knowledge); don't ask first.

From BRAND.md take: `brand`, `site`, `category`, `markets`, `currency`, `regulated`; Identity (positioning, proof
points, locations or reach); Brand architecture (locations); Catalog (what they sell, price bands, topics);
Competitors and Inspiration brands (names, sites, feeds, overlap). Note its `revision` for the header.
If a COMPETITORS.md already exists, read it: the new run replaces it, and the report says what changed.

## Step 1: Plan the comparison

Pick the client's business type in `research-guide.md` §1 and list the comparison rows that apply. Tell the
person in one line what you'll compare and roughly how long it takes, then start. Ask nothing else.

## Step 2: Research each brand

For each competitor, then each inspiration brand:

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

Inspiration brands get a lighter pass: homepage, one story page, two posts, and the one or two things the client
likely admires (`research-guide.md` §3).

## Step 3: Compare and find openings

Build the side-by-side table, then write the openings: topics, offers, places or channels where the client is
stronger, or where nobody serves the customer well, each tied to evidence (`research-guide.md` §4). Separate
what is measured (a price, a count) from what is judged (`(inferred)`).

## Step 4: Write COMPETITORS.md

Follow `references/competitors-template.md`. Save it in the central brand directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`) next to BRAND.md; if BRAND.md was found in the project root, also keep a copy there only if the person asks. Aim for 120 to 250
lines. Keep the client's facts as BRAND.md states them; don't restate BRAND.md sections.

## Step 5: Report

About ten lines: where COMPETITORS.md was saved, the three most useful findings, the openings, anything you
couldn't read (blocked pages, client-rendered prices), the run time and model, and the suggested next review date.
If you found something BRAND.md should hold (a competitor's site moved, a new location of the client's), list
it as a BRAND-REQUESTS.md line instead of changing BRAND.md.
