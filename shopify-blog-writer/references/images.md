# Images: finding, sizing and crediting free photos

Plan 3–5 images per post: **1 featured image** (1200×630, for the blog index and social shares) and **2–4 in-body images**, each illustrating a specific section (a step, a comparison, a detail). An image placed "because posts have images" adds weight without value.

## 0. Which path? (the user's media choice)

| Choice | What to do |
|---|---|
| **Pick free stock photos for me** | Sections 1–5 below |
| **I'll upload my own** | Skip the stock search. Use any files or URLs the user attached. For every other slot, leave a marked placeholder in the HTML, `<img src="[[USER MEDIA: file-name.webp]]" alt="…" width="1200" height="800">`, and add a **shot list** to the fields sheet: for each slot, what the image should show, the section it belongs to, suggested file name, draft alt text, and size (featured 1200×630; in-body 1200 wide). Alt text must describe the intended image. The user replaces the placeholder after uploading |
| **Both** | Use what the user provided; fill the remaining slots from stock (sections 1–5) |

**AI-generated images are not part of the default flow.** Newer rules in many places require AI-generated images to be labeled, which can be off-brand, especially for medical or scientific brands, and curated stock avoids the issue. If the user asks for them, explain this and treat it as an optional extra they configure themselves, not something this skill sets up.

If the brand's existing posts set the featured image in the article's image field (see `house-style.md`), put the featured image there and don't repeat it inline.

## 1. Search Unsplash first

Build 2–3 concrete queries per image from the section's subject — objects, actions, settings — not abstract concepts ("folded linen sheets on bed", not "comfort").

Ways to search, in order of reliability:

1. **Web search**: `site:unsplash.com/photos <query>` — returns photo pages directly.
2. **Unsplash search page**: fetch `https://unsplash.com/s/photos/<query-with-hyphens>`. It's partly JS-rendered; if the fetch returns no photos, use a browser tool if available, or option 1.
3. **Unsplash's JSON endpoint** (used by its own site; may change): `https://unsplash.com/napi/search/photos?query=<query>&per_page=20` returns `results[]` with `id`, `slug`, `alt_description`, `description`, `urls.raw`, `user.name`, `user.username`, `links.html`, `premium`.

**Skip premium images.** Unsplash+ photos (host `plus.unsplash.com`, or `premium: true`) are not free.

If Unsplash has nothing suitable, try **Pexels** (`site:pexels.com/photo <query>`) then **Pixabay** (`site:pixabay.com/photos <query>`). Both are free for commercial use under their own licenses.

Pick images that: show the actual subject, look like the brand (lighting, palette, lifestyle vs. studio), don't show competitor logos or recognizable branded products, and don't feature people's faces in ways that imply endorsement.

## 2. Build a sized WebP URL

Unsplash images are served through imgix, which resizes and converts on the fly. Take the `images.unsplash.com/photo-…` base URL (strip its existing query string) and append:

| Use | Parameters |
|---|---|
| Featured / social | `?w=1200&h=630&fit=crop&crop=entropy&fm=webp&q=75` |
| In-body, full width | `?w=1200&fit=max&fm=webp&q=75` |
| In-body, half width | `?w=800&fit=max&fm=webp&q=75` |

At these settings most photos land well under 150 KB. If you can download and measure (e.g. `curl -sI` for Content-Length, when allowed), report the size; otherwise say "should be <150 KB — verify after download".

Pexels URLs accept `?auto=compress&cs=tinysrgb&w=1200&h=630&fit=crop`; convert to WebP before upload (Squoosh, or Shopify's CDN will serve WebP automatically to supporting browsers from uploaded JPG/PNG).

## 3. Name, alt text and caption

- **File name**: descriptive kebab-case + `.webp` — what's in the picture plus the topic: `washing-linen-sheets-cold-cycle.webp`. The user should rename the file before uploading to Shopify (Content → Files, or the image picker), because Shopify keeps the upload file name in the CDN URL.
- **Alt text**: describe what's visible in ≤ 125 characters, as you would to someone who can't see it. Use the keyword only where it describes the image naturally. Don't start with "Image of".
- **Credit**: Unsplash's license doesn't require attribution, but it's appreciated and good practice: `Photo by <Name> on Unsplash` linking to the photo page. Put credits in a small caption or a "Photo credits" line at the end of the post.

## 4. Record for delivery

For each image, list in the fields sheet:

| Field | Example |
|---|---|
| Role | Featured / in-body after H2 "How to dry linen" |
| Source page | `https://unsplash.com/photos/…` |
| Photographer | Photographer Name (`@handle`) |
| Download URL | `https://images.unsplash.com/photo-…?w=1200&h=630&fit=crop&fm=webp&q=75` |
| File name | `linen-sheets-drying-on-line.webp` |
| Alt text | Cream linen sheets drying on a washing line in a sunny garden |
| License | Unsplash License (free, commercial use OK) |

In the HTML, reference images by their intended file name with a placeholder CDN path the user replaces after upload, e.g. `src="[[UPLOAD: linen-sheets-drying-on-line.webp]]"`, *or* use the sized Unsplash URL directly if the user prefers hotlinking for a draft. Always include `width`, `height`, `alt` and `loading="lazy"` (except the first image) to protect Core Web Vitals.

## 5. Flag original-photo opportunities

Stock can't show the brand's own product, process or team. Note 1–2 spots where an original photo would be stronger (product in use, testing setup, workshop, before/after) — original imagery is an E-E-A-T signal.
