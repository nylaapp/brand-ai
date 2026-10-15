---
name: analytics-guardrails
description: "Keep a site's analytics working after setup, for any store or business. Build: derive the site dependency register and rules from a GTM export, Shopify pixels and site code (link hosts, CTA text, page paths, hostnames, form behaviour, dataLayer events conversions rely on). Check: before and after any site, theme, content, app or domain change, find the tracking at risk, run static and live checks, log an analytics-impact line. Watch: a scheduled, no-login drift snapshot (live GTM version, pixel list, script hosts, theme, tag IDs) plus optional GA4 sanity checks. Writes to ANALYTICS.md. Use for \"analytics guardrails\", \"will this change break tracking\", \"check analytics impact\", \"build the dependency register\", \"refresh guardrails from the new GTM export\", \"did someone change GTM\", before a theme switch or domain change, or when a project rule asks for an analytics impact check. Read-only toward tags and accounts."
---

# Analytics guardrails (maintenance)

## Effort (read before starting)

Build: about 45 to 90 minutes from a GTM export and the site code; refreshing from a new export about 20 to 40 minutes. Check: 5 minutes when nothing is at risk, 20 to 40 minutes with live checks. Watch: about 1 minute per run once set up. Estimates, not yet measured. Stop and report if a build passes 3 hours.

Most analytics failures after launch are caused by ordinary site work: a reworded button, a link turned into a button, a moved page, a new theme, an app someone installed. None of them shows an error. This skill keeps a register of what tracking depends on, checks every change against it, and watches for changes made outside the code.

If the project has its own instructions file (AGENTS.md, CLAUDE.md) with an analytics or QA-log rule, read it first; it outranks this skill and usually says where the impact line goes.

## 0. Non-negotiables

- **Read-only toward tags and accounts.** This skill never edits a container, pixel, consent setting or account. A needed fix goes to `analytics-setup` (or the owner, with exact steps).
- **Never write "no impact" without looking.** The impact line names the rows and rules checked, or says "NOT verified" with the reason.
- **Tier 1 at risk is stop-ship:** the change needs the analytics owner's written OK or a different approach.
- **Exports go stale.** A register built from an export older than the live GTM version is flagged as stale until refreshed.
- Never sign in for anyone; scheduled runs never ask for or use credentials.

## 1. Find the client file

Follow analytics-audit `references/analytics-file.md` (accepts the legacy name `ANALYTICS_GUARDRAILS.md`). Read sections 1, 4, 6 and 8. If there is no file or no tracking plan, run `analytics-audit` (tagging) first; guardrails without a plan protect the wrong things.

## 2. Build mode: register and rules

Follow `references/dependency-register.md`.

1. **Freshness.** `python scripts/drift_snapshot.py <site urls>` shows the live GTM version. Use an export of that version; if the person's export is older, ask for the current one and mark the register stale until it arrives.
2. **Container dependencies.** `python ../analytics-audit/scripts/gtm_export_summary.py <export.json>` lists every trigger condition and variable that reads the site. For a refresh, also `--diff <old export> <new export>` and revisit only the rows touched.
3. **Other sources:** custom pixel code (custom events the site must publish), site code (`dataLayer.push`, `Shopify.analytics.publish`, data attributes), third-party domain contracts (a booking engine's `purchase` push and its keys).
4. **Check reality** for each dependency in the site code and on live pages, with evidence and date.
5. **Write** section 4 (one `D` row per dependency, grouped by kind, with status and the events it feeds), section 6 (rules for every Tier 1 and 2 dependency plus the general rules, and the change-impact matrix), and section 8 (static check commands with expected results). Keep existing IDs; retire rows instead of deleting them.
6. Broken or at-risk rows become findings in section 5 (catalog FC-07, FC-08, FC-19 and so on) for `analytics-setup` to fix.

## 3. Check mode: before and after a change

Follow `references/change-check.md`.

- **Before:** list the touched components, look them up in the register and the impact matrix, name the events at risk and their tiers, and plan the after-check. Tier 1 at risk with a rule broken: stop and ask for the owner's OK.
- **After:** run the static checks for those rows, the live checks for the events at risk (accept state; reject too for Tier 1), update the register's reality and add any new dependency, and log the impact line in the project's QA log: `Analytics impact: none (checked D-x..D-y, G-a..G-b) | checked: <what, how> | NOT verified: <reason>`.
- Theme switches and base-theme upgrades are full checks: diff tracking between themes and run the privacy matrix on the new theme's preview before it is published.

## 4. Watch mode: drift

Follow `references/drift-watch.md`.

1. Run `python scripts/drift_snapshot.py <2 to 4 urls> --dir <client folder>/analytics-snapshots`. The first run is the baseline; later runs print what changed.
2. For each change, report it in plain words with the action from the drift table (new export and diff, find a new install point, identify a new host, run a theme-switch check).
3. Optional with GA4 access: the weekly data checks (event volumes vs trailing average, page views per session, duplicate transactions, new hostnames).
4. Offer to schedule it (weekly by default; daily around a launch) with the environment's scheduler. A scheduled run only reads and reports.

## 5. Record

ANALYTICS.md sections 4, 6, 8 and 10 for build; the touched rows and the QA-log line for check; the changelog line for any drift found, with what was done about it.

## Final message

Build: rows and rules written, how many broken or at risk, the export version used and whether it is current. Check: events at risk, checks run, the impact line. Watch: drift found (or "no drift since <date>") and the next run.

## Checklist

- [ ] Client file read; tracking plan present (or tagging audit run first)
- [ ] Register built from an export matching the live GTM version, or marked stale
- [ ] Every Tier 1 and 2 dependency has a rule; general rules and impact matrix present
- [ ] Static checks written with expected results
- [ ] Check mode: rows looked up before the change; static and live checks after; impact line logged
- [ ] Watch mode: baseline saved; drift reported with actions; schedule offered
- [ ] Nothing edited in tags, pixels, consent or accounts
