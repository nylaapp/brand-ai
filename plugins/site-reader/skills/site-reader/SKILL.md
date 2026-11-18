---
name: site-reader
description: "Read a web page's text, structure and visual layout quickly and with few tokens, without opening the browser pane or an extension. One command returns a short summary: what the page says (title, headings, copy, links, structured data), how it is laid out at desktop and mobile (sections top to bottom with height, what the first screen shows, calls to action, popups in the way, fonts and colours as measured, small tap targets, broken images, sideways overflow) and, for Shopify, which theme id the page reports. Pictures are saved only when asked. Read-only. Use whenever a skill or person needs to look at a live page, a draft theme preview or a competitor page: \"what does this page look like\", \"check the homepage\", \"read this page\", \"compare desktop and mobile\", \"which theme is this\", \"what is in the first screen\", \"is there a popup\". Not for logged-in pages, clicking through flows, or speed scores (use theme-audit)."
---

# Site reader

Look at a page without driving a browser. One command, a short answer, the same method every time.

## How to reply (every message)

Short and direct. Start with the answer. Plain words, no technical terms without a few words of explanation.
Say what you could not read ("Can't tell") instead of guessing.

## Run it

The script is `scripts/site_read.py` (Python 3, standard library only). It uses the Chrome or Chromium already on
the machine, headless, in a fresh private profile. Nothing is installed and nothing is clicked.

```bash
python <skill>/scripts/site_read.py https://example.com/ --out site-read/home
```

It prints a summary of about 1,000 to 1,500 tokens for both devices and saves the full detail
(`report.json`) and a wireframe picture per device to `--out`. Read the summary first. Open the saved
detail or the pictures only when the summary does not answer the question.

| Need | Option |
|---|---|
| Text and structure only, fastest, no Chrome | `--layers fetch` |
| Layout and first screen at desktop and mobile (default) | none |
| A small picture of the first screen per device | `--shots` |
| A shrunk full-page picture per device | `--full` |
| Catch popups that appear late | `--late 15` |
| Prove it is the theme you were asked about (Shopify) | `--expect-theme-id <id>` |
| Everything as JSON | `--json` |

## Rules

- **Desktop and mobile, always.** Any claim about how a page looks needs both devices. If only one was read,
  say so and mark the other "Can't tell". Don't read one device with `--devices` unless the question is not visual.
- **Read the summary before looking at pictures.** A picture costs more than the text and is usually not needed.
  Use `--shots` when something looks wrong in the numbers or the person wants to see it.
- **Say which layer a fact came from.** Text facts come from the HTTP read; positions, heights, fonts, colours,
  popups and tap targets come from the Chrome read. Copy the page's own words when you quote it.
- **"Can't tell", never a guess.** If Chrome is not found, the layout layer is skipped and the summary says
  so: set `CHROME_PATH`, or report the text read only. If the page is locked (a password page), it is reported as
  blocked: never type a password; ask the person to lift it or use a theme preview, and read the theme files.
- **Confirm which page you read.** Compare the final address and, on Shopify, the theme id with what you were
  asked to look at (`--expect-theme-id`). A preview link can redirect to the live theme.
- **Needs a browser?** If the summary says the page renders only in a browser, the layout layer already ran with
  a real render; if the layout is empty too, say the page is blocked or app-like, and ask.
- **Public pages, read-only.** It loads and scrolls. It does not log in, click, type or submit. A page that needs
  a login is not readable this way.
- **On a Mac with a Python SSL error**, set `SSL_CERT_FILE=/etc/ssl/cert.pem` (the script already tries it).

## Reading the summary

- `wireframe` lines: `top-bottom  kind:id  “heading or first words”  [media]  CTA: ...`. A dashed line marks where the
  first screen ends. Check that the offer, the main action and a picture sit above it, at both widths.
- `in the way`: fixed or sticky things that cover part of the first screen (cookie banners, country pickers,
  sign-up popups, chat). `covers n%` is how much of the screen.
- `tap targets under 44px`: links and buttons smaller than a finger, per device. High on mobile is a finding.
- `sideways overflow`: pixels of the page wider than the screen. Anything above 0 is a layout bug.
- `page errors` and `failed requests`: counts only; use the browser console if they matter.

## When this is not enough

| Need | Use |
|---|---|
| Speed, accessibility scores | `theme-audit` |
| Click through a flow, a logged-in page, a form | A browser tool, with the person's permission |
| Theme files and settings | The Shopify CLI or connector |
| Analytics and tags | `analytics-audit` |
