#!/usr/bin/env python3
"""QA checker for a Shopify blog post body HTML + fields JSON.

Usage:
    python check_post.py post.html --fields post-fields.json [--json]

Prints PASS / WARN / FAIL per check. Exit code 1 if any FAIL.
Stdlib only.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser

STOPWORDS = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "for", "our",
             "your", "you", "with", "is", "are", "that", "this", "at", "by", "we"}
BAD_ANCHORS = {"click here", "here", "read more", "learn more", "this", "link",
               "this post", "this article", "more"}
GENERIC_IMG = re.compile(r"^(img|dsc|dscn|image|photo|pic|screenshot|untitled|pxl)[-_ ]?\d*", re.I)


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []        # (tag, text, attrs) for p/h1-h6/li/td/th
        self.links = []         # (href, anchor_text)
        self.images = []        # attrs dict
        self.tags = {}
        self._stack = []        # open block-level capture
        self._link = None
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.tags[tag] = self.tags.get(tag, 0) + 1
        if tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "td", "th"):
            self._stack.append([tag, [], a])
        elif tag == "a":
            self._link = [a.get("href", ""), []]
        elif tag == "img":
            self.images.append(a)

    def handle_endtag(self, tag):
        if tag == "a" and self._link is not None:
            self.links.append((self._link[0], " ".join("".join(self._link[1]).split())))
            self._link = None
        if self._stack and self._stack[-1][0] == tag:
            t, parts, a = self._stack.pop()
            text = " ".join("".join(parts).split())
            self.blocks.append((t, text, a))
            if self._stack:  # nested (e.g. p inside li): propagate text upward
                self._stack[-1][1].append(" " + text + " ")

    def handle_data(self, data):
        self.text_parts.append(data)
        if self._stack:
            self._stack[-1][1].append(data)
        if self._link is not None:
            self._link[1].append(data)


def words(s):
    return re.findall(r"[A-Za-z0-9À-ɏ']+", s)


def contains_kw(text, kw):
    t, k = text.lower(), kw.lower().strip()
    if not k:
        return "none"
    if k in t:
        return "exact"
    toks = [w for w in words(k) if w not in STOPWORDS]
    if toks and all(w in t for w in toks):
        return "partial"
    return "none"


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, name, detail=""):
        self.rows.append({"status": status, "check": name, "detail": detail})

    def rng(self, name, value, ok, warn, unit=""):
        lo, hi = ok
        wlo, whi = warn
        if lo <= value <= hi:
            s = "PASS"
        elif wlo <= value <= whi:
            s = "WARN"
        else:
            s = "FAIL"
        self.add(s, name, f"{value}{unit} (target {lo}–{hi})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("html")
    ap.add_argument("--fields", help="fields JSON path")
    ap.add_argument("--json", action="store_true", help="output JSON")
    args = ap.parse_args()

    html = open(args.html, encoding="utf-8").read()
    fields = json.load(open(args.fields, encoding="utf-8")) if args.fields else {}
    p = Parser()
    p.feed(html)
    r = Report()

    body_text = " ".join(" ".join(p.text_parts).split())
    wc = len(words(body_text))
    brand = fields.get("brand", "")
    kw = fields.get("primary_keyword", "")
    intent = fields.get("intent", "search")
    if intent not in ("education", "brand", "search", "promotion"):
        intent = "search"
    lt = fields.get("length_target")
    r.add("INFO", "Post intent", f"{intent}; house style: {fields.get('house_style', 'not set')}")

    # Intent-aware targets. Search and education follow the full SEO standard;
    # brand journals and promotions relax the parts that only serve ranking.
    wc_ok, wc_warn = {"search": ((1200, 2500), (900, 3200)), "education": ((1200, 2500), (900, 3200)),
                      "brand": ((600, 1500), (400, 2000)), "promotion": ((800, 2000), (500, 2800))}[intent]
    if isinstance(lt, (list, tuple)) and len(lt) == 2:
        wc_ok = (int(lt[0]), int(lt[1]))
        wc_warn = (int(lt[0] * 0.8), int(lt[1] * 1.2))
    h2_ok, h2_warn = ((2, 10), (1, 14)) if intent == "brand" else ((4, 12), (3, 16))
    prod_ok, prod_warn = {"promotion": ((2, 5), (1, 7)), "brand": ((1, 3), (0, 5))}.get(intent, ((2, 4), (1, 6)))
    blog_ok, blog_warn = ((1, 3), (0, 5)) if intent == "brand" else ((2, 3), (1, 5))
    ext_ok, ext_warn = ((0, 8), (0, 12)) if intent in ("brand", "promotion") else ((3, 8), (2, 12))
    kw_miss = "WARN" if intent == "brand" else "FAIL"

    # ---------- Structure ----------
    h1 = p.tags.get("h1", 0)
    r.add("PASS" if h1 == 0 else "FAIL", "No H1 in body (title is the H1)", f"{h1} <h1> found")

    headings = [(t, x) for t, x, _ in p.blocks if re.fullmatch(r"h[1-6]", t)]
    first_h2 = next((i for i, (t, _) in enumerate(headings) if t == "h2"), None)
    first_h3 = next((i for i, (t, _) in enumerate(headings) if t == "h3"), None)
    bad_order = first_h3 is not None and (first_h2 is None or first_h3 < first_h2)
    r.add("WARN" if bad_order else "PASS", "Heading hierarchy (H2 before H3)")
    h2s = [x for t, x in headings if t == "h2"]
    r.rng("Number of H2 sections", len(h2s), h2_ok, h2_warn)

    r.rng("Word count" + (" (length target)" if lt else ""), wc, wc_ok, wc_warn)

    paras = [(x, a) for t, x, a in p.blocks if t == "p" and x]
    content_paras = [x for x, a in paras
                     if "last updated" not in x.lower()
                     and "post-meta" not in (a.get("class") or "")]
    if content_paras:
        af = len(words(content_paras[0]))
        if intent in ("search", "education"):
            r.rng("Answer-first paragraph length", af, (40, 60), (30, 75), " words")
        else:
            r.add("INFO", "Opening paragraph length (answer-first not required for this intent)", f"{af} words")
    else:
        r.add("FAIL", "Answer-first paragraph", "no paragraphs found")

    long_paras = [x[:60] for x in content_paras if len(words(x)) > 100]
    r.add("PASS" if not long_paras else "WARN", "Paragraphs ≤100 words",
          f"{len(long_paras)} long: {long_paras[:3]}" if long_paras else "")

    has_table = p.tags.get("table", 0) > 0
    has_list = p.tags.get("ul", 0) + p.tags.get("ol", 0) > 0
    r.add("PASS" if has_list else "WARN", "Uses lists", f"{p.tags.get('ul',0)} ul, {p.tags.get('ol',0)} ol")
    if intent in ("search", "education"):
        # Readability: long runs of plain paragraphs with no list or table break
        run = best = 0
        for t, x, a in p.blocks:
            if t == "p" and len(words(x)) >= 8:
                run += 1
                best = max(best, run)
            elif t in ("li", "td", "th", "h2", "h3", "h4"):
                run = 0
        r.add("PASS" if best <= 4 else "WARN", "Readability: paragraphs in a row within a section",
              f"longest run {best} paragraphs (use bullets for parallel items, numbered lists for steps or rankings)")
        h2_text = " ".join(h2s).lower()
        if re.search(r"\bsteps?\b|how to|\bstep-by-step\b|\bbest\b|\btop \d+\b", h2_text + " " + fields.get("title", "").lower()) and p.tags.get("ol", 0) == 0:
            r.add("WARN", "Steps or rankings use a numbered list", "no <ol> found")
    if intent in ("search", "education"):
        r.add("PASS" if has_table else "WARN", "Has a table/comparison block", f"{p.tags.get('table',0)} tables")

    # FAQ: h3s after an FAQ h2 until next h2
    faq_count, in_faq = 0, False
    for t, x in headings:
        if t == "h2":
            in_faq = bool(re.search(r"faq|frequently asked", x, re.I))
        elif t == "h3" and in_faq:
            faq_count += 1
    if faq_count == 0:
        if intent in ("search", "education"):
            r.add("FAIL", "FAQ section with 3–6 questions", "no FAQ H2 with H3 questions found")
        elif intent == "promotion":
            r.add("WARN", "FAQ section (optional; helps answer purchase objections)", "none found")
        else:
            r.add("INFO", "FAQ section (optional for brand posts)", "none found")
    else:
        r.rng("FAQ questions", faq_count, (3, 6), (2, 8))

    r.add("PASS" if re.search(r"last updated", body_text, re.I) else "FAIL", "Visible 'Last updated' date")
    r.add("PASS" if re.search(r"about the author|author", body_text, re.I) else "WARN", "Author bio present")

    # ---------- Links ----------
    prod = [h for h, _ in p.links if re.search(r"/(products|collections)/", h)]
    blog = [h for h, _ in p.links if re.search(r"/blogs/", h)]
    ext = [h for h, _ in p.links if h.startswith("http") and not re.search(r"/(products|collections|blogs|pages)/", h)
           and "unsplash.com" not in h and "pexels.com" not in h and "pixabay.com" not in h]
    r.rng("Product/collection links", len(set(prod)), prod_ok, prod_warn)
    r.rng("Related blog post links", len(set(blog)), blog_ok, blog_warn)
    r.rng("External citations", len(set(ext)), ext_ok, ext_warn)
    bad = [a for _, a in p.links if a.lower().strip(" .!→>") in BAD_ANCHORS]
    r.add("PASS" if not bad else "FAIL", "Descriptive anchor text", f"bad anchors: {bad}" if bad else "")

    # ---------- Images ----------
    if not p.images:
        r.add("WARN", "In-body images", "none")
    for i, img in enumerate(p.images, 1):
        src = img.get("src", "")
        alt = (img.get("alt") or "").strip()
        m = re.search(r"\[\[\s*(?:UPLOAD|USER MEDIA):\s*([^\]]+?)\s*\]\]", src)
        fname = m.group(1) if m else src.split("?")[0].rstrip("/").split("/")[-1]
        r.add("PASS" if alt else "FAIL", f"Image {i} alt text", alt[:80] or "missing")
        if len(alt) > 125:
            r.add("WARN", f"Image {i} alt ≤125 chars", f"{len(alt)} chars")
        if "images.unsplash.com" in src or "images.pexels.com" in src:
            r.add("WARN", f"Image {i} file name", "hotlinked stock URL — rename to descriptive .webp on upload")
        else:
            stem = re.sub(r"\.[a-z0-9]+$", "", fname, flags=re.I)
            ok = bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){1,}", stem)) and not GENERIC_IMG.match(stem)
            r.add("PASS" if ok else "FAIL", f"Image {i} descriptive kebab-case name", fname)
            if not fname.lower().endswith(".webp"):
                r.add("WARN", f"Image {i} WebP format", fname)
        if not (img.get("width") and img.get("height")):
            r.add("WARN", f"Image {i} width/height set", "missing (hurts CLS)")

    # ---------- Fields ----------
    if fields:
        st = fields.get("seo_title", "")
        r.rng("SEO title length", len(st), (50, 60), (45, 65), " chars")
        md = fields.get("meta_description", "")
        r.rng("Meta description length", len(md), (140, 155), (120, 160), " chars")
        h = fields.get("handle", "")
        handle_ok = bool(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", h))
        r.add("PASS" if handle_ok else "FAIL", "Handle lowercase-hyphenated", h)
        if re.search(r"(19|20)\d{2}", h):
            r.add("FAIL", "Handle has no dates", h)
        hw = h.split("-")
        filler = [w for w in hw if w in STOPWORDS and w not in {"to", "vs"}]
        if len(hw) > 7 or filler:
            r.add("WARN", "Handle short, no filler", f"{len(hw)} words; filler: {filler}")
        ex = fields.get("excerpt", "")
        r.add("PASS" if 80 <= len(ex) <= 320 else ("WARN" if ex else "FAIL"), "Excerpt filled", f"{len(ex)} chars")
        tags = fields.get("tags", [])
        r.rng("Tags", len(tags), (2, 5), (1, 7))
        r.add("PASS" if fields.get("author") else "WARN", "Author set", fields.get("author", ""))
        fi = fields.get("featured_image") or {}
        r.add("PASS" if fi.get("alt") and fi.get("file_name") else "WARN", "Featured image with alt", fi.get("file_name", ""))

        if kw:
            first100 = " ".join(words(" ".join(content_paras))[:100])
            for name, text in [("title", fields.get("title", "")), ("SEO title", st),
                               ("meta description", md), ("first 100 words", first100),
                               ("an H2", " | ".join(h2s))]:
                res = contains_kw(text, kw)
                r.add({"exact": "PASS", "partial": "WARN", "none": kw_miss}[res],
                      f"Primary keyword in {name}", f"'{kw}' → {res}")
            density = body_text.lower().count(kw.lower()) / max(wc, 1) * 100
            if density > 2.5:
                r.add("WARN", "Keyword not stuffed", f"{density:.1f}% exact-match density")
        sec = fields.get("secondary_keywords", [])
        if sec:
            found = [s for s in sec if contains_kw(body_text, s) != "none"]
            r.add("PASS" if len(found) >= min(3, len(sec)) else "WARN", "Secondary keywords used",
                  f"{len(found)}/{len(sec)}: missing {[s for s in sec if s not in found]}")
        if brand:
            bc = len(re.findall(re.escape(brand), body_text, re.I))
            r.rng("Brand mentions", bc, (3, 6), (2, 9))

    # ---------- Call to action, value, tone ----------
    cta = re.search(r'<(div|section|aside|p)[^>]*class="[^"]*post-cta[^"]*"[^>]*>(.*?)</\1>', html, re.I | re.S)
    if cta and re.search(r"<a\s[^>]*href=", cta.group(2), re.I):
        r.add("PASS", "Clear call to action (post-cta block with a link)")
    elif cta:
        r.add("FAIL", "Call to action needs a tangible next step", "post-cta block has no link")
    else:
        tail = html[int(len(html) * 0.7):]
        if re.search(r'<a\s[^>]*href="[^"]*(/products/|/collections/|/pages/|mailto:)', tail, re.I):
            r.add("WARN", "Call to action", "no post-cta block; a link near the end may serve as the CTA. Wrap it in <div class=\"post-cta\">")
        else:
            r.add("FAIL", "Call to action", "no clear next step for the reader (add a post-cta block with a link)")
    if fields and not fields.get("cta"):
        r.add("WARN", "CTA recorded in fields JSON", "add a 'cta' object: {text, url, goal}")
    if fields and not fields.get("net_new_value"):
        r.add("WARN", "Net-new value stated", "add 'net_new_value' (what a reader gets here that a generic article lacks)")
    if fields and not fields.get("first_hand_asset"):
        r.add("WARN", "First-hand asset named", "add 'first_hand_asset' (founder story, testing note, customer question, data, photo) or a [[BRAND TO ADD]] placeholder")
    if fields and not fields.get("stance"):
        r.add("WARN", "Point of view stated", "add 'stance' (the position taken and who it's not for)")
    vague = re.findall(r"high-?quality|premium quality|best-in-class|top-?notch|it depends on (?:many|several) factors|everyone is different|a wide range of|numerous benefits|results may vary widely", body_text, re.I)
    if vague:
        r.add("WARN", "Vague claims (replace with numbers, names, materials)", "; ".join(sorted(set(v.lower() for v in vague))[:6]))
    sents = [len(words(s)) for s in re.split(r"(?<=[.!?])\s+", " ".join(content_paras)) if len(words(s)) > 2]
    if len(sents) >= 12:
        mean = sum(sents) / len(sents)
        sd = (sum((x - mean) ** 2 for x in sents) / len(sents)) ** 0.5
        r.add("PASS" if sd >= 5 else "WARN", "Sentence length varies (reads natural)", f"mean {mean:.0f} words, spread {sd:.1f}")
    if not re.search(r"\b(we|our|I|my)\b", body_text, re.I):
        r.add("WARN", "Brand voice present (we/our)", "post never speaks as the brand")
    press = re.findall(r"we(?:'re| are) (?:so )?(?:excited|thrilled|proud) to|game-?chang\w+|revolutionary|world-class|cutting-edge|state-of-the-art|industry-leading|best-in-class|unparalleled|in today's fast-paced", body_text, re.I)
    if press:
        r.add("WARN" if intent == "promotion" else "FAIL", "Press-release or generic filler wording", "; ".join(sorted(set(x.lower() for x in press))[:6]))
    else:
        r.add("PASS", "No press-release or generic filler wording")

    # ---------- Placeholders ----------
    ph = re.findall(r"\[\[([^\]]+)\]\]", html)
    r.add("INFO", "Placeholders to fill", f"{len(ph)}: " + "; ".join(ph[:20]))

    if args.json:
        print(json.dumps({"word_count": wc, "results": r.rows}, indent=2))
    else:
        for row in r.rows:
            print(f"[{row['status']:4}] {row['check']}" + (f" — {row['detail']}" if row["detail"] else ""))
        counts = {s: sum(1 for x in r.rows if x["status"] == s) for s in ("PASS", "WARN", "FAIL")}
        print(f"\nSummary: {counts['PASS']} pass, {counts['WARN']} warn, {counts['FAIL']} fail")
    sys.exit(1 if any(x["status"] == "FAIL" for x in r.rows) else 0)


if __name__ == "__main__":
    main()
