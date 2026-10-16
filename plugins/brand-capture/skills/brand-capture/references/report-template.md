# Report template (last step). Shown in chat; also saved to the scratch folder as brand-capture-report-<date>.md

Keep it short: the person reading it decides what to send the client and what to approve.

```markdown
# brand-capture · <Brand> · <new | apply-answers | apply-documents | split-voice> · <YYYY-MM-DD>

**Saved:** <path to BRAND.md> · rev <n> · <draft | approved> · <lines> lines · validator <OK | n warnings>
**Voice file:** <path to BRAND-VOICE.md> · rev <n> · <lines> lines
**Design file:** <path to design.md, or "existing: <path>"> · rev <n> · <lines> lines · measured <date and viewports, or "scan CSS only">
**Client copy:** <path to BRAND.html, which includes the voice> (send it with the questions, or after approval)
**Next step:** <send the <n> questions to <approver> | apply the answers | nothing pending>
**Run:** <minutes> min · model <name, effort> · <n> pages fetched

## What the file says (the 3 or 4 most useful findings)
- <positioning in one line>
- <catalog size and price range, or services>
- <names and architecture, if more than one name>
- <voice and claim limits in one line>

## Questions sent to the client (max 4)
| Id | Question |
|---|---|

## Held for later (reviewer only)
| Id | Item | Why it waited |
|---|---|---|

## For the agency, not the client
<site problems found while reading (outdated pages, wrong addresses), font licences, accounts to connect. Never
in BRAND.md.>

## Coverage
| Page type | Read | URL(s) | Notes |
|---|---|---|---|

## Client documents (only when the client gave any; `client-documents.md` §8)
| Document | Dated | Pages | Read how | sha8 |
|---|---|---|---|---|

- **What changed:** <section: before → after, one line each>
- **Left out as illustration:** <mockup prices, offers, counts, names not used>
- **For the design doc owner:** <visual items the documents add or contradict>
- **Conflicts with the site or repo:** <each with its Q-id>


## Linked to BRAND.md
| File | Status |
|---|---|
<from link_brand.py; plus "Cowork / Claude project: paste the one-line instruction into the project's
instructions" when the run was in Cowork or a Claude project>

## Not done
<pages blocked by robots or errors; client-rendered pages read without a browser; anything skipped>

## Next
- Deep competitor research: run the competitor-research skill to write COMPETITORS.md (about <n> min); when
  COMPETITORS.md already exists and only the client's side changed, its client-refresh mode.
```
