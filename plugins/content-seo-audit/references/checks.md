# What to check on the live page, and how to judge it

Judge `extract_page.js` output against these. FAIL means fix soon, WARN means worth fixing, INFO is for the record. The numbers are defaults for a guide-style post; if the brand profile has an `audit:` block, use its ranges instead. Judge each post by its type: length and link counts matter for guides, not for short launch or news notes.

| Check | Pass | Otherwise |
|---|---|---|
| Leftover placeholders (`[[...]]`) | none | FAIL. Public readers can see them. Name where each one is. |
| Robots | no `noindex` | FAIL if noindex |
| Canonical | points to this same URL | WARN if it points elsewhere |
| Title tag | 50 to 60 characters, keyword near the front | WARN outside 45 to 65 |
| Meta description | 140 to 160 characters | WARN if missing or auto-cut from the intro |
| H1 | exactly 1 | FAIL if 0 or 2 or more (the theme shows the title as H1, so the body must not add one) |
| Headings | H2s exist, no H3 before an H2 | WARN |
| Schema | one BlogPosting or Article; FAQPage if the post has an FAQ | WARN if missing; WARN if duplicated |
| Schema matches the visible FAQ | same questions and answers | WARN |
| Images | every image has alt text | WARN per missing alt |
| Image source | hosted on the store CDN | INFO if hotlinked from another site (works, but can break) |
| Featured image / og:image | present | WARN if missing (social shares look bare) |
| Links | 2 to 4 product/collection links, 2 to 3 related posts, no dead links | WARN |
| First paragraph | 40 to 60 words that answer the main question | INFO |
| Word count | 1,200 to 2,500 for a guide (profile can change this) | INFO |

PageSpeed (mobile) guide, using Google's own bands: performance 90 to 100 good, 50 to 89 needs work, under 50 poor. LCP under 2.5 s good; INP under 200 ms good; CLS under 0.1 good. When the result is poor, point to the top one or two causes Google lists (often large images or third-party scripts) and say plainly that some causes come from the theme or apps, not the post.
