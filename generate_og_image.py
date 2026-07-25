#!/usr/bin/env python3
"""Generate the branded 1200x630 Open Graph share image.

Composes the site's brand card: paw glyph + "The Bark Facts" wordmark +
tagline on a brown field (matching the header), with the mascot cartoon
framed on the right. Output: images/og-cover.jpg (used as og:image on the
home + section-index pages).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
IMAGES = ROOT / "images"

W, H = 1200, 630
BROWN = (92, 61, 17)       # #5C3D11
ORANGE = (192, 86, 33)     # #C05621
ORANGE_L = (232, 134, 59)  # #E8863B
CREAM = (250, 240, 220)    # #FAF0DC
TAN = (228, 201, 160)      # muted cream for tagline

FONTS = "C:/Windows/Fonts/"
def font(name, size):
    return ImageFont.truetype(FONTS + name, size)

TAGLINE = "Real facts and honest takes on the dogs we love."

# Paw geometry (normalised), same mark as the favicon.
PAD = (0.50, 0.63, 0.22, 0.18)
TOES = [(0.265, 0.44, 0.085, 0.100), (0.425, 0.325, 0.093, 0.113),
        (0.585, 0.325, 0.093, 0.113), (0.745, 0.44, 0.085, 0.100)]


def draw_paw(d, cx, cy, size, color):
    def bean(c):
        nx, ny, nrx, nry = c
        x = cx - size / 2 + nx * size
        y = cy - size / 2 + ny * size
        rx, ry = nrx * size, nry * size
        d.ellipse([x - rx, y - ry, x + rx, y + ry], fill=color)
    bean(PAD)
    for t in TOES:
        bean(t)


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def rounded_thumb(src_path, box_w, box_h, radius, border, border_color):
    """Return an RGBA rounded-corner thumbnail with a border."""
    im = Image.open(src_path).convert("RGB")
    # cover-fit into box
    scale = max(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    left = (im.width - box_w) // 2
    top = (im.height - box_h) // 2
    im = im.crop((left, top, left + box_w, top + box_h)).convert("RGBA")
    mask = Image.new("L", (box_w, box_h), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, box_w - 1, box_h - 1],
                                           radius=radius, fill=255)
    im.putalpha(mask)
    # border layer
    out = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    bd = ImageDraw.Draw(out)
    bd.rounded_rectangle([0, 0, box_w - 1, box_h - 1], radius=radius,
                         fill=border_color)
    inner = im.resize((box_w - 2 * border, box_h - 2 * border), Image.LANCZOS)
    out.alpha_composite(inner, (border, border))
    return out


def main():
    img = Image.new("RGB", (W, H), BROWN)
    d = ImageDraw.Draw(img)

    # Right: mascot in a cream-bordered rounded frame.
    tw, th = 470, 470
    thumb = rounded_thumb(IMAGES / "the_bark_facts_2.jpg", tw, th, 28, 8, CREAM)
    img.paste(thumb, (W - tw - 60, (H - th) // 2), thumb)

    # Left column brand stack, vertically centered.
    lx, col_w = 72, 560
    f_title = font("georgiab.ttf", 88)
    f_tag = font("georgiai.ttf", 34)

    title_lines = ["The Bark", "Facts"]
    tag_lines = wrap(d, TAGLINE, f_tag, col_w)

    paw_sz = 92
    line_h = 96
    tag_h = 46
    gap1, gap2, gap3 = 26, 22, 26
    block_h = (paw_sz + gap1 + line_h * len(title_lines) + gap2 + 6
               + gap3 + tag_h * len(tag_lines))
    y = (H - block_h) // 2

    draw_paw(d, lx + paw_sz / 2, y + paw_sz / 2, paw_sz, ORANGE_L)
    y += paw_sz + gap1

    for ln in title_lines:
        d.text((lx, y), ln, font=f_title, fill=CREAM)
        y += line_h
    y += gap2

    d.rounded_rectangle([lx, y, lx + 200, y + 6], radius=3, fill=ORANGE)
    y += 6 + gap3

    for ln in tag_lines:
        d.text((lx, y), ln, font=f_tag, fill=TAN)
        y += tag_h

    # Bottom accent bar.
    d.rectangle([0, H - 12, W, H], fill=ORANGE)

    out = IMAGES / "og-cover.jpg"
    img.save(out, "JPEG", quality=90, optimize=True, progressive=True)
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size//1024} KB, {W}x{H})")


if __name__ == "__main__":
    main()
