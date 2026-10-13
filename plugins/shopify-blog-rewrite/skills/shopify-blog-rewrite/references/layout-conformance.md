# Layout conformance: the rewrite must look like the store's own articles

This file is the working detail of the rule at the top of SKILL.md: **the destination store's blog conventions always win**. Where the project has its own blog rules, they come first; the store's published articles come second (below); the writer's defaults are the last resort.

A rewrite that only matches the brand's *words* is half done. It must also match how the store's own articles are built: the same
opening element, the same image markup, the same closing block, the same allowed tags. Otherwise it renders differently from its
neighbours, loses the theme's styling, or leaves a visible gap (for example no image where every other article opens with one).
Read this at Step 2 (learn the layout) and Step 4 (check it).

## 1. Learn the layout from the store, not from memory

Fetch the store's **newest published articles** (6 is enough; a few from each blog if the store has several) and save them as
`<run folder>/layout-samples.json`:

```graphql
query { articles(first: 6, sortKey: PUBLISHED_AT, reverse: true, query: "published_status:published") {
  nodes { handle title blog { handle } templateSuffix tags author { name } summary image { url altText width height } body } } }
```

(Validate it before running, as for any connector call. Through a browser or a live page, copy each article's body HTML.) Then read:

| Look at | Copy it when |
|---|---|
| **What opens the body** (a figure, a paragraph) | Most samples with an image open with a figure: the rewrite opens with one too |
| **The image markup** (`figure`, `img` attributes, `figcaption` or not, width and height, `loading`) | Always: same elements, same attributes, real width and height from the file |
| **Where images are hosted** | Always the store's own CDN, never the source site |
| **The article image field** (`image`, with alt text) | Set when the samples set it (blog cards and social previews use it) |
| **Heading levels and how many** | Use only the levels the samples (or the theme's CSS) use; no `<h1>` ever |
| **Allowed tags and classes** | Only what the samples use. No inline styles, scripts, iframes or `data-` attributes |
| **The closing block** (a standard disclaimer, a CTA panel, a sign-off) | Copy its HTML **verbatim from the newest sample**. Never retype it from BRAND.md: retyping loses paragraph breaks and spacing |
| **templateSuffix, author, tags** | Same suffix and author as the samples; tags only if the samples use reader-facing tags |
| **Length, paragraph size, lists** | Within the samples' range |

The theme's own CSS and the project's blog rules (for example a theme stylesheet that floats the first figure, or a rule that
a post with two or more images needs a developer-mapped layout) are part of the layout. Read them if the project has them
(`assets/*.css` rules for the article content, the project's blog skill or AGENTS.md) and follow them: they win over this file.

## 2. The lead image is part of the layout

When the store's articles open with an image, the rewrite opens with one:

- **Source has an image:** extract it and upload it to the store's CDN (`references/media-transfer.md`), then place it as the first
  figure, in the store's exact markup, and set the article image field with the same file.
- **Source has no image, or every image was flagged:** do not leave the opening empty without saying so. Ask the person for an
  image (a public URL, or a file already in the store's Files), or record "no lead image: blog card will show without a thumbnail" as
  the first item in the report and keep the draft marked not ready. Never substitute stock.
- **Series:** an article without a usable lead image is `needs_attention` in the tracker until the person supplies one or accepts
  the gap.

## 3. Check the draft against the store

```bash
python3 scripts/layout_check.py --samples <run folder>/layout-samples.json --draft <run folder>/<handle>.html --image-set yes
```

It reports PASS, WARN, INFO or FAIL for: the lead figure, each image's attributes, the image host, the article image field,
forbidden tags, unknown classes, inline styles, heading levels, the closing block (identical text and last position),
paragraph length and lists. Fix every FAIL before delivery and say each WARN in the report. Run it once on the HTML body you
will send, and once more on the body read back from Shopify after the draft is created. The check looks at structure, not
wording, and it is only as good as its samples: with fewer than two published articles it stops, and you follow the project's
blog rules instead.
