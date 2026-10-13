#!/usr/bin/env python3
"""Compare a draft article's HTML with the layout of the store's own published articles.

    python3 layout_check.py --samples samples.json --draft <post>.html [--image-set yes|no] [--json]

`samples.json` is a list of the store's newest published articles, from the Admin API
(`articles(first: 6, sortKey: PUBLISHED_AT, reverse: true, query: "published_status:published") { nodes { handle body image { url } } }`):
either a list of body strings, or objects with a `body` and an optional `image`. It learns what is typical (does the body start with a
figure, which attributes the images carry, where they are hosted, which heading levels and attributes appear, the closing block) and
reports where the draft differs. It checks structure, not wording. Python 3 standard library only.
Exit codes: 0 no FAIL (warnings allowed), 1 at least one FAIL, 2 unreadable input.
"""
import argparse, json, re, sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ALLOWED_CLASS = re.compile(r"^(aya-blog-|post-cta|post-faq)")  # classes the store's own articles use; learned from samples below


class Scan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.first = None; self.tags = Counter(); self.imgs = []; self.attrs = Counter(); self.classes = Counter()
        self.stack = []; self.last_top = None; self.para_words = []; self._p = None; self.depth = 0; self.block_text = {}; self._blk = None; self._buf = []
        self.top_order = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if self.depth == 0:
            if self.first is None:
                self.first = tag
            self.top_order.append(tag)
            if tag == "div" and a.get("class"):
                self._blk, self._buf = a["class"], []
        if tag not in ("img", "br", "hr", "meta", "link", "input"):
            self.depth += 1
        self.tags[tag] += 1
        for k, v in attrs:
            self.attrs[(tag, k)] += 1
            if k == "class":
                for c in (v or "").split():
                    self.classes[c] += 1
        if tag == "img":
            self.imgs.append(a)
        if tag == "p":
            self._p = []

    def handle_endtag(self, tag):
        if tag not in ("img", "br", "hr", "meta", "link", "input"):
            self.depth = max(0, self.depth - 1)
        if tag == "p" and self._p is not None:
            self.para_words.append(len(" ".join(self._p).split())); self._p = None
        if self.depth == 0 and self._blk is not None and tag == "div":
            self.block_text[self._blk] = " ".join(" ".join(self._buf).split()); self._blk = None

    def handle_data(self, d):
        if self._p is not None:
            self._p.append(d)
        if self._blk is not None:
            self._buf.append(d)


def scan(html):
    s = Scan(); s.feed(html); return s


