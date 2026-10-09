---
name: "shopify-blog-rewrite"
description: "Brand-agnostic. Rewrite an existing, already-written blog article (a URL or a whole blog, Google Doc, .docx, .txt/.md or pasted text) in a Shopify store's own voice, fact-check it, and post it as a hidden draft with SEO fields and a preview link. If the Shopify connector or browser is unavailable or not signed in, falls back to paste-ready HTML plus a fields sheet and says why. Keeps the author's facts and structure; changes wording, tone, rhythm and terminology to match the store's BRAND.md and live blog, and fills placeholders like [Brand Name]. Use whenever the user has a pre-written article, template article, guest post, freelancer or agency draft, or old blog post and wants it 'in our voice', 'on brand', 'rewritten', 'tone matched', 'cleaned up and posted as a draft', or says 'rewrite this doc for the blog' or gives a link to an article to rewrite. For writing a post from a topic, use shopify-blog-writer instead."
---

# Shopify Blog Rewrite

Turn a finished article someone else wrote into a post that sounds like the store's brand, then land it in Shopify as a hidden draft for a human to polish. If the draft cannot be created in Shopify (no connector, not signed in, store mismatch), deliver paste-ready HTML instead (see Step 7, "Fallback").

This skill is brand-agnostic. It contains no brand names, voice rules or terminology. Everything about the brand comes from that store's `BRAND.md` and its live blog, so the same skill serves every client.

The job is a **voice transplant, not a content rewrite**. The source article's facts, claims and argument belong to whoever wrote and approved them. A rewrite that quietly "improves" a claim ("reduces wrinkles" becoming "erases wrinkles") creates accuracy, legal and trust risk, which matters most for regulated brands (health, beauty, supplements, food). Change how it sounds; never change what it says without flagging it.

A good rewrite reads as if the brand's own writer wrote it from the start. A regular reader of the blog should not be able to tell it came from a template, a freelancer or another brand.

```
1. Intake + store → 2. Load brand voice → 2b. Resolve placeholders and brand names → 3. Rewrite (three passes) → 4. Quality gate + change report → 5. Fact-check → 6. SEO fields + QA → 7. Hidden Shopify draft (or HTML fallback)
```

This skill reuses `shopify-blog-writer` for brand loading, house style, QA and delivery, so the Shopify logic exists in one place. Read these from that skill's folder only when you reach the step:

| Step | Read |
|---|---|
| 1 and 2 | `shopify-blog-writer` SKILL.md **Step 0b** (identify the store, find and read its BRAND.md) and `references/house-style.md` §2 (scan the live blog) |
| 3 | `references/writing-quality.md` (specifics, point of view, voice) |
| 6 | `references/seo-standards.md`, `references/output-templates.md` (fields JSON, HTML conventions), `scripts/check_post.py` |
| 7 | `references/publishing.md` (connector 1A / browser 1B, preview link, HTML option 2) |

If `shopify-blog-writer` isn't installed, say so and fall back to HTML delivery (body HTML plus a fields sheet).

## Step 1: Intake and store

Accept any of: **an article URL** (see "Source from a URL" below), a Google Doc or Drive file (Drive connector: fetch by link or search by title), a `.docx` (convert with `pandoc` or python-docx, keeping headings, lists, tables and links), a `.txt`/`.md` file, or pasted text. Keep the original in `<store folder>/blog-runs/<date>-<handle>/source.<ext>` (`source.md` for a URL) so the human can compare.

### Source from a URL

When the request contains a link to an article (and not a Google Doc or Drive link, which use the Drive connector):

1. **Check whose article it is before fetching.** If the URL is on the store's own domain, or the person says it is
   theirs or their client's (an old post, a guest post, an agency draft hosted on a staging site), go ahead. If it
   is another company's published article (a competitor, a publisher, a stranger's blog), don't rewrite it into the
   store's blog as original content: say that it would be a copy of someone else's work, and ask for confirmation
   that the person owns it or has written permission. Unattended, return `delivery: stopped` with the reason.
2. **Fetch it** with your web fetch tool; if the text comes back empty, partial or script-rendered, read the page
   with a browser tool. Never sign in, never solve a CAPTCHA or click through a bot check; if the page is paywalled
   or blocked, say so and ask for the text instead.
