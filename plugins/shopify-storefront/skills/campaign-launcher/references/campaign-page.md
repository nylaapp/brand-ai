# Campaign page (a landing page for the campaign)

Use when the owner asks for a campaign landing page, or for a **design draft** (options side by side before the
homepage changes), or when the campaign's button needs somewhere to go and no page exists. It is an extra, never added
unasked. It uses the same facts as the plan (name, offer, exact dates, link), so the page, the bar and the hero can
never disagree.

**Building it is `page-create`'s job.** If the page-studio skill `page-create` is available, hand the build to it with
the region list below as the plan: it already handles the working copy, verification and shipping to a draft. If it
isn't, follow the steps here on the preview copy, with the same rules: reuse before building, no live edits.

## 1. Read the theme's own sections first

Never assume which sections exist. List `sections/*.liquid` and read each candidate's `{% schema %}` (setting ids,
blocks, presets). Honey: `references/honey.md` lists the colour groups and countdown; its marketing sections include
hero-image, hero-video, countdown, featured-collection, featured-product, collection-list, multicolumn, feature
cards, media with text, media grid, collage, video column, spotlight, shop-the-look, checklist, quotes, collapsible
content (FAQ), rich text, logo banner and email signup. Other themes: `references/other-themes.md`. Colours: Honey
picks one of five fixed groups with a section `background` setting; other themes pick a colour scheme.

If the theme has no page template for campaigns (Honey's are About, Contact, FAQ and default), the new template is
`templates/page.<slug>.json` (the campaign slug), and the Shopify page that uses it is created unpublished.

## 2. One section per region

Default order, dropping any region the campaign doesn't need:

| # | Region | Typical section | Notes |
|---|---|---|---|
| 1 | Hero or banner | hero-image / hero-video | Name, one supporting line, one button. Same text as the homepage hero |
| 2 | Offer and dates | rich text or multicolumn | The offer, exclusions, exact dates in shopper form ("Nov 27 to Dec 1") |
| 3 | Countdown (optional) | countdown | Only for a real deadline; ends at the plan's end time |
| 4 | Featured products or collection | featured-collection / featured-product | An existing collection or product; check it exists |
| 5 | Terms and FAQ | collapsible content | Exclusions, shipping, gift-card rule, how a code works |
| 6 | Closing call to action | rich text with a button, or a banner | The same link as the website button |

Every region is its own section, so swapping the hero means swapping one section. Blocks are only for repeated items
inside a region (cards, questions). Reuse an existing section, then the same section with one new setting; add a new
section only when no existing one produces the layout. No hardcoded colours, fonts or copy that a setting could hold.
Leave image pickers blank when image rights aren't confirmed.

## 3. Show it before the owner picks

Owners choose widgets they have never seen ("I thought it'd be a little '10 days until'"). Before building, show each
unfamiliar region as a screenshot or a link to an existing example in the theme (a store page, the theme demo). One
line per region: what it is, what it looks like. Where nothing can be shown, say so.

## 4. Copy

Write with `references/copywriting.md`, region by region. The facts never change between options.

**Design draft mode** (the owner wants to choose): give 2 or 3 copy options **per region** on one unpublished page,
labelled "Option A / B / C" in plain text sections the owner can see side by side, with the recommended one first
and one line on why it fits the voice. When they pick, rebuild the page with only the chosen options and apply the same
choices to the bar and hero. A design draft is never linked from the live site and is deleted or kept unpublished.

## 5. Check and hand over

- Open it at desktop (1440x900) and mobile (375x812). Nothing cut off, one clear button above the fold, the countdown
  reads the right time zone.
- Every link, dates and offer match `campaign.md`. The page is unpublished; the preview link is the last line of the
  message.
- Record the template, the page handle and the preview link in `campaign.md`. Stop removes or unpublishes the page,
  and the before → after table notes it.
- Anything unrelated spotted on the way (a hero height problem, an old colour) is one line in the hand-over for later,
  never offered inside the campaign.
