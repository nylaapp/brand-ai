# What makes a campaign page look designed

`effective-page.md` says what a page must contain to sell. This file says how it must look. A page can pass all nine
selling rules and still look like a stack of default sections. Both files apply to every page, and neither replaces
the other. Read this one before choosing sections, and again before the hand-over.

Never invent a look. Every choice below comes from the brand's own files, a reference page or the theme's own
settings, and the plan says which (the design basis, below).

## 1. Settle the design basis first: study real pages

**The rule.** When the owner gives no Figma file, mockup or reference link, never design from the skill's defaults
alone. Always study similar pages first: a competitor, an inspiration brand and a brand in a similar industry
running the same kind of campaign, plus a current trend leader. Read their content and their layout, then read the store's own design system and
branding, and only then choose sections. If the owner did give a reference, use it (it wins) and skip to step 4.

### 1. Choose four to six pages to study
Take them from these sources, in this order, and write down the URL and the date you looked:
1. **Competitors:** `COMPETITORS.md`, or BRAND.md → Competitors. At least one.
2. **Inspiration brands:** BRAND.md → Inspiration brands, the ones suggested for style. At least one.
3. **The same industry or product type:** brands that sell something similar to a similar audience, found by
   search, plus the matching pages in `examples.md` (dated, so open them live).
4. **Trend leaders:** one or two notable brands in the same or a neighbouring industry (similar customer, price point
   or kind of purchase), praised now for their design or growing fast, preferably redesigned in the last 18 months.
   Say how each was found. BRAND-VOICE.md's Tone references, when present, name brands the owner already admires:
   start there.

Pick the page that does the same job as the one being built: their gift guide for a gift guide, their sale page for
a sale, their launch page for a launch. A homepage is a second choice. A page that is not live now (last year's
campaign) is read from the brand's current equivalent and said so.

### 2. Read each page at 375 and 1440 px
Use `site-reader` (`../../site-reader/skills/site-reader/SKILL.md`: text, section order and heights, first screen,
fonts and colours as measured, no browser needed) or the browser at both widths, scrolling slowly so lazy content
loads. If a page can't be read (blocked, login wall), say so and pick another. Never describe a page from memory or
from a search snippet.

### 3. Study three lenses and write them down
| Lens | What to record |
|---|---|
| **Content** | What the hero says and in what order (offer, date, button); how the offer, proof and objections are ordered; how products are named and priced; the labels on buttons; how long the copy is; what trust and FAQ items appear |
| **Layout** | Section order and count; hero type (full-bleed image, split, type only, video); how the backgrounds alternate; product grid columns and card style; how dense it is; what the first screen at 375 px shows |
| **Design system and branding** | Their fonts, palette, spacing, corners, button style and imagery style, read only to understand why the page feels as it does. Then read the store's own `design.md` and theme settings, and note where they agree or differ |
| **Works / doesn't** | What makes the page clear and easy to act on (offer read in one glance, proof at the button, the action in the mobile first screen, light media), and what costs clarity or speed (a heavy hero, a first-screen popup, styling that hides the price or the button, competing buttons) |

**Durable trend or fad.** Across all the pages, list the patterns that repeat in three or more. Mark each one durable
(it helps clarity, trust or speed and fits the brand: product in use, plain terms, on-page FAQs, photo reviews, a
sticky mobile button) or a fad (mostly decoration, slows the page or clashes with the brand: heavy scroll animation,
cursor effects, autoplay with sound). Borrow durable ones only. A more stylised page can sell less than a plainer one,
so no pattern may hide the offer, the price or the button.

### 4. Decide, then record it
Add a **Reference study** table to the plan artifact (Website section), one row per page: brand, URL, date, source
type, what we borrow, what we leave and why. Under it, one line: "Design basis: <patterns borrowed> built in
<store>'s design system", and one line naming the durable trends used. Then map each borrowed pattern to a section
the theme actually has, or, when none can produce it, to a recommended new section (`SKILL.md` → Rules, rule 3).

