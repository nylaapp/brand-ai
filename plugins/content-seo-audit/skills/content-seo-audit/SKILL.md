---
name: "shopify-post-publish-audit"
description: Post-publish SEO and AEO audit for Shopify blog posts. Checks the live page (structured data / Rich Results, PageSpeed Insights, title, meta, H1, leftover placeholders, indexing), then tracks real Search Console rankings about 2 and 4 weeks later. Use this whenever a Shopify blog post has just been published or made Visible, when the user says "I published the post", "check my new blog post", "audit the live post", "did the post get indexed", "how is the blog post doing in Google", or when a scheduled daily blog check fires. Use it even if the user does not say SEO. Works for any Shopify store or brand. Pairs with shopify-blog-writer, which writes the post; this skill checks it after it goes live.
---

# Shopify post-publish audit

## Effort (read before starting)

About 3 to 5 minutes and under $1 per post per check (publish day, week 2, week 4). Estimate, not yet measured. Stop and report if a check passes 15 minutes or $2.

A post can pass every check on the draft and still fail once live: a placeholder left in the text, a duplicate schema from the theme, slow images, or a page Google has not indexed. This skill checks the **live** page with Google's own tools and then follows the real ranking numbers over the next month. Real numbers matter because a self-made score only measures a checklist, while Google's tools measure what Google sees.

The reader is usually not a developer. Write reports in short, plain language and explain any technical word in a few words. Use the reader's language: `markets.language` or `audit.report_language` from the brand profile if there is one, otherwise the language the user writes in (plain English by default).

## Ground rules

- **Read-only.** Never edit, hide, unhide or publish any post, page or theme, and never touch old posts. Suggest fixes; the user decides.
- **No made-up numbers.** If a tool is blocked or not signed in, say so and ask the user to sign in or to paste an export. Do not estimate Search Console or PageSpeed numbers.
- **Never enter passwords** or 2FA codes. If Google or Shopify asks for sign-in, ask the user to do it.
- **Ask before "Request indexing"** in Search Console. It changes something in their account.
- Do not invent one big "SEO score". Report Google's numbers and pass / warn / fail checks.

## Step 0: Know which brand and store

This skill works for any Shopify store and holds nothing about a particular brand. Everything store-specific comes from the request or a brand profile. Work out the brand first:

1. **A scheduled or explicit request names the brand** and gives a store URL or a profile path. Use that.
2. **A brand profile exists** at `blog-autopilot/<brand-slug>/brand-profile.yaml` (made by the `shopify-blog-autopilot` skill). If so, read what it has: `brand.name`, `brand.slug`, `brand.store_url`, `shopify.blog_handle`, `markets.language`, `sources.search_console.property`, and an optional `audit:` block (see "Settings that can vary by brand" below). Use them; don't ask for what the profile already says.
3. **Otherwise ask once** for the store URL (and the Search Console property, if they want ranking checks). A scheduled run with no brand named can't ask: write a one-line "needs a brand" note and stop.

Derive the `brand-slug` from the profile, or from the store's domain in lowercase-kebab form. If the user has several stores, keep them fully separate. Never mix logs or reports between brands, and check that every post you audit is on that brand's domain.

Keep a small log at `blog-audits/<brand-slug>/log.json` in the user's working folder: `[{"url","handle","title","published_at","audits":[{"stage","date","file"}]}]`. Create it if missing.

## Step 0b: Find what to audit

Find posts in this order, and stop at the first that works:

1. A URL the user gave you.
2. The Shopify connector: query `articles(first: 10, sortKey: PUBLISH_DATE, reverse: true)` and keep those with `isPublished: true`. Follow the connector's GraphQL workflow (schema first, then validate).
3. The browser: open Shopify admin, Online Store, Blog posts, and read the newest rows with status Visible.

Then decide what is due, per post in the last 35 days:

| Stage | Due when | What to run |
|---|---|---|
| `day0` | Published, no audit yet | Step 1 |
| `week2` | 11 to 17 days after publish, no `week2` audit | Step 2 |
| `week4` | 25 to 31 days after publish, no `week4` audit | Step 2 |

Rules that keep scheduled runs quiet and cheap:
- **Never back-audit the archive.** On the first run, only take posts published in the last 7 days. Older posts, however many the store has, are not the job.
- **Skip Hidden drafts.** Only Visible posts are live.
- If nothing is due, reply in one line ("No new posts to audit today") and stop.

## Step 1: Day-0 audit (live page)

Use the user's browser (Claude in Chrome is preferred; the built-in browser also works). Open the post's public URL.

