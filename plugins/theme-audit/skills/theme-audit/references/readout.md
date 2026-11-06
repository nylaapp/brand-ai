# Readout: how the result is presented

`THEME-AUDIT.md` is the full record. The chat message is what the person actually reads, so it gets
its own layout, the same one the CRO audit uses: short, in plain words, in the order a store owner
thinks (what's wrong, what to do, how sure we are), not in the order the audit ran. The same text
goes at the top of `THEME-AUDIT.md` as **Read this first**, so a client opening the file sees it too.
The "How to reply" rules at the top of `SKILL.md` still apply to every word here (short, plain,
simple English, formal, not intimidating); this file adds the layout.

## Layout, in this order

Use these labels as short bold lines. Skip a part that has nothing in it.

1. **Headline.** Two sentences at most: the single thing that matters most, and the overall state.
   Lead with what a visitor feels (the page is slow to show its main picture on phones), not the method.
2. **What I looked at.** One line: the page and theme, devices, how many test runs, and what wasn't
   available. Example shape: "Live homepage on phone and desktop · 3 test runs each · Google's
   real-visitor data · theme code check · server timing. Not available: real-visitor data for this
   page."
3. **Scorecard.** One table, one row per category and device (skip a category the Lighthouse version doesn't have), using the words below as well as the
   number. Speed shows the middle of the runs and how much it moved.

   | | Phone | Desktop | What it means |
   |---|---|---|---|
   | Speed | 42 (poor) | 88 (good) | How fast the page shows and reacts |
   | Accessibility | 97 (good) | 97 (good) | How usable for people with disabilities |
   | Best practices | 77 (needs work) | 77 (needs work) | Safe, modern, error-free code |
   | Search (SEO) | 100 (good) | 100 (good) | Basics Google needs to read the page |
   | AI-assistant readiness (new, Google says still in development) | 75 (needs work) | 100 (good) | Whether AI assistants can read and use the page |
   | Server time (theme code) | about 510 ms (heavy) | | Time the server spends before sending the page |
   | Theme code check | 12 problems, 2 broken | | Shopify's own check of the theme files |

   Number bands (Lighthouse's own): **90 to 100 good, 50 to 89 needs work, 0 to 49 poor.** After a fix,
   show "before then after" in the cell ("42 then 61").
4. **The speed numbers in plain words.** Three or four bullets, one idea each, using the glossary:
   time until the main picture shows, how much the layout jumps, how long the page is frozen, and
   what real visitors see (or "not enough real-visitor data yet"). Say how far to trust the speed
   score: "scores moved from 38 to 45 between runs".
5. **What changed since last time** (re-audits only). Up to four bullets: fixed, new, and any
   correction ("Last time I said X; that was wrong because Y").
6. **Fix these first.** A table of at most five rows, most important first:

   | # | The problem | Why it matters | What to do | Who does it | How we know | Effort |
   |---|---|---|---|---|---|---|

   - **#**: the rank, then the finding ID in brackets so the person can refer to it later: "1 (TA-03)".
     IDs run TA-01, TA-02... in the file.
   - **The problem**: what a visitor experiences, in one sentence, with one concrete number ("The main
     picture takes about 40 seconds to show on a phone").
   - **Why it matters**: one sentence about the visitor or the goal, not a metric name.
   - **What to do**: one action.
   - **Who does it**: This theme (we can fix it), An app (name it), Store content (the store owner,
     in the admin), Shopify (nothing to do).
   - **How we know**: "Measured" (Lighthouse test), "Real visitors" (Google's data), "Theme code
     check", "Server timing". Add "likely" only for anything not measured.
   - **Effort**: Quick, Medium or Bigger.

   Rank by what visitors feel first: the main picture's time, then layout jumping, then frozen time,
   then accessibility failures, then everything else. Anything the theme can fix outranks an app
   cost of the same size only when the fix is safe; a large app cost still goes in the table, marked
   "An app".
7. **Quick wins.** Up to six one-line bullets of small, safe fixes not already in the table, each
   with who does it.
8. **Not the theme's to fix.** Up to four bullets: app and outside-script costs with their size and
   owner ("The chat tool adds about 250 KB and 50 ms of waiting; it belongs to the app's settings"),
   and things Shopify controls. This is where "why can't you get it to 100?" is answered.
9. **What I couldn't check.** One or two lines, every lane marked "not run" with its reason.
10. **Close.** The link to `THEME-AUDIT.md` and the folder of HTML reports (one per run, the person
    can open them in a browser), then one question offering the next step, such as applying the
    safe fixes on a draft theme.

## Writing rules

- **Plain words.** No shorthand in the chat: no "LCP", "TBT", "CLS", "TTFB", "Liquid", "render-blocking".
  If a technical term is unavoidable, explain it once in passing.
- **Round numbers** and say "about": "about 4 seconds", "250 KB". Seconds for anything over a second.
- **One idea per line.** Table cells are one sentence; bullets are one line. No nested bullets, no
  paragraph longer than three lines.
- **Five rows, not fifteen.** The full ranked list stays in the file. If more than five matter, say
  "N more in the file".
- **Keep the honesty, compress the caveats.** Every limit from the file still appears, in "What I
  couldn't check" or a one-line trust note, not spread through every sentence.
- **Say "phone" and "desktop".**
- **Never claim a speed change is real inside the run-to-run spread.**
- **Length:** about 250 to 400 words plus the tables. Never paste the file.

## Glossary: file terms to chat words

| In the file | In the chat |
|---|---|
| LCP (largest contentful paint) | time until the main picture or headline shows. Good: 2.5 s or less. Poor: over 4 s |
| FCP | time until anything shows. Good: 1.8 s or less. Poor: over 3 s |
| CLS | how much the page jumps while loading. Good: 0.1 or less. Poor: over 0.25 |
| TBT | how long the page is frozen while loading. Good: 200 ms or less. Poor: over 600 ms |
| INP | how fast the page reacts when tapped. Good: 200 ms or less. Poor: over 500 ms |
| TTFB, `server-response-time` | how long the page waits for the server |
| Field data, CrUX | real visitors over the last 28 days |
| Lab data | our test runs |
| Third-party script | code from another company (an app, a tracker, a chat tool) |
| Render-blocking | holds the page back until it has loaded |
| Theme Inspector, Liquid profile | server timing of the theme's code |
| Theme Check offense | a problem Shopify's checker found in the theme files |
| Fix, Skip, Ask (buckets) | the theme can fix it, someone else owns it, needs your decision |
| Spread | how much the score moved between test runs |