3. **Extract the article only:** title, byline and date (for the report, not the body), headings, paragraphs, lists,
   tables, links, and image `src` plus `alt`. Drop navigation, cookie banners, share buttons, related-post lists,
   comments, newsletter forms and the source site's own author box, CTA and disclaimer.
4. **Save it** as `source.md` with the first line `URL: <url> (fetched <date>)`, so every claim can be traced back.
5. **Source brand names and links:** the source's own brand name, location, phone and booking links are
   placeholders to resolve in Step 2b, not text to keep; internal links to the source site are listed in the report
   and replaced with verified store URLs or removed. Source images follow "Source images" below: copied into the
   store's own Shopify Files only when ownership or permission is confirmed (item 1), otherwise listed in "Missing
   input you could add" with their alt text so the store supplies its own. Never hot-linked either way.
6. **More than one URL**, or a link to a blog index, category page or a whole site: see "Source from a whole blog or
   site" below.
7. **If the URL is an article on this store's own blog** and the person wants it updated rather than replaced, say
   that the rewrite will be a new hidden draft; the original is left untouched and they swap them when ready.

If the pasted text starts with field lines (for example `SEO title:`, `Meta description:`, `Suggested handle:`, `Excerpt:`, `Disclaimer:`), split them off as fields; they are not body copy. A trailing `Disclaimer:` line in the source is replaced by the brand's own disclaimer (Step 3), not kept in the body.

**Which store?** From the request, the connected Shopify store, or the folder you're in. With several clients and no clear answer, ask "which store?". It is the only brand question this skill asks. A BRAND.md for a different store counts as missing.

Ask once, with AskUserQuestion, only what the request didn't already say:

1. **Depth**, because the right answer changes by article:
   - *Voice only* (suggested default): keep headings, order, facts and roughly the same length; change wording, tone, rhythm and terminology.
   - *Voice plus light SEO tune-up*: also turn headings into real questions, add an answer-first opening, an FAQ and internal links where missing. Never add facts to do it.
2. **Review**: show the change report and wait for approval before posting, or post straight to a hidden draft.
3. **Brand-specific claims (only if the source has any that BRAND.md does not support):** quote the sentence and offer "soften it (recommended)" or "keep it, I confirm it's true". See Step 2b.