1. **Page is live.** It loads, is not a 404, and is not password-protected. A 404 usually means the post is still Hidden or the domain is not connected yet. Report that instead of continuing.
2. **On-page facts.** Run `scripts/extract_page.js` in the page (javascript tool). It returns title, meta description, canonical, robots, H1 count, heading list, JSON-LD types, image alt gaps, link counts, word count and any leftover `[[...]]` placeholders. Judge the results with `references/checks.md`. A leftover placeholder is a **FAIL**, because the public can read it.
3. **Rich Results Test.** Open `https://search.google.com/test/rich-results?url=<encoded post URL>`, wait for it to finish, and read the result text. Note detected items (BlogPosting or Article, FAQ) and any errors or warnings. If Google shows a captcha or a "verify you are human" step, tell the user to click it, then continue. Fallback: `https://validator.schema.org/#url=<encoded URL>`. Check for a duplicate Article/BlogPosting, which some themes add on top of a hand-added one.
4. **PageSpeed Insights.** Open any `pagespeed.web.dev` tab and run `scripts/psi_summary.js` (set the post URL first). It returns mobile and desktop scores for Performance, Accessibility, Best Practices and SEO, plus LCP, TBT and CLS. Google's free shared quota is often used up (HTTP 429). If so, use the page instead: open `https://pagespeed.web.dev/analysis?url=<encoded URL>&form_factor=mobile` and check the text every 15 seconds for up to 90 seconds. If it is still "Running analysis" or "loading" after that, do not guess. Mark PageSpeed as **"not available right now"** in the report, say why, and retry on the next run. Tell the user once that a free Google API key (Google Cloud Console, PageSpeed Insights API) removes this limit, and put the key in the script's `API_KEY` line only if they give it to you. Report lab numbers and, when shown, the "real user" field data; field data is usually empty for a brand-new page, so say so.
5. **Indexing.** If Search Console is open and signed in, use URL Inspection on the post URL. "URL is not on Google" is normal in the first days, so mark it WARN and not FAIL. Offer to request indexing, and only do it after the user says yes.
6. **Sitemap.** Check that the handle appears in the blogs sitemap linked from `/sitemap.xml`. It may lag a day; WARN, not FAIL.

## Step 2: Week-2 and week-4 ranking check

Use Search Console, Performance, Search results. Pick the property that matches the brand's store domain (the profile's `sources.search_console.property`, or ask; it may be a Domain property or a URL-prefix property). Filter Page contains the post handle. Set the date range from the publish date to today.

Capture: clicks, impressions, CTR, average position, and the top 10 queries. Check whether the post's primary keyword appears in the queries. Compare with the earlier audit for this post (read its saved file).

How to read it:
- **Under about 10 impressions at week 2:** probably not indexed or not yet trusted. Check indexing first.
- **Impressions but low CTR:** the title or meta description is not pulling clicks. Suggest a rewrite.
- **Average position 8 to 20:** close to page one. Suggest more internal links from older posts and a stronger answer near the top.
- **Nothing wrong at week 2:** say "too early" honestly. New pages move around for weeks.
- **Week 4** is the first check worth judging. Give a clear verdict and next steps.

If Search Console cannot be opened, ask the user for a screenshot or CSV export. Do not guess.

## Step 3: Report

Save to `blog-audits/<brand-slug>/<handle>-<stage>-<YYYY-MM-DD>.md`, update that brand's `log.json`, then show the user a short version. Use the layout in `references/report-template.md`. Lead with the verdict and the fixes, put the numbers after. End with the single most useful next step.

## Settings that can vary by brand

The defaults in `references/checks.md` suit a typical guide-style post. A brand profile can override them in an optional `audit:` block; use those values when present:

```yaml
audit:
  report_language: "en-US"        # language of the report; defaults to markets.language
  title_length: [50, 60]          # SEO title characters
  meta_length: [140, 160]         # meta description characters
  word_count: [1200, 2500]        # for guide-style posts; short posts (news, launches) aren't failed for length
  product_links: [2, 4]
  related_post_links: [2, 3]
  check_days: [14, 28]            # when to run the ranking follow-ups
```

Don't fail a post for something that only matters to one kind of post. A short launch note is not a guide.

## When this runs on a schedule

A scheduled run has no one to ask. If a step needs sign-in or a captcha, finish what you can, mark that step "needs you", and say exactly what to do. Never fail silently and never skip a due follow-up without saying so.

### Setting up the daily check for a brand

When a user asks for automatic checks, list existing scheduled tasks first (avoid duplicates), then create one per brand:

- name: `blog-audit-<brand-slug>`
- cron: daily at 9:00 local time unless the user or profile says otherwise
- prompt: `Run the shopify-post-publish-audit skill for brand "<Brand>" (store <store URL>, profile <path if any>). Scheduled run: no user is present, so don't ask questions. Audit only posts that are due, write the reports, and say what needs the user.`

Tell the user plainly: the check runs on their computer, so it needs to be awake with Claude open, and Google may ask them to sign in or click a captcha, which the run will flag rather than skip.
