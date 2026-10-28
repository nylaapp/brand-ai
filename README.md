# brand-ai

Claude Code plugin marketplace for brand-agnostic Shopify content and analytics skills.

## Install

```
/plugin marketplace add nylaapp/brand-ai
/plugin install brand-capture@brand-ai
/plugin install competitor-research@brand-ai
/plugin install content-fact-check@brand-ai
/plugin install accessibility-audit@brand-ai
/plugin install content-seo-audit@brand-ai
/plugin install blog-generator@brand-ai
/plugin install blog-rewriter@brand-ai
/plugin install shopify-blog-autopilot@brand-ai
/plugin install styles-builder@brand-ai
/plugin install page-content-studio@brand-ai
/plugin install analytics@brand-ai
```

## Plugins

| Plugin | What it does | Requires |
|---|---|---|
| brand-capture | One-time brand setup: always asks for the brand's site or store and any brand book, reads them, and writes BRAND.md, BRAND-VOICE.md, design.md, BRAND-QUESTIONS.md | none |
| competitor-research | Dated competitor and inspiration research: writes COMPETITORS.md | brand-capture |
| content-fact-check | Verify claims in copy, with regulated-claim guardrails | none |
| accessibility-audit | Lighthouse accessibility scoring and additive fixes for Shopify themes | none |
| content-seo-audit | Audit a live blog post (schema, PageSpeed, on-page) and track Search Console rankings at 2 and 4 weeks | none (pairs with blog-generator) |
| blog-generator | Research and write SEO/AEO blog posts, deliver as hidden drafts | brand-capture |
| blog-rewriter | Rewrite an existing article in a store's brand voice | blog-generator |
| shopify-blog-autopilot | Decide when and what to blog, then hand off to the writer | blog-generator, brand-capture |
| styles-builder | Generate design.md (colors, type, spacing, radius, shadows, buttons, components) from a brand book or reference store, apply it and the starter setup (logo, favicon, motion, inputs, variant pickers) into the theme's settings, and optionally brand the starter section templates | brand-capture |
| page-content-studio | Page work in focused skills behind a thin front door: `page-audit` (read-only gap analysis, `PAGE-AUDIT.md`), `page-create` (new pages and sections), `page-edit-content` (words, images, links) and `page-edit-design` (layout, order, style). Each verifies on the rendered page and pushes only the touched files to the theme you chose | brand-capture |
| analytics | Four skills sharing one `ANALYTICS.md` per client: `analytics-audit` (tagging audit, full audit across privacy states), `analytics-setup` (issue list to approved, verified fixes), `analytics-cleanup` (quick cleanup, zero-based deep tag cleanup), `analytics-guardrails` (dependency register, change checks, drift watch) | none (reads BRAND.md if present) |

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
```

The `analytics` plugin holds four skills in one plugin (`plugins/analytics/skills/analytics-*/`) because they share a file contract, references and scripts; the shared references and scripts live in `analytics-audit`.

Validate with `claude plugin validate .`


## Brand files

Brand skills read and write `BRAND.md`, `BRAND-VOICE.md`, `COMPETITORS.md`, `BRAND-QUESTIONS.md` and `BRAND-REQUESTS.md`. They look in the project root, then `~/` and `~/.claude/`, then the central directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`), then memory and connected knowledge, and only then offer to generate. Generated files are saved to the central directory. Full rules: `plugins/brand-capture/skills/brand-capture/references/brand-context.md`.

## Theme target

Skills that can change theme files (`page-create`, `page-edit-content`, `page-edit-design`, `styles-builder`, `accessibility-audit`, and `analytics-setup` and `analytics-cleanup` when they touch theme code) ask once which theme to work on, a draft or the live theme, and remember the answer in `THEME-TARGET.md` next to `BRAND.md` (or in the central directory), so the next skill reuses it without asking. Name a different theme at any time to switch. The file records the theme only, never permission: for the live theme, each skill asks for an explicit yes before any edit and again before the push, every run. Read-only skills (audits) never need the question. Full rules, identical in each plugin that changes themes: `references/theme-target.md` (in `page-content-studio`, `styles-builder`, `accessibility-audit` and `analytics-setup`).

## Analytics file

The analytics skills keep one `ANALYTICS.md` per client site: tracking plan, stack inventory, consent setup, site dependency register, findings, rules, load policy, verification baseline, questions and changelog. Lookup: project root (also the legacy name `ANALYTICS_GUARDRAILS.md`), then `~/` and `~/.claude/`, then `$BRAND_AI_HOME/brands/<slug>/ANALYTICS.md`. Full rules: `plugins/analytics/skills/analytics-audit/references/analytics-file.md`. Scripts need Python 3 (standard library); the privacy matrix needs Node and Playwright; the cost benchmark needs Node and Chrome (Lighthouse via npx). GA4 checks can use Google's Analytics MCP server.
