# Setup check: make sure the essentials are ready, and guide the person through what isn't

Run this **before the first step** of every Blog and content skill (`blog-generator`,
`blog-rewriter`, `blog-autopilot`, `fact-check` and `seo-audit`). It checks that what the skill needs
to run, and what it needs to do the job **well**, is in place, and walks the person through setting
up anything that is missing.

This file is the same in all five plugins. Plugins can't read each other's folders, so each keeps a
copy; change them together and keep them identical.

## Who you are guiding

Assume the person is **not technical**: a marketer, a store owner or a content writer. They may never
have connected a tool to Claude, opened a terminal or exported data from Google. So:

- **Do the checking yourself.** Find out quietly whether each item is there (try the connector, look
  for the file, run the command). Never ask "do you have the Shopify connector?"; check. Only bring
  the person the things that actually need them.
- **One missing thing at a time**, in the order of the table in section 3. Never dump the whole list.
- **Explain each thing in one plain sentence first**: what it is and what it does for this post or
  check ("Connecting Shopify lets me put the post straight into your store as a hidden draft, so you
  don't have to copy and paste it").
- **Numbered steps, one action per step**, naming exactly what to click or type, and what they should
  see when it worked.
- **Then say "Tell me when that's done"** and check again yourself. If it still fails, read the error
  and give the next step in plain words.
- **Never type a password, verification code or API key into a sign-in page** for the person, and
  never ask them to paste a password into the chat. They sign in themselves, in the window that asks.
- **Ask before installing anything** on their computer.
- **Keep it calm and short.** When everything needed is ready, say one line ("Setup check: everything
  this needs is ready.") and move on. Don't list what passed.

Once a check has passed in this conversation, don't run it again. In a new conversation, re-run the
checks; they're quick and silent when everything is fine.

## 1. Required, recommended and "makes it better"

- **Required:** the skill can't do its job without it. Stop and guide the person through it. If they
  can't do it now, stop politely (section 6).
- **Recommended:** the skill runs without it but the result is weaker, or it falls back (for example
  paste-ready HTML instead of a Shopify draft). Offer it **once**, say in one line what they get with
  it and what happens without it, and let them choose "set it up now" or "skip for now". If they skip,
  don't bring it up again in this conversation.
- Never block a run on a recommended item, and never pretend a fallback is as good as the real thing.

## 2. Runs with nobody there

In a **scheduled run, a test run, or a run the autopilot triggered in fully automated mode**, nobody can
answer. Check silently, never ask or guide, use the skill's own fallback for anything missing, and put
each missing item with its fix steps under "Needs your attention" in the run report (or the summary),
so the person can set it up later.

## 3. What each skill needs

Check only the rows for the current skill, in this order. R = required, Rec = recommended,
Opt = only when that situation applies, blank = not needed.

| # | Item | blog-generator | blog-rewriter | blog-autopilot | fact-check | seo-audit |
|---|---|---|---|---|---|---|
| A | The Claude desktop app with a folder on this computer | Rec | Rec | R | | Rec |
| B | Web search and web pages turned on in Claude | R | R | R | R | Rec |
| C | Brand files (`BRAND.md`, `BRAND-VOICE.md`) | R | R | R | Rec | |
| D | Competitor research (`COMPETITORS.md`) | Rec | | Rec | | |
| E | The other Brand AI plugins this one works with | Rec (fact-check) | R (blog-generator) | R (blog-generator) | | |
| F | Shopify connected (connector, or a browser signed in to the Shopify admin) | Rec | Rec | R | Opt (to check a Shopify article) | Rec |
| G | A browser Claude can use | Rec | Rec | | Opt (pages that need one) | R |
| H | Python 3 | Rec | R for series and image transfer, Rec otherwise | R | Rec | |
| I | Google Drive connected | | Opt (Google Doc sources) | | Opt (Google Doc sources) | |
| J | A Word (.docx) reader | | Opt (.docx sources) | | Opt (.docx sources) | |
| K | Google Search Console access | Opt (if they have it) | | Rec | | R for week 2 and week 4 checks |
| L | Review and helpdesk exports | | | Rec | | |
| M | A free PageSpeed API key | | | | | Rec |
| N | Scheduled runs: the computer awake with Claude open | | | R (for the weekly check-in) | | Opt (for daily checks) |

`blog-autopilot` hands off to `blog-generator` with the check already done: say so in the brief, so
the writer doesn't repeat it.

## 4. The checks, and how to guide each one

### A. The Claude desktop app with a folder on this computer

**Check:** you can read and write files in a working folder (the project's folder, or the folder that
holds the brand files).

**Why:** the skills keep each post's brief, HTML, checklist and audit log there, so nothing is lost
between sessions and clients don't get mixed up. `blog-autopilot` needs it to remember its settings
and past posts from week to week.

**If missing:** explain that, and guide:
1. Use the **Claude desktop app** (download it from **https://claude.ai/download** if they're in a web
   browser).
2. Start a **Cowork** task, and when it asks for a folder, choose or create one, for example
   `Documents/<store name>`. Use the folder that already holds the brand files if there is one.

In a plain chat with no folder, `blog-generator`, `blog-rewriter`, `fact-check` and `seo-audit` still
work but hand files back in the chat; `blog-autopilot` can't keep its weekly settings (its own
`references/setup.md` has the store-metafield fallback, which needs the person's yes).

### B. Web search and web pages

**Check:** a web search and a page fetch both work (try a search for the store's name).

**Why:** the post is researched fresh every time (what ranks now, sources, current rules on
regulated claims), and fact-checking needs the original sources.

**If missing:** in the Claude app, open **Settings** and turn on **web search** (in some plans an
admin turns it on for the whole organisation, so they may need to ask their Claude admin). If it can't
be turned on, say plainly that the research and fact-check will be limited to what they paste in.

### C. Brand files

**Check:** find `BRAND.md` and `BRAND-VOICE.md` for this store with the skill's own lookup (brand-capture
`references/brand-context.md`: project root, `~/` and `~/.claude/`, then
`~/.brand-ai/brands/<slug>/`). A file for a different store counts as missing.

**Why:** "Your brand files tell me how the brand sounds, what it sells, and what it can and can't
claim, so I don't have to guess or ask you every time."

**If missing:** offer to run **brand-capture** now (about 10 to 25 minutes, once per store). If it isn't
installed, guide the install as in row E.

### D. Competitor research

**Check:** `BRAND.md` names a `competitors_doc`, or a `COMPETITORS.md` sits next to it.

**Why:** "It shows what your competitors already write about, so your post covers what they miss
instead of repeating them."

**If missing (recommended):** offer to run **competitor-research** (it reads the competitors listed in
`BRAND.md`), or skip for now.

### E. The other Brand AI plugins

**Check:** the skill this one hands work to is available (`blog-rewriter` and `blog-autopilot` need
`blog-generator`; `blog-generator` hands claims to `fact-check`).

**If missing**, guide:
1. In the Claude app, open **Customize**, then **Plugins**.
2. Find the plugin (for example **blog-generator**) under the **Brand AI** marketplace and click
   **Install**.
3. Start a new task so Claude loads it, and ask again.

### F. Shopify connected

**Check:** the Shopify connector answers a read-only question about the shop (its name and domain), and
it is the **same store** the brand files are for. If there's no connector, check whether the browser is
signed in to that store's Shopify admin (`https://admin.shopify.com`).

**Why:** "Connecting Shopify lets me read your existing posts and products for links, and put the
finished post into your store as a **hidden draft** that only you can see until you publish it.
Without it you get the post as HTML to paste in yourself."

**If missing**, guide the connector first:
1. In the Claude app, open **Customize** (or **Settings**), then **Connectors**.
2. Find **Shopify** and click **Connect**.
3. A Shopify page opens: sign in with **your own** Shopify login and choose the right store.
4. Approve the access it asks for, then come back and tell me.

**If the connector can't be used**, the browser works too: open `https://admin.shopify.com` in the
browser Claude uses (row G), sign in yourself, and leave it open.

**If it's signed in to the wrong store**, ask them to switch store in the connector (or in the Shopify
admin's store picker) before going on. Writing to the wrong store is a stop.

**If Shopify says they don't have permission:** their staff account needs **Blog posts and pages**
(and **Files**, for `blog-rewriter`'s image transfer). The store owner turns these on in the Shopify
admin under **Settings > Users and permissions**, on that person's account.

### G. A browser Claude can use

**Check:** a browser tool is available (Claude in Chrome, or the browser built into the Claude app) and
can open a page.

**Why:** `seo-audit` checks the live post with Google's own tools (Rich Results Test, PageSpeed
Insights, Search Console), which only work in a browser. The writers use it to show a preview and as a
backup way into Shopify; the rewriter uses it for source pages that don't load as plain text.

**If missing**, guide:
1. Easiest: use the **Claude desktop app**, which has a browser built in; nothing to install.
2. For Search Console and the Shopify admin, **Claude in Chrome** is better, because it uses the Chrome
   you're already signed in to: install the **Claude in Chrome** extension from the Chrome Web Store,
   sign in to it with the same Claude account, and turn it on in the Claude app's settings. Keep Chrome
   open while the skill runs.

### H. Python 3

**Check:** `python3 --version` (Windows: `python --version` or `py --version`) prints 3.8 or higher.
Skip this row where commands can't run at all, and do the steps by reading instead.

**Why:** small helper scripts check the post before delivery (headings, links, leftover placeholders),
spot risky claims, score blog ideas and move images. They only use what comes with Python; nothing
else to install.

**If missing**, explain that Python is a free program the helper scripts run on, then:
- **Mac:** offer to run `python3 --version` once; if the Mac offers to install the **command line
  developer tools**, click **Install** and wait for it to finish. Otherwise download the installer
  from **https://www.python.org/downloads/** and click through it.
- **Windows:** download the installer from **https://www.python.org/downloads/**, and on the first
  screen **tick "Add python.exe to PATH"** before clicking **Install Now**.

Then quit and reopen the Claude app, and check again.

### I. Google Drive connected (only for a Google Doc source)

**Check:** the Google Drive connector can open the document link.

**If missing**, offer two ways and let them pick:
1. **Connect Google Drive:** in the Claude app, **Customize > Connectors > Google Drive > Connect**,
   sign in with the Google account that can open the document, and allow access.
2. **Or skip connecting:** in the Google Doc, choose **File > Download > Microsoft Word (.docx)** and
   attach the file here, or select all the text and paste it into the chat.

### J. A Word (.docx) reader (only for a .docx source)

**Check:** `pandoc --version`, or `python3 -c "import docx"` works.

**If missing**, keep it simple: offer to install the small reader for them (`pip3 install python-docx`,
or `brew install pandoc` on a Mac with Homebrew), with their OK. Or they open the file in Word or
Google Docs, select all, and paste it into the chat. Headings and links paste fine; tables may need a
second look.

### K. Google Search Console access

**Check:** in the browser, `https://search.google.com/search-console` opens and lists a property for
the store's domain (or, for `blog-autopilot`, a recent export is in `inputs/gsc/`).

**Why:** "Search Console is Google's free report on how your site shows up in search. It's the only
place real ranking numbers come from, so without it I can't say how a post is doing, and I won't
guess."

**If they're not signed in:** ask them to sign in themselves in that browser, with the Google account
that has access, then tell you.

**If the store isn't in their Search Console:** whoever owns it adds them: in Search Console, **Settings
> Users and permissions > Add user**, their email, permission **Full** or **Restricted**. If nobody has
set Search Console up for the store yet, that's a bigger job (verifying the domain); suggest asking
whoever manages the domain or website, and carry on without it for now.

**For `blog-autopilot`, export instead of browsing** (once a month):
1. In Search Console, open **Performance > Search results**.
2. Click the date filter, choose **Compare**, and pick **Last 28 days** vs **Previous period**. Apply.
3. Click **Export** (top right) and choose **Download CSV** (or **Download Excel**).
4. Put the downloaded file in the `inputs/gsc` folder inside the autopilot's brand folder (I'll tell
   you the exact folder).

### L. Review and helpdesk exports (blog-autopilot)

**Why:** "Real customer questions and reviews are the best source of post ideas that people actually
search for."

**If they want it:** most review apps (for example Judge.me, Yotpo, Okendo, Stamped) and helpdesks (for
example Gorgias, Zendesk) have an **Export** button that downloads a CSV, usually in the
app's settings or reviews list. Ask which app they use and give the steps for that app if you know
them; otherwise ask them to look for "Export" in it. Put the files in `inputs/reviews` and
`inputs/helpdesk`. Re-export about once a month.

### M. A free PageSpeed API key (seo-audit)

**Why:** "Google's free speed test is shared by everyone, and it's often busy. A free key of your own
means the speed check runs every time instead of saying 'not available right now'."

**If they want it**, guide:
1. Go to **https://console.cloud.google.com** and sign in with a Google account.
2. Create a project if asked (any name, for example "Store checks").
3. Search for **PageSpeed Insights API** at the top, open it and click **Enable**.
4. Go to **APIs & Services > Credentials**, click **Create credentials > API key**, and copy the key.
5. Open the file `scripts/psi_summary.js` and paste the key between the quotes on the `API_KEY` line,
   or give it to me and I'll put it there. I won't repeat it back or put it anywhere else.

It's free for this use. If Google asks for payment details, stop and skip this item: the audit still
runs, it just retries the speed check on the next run when Google's shared quota is busy.

### N. Scheduled runs: computer awake with Claude open

**Check:** only when the person asks for a schedule (`blog-autopilot`'s weekly check-in, `seo-audit`'s
daily check).

**Explain plainly:** "Scheduled checks run on your computer. At the scheduled time it needs to be on,
awake, and have the Claude app open. If it's asleep, that run is skipped and the next one catches up."
Suggest a time they're usually at their desk (the default is Monday 9:00), and that they keep the Claude
app open during the day. Then create the schedule as the skill describes.

## 5. Recommended next, after the first run

When the run is done and it went well, mention at most one recommended item that was skipped and would
have made the biggest difference (usually Shopify connected, Search Console or competitor research),
in one line. Don't repeat it in later runs once they've said no.

## 6. Hand-off

When every required item passes, say one line and go to the skill's first step. If a required item
can't be fixed now ("I'll ask the store owner"), stop politely: say what's left, that nothing was
written or changed, and that the next run picks up from here. For a recommended item that's still
missing, say in one line what the skill will do without it (for example "I'll give you the post as
HTML to paste in") and continue.
