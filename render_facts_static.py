#!/usr/bin/env python3
"""Pre-render breed facts into static HTML (SEO/AEO).

Breed pages built their fact cards client-side from a `const FACTS = [...]`
array via `FACTS.forEach(...)`, so the fact text was invisible to crawlers
and AI answer engines that don't run JavaScript.

This script rewrites each breeds/*.html so the fact cards are present in the
static HTML exactly as the JS produced them, then removes the now-redundant
FACTS array and render loop. The photo-carousel JS is left untouched.

Idempotent: pages already converted (no `FACTS.forEach`) are skipped.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).parent


def card_html(fact, tag):
    """One fact card, matching the exact markup the JS generated."""
    return (
        '    <div class="fact-card">\n'
        f'      <div class="fact-number">Fact #{fact["fact_number"]}</div>\n'
        f'      <div class="fact-category">{fact["category"]}</div>\n'
        f'      <div class="fact-text">{fact["fact"]}</div>\n'
        f'      <div class="fact-footer"><span class="fact-breed-tag">{tag}</span></div>\n'
        '    </div>'
    )


def process(path: Path):
    src = path.read_text(encoding="utf-8")
    if "FACTS.forEach" not in src:
        return "skip (already static)"

    # Breed-tag text is the literal used inside the JS template.
    m_tag = re.search(r'fact-breed-tag">([^<]*)</span>', src)
    tag = m_tag.group(1) if m_tag else path.stem.replace("-", " ")

    # The FACTS array lives on a single line; capture it without crossing lines.
    m_facts = re.search(r"const FACTS\s*=\s*(\[.*\]);", src)
    if not m_facts:
        return "WARN: FACTS array not found — skipped"
    try:
        facts = json.loads(m_facts.group(1))
    except Exception as e:
        return f"WARN: FACTS JSON parse failed ({e}) — skipped"

    cards = "\n".join(card_html(f, tag) for f in facts)

    # 1. Inject the static cards into the (currently empty) facts container.
    new, n = re.subn(
        r'<div id="facts-section">\s*</div>',
        '<div id="facts-section">\n' + cards + "\n  </div>",
        src, count=1,
    )
    if n != 1:
        return "WARN: empty #facts-section not found — skipped"
    src = new

    # 2. Remove the JS render loop (const section … forEach … });).
    src = re.sub(
        r"\n\s*const section = document\.getElementById\('facts-section'\);"
        r"[\s\S]*?\}\);",
        "", src, count=1,
    )

    # 3. Remove the now-unused FACTS array declaration line.
    src = re.sub(r"\n\s*const FACTS\s*=\s*\[.*\];", "", src, count=1)

    path.write_text(src, encoding="utf-8")
    return f"rendered {len(facts)} facts"


def main():
    counts = {}
    for f in sorted((ROOT / "breeds").glob("*.html")):
        if f.name == "index.html":
            continue
        r = process(f)
        key = r if r.startswith(("skip", "WARN")) else "rendered"
        counts[key] = counts.get(key, 0) + 1
        if r.startswith("WARN"):
            print(f"  {f.name}: {r}")
    for k, v in counts.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