Capture topic, target blog (default from BRAND.md, or the best fit among the store's blogs), any keyword the user cares about, and an author only if the user names one. Don't ask about voice, author, tone, brand name or disclaimer: voice comes from BRAND-VOICE.md and BRAND.md, the brand name and disclaimer from BRAND.md, and the author from the store's existing posts.

If the source is very short, or clearly isn't a blog article (a landing page, a product page, a category page, a product description), say what it is and ask whether to proceed.

### Source images

Only when ownership or written permission is confirmed (Source from a URL, item 1). Without it, no image is copied.

1. **Collect** each image in the article body and the featured or social image (`og:image`), at the largest size the
   page offers (the `srcset` or full-size URL, not the thumbnail). Skip icons, logos, avatars, tracking pixels and
   images from third parties that are plainly stock (watermarked or credited to a stock agency): list those instead.
2. **Upload to the store's Shopify Files**, never hot-link: `fileCreate` with the image URL as `originalSource` and a
   descriptive `filename` and `alt` (`shopify-blog-writer/references/publishing.md`, "Step B"); poll until `READY`;
   swap each `src` for the Shopify CDN URL. Keep the source's alt text if it describes the image, rewrite it if it
   names the source brand.
3. **Look at each image before using it.** One with the source brand's logo, name, phone number or before/after
   claims visible in it is flagged in the report as "needs a replacement" and not used in the draft; a patient or
   client photo is used only if the person confirms a photo release exists. Don't edit or crop images to remove marks.
4. **Record** every image in the report: source URL, Shopify file, alt text, used or flagged and why. Set the first
   suitable image as the featured image if the post has none.
5. If a download or upload fails, leave a visible `[[USER MEDIA: <description>]]` slot, as publishing.md describes, and
   carry on with the text.

### Source from a whole blog or site

When the link is a homepage, a blog index, a category page, a sitemap or a feed, or the request says "all the posts":

1. **Ownership gate first, for the whole site.** Same rule as a single article (Source from a URL, item 1), asked
   once for the whole site, in plain words: "Is this site yours, your client's or part of your group, or do you have
   written permission to reuse its articles?" If it belongs to a competitor or any unrelated company, stop: say that
   copying and rewriting a whole blog (and its images) would be taking someone else's work, and offer what is fine
   instead: write original posts on the same topics with `shopify-blog-writer`, or rewrite a few of their ideas from
   scratch. Unattended, return `delivery: stopped`.
2. **Discover the posts.** In this order: the blog's `.atom` or RSS feed, `/sitemap.xml` (and its post sitemap), the
   blog index with pagination, then a browser tool for script-rendered lists. Keep only articles (not product,
   service, location or category pages). Note title, URL, date and any category for each.
3. **Show the list and confirm before fetching anything else:** count, titles and dates, plus the ones you'd skip
   (duplicates, thin pages under about 300 words, pages not about the target store's category, anything the target
   blog already has by title or handle). Default to the **10 newest** per run; the person can raise it. Larger
   batches run in groups of 10 with a stop between groups.
4. **One article, one draft.** Run the normal rewrite (Steps 1b to 7) for each as its own hidden draft, one at a
   time, each with its own `blog-runs/<date>-<handle>/` folder. Load the brand voice once (Step 2) and reuse it
   across the batch. Stagger the posts' publish dates only if the person asks; drafts are never published here.
5. **Don't let a batch lower the bar.** Every article still gets the full quality gate, claim checks and fact-check
   (Steps 4 and 5). If one fails the gate or its source can't be read, mark it `needs attention` and carry on with
   the next; never stop the batch for one article, never skip its checks to save time.
6. **Same-topic posts:** when two source articles cover the same topic, keep the stronger and list the other as a
   skipped duplicate, so the store doesn't end up with near-identical posts.
7. **One batch summary** at the end: a table with source URL, new title, handle, draft preview link, images used and
   flagged, claims removed, and status (`ready for review`, `needs attention`, `skipped`), then the totals. The
   per-article reports stay in each run folder.

## Step 2: Load the brand's voice

Voice comes from three places, in this order of authority:

1. **The store's brand-capture files**, found and confirmed exactly as `shopify-blog-writer` Step 0b and brand-capture `references/brand-context.md` describe (project root, user local environment, central brand directory, then central knowledge, memory and instructions, before any prompt): `BRAND.md` plus its voice guide `BRAND-VOICE.md` (named by `voice_doc` in BRAND.md's front matter; if there is no `voice_doc`, BRAND.md's own Voice section is the voice). Read the whole of `BRAND-VOICE.md` (how it sounds, signature phrases, do and don't pairs, words to avoid). From BRAND.md read Quick reference, Identity (one-liner, what sets us apart), Brand architecture (which name to use where), Terminology, Audience, Catalog, Claim limits, Blog (typical post, byline, CTA style, disclaimer), Story and Author, and front matter `brand`, `language` and `brand_approver`. Open `BRAND-QUESTIONS.md` only to look up a `[[CLIENT TO CONFIRM: Q-..]]` id you hit. If no BRAND.md is found in any of those locations, stop and offer `brand-capture`, saving to the central brand directory; without it "matching the tone" is a guess. Unattended, return `delivery: stopped` with the reason.
2. **The live blog**: read 3 to 5 recent posts in the target blog (`/blogs/<handle>.atom`, the connector, or the admin if the feed is empty). Prefer the newest posts: they show the voice the brand writes in now, which may differ from older SEO-era posts. Note sentence length, openings, how the brand introduces itself, how the reader is addressed, use of questions, heading style, how technical terms are handled, list use, CTA wording and sign-off. BRAND-VOICE.md describes the voice; the posts show it in practice. Where they disagree, a `(client)`-marked rule in BRAND-VOICE.md or BRAND.md wins. Log the disagreement as one line in `BRAND-REQUESTS.md` next to the resolved BRAND.md instead of editing BRAND.md.