- **Borrow structure and patterns, never the look.** Order of bands, what each holds, grid shape, how the offer and
  proof are staged. Never copy their words, images, logo or typefaces, and never hotlink their files.
- **The store's brand wins every conflict.** Colours, fonts, spacing, corners, buttons and imagery come from
  `design.md` and the theme settings (`styles-builder` sets them). Where a reference differs, use the store's value
  and say so in the table.
- **Show the owner what you borrowed.** Two or three patterns with a link each, for example "hero like X's, trust row
  like Y's", before building, so a wrong turn is caught early.
- **Nothing to study?** If no similar page can be read (offline, all blocked), say the design basis is the brand
  files only and flag it. Never present an improvised style as researched.

## 2. Pick a layout recipe by campaign type

A gift guide, a sale and a launch don't share one layout. Choose the recipe, then adjust it to the design basis.

| Campaign | Hero | Middle | Close |
|---|---|---|---|
| **Sale** (discount) | Offer and end date as the headline; product or lifestyle image; one button | Trust row, then deepest discounts and best sellers in one grid, then bundles | FAQ, the offer again as the closing band |
| **Gift guide** (no discount) | A gifting image or a bold type hero in a brand colour | Trust row with the shipping cutoff, then gift groups as image tiles ("For her", "Under $50"), then a short best-seller grid | Gift card band, FAQ |
| **Product launch** | The product at large size; name, one line, price, button | Three benefit blocks with images, a "how it's used" row, reviews or press if real | Product card repeated, FAQ |
| **Limited drop or event** | Date and countdown first; the product teaser | What is in it, how to get it, notify-me or signup | Signup band |
| **Values or awareness day** | Story headline and image; no price | Two or three story blocks, then the products that tie in | Soft call to action |

Each recipe still drops regions the campaign doesn't need (`SKILL.md` → The template).

## 3. Visual rules

These are checked at the hand-over. Each names the fix, so a failed check is never just a complaint.

1. **The hero never shows the theme's placeholder.** In order: the owner's image or video; an image the store
   already has (Content → Files, the featured product or collection images); or a type-only hero on a brand colour
   group, built from `rich-text` or a hero with no media and the text colour set for contrast. A grey placeholder
   or faint text on a pale default is a failure.
2. **Background rhythm.** Use at most three of the brand's colour groups. Never two neighbouring sections on the
   same group unless they are one idea (trust row under the hero). Open and close on the strongest group: the hero and
   the closing band.
3. **One spacing scale.** Pick three padding steps from the theme's range and reuse them: small for the trust row,
   medium between content sections, large around the hero and the closing band. No section with zero padding between
   two sections of the same background.
4. **Type hierarchy.** One H1 only, the hero headline: at most eight words, no more than two lines at 375 px. Every
   region heading is one size down and one size across the page. Supporting text is one or two sentences.
5. **Images behave.** Every product card has the same aspect ratio and crop. Hero media is at least 1,600 px wide.
   A tile or card whose collection or product has no image is left out, never shown as a grey box.
6. **Products fill the grid.** Two columns on a phone, three or four on desktop. Show a number that fills the last row
   (4, 6 or 8). Sold-out products are removed from the region or marked as sold out.
7. **Density.** Six to nine visible sections. No more than one text-only band in a row. Long copy goes in a
   collapsible block. A page with only text bands and one product row is not finished.
8. **One alignment and one button style.** A centred hero means centred region headings; a left-aligned hero, left.
   Every primary button looks the same, and a second action is plain text.
9. **No empty region.** A section with no image, no products or no content is removed from the template, not left on
   with a placeholder.
