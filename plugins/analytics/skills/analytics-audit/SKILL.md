---
name: analytics-audit
description: "Audit a website's analytics and tagging, for any store or business. Tagging Audit: inventory of everything installed, where, what it sends, and what should change. Full Analytics Audit: also tests every core event end to end across privacy states (no choice, accept, reject, GPC, blocked) and regions. Finds double tracking, missing conversions, consent gaps, broken cross-domain, leftover and unowned tags and GA4 settings problems, with evidence. Works from the public site alone; goes deeper with site code, a GTM export, GA4 access or screenshots. Shopify-first (app and custom pixels, app embeds, Google & YouTube app, Customer Privacy API); also WordPress and custom sites. Writes a client-ready report and the shared ANALYTICS.md. Use for \"audit the analytics\", \"tagging audit\", \"check our tracking\", \"are we double counting\", \"why don't GA4 and Shopify match\", \"check consent mode\", or new-client analytics. Read-only."
---

# Analytics audit

## Effort (read before starting)

Tagging audit: about 15 to 30 minutes of agent time for one site with a booking or checkout domain at access levels 0 to 2; most of it goes to the page inventory and the write-up. This is one measurement (one client, 2026-10-15: about 20 minutes over 14 page loads on 4 hosts); re-measure on the next clients. Full audit: add about 1 to 2 hours for the privacy matrix and core-event tests, more if test orders or bookings must be arranged (not yet measured). Stop and report if a tagging audit passes 1 hour or a full audit passes 4.

Analytics is only useful if the numbers can be trusted, and most breakages are silent: a duplicated tag, a renamed button, a consent banner that never tells the store the visitor said yes. This skill finds out what is really installed and what really leaves the browser, so decisions about fixes rest on evidence. It changes nothing; fixes go through `analytics-setup` (getting it working) or `analytics-cleanup` (removing and slimming).

If the project has its own instructions file (AGENTS.md, CLAUDE.md) with analytics or safety rules, read it first; it outranks this skill.

## 0. Non-negotiables

- **Read-only.** Never edit tags, containers, pixels, theme code, consent settings or account settings. Never publish, pause or delete anything. Suggest; the person decides.
- **Evidence for every claim.** Each inventory row and finding cites what showed it (page source, a decoded request, an export line, a screenshot) and the date. Observed facts and inferences are labelled differently. "Not checked" is a valid answer; a guess is not.
- **Never sign in for anyone** or type credentials or 2FA codes. If a tool needs access, ask the person to sign in or to export what is needed.
- **No real orders, bookings or form submissions** without the owner's explicit OK for that specific test (see `references/privacy-matrix.md` section 4). Never type real customer data.
- **Test traffic is data in the client's account.** On live sites capture dry (`privacy_matrix.cjs --dry`): collection requests are answered locally, so no test hit reaches any account. Any live test stays short, and the report says when and from where you tested.
- **No personal data or secrets** in reports or ANALYTICS.md. Tag IDs are fine; tokens, emails and customer details are not. HAR files stay in the scratch folder.
- **Not legal advice.** Report what fires in each privacy state; compliance calls belong to the client's counsel.

## 1. Set up the audit

1. **Which site and which depth.** Ask once if unclear: the URL, tagging or full, and the business's main conversions (purchase, booking, lead). For Shopify, get the store domain and whether a theme preview or staging exists.
2. **Find the client file.** Follow `references/analytics-file.md` to find `ANALYTICS.md` (or legacy `ANALYTICS_GUARDRAILS.md`). If one exists, read it fully: it holds the tracking plan, past findings and the last test baseline, so this audit updates it rather than starting over. If none exists, create it from `references/analytics-template.md` at the end. Read `BRAND.md` if available for business type, markets and whether the category is regulated.
3. **Establish the access level** and say it in one line. Ask for what is missing only if the depth needs it:

   | Level | Access | Ask for |
   |---|---|---|
   | 0 | Public site | nothing |
   | 1 | Site code | repo path, or `shopify theme pull` of the live theme into a scratch folder |
   | 2 | Tag manager | GTM Admin > Export Container of the **published** version (JSON) |
   | 3 | GA4 | Google's Analytics MCP server signed in by the person (see `references/ga4-checks.md`), or screenshots and CSV exports |
   | 4 | Ad platforms and store admin | screenshots of Google Ads conversion status, Meta Events Manager overview and deduplication, Shopify Settings > Customer events and Customer privacy |