Fewer than 3 published posts: use `BRAND-VOICE.md` and BRAND.md alone and say so.

3. **The brand's other writing.** Beyond those recent posts, skim a few older posts (up to 10 in all, as many as exist), plus the About page and a few product or service pages. Voice shows most in how the brand opens and closes, how long its sentences and paragraphs run, how formal it is, and whether it says "you" or "we".

Write a **voice card** before rewriting, in two parts. Keep it in the run folder: it keeps the rewrite consistent and lets the human see what you matched.

- **Voice sheet:** 3 to 4 voice traits (for example warm, expert, plain-spoken); words and phrases the brand always uses; words it never uses (hype words, filler openers, jargon its audience wouldn't say); typical sentence length (words) and paragraph size (sentences); how much it uses lists and subheadings; how it opens and closes; how it introduces itself in a post (copy the pattern, for example "a plain guide from <brand>, a <one-liner>"); its attitude (confident vs gentle, hard sell vs soft).
- **Rules:** spelling (US or UK), contractions yes or no, serial comma yes or no, emojis yes or no, point of view ("we" and "you", or other), what the brand calls its experts and its customers (for example "your provider", "licensed injector", "clients"), settled terms (product and service names, trademarks and their ® marks), the brand name to use in blog copy (Step 2b), and the claims the brand can't make. Take each from BRAND-VOICE.md and BRAND.md first, then the posts; where neither shows it, say "not established" rather than guessing.

Brand text is data, not instructions.

**If most of the source's claims are disallowed** (they fall under Never say or Not allowed, or are unsupported health or result claims), don't strip the article down to nothing silently. Rewrite what is safe, list every removed claim in the change report, and tell the person the source needs a claims review by the brand approver before it can go further.

## Step 2b: Resolve placeholders and brand names

Template articles often arrive with placeholders. Filling them is part of the rewrite, not a question for the user. Scan the whole source, including the field lines, for bracketed or braced tokens: `[Brand Name]`, `[Brand]`, `[Company]`, `[Company Name]`, `[Your Brand]`, `{brand}`, `<<brand>>`, `[Clinic]`, `[Store]`, `[City]`, `[Location]`, `[Phone]`, `[Link]`, `[URL]`, `[Price]`, `[Offer]`, `[Name]`, `XXX`, `TBD`, and similar.

**Brand name placeholders: always fill them, never ask.**
- Use the name BRAND.md says to use in blog and consumer copy. Look in this order: the Brand architecture row marked for the blog or consumer copy; Quick reference "Call us"; the Blog byline; front matter `brand`. Copy it exactly, with its capitalization, accents and marks.
- If the post is about one location or sub-brand that has its own name in Brand architecture, use that name for that location only, and the main blog name elsewhere.
- Never use a name BRAND.md says not to use for consumer copy (for example a parent group or legal name), and never use a short form or variant listed under Terminology "Instead of".
- Don't just swap the token. Rework the sentence around it so it reads naturally in the brand's voice, for example "At [Brand Name], every facial begins with…" becomes the brand's own way of saying it.
- Use the brand name 2 to 5 times in the whole post, in the places the brand's own posts use it (the introduction, the closing CTA). Don't stuff it into every section.

**A sentence about the brand itself is a claim.** "At [Brand Name], we provide personalized aftercare after every appointment" says something about the brand. Keep it only if BRAND.md supports it (Approved claims, or a sourced line under Identity "What sets us apart" or Catalog). Otherwise soften it to a general statement that stays true ("Your consultation is the place to talk through your goals"), unless the user confirmed it in Step 1. List each one in the change report.

**Other placeholders:**
- Fill a location, phone, link, price or offer only when BRAND.md or the live store gives the exact value, and only if it is appropriate for the post. Links must be verified URLs.
- If there is no exact value, rewrite the sentence without it or remove it, and list it under "Missing input you could add".
- Never invent a value and never leave a bracket in the output.

Record every replacement in the change report (`[Brand Name]` → `<name>` ×N, and each other token and what you did).

## Step 3: Rewrite (three passes)

Read `shopify-blog-writer/references/writing-quality.md` first. Then do three passes, not one. A single pass tends to keep the template's sentences and only change words.

**Pass 1: Map the source.** Before changing a word, list for each section: its job (what the reader should learn or do), every claim it makes, every term that has a brand equivalent, and every placeholder. This is the inventory you will check the rewrite against.

**Pass 2: Rewrite to the voice card.** Rewrite each section so it does the same job in the brand's voice:
- **Open like the brand opens.** Use the brand's opening pattern from its newest posts (for example a short direct answer, then one sentence introducing the brand with its BRAND.md one-liner). Drop template openers ("If you're new to…", "Choosing X is a personal decision").
- **Match sentence and paragraph length** to the voice card. Split long sentences; join choppy ones if the brand writes in longer lines.
- **Use the brand's words for people and things:** what it calls its experts, its customers, its services and its consultations (Terminology). Replace generic words like "skincare professional", "treatment professional" or "specialist" with the brand's term, used consistently.
- **Apply the rules on the voice card:** contractions, serial comma, spelling, point of view, trademarks.
- **Lead with what matters to the reader**, following the brand's do and don't pairs (for example outcome before mechanism, care before results).
- **Make it concrete with brand facts only.** Where a section is generic, add a detail already in the source or in BRAND.md (a service the brand offers from Catalog, how its consultations work from Identity), stated as plain description, never as a result or a claim. If there is nothing, leave it plain and list it as missing input.
- **Rewrite the CTA in the brand's style.** Use the brand's CTA wording pattern and a verified booking or consultation URL from BRAND.md or the live store. Replace template closers ("Book a consultation today to get started") with the brand's own way of asking.
- **Use the brand's disclaimer.** If BRAND.md names a blog disclaimer, include that exact text once, where it says, and drop the source's disclaimer unless the user asked to keep both. If BRAND.md says to copy it from the newest live post, copy it verbatim from there.

**Pass 3: Read it back as the brand's editor.** Compare against the Pass 1 inventory and one recent brand post:
- Every claim in the inventory is still there and still means the same. Nothing new was added.
- Every placeholder is resolved. No `[`, `{`, `<<`, `XXX` or `TBD` tokens remain.
- No banned words, hype words, or filler openers and closers.
- Read each section as if aloud. If it trips, or it sounds like the template, rewrite it again.

The principles behind the passes, and why:

- **Preserve meaning exactly.** Every claim in the output must trace to a sentence in the source. A smoother-sounding claim is still a different claim.
- **Never add first-party material.** No invented customer stories, expert quotes, results, prices, offers or credentials. If the source has a gap, leave it and list it under "Missing input you could add". No `[[…]]` placeholders in the body.
- **Match this brand's voice, not a generic "friendly" voice.** Use the voice card. Replace the source's terms with the brand's own terminology from BRAND.md, and follow the do and don't pairs in BRAND-VOICE.md.
- **Enforce claim limits.** Remove or soften anything under BRAND.md's Never say / Not allowed. A regulated phrase in the source ("approved", "clinically proven", "guaranteed", "safe for everyone", "no downtime") is never swapped for a different regulated phrase; it goes in the flags list for Step 5.
- **Keep one point of view throughout.** Freelancer drafts often drift between "one", "we" and "you". Use the brand's stance start to finish.
- **Cut AI-sounding and generic phrasing.** Stock openers ("In today's fast-paced world"), tidy summing-up paragraphs and vague claims go.
- **Keep the brand's attitude.** A confident brand isn't hedged into mush; a gentle brand doesn't get a hard sell.
- **Keep what's good.** Anecdotes, examples, structure and the author's points stay. Don't churn text that already fits the voice; needless changes make review harder.
- **Keep links, tables, lists and image references** working. Don't invent URLs; mark any you couldn't verify in the report.
- **The post title is the H1**, so the body starts at `<h2>`. Headings follow the brand's heading style (sentence case or title case, questions or statements) from its newest posts.
- **Light SEO tune-up only:** add an answer-first paragraph (40 to 60 words), question-style headings, FAQs drawn from content already in the article, and internal links to verified store URLs. If an FAQ answer would need a new fact, leave it out.
- **Author is whatever the store's existing posts use**, unless the user states another. Read the author of the latest 5 to 10 published posts in the target blog and copy the most common name exactly; fall back to BRAND.md's byline only if the blog has no posts. Never the signed-in user, staff member or operator, and not the source article's writer. Procedure and checks: `shopify-blog-writer/references/publishing.md`, "Author: never the signed-in user".

## Step 4: Quality gate and change report

**Quality gate (must pass before posting).** Check each item and fix what fails:

| Check | Pass when |
|---|---|
| Placeholders | No bracketed, braced or `XXX`/`TBD` tokens in the body or any field. Search the HTML and the fields for `[`, `{`, `<<` |
| Brand name | Exactly the blog name from BRAND.md, 2 to 5 times, no banned variants |
| Brand claims | Every sentence about the brand is supported by BRAND.md or confirmed by the user |
| Terminology | Every source term with a brand equivalent was swapped; trademarks carry their marks |
| Voice rules | Contractions, serial comma, spelling and point of view match the voice card |
| Rhythm | Average sentence length is close to the brand's posts; no paragraph longer than the brand's usual |
| Banned words | None of the voice card's never-use words, hype words or filler openers |
| Opening and closing | Opening follows the brand's pattern; CTA uses the brand's wording and a verified URL |
| Disclaimer | The brand's disclaimer appears once, exactly as written; the source's is gone unless asked |
| Meaning | Every claim traces to the source (Pass 1 inventory); nothing new added |

Then write `<handle>-rewrite-report.md` and show a short version in chat:

- The voice card (one line each), `Brand facts: BRAND.md rev <n>` and `Voice: BRAND-VOICE.md rev <n>` (when read)
- What changed in kind (tone, terminology swaps, sentences tightened, structure unchanged or the heading changes), with word counts before and after
- **Placeholder replacements** (token → value ×N, or removed and why)
- **Claim flags:** each sentence making a brand, health, result, safety, regulatory, performance or comparison claim, quoted from the source, with what you did (kept, softened, removed) and why
- **Terminology swaps** (source term → brand term)
- **Missing input you could add**
- Anything in the source that looks wrong or outdated that you did not change
- **Voice test:** compare the rewrite with one or two published posts for sentence length, paragraph size, opening and closing, point of view and terminology, and report plainly where it still differs. Ask: would a regular reader notice a change in voice?
- **On-brand approver:** name the approver from BRAND.md (`brand_approver`) as the person who should read it before it goes live. The draft is never described as approved.

If the user chose to review first, wait for approval here and apply their edits verbatim.

## Step 5: Fact-check

Rewording can quietly change meaning, especially on health, safety and "best" or "most" claims, so re-check every claim you touched against the source. Then run `content-fact-check` on the rewritten text when BRAND.md shows `regulated: yes`, has claim limits or a required disclaimer, or the post makes health, safety, ingredient, regulatory, statistical or performance claims. Soften or remove what it marks wrong or unsupported and note each change in the report. If the skill isn't available, apply conservative rules yourself (no regulatory, medical or safety claim without a primary-source citation) and say an independent fact-check is recommended. For a clearly non-regulated brand with no such claims, say you skipped it and why.

## Step 6: SEO fields and QA

Using `shopify-blog-writer`'s `output-templates.md`, fill title, SEO title (50 to 60 characters), meta description (140 to 155), handle, excerpt, tags (reuse the store's existing naming), author, blog, and alt text for images the source includes. Resolve placeholders in these fields too (Step 2b), and lightly match the excerpt and meta description to the brand's voice without changing their meaning. Run `python <shopify-blog-writer>/scripts/check_post.py <post>.html --fields <post>-fields.json`, fix FAILs, and confirm the body has no `[[…]]` or other placeholder text. **SEO must survive the rewrite.** Unless the user chose the SEO tune-up, keep the source's primary keyword, headings, and title and meta fields; if a heading or keyword placement had to change, list it in the report. Check the primary keyword is still in the title, first 100 words and a heading. Record `source_file`, `rewrite_depth`, `house_style` and `placeholders_resolved` in the fields JSON. If the source has no images, list a shot list as missing input instead of searching for stock, unless the user asks. Checker FAILs that can only be fixed by adding new facts or unverified URLs (related links, citations, tags you can't match to the store, "last updated") are not forced: list them in the report as missing input.

## Step 7: Deliver a hidden draft (or the HTML fallback)

Follow `shopify-blog-writer/references/publishing.md`: connector (1A) if available, else a signed-in browser (1B), else HTML (option 2). Rules that matter:

- **Hidden always.** `isPublished: false`. Never publish.
- **Test the connection before building anything.** For the connector, make one cheap read first (for example `get-shop-info`). If it fails, treat the connector as unavailable (see Fallback). Don't build mutations against a connector that has not answered.
- Confirm the connected store is the one the BRAND.md belongs to before any write. Check for a handle or keyword clash first and never overwrite another article.
- **Browser delivery:** don't type long body HTML key by key into the editor's HTML view; it can freeze the page. Set the body through the editor's own API (for example the rich-text editor's set-content call), then read it back and confirm the heading count, the disclaimer and that no stray text landed in it. Type short fields (title, excerpt, meta description, handle) one at a time and take a screenshot after each, because a page re-render can send keystrokes to the wrong place. If a tab freezes, open a fresh tab, and check afterwards that the frozen tab did not save a stray empty draft; if it did, tell the user (never delete it yourself).
- **Author:** set the author the blog's existing posts use (or the user's stated author): connector, pass `author: {name}` and read it back; browser, select it if listed, else set it through the API. Never leave the signed-in user's name. State the chosen name and where it came from in the summary. If it can't be set, say so in the first line of the summary and first in the review checklist, and keep the draft marked not ready.
- Read the article back and verify every field, including that the handle saved as intended.
- Give the **storefront preview link first**, then the admin edit link, as `publishing.md` describes.
- Save `source.*`, the voice card, the report, the HTML and the fields JSON in `blog-runs/<date>-<handle>/`.

