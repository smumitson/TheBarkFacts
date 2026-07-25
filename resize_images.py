#!/usr/bin/env python3
"""Resize oversized images for web (performance / Core Web Vitals).

Source photos are full-resolution (mostly 4000-6500px, ~1.7MB avg) but are
displayed at 150-380px. This caps the long edge at MAX_EDGE and re-encodes as
optimized progressive JPEG, baking in EXIF orientation and stripping metadata.

Only images whose long edge exceeds MAX_EDGE are touched, so re-running is safe
(no repeated re-encoding / generation loss). Overwrites in place — originals
are assumed backed up elsewhere.
"""
import os
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"
MAX_EDGE = 1200
QUALITY = 82


def collect():
    files = []
    for ext in ("*.jpg", "*.jpeg", "*.JPG", "*.JPEG"):
        files += IMAGES.glob(ext)
    return sorted(set(files))


def main():
    files = collect()
    before = after = 0
    resized = skipped = failed = 0

    for f in files:
        orig_bytes = f.stat().st_size
        before += orig_bytes
        try:
            with Image.open(f) as im:
                im = ImageOps.exif_transpose(im)      # bake orientation
                w, h = im.size
                if max(w, h) <= MAX_EDGE:
                    after += orig_bytes
                    skipped += 1
                    continue
                if im.mode != "RGB":
                    im = im.convert("RGB")
                scale = MAX_EDGE / max(w, h)
                new_size = (round(w * scale), round(h * scale))
                im = im.resize(new_size, Image.LANCZOS)
                im.save(f, "JPEG", quality=QUALITY, optimize=True,
                        progressive=True)
            after += f.stat().st_size
            resized += 1
        except Exception as e:
            after += orig_bytes
            failed += 1
            print(f"  FAIL {f.name}: {e}")

    mb = 1048576
    print(f"\nImages:  {len(files)}")
    print(f"Resized: {resized}   Skipped (already <= {MAX_EDGE}px): {skipped}   Failed: {failed}")
    print(f"Total:   {before/mb:.1f} MB  ->  {after/mb:.1f} MB  "
          f"({(1 - after/before)*100:.0f}% smaller)")


if __name__ == "__main__":
    main()
