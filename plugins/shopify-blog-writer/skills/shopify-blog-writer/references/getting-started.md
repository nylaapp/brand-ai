# Shopify Blog Skills: Getting Started

Four skills that work together to plan, write, check and follow up on blog posts for a Shopify store.

| Skill | What it does | Use it when |
|---|---|---|
| **shopify-blog-writer** | Researches, writes and delivers one SEO-ready blog post | You want a post written now |
| **content-fact-check** | Checks a post's claims (FDA and other regulatory wording, medical, ingredient, pregnancy, statistics) against official sources and suggests safer wording | Before publishing anything with health, beauty, treatment or product claims |
| **shopify-blog-autopilot** | Looks at your store, search data, reviews and the calendar, then **asks you each week** whether to write the best idea | You want a regular posting rhythm without it posting on its own |
| **shopify-post-publish-audit** | Checks a live post (schema, speed, indexing), then tracks Google rankings at 2 and 4 weeks | A post has just gone live |

New here? Start with **shopify-blog-writer**. Add the others later.

---

## 1. Before you start (2 minutes)

- [ ] **The skills are on.** Open Claude, go to **Customize > Skills**, and look under **Organization skills**. Switch on the skills above. If you don't see them, ask your Claude admin (see the last section).
- [ ] **Use Claude Desktop (Cowork) for the full experience.** Chat can write a post, but saving drafts through your browser and scheduled runs need the desktop app.
- [ ] **Shopify connection (recommended).** Connect the Shopify connector so Claude can save drafts straight into your store. Each person signs in to their own Shopify access.
- [ ] **No connector?** Install Claude in Chrome and stay signed in to Shopify admin. The skill can fill in the blog editor for you. It never types your password.
- [ ] **Your BRAND.md.** Set up the brand once with the **brand-capture** skill (about 10 to 25 minutes). It saves `BRAND.md` to the central brand directory (`$BRAND_AI_HOME/brands/<store>/`, default `~/.brand-ai/brands/<store>/`) and the skills also find it in your project folder or home directory: voice, audience, claim limits, competitors, inspiration brands and how your blog looks. Then run **competitor-research** to add `COMPETITORS.md`. The blog writer reads both and never asks about the brand again. Each store has its own folder and its own BRAND.md.

---

## 2. Write your first post

Type something like:

> Use shopify-blog-writer. Write a blog post for **[your store URL]** about **[topic]**.

Claude asks a few quick questions first, once, before it starts:

1. **What is this post for?** Education and support, brand and journal, search and AI visibility, or promotion and launch. This shapes the structure and call to action.
2. **Do you want to upload your own media, or should I pick it?** Free stock photos from Unsplash, your own images (it leaves marked slots and a shot list), or both.
3. **Where should it go?** A hidden Shopify draft, or paste-ready HTML to post later.
4. **How involved do you want to be?**
   - **Fully automated:** no more questions. It researches, writes and delivers, and lists anything it assumed.
   - **Guided:** you choose which open questions to answer (products and links, your own insights) and where to review (outline, images, final post). It never re-asks what your request, earlier answers or your BRAND.md already say, such as voice, author, topic or keywords.
5. **Should it match your existing blog posts?** Match them, match the layout but go deeper for search ranking, or use best-practice format. (Asked only if your blog has at least 3 posts.)

It never asks about your competitors, inspiration brands, claim limits, voice or author: those come from BRAND.md. If something is missing it adds a line to `BRAND-REQUESTS.md` for your brand owner. If there is no BRAND.md yet, it offers to run brand-capture first.

Then wait a few minutes. You get the post, with title, SEO title, meta description, URL handle, excerpt, tags, images, schema code and internal links, plus a short summary with a **list of placeholders** to fill.

**What it researches fresh every time:** what ranks now, your competitors' latest posts, trends and timing, statistics and sources, current rules on any regulated claim, and your store's current products and posts.

---

## 3. Before you publish

