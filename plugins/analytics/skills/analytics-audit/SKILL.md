---
name: analytics-audit
description: "Audit a website's analytics and tagging, for any store or business. Tagging Audit: inventory of everything installed, where, what it sends, and what should change. Full Analytics Audit: also tests every core event end to end across privacy states (no choice, accept, reject, GPC, blocked) and regions. Finds double tracking, missing conversions, consent gaps, broken cross-domain, leftover and unowned tags and GA4 settings problems, with evidence. Works from the public site alone; goes deeper with site code, a GTM export, GA4 access or screenshots. Shopify-first (app and custom pixels, app embeds, Google & YouTube app, Customer Privacy API); also WordPress and custom sites. Writes a client-ready report and the shared ANALYTICS.md. Use for \"audit the analytics\", \"tagging audit\", \"check our tracking\", \"are we double counting\", \"why don't GA4 and Shopify match\", \"check consent mode\", or new-client analytics. Read-only."
---

# Analytics audit

## Effort (read before starting)

Tagging audit: about 30 to 60 minutes for one site from the public pages, plus 15 to 30 minutes per extra access level (code, GTM export, GA4). Full audit: add about 1 to 2 hours for the privacy matrix and core-event tests, more if test orders or bookings must be arranged. Estimates, not yet measured. Stop and report if a tagging audit passes 2 hours or a full audit passes 5.

Analytics is only useful if the numbers can be trusted, and most breakages are silent: a duplicated tag, a renamed button, a consent banner that never tells the store the visitor said yes. This skill finds out what is really installed and what really leaves the browser, so decisions about fixes rest on evidence. It changes nothing; fixes go through `analytics-setup` (getting it working) or `analytics-cleanup` (removing and slimming).

If the project has its own instructions file (AGENTS.md, CLAUDE.md) with analytics or safety rules, read it first; it outranks this skill.

## 0. Non-negotiables

- **Read-only.** Never edit tags, containers, pixels, theme code, consent settings or account settings. Never publish, pause or delete anything. Suggest; the person decides.
- **Evidence for every claim.** Each inventory row and finding cites what showed it (page source, a decoded request, an export line, a screenshot) and the date. Observed facts and inferences are labelled differently. "Not checked" is a valid answer; a guess is not.
- **Never sign in for anyone** or type credentials or 2FA codes. If a tool needs access, ask the person to sign in or to export what is needed.
- **No real orders, bookings or form submissions** without the owner's explicit OK for that specific test (see `references/privacy-matrix.md` section 4). Never type real customer data.
- **Test traffic is data in the client's account.** Keep live tests short, and say when and from where you tested.
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

4. **Pick the pages**: home, a category or collection, a product or service, cart, the start of checkout or booking, the confirmation page if a test conversion is approved, key landing pages for paid traffic, and any third-party domain in the journey (booking engine, payment page).

## 2. Inventory (both depths)

Work outward from what visitors' browsers actually load.

