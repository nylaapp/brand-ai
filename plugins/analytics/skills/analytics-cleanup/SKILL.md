---
name: analytics-cleanup
description: "Clean up and optimise a site's analytics and marketing tags, for any store or business. Quick Cleanup removes what is clearly dead, duplicated or left behind (double installs, uninstalled-app leftovers, Universal Analytics, paused and orphan GTM items, unused pixels, idle A/B and heatmap tools) without touching anything a conversion depends on. Deep Tag Cleanup is zero-based budgeting: measure pages with every tag off, add tags back one group at a time with repeated Lighthouse runs, require an owner and a question per tag, allow one heatmap tool at a time during a study, and load each tag no earlier than needed. Blocks tags in the test browser, so live stores are benchmarked safely. Writes the load policy to ANALYTICS.md. Use for \"clean up our tags\", \"quick cleanup\", \"deep tag cleanup\", \"zero-based\", \"too many pixels\", \"are tags slowing the site\", \"remove old tracking\". Never removes or publishes without approval."
---

# Analytics cleanup (quick and deep)

## Effort (read before starting)

Quick cleanup: about 1 to 2 hours for a typical store once an audit exists, plus owner turnaround. Deep cleanup: about half a day to a day of work spread over a week (owners, approvals, re-measurement), plus a field-data check 28 days later. Each `tag_cost.py` configuration takes about 30 to 60 seconds per Lighthouse run. Estimates, not yet measured. Stop and check in if a quick cleanup passes 3 hours or a deep cleanup's measurement passes 2.

Every tag costs speed, consent scope and maintenance, and many stay long after anyone reads their data. This skill removes the dead weight (quick) and then makes every remaining tag earn its place and load at the right moment (deep). It starts from an audit, because cleaning what you have not inventoried is how conversions get deleted.

If the project has its own instructions file (AGENTS.md, CLAUDE.md), read it first; it outranks this skill.

## 0. Non-negotiables

- **Audit first.** Use a tagging or full audit from `analytics-audit` that is less than 30 days old and matches the current live GTM version (`analytics-guardrails` drift check); otherwise run the tagging audit first.
- **Never touch what a core event depends on** in a quick cleanup: anything in the tracking plan, the dependency register, the rules, consent tools, conversion tags, or the only path to a destination.
- **Disable before delete.** Pause, disconnect, or remove in a duplicate theme; delete after a quiet week with the owner's OK.
- **Approval per item**, from the person who owns that tool. Publishing a GTM version, changing a live pixel or a live theme needs that owner's explicit OK for that change. Which theme code changes go on is settled once, the first time a change touches theme code (`../analytics-setup/references/theme-target.md`); for the live theme the owner's yes comes before the edit and again before the push.
- **Benchmarks block in the browser, never on the store.** `tag_cost.py` changes nothing on the site.
- **Never trade a Tier 1 event for speed.** Change how an expensive conversion tag loads; never drop the conversion.
- **Lab numbers are lab numbers.** Report them as comparisons, not as real-user promises.
- Never sign in for anyone or type credentials.

## 1. Set up

1. Find the client file (analytics-audit `references/analytics-file.md`) and read sections 1, 2, 4, 6 and 7. Check the audit date and the GTM version it used against the live one (`python ../analytics-guardrails/scripts/drift_snapshot.py <url>`).
2. Ask which mode, if unclear: **quick** (safe removals) or **deep** (zero-based). Deep starts with a quick pass.
3. Confirm who owns each system that may change (theme or site code, Shopify apps and pixels, GTM, each vendor account).

## 2. Quick cleanup

Follow `references/quick-cleanup.md`:

1. Build the candidate list from the audit inventory, `../analytics-audit/scripts/gtm_export_summary.py` health flags (paused tags, triggers without tags, unused variables, Universal Analytics, duplicate Google tags) and `../analytics-audit/scripts/shopify_pixels.py` (duplicates, unknown apps, custom pixels).
2. Drop every candidate that a core event, the dependency register or a rule depends on. Unidentified tags go to the deep cleanup and the client's questions, not to removal.
3. Ask the owner for approval per item, with evidence, in plain words.
4. For each approved item: backup (setup skill `references/fix-playbooks.md` P12), disable, verify (inventory shows it gone; Tier 1 and Tier 2 events still fire once in the accept state), log.
5. Show before and after: counts of tags, hosts and pixels, and a short `tag_cost.py` comparison.

## 3. Deep cleanup (zero-based)

Follow `references/zero-based.md`:

1. **Owners and questions.** For every tag in the inventory, record owner, the question it answers, when its data was last used, and where it is needed. Write them into ANALYTICS.md section 7 before measuring.
2. **Benchmark.** On 3 to 4 representative pages, mobile first:
   `python scripts/tag_cost.py <url> --runs 5 --mode addback --out <scratch>/cost-<page>.md`
   Add client-specific groups with `--groups` (first-party or server-side endpoints). `--list-groups` shows the built-in groups. Read the all-on vs all-off gap first: if it is small, say the deep cleanup is about hygiene and risk rather than speed.
3. **Decide per tag** with the decision table (keep at load, keep deferred, keep only where used, on demand, move, remove). One heatmap or replay tool at a time, only during a study with an end date. Present a table (tag, owner, question, cost, decision, why) and get approval per tag.
4. **Implement** with `references/load-timing.md` (what must stay early, what can wait, how to delay it in theme code, app embeds, Shopify pixels or GTM). Removals first, then template conditions, deferrals, on-demand switches, moves. Anything that touches a destination path uses the setup skill's playbooks (P1, P2, P6) and rollback kit (P12). Re-verify Tier 1 and Tier 2 events after each batch.
5. **Re-measure** with the same pages and settings; report before and after. Set a field-data check (PageSpeed Insights / CrUX) 28 days after the last change.

## 4. Record

- ANALYTICS.md section 7 (load policy: every tag's owner, question, timing rule, cost, decision, review date), section 2 (inventory statuses), section 5 (findings statuses), section 6 (rule: no new tag without a load-policy row), section 10 (changelog with approvers).
- The project's QA log if it has one.
- A short client note: what was removed or delayed, the measured lab difference, what they might notice (for example a heatmap tool now off until the next study), and the field-data check date.

## Final message

Mode run; items removed, delayed or kept with reasons; before and after numbers (lab, with run counts); what waits on whom; the field-data check date; anything that turned out to be load-bearing and was left alone.

## Checklist

- [ ] Audit less than 30 days old and on the live GTM version, or tagging audit run first
- [ ] Candidates checked against tracking plan, dependency register and rules
- [ ] Approval per item from its owner; backups ready
- [ ] Disabled before deleted; quiet-week deletes scheduled with the owner
- [ ] Tier 1 and 2 events re-verified after each batch
- [ ] Deep: owner and question for every tag; all-on and all-off measured; median of 5 runs on the final pass
- [ ] Deep: one heatmap tool at most, with a study and end date
- [ ] Load policy, inventory, findings, rules and changelog updated
- [ ] Field-data check dated
