# Output templates

Contents: 1. Content brief · 2. Body HTML conventions · 3. Fields JSON · 4. Shopify fields sheet · 5. JSON-LD schema

---

## 1. Content brief (`<handle>-brief.md`)

```markdown
# Content brief: <Working title>

**Brand:** <Brand> — <one-line what/for whom>   **Date:** <YYYY-MM-DD>
**Post intent:** <education | brand | search | promotion> (chosen by user | inferred: why)
**Media:** <own uploads | stock | both>   **Format:** <match | match-layout | best-practice> (length target <min–max> words)
**Brand facts:** BRAND.md rev <n> (<status>, <last_updated>) for <store>; COMPETITORS.md (<researched date>) or "none; assumptions below"
**Assumptions:** <anything you had to assume; "none" if all confirmed>

## Keywords and search intent
- Primary: <keyword> — search intent: <informational | commercial> — format: <how-to | guide | listicle | comparison>
- Secondary / long-tail: <3–5>
- Volume/difficulty: <from tool export, or "not verified — check in Keyword Planner/Ahrefs">
- Seasonality: <none | peak month, publish by …>

## Target reader
<Who, what problem, what they've already tried, the words they use (from VOC research)>

## Titles
- Post title (H1): <…>
- SEO title (<n> chars): <…>
- Meta description (<n> chars): <…>
- URL handle: /blogs/<blog>/<handle>

## SERP summary and gaps
| # | Result | Format | ~Words | Notable | Gap |
|---|---|---|---|---|---|
SERP features present: <featured snippet type, PAA, video, AI Overview>
**Our angle / how we beat them:** <…>

## Outline
- Answer-first (40–60 words): <draft>
- H2 … / H3 …
- FAQ (3–6): <questions + source: PAA / Reddit / reviews>

## Unique asset
<framework / table / checklist / stat — and its source>

## Brand facts and first-party material
- Found: <from store pages>
- Needed from brand: <placeholders to fill>

## Sources to cite
1. <Title — publisher — year — URL>

## Internal links
- Products/collections (2–4): <anchor → URL (verified | [[VERIFY]])>
- Related posts (2–3): <anchor → URL>; pillar: <…>
- Link-back from: <product/collection pages → suggested anchor>

## Media
<own uploads → shot list; stock → image plan; featured image goes in the article image field | inline>; tables; optional video

## Claims to fact-check
<regulated or factual claims the post makes, and whether the fact-check was run>

## First-hand asset and stance
<the one thing only this brand has that the post is built around (founder story, testing note, repeated customer question, mistake, data, photo); and the position the post takes, including who it's not for. If missing: say so and list the placeholder>

## Net-new value
<what the reader gets here that a generic article on this topic doesn't: a specific angle, real example, comparison, expert or first-party input. If none can be found, say so and add a placeholder for the user's input>

## CTA
<one tangible next step: text, link, goal, and placement (every post needs one)>
```

---

## 2. Body HTML conventions (`<handle>.html`)

Paste target is Shopify's article editor in HTML view, so output **only the body content** — no `<html>`, `<head>`, `<body>`, `<style>` or `<script>` (Shopify strips scripts from articles; JSON-LD goes in the theme or an app — see section 5). Use semantic tags and minimal inline styling so the theme's typography applies.

Skeleton:

```html
<p class="post-meta"><em>Last updated: September 29, 2026 · By <a href="/pages/about">Author Name</a>, Role at Brand</em></p>

<p><strong>Direct 40–60 word answer to the primary query…</strong></p>

<p>Short intro: who this is for, what they'll learn, where Brand fits.</p>

<h2>Question-shaped H2 with primary keyword</h2>
<p>…</p>
<img src="[[UPLOAD: descriptive-name.webp]]" alt="Describes the image" width="1200" height="800">

<h2>…</h2>
<h3>…</h3>
<ul><li>…</li></ul>

<h2>Comparison / framework</h2>
<table>
  <thead><tr><th>…</th><th>…</th></tr></thead>
  <tbody><tr><td>…</td><td>…</td></tr></tbody>
</table>

<!-- Contextual CTA -->
<div class="post-cta">
  <p><strong>Ready to …?</strong> Our <a href="/collections/…">descriptive collection anchor</a> is …</p>
</div>

<h2>Frequently asked questions</h2>
<h3>Question one?</h3>
<p>Standalone 40–80 word answer.</p>
…

<h2>Sources</h2>
<ol><li><a href="https://…" rel="noopener" target="_blank">Title — Publisher (Year)</a></li></ol>

<h2>Related reading</h2>
<ul>
  <li><a href="/blogs/journal/…">Descriptive title of related post</a></li>
</ul>

<div class="author-box">
  <p><strong>About the author:</strong> Name is … at Brand, with … years of … <a href="/pages/about">More about Brand</a>.</p>
</div>

<p class="photo-credits"><small>Photos: <a href="…">Name</a> on Unsplash.</small></p>
```

Rules: no `<h1>`; when the house style sets the featured image through the article's image field, don't repeat it in the body; user-supplied media slots use `[[USER MEDIA: file-name.webp]]` in `src`; first image without `loading="lazy"`, the rest with it; internal links are root-relative (`/products/…`) so they work on any domain; external links open in a new tab with `rel="noopener"`.

---

## 3. Fields JSON (`<handle>-fields.json`)

