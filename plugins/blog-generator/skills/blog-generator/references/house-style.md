# House style: matching the brand's existing blog posts

A new post can look out of place next to the brand's other posts: the featured image sits in a different spot, headings follow a different pattern, and the length is far off. The user chooses how much to match. BRAND.md's **Blog** section gives the typical post (length, headings, byline, CTA style). The scan below fills in what that section doesn't say, from the live blog.

## 1. The user's choice

Ask only if the blog already has at least 3 published posts. With fewer, there's nothing to match, so use the best-practice format and say so.

> Should this post match the format of your existing blog posts?

| Option | What it means |
|---|---|
| **Yes, match them** | Same layout and conventions, and a length close to their typical range. Expect a lower ranking potential on competitive keywords. |
| **Match the layout, but go deeper for ranking** (recommended for search intent) | Same look and conventions, but with the length and depth the topic needs to rank (usually 1,200–2,500 words). |
| **No, use best-practice format** | The skill's own standard format. |

Record as `house_style` in the fields JSON: `match`, `match-layout`, or `best-practice`. For the first two, also record `length_target` as `[min, max]` words: the range from the scan for `match`, or the SEO range for `match-layout`.

Defaults when the user can't be asked: `match-layout` for the search and education intents, `match` for brand and promotion.

## 2. Scan the live blog (nothing is saved to BRAND.md)

Start from BRAND.md's Blog section. Then fetch 3–5 recent published posts, fresh each time because the blog changes and BRAND.md deliberately lists no posts: use `https://<store>/blogs/<blog-handle>.atom` (lists recent articles), the blog index page, or the Shopify connector (`articles` query). Open each post and note:

| Aspect | What to capture |
|---|---|
| **Featured image** | Set as the article's image (shown at the top or side by the theme) or placed inline in the body? Which position? Typical shape |
| **Headings** | H2-only or H2 + H3; question-style or label-style; sentence case or title case |
| **Opening** | Direct answer, story, or short intro; any summary or "key takeaways" box |
| **Length** | Word count of each; the typical range |
| **Formatting** | Use of lists, tables, pull quotes, callouts, emoji |
| **Byline and date** | Author shown how; date shown; "last updated" present? |
| **CTA style** | Inline links, end-of-post block, product cards, email signup |
| **Tags and categories** | Naming style; which tags are in use |
| **Tone** | Formal or friendly; first person plural; reading level |

Keep these notes in the run's brief. Don't write them to BRAND.md (only brand-capture writes it). If the live blog contradicts BRAND.md's Blog section, follow the live blog for this post and add a `BRAND-REQUESTS.md` line.

## 3. How to apply each option

- **Featured image:** if their posts use the article image field with the image not repeated in the body, set the featured image through the article's image field and **don't** also place it inline in the body HTML. Match their other conventions the same way.
- **Headings, opening, formatting, CTA, tags, byline:** follow the scan.
- **Length** (for `match`): stay within their typical range, plus or minus about 20%. Cut sections that don't serve the intent, but never cut required accuracy (sources, qualifiers).
- **Length** (for `match-layout`): follow the SEO standard for the intent, and keep every other convention.
- **The SEO standard still applies** to the parts that don't change appearance: SEO title, meta description, handle, alt text, internal links, schema.

## 4. Say what you did

In the final summary, add one short comparison so the user can see the trade-off:

> Your recent posts run about 500–1,000 words with the image set as the article image. This one is 1,720 words with the same layout, because the topic needs depth to rank for "…". Say the word if you'd rather I match your usual length.

Report only what you measured (word counts, layout), not made-up scores.

## 5. Refresh

Rescan only when the user asks ("our blog layout changed", "rescan my posts") or when the saved section is missing.
