# Setup check: make sure the essentials are ready, and guide the person through what isn't

Run this **before step 1** of every Pages and theme skill (`page-audit`, `page-create`,
`page-edit-content`, `page-edit-design`, the `page-studio` front door and `theme-audit`).
It checks that the tools and access the skill needs are in place, and walks the person through
setting up anything that is missing.

This file is the same in page-studio and theme-audit. Plugins can't read each other's
folders, so each keeps a copy; change them together and keep them identical. Only page-studio
has `connector-route.md` (changing a theme through the Shopify connector, with no CLI).
theme-audit has no connector route: it skips row K and the route choice, and always needs the CLI.

## Who you are guiding

Assume the person is **not technical**: they may never have opened a terminal, installed a
developer tool or heard of a "theme CLI". So:

- **Do the checking yourself.** Run the check commands silently. Never ask "do you have Node
  installed?"; find out. Only bring the person the things that actually need them.
- **One missing thing at a time**, in the order of the table in section 2. Never dump the whole
  list on them.
- **Explain each thing in one plain sentence first**: what it is and why this skill needs it.
  No jargon without a translation ("the Shopify CLI, a small free tool from Shopify that lets me
  copy your theme to this computer and send changes back to a draft").
- **Numbered steps, one action per step**, naming exactly what to click or type. Give commands
  in their own copy-able block. Say what they should see when it worked.
- **Then say "Tell me when that's done"** and re-run the check yourself. Don't take "done" on
  trust; if the check still fails, read the error and give the next step in plain words.
- **Never type a password, verification code or other credential** for the person, and never
  ask them to paste one into the chat. When a step needs their password (a computer password, a
  Shopify sign-in), they type it themselves, in the window that asks for it.
- **Ask before installing anything on their computer.** If you can run commands, offer to run
  an install command for them ("I can run this for you, OK?"). Anything that asks for their
  computer password they run themselves in the Terminal (section 4).
- **Keep it calm and short.** When everything passes, say one line ("Setup check: everything
  this skill needs is ready.") and move on. Don't list what passed.

Once a check has passed in this conversation, don't run it again. In a new conversation re-run
the checks; they take seconds and stay silent when everything is fine.

## 1. If you can't run commands

Some places Claude runs (a plain chat, a Claude project with no computer access) can't run
commands or reach the person's computer. There, say plainly that this skill needs the Claude
desktop app (Claude Code or Cowork, with access to a folder on their computer), because it has to
reach the theme (with a tool on their computer, or through the Shopify connection), keep a record
of the change and backups of the files it changes, and preview the page. `page-audit` is the
exception: it can still run from a browser alone, without the theme tools, and says which checks
it couldn't do.

## 2. What each skill needs

Check only the rows the current skill needs, in this order. **Required** blocks the skill until
it is fixed. **Recommended** lets it run with less, and you say what will be missing.

| # | Item | page-audit | page-create, page-edit-content, page-edit-design | theme-audit |
|---|---|---|---|---|
| A | A browser Claude can use to look at the page | Required | Required (to check each change) | Required (to check each fix) |
| B | The page's address, and the storefront password if the store has one | Required | Required | Required |
| C | Brand files (`BRAND.md`, `BRAND-VOICE.md`, `design.md`) | Recommended | Required for new or rewritten words; `design.md` recommended for design changes | Not needed |
| D | Node.js | Not needed | Required on the CLI route (below) | Required |
| E | Shopify CLI | Recommended (lets it read theme files) | Required on the CLI route | Required |
| F | Shopify CLI signed in to the right store, with theme access | Recommended | Required on the CLI route | Required |
| G | Google Chrome | Not needed | Not needed | Required |
| H | Lighthouse | Not needed | Not needed | Required |
| I | A folder on this computer (the theme copy on the CLI route; on the connector route only the change record and backups of the files changed) | Not needed | Required | Required |
| J | A draft theme | Not needed | Required (settled next, by `theme-target.md`) | Required (settled next, by `theme-target.md`) |
| K | The Shopify connector, with theme read and write access to the right store (detected read-only) | Recommended instead of E and F (read access is enough) | Required on the connector route | Not applicable (theme-audit needs the CLI) |

**Two routes to the theme** (`page-create`, `page-edit-content`, `page-edit-design`). One must be
ready: the **CLI route** (rows D, E and F: the Shopify CLI signed in) or the **connector route**
(row K: the Shopify connector). They do the same job with the same safety rules; the connector
route is in `connector-route.md` (page-studio) and has no CLI, no local theme copy and no
`theme check`. Choose the route like this, silently:

1. Check rows D, E and F. If all pass, use the **CLI route**, exactly as before. Don't check row K.
   The CLI route can check a change before anything is sent and runs `theme check`, so it wins
   when both are ready.
2. If they don't, check row K. If it passes, use the **connector route** and say one line:
   "I can work on your theme through your Shopify connection, so there is nothing to install."
   The plan step then says what is different (`connector-route.md` section 5).
3. If neither is ready, say which and why in plain words, then guide the CLI setup (rows D, E, F)
   one step at a time, as before. Row K says what to say when the connector is the reason.
4. If the route chosen in step 2 fails at its first write because Shopify refuses it, nothing
   was changed: go to step 3.

`page-audit` and `theme-audit` do not choose a route: `page-audit` reads theme files with either
tool when one is ready, and `theme-audit` always uses the CLI.

The `page-studio` front door runs the rows for the skill it is about to hand to, then tells that
skill the check already passed (and which route was chosen), so it isn't repeated.

## 3. The checks, and how to guide each one

### A. A browser Claude can use

**Check:** a browser tool is available (Claude in Chrome, or the browser built into the Claude
app) and can open a page.

**If missing**, explain: "To check the page the way your visitors see it, I need a browser I can
look through." Then guide:
1. Easiest: use the **Claude desktop app**, which has a browser built in; nothing to install.
2. Or use **Claude in Chrome**: install the **Claude in Chrome** extension from the Chrome Web
   Store, sign in to it with the same Claude account, and turn it on in the Claude app's
   settings (under connectors or browser). Keep Chrome open while the skill runs.

Never sign in to anything in that browser for them.

### B. The page's address and the storefront password

**Check:** you know which page (a full address such as `https://example.com/pages/about`, or a
page name you can resolve from the store), and the page loads.

- If the person named the page in words ("the about page"), find the address yourself first.
- If the store shows a **password page** ("Opening soon", "Enter store using password"):
  explain that the shop is password protected, so you can't see the pages until it's unlocked
  in the browser. Ask them to type the store password into that page themselves, in the browser
  Claude is using, and tell you when the page shows. Never ask for the password in chat. The
  password is in the Shopify admin under **Online Store > Preferences > Password protection**
  if they don't know it.

### C. Brand files

**Check:** look for `BRAND.md`, `BRAND-VOICE.md` and `design.md` with the lookup in
`../page-audit/references/intake.md` section 1 (or, for `theme-audit`, skip this row).

**If missing**, explain: "Your brand files tell me how the brand sounds, what it can and can't
claim, and its colours and fonts, so I never guess." Offer to run **brand-capture** first (about
10 to 25 minutes, once per store). If brand-capture isn't installed: in the Claude app open
**Customize > Plugins**, find **brand-capture** under the Brand AI marketplace and click
**Install**, then start a new task. What can go ahead without them is in
`../page-audit/references/intake.md` section 1 (structure-only changes, audits).

### D. Node.js

Rows D, E and F are the CLI route (`theme-audit` always needs them).

**Check:** `node --version` prints `v20` or higher.

**If missing or older**, explain: "Node.js is a free program that the Shopify and Lighthouse
tools run on. You install it once, like any other app."
1. Go to **https://nodejs.org** and download the version marked **LTS** (the recommended one).
2. Open the downloaded file and click through the installer, keeping the default options. On a
   Mac it may ask for your computer password; type it yourself.
3. When it finishes, **quit and reopen the Claude app** so it can see the new program.

Then re-check. If the check still fails after reopening, restart the computer and check again.

### E. Shopify CLI

**Check:** `shopify version` prints a version number.

**If missing**, explain: "The Shopify CLI is a free tool from Shopify. It lets me copy your theme
to this computer, preview changes privately, and send them to a draft theme that visitors can't
see." Needs Node.js first (row D). Then offer to run the install for them:

```
npm install -g @shopify/cli@latest
```

- If it fails with `EACCES` or "permission denied" (common on a Mac), the person runs it
  themselves in the Terminal with `sudo` in front (section 4), and types their computer
  password when asked. Nothing shows on screen while they type the password; that's normal.
- On a Mac that already has Homebrew (`brew --version` works), `brew install shopify-cli` is an
  alternative.

Then re-check with `shopify version`.

### F. Signed in to the right store, with theme access

**Check:** `shopify theme list --store <store>.myshopify.com` lists the store's themes.

Find the store's `.myshopify.com` address yourself first (from the brand files, `THEME-TARGET.md`
or the repo's theme config). If you can't, ask the person: "In your Shopify admin, open
**Settings > Domains**; the address ending in `.myshopify.com` is the one I need."

**If it isn't signed in**, the command prints a link and a code and may open the browser.
Explain: "Shopify needs you to confirm it's OK for this computer to work on your store." Then:
1. A Shopify page opens in the browser (if not, open the link shown).
2. Check the code on the page matches the code I show you.
3. Sign in with your own Shopify login and click **Confirm** or **Log in**.
4. Come back here and tell me it's done.

**If it says you don't have access**, explain that their Shopify account needs permission to
manage themes. The store owner can give it: in the Shopify admin, **Settings > Users and
permissions**, open the person's account and turn on **Themes** (under Online Store). Agencies
and freelancers may need a collaborator request instead. Then sign in again.

**If it lists the wrong store's themes**, run `shopify auth logout` and sign in again with the
right account.

### G. Google Chrome

**Check:** Chrome is installed (on a Mac, `/Applications/Google Chrome.app` exists; on Windows,
`chrome.exe` is under Program Files). Lighthouse uses Chrome to score the page.

**If missing**, explain that Lighthouse, Google's page-checking tool, runs inside Chrome. Guide
them to download it from **https://www.google.com/chrome**, open the file and install it like any
app. They don't need to make it their default browser.

### H. Lighthouse

**Check:** `npx --yes lighthouse --version` prints a version number. The first run downloads it
by itself (a minute or so), so there's nothing for the person to install; it just needs Node.js
(row D) and an internet connection.

**If it fails**, read the error: "No Chrome installations found" means row G; "command not found:
npx" means row D. Anything else, explain it in plain words and offer to try again.

### I. A folder on this computer for the theme copy

**Check:** you have a working folder you can write to: the project's folder, or the draft theme's
folder where the brand files live (`BRAND-HOME.md` or `THEME-TARGET.md` names it).

**If not**, explain: "I'll keep a private copy of your theme in a folder on your computer. I make
the changes there, check them, and only then send them to the draft." Ask them to pick or create
a folder (for example `Documents/<store name> theme`) and, in Cowork, to connect it to this task.
The skill pulls the theme into it; they don't need to download anything.

On the connector route, say instead: "I'll keep a short record of the change, and a backup of each
file before I change it, in a folder on your computer, so I can undo exactly what I did."

### J. A draft theme

Not checked here. Say in one line that the next step is choosing the draft theme the work will
go to, then follow `theme-target.md`. If the person has never made one, explain once: "A draft
theme is a private copy of your website's design. I make changes there; visitors keep seeing your
current site until you choose to publish."

### K. The Shopify connector, with theme read and write access (connector route)

`page-studio` only. `theme-audit` skips this row.

**Check**, silently, read-only (the exact queries are in `connector-route.md` section 1): the
Shopify connector is connected, it is the **same store** as the page, it can read the themes and
their roles, and the access it was granted (`currentAppInstallation { accessScopes { handle } }`)
includes both `read_themes` and `write_themes`. Never test it with a trial write, never ask for or
type a token, and never switch the connector's store silently.

Having the scope is not the whole answer: Shopify also has to have approved the connection to
change themes, and that can't be read. The first real write finds out. If Shopify refuses it,
nothing has changed; treat it as "can look, can't change" below.

**If the connector is not connected,** use the CLI route and guide rows D, E and F as before. If
the person says they would rather not install anything, offer the connection instead:
1. In the Claude app, open **Customize** (or **Settings**), then **Connectors**.
2. Find **Shopify** and click **Connect**.
3. A Shopify page opens: sign in with **your own** Shopify login and choose the right store.
4. Approve the access it asks for, then come back and tell me.

Say once, in plain words: "Shopify only lets a connection change themes when it has approved that
connection. I can only find out after it is connected. If it isn't approved, I'll set up the other
tool with you." Then re-check.

**If it is connected to another store,** say so, and ask them to switch the connector to this
store (the same steps) or use the CLI route. Never write to the wrong store.

**If it can look but not change** (no `write_themes`, or Shopify refused the first write), explain:
"Your Shopify connection can read your themes but isn't allowed to change them. Shopify has to
approve a connection before it can, and I can't switch that on. I'll set up a different tool on
this computer instead." Then guide rows D, E and F. Anyone who manages the connection for them can
ask Shopify for that approval; offer this as a side note, never as the next step.

**If the connection drops partway,** stop, say what was and wasn't changed (`connector-route.md`
section 7), and ask them to reconnect it themselves.

## 4. Opening the Terminal (only when the person must run a command themselves)

Explain once: "The Terminal is a window where you type commands. You'll paste one line, press
Return, and I'll take it from there."

- **Mac:** press **Command + Space**, type **Terminal**, press **Return**.
- **Windows:** click **Start**, type **PowerShell**, click **Windows PowerShell**.

Then: paste the command (Command + V on a Mac, Ctrl + V on Windows), press **Return**, and wait
for it to finish (the cursor comes back). If it asks for a password, type your computer password
(nothing appears on screen while typing; that's normal) and press **Return**. Ask them to copy
anything red or anything that says "error" back into the chat.

## 5. Hand-off

When every required row passes (for the three editing skills: the rows of the one route chosen,
section 2), say one line, then go to the skill's step 1. If a required row
can't be fixed now ("I'll ask IT tomorrow"), stop politely: say what's left, that nothing was
changed, and that the next run will pick up where this left off. For a recommended row that's
still missing, say in one line what the skill will do without it and continue.
