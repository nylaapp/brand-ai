#!/usr/bin/env python3
"""List and download the images of a source article, ready to be uploaded to the store's own file library.

    python3 extract_media.py --url <article-url> --out media.json [--download <dir>] [--min-width 400]
    python3 extract_media.py --html <saved.html> --base <article-url> --out media.json [--download <dir>]

For each image in the article body (and the page's og:image) it records the largest version the page offers, the alt text,
any caption, where it sits (the heading and paragraph it follows), and whether to keep it. Navigation, header, footer,
sidebar, logos, icons, avatars, tracking pixels, data: URIs and tiny images are skipped with the reason. With --download
it fetches each kept image (original size first, then the sized copy), checks the type by its first bytes, reads the real
width and height, and flags images that are too small or too big for Shopify (20 MB). Videos and embeds are listed, not
downloaded. Public pages only, honours robots.txt, one request at a time. Python 3 standard library.
Exit codes: 0 ok (even if no images), 2 bad input or page unreadable.
"""
import argparse, hashlib, json, re, shutil, ssl, struct, subprocess, sys, time, urllib.error, urllib.parse, urllib.request, urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path

UA = "Mozilla/5.0 (compatible; brand-ai-blog-transfer/1.0)"
SKIP_TAGS = {"nav", "header", "footer", "aside", "form", "noscript", "script", "style", "svg"}
SKIP_URL = re.compile(r"(logo|icon|avatar|gravatar|sprite|spinner|badge|emoji|favicon|pixel|tracking|spacer|blank\.|loading\.|placeholder)", re.I)
MAX_BYTES = 20 * 1024 * 1024
_last = [0.0]
_robots = {}


# ------------------------------------------------------------------ fetching
def _curl(url, binary=False):
    if not shutil.which("curl"):
        return None, None
    r = subprocess.run(["curl", "-sL", "-m", "40", "--max-filesize", str(MAX_BYTES), "-A", UA, "-w", "\n%{http_code}", url], capture_output=True, timeout=60)
    body, _, code = r.stdout.rpartition(b"\n")
    ok = r.returncode == 0 and code.strip() == b"200"
    return (body if ok else None), (code.decode() if code else None)


def allowed(url):
    p = urllib.parse.urlsplit(url); base = f"{p.scheme}://{p.netloc}"
    if base not in _robots:
        rp = urllib.robotparser.RobotFileParser(base + "/robots.txt")
        data, _ = fetch(base + "/robots.txt", check=False)
        if data is None:
            rp = None
        else:
            rp.parse(data.decode("utf-8", "replace").splitlines())
        _robots[base] = rp
    rp = _robots[base]
    return True if rp is None else rp.can_fetch(UA, url)


def fetch(url, check=True):
    if check and not allowed(url):
        return None, "blocked by robots.txt"
    wait = 0.4 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read(MAX_BYTES + 1)
            return data, str(r.status)
    except urllib.error.HTTPError as e:
        return None, str(e.code)
    except urllib.error.URLError as e:
        if isinstance(getattr(e, "reason", None), ssl.SSLError):
            return _curl(url)  # system trust store; certificate checks stay on
        return None, str(e.reason)
    except Exception as e:
        return None, str(e)
    finally:
        _last[0] = time.time()


# ------------------------------------------------------------------ parsing
def best_from_srcset(srcset):
    best, best_w = None, -1
    for part in (srcset or "").split(","):
        bits = part.strip().split()
        if not bits:
            continue
        w = 0
        if len(bits) > 1:
            m = re.match(r"([\d.]+)([wx])", bits[1])
            if m:
                w = float(m.group(1)) * (1000 if m.group(2) == "x" else 1)
        if w >= best_w:
            best, best_w = bits[0], w
    return best