def host(u):
    return urlsplit(u).netloc.lower().removeprefix("www.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--samples", required=True); ap.add_argument("--draft", required=True)
    ap.add_argument("--image-set", choices=["yes", "no", "unknown"], default="unknown", help="is the article's image field set on the draft?")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        raw = json.loads(Path(a.samples).read_text(encoding="utf-8"))
        bodies = [(x if isinstance(x, str) else x.get("body", "")) for x in raw]
        sample_imgfield = [(None if isinstance(x, str) else bool(x.get("image"))) for x in raw]
        draft = Path(a.draft).read_text(encoding="utf-8")
    except Exception as e:
        print(f"cannot read input: {e}", file=sys.stderr); return 2
    S = [scan(b) for b in bodies if b.strip()]
    if len(S) < 2:
        print("need at least 2 published samples to learn a layout", file=sys.stderr); return 2
    D = scan(draft)
    n = len(S)
    res = []  # (level, check, detail)

    def add(level, check, detail):
        res.append((level, check, detail))

    with_img = [s for s in S if s.imgs]
    lead_rate = sum(1 for s in S if s.first == "figure") / n
    typical_closing = Counter(s.top_order[-1] for s in S if s.top_order).most_common(1)[0][0]
    # 1 lead figure
    if lead_rate >= 0.3:
        if D.first == "figure":
            add("PASS", "lead image", f"the body starts with a figure, like {int(lead_rate*100)}% of the store's articles")
        elif D.imgs:
            add("FAIL", "lead image", f"the store's articles with an image open the body with it ({int(lead_rate*100)}% of samples); this draft has images but does not start with a figure")
        else:
            add("FAIL", "lead image", f"no image in the body; {int(lead_rate*100)}% of the store's articles open with a lead figure. Add the source image or list it as missing input")
    else:
        add("INFO", "lead image", "the store's articles rarely open with a figure; not enforced")
    # 2 image attributes
    if with_img:
        need = [k for k in ("src", "alt", "width", "height", "loading") if sum(1 for s in with_img for i in s.imgs if k in i) / max(1, sum(len(s.imgs) for s in with_img)) >= 0.75]
        for i, img in enumerate(D.imgs, 1):
            miss = [k for k in need if not img.get(k) and not (k == "alt" and "alt" in img)]
            if miss:
                add("FAIL", f"image {i} attributes", "missing " + ", ".join(miss))
            elif img.get("alt", "") == "":
                add("WARN", f"image {i} alt text", "empty alt: the store's migrated articles do this, but a new post should describe the image")
            else:
                add("PASS", f"image {i} attributes", "has " + ", ".join(need))
        hosts = Counter(host(i["src"]) for s in with_img for i in s.imgs if i.get("src"))
        dh = {host(i["src"]) for i in D.imgs if i.get("src")}
        shop = lambda h: h.endswith("shopify.com") or h.endswith("shopifycdn.com")
        known = set(hosts)
        for h in dh:
            if h in known or shop(h):
                add("PASS", "image host", f"{h} (store hosts: {', '.join(f'{k} x{v}' for k, v in hosts.most_common())})")
            else:
                add("FAIL", "image host", f"{h} is not the store's own CDN: images must be uploaded to the store, not linked from the source site")
        dims = Counter((i.get("width"), i.get("height")) for s in with_img for i in s.imgs)
        if dims:
            add("INFO", "image size attributes", "samples use " + ", ".join(f"{w}x{h} (x{c})" for (w, h), c in dims.most_common(3)) + "; the draft uses the real file size")
        if sum(1 for _ in D.imgs) > 1 and max((len(s.imgs) for s in S), default=0) <= 1:
            add("WARN", "number of images", "the store's articles carry one image; this draft has several: check the store's multi-image rule before keeping them")
    # image field
    if a.image_set == "no" and D.imgs:
        add("WARN", "article image field", "the body has an image but the article's image field is empty (used for blog cards and social previews)")
    elif a.image_set == "yes":
        add("PASS", "article image field", "set")
    # 3 forbidden constructs
    bad = [t for t in ("h1", "script", "iframe", "style", "form") if D.tags[t]]
    if bad:
        add("FAIL", "forbidden tags", ", ".join(bad))
    else:
        add("PASS", "tags", "no h1, script, iframe, style or form")
    used_classes = set(D.classes)
    sample_classes = set(c for s in S for c in s.classes)
    odd = sorted(c for c in used_classes if c not in sample_classes and not ALLOWED_CLASS.match(c))
    add("FAIL" if odd else "PASS", "classes", ("classes the store's articles never use: " + ", ".join(odd)) if odd else "only classes the store's own articles use")
    if D.attrs.get(("p", "style")) or any(k == "style" for (_, k) in D.attrs) or any(k.startswith("data-") for (_, k) in D.attrs):
        add("FAIL", "inline style or data attributes", "remove them; the theme styles the article")
    # 4 headings
    sh = Counter(t for s in S for t in s.tags if re.fullmatch(r"h[1-6]", t))
    dh = {t: c for t, c in D.tags.items() if re.fullmatch(r"h[1-6]", t)}
    if sh:
        extra = [t for t in dh if t not in sh and t != "h2"]
        add("WARN" if extra else "PASS", "heading levels", f"samples use {dict(sh)}; draft uses {dh or 'none'}" + (f" (new levels: {', '.join(extra)})" if extra else ""))
    else:
        add("INFO", "heading levels", f"the samples have no subheadings; draft uses {dh or 'none'}. The theme styles h2 to h4 compactly")
    # 5 closing block
    for cls in {c for s in S for c in s.block_text if "disclaimer" in c}:
        ref = Counter(s.block_text.get(cls) for s in S if cls in s.block_text).most_common(1)[0][0]
        got = D.block_text.get(cls)
        if got is None:
            add("FAIL", f"closing block .{cls}", "missing")
        elif got != ref:
            add("FAIL", f"closing block .{cls}", "text differs from the store's standard block")
        else:
            add("PASS", f"closing block .{cls}", "identical to the store's standard text")
        if D.top_order and D.top_order[-1] != typical_closing:
            add("FAIL", "closing position", f"the last element should be the {typical_closing} block")
        elif D.top_order:
            add("PASS", "closing position", "the block is last")
    # 6 paragraphs and lists
    mx = max((max(s.para_words) for s in S if s.para_words), default=0)
    if D.para_words and max(D.para_words) > max(150, mx):
        add("WARN", "paragraph length", f"longest paragraph {max(D.para_words)} words (samples up to {mx})")
    sl = sum(1 for s in S if s.tags["ul"] or s.tags["ol"]) / n
    add("INFO", "lists", f"{int(sl*100)}% of samples use lists; the draft has {D.tags['ul'] + D.tags['ol']}")
    out = {"samples": n, "checks": [{"level": l, "check": c, "detail": d} for l, c, d in res], "fail": sum(1 for r in res if r[0] == "FAIL"), "warn": sum(1 for r in res if r[0] == "WARN")}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"layout check against {n} published articles")
        for l, c, d in res:
            print(f"  [{l}] {c}: {d}")
        print("RESULT:", "FAIL" if out["fail"] else ("PASS with warnings" if out["warn"] else "PASS"))
    return 1 if out["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
