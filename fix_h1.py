#!/usr/bin/env python3
"""Fix heading hierarchy for SEO across BarkFacts pages.

Every page except the home page repeated the site name as the <h1>
("The Bark Facts") and demoted the real page topic (breed name / section
name) to an <h2>. Search engines treat the <h1> as the page's primary
subject, so each page should have ONE <h1> describing that page.

This script, for every page EXCEPT the root index.html:
  - turns the header site-name  <h1>The Bark Facts</h1>  into a
    non-heading  <div class="site-brand">…</div>  (visually identical), and
  - promotes the single topic <h2> (inside .breed-hero / .deep-hero /
    .page-heading) to an <h1>,
updating the matching CSS selectors so the look is unchanged.

The home page (index.html) already has a single correct <h1> and is left
untouched. Safe to re-run: pages already converted are skipped.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# CSS hero selectors whose <h2> becomes the page <h1>.
HERO_SELECTORS = (".breed-hero h2", ".deep-hero h2", ".page-heading h2")


def discover():
    files = []
    for section in ("breeds", "deep-dives"):
        files += sorted((ROOT / section).glob("*.html"))
    return [f for f in files if f.exists()]  # root index.html deliberately excluded


def convert(src: str) -> str:
    # 1. Header brand: <h1>The Bark Facts</h1> -> <div class="site-brand">…</div>
    src = re.sub(r"<h1>\s*The Bark Facts\s*</h1>",
                 '<div class="site-brand">The Bark Facts</div>', src)

    # 2. CSS: header h1 { ... }  ->  header .site-brand { ... }
    #    (covers the base rule and any responsive @media override)
    src = re.sub(r"header\s+h1(\s*\{)", r"header .site-brand\1", src)

    # 3. CSS hero selectors: ".breed-hero h2 {" -> ".breed-hero h1 {" etc.
    for sel in HERO_SELECTORS:
        src = src.replace(sel + " {", sel[:-2] + "h1 {")

    # 4. Markup: the single topic heading <h2 …>…</h2> -> <h1 …>…</h1>
    src = re.sub(r"<h2(\s[^>]*)?>", lambda m: "<h1" + (m.group(1) or "") + ">", src, count=1)
    src = src.replace("</h2>", "</h1>", 1)
    return src


def process(path: Path) -> str:
    src = path.read_text(encoding="utf-8")
    if 'class="site-brand"' in src:
        return "skip (already converted)"
    new = convert(src)
    # sanity: exactly one <h1> after conversion
    n_h1 = len(re.findall(r"<h1[ >]", new))
    if n_h1 != 1:
        return f"WARN: {n_h1} <h1> tags after conversion — NOT written"
    path.write_text(new, encoding="utf-8")
    return "converted"


def main():
    counts = {}
    for f in discover():
        r = process(f)
        counts[r] = counts.get(r, 0) + 1
        if r.startswith("WARN"):
            print(f"  {f.relative_to(ROOT)}: {r}")
    for k, v in counts.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