4. **Pick the pages**: home, a category or collection, a product or service, cart, the start of checkout or booking, the confirmation page if a test conversion is approved, key landing pages for paid traffic, and any third-party domain in the journey (booking engine, payment page). **Hybrid or headless stores** serve visitors from more than one host (a headless or custom front end, the platform's own domain or checkout subdomain, a theme preview of a site being rebuilt): run the page list on every host that visitors or the launch plan will use, and name the host in every inventory row.

## 2. Inventory (both depths)

Work outward from what visitors' browsers actually load.

1. **Page inventory.** On each page, run `scripts/page_inventory.js` in a browser (the browser tool's JavaScript action, or the DevTools console). It returns script hosts, vendor globals and IDs (per project for Clarity, Hotjar and TikTok), GTM containers, dataLayer events, gtag and consent commands, Google's consent state, the CMP, GPC, the Shopify theme and its role, pixel list, ScriptTags, app blocks and embeds, Customer Privacy state, cookie names, the tracking requests already sent, and `sameIdTwoPaths` (destination IDs found in more than one install point). Label every vendor with `references/vendor-signatures.md`.
   - **Browser state first.** Before the first page, say whether the browser profile is fresh. A used profile carries cookies, a stored consent choice (`customerPrivacy.visitorChoice`) and on Shopify a theme-preview cookie that keeps serving an unpublished theme on the live domain. Check `shopify.theme.role` (and `themeIsPreview`) on every Shopify page: anything other than `main` is a preview, so say so in every row it produced. Prefer a fresh profile; record the state in the report's method section either way.
   - **Interact, then wait.** Some sites load tools only after the first scroll or click (a second analytics project, replay tools, chat). Scroll once with the browser tool's own scroll or mouse action (scripted `scroll` events usually do not count), wait 3 to 5 seconds, then run the script.
   - **Fewer tokens.** Set `window.PAGE_INVENTORY_MODE = 'summary'` before the script for a 1 to 2 KB result; switch to full mode only for pages that need the detail. For many pages in one tab, set `window.PAGE_INVENTORY_KEEP = true` before the first paste; the script keeps itself in `window.name`, and later pages of the same site run `(0, eval)(window.name)` instead of a new paste. Clear it at the end (`window.name = ''`).
   - **What it cannot see.** Resource timing lists only this frame's requests, and some browser tools list first-party requests only. Sandboxed Shopify pixels (STRICT, LAX) and batched or POST hits need a HAR (`scripts/privacy_matrix.cjs`, then `scripts/decode_hits.py`). A tagging audit without a HAR reports app pixels from the pixel list, not from traffic, and says so.
2. **Shopify pixel list.** `python scripts/shopify_pixels.py <url>` lists every app and custom pixel with its sandbox, consent purposes and destination IDs; flags an ID that also appears in page code or **inside a GTM container on the page** (it reads each container's public `gtm.js`; pass `--gtm GTM-XXXX` for a container injected at runtime); and lists ScriptTags, app blocks and embeds and the theme that served the page. A `?preview_theme_id=` URL fetched without a browser session gets the published theme: the script warns, and previews need the browser inventory. Confirm custom pixel code in the admin when you have Level 4.
3. **Live container version.** `python ../analytics-guardrails/scripts/drift_snapshot.py <urls> --dir <snapshots folder>` records the live GTM version from the public `gtm.js` and the static page tags, in the snapshots folder the client file names (`references/analytics-file.md`), and compares with the last snapshot there. Compare the live version with any export you were given: an export older than the live version is stale, so ask for the current one.
   - **Stale or missing export: read the live build.** While you wait, `python scripts/gtm_public_rules.py GTM-XXXX` maps every live tag (by tag number, the same numbers as in an export) to its firing and blocking conditions, event names, destination IDs and paused state, from the public `gtm.js`. It is enough to confirm or retire findings, read string conditions (hosts, CTA wording, paths, dataLayer events) and spot changes since the old export. Names of tags, triggers and variables are not in `gtm.js`, so cite tag numbers and say the source was the public build.
4. **Code (Level 1).** Search the site code for tag IDs, vendor hosts and `dataLayer`/`gtag(`/`fbq(` calls, and for scripts that intercept link clicks and navigate in JavaScript (`preventDefault` plus `location` changes on links): they hide clicks from tag-manager listeners (FC-31). Note which theme is live: theme code changes with the theme, pixels do not (`references/platforms.md`). **App embeds and ScriptTags:** read them from the rendered page source (`<!-- BEGIN app block: shopify://apps/... -->` comments for embeds and app blocks; the `asyncLoad` URL list for ScriptTags), which `page_inventory.js` and `shopify_pixels.py` both list. A repo copy of `config/settings_data.json` is often stale or ignored by git; use it only to confirm.
5. **Container (Level 2).** `python scripts/gtm_export_summary.py <export.json> --out <scratch>/gtm.md` gives destinations, tags, the site dependencies the container needs (link text, URLs, hostnames, forms, dataLayer events and keys, DOM selectors) and health flags (paused, orphans, unused variables, duplicate Google tags, consent settings, unstable event ids, risky Custom HTML).
6. **GA4 settings (Level 3).** Work through the settings checklist in `references/ga4-checks.md`.
7. **Assemble the stack inventory**: one row per destination and install point, with IDs, host, consent gate and evidence. **Check every destination for a second path:** compare the pixel destination IDs with the IDs inside each tag-manager container (`shopify_pixels.py`, `sameIdTwoPaths`, or `gtm_public_rules.py --ids`), with hardcoded tags in theme code, and with gtag commands a vendor page pushes. List every destination reached by more than one path in one line under the inventory.

## 3. Tagging audit: judge what exists

For each inventory row and each container finding, decide: keep, fix, or question. Use `references/findings-catalog.md` to name what you see (FC codes) and set severity. Typical tagging-audit findings: a destination installed twice, an app's gtag commands sharing the container's dataLayer (FC-33), tags that cannot see what they wait for (GTM in a sandbox, dead dataLayer events, base page views waiting for a previous platform's push), stale site dependencies, consent defaults missing, leftovers, unowned tags, GA4 defaults.

**Tracking plan (section 1 of ANALYTICS.md).** If it is empty, draft it from the business type and what the container already measures, marked as a draft for the client to confirm. If it exists but disagrees with the live container (events renamed, paused or removed since it was written), do not edit it: record a finding for the difference and add a question for `analytics-setup`, which owns the plan.

A tagging audit stops here: write the report (step 6) with "what exists" and "what should change".

## 4. Full audit: prove the core events

1. **Confirm the tracking plan** with the person: the core events by tier, which destinations should receive each, and the key parameters. Without an agreed list there is nothing to test against.
2. **Run the privacy matrix** (`references/privacy-matrix.md`). Automated: `node scripts/privacy_matrix.cjs --dry --scenarios journeys.json --states fresh,accept,reject,gpc,blocked --out <scratch>/matrix [--proxy <region proxy>]` (needs Playwright in a scratch folder; `--url` pages work too). **Use `--dry` on live sites:** every collection request is answered locally and logged in full, so nothing reaches the client's accounts. The browser hides the automation flag by default, because some pixels send nothing otherwise. By hand: a fresh browser profile per state, DevTools Network open with "Preserve log", then Save all as HAR (live hits; keep it short). Cover each region type the store serves, or mark it not tested.
3. **Trigger each core event** in the states that matter (at least accept and reject; all states for Tier 1) with one labelled scenario per journey, each in a fresh profile. Clicks are dispatched on the element and a link's navigation is answered locally, so tag-manager link listeners fire as for a person and the page stays; test each booking or checkout landing with its own `goto` to the URL the CTA points to (a landing that redirects is recorded, FC-35). Purchases and bookings only with the owner's approved test method.
4. **Decode what left the browser**: `python scripts/decode_hits.py <state>/hits.har --by-step` per state shows what each step sent (and steps that sent nothing); `--by-source` names the install point behind each hit (frame, GA4 endpoint, GTM container marker, Meta event id prefix, Shopify app endpoints) and lists events a destination got from more than one source in the same step (FC-01, FC-33), and hits whose page address is a pixel sandbox (FC-34). Google mirrors and Merchant Center are listed apart, never as GA4 events. Compare with the expectations table in the privacy-matrix reference.
5. **Confirm on the receiving side** where you can: GA4 realtime (`run_realtime_report`) or DebugView, Google Ads conversion diagnostics, Meta Test Events and deduplication, TikTok Events Manager. Without access, ask the person for a screenshot taken during your test window.
6. **Data checks (Level 3)**: run the data checks in `references/ga4-checks.md` (duplicate transactions, platform gap, hostnames, self-referrals, channel health, landing pages, event hygiene, page views per session, PII).
7. Record each event and state as: sent once, sent twice, not sent, sent cookieless, or not tested.

## 5. Findings

One row per finding: ID, severity (S1 to S4), the catalog code, what was seen, the evidence, the business effect in plain words, the suggested fix and its owner (site, analytics owner, platform vendor, client). Order by severity, then by how many core events it touches. Sort them into three tables (the report template has them): **broken** (an event that should fire does not, or fires wrong), **risky** (works today but breaks on a likely change, or a legal or data-quality exposure) and **hygiene** (clutter, unowned tools, cost).

## 6. Write it up

1. **Report** for the client and the team, following `references/report-template.md`. Save it next to ANALYTICS.md as `analytics-audit-<YYYY-MM-DD>.md` (or where the project keeps QA notes). Offer a shareable page if the person wants to send it on.
2. **ANALYTICS.md**: update front matter (`last_audit`, `sources`, `snapshots`), section 2 (inventory, with the multi-path line and the install points checked), 3 (consent), 5 (findings, keeping old IDs and statuses), 8 (baseline and matrix result, full audit only), 9 (questions) and 10 (changelog). Draft section 1 only if empty (step 3). Leave sections 4 and 6 to `analytics-guardrails` unless they are empty, in which case seed section 4 from the container's site dependencies. **Older or legacy files** (other section numbers, no severity or status columns, their own ID style): follow the mapping rules in `references/analytics-file.md` section 4; never renumber.
3. **Hand-off**: suggest `analytics-setup` for the fixes (it builds the prioritised plan and asks for approval), `analytics-cleanup` if the stack is heavy or full of leftovers, and `analytics-guardrails` to build the dependency register and start drift checks.

## Final message

Access level reached, browser state, and what could not be checked; the top findings in plain words; where the report and ANALYTICS.md are; questions for the client; the suggested next skill.

## Checklist

- [ ] Client file found or created; BRAND.md read if present
- [ ] Access level stated; missing access asked for or listed as a limit
- [ ] Browser state recorded (fresh profile or not; Shopify theme role on every page)
- [ ] Every host in the journey inventoried (headless front end, platform domain, preview, third-party domains)
- [ ] Inventory covers every install point (theme, embeds, ScriptTags, pixels, tag manager, server, third-party domains)
- [ ] Live GTM version compared with any export used; a stale export backed by `gtm_public_rules.py` and said so
- [ ] Every destination checked for a second path, including IDs inside tag-manager containers; multi-path line written
- [ ] Drift snapshot saved in the client's snapshots folder
- [ ] Full audit: tracking plan agreed; matrix run per state and region type, or marked not tested
- [ ] Full audit: captured dry on live sites (or live hits listed with time and place); every core event decoded per state and attributed to its install point; receiving side confirmed or listed as not confirmed
- [ ] Findings have evidence, severity, catalog code, effect and owner
- [ ] Report written; ANALYTICS.md updated with dates and sources
- [ ] Nothing changed on the site or any account; no personal data stored
