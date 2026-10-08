# brand-ai

Claude Code plugin marketplace for brand-agnostic Shopify content skills.

## Install

```
/plugin marketplace add nylaapp/brand-ai
/plugin install brand-capture@brand-ai
/plugin install competitor-research@brand-ai
/plugin install content-fact-check@brand-ai
/plugin install accessibility-audit@brand-ai
/plugin install shopify-blog-writer@brand-ai
/plugin install shopify-blog-rewrite@brand-ai
/plugin install shopify-blog-autopilot@brand-ai
```

## Plugins

| Plugin | What it does | Requires |
|---|---|---|
| brand-capture | One-time brand setup: writes BRAND.md, BRAND-VOICE.md, BRAND-QUESTIONS.md | none |
| competitor-research | Dated competitor and inspiration research: writes COMPETITORS.md | brand-capture |
| content-fact-check | Verify claims in copy, with regulated-claim guardrails | none |
| accessibility-audit | Lighthouse accessibility scoring and additive fixes for Shopify themes | none |
| shopify-blog-writer | Research and write SEO/AEO blog posts, deliver as hidden drafts | brand-capture |
| shopify-blog-rewrite | Rewrite an existing article in a store's brand voice | shopify-blog-writer |
| shopify-blog-autopilot | Decide when and what to blog, then hand off to the writer | shopify-blog-writer, brand-capture |

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
```

Validate with `claude plugin validate .`


## Brand files

Brand skills read and write `BRAND.md`, `BRAND-VOICE.md`, `COMPETITORS.md`, `BRAND-QUESTIONS.md` and `BRAND-REQUESTS.md`. They look in the project root, then `~/` and `~/.claude/`, then the central directory (`$BRAND_AI_HOME/brands/<slug>/`, default `~/.brand-ai/brands/<slug>/`), then memory and connected knowledge, and only then offer to generate. Generated files are saved to the central directory. Full rules: `plugins/brand-capture/skills/brand-capture/references/brand-context.md`.
