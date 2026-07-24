#!/usr/bin/env python3
"""Generate the BarkFacts favicon set (paw print, brand palette).

Draws a paw print on a rounded brown tile at high resolution, then exports:
  favicon.ico            (16/32/48 multi-size, for tabs + Google)
  favicon-16.png, -32.png
  apple-touch-icon.png   (180, iOS home screen)
  icon-192.png, icon-512.png (Android / PWA)
  favicon.svg            (crisp vector for modern browsers)
  site.webmanifest       (tells phones which icons to use)

Re-run any time to regenerate. Requires Pillow.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).parent

BROWN = (92, 61, 17, 255)     # #5C3D11 tile
ORANGE = (232, 134, 59, 255)  # #E8863B paw
MASTER = 1024                 # supersampled master canvas

# Paw geometry in normalised (0..1) coordinates: main pad + four toe beans.
PAD = (0.50, 0.63, 0.22, 0.18)          # cx, cy, rx, ry
TOES = [                                 # cx, cy, rx, ry
    (0.265, 0.44, 0.085, 0.100),
    (0.425, 0.325, 0.093, 0.113),
    (0.585, 0.325, 0.093, 0.113),
    (0.745, 0.44, 0.085, 0.100),
]


def ellipse(draw, c, S, fill):
    cx, cy, rx, ry = c
    draw.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                 fill=fill)


def draw_master(bg=True) -> Image.Image:
    S = MASTER
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if bg:
        d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(0.22 * S), fill=BROWN)
    ellipse(d, PAD, S, ORANGE)
    for toe in TOES:
        ellipse(d, toe, S, ORANGE)
    return img


def export_png(master, size, name):
    master.resize((size, size), Image.LANCZOS).save(ROOT / name)
    print(f"  {name} ({size}px)")


def export_ico(master):
    master.save(ROOT / "favicon.ico",
                sizes=[(16, 16), (32, 32), (48, 48)])
    print("  favicon.ico (16/32/48)")


def export_svg():
    def circ(c):
        cx, cy, rx, ry = c
        return (f'<ellipse cx="{cx*64:.2f}" cy="{cy*64:.2f}" '
                f'rx="{rx*64:.2f}" ry="{ry*64:.2f}" fill="#E8863B"/>')
    beans = "".join(circ(PAD) if i == 0 else circ(t)
                    for i, t in enumerate([PAD] + TOES))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">'
        '<rect width="64" height="64" rx="14" fill="#5C3D11"/>'
        f'{beans}</svg>\n'
    )
    (ROOT / "favicon.svg").write_text(svg, encoding="utf-8")
    print("  favicon.svg")


def export_manifest():
    manifest = '''{
  "name": "The Bark Facts",
  "short_name": "Bark Facts",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ],
  "theme_color": "#5C3D11",
  "background_color": "#FAF0DC",
  "display": "standalone"
}
'''
    (ROOT / "site.webmanifest").write_text(manifest, encoding="utf-8")
    print("  site.webmanifest")


def main():
    master = draw_master()
    print("Generating favicon set:")
    export_ico(master)
    export_png(master, 16, "favicon-16.png")
    export_png(master, 32, "favicon-32.png")
    export_png(master, 180, "apple-touch-icon.png")
    export_png(master, 192, "icon-192.png")
    export_png(master, 512, "icon-512.png")
    export_svg()
    export_manifest()
    # A quick preview strip so we can eyeball the small sizes.
    strip = Image.new("RGBA", (16 + 32 + 48 + 8 * 3, 48), (250, 240, 220, 255))
    x = 0
    for s in (16, 32, 48):
        strip.paste(master.resize((s, s), Image.LANCZOS), (x, 48 - s), master.resize((s, s), Image.LANCZOS))
        x += s + 8
    strip.save(ROOT / "_favicon_preview.png")
    print("  _favicon_preview.png (tmp, small-size eyeball)")


if __name__ == "__main__":
    main()
