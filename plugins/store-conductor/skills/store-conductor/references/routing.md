# Routing: which skill does which work

Each backlog row gets one owner skill. This table is the source for that choice, for the toolbox
check in step 0, and for what to do when a skill isn't installed yet.

## Lanes

`foundation` (brand files), `evidence` (an audit or research that closes a gap), `tracking`,
`a11y`, `page`, `section`, `blog`, `seo`, `handoff` (someone else owns the fix).

## Routing table

| Backlog row | Lane | Owner skill (plugin) | Needs first | Its own gate |
|---|---|---|---|---|
| Brand files missing or stale | foundation | `brand-capture` (brand-capture) | nothing | Client questions it asks |
| Competitors unknown or old | evidence | `competitor-research` (competitor-research) | `BRAND.md` | none |
| Product reviews not mined | evidence | `cro-review-mining` (cro-review-mining, when installed) | A review export | none |
| Page shortfalls unknown | evidence | `page-audit` (page-content-studio) | Brand files, a goal | Read-only |
| Tracking or consent unknown or broken | tracking | `analytics-audit`, then `analytics-setup`, then `analytics-cleanup`, `analytics-guardrails` (analytics) | Site access it asks for | Its own approvals |
| Accessibility gaps | a11y | `accessibility-audit` (accessibility-audit) | A draft theme and a local dev server | Its approval before fixes |
| Blog post performance | seo | `content-seo-audit` (content-seo-audit) | A published post | none |
| Claims need verifying | evidence | `content-fact-check` (content-fact-check) | The copy | Before any publish |
| A named change this theme owns | page | `page-content-studio` (later `page-update`) | A picked `PAGE-AUDIT.md` row; brand files if copy changes | Draft only; plan table where it asks |
| A new page | page | `page-content-studio` (later `page-build`) | Playbook must-haves for the type; brand files | Plan table approved |
| A new section or block type | section | `section-builder` (not built yet; until then `page-content-studio` Step 3b rules) | The theme's rules; the page that needs it | Sibling pattern; core-file register |
| New blog post | blog | `shopify-blog-writer` (shopify-blog-writer) | `BRAND.md`, `COMPETITORS.md` | Delivers a hidden draft |
| Rewrite an existing article | blog | `shopify-blog-rewrite` (shopify-blog-rewrite) | The source article | Hidden draft |
| When and what to blog | blog | `shopify-blog-autopilot` (shopify-blog-autopilot) | The writer, brand files | Its check-ins |
| Verify a change | page | `page-verify` (later; until then `page-content-studio` Step 4) | A baseline from before | none |
| Push to draft, or go live | page | `page-ship` (later; until then `page-content-studio` Step 5) | Verified files | **Explicit yes in chat to go live** |
| Store settings, an app, an off-site page | handoff | nobody; the named owner | none | Report only |

## Choosing the owner

1. Match the row's type above. If two fit, prefer the more specific skill (an h1 problem is
   `page-content-studio`, a consent banner is a store setting, a double GA4 tag is `analytics-*`).
2. A row whose fix lives outside the theme (store settings, an app, an off-site page) is
   `handoff` even when an audit found it; write what was observed and what to ask the owner.
3. If a row needs evidence the plan doesn't have (an old or missing audit), the owner is the audit
   that produces it, and the build row is `blocked` behind it.
4. Never route a row to a skill because it is installed and convenient; route it to the skill
   whose job it is.

## Dependencies the sequence must respect

- Brand files before any new or rewritten copy.
- Claim checks (`content-fact-check`) before anything with regulated or numeric claims goes live.
- Tracking trustworthy (`analytics-audit`, then `analytics-setup`) before conclusions that rely
  on conversion numbers.
- A new section exists before the page that uses it.
- A change is verified before it ships to a draft, and a draft is reviewed before anyone is asked
  to approve going live.
- A rebuild of a page waits for the audit of that page, so it builds from evidence.

## When a skill isn't installed

State it once in step 0 with the plugin and install command (for example
`/plugin install analytics@brand-ai`), mark the rows it owns `blocked: skill not installed`, and
continue with the rest. For skills that don't exist yet, use the interim owner in the table and
say the split is not built yet. Never imitate a missing specialist.
