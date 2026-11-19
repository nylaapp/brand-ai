---
name: campaign-page
description: Generates a campaign landing page template for a Shopify store, built to sell and built so any part swaps in one switch. The offer, end date and one button sit in the first screen on mobile; urgency is real; products are curated with the saving shown; the shipping cutoff and FAQ sit near the button; it has an email signup and a tagged link per channel; phases from coming soon to ended run on one URL. Each part (hero, trust row, countdown, products, FAQ, signup, closing call to action) is its own section with ready alternates, swapped in the theme editor or by asking Claude. Uses only the theme's sections and the plan's facts, and can make a design draft with 2 or 3 copy options per section. Built on the store's staging theme, never the live theme. Requires BRAND.md, BRAND-VOICE.md and design.md. Use for "campaign landing page", "sale page", "BFCM page", "gift guide page", "swap the hero", "design draft" or "a page for the Black Friday sale".
---

# Campaign page

Make a landing page for a campaign out of parts the owner can swap in a click. The person using this is usually a solo
founder with ten minutes who edits in the Shopify theme editor, or asks Claude. Either way, changing the hero must
mean changing one section, never rebuilding the page.

## Ground rules (every run)

These come before every step below. The full text is `references/ground-rules.md`; where it and a step below disagree, the
stricter rule wins.

- **Brand files first (required: BRAND.md, BRAND-VOICE.md and design.md).** Read them before any work and follow them: words follow
  BRAND-VOICE.md and stay inside BRAND.md's claim limits; visuals use design.md's values. If one is missing or
  belongs to another store, stop and ask once: create it now (brand-capture, voice-builder or styles-builder,
  `references/ground-rules.md` section 1) or tell me where it is. Never work from memory or the live site instead, and
  never carry on without it. With no person present, stop and report what is missing.
- **Staging only.** Every change goes to the store's staging theme (an unpublished theme whose name contains
  "staging"), and to the `staging` branch when the theme is in a git repository. If none is remembered, settle
  it before the first change, offering to create "<live theme name> staging" (`references/theme-target.md` sections 3
  and 4). Never edit, push to or commit for the live theme. The page itself is created unpublished.
- **Live only when the person asks.** Never suggest, offer or schedule publishing. Only when the person asks in
  their own words in this chat, run the go-live gate (`references/ground-rules.md` section 3; `references/theme-target.md` section 7):
  checks first, then two confirmations, the second typed. End every change with the preview link and "Your live
  store has not changed."

## Where it fits

- **`campaign-launcher`** plans the campaign (name, offer, exact dates, link) and calls this skill when a landing
  page is wanted or the button needs a destination. This skill reads the same `campaign.md`, so the page, the bar and
  the hero never disagree. With no `campaign.md`, ask for the four facts in one message.
- **`page-studio:page-create`** is the builder. When it is available, hand it the region plan below and the swap rules,
  and let it do the working copy, verification and shipping to the staging theme. This skill does not rebuild that machinery;
  it adds the campaign preset on top: the region order, the alternates, the swap map and the design draft.
- **`copywriter`** (brand-voice plugin) writes the words (`references/copywriting.md` there). If BRAND-VOICE.md is
  missing, stop and ask (Ground rules above). If it is thin, say so before writing copy and offer `voice-builder`
  (same plugin) first.

## Rules

1. **Only the theme's own sections.** List `sections/*.liquid` and read each candidate's `{% schema %}` (setting ids,
   blocks, presets) before choosing. Never assume Horizon's sections: Honey 11 (Archer Commerce) has five fixed colour
   groups chosen by each section's `background` setting, and its own list (hero-image, hero-video, countdown,
   featured-collection, featured-product, collection-list, multicolumn, media with text, collage, collapsible content,
   rich text, email signup and more). Other themes pick a colour scheme.
2. **One section per region.** Hero, trust row, countdown, products, gifting, reviews, FAQ, signup and closing call
   to action are separate sections. Blocks are only for repeated items inside a region (cards, questions).
3. **Reuse before building.** Existing section, then the same section with one new setting, then a new section only
   when nothing produces the layout. No hardcoded colours, fonts or copy that a setting could hold.
4. **Unpublished, always.** The page is created unpublished, and its template goes on the staging theme (on a store
   whose live theme is connected to GitHub, the theme connected to `staging`:
   `../campaign-launcher/references/github-stores.md`). Never edit the live theme, and never link the page from the
   live site.
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

## What makes it sell

