# What makes a new page good: research, options, conversion, UX and design

`SKILL.md` steps 2b, 3, 4 and 7 point here. The playbook (`../../page-audit/references/page-type-playbook.md`) says what
a page type must contain. This file says how to find the best version of it, how it must work and look, and how to
prove it before the hand-over. It applies to every new page and every new section, landing pages above all.

Never invent a look or a fact. Every choice comes from the brand files, the research below, the theme's own sections
and settings, or the person, and the plan says which.

## 1. The brief (step 2b)

Settle five things before any research. Each one is taken from the brand files or the request when they answer it.
Only ask what is still missing, one question at a time, as multiple choice.

| Item | What it is | Usually found in |
|---|---|---|
| Goal | The one action the page exists for (buy, book, sign up, claim the offer) | The request |
| Traffic source | Where visitors arrive from (an ad, an email, social, search, the homepage), and the promise that brought them | The request, the campaign plan |
| Offer | What they get, the price, dates and exclusions, if any | The request, BRAND.md Catalog |
| Reader and doubts | Who they are and what they need explained or proved before acting | BRAND-VOICE.md Who we're talking to, BRAND.md Audience |
| Proof | Real reviews, ratings, press, guarantees and policies the page can show | BRAND.md Proof points, the store |

A page with no single goal is not a landing page. Say so and ask which goal wins.

## 2. Research (step 3)

Read each page live at 375 and 1440 px, scrolling so lazy content loads, and record the URL and the date. Use
`site-reader` first: it sets both viewports exactly and saves first-screen and full-page pictures. Use the browser only
for what site-reader can't do, and check the window really changed size before trusting a mobile read (a browser
window can refuse to resize). Never describe a page from memory or from a search snippet. A page that can't be read
is replaced by another, and the replacement is noted.

### 2.1 The sources (five to eight pages in all)

1. **Inspiration brands:** BRAND.md Inspiration brands, plus the Tone references in BRAND-VOICE.md. At least two,
   because these show where the owner wants the brand to go.
2. **Competitors:** `COMPETITORS.md` or BRAND.md Competitors. At least one, to see what shoppers in this category
   already know and what the brand must beat.
3. **Trend leaders:** two or three notable brands in the same or a neighbouring industry, praised now for their
   design or growing quickly. Neighbouring means a similar customer or price point, or the same kind of purchase.
   For a fashion-minded accessory, for example, that could be beauty, fragrance, small leather goods or design-led
   drinks. Find them by search ("best designed <industry> DTC sites <year>", recent redesign write-ups, Shopify's own
   store showcases). Prefer pages redesigned within the last 18 months, and say in the notes how each one was chosen.
4. **A page doing the same job:** their landing page for a landing page, their gift guide for a gift guide. A
   homepage is a second choice.

### 2.2 What to record for each page

| Lens | Record |
|---|---|
| Content | What the first screen says and in what order; how the offer, proof and objections are staged; naming, pricing and button labels; copy length |
| Layout | Section order and count; hero type; background rhythm; grid columns; density; what the first screen at 375 px holds; where the button repeats |
| Design | Fonts, palette, spacing, corners, button style, imagery and motion. Read these only to understand why the page feels as it does, never to copy |
| Works | Patterns that make the page clear and easy to act on: the offer read in one glance, proof at the button, a mobile first screen with the action, fast media |
| Doesn't work | Patterns that cost clarity or speed: a slow or heavy hero, a popup in the first screen, a theme so stylised the product or price is hard to find, a wall of text, competing buttons, an unreadable headline over a photo |

### 2.3 Trends: keep what is durable, leave what is a fad

After the pages are read, list the patterns that repeat across three or more of them. Mark each one:
- **Durable:** it helps clarity, trust or speed, and it fits the brand. Examples: product shown in use; plain price
  and terms; short FAQs on the page; reviews with photos; a sticky add-to-cart on mobile; bold type heroes when there
  is no strong image.
