# Research workflow

Six stages: **what people search → what already ranks → what the audience says → what the brand uniquely knows → what facts back it up → where it fits on the site.**

## What is saved, and what is researched every time

Don't pay twice for facts that don't change, and don't trust stale facts about things that do.

| Read from brand.md and competitors.md (captured once by other skills; never re-asked) | Researched fresh for every post |
|---|---|
| Brand identity, voice, audience, catalog topics | What ranks now: top results, PAA, SERP features, AI answers, gaps |
| The **list** of competitors (with feeds) and inspiration brands | The competitors' **latest** posts and what they cover now |
| Claim limits, regulated-category flags, required disclaimers | Current rules and status for any regulated claim in the post |
| Blog section (typical post, byline, default blog) | Statistics, studies and sources (checked for date) |
| Author and approver | Trends, seasonality, timing |
| competitors.md: positioning, pricing model, content cadence, openings (dated) | The store's **current** products, stock and existing posts (duplicates, cannibalization) |
| | Customer questions and objections (new reviews, forums, support data) |

Load the right store's brand.md first (Step 0b in SKILL.md), then competitors.md if it exists. If brand.md lacks something you need, don't ask the user a brand question: use the live store for non-brand facts, list the assumption, and add a `brand-requests.md` line. The intent (`intents.md`) sets how deep each stage goes: a brand journal needs little keyword research, a search post needs all of it.

Keep a running research log as you go (queries run, URLs, findings). Everything in the brief should trace back to it. Aim for depth proportional to the post: typically 8–20 searches and 5–10 page fetches.

---

## Stage 1 — Keyword and intent

**Goal:** one primary keyword with clear intent, plus 3–5 secondary/long-tail variants.

1. **Seeds** — from the brand's product categories, customer problems and use cases (e.g. a linen bedding brand: "linen sheets", "how to wash linen", "linen vs cotton", "best sheets for hot sleepers").
2. **Discovery** — use web search on seed phrases and variants ("how to…", "best … for …", "… vs …", "is … worth it", "why does my …"). Note which phrasings recur across results, titles and PAA boxes.
3. **Long-tail and questions** — capture "People Also Ask" questions, "Related searches" and autocomplete-style variants that appear in search results. AnswerThePublic-style patterns: who/what/why/how/can/does/vs/near/for.
4. **Intent** — classify: *informational* (learn/how-to → guide or how-to), *commercial investigation* (compare/best → listicle, comparison, buying guide), *transactional* (buy → usually a product/collection page, not a blog post). Match the format the top results use; Google has already told you what it thinks the intent is.
5. **Seasonality** — note if the topic is seasonal (gifting, summer care, back-to-school) and when to publish (4–8 weeks before peak).
6. **Brand fit (topic fit check)** — keep only topics the brand can credibly own, judged against the catalog and categories in brand.md and the live store. A post that ranks but has no path to the brand's products is wasted effort, and a post about something the brand doesn't sell damages trust. If the topic doesn't fit, stop and re-choose (guided: propose alternatives; automated: pick the closest fitting topic and say why). Never invent products to make a topic fit.

**Honesty rule:** without a keyword tool, don't state volumes or difficulty. Rank by visible evidence and write "volume: not verified" in the brief. If the user supplied tool exports, use those numbers and cite the source.

## Stage 2 — SERP and competitor analysis

**Goal:** know exactly what you must match and where you can beat it.

1. Search the primary keyword. For the top 5–10 organic results, fetch the pages and note: format (guide/listicle/comparison), approximate word count, H2 structure, depth, media (tables, video, images), date updated, and who publishes (brands, publishers, forums).
2. **Content gaps** — what do they miss, get wrong, leave outdated, or answer vaguely? Which PAA questions does none of them answer well? These gaps become your H2s and unique angle.
3. **SERP features** — featured snippet (paragraph/list/table?), PAA, video carousel, AI Overview, shopping results. Structure the post to compete: a 40–60 word answer for paragraph snippets, a numbered list for list snippets, a table for table snippets.
4. **Competitor brands** — use the competitors named in brand.md (don't search for new ones; if brand.md lists none, say so and add a `brand-requests.md` line). Read competitors.md first, if it exists, for their positioning, content cadence and the openings already identified, so this stage only adds what is new for this topic. Fetch each competitor's **latest** posts on this topic (their blog feed `/blogs/<handle>.atom`, sitemap, or a `site:` search) and note what they cover, how deep, and what they link to. The list is saved; what they publish is researched fresh every time. Note any inspiration-brand pattern worth borrowing as a *style cue* (structure, pacing), never wording.
5. **Link-earning patterns** — what makes the most-cited pages cite-worthy (original data, tools, definitive guides)? Plan one asset of that type.

## Stage 3 — Audience and voice-of-customer

**Goal:** the exact words customers use, their real questions, objections and misconceptions.

- **Brand's own data** (ask the user if not provided): reviews, support tickets, chat logs, return reasons, post-purchase surveys.
- **Communities**: search `site:reddit.com <topic>`, Quora, niche forums, YouTube comments. Capture verbatim phrasing (paraphrase in the post; don't quote users by name).
- **Social**: trending questions on TikTok/Instagram if visible via search.
- **Objections**: what stops people buying? What do they misunderstand about the category? Each objection is a candidate section or FAQ.

## Stage 4 — First-party and brand research (the E-E-A-T advantage)

**Goal:** the material only this brand can provide.

- Brand identity, voice and story: **read from brand.md** (Identity, Story, Voice); never re-scan the about page or home page for them.
- Store pages for the products this post features: current specs, materials, certifications, care instructions, price and stock (fetch fresh from product pages / `products.json`; these change).
- User-supplied: testing notes, internal expertise, customer data, before/after results, Search Console "page 2–3" queries (quick wins).
- If none is available, plan placeholders `[[BRAND TO ADD: …]]` at the points where first-hand experience would land hardest, and tell the user what to supply.

## Stage 5 — Fact and source research

**Goal:** every factual claim is accurate, current and citable.

- Prefer: government/regulatory sites, standards bodies, academic papers, industry associations, established publishers. Avoid citing competitors' marketing pages as authority.
- Check dates; use the most recent figures and say what year they're from.
- Claims check: health, safety, sustainability ("eco-friendly", "non-toxic"), performance ("lasts 2x longer") need substantiation. If you can't source it, soften or drop it.
- Regulated claims (regulatory status such as "FDA approved", medical, ingredient, pregnancy and safety statements): confirm against the regulator's own current records, not another blog. Status can change, so check it each time. For these, use the `content-fact-check` skill if available (`SKILL.md` Step 6).
- Aim for 3–6 cited sources in a typical post.

## Stage 6 — Site and cluster mapping

**Goal:** the post strengthens the site instead of competing with it.

1. **Cannibalization check** — search `site:<store> <primary keyword>` and scan the blog sitemap. If an existing post already targets this keyword, recommend refreshing it instead of writing a new one (and tell the user).
2. **Cluster fit** — which pillar topic does this support? Is this post the pillar or a supporting post? Pillar links out to all supporting posts; supporting posts link back to the pillar and to 1–2 siblings.
3. **Product/collection links** — pick 2–4 real product/collection URLs that fit naturally.
4. **Link-back plan** — which product/collection pages should link to this post.
5. **Tags** — reuse the blog's existing tags where they fit, so posts group into clusters rather than creating one-off tags.

---

## Research output → brief

Carry forward into the brief: post intent, keywords + search intent, SERP summary and gaps, customer language and questions, first-party material (or placeholders), sources with URLs, internal link map. See `output-templates.md`.