Read `references/effective-page.md` before planning the regions. It holds nine rules, and these are the ones a
page most often misses:
- **The first screen does the job.** At 375 px it shows the offer in concrete terms, the end date, the code or
  "applied at checkout", and one button.
- **The page matches the ad or email** that sent the visitor.
- **Urgency is real.** A countdown only to a real end, which never resets. Phases (coming soon, early access, live,
  last chance, ended) all run on one URL.
- **The products are curated.** Lead with best sellers and the deepest discounts, never the whole catalog. A big
  catalog starts with category tiles that each carry their own offer. Each card shows the saving (and a value line
  on sets), and quick add is on where the theme has it.
- **Coming soon still sells:** an early offer, best sellers, and notify-me or a signup.
- **Trust sits near the button:** the shipping cutoff, returns and real reviews only. The FAQ covers stacking and
  exclusions.
- **A low-pressure email signup** catches visitors who aren't ready to buy.
- **The page is mobile first and lean.** No new apps.
- **One tagged URL per channel**, and the owner's pre-launch checks go in the hand-over.

Each rule names its owner: the page, store data (ask first) or the owner. Never fake a rule to meet it. No reviews
in the store means no reviews region. An unknown cutoff stays `[confirm: …]`.

## The template

Default order, dropping any region the campaign doesn't need:

| # | Region | Typical section | Notes |
|---|---|---|---|
| 1 | Hero or banner | hero-image / hero-video | Offer in concrete terms as the headline, end date and code (or "applied at checkout") in the supporting line, one button to the products region; same facts as the homepage hero and the ad |
| 2 | Trust row | multicolumn or an icon row | Shipping cutoff, returns, delivery estimate; confirmed facts only |
| 3 | Countdown (optional) | countdown | Only for a real deadline; ends at the plan's end time; never resets |
| 4 | Featured products | featured-collection / featured-product | Best sellers and deepest discounts first, from an existing collection; compare-at prices and the theme's sale badge show the saving; quick add on if the section has it |
| 5 | Gifting, bundle or gift with purchase (optional) | collection-list / multicolumn / featured-product | Only existing collections or products; "Under $50", gift sets |
| 6 | Reviews (optional) | the theme's or reviews app's own section | Real reviews only; leave out if the store has none |
| 7 | Terms and FAQ | collapsible content | Stacking, exclusions and final sale, end time and zone, shipping cutoff, how the code or gift applies |
| 8 | Email signup | newsletter / email-signup | Low-pressure, in the brand's voice ("Get first access to the next sale") |
| 9 | Closing call to action | rich text with a button, or a banner | The offer and end date again, same link as the hero button |

The offer and dates sit in the hero and the FAQ, so a separate offer region is optional. Keep one only when the
offer needs more than a line, for example tiers or several exclusions. Give the products region an anchor the hero
button can link to, where the theme supports it.

**Phases.** If the plan has phases, the hero and countdown each get one hidden alternate per phase (`hero_soon`,
`hero_live`, `hero_last`, `hero_ended`). Every alternate carries its phase's copy, and the swap map lists when each
one switches on. The Ended alternate is never optional.

**Recurring campaigns.** Use a page handle with no year (`black-friday`). If last year's page exists, point it at
the new template rather than making a second page (`references/effective-page.md` → Recurring campaigns).

Theme templates are JSON with a comment header the editor rewrites; keep that header on existing files and write
new ones as plain JSON. Name the file `templates/page.campaign-<slug>.json` (the campaign slug) and create the Shopify page that uses it
unpublished. Each campaign gets its own template, so the next campaign starts from this structure, not from a blank
page and not by editing the last campaign's.

## Making each part swappable

