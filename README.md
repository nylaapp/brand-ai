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
| brand-capture | `brand-capture` | One-time brand setup: always asks for the brand's site or store and any brand book, reads them, and writes BRAND.md, BRAND-VOICE.md, design.md, BRAND-QUESTIONS.md, saved in the folder of the staging theme you choose | none |
| competitor-research | `competitor-research` | Dated research on the top 3 competitors: writes COMPETITORS.md next to BRAND.md in the staging theme's folder (inspiration brands are covered by brand-capture) | brand-capture |
| fact-check | `fact-check` | Verify claims in copy, with regulated-claim guardrails | web search (checked first, with step-by-step setup help) |
| theme-audit | `theme-audit` | Full Lighthouse suite from the command line (speed, accessibility, best practices, SEO; phone and desktop; several runs; HTML reports saved), Shopify Theme Inspector (`shopify theme profile`: which theme files take the server longest) and Theme Check, presented as a plain-language readout like `cro-audit` (headline, scorecard, fix these first). Names who owns each problem; read-only audit mode, or fix mode on the staging theme with proof nothing visible changed. Accessibility to 1.00; speed as a median of several runs plus real-visitor data. Written to `THEME-AUDIT.md`. Replaces `accessibility-audit` | Node.js, Shopify CLI, Chrome (checked first, with step-by-step setup help) |
| seo-audit | `seo-audit` | Audit a live blog post (schema, PageSpeed, on-page) and track Search Console rankings at 2 and 4 weeks | a browser and Search Console access (checked first, with step-by-step setup help); pairs with blog-generator |
| blog-generator | `blog-generator` | Research and write SEO/AEO blog posts, deliver as hidden drafts | brand-capture; Shopify connected recommended (checked first, with step-by-step setup help) |
| blog-rewriter | `blog-rewriter` | Rewrite an existing article in a store's brand voice | blog-generator (setup checked first, with step-by-step help) |
| blog-autopilot | `blog-autopilot` | Decide when and what to blog, then hand off to the writer | blog-generator, brand-capture; a folder, Shopify connected, Python 3 (checked first, with step-by-step setup help) |
| styles-builder | `styles-builder` | Generate design.md (colors, type, spacing, radius, shadows, buttons, components) from a brand book or reference store, apply it and the starter setup (logo, favicon, motion, inputs, variant pickers) into the theme's settings, and optionally brand the starter section templates | brand-capture |
| page-studio | `page-audit`, `page-create`, `page-edit-content`, `page-edit-design`, `page-studio` | Page work in focused skills behind a thin front door: `page-audit` (read-only gap analysis, `PAGE-AUDIT.md`), `page-create` (new pages and sections), `page-edit-content` (words, images, links) and `page-edit-design` (layout, order, style). Each verifies on the rendered page and pushes only the touched files to the staging theme. Works through the Shopify CLI, or, with no CLI installed, through the Shopify connector when it is allowed to change themes (nothing renders before the write on that route, so the check runs on the private draft right after it, and Theme Check can't run) | brand-capture; to change pages either Node.js and the Shopify CLI, or the Shopify connector with permission to change themes (checked first, with step-by-step setup help) |
| analytics | `analytics-audit`, `analytics-cleanup`, `analytics-guardrails`, `analytics-setup` | Four skills sharing one `ANALYTICS.md` per client: `analytics-audit` (tagging audit, full audit across privacy states), `analytics-setup` (issue list to approved, verified fixes), `analytics-cleanup` (quick cleanup, zero-based deep tag cleanup), `analytics-guardrails` (dependency register, change checks, drift watch) | none (reads BRAND.md if present) |
| cro-audit | `cro-audit` | Full CRO audit suite, strictly read-only: technical and speed, heuristic and competitive review, Shopify Analytics read through the Shopify CLI (or supplied numbers) with data-validity checks, behavioural review, voice of customer, survey and user-test plans, prioritisation, experiment planning and an A/B result checker; written to `CRO-AUDIT.md` | none (uses analytics numbers, recordings, reviews if you have them) |
| site-reader | `site-reader` | Read a live page cheaply without the browser pane: text and structure over HTTP, then headless Chrome at desktop and mobile for sections, first screen, popups, type and colours, as a short summary. Pictures only on request. Read-only | Python 3 and Chrome or Chromium on the machine (no install) |
| brand-docs | `brand-docs` | Open this documentation inside Claude ("show the documentation"): every plugin and skill, example prompts and how they fit together | none |

## How the skills reply

Every skill starts with a "How to reply" section that applies in Claude and in any other AI app: short and direct; no technical knowledge assumed, including of Shopify; numbered step-by-step guides for anything the person must set up or do; simple English with no figures of speech; formal and professional. It covers messages to the person only. Content written for the brand follows `BRAND-VOICE.md`.

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<skill>/SKILL.md
plugins/<name>/skills/<skill>/references/ground-rules.md   # copied from shared/references/
shared/references/                                     # ground-rules.md, theme-target.md: edit here, then sync
```

The `analytics` plugin holds four skills in one plugin (`plugins/analytics/skills/analytics-*/`) because they share a file contract, references and scripts; the shared references and scripts live in `analytics-audit`.

Validate with `claude plugin validate .` and `scripts/sync-shared.sh --check`.


## Brand files

Brand skills read and write `BRAND.md`, `BRAND-VOICE.md`, `design.md`, `COMPETITORS.md`, `BRAND-QUESTIONS.md` and `BRAND-REQUESTS.md`. They look in the project root, then `~/` and `~/.claude/`, then the central directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`), which holds the files or a `BRAND-HOME.md` that names the staging theme's folder where they are. Memory and connected knowledge can add supporting facts but never stand in for a required file: if one is missing, the skill stops and offers to create it. `brand-capture` asks which theme is the staging theme at the start of the project (offering to create one), and it and `competitor-research` save the brand files in that theme's folder on the computer, at its root beside `assets/`, `config/` and the rest (never inside the theme's own folders, and never in `assets/`, which is public), so later customization and every other skill finds them there. Nothing is pushed to the store. With no staging theme yet, or no Shopify store, they go in the central directory. Full rules: `plugins/brand-capture/skills/brand-capture/references/brand-context.md` and `brand-home.md`.

## Ground rules (every plugin, every skill)

Three rules hold for every skill in the marketplace. Each `SKILL.md` opens with a short **Ground rules** block that names
its required brand files; the full text is `references/ground-rules.md` in every skill.

1. **Brand files first.** A skill that writes, designs or judges anything for the brand reads the brand files it needs
   (`BRAND.md`, `BRAND-VOICE.md`, `design.md`, and `COMPETITORS.md` where used) before any work, and follows them. If a
   required file is missing or belongs to another store, the skill stops and asks: create it now (brand-capture,
   voice-builder or styles-builder) or say where it is. There is no "carry on without it", and memory or the live site
   never stand in for it. Unattended runs stop and report what is missing.
2. **Staging first.** Each store has one **staging theme**: an unpublished theme whose name contains "staging", chosen
   at the start of the store project (brand-capture asks in its Step 1) and remembered in `THEME-TARGET.md`. If there
   is none, the skill offers to create "<live theme name> staging". Every skill that changes a theme puts its changes
   there; the live theme is never edited directly. When the theme is in a git repository, work is committed on the
   `staging` branch (kept up to date with the live branch), never on the branch the live theme comes from. Store
   content (blog posts, pages) is created hidden. Read-only skills never ask for a staging theme.
3. **Going live is the person's decision.** No skill suggests, offers or schedules publishing. The person publishes in
   the store admin, or asks Claude in their own words; then the **go-live gate** runs: a drift check (was live edited
   since?), the full list of what ships, what was verified, how to undo it, then two confirmations, the second typed.
   Scheduled and automated runs never go live.

| | Applies to | Detail |
|---|---|---|
| Brand files | Every brand-dependent skill (blogs, copy, pages, campaigns, styles, CRO, fact-check) | `references/ground-rules.md` §1; lookup: `plugins/brand-capture/skills/brand-capture/references/brand-context.md` |
| Staging theme and branch | Skills that change a theme or save files in its folder: `brand-capture`, `competitor-research`, `voice-builder`, `styles-builder`, `page-studio` (create, edit content, edit design), `theme-audit` (fix mode), `shopify-storefront`, `analytics-setup` and `analytics-cleanup` (theme code) | `references/theme-target.md` §1 to §6 |
| Go-live gate | Every skill, when the person asks to publish, merge to live or make content visible | `references/ground-rules.md` §3, `references/theme-target.md` §7 |

The `page-studio` editing skills can do the same work through the Shopify connector when the Shopify CLI isn't
installed (`plugins/page-studio/skills/page-studio/references/connector-route.md`): it needs the connector to read and
change themes on the right store, and writes only to the staging theme.

### Keeping the shared rules in sync

`ground-rules.md` and `theme-target.md` are written once in `shared/references/` and copied into each skill, because a
plugin can't read another plugin's folder. Edit only the files in `shared/`, then run:

```
scripts/sync-shared.sh          # copy into every skill
scripts/sync-shared.sh --check  # fail if a copy differs or a SKILL.md lacks its Ground rules block
```

## Analytics file

The analytics skills keep one `ANALYTICS.md` per client site: tracking plan, stack inventory, consent setup, site dependency register, findings, rules, load policy, verification baseline, questions and changelog. Lookup: project root (also the legacy name `ANALYTICS_GUARDRAILS.md`), then `~/` and `~/.claude/`, then `$BRAND_AI_HOME/brands/<slug>/ANALYTICS.md`. Full rules: `plugins/analytics/skills/analytics-audit/references/analytics-file.md`. Scripts need Python 3 (standard library); the privacy matrix needs Node and Playwright; the cost benchmark needs Node and Chrome (Lighthouse via npx). GA4 checks can use Google's Analytics MCP server.
