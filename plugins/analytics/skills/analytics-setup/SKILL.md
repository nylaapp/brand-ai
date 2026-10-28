---
name: analytics-setup
description: "Get a client's analytics working, as a partner through the whole critical path: collect the client's issue list (double tracking, anomalies, numbers that don't match), agree the tracking plan, run a full audit across privacy states, build a prioritised action list for approval, make approved fixes one at a time with a rollback ready, and re-test every core event. Also sets up tracking from zero. Any store or business; Shopify-first (Google & YouTube app, Meta app, pixels, Customer Privacy API, consent mode), also WordPress and custom sites. Keeps state in ANALYTICS.md. Use for \"fix our analytics\", \"get tracking working\", \"set up GA4\", \"conversions aren't showing in Google Ads\", \"Meta shows more purchases than we have\", \"set up consent mode\", or a list of analytics problems. Never publishes a container, changes consent or makes a test purchase without explicit approval."
---

# Analytics setup (getting it working)

## Effort (read before starting)

Intake and tracking plan: 30 to 60 minutes with the client's answers in hand. Audit: see `analytics-audit` (1 to 3 hours for a full audit). Fixes: 15 to 60 minutes each plus waiting on owners; plan for several sessions over days when GTM or ad accounts belong to someone else. Estimates, not yet measured. Stop and check in with the person at each approval point, and if a single fix passes 2 hours.

The goal is numbers the client can make decisions with: every core event reaching every destination that uses it, once, with the right values, and only when the visitor allowed it. The path is Michael's critical path: collect the issues, audit, prioritise and approve, fix, test. This skill runs that path with the person, keeps state in `ANALYTICS.md`, and never skips the approval or the test.

If the project has its own instructions file (AGENTS.md, CLAUDE.md), read it first; it outranks this skill. For theme code it usually defines where edits may go and what must be logged.

## 0. Non-negotiables

- **No change without approval.** Plan first, then change only the approved items. Approval names the item; "looks good" for a list approves that list only.
- **One change at a time, tested before the next.** Batch only changes that are tested together and owned by the same person.
- **Rollback ready before every change** (`references/fix-playbooks.md` P12).
- **Never publish** a GTM container, a live theme, or a pixel or consent change on a live store unless the owner explicitly asks for that specific publish. Prefer that the owner presses publish.
- **Consent is the client's legal decision.** Propose settings and mappings; the client (and their counsel) decides regions, categories and banner wording. Not legal advice.
- **Never sign in for anyone**, type credentials or 2FA codes, or accept terms on their behalf.
- **No real orders, bookings or form submissions** without the owner's OK for that test and an agreed test method; never real customer data.
- **Theme and site code follow the project's rules** (for a Shopify theme: prefer new files, mark and log any edit to a core file). Which theme the code goes on is asked once and remembered (`references/theme-target.md`), settled the first time a change touches theme code, not before; a draft or dev theme is recommended, and the live theme needs the owner's explicit yes before the edit and again before the push.

## 1. Intake

1. Find or create the client file (analytics-audit `references/analytics-file.md`); read `BRAND.md` if present. If ANALYTICS.md already has a plan and recent audit, say what you found and continue from where it left off.
2. Send the intake questions in `references/intake.md` (at most eight, one message). Triage the answers with its symptom table. Record each reported issue in ANALYTICS.md (section 5 as a suspected finding, or section 9 as a question) with the client's words.
3. Establish access and owners: who changes the tag manager, the store, each ad account; how fast. Missing owners block fixes, not the audit.

## 2. Tracking plan

Draft section 1 of ANALYTICS.md with `references/tracking-plan.md`: Tier 1 to 4 events for this business model, names per destination, key parameters, the value definition, and where each event originates. Review it with the person in plain words and mark it confirmed (date, by whom). Tests are only as good as this list.

**From zero** (no tracking yet): also choose the stack before the audit: destinations the business will actually use, one path per destination (P1), the consent approach for the regions served (P5). Then build in this order: consent foundations, base measurement, Tier 1, Tier 2, Tier 3, then verify everything with the full matrix.

## 3. Audit

Run `analytics-audit` in full mode, unless a full audit is less than 14 days old and the drift check (`analytics-guardrails` watch) shows no change since; then reuse it and say so. Every client-reported issue must come out of the audit as proved, disproved (with evidence) or not testable (with the reason).

## 4. Action plan and approval

Build the plan with `references/action-plan.md`: order (blocking decisions, consent, S1, S2, hygiene, the rest), one row per change with the exact object, system, who, effort, risk, test and rollback. Present it in plain words, then the table. Put blocking questions in section 9 with the item they block. Wait for approval; record who approved what and when in the changelog.

## 5. Fix

For each approved item, in order:

1. Prepare the rollback (P12) and say what it is.
2. Make the change with the matching playbook in `references/fix-playbooks.md` (P1 one path per destination, P2 remove a duplicate, P3 Shopify purchases, P4 storefront events for pixels, P5 consent, P6 GTM changes, P7 cross-domain, P8 lead and booking signals, P9 dataLayer pushes, P10 stale trigger conditions, P11 deduplication).
   - Changes we make: site or theme code, on the theme settled with `references/theme-target.md` (asked once, at the first theme-code change; a draft is recommended), following the project's rules.
   - Changes the owner makes: GTM publishes, ad accounts, Shopify settings, consent. Give them exact, numbered steps naming each object and value, and wait for them to confirm.
3. Verify right away (step 6) before the next item. If verification fails, roll back first, then investigate.

## 6. Test

1. For each fixed item, run the test named in the plan: the privacy-matrix states and core events it touches (scripts in `../analytics-audit/scripts/`: `privacy_matrix.cjs`, `decode_hits.py`, `page_inventory.js`).
2. Confirm on the receiving side (GA4 realtime or DebugView, Ads diagnostics, Meta Test Events) or ask the person for a screenshot from the test window.
3. After the last item, re-run the full matrix for every Tier 1 and Tier 2 event, in every state and region type that can be produced. Regions that cannot be produced are listed as not tested.
4. Static checks: re-run the inventory and `../analytics-audit/scripts/shopify_pixels.py`; the stack inventory must show one path per destination.

## 7. Record and hand over

1. ANALYTICS.md: findings statuses (`fixed (verified YYYY-MM-DD)` only with a verification line), section 8 baseline and matrix result, section 10 changelog with dates and approvers, and the date of every change that moves numbers.
2. The project's QA log if it has one (one line per change: what, why, how verified).
3. A short note for the client: what changed, what they will see in their reports (for example "page views drop by about half from 2026-10-20 because they were counted twice"), what to watch, and what still needs them.
4. Follow-ups: a data check 7 and 14 days later (duplicate transactions, platform gap, channel shares; `references/ga4-checks.md` in the audit skill); suggest `analytics-guardrails` (build the dependency register, start weekly drift checks) and `analytics-cleanup` if the stack is heavy.

## Final message

What was fixed and verified, what is waiting on whom, what the client will notice in their numbers and from when, the next check date, and the suggested next skill.

## Checklist

- [ ] Client file found or created; BRAND.md read if present
- [ ] Intake sent; every reported issue recorded in the client's words
- [ ] Tracking plan confirmed by the client (date, name)
- [ ] Full audit run or reused (less than 14 days old, no drift)
- [ ] Action plan ordered, with exact objects, owners, tests and rollbacks; approved per item or batch
- [ ] Each change made with its rollback ready, verified before the next
- [ ] No publish, consent change or test conversion without the named approval
- [ ] Final full matrix for Tier 1 and 2; regions not tested listed
- [ ] ANALYTICS.md, QA log and client note updated; follow-up check dated
