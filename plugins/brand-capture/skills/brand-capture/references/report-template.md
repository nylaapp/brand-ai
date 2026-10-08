# Report template (last step). Shown in chat; also saved to the scratch folder as brand-capture-report-<date>.md

Keep it short: the person reading it decides what to send the client and what to approve.

```markdown
# brand-capture · <Brand> · <new | apply-answers | split-voice> · <YYYY-MM-DD>

**Saved:** <path to BRAND.md> · rev <n> · <draft | approved> · <lines> lines · validator <OK | n warnings>
**Voice file:** <path to BRAND-VOICE.md> · rev <n> · <lines> lines
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

## Linked to BRAND.md
| File | Status |
|---|---|
<from link_brand.py; plus "Cowork / Claude project: paste the one-line instruction into the project's
instructions" when the run was in Cowork or a Claude project>

## Not done
<pages blocked by robots or errors; client-rendered pages read without a browser; anything skipped>

## Next
- Deep competitor research: run the competitor-research skill to write COMPETITORS.md (about <n> min).
```
