# Media transfer: from the source article to the store's own CDN

Read at "Source images" in SKILL.md, after ownership or written permission is confirmed (Source from a URL, item 1). Without
that confirmation no image is copied. With it, the images of a source article are extracted, checked, uploaded to the
store's Shopify Files (the Shopify CDN) and placed in the new post: inside the body, in the store's own layout, and as the
article's blog image.

## 1. Extract

```bash
python3 scripts/extract_media.py --url <article-url> --out <run folder>/media.json --download <run folder>/media
# page already saved (browser tool, script-rendered page):
python3 scripts/extract_media.py --html <saved.html> --base <article-url> --out <run folder>/media.json --download <run folder>/media
```

It lists every image in the article body and the page's `og:image`, at the largest size the page offers (the `srcset`
or the original without the `-300x200` suffix), with alt text, caption, the heading and paragraph it follows, and a
verdict: `keep`, `flag` (too small under 400 px, or over 20 MB), `skip` (logo, icon, avatar, tracking pixel, navigation,
sidebar, duplicate) or `failed`. Each kept image is downloaded, checked by its first bytes (a page that returns HTML
instead of a picture is a failure) and measured for its real width and height. Videos and embeds (YouTube, Vimeo,
players) are listed under `videos_and_embeds`: they are not downloaded or uploaded. Say so in the report and leave a
`[[USER MEDIA: video "<title>", source <url>]]` slot.

If the page is script-rendered and the script finds nothing (`0 image(s)` on an article that clearly has pictures), open the
page in a browser tool, save the rendered HTML, and run it again with `--html`.

## 2. Look at every image, then decide

Open each downloaded file with the image viewer (the Read tool shows images). The script cannot see inside a picture.

| What you see | Do |
|---|---|
| A normal photo or graphic for the topic, no marks | Use it |
| The source brand's logo, name, phone, address or URL in the picture | `flag`: needs a replacement, not used |
| Before and after photos, result claims, price or offer text | `flag`: a claim, not an image; the brand's claim limits apply; not used unless the approver confirms |
| A recognisable person (patient, client, model) | Use only if the person confirms a photo release exists; otherwise `flag` |
| Watermark or a stock agency credit | `flag`, list it |
| Text overlay that contradicts the rewrite (a different brand, a different claim) | `flag` |
| Too small (under 400 px wide) for a lead image | Inline only, if the person accepts it; never as the blog image |

Never crop, blur or edit an image to hide a mark. A flagged image is listed in the report with the reason and left out.
The person can supply a replacement.

## 3. Upload to the Shopify CDN

Use the Shopify connector (Admin GraphQL) or whatever transport the project defines. **Staged upload is the default**: it
accepts any file extension and does not depend on the source site allowing Shopify to fetch it. Validate each operation
before running it (`validate_graphql_codeblocks` on the connector).

1. **Ask for an upload target** for each kept image:

```graphql
mutation($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
```
```json
{"input": [{"resource": "IMAGE", "filename": "<handle>-1-<what-it-shows>.jpg", "mimeType": "image/jpeg", "httpMethod": "POST"}]}
```

2. **Send the file** to the target. Save one `stagedTargets` object as `target.json`, then:

```bash
python3 scripts/upload_staged.py --target target.json --file <run folder>/media/<file>
```
It prints the `resourceUrl`. The target is single-use and signed; do not keep or share it.

3. **Create the file record** with that `resourceUrl`, the alt text and a stable filename:

```graphql
mutation($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files { id fileStatus alt ... on MediaImage { image { url width height } } }
    userErrors { field message code }
  }
}
```
```json
{"files": [{"originalSource": "<resourceUrl>", "contentType": "IMAGE", "filename": "<handle>-1-<what-it-shows>.jpg",
            "alt": "<alt text>", "duplicateResolutionMode": "APPEND_UUID"}]}
```

4. **Wait for `READY`.** Processing is asynchronous: poll
`node(id: "<file id>") { ... on MediaImage { fileStatus image { url width height } } }` until `fileStatus` is `READY` and
`image.url` is set (a few tries, a few seconds apart). That `image.url` is the CDN address to use. A file still processing
after several tries, or `FAILED`, becomes a `[[USER MEDIA: ...]]` slot and a line in the report; carry on with the text.

Simpler path, when the image URL ends in its true extension and the host allows fetching: `fileCreate` with the source URL
as `originalSource` (publishing.md, "Step B"). If it errors on the extension or the fetch, switch to staged upload.

**Filenames:** `<post-handle>-<n>-<what-it-shows>.<ext>` (lowercase, hyphens, ASCII): stable, descriptive, scoped to the
article so a later edit never collides. **Alt text:** a plain description of what the picture shows, 125 characters or
fewer, in the brand's words; keep the source's alt when it describes the image, rewrite it when it names the source
brand or stuffs keywords; empty `alt=""` only for a purely decorative image. Never invent a caption: add `<figcaption>`
only when the source had one worth keeping, reworded like any other text.

**Series:** keep `uploaded-media.json` in the transfer folder (sha256, Shopify file id, CDN url). An image that already
appears in an earlier article of the series is reused, not uploaded again. A resumed run reads each article's `media.json`
and skips images that already have a Shopify file id.

## 4. Place the images in the post, in the store's own layout

**Copy the store's pattern, do not invent one.** Read the newest published article (connector:
`articles(first: 3, sortKey: PUBLISHED_AT, reverse: true) { nodes { body image { url altText width height } templateSuffix } }`,
or the live page) and note three things: how an in-body image is marked up (for example `<figure><img src alt width height
loading="lazy"></figure>`, with or without `<figcaption>`, any wrapper class); whether the first image sits in the body, in
the article's image field, or both; and its size and position on the page. Write that pattern into the fields JSON as
`image_pattern`. If the project has its own rule for multi-image posts or galleries (a special-layout check), it wins:
follow it, and ask before placing more than one image.

- **In the body:** each kept image becomes the store's figure markup with the CDN `src`, the alt text, the real `width` and
  `height` from the file (stops layout shift), and `loading="lazy"`. No inline styles, scripts or tracking.
- **Position:** keep each image beside the content it illustrated. At Match and Reword, put it after the same section
  heading and paragraph (`after_heading`, `after_paragraph`). At Restructure and Reimagine the outline changes: place it
  next to the new section about the same subject, using its alt text and caption to match. Never gather every image at the end.
- **The blog image (article image):** set the article's `image` field (`{"url": "<CDN url>", "altText": "<alt>"}`) when the
  store's posts use one: that file feeds blog-listing cards and social previews. Use the lead image, or the source's
  `og:image` if the lead is too small. If the store's pattern puts the lead image in the body and the image field, use the
  same file in both; if its posts keep the image only in the field, do **not** repeat it in the body.
- **No usable image:** leave `image` empty, put the reason in the report ("Missing input you could add") and, in a series,
  in the tracker's `images_flagged` count. Do not substitute stock.

## 5. Record

Update `<run folder>/media.json` for each image with `shopify_file_id`, `cdn_url`, `alt_final`, `placement`
(`body`, `blog image` or `both`) and the verdict. Report, per article: images used, flagged (with reason), placed where,
and the blog image. In a series, set `images_used` and `images_flagged` on the tracker row and show them in the batch table.
Rights stay the person's call: the report says "images copied from <source> with the ownership or permission confirmed by
<who> on <date>".
