# Change check: before and after a site change

Run this for any change to site code, templates, theme settings, menus, page handles, content that contains CTAs or links, apps, domains, or the consent banner. It is quick when nothing is at risk, and it is how a renamed button gets caught before it zeroes a conversion.

## Before the change

1. **What is changing:** the diff (`git diff`, a list of files), or the description (a new theme, a content edit, an app install, a domain change).
2. **Look it up in the register** (ANALYTICS.md section 4) and the change-impact matrix (section 6): for each touched component, list matching `D` rows and `G` rules. Search by file, component, CTA text, link host, page handle and event name.
3. **Name the events at risk** and their tiers. Tier 1 at risk with a rule that would be broken is stop-ship: the change needs the analytics owner's written OK, or a different approach.
4. **Plan the after-check:** which static checks (section 8) and which live checks (states and events) will prove nothing broke.

If nothing in the register matches, say so explicitly ("Analytics impact: none, checked D-1..D-14 and G-1..G-12 on 2026-10-15"), never "no impact" without having looked.

## After the change

1. **Static checks** for the touched rows: run the section 8 commands and compare with the expected results.
2. **Live checks** on the preview or live URL for the events at risk: `page_inventory.js` on the page, then trigger the event in the accept state and decode the capture (`../analytics-audit/scripts/decode_hits.py`). Tier 1 at risk: also the reject state.
3. **Update** register rows (`Reality`, `Status`, date) and add rows for any new dependency the change created (a new CTA, a new custom event).
4. **Log** one line in the project's QA log: `Analytics impact: none | checked: <rows, how> | NOT verified: <reason>`. Never write "checked" for a check that was not run.

## Content and other skills

Skills that write content (blog posts, product pages, location pages, treatment pages) can change dependencies too: a booking link written into body copy, a page handle, a CTA label. They should apply the same rules: plain links to the agreed hosts without tracking wrappers, CTA wording from the matched list, stable handles. When such a skill creates or renames pages or links that a tag depends on, run this check.

## Theme upgrades and theme switches

Treat as a full change: diff the tracking code and app embeds between the old and new theme, re-run every static check, and run the privacy matrix for Tier 1 and Tier 2 events on the new theme's preview before publishing (pixels apply to previews too; theme code and embeds are the new theme's).
