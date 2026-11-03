# brand-ai

Plugin marketplace for brand-agnostic Shopify content and analytics skills.

## Install (Claude Cowork)

1. In Claude Cowork, select **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and enter `nylaapp/brand-ai` (or `https://github.com/nylaapp/brand-ai`). Do this once.
3. Find **brand-capture** under the Brand AI marketplace and click **Install**. Every other plugin builds on its output, so install it first.
4. Install any other plugin from the table below the same way.
5. Start a Cowork task in the client's project folder and say "Capture the brand for example.com".

To pick up new versions, select **Check for updates** on the marketplace (or turn on **Sync automatically**). To see the documentation from inside Claude, install **brand-docs** and say "show the documentation".

## Plugins

| Plugin | Skills | What it does | Requires |
|---|---|---|---|
| brand-capture | `brand-capture` | One-time brand setup: always asks for the brand's site or store and any brand book, reads them, and writes BRAND.md, BRAND-VOICE.md, design.md, BRAND-QUESTIONS.md, saved in the folder of a draft theme you choose | none |
| competitor-research | `competitor-research` | Dated competitor and inspiration research: writes COMPETITORS.md next to BRAND.md in the draft theme's folder | brand-capture |
| fact-check | `fact-check` | Verify claims in copy, with regulated-claim guardrails | none |
| accessibility-audit | `accessibility-audit` | Lighthouse accessibility scoring and additive fixes for Shopify themes | none |
| seo-audit | `seo-audit` | Audit a live blog post (schema, PageSpeed, on-page) and track Search Console rankings at 2 and 4 weeks | none (pairs with blog-generator) |
| blog-generator | `blog-generator` | Research and write SEO/AEO blog posts, deliver as hidden drafts | brand-capture |
| blog-rewriter | `blog-rewriter` | Rewrite an existing article in a store's brand voice | blog-generator |
| blog-autopilot | `blog-autopilot` | Decide when and what to blog, then hand off to the writer | blog-generator, brand-capture |
| styles-builder | `styles-builder` | Generate design.md (colors, type, spacing, radius, shadows, buttons, components) from a brand book or reference store, apply it and the starter setup (logo, favicon, motion, inputs, variant pickers) into the theme's settings, and optionally brand the starter section templates | brand-capture |
| page-studio | `page-audit`, `page-create`, `page-edit-content`, `page-edit-design`, `page-studio` | Page work in focused skills behind a thin front door: `page-audit` (read-only gap analysis, `PAGE-AUDIT.md`), `page-create` (new pages and sections), `page-edit-content` (words, images, links) and `page-edit-design` (layout, order, style). Each verifies on the rendered page and pushes only the touched files to the theme you chose | brand-capture |
| analytics | `analytics-audit`, `analytics-cleanup`, `analytics-guardrails`, `analytics-setup` | Four skills sharing one `ANALYTICS.md` per client: `analytics-audit` (tagging audit, full audit across privacy states), `analytics-setup` (issue list to approved, verified fixes), `analytics-cleanup` (quick cleanup, zero-based deep tag cleanup), `analytics-guardrails` (dependency register, change checks, drift watch) | none (reads BRAND.md if present) |
| cro-audit | `cro-audit` | Conversion audit with no integrations: heuristic review, page speed, mobile pass, funnel math from pasted numbers; findings labelled by evidence type, written to `CRO-AUDIT.md` | none |
| brand-docs | `brand-docs` | Open this documentation inside Claude ("show the documentation"): every plugin and skill, example prompts and how they fit together | none |

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill>/SKILL.md
```

The `analytics` plugin holds four skills in one plugin (`plugins/analytics/skills/analytics-*/`) because they share a file contract, references and scripts; the shared references and scripts live in `analytics-audit`.

Validate with `claude plugin validate .`


## Brand files

Brand skills read and write `BRAND.md`, `BRAND-VOICE.md`, `COMPETITORS.md`, `BRAND-QUESTIONS.md` and `BRAND-REQUESTS.md`. They look in the project root, then `~/` and `~/.claude/`, then the central directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`), which holds the files or a `BRAND-HOME.md` that names the draft theme's folder where they are, then memory and connected knowledge, and only then offer to generate. `brand-capture` and `competitor-research` ask which draft theme to save the brand files in and save them in that theme's folder on the computer, at its root beside `assets/`, `config/` and the rest (never inside the theme's own folders, and never in `assets/`, which is public), so later customization and every other skill finds them there. Nothing is pushed to the store. With no draft theme yet, or no Shopify store, they go in the central directory. Full rules: `plugins/brand-capture/skills/brand-capture/references/brand-context.md` and `brand-home.md`.

## Theme target

Skills that can change theme files (`page-create`, `page-edit-content`, `page-edit-design`, `styles-builder`, `accessibility-audit`, and `analytics-setup` and `analytics-cleanup` when they touch theme code) ask once which theme to work on, a draft or the live theme, and remember the answer in `THEME-TARGET.md` next to `BRAND.md` (or in the central directory), so the next skill reuses it without asking. Name a different theme at any time to switch. The file records the theme only, never permission: for the live theme, each skill asks for an explicit yes before any edit and again before the push, every run. Read-only skills (audits) never need the question. `brand-capture` asks for a draft theme too, to save the brand files in, and that choice is remembered the same way. Full rules, identical in each plugin that uses them: `references/theme-target.md` (in `page-studio`, `styles-builder`, `accessibility-audit`, `analytics-setup` and `brand-capture`).

## Analytics file

The analytics skills keep one `ANALYTICS.md` per client site: tracking plan, stack inventory, consent setup, site dependency register, findings, rules, load policy, verification baseline, questions and changelog. Lookup: project root (also the legacy name `ANALYTICS_GUARDRAILS.md`), then `~/` and `~/.claude/`, then `$BRAND_AI_HOME/brands/<slug>/ANALYTICS.md`. Full rules: `plugins/analytics/skills/analytics-audit/references/analytics-file.md`. Scripts need Python 3 (standard library); the privacy matrix needs Node and Playwright; the cost benchmark needs Node and Chrome (Lighthouse via npx). GA4 checks can use Google's Analytics MCP server.
