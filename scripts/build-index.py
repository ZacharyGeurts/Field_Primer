#!/usr/bin/env python3
"""Sync docs/index.html chapter grid and copy with image-manifest + long book."""
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from social_meta import social_meta  # noqa: E402

INDEX = ROOT / "docs/index.html"
MANIFEST = ROOT / "docs/data/image-manifest.json"
MARKER_START = "  <!-- social-meta -->"
MARKER_END = "  <!-- /social-meta -->"
GRID_START = "      <!-- chapter-grid -->"
GRID_END = "      <!-- /chapter-grid -->"

CHAPTER_BLURBS: dict[str, str] = {
    "01": "Start here · illustration theory",
    "19": "SQUIDGIE · terror-threat posture",
    "20": "DNS · DHCP · NTP",
    "21": "Robot brain · SDF imaging · KILROY",
    "22": "Full glossary index",
}


def chapter_keys(manifest: dict) -> list[str]:
    return sorted(manifest["chapters"].keys(), key=lambda x: int(x))


def chapter_card(key: str, ch: dict) -> str:
    num = int(key)
    slug = ch["slug"]
    title = html.escape(ch["title"])
    img = html.escape(ch["image"])
    alt = html.escape(ch.get("alt", ""))
    blurb = CHAPTER_BLURBS.get(key, "")
    short = title.split(" — ", 1)[-1] if " — " in title else title
    if len(short) > 42:
        short = short[:39] + "…"
    p = f'<p>{html.escape(blurb)}</p>' if blurb else ""
    return (
        f'<a class="chapter-card" href="chapters/{slug}.html">'
        f'<img class="thumb" src="assets/images/{img}" alt="{alt}" loading="lazy" />'
        f'<span class="num">{num:02d}</span><h4>{short}</h4>{p}</a>'
    )


def build_chapter_grid(manifest: dict) -> str:
    lines = [GRID_START]
    for key in chapter_keys(manifest):
        lines.append("        " + chapter_card(key, manifest["chapters"][key]))
    lines.append("      " + GRID_END)
    return "\n".join(lines)


READER_CSS = '  <link rel="stylesheet" href="css/reader.css" />'
READER_JS = '  <script src="js/reader.js" defer></script>'


def patch_reader_assets(text: str) -> str:
    if 'href="css/reader.css"' not in text:
        text = text.replace(
            '  <link rel="stylesheet" href="css/chapters.css" />',
            '  <link rel="stylesheet" href="css/chapters.css" />\n' + READER_CSS,
            1,
        )
    if 'src="js/reader.js"' not in text:
        text = text.replace("</body>", READER_JS + "\n</body>", 1)
    return text


def patch_reader_cta(text: str) -> str:
    pairs = (
        ('href="chapters/01-preface.html">Start Chapter 1', 'href="chapters/01-preface.html?reader=1">Start Chapter 1'),
        ('href="chapters/01-preface.html" class="btn">Read Chapter 1', 'href="chapters/01-preface.html?reader=1" class="btn">Read Chapter 1'),
    )
    for old, new in pairs:
        if old in text and new not in text:
            text = text.replace(old, new)
    return text


def patch_about_copy(text: str) -> str:
    """Ensure index about section matches long-book edition."""
    old_snippet = (
        "Illustration follows Leonardo-to-Mayer theory: about <strong>one signaled figure per 1,000 words</strong> "
        "— mechanism, not wallpaper."
    )
    new_snippet = (
        "Illustration follows Leonardo-through-Mayer theory (Chapter 1): about <strong>one signaled figure per 1,000 words</strong> "
        "— mechanism, not wallpaper. Queen’s in-process robot brain runs Hostess 7: she folds prose to <strong>SDF brain-imaging plates</strong> "
        "and recalls them through neural Super Intelligence — same density standard, two surfaces (web reader + Hostess storage)."
    )
    if old_snippet in text:
        text = text.replace(old_snippet, new_snippet)
    queen_line = (
        "how Queen holds every browser gate without amputating the web, and how KILROY seals"
    )
    queen_replacement = (
        "how Queen’s DARPA robot brain holds every browser gate without amputating the web, how Hostess 7 owns SDF self-storage, and how KILROY seals"
    )
    if queen_line in text and queen_replacement not in text:
        text = text.replace(queen_line, queen_replacement)
    return text


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    text = INDEX.read_text(encoding="utf-8")

    meta = social_meta(
        title="Field Technology v5 — Serious Book · Textbook of 2026",
        description=(
            "22 long-form chapters · illustration theory · Queen robot brain · Hostess 7 SDF imaging · "
            "Field Die · packet field · sovereign time · KILROY. Reality is 3D. Time is linear. Energy can be moved."
        ),
        url="https://zacharygeurts.github.io/Field_Primer/",
        image_alt="Field Technology v5 — Serious Book cover and axioms",
        path_prefix="",
    )
    block = f"{MARKER_START}\n{meta}\n{MARKER_END}"
    if MARKER_START not in text:
        raise SystemExit("index.html missing social-meta markers")
    text = re.sub(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        block,
        text,
        count=1,
        flags=re.DOTALL,
    )

    if GRID_START not in text:
        raise SystemExit("index.html missing chapter-grid markers")
    grid = build_chapter_grid(manifest)
    text = re.sub(
        rf"{re.escape(GRID_START)}.*?{re.escape(GRID_END)}",
        grid,
        text,
        count=1,
        flags=re.DOTALL,
    )

    text = patch_about_copy(text)
    text = patch_reader_assets(text)
    text = patch_reader_cta(text)
    INDEX.write_text(text, encoding="utf-8")
    print(f"index.html updated — {len(chapter_keys(manifest))} chapter cards from manifest")


if __name__ == "__main__":
    main()