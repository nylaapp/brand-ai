#!/usr/bin/env python3
"""WCAG 2.x contrast for foreground:background pairs.

  python contrast.py "#ffffff:#c93d0d" "#c93d0d:#111B18" [--label "button text,accent on dark"]

Prints ratio and AA pass/fail for normal text (4.5:1) and large text / UI (3:1). Exit 1 if any pair fails 3:1.
Standard library only.
"""
import sys


def lum(hex_color: str) -> float:
    h = hex_color.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise ValueError(f"not a hex colour: {hex_color}")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    r, g, b = out
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg: str, bg: str) -> float:
    a, b = sorted((lum(fg), lum(bg)), reverse=True)
    return (a + 0.05) / (b + 0.05)


def main(argv):
    labels = []
    if "--label" in argv:
        i = argv.index("--label")
        labels = [s.strip() for s in argv[i + 1].split(",")]
        argv = argv[:i] + argv[i + 2:]
    if not argv:
        sys.exit(__doc__)
    worst_fail = False
    print(f"{'pair':<22} {'ratio':>6}  normal  large  label")
    for n, pair in enumerate(argv):
        fg, bg = pair.split(":")
        r = ratio(fg, bg)
        normal = "PASS" if r >= 4.5 else "fail"
        large = "PASS" if r >= 3 else "fail"
        if r < 3:
            worst_fail = True
        label = labels[n] if n < len(labels) else ""
        print(f"{fg}:{bg:<14} {r:6.2f}  {normal:<6}  {large:<5}  {label}")
    sys.exit(1 if worst_fail else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
