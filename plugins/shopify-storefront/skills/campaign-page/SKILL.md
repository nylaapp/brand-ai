---
name: campaign-page
description: Builds a campaign landing page template for a Shopify store where every part (hero or banner, offer and dates, countdown, products, terms and FAQ, closing call to action) is its own section that is easy to swap, either in the Shopify theme editor (switch a part on or off, reorder, or change one setting) or by asking Claude ("swap the hero for the video one"). Uses only the theme's existing sections, keeps the same offer, dates and link as the campaign plan, ships each swappable part with ready alternates, and can produce a design draft page that shows 2 or 3 copy options per section side by side before the homepage changes. Always an unpublished copy, never the live theme. Use whenever someone says "campaign landing page", "sale page", "landing page template for the campaign", "make the sections swappable", "swap the hero", "change the banner on the campaign page", "design draft", "show me options for the page", or "a page for the Black Friday sale", even without saying "template".
---

# Campaign page

Make a landing page for a campaign out of parts the owner can swap in a click. The person using this is usually a solo
founder with ten minutes who edits in the Shopify theme editor, or asks Claude. Either way, changing the hero must
mean changing one section, never rebuilding the page.

## Where it fits

- **`campaign-launcher`** plans the campaign (name, offer, exact dates, link) and calls this skill when a landing
  page is wanted or the button needs a destination. This skill reads the same `campaign.md`, so the page, the bar and
  the hero never disagree. With no `campaign.md`, ask for the four facts in one message.
- **`page-studio:page-create`** is the builder. When it is available, hand it the region plan below and the swap rules,
  and let it do the working copy, verification and shipping to a draft. This skill does not rebuild that machinery;
  it adds the campaign preset on top: the region order, the alternates, the swap map and the design draft.
- **`brand-voice`** writes the words (`references/copywriting.md` there). If BRAND-VOICE.md is thin or missing, say so
  before writing copy.

## Rules

1. **Only the theme's own sections.** List `sections/*.liquid` and read each candidate's `{% schema %}` (setting ids,
   blocks, presets) before choosing. Never assume Horizon's sections: Honey 11 (Archer Commerce) has five fixed colour
   groups chosen by each section's `background` setting, and its own list (hero-image, hero-video, countdown,
   featured-collection, featured-product, collection-list, multicolumn, media with text, collage, collapsible content,
   rich text, email signup and more). Other themes pick a colour scheme.
2. **One section per region.** Hero, offer, countdown, products, terms and FAQ, closing call to action are separate
   sections. Blocks are only for repeated items inside a region (cards, questions).
3. **Reuse before building.** Existing section, then the same section with one new setting, then a new section only
   when nothing produces the layout. No hardcoded colours, fonts or copy that a setting could hold.
4. **Unpublished, always.** The page is created unpublished on a preview copy of the theme. Never edit the live theme,
   and never link the page from the live site.
5. **Same facts everywhere.** Offer, exclusions, exact dates in shopper form ("Nov 27 to Dec 1") and link come from the
   plan and appear identically in every region.
6. **Leave image pickers blank** when image rights aren't confirmed, then check the text still reads: a hero with
   no image or video falls back to the theme's pale default, so set the text colour from the section's colour group
   (or a dark value) and confirm 4.5:1 contrast in the screenshot. Hero text left white on that default was
   unreadable in testing.
