# Quick cleanup: safe removals

Remove what is clearly dead, duplicated or left behind, without touching anything a core event depends on. A quick cleanup should be boring: low risk, easy to undo, done in an hour or two.

## 1. What qualifies

| Candidate | How it shows up | Safe when |
|---|---|---|
| Duplicate install of a destination (FC-01) | Same ID in two install points | The keeper is chosen (fix playbook P1) and covers the same events |
| Leftovers from uninstalled apps (FC-17) | Script hosts or snippets for apps not in the installed list; app embeds for removed apps | The app is confirmed uninstalled and nobody uses its data |
| Universal Analytics tags | `UA-` IDs, tag type `ua` | Always (UA stopped processing in 2024); keep the export for history |
| Paused GTM tags (FC-16) | Health flag "paused tag" | Owner confirms they are not coming back |
| Triggers without tags, unused variables (FC-16) | Health flags | Not referenced by a template or sequencing; owner agrees |
| Disconnected or empty custom pixels | Shopify Customer events | Owner confirms |
| A/B testing tool with no running test (FC-25) | VWO, Optimizely present | Owner confirms no live experiment |
| Second heatmap or replay tool (FC-26) | Two or more of Clarity, Hotjar, Lucky Orange, Crazy Egg | One is kept for the current study, or all are paused until one is needed |
| Tags for platforms the client stopped using | IDs for ad accounts no longer active | Owner confirms the account is closed or unused |

Not a quick-cleanup item: anything in the dependency register, anything a Tier 1 or Tier 2 event uses, consent tools, conversion tags, the only path to a destination, or anything nobody can identify (that goes to the deep cleanup as an unowned tag and to the client as a question).

## 2. Steps per item

1. **Evidence:** the inventory row, the export line or the snippet path.
2. **Dependency check:** search ANALYTICS.md sections 1, 4 and 6 for the tag, its trigger, its ID and its host. Any hit means it is not a quick item.
3. **Owner OK:** list the items in one message, plain words, with evidence; ask for a yes per item or for the list.
4. **Backup:** fix playbook P12 (duplicate theme, note the GTM version, screenshot pixel settings).
5. **Disable, do not delete:** pause, disconnect, remove from a duplicate theme. Delete after a quiet week with the owner's OK.
6. **Verify:** the inventory no longer shows it; a quick accept-state check that every Tier 1 and Tier 2 event still fires once; `theme check` unchanged if theme code moved.
7. **Log:** ANALYTICS.md section 2 (inventory status `removed YYYY-MM-DD`), section 5 statuses, section 10 changelog.

## 3. Show the result

Before and after: number of tags, script hosts and pixels; a quick `tag_cost.py --mode removal --runs 3` on the home page and one product or service page for the removed groups, or an all-on comparison before and after. Present the saving as lab numbers, not a promise of real-user speed.
