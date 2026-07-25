#!/usr/bin/env python3
"""Image performance + static lead photos (SEO/AEO, Core Web Vitals).

Idempotent pass over all pages:
  - Breed hero <img id="dog-photo">: give it a real static src/alt (the first
    photo, matching showPhoto(0)) so the lead image is in static HTML, and
    fetchpriority="high" since it's the LCP element. NOT lazy-loaded.
  - Deep-dive <img class="narrative-img">: add loading="lazy" (below the fold)
    plus real width/height (from the file) to prevent layout shift (CLS).
  - Home hero <img id="dog-photo">: stays dynamic (date-based fact-of-the-day);
    just add fetchpriority="high".
  - Home logo: add width/height for aspect ratio.

Requires Pillow. Re-running is safe (attributes already present are left alone).
"""
import json
import re
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"
_cache = {}


def dims(filename):
    if filename in _cache:
        return _cache[filename]
    try:
        with Image.open(IMAGES / filename) as im:
            _cache[filename] = im.size  # (w, h)
    except Exception:
        _cache[filename] = None
    return _cache[filename]


def first_photo(src):
    m = re.search(r"const PHOTOS\s*=\s*(\[.*?\]);", src)
    if not m:
        return None
    try:
        arr = json.loads(m.group(1))
        return arr[0] if arr else None
    except Exception:
        return None


def process_breed(path):
    src = path.read_text(encoding="utf-8")
    if 'id="dog-photo"' not in src or 'fetchpriority' in src:
        return "skip"
    photo = first_photo(src)
    if not photo:
        return "skip (no photos)"
    file, cap = photo["file"], photo["caption"].replace('"', "&quot;")
    new = re.sub(
        r'<img id="dog-photo"[^>]*>',
        f'<img id="dog-photo" src="../images/{file}" alt="{cap}" '
        f'fetchpriority="high" />',
        src, count=1,
    )
    path.write_text(new, encoding="utf-8")
    return "hero set"


def process_deepdive(path):
    src = path.read_text(encoding="utf-8")
    if 'class="narrative-img"' not in src or 'loading="lazy"' in src:
        return "skip"

    def repl(m):
        file, alt = m.group(1), m.group(2)
        wh = dims(file)
        size = f' width="{wh[0]}" height="{wh[1]}"' if wh else ""
        return (f'<img class="narrative-img" src="../images/{file}" '
                f'alt="{alt}" loading="lazy"{size} />')

    new, n = re.subn(
        r'<img class="narrative-img" src="\.\./images/([^"]+)" alt="([^"]*)"\s*/?>',
        repl, src, count=1,
    )
    if n != 1:
        return "skip (pattern miss)"
    path.write_text(new, encoding="utf-8")
    return "narrative optimized"


def process_home(path):
    src = path.read_text(encoding="utf-8")
    changed = False
    # Hero: add fetchpriority only (stays dynamic).
    if 'id="dog-photo"' in src and "fetchpriority" not in src:
        src = re.sub(r'<img id="dog-photo"([^>]*?)\s*/?>',
                     r'<img id="dog-photo"\1 fetchpriority="high" />',
                     src, count=1)
        changed = True
    # Logo: add width/height for aspect ratio.
    m = re.search(r'<img src="images/([^"]+)" alt="([^"]*)"([^>]*)>', src)
    if m and "width=" not in m.group(0):
        wh = dims(m.group(1))
        if wh:
            src = src.replace(
                m.group(0),
                f'<img src="images/{m.group(1)}" alt="{m.group(2)}" '
                f'width="{wh[0]}" height="{wh[1]}"{m.group(3)}>',
                1,
            )
            changed = True
    if changed:
        path.write_text(src, encoding="utf-8")
        return "home optimized"
    return "skip"


def main():
    counts = {}
    def tally(r):
        k = "skip" if r.startswith("skip") else r
        counts[k] = counts.get(k, 0) + 1

    tally(process_home(ROOT / "index.html"))
    for f in sorted((ROOT / "breeds").glob("*.html")):
        if f.name != "index.html":
            tally(process_breed(f))
    for f in sorted((ROOT / "deep-dives").glob("*.html")):
        if f.name != "index.html":
            tally(process_deepdive(f))

    for k, v in sorted(counts.items()):
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