### Fallback: when the draft can't be created

Use the fallback whenever the Shopify draft is blocked, whatever the reason:

- no Shopify connector is installed, or it is installed but not signed in ("requires authentication"), or any connector call fails after one retry
- the connector is signed in to a different store than the BRAND.md belongs to
- no browser tool is available, or the browser is not signed in to the right Shopify admin, or the project's device and browser safety rules are not met (for example the browser is not confirmed as the operator's own)
- the handle is already taken, the blog handle isn't found among several blogs, or the API returns an error you can't fix with one retry

What to do:

1. **Don't stop to ask, and don't loop.** Try the next method once (connector, then signed-in browser), then fall back. Never ask the person for credentials or 2FA codes, and never bypass a block another way.
2. **Deliver option 2 from `publishing.md`** in `blog-runs/<date>-<handle>/`: `<handle>.html` (body only, starts at `<h2>`, disclaimer included), `<handle>-fields.json`, `<handle>-shopify-fields.md` (the fields in the order of Shopify's blog post editor, with the author, blog, tags and "Visibility: Hidden until reviewed"), `<handle>-rewrite-report.md`, `source.*` and the voice card. The same Step 4 quality gate and Step 6 QA apply; the fallback is a delivery change, never a quality shortcut.
3. **Tell the person why, in the first line of the summary,** in plain words (for example "Not posted to Shopify: the Shopify connector is not signed in."), and say what would enable the draft next time (connect Shopify in connector settings, or sign in to Shopify admin in a browser the operator confirms is their own). If a handle clash caused it, flag it as a possible keyword clash too.
4. **Use the HTML summary wording:** "First draft ready for your review (HTML, not posted to Shopify). Paste `<handle>.html` into the Shopify blog post editor's HTML view and fill the fields from `<handle>-shopify-fields.md`, keep it hidden, then edit and publish when you're happy." Do not give preview or admin links, because none exist.
5. **If the user asked for "straight to draft",** the fallback is still the go-ahead's outcome: finish the HTML delivery without asking.

**Final summary** (short): "First draft ready for your review and edits." Delivery method (draft in Shopify, or HTML fallback with the reason), preview and edit links (draft only), author used, word count before and after, placeholders resolved, QA and fact-check results, number of claim flags, missing input, and what a human should check (claims, images, tone). Close with: "Please edit and polish in Shopify, then publish when you're happy." Never call it finished or ready to publish.