Used by `scripts/check_post.py`. Keep keys exactly. `intent` is `education`, `brand`, `search` or `promotion` (default `search` if absent); `house_style` is `match`, `match-layout` or `best-practice`; `cta` is the single next step (`text`, `url`, `goal`) `first_hand_asset` and `stance` are one line each, and `net_new_value` is one line on what the reader gets that a generic article lacks (both checked); `length_target` is `[min_words, max_words]` (the checker uses it instead of its default range, and treats a post inside it as on target).

```json
{
  "brand": "Brand",
  "intent": "education",
  "house_style": "match-layout",
  "cta": {"text": "Shop linen sheets", "url": "/collections/linen-sheets", "goal": "shop"},
  "first_hand_asset": "Our 6-week wash test on 3 linen weights",
  "stance": "We stopped recommending hot washes; not for people who need sanitizing cycles",
  "net_new_value": "A wash-temperature table tested against our own fabric weights",
  "length_target": [1200, 2500],
  "primary_keyword": "how to wash linen sheets",
  "secondary_keywords": ["washing linen bedding", "linen care", "..."],
  "title": "How to Wash Linen Sheets (So They Get Softer, Not Worn Out)",
  "seo_title": "How to Wash Linen Sheets: Care Guide | Brand",
  "meta_description": "…",
  "handle": "how-to-wash-linen-sheets",
  "blog_handle": "journal",
  "excerpt": "…",
  "tags": ["Linen Care", "Bedding Guides"],
  "author": "Name",
  "published_date": "2026-09-29",
  "featured_image": {"file_name": "….webp", "alt": "…", "source_url": "…", "download_url": "…", "credit": "…"}
}
```

---

## 4. Shopify fields sheet (`<handle>-shopify-fields.md`)

Organised in the order the user will meet the fields in Shopify admin (Online Store → Blog posts → Add blog post):

```markdown
# Shopify fields: <title>

| Field (Shopify editor) | Value | Notes |
|---|---|---|
| Title | … | Renders as H1 |
| Content | Paste `<handle>.html` in HTML view (`<>`) | |
| Excerpt | … | |
| Featured image | `<file>.webp` — alt: "…" | 1200×630 |
| Blog | <blog handle> | |
| Author | … | |
| Tags | …, … | Reuse existing cluster tags |
| Visibility | Hidden until reviewed → Visible | |
| SEO: Page title | … (<n> chars) | Search engine listing → Edit |
| SEO: Meta description | … (<n> chars) | |
| SEO: URL handle | … | Full URL: /blogs/<blog>/<handle> |

## Images
<table from images.md §4>

## Placeholders to fill before publishing
- [[…]]

## Structured data
<JSON-LD blocks + where to add them>

## Link-back plan
| Page | Add link with anchor | Where on page |

## Pre-publish technical checklist
- [ ] Rich Results Test passes (no duplicate Article schema from the theme)
- [ ] Social preview shows correct image/title/description
- [ ] PageSpeed Insights mobile check
- [ ] Post visible; appears in /sitemap.xml
- [ ] No other post targets "<primary keyword>"
- [ ] Refresh reminder set for <date>
```

---

## 5. JSON-LD schema

Shopify strips `<script>` from article content, so deliver these for the theme (`sections/main-article.liquid` or `templates/article.json` custom liquid block) or an SEO app. Provide static values filled in *and* a note that the theme may already output `Article`/`BlogPosting` — check before adding to avoid duplicates.

**BlogPosting**
```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "<title, ≤110 chars>",
  "description": "<meta description>",
  "image": ["https://<store>/cdn/shop/files/<featured>.webp"],
  "datePublished": "2026-09-29",
  "dateModified": "2026-09-29",
  "author": {"@type": "Person", "name": "<Author>", "url": "https://<store>/pages/about", "jobTitle": "<Role>"},
  "publisher": {"@type": "Organization", "name": "<Brand>", "logo": {"@type": "ImageObject", "url": "https://<store>/cdn/shop/files/logo.png"}},
  "mainEntityOfPage": {"@type": "WebPage", "@id": "https://<store>/blogs/<blog>/<handle>"},
  "keywords": "<primary>, <secondary…>",
  "about": {"@type": "Thing", "name": "<topic>"}
}
```

Liquid version for the theme (dynamic):
```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": {{ article.title | json }},
  "description": {{ article.excerpt_or_content | strip_html | truncate: 155 | json }},
  "image": {{ article.image | image_url: width: 1200 | prepend: 'https:' | json }},
  "datePublished": {{ article.published_at | date: '%Y-%m-%d' | json }},
  "dateModified": {{ article.updated_at | date: '%Y-%m-%d' | json }},
  "author": {"@type": "Person", "name": {{ article.author | json }}},
  "publisher": {"@type": "Organization", "name": {{ shop.name | json }}},
  "mainEntityOfPage": {{ shop.url | append: article.url | json }}
}
</script>
```

**FAQPage** — questions and answers must match the visible FAQ text exactly.
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {"@type": "Question", "name": "<Q1>", "acceptedAnswer": {"@type": "Answer", "text": "<A1>"}}
  ]
}
```

**HowTo** — only for genuinely step-by-step posts.
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "<How to …>",
  "totalTime": "PT20M",
  "supply": [{"@type": "HowToSupply", "name": "…"}],
  "step": [{"@type": "HowToStep", "position": 1, "name": "…", "text": "…"}]
}
```

**Organization** — site-wide, once, in `layout/theme.liquid` (if not already present).
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "<Brand>",
  "url": "https://<store>",
  "logo": "https://<store>/cdn/shop/files/logo.png",
  "description": "<Brand> is a <what> that makes <products> for <who>.",
  "sameAs": ["https://www.instagram.com/<brand>", "https://www.tiktok.com/@<brand>"]
}
```
