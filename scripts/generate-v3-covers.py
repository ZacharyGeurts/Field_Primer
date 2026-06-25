#!/usr/bin/env python3
"""Field Technology v3 — book covers, OG card, axiom banner."""
from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
MEME_SWORDS = ROOT / "assets/images/v3/meme-ref/Swords.jpg"
MEME_WANDS = ROOT / "assets/images/v3/meme-ref/Wands.jpg"
HERO = ROOT / "assets/images/field-primer-hero.jpg"

COVER_SIZE = (1800, 2700)
OG_SIZE = (1200, 630)
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

AXIOMS = (
    "Reality is 3D.",
    "Time is linear.",
    "Energy can be moved.",
)


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def cover_crop(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    sw, sh = img.size
    scale = max(tw / sw, th / sh)
    resized = img.resize((int(sw * scale), int(sh * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - tw) // 2
    top = (resized.height - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def gradient_bg(size: tuple[int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size, (4, 8, 16))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(int(4 + 14 * t), int(8 + 28 * t), int(16 + 52 * t)))
    return img


def blend_base(size: tuple[int, int], sources: list[Path], opacities: list[float]) -> Image.Image:
    base = gradient_bg(size).convert("RGBA")
    for src, op in zip(sources, opacities):
        if not src.exists():
            continue
        layer = cover_crop(Image.open(src).convert("RGB"), size).convert("RGBA")
        layer.putalpha(int(255 * op))
        base = Image.alpha_composite(base, layer)
    return base.convert("RGB")


def draw_axiom_strip(draw: ImageDraw.ImageDraw, y: int, w: int, margin: int, font: ImageFont.FreeTypeFont) -> int:
    colors = [(56, 189, 248), (240, 208, 96), (167, 139, 250)]
    x = margin
    for axiom, color in zip(AXIOMS, colors):
        bb = font.getbbox(axiom)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]
        pad = 14
        draw.rounded_rectangle((x, y, x + tw + pad * 2, y + th + pad * 2), radius=10, outline=color, width=2)
        draw.text((x + pad, y + pad - 2), axiom, font=font, fill=color)
        x += tw + pad * 2 + 20
    return y + 56


def draw_front() -> Image.Image:
    w, h = COVER_SIZE
    img = blend_base(COVER_SIZE, [MEME_SWORDS, HERO], [0.42, 0.22])
    overlay = Image.new("RGBA", COVER_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(h):
        t = y / h
        alpha = int(60 + 210 * max(0, (t - 0.3) / 0.7) ** 1.1)
        draw.line([(0, y), (w, y)], fill=(4, 8, 16, alpha))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)

    margin = 120
    draw.rectangle((0, 0, 32, h), fill=(167, 139, 250))
    draw.rectangle((0, h // 4, 32, h // 4 + 200), fill=(240, 208, 96))

    mono = load_font(FONT_MONO, 20)
    draw.text((margin, margin), "SOVEREIGN FIELD TECHNOLOGY", font=mono, fill=(56, 189, 248))
    draw.rectangle((margin, margin + 30, margin + 220, margin + 34), fill=(56, 189, 248))

    ax_font = load_font(FONT_MONO, 22)
    draw_axiom_strip(draw, margin + 52, w, margin, ax_font)

    title_font = load_font(FONT_BOLD, 108)
    v3_font = load_font(FONT_BOLD, 96)
    y = h - margin - 600
    draw.text((margin, y), "FIELD", font=title_font, fill=(232, 242, 255))
    y += 108
    draw.text((margin, y), "TECHNOLOGY", font=title_font, fill=(240, 208, 96))
    tech_w = title_font.getbbox("TECHNOLOGY")[2] - title_font.getbbox("TECHNOLOGY")[0]
    v3_bb = v3_font.getbbox("v3")
    vx = margin + tech_w + 32
    vy = y + 8
    pad = 20
    draw.rounded_rectangle(
        (vx, vy, vx + v3_bb[2] - v3_bb[0] + pad * 2, vy + v3_bb[3] - v3_bb[1] + pad * 2),
        radius=16,
        fill=(12, 24, 48),
        outline=(167, 139, 250),
        width=4,
    )
    draw.text((vx + pad, vy + pad - 6), "v3", font=v3_font, fill=(167, 139, 250))

    sub = load_font(FONT_BOLD, 56)
    y += 128
    draw.text((margin, y), "Offense. Defense. Operator Truth.", font=sub, fill=(232, 242, 255))
    body = load_font(FONT_REG, 28)
    y += 72
    draw.text((margin, y), "The greatest weapon is field literacy you already carry.", font=body, fill=(138, 164, 200))
    y += 44
    draw.text((margin, y), "Zachary Robert Geurts", font=load_font(FONT_REG, 34), fill=(232, 242, 255))

    credit = load_font(FONT_MONO, 16)
    draw.text((margin, h - margin - 24), "AMOURANTHRTX  |  NEXUS-Shield  |  memes corpus honored", font=credit, fill=(100, 130, 170))
    return img.convert("RGB")


def wrap(text: str, font: ImageFont.FreeTypeFont, width: int) -> list[str]:
    words, lines, cur = text.split(), [], []
    for word in words:
        trial = " ".join(cur + [word])
        if font.getbbox(trial)[2] - font.getbbox(trial)[0] <= width:
            cur.append(word)
        else:
            if cur:
                lines.append(" ".join(cur))
            cur = [word]
    if cur:
        lines.append(" ".join(cur))
    return lines


def draw_back() -> Image.Image:
    w, h = COVER_SIZE
    img = blend_base(COVER_SIZE, [MEME_WANDS, HERO], [0.38, 0.2])
    overlay = Image.new("RGBA", COVER_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(h):
        draw.line([(0, y), (w, y)], fill=(4, 8, 16, int(90 + 150 * y / h)))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    margin = 140
    max_w = w - margin * 2
    head = load_font(FONT_BOLD, 40)
    body = load_font(FONT_REG, 26)
    small = load_font(FONT_REG, 22)
    mono = load_font(FONT_MONO, 18)
    y = margin

    draw.text((margin, y), "SUBTEXT — THREE AXIOMS", font=head, fill=(240, 208, 96))
    y += 58
    for ax in AXIOMS:
        draw.text((margin, y), f"• {ax}", font=body, fill=(56, 189, 248))
        y += 36
    y += 20
    blurb = (
        "Field Technology v3 is the serious manual: the offensive and defensive weapon "
        "is not a gadget you order — it is reading continuous state, imposing boundary "
        "conditions, and refusing to surrender the verdict. We do not hide the rocks."
    )
    for line in wrap(blurb, body, max_w):
        draw.text((margin, y), line, font=body, fill=(200, 220, 245))
        y += 34
    y += 24
    draw.text((margin, y), "THE ROCKS (WE SAY THEM OUT LOUD)", font=head, fill=(245, 158, 11))
    y += 54
    rocks = [
        "Packet field = local sockets + heuristics, not global omniscience",
        "Landauer in-engine = proxy integral, not lab calorimetry",
        "Planetary RF weave = visual shader, not spectrum instrumentation",
        "Metaphors are labeled — grep beats marketing",
    ]
    for rock in rocks:
        for line in wrap(rock, small, max_w):
            draw.text((margin, y), line, font=small, fill=(138, 164, 200))
            y += 30
    y += 28
    draw.text((margin, y), "MEME CORPUS", font=head, fill=(167, 139, 250))
    y += 50
    meme_note = "Visual language drawn from ZacharyGeurts/memes — tarot suits, operator culture, alchemical cards. Honored, not hidden."
    for line in wrap(meme_note, small, max_w):
        draw.text((margin, y), line, font=small, fill=(180, 200, 230))
        y += 30
    y = h - margin - 100
    draw.text((margin, y), "zacharygeurts.github.io/Field_Primer", font=mono, fill=(56, 189, 248))
    y += 28
    draw.text((margin, y), "CC BY-NC-SA 4.0", font=small, fill=(100, 130, 170))
    return img.convert("RGB")


def draw_og() -> Image.Image:
    w, h = OG_SIZE
    img = blend_base(OG_SIZE, [MEME_SWORDS, HERO], [0.45, 0.25])
    overlay = Image.new("RGBA", OG_SIZE, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    for y in range(h):
        t = y / h
        draw.line([(0, y), (w, y)], fill=(4, 8, 16, int(40 + 180 * max(0, (t - 0.35) / 0.65))))
    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    draw = ImageDraw.Draw(img)
    m = 56
    draw.text((m, m), "FIELD TECHNOLOGY v3", font=load_font(FONT_BOLD, 52), fill=(240, 208, 96))
    draw.text((m, m + 62), "Reality is 3D · Time is linear · Energy can be moved", font=load_font(FONT_REG, 22), fill=(200, 220, 245))
    draw.text((m, h - m - 36), "Offense. Defense. Operator truth. We do not hide the rocks.", font=load_font(FONT_REG, 20), fill=(138, 164, 200))
    return img.convert("RGB")


def main() -> None:
    for base in (ROOT / "assets/images/v3", ROOT / "docs/assets/images/v3"):
        base.mkdir(parents=True, exist_ok=True)
    front, back, og = draw_front(), draw_back(), draw_og()
    pairs = [
        ("field-technology-v3-cover-front.jpg", front),
        ("field-technology-v3-cover-back.jpg", back),
        ("field-technology-v3-cover-spread.jpg", Image.new("RGB", (COVER_SIZE[0] * 2 + 8, COVER_SIZE[1]), (20, 30, 50))),
    ]
    spread = pairs[2][1]
    spread.paste(back, (0, 0))
    spread.paste(front, (COVER_SIZE[0] + 8, 0))
    for folder in (ROOT / "assets/images/v3", ROOT / "docs/assets/images/v3"):
        for name, im in pairs:
            im.save(folder / name, "JPEG", quality=93, optimize=True)
    og.save(ROOT / "assets/images/og-image.jpg", "JPEG", quality=92, optimize=True)
    og.save(ROOT / "docs/assets/images/og-image.jpg", "JPEG", quality=92, optimize=True)
    og.save(ROOT / ".github/social-preview.png", "PNG", optimize=True)
    print("v3 covers + og written")


if __name__ == "__main__":
    main()