class Page(HTMLParser):
    def __init__(self, base):
        super().__init__(convert_charrefs=True)
        self.base, self.stack, self.items, self.videos = base, [], [], []
        self.og, self.heading, self.para, self.in_h, self.h_buf = None, "", 0, None, []
        self.has_article = False
        self.fig, self.figcap, self.cap_buf = None, False, []
        self.title = ""
        self.in_title = False

    def _skipped(self):
        return any(t in SKIP_TAGS for t in self.stack)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "meta" and (a.get("property") in ("og:image", "og:image:secure_url") or a.get("name") == "twitter:image") and a.get("content") and not self.og:
            self.og = urllib.parse.urljoin(self.base, a["content"])
        if tag in ("br", "hr", "img", "meta", "link", "source", "input", "wbr"):
            pass
        else:
            self.stack.append(tag)
        if tag == "article":
            self.has_article = True
        if re.fullmatch(r"h[1-6]", tag) and not self._skipped():
            self.in_h, self.h_buf = tag, []
        if tag == "p" and not self._skipped():
            self.para += 1
        if tag == "figure":
            self.fig = {"caption": ""}
        if tag == "figcaption":
            self.figcap, self.cap_buf = True, []
        if tag in ("video", "iframe") and not self._skipped():
            self.videos.append({"type": tag, "src": urllib.parse.urljoin(self.base, a.get("src") or a.get("data-src") or "")})
        if tag == "img":
            self._img(a)

    def _img(self, a):
        cands = [best_from_srcset(a.get("srcset")), best_from_srcset(a.get("data-srcset")), a.get("data-src"), a.get("data-lazy-src"),
                 a.get("data-original"), a.get("src")]
        src = next((c for c in cands if c and not c.startswith("data:")), None)
        if not src:
            return
        w = int(re.sub(r"\D", "", a.get("width", "") or "") or 0)
        h = int(re.sub(r"\D", "", a.get("height", "") or "") or 0)
        self.items.append({"src": urllib.parse.urljoin(self.base, src.strip()), "alt": (a.get("alt") or "").strip(), "declared_width": w,
                           "declared_height": h, "after_heading": self.heading, "after_paragraph": self.para, "skipped_container": self._skipped(),
                           "in_article": "article" in self.stack or "main" in self.stack, "fig": self.fig is not None, "caption": ""})
        if self.fig is not None:
            self.fig.setdefault("imgs", []).append(len(self.items) - 1)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if self.in_h and tag == self.in_h:
            self.heading = " ".join("".join(self.h_buf).split()); self.in_h = None
        if tag == "figcaption":
            self.figcap = False
            if self.fig is not None:
                self.fig["caption"] = " ".join("".join(self.cap_buf).split())
        if tag == "figure" and self.fig is not None:
            for i in self.fig.get("imgs", []):
                self.items[i]["caption"] = self.fig["caption"]
            self.fig = None
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass

    def handle_data(self, d):
        if self.in_title:
            self.title += d
        if self.in_h:
            self.h_buf.append(d)
        if self.figcap:
            self.cap_buf.append(d)


def original_of(url):
    """WordPress and many CMSs add -300x200 before the extension; the full-size file sits without it."""
    m = re.search(r"-\d{2,4}x\d{2,4}(\.[A-Za-z0-9]+)(\?.*)?$", url)
    return re.sub(r"-\d{2,4}x\d{2,4}(\.[A-Za-z0-9]+)(\?.*)?$", r"\1", url) if m else None


def classify(items, og, min_w):
    seen, out, lead_set = set(), [], False
    in_article_any = any(i["in_article"] and not i["skipped_container"] for i in items)
    for i in items:
        key = re.sub(r"-\d{2,4}x\d{2,4}(?=\.[A-Za-z0-9]+(\?|$))", "", i["src"].split("?")[0])
        reason = None
        if key in seen:
            reason = "duplicate of an earlier image"
        elif i["skipped_container"]:
            reason = "inside navigation, header, footer, sidebar or a form"
        elif in_article_any and not i["in_article"]:
            reason = "outside the article body"
        elif SKIP_URL.search(i["src"].rsplit("/", 1)[-1]) or SKIP_URL.search(i["alt"] or "x" * 0):
            reason = "looks like a logo, icon, avatar or tracking image"
        elif 0 < i["declared_width"] <= 2 or 0 < i["declared_height"] <= 2:
            reason = "tracking pixel"
        elif i["src"].lower().split("?")[0].endswith(".svg"):
            reason = "SVG (usually an icon or logo)"
        elif 0 < i["declared_width"] < 120 and 0 < i["declared_height"] < 120:
            reason = "tiny image"
        seen.add(key)
        i["status"] = "skip" if reason else "keep"
        i["reason"] = reason or ""
        i["role"] = ""
        if not reason:
            i["role"] = "lead" if not lead_set else "inline"
            lead_set = True
        out.append(i)
    if og:
        key = re.sub(r"-\d{2,4}x\d{2,4}(?=\.[A-Za-z0-9]+(\?|$))", "", og.split("?")[0])
        if key not in seen:
            out.append({"src": og, "alt": "", "declared_width": 0, "declared_height": 0, "after_heading": "", "after_paragraph": 0,
                        "caption": "", "status": "keep", "reason": "", "role": "social" if lead_set else "lead",
                        "note": "page social-share image (og:image); not in the article body"})
    for n, i in enumerate(out, 1):
        i["index"] = n
        for k in ("skipped_container", "in_article", "fig"):
            i.pop(k, None)
    return out


