#!/usr/bin/env python3
"""Generate sitemap.xml for TheBarkFacts.

Walks the site's HTML files, derives canonical URLs, and writes a
sitemap using each file's last git commit date as <lastmod>.
Re-run this whenever pages are added or updated.
"""
import subprocess
import datetime
from pathlib import Path

DOMAIN = "https://thebarkfacts.com"
ROOT = Path(__file__).parent

# Priority / changefreq rules by location.
def meta_for(rel: str):
    if rel == "":                       # home page
        return "1.0", "weekly"
    if rel.endswith("/"):               # section index pages
        return "0.9", "weekly"
    if rel.startswith("breeds/"):
        return "0.8", "monthly"
    if rel.startswith("deep-dives/"):
        return "0.8", "monthly"
    if rel.startswith("Rankings/"):
        return "0.8", "monthly"
    return "0.7", "monthly"


def git_lastmod(path: Path) -> str:
    """Last commit date (YYYY-MM-DD) for a file; falls back to mtime."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path.relative_to(ROOT))],
            cwd=ROOT, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.fromtimestamp(path.stat().st_mtime).isoformat()


def canonical_url(path: Path) -> str:
    """Map a file to its canonical public URL."""
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return DOMAIN + "/", ""
    if rel.endswith("/index.html"):
        d = rel[: -len("index.html")]     # e.g. "breeds/"
        return DOMAIN + "/" + d, d
    return DOMAIN + "/" + rel, rel


def discover():
    files = [ROOT / "index.html", ROOT / "about.html"]
    for section in ("breeds", "deep-dives", "Rankings"):
        files += sorted((ROOT / section).glob("*.html"))
    return [f for f in files if f.exists()]


def main():
    entries = []
    for f in discover():
        loc, rel = canonical_url(f)
        prio, freq = meta_for(rel)
        entries.append((loc, git_lastmod(f), freq, prio))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, freq, prio in entries:
        lines += [
            "  <url>",
            f"    <loc>{loc}</loc>",
            f"    <lastmod>{lastmod}</lastmod>",
            f"    <changefreq>{freq}</changefreq>",
            f"    <priority>{prio}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(entries)} URLs")


if __name__ == "__main__":
    main()