- **Fad:** it is mostly decoration, slows the page or clashes with the brand. Examples: heavy scroll animation, a
  cursor effect, autoplaying video with sound, novelty type that hurts reading.

Borrow durable patterns only. A fad that the owner asks for by name is used once, measured for speed, and noted.
A more stylised page can convert worse than a plainer one, so a pattern that adds style must not hide the offer,
the price or the button.

### 2.4 Record it

Put a **Reference study** table in the plan: brand, URL, date, source type (inspiration, competitor, trend leader),
what we borrow, what we leave and why. Under it, one line each:
- **Design basis:** the patterns borrowed, built in <store>'s design system.
- **Durable trends used:** the patterns, or "none".

If fewer than five pages could be read, say how many and flag it. With nothing readable, say the design basis is the
brand files and the playbook only. Never present an improvised style as researched.

## 3. Options and the pick (step 4)

Build **two or three page options**, each a section order adjusted to the design basis (not three wordings of one
layout). Score each 1 to 5 on these, with one line of reasoning:

| Criterion | The question |
|---|---|
| Conversion | Is the goal reachable from the first screen, are the reader's doubts answered before the button, and is the proof next to it? |
| Brand fit | Does it sound and look like BRAND-VOICE.md and design.md, at the distance set in Tone references? |
| UX | Is it easy on a phone? Can it be skimmed? Is it free of blocking overlays? |
| Speed | How light are the media and the scripts? |
| Build cost | Existing sections, one new setting, or a new section? |

Recommend the highest total; on a tie, conversion wins. Show the options in the plan, as a table or a quick mockup,
with the recommendation first. The person picks; their pick wins.

## 4. Where each section comes from (step 4)