# ------------------------------------------------------------------ images
def sniff(b):
    """Return (extension, width, height) from the first bytes, or None."""
    try:
        if b[:3] == b"\xff\xd8\xff":
            i = 2
            while i < len(b) - 9:
                if b[i] != 0xFF:
                    i += 1; continue
                m = b[i + 1]
                if m in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
                    h, w = struct.unpack(">HH", b[i + 5:i + 9]); return "jpg", w, h
                i += 2 + struct.unpack(">H", b[i + 2:i + 4])[0]
            return "jpg", 0, 0
        if b[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", b[16:24]); return "png", w, h
        if b[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", b[6:10]); return "gif", w, h
        if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
            t = b[12:16]
            if t == b"VP8 ":
                w, h = struct.unpack("<HH", b[26:30]); return "webp", w & 0x3FFF, h & 0x3FFF
            if t == b"VP8L":
                v = struct.unpack("<I", b[21:25])[0]; return "webp", (v & 0x3FFF) + 1, ((v >> 14) & 0x3FFF) + 1
            if t == b"VP8X":
                return "webp", 1 + int.from_bytes(b[24:27], "little"), 1 + int.from_bytes(b[27:30], "little")
            return "webp", 0, 0
    except Exception:
        return None
    return None


def slug(s):
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")[:60] or "image"


def download(items, folder, min_w, seed):
    folder = Path(folder); folder.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for it in items:
        if it["status"] != "keep":
            continue
        tries = [u for u in (original_of(it["src"]), it["src"]) if u]
        data, code, used = None, None, None
        for u in tries:
            d, code = fetch(u)
            if d and sniff(d[:64] if len(d) > 64 else d) or d and sniff(d):
                data, used = d, u; break
        if not data:
            it.update(status="failed", reason=f"could not download an image (last status {code})"); continue
        if len(data) > MAX_BYTES:
            it.update(status="flag", reason="over Shopify's 20 MB image limit"); continue
        ext, w, h = sniff(data)
        digest = hashlib.sha256(data).hexdigest()
        if digest in hashes:
            it.update(status="skip", reason=f"identical file to image {hashes[digest]}"); continue
        hashes[digest] = it["index"]
        name = f"{it['index']:02d}-{slug(it['alt'] or it['after_heading'] or seed or 'image')}.{ext}"
        (folder / name).write_bytes(data)
        it.update(downloaded_from=used, file=str(folder / name), bytes=len(data), width=w, height=h, sha256=digest[:16])
        if w and w < min_w:
            it["status"], it["reason"] = "flag", f"small: {w}px wide (under {min_w}px); fine as an inline image only if the person accepts it"
    return items


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--url"); g.add_argument("--html")
    ap.add_argument("--base"); ap.add_argument("--out", required=True)
    ap.add_argument("--download"); ap.add_argument("--min-width", type=int, default=400)
    a = ap.parse_args()
    if a.url:
        data, code = fetch(a.url)
        if not data:
            print(f"could not read the page ({code}); read it with a browser tool and save the HTML, then use --html", file=sys.stderr); return 2
        text, base = data.decode("utf-8", "replace"), a.url
    else:
        text, base = Path(a.html).read_text(encoding="utf-8", errors="replace"), (a.base or "")
        if not base:
            print("--html needs --base (the article URL) to resolve relative image links", file=sys.stderr); return 2
    p = Page(base); p.feed(text)
    items = classify(p.items, p.og, a.min_width)
    seed = slug(urllib.parse.urlsplit(base).path.rstrip("/").rsplit("/", 1)[-1])
    if a.download:
        items = download(items, a.download, a.min_width, seed)
    out = {"source": base, "page_title": " ".join(p.title.split()), "images": items, "videos_and_embeds": p.videos,
           "counts": {k: sum(1 for i in items if i["status"] == k) for k in ("keep", "flag", "skip", "failed")}}
    Path(a.out).write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    c = out["counts"]
    print(f"{len(items)} image(s): keep {c['keep']}, flag {c['flag']}, skip {c['skip']}, failed {c['failed']}; {len(p.videos)} video/embed(s) listed -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
