# The weekly check-in (ask first, then write)

By default the autopilot **asks before it writes**. A scheduled run scans cheaply, picks the best idea, and sends the user one short message. Nothing is drafted until they answer. This keeps usage low (most weeks may end in "skip") and keeps the user in charge of what goes on their blog. Brands that want fully hands-off drafting can switch to `approval: auto_draft` in their profile.

```
scheduled run → scan → score → decide → CHECK-IN MESSAGE → (user replies) → hand off to the writer → log
```

## 1. When it applies

| `approval` in the profile | Behavior |
|---|---|
| `ask_first` (default) | Steps 1–5 as usual, then send the check-in. Hand off only after the user chooses to write. |
| `auto_draft` | Skip the check-in. Hand off every `write` decision (up to the caps) as hidden drafts, as before. |

A dry run never sends a check-in or creates anything; it shows what the check-in would say.

## 2. The check-in message

Keep it short. One top idea, up to two alternates (fewer if fewer exist, none if there are none), the reason, and the choices. No jargon.

```
Hi! It's time for this week's blog check-in for <Brand>.

Top idea: "<working title>"
- Why now: <one line of evidence: a new product, a search query ranking on page 2, a question customers keep asking, an upcoming date>
- Goal: <education | brand journal | search visibility | promotion>

Also on the list: "<idea 2>" · "<idea 3>"

What would you like to do?
1. Write it for me — I'll research, write and save a hidden draft in Shopify (no more questions)
2. Let's do it together — I'll ask a few questions and check in with you along the way
3. Pick a different idea
4. Skip this week
```

If no idea clears the thresholds, send nothing (a quiet run) and log it. Don't nag the user with weak ideas.

Present the choices with AskUserQuestion when a user is present; in a scheduled session, put them in the final message and wait for the reply.

## 3. Handling the reply

| Reply | Do this |
|---|---|
| **Write it for me** | Build the autopilot brief (`handoff.md`) with `Mode: fully automated` and call the writer. The reply is the go-ahead; no other confirmation. |
| **Do it together** | Build the brief with `Mode: guided`. The writer runs its guided setup, skipping what the brief answers. |
| **Pick a different idea** | Show the next 3 backlog ideas with a line each; when chosen, treat as above. |
| **Skip this week** | Log it; move the idea to backlog with its expiry; mark the week as skipped. Don't re-ask until the next scheduled run. |
| Asks to change something ("make it about X", "more promotional") | Update the candidate (keyword, intent) and re-confirm in one line, then proceed. |

The brief's `Intent`, `Media` and `Format` come from the profile defaults unless the user states otherwise in the reply. (Intent defaults by trigger: store and occasion triggers → promotion; search, competitor and AI-citation triggers → search; customer-question triggers → education.)

## 4. Unanswered check-ins

A scheduled session may end before the user replies. Record it in the ledger so the next run behaves:

```json
"checkin": {"date": "2026-10-05", "candidate_ids": ["gsc-..."], "status": "awaiting_reply", "expires": "2026-10-19"}
```

- `expires` is the check-in date plus `schedule.checkin_expire_days` (default 14), so a weekly schedule gives one quiet reminder week before a fresh check-in.
- Next run, if `checkin.status` is `awaiting_reply` and today is **before** `expires`: don't send a second check-in. Add a one-line reminder ("Still waiting on last week's idea") to the report, and send a new check-in only if something urgent appeared (a deadline in under 14 days).
- On or after `expires`: mark it `lapsed`, move its ideas to the backlog, count it as a skip, and send a fresh check-in.
- **Late replies:** if the user answers in a later session ("write the idea from last week's check-in"), read `checkin` from the ledger, including a lapsed one, process the reply as above, and then clear `checkin`.
- The ledger key is `checkin`, not `pending`, because topics already use the status `pending` (decided, not yet written).

## 5. Caps and logging

- **Don't touch the ledger's topics before consent.** In `ask_first` mode, run `score_opportunities.py` **without** `--write-ledger` until the user chooses to write. Then add the chosen topic (status `pending`, then `drafted` when the writer returns). This stops an unanswered check-in from using up a weekly-cap slot or blocking a cluster.

- A check-in doesn't use a weekly-cap slot. Only a created draft does.
- Log every check-in (sent, answered, skipped, lapsed) in the ledger's `runs`, so the report can show the user's response history.
- A lapsed check-in counts as a skip. If the user skips or lets three check-ins lapse in a row, mention it in the report and offer to change the schedule or thresholds ("Want fewer check-ins, or a different day?").

## 6. What to verify with a real user

How a scheduled task shows its message and takes the reply depends on the app: the task runs in its own session and the user answers there. Test it once with a real user at setup ("Want me to send a test check-in now?") and note the result in the run report. If replies can't be captured in that session, fall back to a message that tells the user to start the blog writer with the idea, and say that in setup.
