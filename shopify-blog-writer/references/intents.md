# Post intent: what is this post for?

The user picks one intent at the start. It decides the post type, where research goes, how the outline is built, which SEO rules matter most, and what the call to action does. Without it, every post gets forced into the same SEO-guide shape, which suits some goals and fails others.

Record the choice as `intent` in the fields JSON: `education`, `brand`, `search`, or `promotion`.

| Intent | Goal | Typical post types | Research emphasis | Call to action |
|---|---|---|---|---|
| **Education and support** (`education`) | Help customers use, choose or care for products; cut support questions | How-to, care guide, troubleshooting, FAQ, explainers | Customer questions (reviews, support, forums), accuracy of steps and facts | Soft: the product or collection that solves the problem, or the support page |
| **Brand and journal** (`brand`) | Build the brand's story, values and trust | Founder story, behind the scenes, sourcing, process, values, team | The brand's own material first (about page, interviews, notes). Light keyword research | Gentle: explore the collection, follow, sign up |
| **Search and AI visibility** (`search`) | Rank in Google and be cited by AI answers | Pillar guide, buying guide, comparison, "best X for Y", definitive how-to | Full keyword, SERP and gap research; PAA; sources | Contextual product block plus email signup |
| **Promotion and launch** (`promotion`) | Introduce or sell a product, collection or offer | Launch announcement, product spotlight, gift guide, seasonal edit, "why we made it" | The product's real specs and benefits, who it's for, objections, timing | Direct: product or collection links, offer details, deadline |

## Every post needs one clear call to action

Whatever the intent, the post ends with **one tangible next step** the reader can take, with a real link: shop a collection, book, read the next guide, download, subscribe or contact support. Pick it at the brief stage from the table above, not at the end. Put it in a `<div class="post-cta">` block with a link; `check_post.py` fails posts without one. Offers, dates and prices come only from the user or the live store.

## How each intent changes the work

**Education and support**
- Lead with the answer; steps are numbered; include a "common mistakes" or troubleshooting section.
- An FAQ section is expected. Prefer real customer wording.
- Claims need the most care here (care, safety, ingredients, health). Offer the fact-check.

**Brand and journal**
- Voice and first-hand detail matter most. Use brand.md and what the user provides; use `[[BRAND TO ADD: …]]` placeholders for real stories, quotes and photos. Never invent a founder story or customer result.
- Answer-first and FAQ are optional. A short, clear opening that says what the post is about is enough. Length can be shorter (600–1,500 words).
- Still set the SEO fields, 1–3 product or collection links, and tags.

**Search and AI visibility**
- Everything in `seo-standards.md` applies in full: answer-first, question-style headings, FAQ, table or comparison, sources, schema, 1,200–2,500 words.
- One primary keyword, secondary keywords, and the SERP gaps drive the outline.

**Promotion and launch**
- Open with the product's value to the reader, not a list of features. Be specific about who it's for.
- 2–5 product or collection links, each with a descriptive anchor; one clear primary call to action, repeated once near the end.
- Offers, dates and prices come only from the user or the live store; never guess them. If a deadline exists, put it near the top.
- Keep claims factual and qualified. An FAQ that answers purchase objections (sizing, shipping, ingredients, returns) helps.

## Mixed goals

If the user wants two things (for example a how-to that also promotes a product), pick the primary intent for structure and add the secondary one as a section, not a second post. Tell them what you did.

## When the user doesn't pick

In fully automated mode, infer from the topic: a "how to…" question → education, "best X for Y" or a keyword with search demand → search, a new product → promotion, a story or values topic → brand. State the inferred intent in the summary. For autopilot runs, the brief supplies it.