1. **Page inventory.** On each page, run `scripts/page_inventory.js` in a browser (the browser tool's JavaScript action, or the DevTools console). It returns script hosts, vendor globals and IDs, GTM containers, dataLayer events and consent commands, Google's consent state, the CMP, GPC, Shopify theme, pixel list and Customer Privacy state, cookie names and the tracking requests already sent. Label every vendor with `references/vendor-signatures.md`.
2. **Shopify pixel list.** `python scripts/shopify_pixels.py <url>` lists every app and custom pixel with its sandbox, consent purposes and destination IDs, and flags an ID that also appears in page code. Confirm custom pixel code in the admin when you have Level 4.
3. **Live container version.** `python ../analytics-guardrails/scripts/drift_snapshot.py <urls>` records the live GTM version from the public `gtm.js` and the static page tags. Compare it with any export you were given: an export older than the live version is stale, so ask for the current one.
4. **Code (Level 1).** Search the site code for tag IDs, vendor hosts and `dataLayer`/`gtag(`/`fbq(` calls; list app embeds (`config/settings_data.json` > `current.blocks`) and snippets from apps no longer installed. Note which theme is live: theme code changes with the theme, pixels do not (`references/platforms.md`).
5. **Container (Level 2).** `python scripts/gtm_export_summary.py <export.json> --out <scratch>/gtm.md` gives destinations, tags, the site dependencies the container needs (link text, URLs, hostnames, forms, dataLayer events and keys, DOM selectors) and health flags (paused, orphans, unused variables, duplicate Google tags, consent settings, unstable event ids, risky Custom HTML).
6. **GA4 settings (Level 3).** Work through the settings checklist in `references/ga4-checks.md`.
7. **Assemble the stack inventory**: one row per destination and install point, with IDs, consent gate and evidence. Mark every destination that arrives by more than one path.

## 3. Tagging audit: judge what exists

For each inventory row and each container finding, decide: keep, fix, or question. Use `references/findings-catalog.md` to name what you see (FC codes) and set severity. Typical tagging-audit findings: a destination installed twice, tags that cannot see what they wait for (GTM in a sandbox, dead dataLayer events), stale site dependencies, consent defaults missing, leftovers, unowned tags, GA4 defaults. Draft the tracking plan (section 1 of ANALYTICS.md) from the business type and what the container already measures, marked as a draft for the client to confirm.

A tagging audit stops here: write the report (step 6) with "what exists" and "what should change".

## 4. Full audit: prove the core events

1. **Confirm the tracking plan** with the person: the core events by tier, which destinations should receive each, and the key parameters. Without an agreed list there is nothing to test against.
2. **Run the privacy matrix** (`references/privacy-matrix.md`). Automated: `node scripts/privacy_matrix.cjs --url <page> [--url ...] --states fresh,accept,reject,gpc,blocked --out <scratch>/matrix [--steps journey.json] [--proxy <region proxy>]` (needs Playwright in a scratch folder). By hand: a fresh browser profile per state, DevTools Network open with "Preserve log", then Save all as HAR. Cover each region type the store serves, or mark it not tested.
3. **Trigger each core event** in the states that matter (at least accept and reject; all states for Tier 1), using the journey steps or by hand. Purchases and bookings only with the owner's approved test method.
4. **Decode what left the browser**: `python scripts/decode_hits.py <state>/capture.har` per state. It lists each event per vendor with account, page, transaction or event id, value and Google consent state, separates blocked attempts, and flags repeats. Compare with the expectations table in the privacy-matrix reference.
5. **Confirm on the receiving side** where you can: GA4 realtime (`run_realtime_report`) or DebugView, Google Ads conversion diagnostics, Meta Test Events and deduplication, TikTok Events Manager. Without access, ask the person for a screenshot taken during your test window.
6. **Data checks (Level 3)**: run the data checks in `references/ga4-checks.md` (duplicate transactions, platform gap, hostnames, self-referrals, channel health, landing pages, event hygiene, page views per session, PII).
7. Record each event and state as: sent once, sent twice, not sent, sent cookieless, or not tested.

## 5. Findings

One row per finding: ID, severity (S1 to S4), the catalog code, what was seen, the evidence, the business effect in plain words, the suggested fix and its owner (site, analytics owner, platform vendor, client). Order by severity, then by how many core events it touches. Separate "broken" from "risky" from "hygiene".

## 6. Write it up

1. **Report** for the client and the team, following `references/report-template.md`. Save it next to ANALYTICS.md as `analytics-audit-<YYYY-MM-DD>.md` (or where the project keeps QA notes). Offer a shareable page if the person wants to send it on.
2. **ANALYTICS.md**: update front matter (`last_audit`, `sources`), section 2 (inventory), 3 (consent), 5 (findings, keeping old IDs and statuses), 8 (baseline and matrix result, full audit only), 9 (questions) and 10 (changelog). Draft section 1 if empty. Leave sections 4 and 6 to `analytics-guardrails` unless they are empty, in which case seed section 4 from the container's site dependencies.
3. **Hand-off**: suggest `analytics-setup` for the fixes (it builds the prioritised plan and asks for approval), `analytics-cleanup` if the stack is heavy or full of leftovers, and `analytics-guardrails` to build the dependency register and start drift checks.

## Final message

Access level reached and what could not be checked; the top findings in plain words; where the report and ANALYTICS.md are; questions for the client; the suggested next skill.

## Checklist

- [ ] Client file found or created; BRAND.md read if present
- [ ] Access level stated; missing access asked for or listed as a limit
- [ ] Inventory covers every install point (theme, embeds, pixels, tag manager, server, third-party domains)
- [ ] Live GTM version compared with any export used
- [ ] Every destination checked for a second path
- [ ] Full audit: tracking plan agreed; matrix run per state and region type, or marked not tested
- [ ] Full audit: every core event decoded per state; receiving side confirmed or listed as not confirmed
- [ ] Findings have evidence, severity, catalog code, effect and owner
- [ ] Report written; ANALYTICS.md updated with dates and sources
- [ ] Nothing changed on the site or any account; no personal data stored
