# Building the dependency register and rules

Tracking breaks silently when the site changes something a tag was quietly relying on: a button's words, a link's host, a page path, how a form reports success, a dataLayer event a previous developer added. The register (ANALYTICS.md section 4) lists every such dependency so a change can be checked before it ships. The rules (section 6) turn the risky ones into "do not change without an analytics check".

## 1. Sources

| Source | Gives you | How |
|---|---|---|
| Tag manager export | Every trigger condition and variable that reads the site | `python ../analytics-audit/scripts/gtm_export_summary.py export.json` > "Site dependencies" and "Variables that read the page" |
| Live public build (no export, or a stale one) | Each live tag by number with its firing and blocking conditions, IDs and paused state; no names | `python ../analytics-audit/scripts/gtm_public_rules.py GTM-XXXX`; mark rows built this way "public gtm.js vN" and confirm with an export later |
| Shopify custom pixels | Custom event names the theme must publish; fields they read | Read each custom pixel's code in Settings > Customer events (person's screenshot or paste) |
| Site code | `dataLayer.push`, `Shopify.analytics.publish`, `gtag(`/`fbq(` calls, data attributes tags read | Search the repo |
| Third-party domains | Events a vendor pushes (booking engine `purchase`, payment confirmation) and the keys tags read from them | Container triggers on those hosts; a test capture on the vendor's pages |
| Tracking plan | Which events matter (tiers) | ANALYTICS.md section 1 |

## 2. One row per dependency

| Field | Write |
|---|---|
| ID | `D-n`, permanent |
| Tag needs (exact) | The literal condition: `Click URL contains booking.example.com`; `Click Text matches /Book now|Book a visit/i`; `custom event = purchase with eventModel.send_to = G-XXXX`; `Page Path contains thank-you`; `Page Hostname does not start with example.com` |
| Site must provide | In site terms: "every booking CTA is a plain `<a href>` to booking.example.com"; "CTA visible text contains one of ..."; "the contact form redirects to a URL containing thank-you" |
| Reality | What the site does today, with evidence and date (file paths and counts, a page check) |
| Status | `ok`, `at risk`, `broken`, `retired` |
| Feeds | Which events and destinations (`E-2 GA4 schedule, Meta Schedule`) and their tier |

Group by kind: links and hosts, visible text, URLs and hostnames, forms, dataLayer events and keys, DOM selectors and attributes, cookies and globals, third-party contracts.

Things that look harmless and break tags:
- turning a link into a `<button>` or a JavaScript navigation (Just Links triggers only see `<a href>`; `preventDefault` or `stopPropagation` hides the click; a site script that intercepts link clicks and redirects in JavaScript does the same for every link it catches, FC-31),
- adding visually hidden text inside a CTA for accessibility (it changes Click Text; `aria-label` does not),
- translating or A/B testing CTA wording,
- moving a page, changing a handle or slug, adding a redirect or a tracking wrapper to a link,
- changing a form to show success in place instead of redirecting (or the reverse),
- changing domain, subdomain or the primary host (hostname rules, cookie domains, linker lists),
- publishing a different theme (theme code and app embeds change; pixels do not),
- a platform migration (old dataLayer events vanish, sometimes including the event the base page view waits for, FC-30).

## 3. Rules

Write a rule for every dependency that feeds a Tier 1 or Tier 2 event, plus the general ones below. A rule says what must not change and what to do if it must.

General rules every client gets (adapt the wording):
- **One path per destination.** Each destination receives each event from one install point.
- **No new tag without a load-policy row** (owner, question, timing, cost).
- **No second measurement stack in site code.** Tags go through the chosen paths; a `dataLayer.push` or `Shopify.analytics.publish` needs an agreed name and schema, recorded here.
- **Don't invent event names** that collide with existing ones.
- **Hostnames and domains are analytics changes.**
- **Theme switches are analytics changes:** diff tracking code between themes before publishing.
- **Accessibility edits keep tracking intact** (keep `<a>` for links, keep visible CTA text; use `aria-label` rather than hidden text inside a matched CTA).
- **Log it:** every change touching the register gets an analytics impact line in the project's QA log.

## 4. Change-impact matrix

A short table mapping common change types to the rows and rules at risk, so a developer can look up "I am renaming a CTA" and see what to check. Keep it in section 6 under the rules.

| Change | At risk | Rules |
|---|---|---|
| Reword a CTA | | |
| Change a link's destination or wrap it | | |
| Link to button, or a click handler on a card | | |
| Move, rename or unpublish a page | | |
| Change how a form reports success | | |
| Add a script, pixel or dataLayer push | | |
| Change domain or hostname | | |
| Publish a different theme or upgrade the base theme | | |

## 5. Static checks

For each register row that code can show, write a command with the expected result into section 8, so a later check is a comparison, not a re-investigation. Examples:

```bash
# booking links point at the current booking host (expected: 9)
grep -rhoE 'https://booking\.example\.com/[^"'\'' <)]*' templates sections snippets blocks | wc -l
# nothing points at the old host (expected: 0)
grep -rlE 'booking\.old-example\.com' templates sections snippets blocks layout | wc -l
# site code loads no tracking of its own (expected: no output)
grep -rIn -iE 'googletagmanager|gtag\(|fbq\(|ttq\.|clarity\.ms' layout sections snippets blocks assets/*.js
```

Content stored in the platform (page metafields, menus, blog posts) does not show up in a repo grep; list those rows with a live-page check instead.
