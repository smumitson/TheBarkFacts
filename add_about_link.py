#!/usr/bin/env python3
"""Add the "About" link to the site nav on every page (idempotent).

Inserts <a href="{..}about.html">About</a> as the last item in the
.site-nav on all pages. Root pages use about.html; pages in breeds/ and
deep-dives/ use ../about.html. about.html itself already has the link.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent


def discover():
    files = [ROOT / "index.html"]
    for section in ("breeds", "deep-dives"):
        files += sorted((ROOT / section).glob("*.html"))
    return [f for f in files if f.exists()]


def process(path: Path) -> bool:
    src = path.read_text(encoding="utf-8")
    if 'about.html">About</a>' in src:
        return False  # already present
    prefix = "" if path.parent == ROOT else "../"
    link = f'  <a href="{prefix}about.html">About</a>\n</nav>'
    new, n = re.subn(r"</nav>", link, src, count=1)
    if n != 1:
        print(f"  ! no <nav> in {path.name}")
        return False
    path.write_text(new, encoding="utf-8")
    return True


def main():
    n = sum(process(f) for f in discover())
    print(f"Added About nav link to {n} pages")


if __name__ == "__main__":
    main()