7. **Respect each setting's range.** Read `min`, `max` and `step` in the schema before writing a number (a scrim of
   40 on a step of 15 is rejected and fails the whole template). Empty every placeholder text setting the section
   would otherwise show (a collapsible section's default "Use this text to share more information about your
   store." appears unless its description is set).

## The template

Default order, dropping any region the campaign doesn't need:

| # | Region | Typical section | Notes |
|---|---|---|---|
| 1 | Hero or banner | hero-image / hero-video | Name, one supporting line, one button; same text as the homepage hero |
| 2 | Offer and dates | rich text or multicolumn | Offer, exclusions, exact dates |
| 3 | Countdown (optional) | countdown | Only for a real deadline; ends at the plan's end time |
| 4 | Featured products or collection | featured-collection / featured-product | An existing collection or product; check it exists |
| 5 | Terms and FAQ | collapsible content | Exclusions, shipping, gift-card rule, how a code works |
| 6 | Closing call to action | rich text with a button, or a banner | Same link as the website button |

Theme templates are JSON with a comment header the editor rewrites; keep that header on existing files and write
new ones as plain JSON. Name the file `templates/page.campaign-<slug>.json` (the campaign slug) and create the Shopify page that uses it
unpublished. Each campaign gets its own template, so the next campaign starts from this structure, not from a blank
page and not by editing the last campaign's.

## Making each part swappable

Do all three, so it works in the editor and through Claude:

1. **Ready alternates, switched off.** For regions with a real choice (hero first, then offer layout and closing call
   to action), put a second and, if the theme has it, a third section of a different type in the template with
   `"disabled": true`, directly under the active one. Give every section a readable id: `hero_a`, `hero_b`,
   `offer_a`, `products_a`. In the editor the owner switches a part by hiding one section and showing the other (the
   eye icon), or removes one and adds another with "Add section". Only one alternate per region is ever on. Tested on Honey 11: hidden sections are not rendered, and the live store
   already keeps a hidden hero beside the active one, so this matches how the owner edits.
2. **Same content in every alternate.** Fill each alternate with the same heading, supporting line, button label and
   link (from the plan), so a swap never loses the words. Where the alternate has an image or video the owner has not
   supplied, leave it blank and say so.
3. **A swap map.** Write a short "Page parts" block in `campaign.md` (or in the hand-over if there is no file):

   | Part | On now | Alternates (off) | To swap |
   |---|---|---|---|
   | Hero | `hero_a` (image) | `hero_b` (video) | Editor: eye icon on both. Or say "swap the hero for the video one" |

   Keep it one table, with the template name, page handle and preview link under it.

**Swap by asking Claude:** "swap the hero for the video one", "move the countdown above the products", "use the
plain offer layout". Read the template, toggle `disabled` and `order` (and carry the content across if the alternate
is new), update the swap map, show the preview link. Never touch other sections, and never go live.

Show before the owner picks: owners choose widgets they have never seen ("I thought it'd be a little '10 days
until'"). For each unfamiliar region, show a screenshot or a link to an existing example (a store page, the theme
demo), one line each: what it is, what it looks like. Where nothing can be shown, say so.

## Design draft (options before the homepage changes)

When the owner wants to choose: build one unpublished page with 2 or 3 copy options **per region**, labelled
"Option A / B / C" in plain text sections placed side by side, the recommended one first with one line on why it fits
the voice. Copy comes from `brand-voice`'s three directions (the brand's wink, product-led, plain offer). When they
pick, rebuild the page with only the chosen options and apply the same choices to the bar and the homepage hero. A
design draft is never linked from the live site and is deleted or kept unpublished.

## Check and hand over

- Push to the preview copy and read the push result: "pushed with errors" means a setting was rejected, so find
  the file it names and fix it. Theme names are at most 50 characters.
- If the Shopify page can't be created (connector not signed in), preview the template on any existing page with
  `?view=<slug>&preview_theme_id=<id>`, and say the real page is still to create.
- Open the page at desktop (1440x900) and mobile (375x812). Nothing cut off, one clear button above the fold, the
  countdown reads the right time zone, and exactly one alternate per region is visible.
- Every link, date and offer matches `campaign.md`.
- Record the template, page handle, swap map and preview link in `campaign.md`. Stop (in `campaign-launcher`) removes
  or unpublishes the page.
- Anything unrelated spotted on the way (a hero height problem, an old colour) is one line in the hand-over for later,
  never offered inside the campaign.
- The preview link is the very last line of the message.

