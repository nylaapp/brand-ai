# The 10-layer standard for a Shopify blog post

This is the full standard, written for the **search and AI visibility** intent. Other intents relax the parts that only serve ranking (see `intents.md`): brand journals don't need answer-first, an FAQ or a table, and run shorter; promotions need an offer-led opening and more product links. Every intent still needs correct SEO fields, descriptive links, alt text, honest claims and a clean heading structure. If the user chose a house-style length (`house-style.md`), that range replaces the word count here.

Use this while writing (Step 3) and as the checklist in QA (Step 6). Items marked **[script]** are checked by `scripts/check_post.py`.

## 1. Search intent and keywords
- [ ] One primary keyword, matched to intent (informational "how to…" / commercial "best X for Y").
- [ ] 3–5 secondary and long-tail variants used naturally. **[script: counts presence]**
- [ ] Topic is one the brand can credibly own (builds topical authority).
- [ ] Primary keyword in: post title, SEO title, meta description, first 100 words, at least one H2. **[script]**

## 2. On-page SEO fields (Shopify post editor)
- [ ] **SEO title** ~50–60 chars, keyword near the front, brand optional at end ("… | Brand"). **[script]**
- [ ] **Meta description** ~140–155 chars, benefit-led, includes keyword and a reason to click. **[script]**
- [ ] **URL handle** short, lowercase, hyphenated, keyword-based, no dates, no stop-word filler (`how-to-wash-linen-sheets`, not `2026-09-our-guide-on-how-you-can-wash-your-linen`). **[script]**
- [ ] **Excerpt** filled in (1–2 sentences, ~150–300 chars) — themes show it on blog index and social previews. **[script]**
- [ ] **Tags** 2–5, chosen to group posts into topic clusters; reuse existing tags. **[script]**

## 3. Content structure
- [ ] One H1 = the article title (the theme renders it). **Body contains no `<h1>`.** **[script]**
- [ ] H2/H3s mirror real searched questions; logical hierarchy (no H3 before an H2). **[script: order]**
- [ ] **Answer first**: a direct 40–60 word answer as the first paragraph. **[script]**
- [ ] Skimmable: paragraphs ≤ ~4 sentences / ~80 words, lists, at least one table or comparison block. **[script: long paragraphs, table/list presence, runs of paragraphs with no list, numbered list for steps and rankings]**
- [ ] FAQ section: 3–6 real questions (PAA, forums, reviews, support). **[script]**
- [ ] Depth over length: typically 1,200–2,500 words, no padding. **[script]**

## 4. E-E-A-T
- [ ] Named author with short bio and credentials (author box at end of body; also set Author in Shopify).
- [ ] First-hand experience: brand testing notes, customer data, founder insight, original photos — or clearly marked placeholders.
- [ ] 3–6 citations to credible sources, linked inline. **[script: external link count]**
- [ ] Visible "Last updated" date near the top. **[script]**

## 5. Internal linking
- [ ] 2–4 product or collection links (`/products/…`, `/collections/…`) with descriptive anchors. **[script]**
- [ ] 2–3 related blog post links (`/blogs/…`), including the cluster pillar. **[script]**
- [ ] No "click here", "read more", "here" anchors. **[script]**
- [ ] Link-back plan: which product/collection pages should link to this post.

## 6. Media
- [ ] Images as WebP, ideally < 150 KB, descriptive kebab-case file names (`linen-duvet-care.webp`, not `IMG_2041.jpg`). **[script: file names]**
- [ ] Alt text on every image, describes the image; keyword only where natural. **[script]**
- [ ] Featured image 1200×630 for social sharing.
- [ ] Optional: embedded video (YouTube/Vimeo) when a process benefits from being shown.

## 7. Structured data
- [ ] `BlogPosting` JSON-LD (many themes output `Article` already — tell the user to check with Google's Rich Results Test and avoid duplicates).
- [ ] `FAQPage` when there's an FAQ; `HowTo` for step-by-step posts. Note: since 2023 Google shows FAQ rich results mainly for authoritative government/health sites and has retired HowTo rich results, but the markup still helps machines (including AI answer engines) parse the content. Add via theme code or an SEO app.
- [ ] `Organization` schema site-wide (theme layout), with `sameAs` social profiles — strengthens brand entity recognition.

## 8. Brand discoverability
- [ ] Brand name used consistently (exact spelling) 3–6 times, tied to the topic ("At Brand, we…"). **[script]**
- [ ] One plain entity sentence: "[Brand] is a [what] that makes [products] for [who]."
- [ ] At least one original, quotable asset: framework, checklist, comparison table, rule of thumb, or stat (brand-sourced or synthesized from cited sources — never invented).

## 9. Conversion and engagement
- [ ] Contextual CTA tied to the post's problem (product block, collection link, email signup) — not only a generic banner.
- [ ] Related-posts module at the end.
- [ ] Open Graph: featured image, SEO title and meta render correctly (Shopify uses these for `og:` tags) — test with a social preview debugger.

## 10. Technical hygiene (pre-publish checklist for the user)
- [ ] Mobile-friendly and fast — check PageSpeed Insights / Core Web Vitals.
- [ ] Post visible (not hidden), blog in `sitemap.xml` (Shopify generates it automatically).
- [ ] No other post targets the same primary keyword (cannibalization).
- [ ] Calendar a refresh (e.g. every 6–12 months; sooner for fast-changing topics) and update the "Last updated" date only when content actually changes.

---

## Writing notes

- **Answer-first paragraph formula**: [direct answer in one sentence] + [the key condition or number] + [what the post covers next]. Example: "Wash linen sheets in cool or lukewarm water (30–40°C) on a gentle cycle with a mild liquid detergent, then line-dry or tumble on low. Skip bleach and fabric softener, which weaken fibres and reduce absorbency. Below, we cover drying, ironing, stain removal and how often to wash."
- **Brand mention without sounding like an ad**: attach the brand to evidence ("In Brand's wash tests over 50 cycles…") rather than adjectives ("our amazing sheets").
- **Tables** beat prose for comparisons, specs, and "which is right for you" decisions — and they're lifted by snippets.
- **FAQ answers** should stand alone (repeat the noun, don't rely on "it") since they may be extracted.