For every region, take the first that works, and say which in the plan:
1. An existing section of the theme as it is (list `sections/*.liquid` and read each candidate's schema first);
2. The same section with one small new setting;
3. A native base-theme section or block;
4. **A new section, recommended,** when the research shows a pattern that works and no existing section can produce
   it without breaking the layout. Examples: a comparison table, a "why this price" band, a sticky mobile buy bar,
   a reviews strip with photos, an in-use gallery. The plan names the pattern, the reference page that shows it,
   what the page gains, and the build cost. It is built to the rules in `SKILL.md` → "If a new section type is
   needed", only after the plan's yes.

Never force a region into a section that changes its layout, and never build a new section for something an existing
one already does.

**Check the schema can show the region.** Before a section is put in the plan, read its schema for what the region
needs: a section heading, a button, a colour band behind the whole section. Many card and column sections have no
section heading setting, so a region planned as "Why it's worth $25" shows only its cards. When the section lacks
something, say so in the plan and either choose another section, carry the point in the blocks themselves (the first
card's title), or add a heading band only when the page still stays within the density rule.

**A reused section is checked against this brief.** A section copied from another template (a hero, a closing band)
was written for that page's brief. Check it still answers this page's main doubt and promise; if not, change its
words or say in the plan why it stays.

## 5. Conversion rules

Each rule names the playbook check it serves. Every one is scored in section 8.

1. **The first screen does the job (LP3).** At 375 px with no scroll: the headline, the benefit or offer, the price or
   terms when there is an offer, one button, and real media or a designed type hero. The reader's main doubt is
   answered here too, in a line or a badge.
2. **The headline keeps the promise (LP1).** It matches the ad, email or link text that brought the visitor.
3. **One goal, one button (LP2).** One primary action, repeated down a long page rather than competing with others.
   Navigation that leads away is trimmed where the theme allows. A second action is plain text.
4. **Doubts in the order people have them.** Does it work? Is it worth the price? Can I trust it? When will it come?
   Can I return it? Take the reader's doubts from the brief and answer each one in a region before the closing
   button.
5. **Proof next to the action (LP4).** Real reviews with names, ratings, customer photos, press or guarantees, beside
   or just above a button, never only at the bottom. Never invent proof.
6. **Terms visible and true (LP5).** Price, dates, exclusions and policies stated plainly and the same everywhere.
   Urgency only when it is real (an end date, real stock). Plan what the page says once the offer ends.
7. **Short FAQs on the page.** Three to six real questions in a collapsible block near the end. They answer last
   doubts and help search and AI answers. Longer explanations go to a blog post or an FAQ page linked from it.
8. **Copy from the voice.** Page copy is written with `copywriter` (brand-voice plugin) when it is installed, at the
   reader and distance set in BRAND-VOICE.md, with two or three headline options. Otherwise follow BRAND-VOICE.md
   directly and say so.

## 6. UX rules

1. **Mobile first.** Tap targets at least 44 px; the button in thumb reach. On a long page, use a sticky add-to-cart
   or button on mobile when the theme has one, or recommend one (section 4). No popup or banner covering the first
   screen (U5).
2. **Easy to skim.** One idea per section. Headings read as the whole pitch on their own, top to bottom. Supporting
   text one or two sentences; longer copy in a collapsible block.
3. **Fast (LP7, U6).** Hero media under about 500 KB and at least 1,600 px wide; no layout shift as it loads;
   no script added for decoration. Recommend a `theme-audit` speed check after the build.
4. **Accessible.** One H1, headings in order, alt text on every image, 4.5:1 text contrast, and visible focus states.

## 7. Visual rules

1. **Never a placeholder in the hero.** Use the owner's image or video, an image the store already has, or a type-only
   hero on a brand colour.
2. **Image-led.** The brand's own photography carries the page. Products are shown in use where the store has those
   images. Every card uses the same aspect ratio and crop.
3. **Background rhythm.** At most three of the brand's colour groups. Neighbouring sections only share one when they
   are one idea. Open and close on the strongest one. Check the real hex of each group, not its name. Judge it on the
   render, not the settings: on some sections the colour group paints only a card or the text box (media with text,
   feature cards), so the band around it stays the page colour.
4. **One spacing scale.** Three padding steps from the theme's range, reused: small, medium, large.
5. **Type hierarchy.** One H1 of at most eight words and two lines at 375 px; region headings one size down,
   consistent across the page.
6. **Density.** Six to nine visible sections; no more than one text-only band in a row; no empty region.
7. **One alignment and one button style** across the page.
8. **Design system only.** Every colour, font, size, spacing, radius and shadow comes from `design.md` and the theme
   settings. Where a reference differs, the brand wins.

## 8. Look, score, fix once (step 7)

After the build, capture the full page at 375 and 1440 px, 3 seconds after load, scrolling to each section. Score one
line per row: met, not met (why), or can't tell.

| # | Check |
|---|---|
| 1 | First screen at 375 px: headline, offer or benefit, the main doubt answered, one button, real media |
| 2 | One goal; the button repeats and nothing competes with it |
| 3 | Every doubt from the brief is answered before the closing button |
| 4 | Proof sits next to a button |
| 5 | Terms, price and dates match everywhere; urgency is real |
| 6 | FAQs present (three to six) |
| 7 | Mobile: tap targets, sticky button where planned, no overlay |
| 8 | Background rhythm, spacing scale and type hierarchy hold |
| 9 | No placeholders, uniform cards, no empty region |
| 10 | Hero media weight and layout shift are in range |

Fix every "not met" the page can fix, capture once more, and list what needs the person (an image, a review, a policy
line) in the hand-back with the region it affects. Never claim a check that wasn't run.

## 9. Measurement (hand-back)

The page is finished when it can be measured. In the hand-back, list:
- one tagged link per traffic source (`utm_source`, `utm_medium`, `utm_campaign`), built from the brief;
- the conversion event to watch (add to cart, checkout, signup) and where to see it (Shopify Analytics, or the
  store's analytics tool);
- what to compare after two to four weeks (conversion rate by source, the button's click rate), and which option from
  section 3 to test next if the numbers are weak.

Setting up tracking is the owner's job, or the `analytics` skills' job when they are installed. This skill only lists
what to set up.
