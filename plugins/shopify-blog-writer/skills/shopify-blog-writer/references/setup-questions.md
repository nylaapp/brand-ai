# Setup questions

Setup gives the user control over the post's purpose, media, format, how involved they are, and where it ends up. It happens once, **before any research**. Brand facts are never asked here: they come from the store's BRAND.md (Step 0b in SKILL.md).

Use AskUserQuestion (max 4 questions per call). Put sensible defaults first and mark them "(Recommended)" where one clearly fits.

---

## 1. Setup round, call A (always)

**Q1 — Intent** (header: "Post intent")
> What is this post for?
- **Education and support** — how-tos, care guides, answering customer questions
- **Brand and journal** — your story, process, values, behind the scenes
- **Search and AI visibility** — rank in Google and get cited by AI answers
- **Promotion or launch** — introduce or sell a product, collection or offer

(If the user already stated a goal in the request, confirm it in your own words instead of asking. If the topic clearly implies one, for example a "best X for beginners" request implies search visibility, mark that option "(Recommended)" and put it first.)

**Q2 — Media** (header: "Images")
> Do you want to upload your own media, or should I pick it?
- **I'll upload my own** — I'll leave marked slots with a shot list (what each image should show, file names, alt text)
- **Pick free stock photos for me** — I'll choose from Unsplash and credit the photographers
- **Both** — use my uploads where I have them, stock for the rest

(Don't offer AI-generated images by default. They may need an "AI-generated" label that can be off-brand for many brands, especially medical or scientific ones. If the user asks for them, explain that, and treat it as an optional extra they set up themselves.)

**Q3 — Delivery** (header: "Delivery")
> Where should the finished post go?
- **Post to Shopify as a draft** — created hidden with title, formatting, excerpt, tags, images and SEO fields, ready to review and publish. *(Offer only if a Shopify connector or a browser tool is available. Say how: connector, or the user's signed-in browser.)*
- **Generate as HTML** — paste-ready HTML plus a fields sheet, to post to Shopify later.

**Q4 — Mode** (header: "Mode")
> How involved do you want to be?
- **Fully automated** — no more questions after this; I research, write and deliver, and list any assumptions.
- **Guided** — you choose which questions to answer and where to review.

## 2. Setup round, call B (as needed)

**Q5 — Format** — only if the blog has at least 3 published posts. Wording and options: `house-style.md` §1.

**Brand and topic** — in plain text, only for what's missing:
- Which store, only if it isn't clear from the request or the connected folder (skip if BRAND.md or the conversation already has it)
- The topic, or "suggest topics"

Then **identify the store and load its BRAND.md** (Step 0b in SKILL.md). Competitors, inspiration brands, claim limits, voice and author are never asked: they are in BRAND.md. The only brand-related question allowed is "which store is this for?" when several clients are present and the request doesn't say. If BRAND.md is missing, Step 0b applies: stop and offer brand-capture; don't interrogate the user. If BRAND.md is `draft`, mention in one line that some lines are unconfirmed and which ones you rely on.

**If the draft goes through the browser**, check right away that the browser is signed in to the right store's Shopify admin (`publishing.md`, Option 1B). If not, ask the user to sign in themselves; if they can't, switch to HTML.

These setup questions are the only required ones. Nothing else is asked after the setup round in fully automated mode.

---

## 3. Guided mode: the question menu

One AskUserQuestion call with two multi-select questions:

**The no-repeat rule.** Never ask, in any mode, what is already established: in the user's request, in an earlier setup answer, in BRAND.md, or implied by the intent. Check those first; ask only the gap, and only once. Specifically, guided mode has **no** voice, tone, author, topic or keyword question:
- Voice, tone, author and brand facts come from BRAND.md (or the defaults in §4).
- The topic was already asked in setup (call B) or given in the request. If the user chose "suggest topics", offer 3–5 researched options as a choice, not as a menu group.
- Keywords come from research and are shown in the brief; the user changes them at the brief checkpoint if they want. If they supply a keyword list or Search Console data, use it.
The user can still change any of these unprompted ("use a different tone this time", "target this keyword"); then follow their instruction.

Guided mode is a guide, not a permission prompt: don't ask "do you want to be involved?". Offer concrete options (topics, outlines, images) and ask for a choice.

**Q-A — "Which of these do you want to weigh in on?"** (only groups not already answered or established; anything not picked uses BRAND.md, discovered facts or defaults)

| Option | Questions asked if picked |
|---|---|
| **Products, links and CTA** | 2–4 products or collections to feature; related posts to link; blog handle; the CTA (default: chosen from the intent, see `intents.md`) |
| **Your own insights** | The first-hand asset the post is built around (testing notes, founder or maker story, a mistake you made, customer questions you keep getting, sales or return data, photos); your point of view on the topic and who it's not for; customer reviews; survey or usage data; certifications; claims you can't make |

**Q-B — "Where do you want to review before I continue?"** (multi-select; none = no pauses)
- **Approve the brief and outline** (before writing)
- **Pick the images** (2–3 candidates per slot)
- **Review the finished post** (before delivery)

Ask the chosen groups' questions in as few calls as possible, each with a default option.

---

## 4. Defaults (anything unanswered)

- Intent: inferred from the topic (`intents.md`), stated in the summary
- Media: pick free stock photos
- Format: `match-layout` for education and search, `match` for brand and promotion; `best-practice` if the blog has fewer than 3 posts (when the post count can't be checked, use the intent default)
- Author: BRAND.md's Blog byline or Author, else "The [Brand] Team" with a placeholder bio (never asked in guided mode)
- Voice: BRAND.md Voice and Terminology, else matched to the store's home and about pages and flagged as an assumption, else clear, warm, expert, second person
- Market: BRAND.md `markets`, else the shop's country; never assume one
- Disclaimer: BRAND.md's required blog disclaimer, verbatim, if it names one
- Blog handle: the store's existing blog, else `news`
- Topic (if "suggest topics" in automated mode): the strongest researched option by brand fit and visible demand
- Links: real products, collections and posts found on the store; leave out any link you couldn't verify
- CTA: one clear next step chosen from the intent (`intents.md`), pointing at the most relevant collection, product or page
- First-party data: left out of the post and listed under missing input in the summary; never invented
- Delivery: HTML if not asked and not an autopilot run

## 5. Discovering facts from the store

For store facts BRAND.md doesn't cover (current products, collections, posts), fetch them fresh for this run only; log brand gaps in `BRAND-REQUESTS.md`:

| URL | What it gives you |
|---|---|
| `https://<store>/` | Voice, positioning, main collections |
| `https://<store>/pages/about` (or `/about-us`, `/our-story`) | Founder story, mission |
| `https://<store>/products.json?limit=250` | Products to link (also checked fresh each post for new items) |
| `https://<store>/collections.json` | Collection handles |
| `https://<store>/sitemap.xml` → `sitemap_blogs_*.xml` | Every existing post (for duplicates and cannibalization; checked fresh each post) |
| `https://<store>/blogs/<handle>.atom` | Recent posts (house style scan) |

If a Shopify connector is connected to this store, read-only queries on products, collections, blogs and articles are fine in any mode.