Do all three, so it works in the editor and through Claude. `scripts/build_template.py` does the mechanical part:
describe the regions and their options in a small spec, run it with `--theme <staging theme folder> --slug <slug> --spec
spec.json`, and it checks every section type and setting id against the theme's own schemas (and number ranges),
writes `templates/page.campaign-<slug>.json` with the first option of each region on and the rest off, and prints
the swap map. `--list` shows the sections the theme has, `--dry-run` only checks. Swapping later is
`--swap hero_b` (turns that one on, its region's others off). Without Python, write the JSON by hand to the same shape. Each section starts from its first preset in the theme, so a hero keeps its heading and button blocks; the script
lists any text still left as the theme's placeholder, and you replace it with the plan's copy (blocks hold the copy on
Horizon-style themes, not section settings). Block types and block settings are checked too.

1. **Ready alternates, switched off.** For regions with a real choice (hero first, then offer layout and closing call
   to action), put a second and, if the theme has it, a third section of a different type in the template with
   `"disabled": true`, directly under the active one. Give every section a readable id: `hero_a`, `hero_b`,
   `offer_a`, `products_a`. In the editor the owner switches a part by hiding one section and showing the other (the
   eye icon), or removes one and adds another with "Add section". Only one alternate per region is ever on. Tested on Honey 11: hidden sections are not rendered, and the live store
   already keeps a hidden hero beside the active one, so this matches how the owner edits.
2. **Same content in every alternate.** Fill each alternate with the same heading, supporting line, button label and
   link (from the plan), so a swap never loses the words. Where the alternate has an image or video the owner has not
   supplied, leave it blank and say so.
3. **A swap map.** Put a short "Page parts" block in the plan artifact (the one document for the campaign, see
   `campaign-launcher`), or in the hand-over where there is none:

   | Part | On now | Alternates (off) | To swap |
   |---|---|---|---|
   | Hero | `hero_a` (image) | `hero_b` (video) | Editor: eye icon on both. Or say "swap the hero for the video one" |

   Keep it one table, with the template name, page handle and preview link under it.

**Swap by asking Claude:** "swap the hero for the video one", "move the countdown above the products", "use the
plain offer layout", "try the other closing banner", "add a reviews section", "drop the gifting row". Read the template, toggle `disabled` and `order` (and carry the content across if the alternate
is new), update the swap map, show the preview link. Never touch other sections, and never go live.

Show before the owner picks: owners choose widgets they have never seen ("I thought it'd be a little '10 days
until'"). For each unfamiliar region, show a screenshot or a link to an existing example (a store page, the theme
demo, or a brand from `references/examples.md`), one line each: what it is, what it looks like. Those brand notes
are dated, so open the page live before showing it. Where nothing can be shown, say so.

## Design draft (options before the homepage changes)

When the owner wants to choose: build one unpublished page with 2 or 3 copy options **per region**, labelled
"Option A / B / C" in plain text sections placed side by side, the recommended one first with one line on why it fits
the voice. Copy comes from `copywriter`'s three directions (the brand's wink, product-led, plain offer). When they
pick, rebuild the page with only the chosen options and apply the same choices to the bar and the homepage hero. A
design draft is never linked from the live site and is deleted or kept unpublished.

## Check and hand over

- Push to the staging theme and read the push result: "pushed with errors" means a setting was rejected, so find
  the file it names and fix it. Theme names are at most 50 characters.
- If the Shopify page can't be created (connector not signed in), preview the template on any existing page with
  `?view=<slug>&preview_theme_id=<id>`, and say the real page is still to create.
- **First time only, a swap check in the editor.** The swap is tested on the generated file (theme check is clean) but
  needs a real push to prove. After the push, open the page in the theme editor, hide the active hero and show its
  alternate, and confirm the preview changes. Say in the hand-over whether you did it or it is left to the owner
  (never pretend it was done).
- Open the page at desktop (1440x900) and mobile (375x812), and check:
  - **Mobile first screen:** at 375x812, without scrolling, the offer, the end date, the code (or "applied at
    checkout") and one button all show.
  - Nothing is cut off.
  - The countdown reads the right time zone.
  - Exactly one alternate per region is visible.
  - Buttons and FAQ rows are at least 44 px tall.
- **Score it** against `references/effective-page.md`. Give one line per rule: met, not met (why), or not
  applicable. Fix what the page can fix. List store-data gaps as offers, for example "no compare-at prices, so cards
  show no saving". List owner gaps in the to-do.
- Every link, date and offer matches `campaign.md`, and the hero states the same offer as `ads.md` and `email.md`
  where they exist.
- Record these in the plan artifact (`campaign.md` when there is a project folder):
  - the template, page handle, swap map and preview link;
  - the tagged link per channel;
  - the phase schedule;
  - the owner's pre-launch checks: a test order, stacking, stock, tracking events.
- **At Stop** (in `campaign-launcher`, only when the owner asks, through the go-live gate), a one-off page is
  unpublished. A recurring page switches to its Ended alternate and stays published.
- Anything unrelated spotted on the way (a hero height problem, an old colour) is one line in the hand-over for later,
  never offered inside the campaign.
- The message ends with the preview link and "Your live store has not changed.", on the last two lines.

