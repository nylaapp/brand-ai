# Best practices and SEO lanes

Both are measured on the local dev server, with the accessibility runs (`SKILL.md` step 3a), and
read from `failing["best-practices"]` and `failing.seo` in the summary. Target: every finding the
theme owns is fixed; the rest are named with their owner. Same fix rules as accessibility:
additive or a guard, no change a visitor can see.

## Best practices

| Finding | Usual owner | What to do |
|---|---|---|
| `errors-in-console` | theme if the error's source is a theme asset (`/assets/` of this theme); otherwise the app or Shopify | theme: find the cause (often a script reading an element that isn't on this page) and guard it, for example `if (!el) return;`. Others: report the message and source. |
| `inspector-issues` | depends on the issue | read the issue type; cookie and third-party issues are not the theme's |
| `deprecations` | the file in the item's `source` | theme: replace the deprecated call only when the replacement behaves the same; otherwise report |
| `image-aspect-ratio` | theme | the shown aspect ratio differs from the image's own: report it; fixing it changes how the image looks, so ask |
| `image-size-responsive` | theme | same fix as `uses-responsive-images` in `performance.md` section 3 |
| `is-on-https`, `redirects-http` | store settings or a hard-coded `http://` link | theme: change the link to `https://` (same address); store: report |
| `third-party-cookies`, `geolocation-on-start`, `notification-on-start` | an app or outside script | report with the source |
| `csp-xss`, `has-hsts`, `origin-isolation`, `clickjacking-mitigation` | Shopify (response headers) | skip with evidence; the theme can't set these |
| `valid-source-maps` | whoever ships the file | report only |
| `doctype`, `charset` | theme layout | fix in `layout/theme.liquid` if missing (very rare) |

## SEO (the quick Lighthouse check)

Lighthouse's SEO check covers basics only. For a deeper SEO review of a blog post (structured data,
search rankings), point the person to the **seo-audit** skill; for content gaps on a page, to
**page-studio's page-audit**.

Preview and dev addresses are often marked "don't index", so judge `is-crawlable` only on the
live page (read it once, read-only). A "don't index" mark on the live page is serious and goes to
the top of the report.

| Finding | Usual owner | What to do |
|---|---|---|
| `meta-description` | store content (each page's search listing) | report the pages without one; the person fills them in the store admin (each page's **Search engine listing**). The theme fix, only when the theme drops a description that exists: output `page_description` in the layout's head. |
| `document-title` | theme layout | output `page_title` (with the shop name) in `<title>`; never invent a title |
| `link-text` (links like "click here", "learn more") | theme if the words are fixed in a theme file or locale; store content if typed in a section setting | theme: add a visually-hidden span that says where the link goes (no visible change). Content: report. Changing the visible words is copy work for **page-edit-content**. |
| `crawlable-anchors` | theme | links without a real address (`href="#"`, `javascript:`) used as buttons: make them `<button>` only when the styling stays identical; otherwise report |
| `hreflang`, `canonical` | theme layout or Shopify markets | theme: output `canonical_url`; language links come from Shopify Markets, report if wrong |
| `image-alt` | see `accessibility.md` | |
| `robots-txt` | store (`templates/robots.txt.liquid` if present) | report; edit only on the person's yes |
| `http-status-code` | the address | wrong page or unpublished page: back to step 1 |