- **Fill the placeholders.** Anything like `[[BRAND TO ADD: ...]]` is something only you know (a founder quote, care-label facts, real customer data). The skill never invents these.
- **Fact-check it.** If the post makes health, treatment, ingredient, pregnancy or regulatory claims, run **content-fact-check** on it (the writer offers or runs it for you). It flags and verifies; it doesn't approve. A person should still review regulated claims.
- **Look at the images.** Check each stock photo fits, or add your own where slots are marked.
- **Drafts are always hidden.** Nothing goes live until you publish it in Shopify admin (Online Store > Blog posts).
- **Check links and facts.** Click the product links and skim the cited sources.

---

## 4. After it's live

Say: *"I published the post, check it."* The **post-publish audit** will check the live page (schema, speed, title and meta, leftover placeholders, indexing) and look at Google Search Console rankings about **2 weeks** and **4 weeks** later. It only reads. It never edits your posts.

---

## 5. Optional: a weekly check-in

The **autopilot** looks at new products, restocks, search data, reviews, competitors and upcoming occasions, then **asks you** once a week:

> Top idea: "..." Why now: ... What would you like to do? Write it for me / Let's do it together / Pick a different idea / Skip this week

Nothing is written until you answer. A week with no good idea is a quiet week with no message.

1. Say: *"Set up shopify-blog-autopilot for [your store]."*
2. Connect a folder when asked. It keeps your brand profile and a log of past posts there.
3. Answer the setup questions. It uses your BRAND.md and finds most answers from your store.
4. It creates a weekly scheduled check-in (Monday 9:00 by default). New drafts appear in Shopify as **hidden**, tagged `autopilot`.

**Good to know:**

- Scheduled runs only happen while your **computer is awake and the Claude app is open**.
- The weekly check-in uses far fewer credits than posting automatically every few days. If you do want hands-off drafting, ask for `auto_draft` in your profile.
- There's a weekly post limit, so you only review what you can handle.
- Try it first with *"Do a dry run of my blog autopilot"*. It shows what it would do without creating anything.

---

## 6. Tips to save usage

- One post uses a fair amount of usage (many searches and page reads). Don't ask for several posts in one go.
- Choose **Sonnet or Opus** for writing. Smaller models tend to write thinner posts.
- Give a specific topic and your store URL up front. It saves questions and research.
- Capture the brand once (brand-capture) so no run repeats brand research.
- Use **HTML delivery** if you don't need the draft in Shopify right away.

---

## 7. If something goes wrong

| Problem | What to do |
|---|---|
| Can't find the skills | Customize > Skills > Organization skills, and switch them on. Otherwise ask your admin. |
| "Shopify draft" isn't offered | Connect the Shopify connector or Claude in Chrome. Or pick HTML delivery. |
| It asks you to sign in to Shopify | Sign in yourself in the browser, then tell Claude to continue. |
| It stops because the topic doesn't fit your brand | It only writes about products and topics your brand really covers. Pick a topic from your catalog. |
| Draft couldn't be saved | It falls back to HTML files and tells you why (for example, the URL handle is already used). |
| Featured image missing | The browser method can't always add it, and "upload my own" leaves slots for you. Add it in the Shopify editor. |
| The check-in didn't reach me | Scheduled runs need the computer awake and the app open. The next run catches up. |
| The post doesn't match my blog's look | Re-run with the format question answered "match them", or say "rescan my blog style". |

---

## For your Claude admin

- **Where:** Organization settings > Plugins & skills. **Cloud code execution and file creation** and **Skills** must both be switched on (Policy tab).
- **Add a skill for everyone:** Add > Upload a skill (a .zip with a SKILL.md). It's available to all members straight away, on by default, and members can switch it off.
- **Only some teams:** on Enterprise, bundle the skills in a plugin and assign it to a group.
- **Connectors:** enabling one makes it available to everyone in the organization.
- **Brand file:** one `BRAND.md` per store, written by brand-capture, read by every other skill. Keep each store in its own folder. Lookup order: project root, your home directory, the central brand directory, then memory and connected knowledge (see brand-capture `references/brand-context.md`).
- **Updates:** re-upload a skill to update it for everyone.
