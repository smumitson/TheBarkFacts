#!/usr/bin/env python3
"""Add a "Breed Rankings" link to the site nav on every existing page.

Inserts the link right before the "About" nav item, matching each page's own
relative path prefix (root pages use "", subdir pages use "../"). Idempotent:
skips any file that already has the link. Does not touch the Rankings/ pages,
which are generated with the link already in place.

Run once after build_rankings.py. Safe to re-run.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Matches the About nav anchor and captures its relative prefix ("" or "../").
ABOUT_RE = re.compile(r'( *)(<a href="((?:\.\./)?)about\.html")')


def targets():
    files = [ROOT / "index.html", ROOT / "about.html"]
    for section in ("breeds", "deep-dives"):
        files += sorted((ROOT / section).glob("*.html"))
    return [f for f in files if f.exists()]


def add_link(html: str) -> str | None:
    if "Breed Rankings" in html:
        return None  # already done

    def repl(m):
        indent, about_anchor, prefix = m.group(1), m.group(2), m.group(3)
        link = f'{indent}<a href="{prefix}Rankings/index.html">Breed Rankings</a>\n'
        return f"{link}{indent}{about_anchor}"

    new, n = ABOUT_RE.subn(repl, html, count=1)
    return new if n else None


def main():
    changed = skipped = missed = 0
    for f in targets():
        html = f.read_text(encoding="utf-8")
        result = add_link(html)
        if result is None:
            if "Breed Rankings" in html:
                skipped += 1
            else:
                missed += 1
                print(f"  ! no About nav anchor found in {f.relative_to(ROOT)}")
            continue
        f.write_text(result, encoding="utf-8")
        changed += 1
    print(f"Updated {changed} file(s), skipped {skipped} already-done, {missed} missed.")


if __name__ == "__main__":
    main()
