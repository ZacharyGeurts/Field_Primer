#!/usr/bin/env python3
"""Field Technology v4 OG + social card."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OG_SIZE = (1200, 630)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MATH = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def load_font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def science_bg(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, (8, 14, 28))
    draw = ImageDraw.Draw(img)
    for x in range(0, w, 36):
        draw.line([(x, 0), (x, h)], fill=(18, 30, 52))
    for y in range(0, h, 36):
        draw.line([(0, y), (w, y)], fill=(18, 30, 52))
    for k in range(6):
        pts = []
        for i in range(0, w, 10):
            pts.append((i, int(h * 0.35 + math.sin(i / 80 + k) * h * 0.12)))
        draw.line(pts, fill=(167, 139, 250) if k % 2 else (56, 189, 248), width=2)
    return img


def main() -> None:
    w, h = OG_SIZE
    img = science_bg(OG_SIZE)
    overlay = Image.new("RGBA", OG_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(8, 14, 28, int(60 + 170 * max(0, (t - 0.3) / 0.7))))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    m = 56
    draw.text((m, m), "FIELD TECHNOLOGY v4", font=load_font(FONT_BOLD, 46), fill=(240, 208, 96))
    draw.text((m, m + 54), "18 chapters · Creditor tributes · Us & God", font=load_font(FONT_REG, 19), fill=(200, 220, 245))
    draw.text((m, m + 86), "Truth · Math · Existence", font=load_font(FONT_MATH, 18), fill=(56, 189, 248))
    draw.text((m, h - m - 32), "zacharygeurts.github.io/Field_Primer", font=load_font(FONT_MATH, 16), fill=(138, 164, 200))
    og = img.convert("RGB")
    og.save(ROOT / "assets/images/og-image.jpg", "JPEG", quality=92, optimize=True)
    og.save(ROOT / "docs/assets/images/og-image.jpg", "JPEG", quality=92, optimize=True)
    og.save(ROOT / ".github/social-preview.png", "PNG", optimize=True)
    print("v4 og written")


if __name__ == "__main__":
    main()