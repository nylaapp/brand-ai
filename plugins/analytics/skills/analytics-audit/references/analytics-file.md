# ANALYTICS.md: the shared client file

Every analytics skill in this plugin reads and writes one file per client site, `ANALYTICS.md`. It is the memory between sessions: what the business counts as a conversion, what is installed where, what the site must keep stable for tracking to work, what is broken, what was changed and how it was tested. A new session starts by reading it instead of re-auditing from scratch.

The blank layout is in `analytics-template.md`. This page holds the rules.

## 1. Finding it

Pick the client slug the same way the brand files do (lowercase store or brand handle, for example `acme-co`). Then look, in order, and stop at the first confirmed match:

| # | Where | Names accepted |
|---|---|---|
| 1 | Project root and subfolders up to three levels | `ANALYTICS.md`; legacy `ANALYTICS_GUARDRAILS.md` |
| 2 | `~/` and `~/.claude/` | `<slug>/ANALYTICS.md`, `ANALYTICS-<slug>.md` |
| 3 | Central brand directory | `$BRAND_AI_HOME/brands/<slug>/ANALYTICS.md` (default `~/.brand-ai/brands/<slug>/`), next to `BRAND.md` |

- **Confirm the match.** Front matter `site` (or `brand`) must match the site you are working on. A file for another site counts as missing. Two matches at the same level: stop and list them.
- **Legacy name.** If only `ANALYTICS_GUARDRAILS.md` exists, use it as the client file and say so in one line. Do not rename it; other project instructions may point at it. Add missing sections to it rather than creating a second file.
- **Nothing found:** create `ANALYTICS.md` from the template. In a code repo for the site, put it in the project root. Otherwise put it in the central brand directory. Tell the person the path.
- **Brand facts** (business type, markets, regulated category) come from `BRAND.md` if one exists (see brand-capture `references/brand-context.md`). Read it; never edit it.

## 2. What goes in it

Sections, in this order. IDs are permanent: never renumber, never reuse an ID, mark rows retired instead of deleting them.

| Section | Holds | IDs |
|---|---|---|
| Front matter | `site`, `brand`, `platform`, `doc_type: analytics`, `last_audit`, `last_verified`, `owner_analytics` (who changes tags), `owner_site`, `sources` (exports and their versions) | |
| 1. Measurement goals and core events | The tracking plan: business outcomes by tier, each core event with its name per destination and where it originates | `T1`..`T4` tiers, events `E-n` |
| 2. Stack inventory | Every destination (GA4 property and stream IDs, Ads account, Meta pixel, others) and every install point (theme code, app embeds, web pixels, tag manager containers with version, server-side endpoints, consent tool), with evidence and date | `S-n` |
| 3. Consent and privacy | Regions served, banner and CMP, how choices reach each vendor (Shopify Customer Privacy API, consent mode defaults per region, GPC), last privacy-matrix result | |
| 4. Site dependency register | What tags need from the site: link hosts and paths, CTA text, page paths and hostnames, form behaviour, dataLayer events and keys, DOM selectors, cookies | `D-n` |
| 5. Findings | What is wrong or risky, with severity, evidence, owner and status | `F-n` |
| 6. Rules | Guardrails derived from the register: what nobody may change without an analytics check | `G-n` |
| 7. Load policy | Per tag: owner, the question it answers, when it loads, measured cost, decision | `L-n` |
| 8. Verification baseline | Static checks with expected counts, the live test matrix and its last result | |
| 9. Open questions | For the client or their analytics owner | `Q-n` |
| 10. Changelog | Dated, one line per change, newest last | |

## 3. Writing rules

- **Evidence or it did not happen.** Every inventory row and finding names its source and date: "page source 2026-10-15", "GTM export v80 2026-09-17", "HAR fresh-state 2026-10-15", "person's screenshot of Ads conversions". Observed and documented facts are labelled differently from inferences.
- **Statuses:** findings are `open`, `in progress`, `fixed (verified YYYY-MM-DD)`, `accepted` (client chose to live with it, with reason) or `retired`. Dependency rows are `ok`, `at risk`, `broken` or `retired`. Never mark something fixed without a verification line in section 8.
- **No secrets, no personal data.** Tag IDs, pixel IDs and conversion labels are fine (they are public in the page). Never write API keys, access tokens, CAPI tokens, passwords, customer emails, order details beyond a test order number, or anything copied from a real visitor.
- **Dates are absolute** (`2026-10-15`), never "last week".
- **One file per site.** A brand with two storefronts on different domains gets two files, or one file with a clearly separated section per site if they share a container.
- **Who writes what:** audit writes 2, 3, 5, 8 and the first draft of 1; setup owns 1 and updates 5, 8, 10; cleanup owns 7 and updates 2, 5, 10; guardrails owns 4 and 6 and updates 8 and 10. Any skill may add to 9.
- **Project instructions win.** If the repo's own instructions (AGENTS.md, CLAUDE.md) add rules about this file, follow them.
- **No em dashes** in anything written for the client or the team; rewrite the sentence instead.