10. **Motion settles.** Sections that fade in must be readable once the animation ends. Take every screenshot after
    about 3 seconds (a video hero's text can take longer), or the page looks faint when it isn't.

### Found when this was first applied (Honey 11, Charlotte Welch gift guide)

- **Almost the whole page was one colour.** `main-background` and `background-modal` are both cream, so a page built
  from the default group of each section looks flat. Check the actual hex of each group, not its name, before
  counting a section as a different band.
- **On `rich-text`, the padding setting sits outside the coloured band,** so a hero with padding 88 showed cream gaps
  above and below a thin green band. For a coloured `rich-text` band set `padding_top` and `padding_bottom` to 0;
  the band brings its own inner space. `multicolumn` and `collapsible-content` use the same structure: check by
  looking, and adjust.
- **On `featured-collection`, `background` colours the product cards, not the section.** Use it for card colour
  only, and take page rhythm from other sections (hero, trust row, closing band).
- **`columns` must match the product count.** Two products in a two-column section became 650 px tiles at 1440.
  Use four products in four columns (two across on a phone), or three in three.
- **`countdown` has the same outer padding.** Set its `padding_top` and `padding_bottom` to 0 so the band meets its
  neighbours, as with `rich-text`.
- **Dark text straight on a photo is a gamble.** On a `hero-image`, setting the scrim to its lightest value changed
  nothing visible, and the line crossed a bright product. When the image is busy, build the hero as `media-with-text`
  (image above or beside, headline and button on a flat band): it was readable at 375 and 1440 px and keeps the
  offer and button in the first screen. Its button is the outlined style, so say so if the rest of the page uses
  solid buttons.
- **Theme defaults can state claims.** `featured-product` showed "Free 60 day returns" from its buy-buttons block
  although the store's policy is 7 days. Read every line the rendered section prints, not only the ones you set,
  and blank the setting (`show_inventory_notification` off, `notification_message` empty).
- **Large hero photos load slowly.** A 2,293 px image took about 15 seconds to appear in the preview. Use a file
  under about 500 KB, as the mobile rule already says.
- **A vertical (phone) video makes the desktop hero 2,500 px tall.** Measured at 1440 px: 2,558 px. Reusing the
  store's own hero video is the right first choice, so add the section `custom_css` from
  `../campaign-launcher/references/honey.md` → Hero to each video hero in the template. It works in a page template
  too: the hero came down to 675 px at 1440 and the mobile hero stayed full height.
- **Capture at a real phone height (375x812), scrolling, not in one tall frame.** In a tall frame, hero heights set
  in `vh` balloon (a 70vh hero became 1,680 px) and some sections stay blank even with fades forced on. Scroll to
  each section, wait, then capture. A hero video's text can take 8 to 14 seconds to appear in the preview, so wait
  for it before calling the hero unreadable. To catch fades in a long page, a one-off style forcing
  `.scroll-animate` to opacity 1 helps for a quick look; never leave it in the theme.

## 4. Look, score, fix once

After the push, open the page and capture it, full length, at 375, 768 and 1440 px wide, 3 seconds after load. Then
score it on one line per row:

| # | Check | Result |
|---|---|---|
| 1 | First screen at 375 px shows the offer or gift angle, one button, and real media or a designed type hero | met / not met (why) |
| 2 | Background groups alternate and the page opens and closes strong | |
| 3 | Spacing steps are consistent | |
| 4 | One H1, headings consistent, nothing cut off | |
| 5 | Images and cards are uniform, no placeholders | |
| 6 | Product grids fill their rows | |
| 7 | The page isn't a wall of text, and has six to nine sections | |
| 8 | Alignment and buttons are consistent | |

Fix every "not met" the page can fix, then capture once more. List what needs the owner (an image, a collection
image, a restock) in the to-do with the section it affects. Never claim a visual check that wasn't run: if no
browser tool is available, say the visual check was not run.

## 5. Show layout options, not only copy options

When the owner wants to choose, the design draft offers two or three layouts, not just wording (`SKILL.md` →
Design draft). Each option is one recipe row adjusted to the design basis. Show them as separate previews, or as a
quick mockup (a Design artifact where available), with one line on why each fits the brand. Pick the layout first and
the copy second, so the words fit the space.
