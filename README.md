# brand-ai

Claude Code plugin marketplace for brand-agnostic Shopify content skills.

## Install

```
/plugin marketplace add nylaapp/brand-ai
/plugin install shopify-blog-writer@brand-ai
/plugin install shopify-blog-rewrite@brand-ai
/plugin install shopify-blog-autopilot@brand-ai
```

## Plugins

| Plugin | What it does | Requires |
|---|---|---|
| shopify-blog-writer | Research and write SEO/AEO blog posts, deliver as hidden drafts | none |
| shopify-blog-rewrite | Rewrite an existing article in a store's brand voice | shopify-blog-writer |
| shopify-blog-autopilot | Decide when and what to blog, then hand off to the writer | shopify-blog-writer |

## Layout

```
.claude-plugin/marketplace.json
plugins/<name>/.claude-plugin/plugin.json
plugins/<name>/skills/<name>/SKILL.md
```

Validate with `claude plugin validate .`
