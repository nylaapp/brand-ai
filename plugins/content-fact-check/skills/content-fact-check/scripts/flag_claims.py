#!/usr/bin/env python3
"""Pre-screen content for sentences that make checkable or risky claims.

Usage:
    python flag_claims.py content.html [--json] [--min-tier low|medium|high]

Splits HTML, Markdown or plain text into sentences and flags those containing regulatory,
medical, safety/pregnancy, ingredient, statistical, performance or sustainability language.
It uses patterns, not understanding: treat the output as a candidate list. Add what it
missed and drop false alarms. Stdlib only.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser

CATEGORIES = {
    "regulatory": (r"\bFDA\b|\bapproved\b|\bcleared\b|\bclearance\b|\bcertified\b|\bcertification\b|\bregistered\b|"
                   r"\blicen[sc]ed\b|\bauthori[sz]ed\b|\bCE[ -]?mark|\bISO\s?\d|\bGMP\b|\bEPA\b|\bUSDA\b|"
                   r"\bMHRA\b|\bTGA\b|\bHealth Canada\b|\bEMA\b|\bNSF\b|\bcompli(?:ant|ance)\b", "high"),
    "medical": (r"\btreat(?:s|ed|ing|ment|ments)?\b|\bcure[sd]?\b|\bheal(?:s|ed|ing)?\b|\bprevent(?:s|ed|ing)?\b|"
                r"\bdiagnos\w+|\btherap\w+|\bclinical(?:ly)?\b|\bproven\b|\bprescription\b|\bdisease\b|\bcondition\b|"
                r"\bsymptoms?\b|\bside effects?\b|\bdermatolog\w+|\bmedical(?:ly)?\b|\binfection\b|\binflammation\b|"
                r"\bpatients?\b|\bdoctor|\bphysician|\bclinician", "high"),
    "safety_pregnancy": (r"\bpregnan\w+|\bbreast-?feed\w*|\bnursing\b|\blactat\w+|\binfants?\b|\bbab(?:y|ies)\b|\bchildren\b|"
                         r"\bkids?\b|\bsafe(?:ly|ty)?\b|\bnon-?toxic\b|\btoxic\b|\bhypoallergenic\b|\ballerg\w+|"
                         r"\bcontraindicat\w+|\brisks?\b|\bharmless\b|\bgentle\b", "high"),
    "ingredient": (r"\bingredients?\b|\bcontains?\b|\bformulated\b|\bfree of\b|\b\w+-free\b|"
                   r"\b\d+(?:\.\d+)?\s?(?:%|percent)\b|\bparabens?\b|\bsulfates?\b|\bfragrance\b|\bpreservatives?\b|"
                   r"\bactive\b|\bconcentrat\w+|\bpeptides?\b|\bacid\b|\bextract\b", "high"),
    "statistic": (r"\b\d+(?:\.\d+)?\s?(?:%|percent|x\b|times\b|million|billion)|\b\d+\s?(?:out of|in)\s?\d+\b|"
                  r"\bstud(?:y|ies)\b|\bresearch (?:shows|suggests|found)\b|\baccording to\b|\bsurvey\b|"
                  r"\bsample\b|\btrials?\b|\bmeta-analysis\b|\b(?:19|20)\d\d\b.{0,30}\b(?:study|report|survey)\b", "medium"),
    "performance": (r"\blasts?\b|\bpermanent(?:ly)?\b|\binstant(?:ly)?\b|\bguarantee[sd]?\b|\bresults?\b|"
                    r"\bwithin \d+\s?(?:days?|weeks?|hours?|minutes?)\b|\bin just \d+|\bworks?\b|\bproven\b|"
                    r"\breduces?\b|\bimproves?\b|\bboosts?\b|\bincreases?\b|\blong-?lasting\b", "medium"),
    "comparison": (r"\bbest\b|\bbetter than\b|\bmost\b|\bonly\b|\bfirst\b|\bleading\b|\b#\s?1\b|\bnumber one\b|"
                   r"\bsuperior\b|\bunlike\b|\bunmatched\b|\bsafest\b|\bstrongest\b", "medium"),
    "sustainability": (r"\beco-?friendly\b|\bsustainab\w+|\bnatural(?:ly)?\b|\borganic\b|\bclean\b|\bgreen\b|\bvegan\b|"
                       r"\bcruelty-?free\b|\bbiodegradable\b|\brecycl\w+|\bcarbon\b|\bplastic-?free\b|\bethical(?:ly)?\b", "medium"),
}
TIER_RANK = {"low": 0, "medium": 1, "high": 2}


class Blocks(HTMLParser):
    """Collects text blocks with their nearest heading and whether a link appears in them."""

    BLOCK = {"p", "li", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "figcaption", "dd", "dt"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks = []
        self.heading = ""
        self._cur = None
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self._skip += 1
        if tag in self.BLOCK:
            self._cur = {"tag": tag, "text": [], "link": False}
        elif tag == "a" and self._cur is not None and dict(attrs).get("href", "").startswith("http"):
            self._cur["link"] = True

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
        if self._cur is not None and tag == self._cur["tag"]:
            text = " ".join("".join(self._cur["text"]).split())
            if re.fullmatch(r"h[1-6]", tag):
                self.heading = text
            if text:
                self.blocks.append({"text": text, "heading": self.heading, "link": self._cur["link"]})
            self._cur = None

    def handle_data(self, data):
        if self._cur is not None and not self._skip:
            self._cur["text"].append(data)


def sentences(text):
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'\[(])", text)
    return [s.strip() for s in parts if len(s.strip()) > 3]


def load_blocks(raw, path):
    if re.search(r"</?(p|h[1-6]|li|div|table|ul|ol)\b", raw, re.I):
        p = Blocks()
        p.feed(raw)
        return p.blocks
    blocks, heading = [], ""
    for para in re.split(r"\n\s*\n", raw):
        t = " ".join(para.split())
        if not t:
            continue
        m = re.match(r"#+\s+(.*)", t)
        if m:
            heading = m.group(1)
            continue
        blocks.append({"text": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t), "heading": heading,
                       "link": bool(re.search(r"\]\(https?://", para))})
    return blocks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--min-tier", default="low", choices=list(TIER_RANK))
    a = ap.parse_args()
    raw = open(a.path, encoding="utf-8").read()
    out, total = [], 0
    for b in load_blocks(raw, a.path):
        for s in sentences(b["text"]):
            total += 1
            if s.endswith("?"):  # a question asserts nothing; its answer is checked on its own
                continue
            cats, tier = [], "low"
            for name, (pat, t) in CATEGORIES.items():
                if re.search(pat, s, re.I):
                    cats.append(name)
                    if TIER_RANK[t] > TIER_RANK[tier]:
                        tier = t
            if not cats:
                continue
            if TIER_RANK[tier] < TIER_RANK[a.min_tier]:
                continue
            out.append({"id": len(out) + 1, "tier": tier, "categories": cats, "sentence": s,
                        "section": b["heading"], "block_has_external_link": b["link"]})
    out.sort(key=lambda x: (-TIER_RANK[x["tier"]], x["id"]))
    summary = {"sentences": total, "flagged": len(out),
               "high": sum(1 for x in out if x["tier"] == "high"),
               "medium": sum(1 for x in out if x["tier"] == "medium")}
    if a.json:
        print(json.dumps({"summary": summary, "claims": out}, indent=2, ensure_ascii=False))
    else:
        print(f"{summary['flagged']} of {summary['sentences']} sentences flagged "
              f"({summary['high']} high, {summary['medium']} medium)\n")
        for x in out:
            cite = "cited" if x["block_has_external_link"] else "no link"
            print(f"[{x['tier'].upper():6}] #{x['id']} ({', '.join(x['categories'])}; {cite}) {x['section']}\n    {x['sentence']}")


if __name__ == "__main__":
    sys.exit(main())
