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

from master_rocks_table import master_rocks_index_rows  # noqa: E402
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
    "21": "Queen gates · Hostess 7 doctrine",
    "22": "Glossary · master rocks table",
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
        f'<a class="chapter-card" href="chapters/{slug}.html?reader=1">'
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
    """Index about section — honest operator-textbook positioning."""
    about_block = """          <p>
            v5 is a <strong>manuscript-grade operator textbook</strong> — full sentences, drills, honesty labels —
            not publisher-certified and not a marketing deck. Chapter 1 locks thesis, audience, and the operator map;
            Chapter 12 and the <a href="chapters/22-glossary.html#master-rocks">master rocks table</a> label every claim
            <span class="tag impl">Implemented</span>, <span class="tag meta">Metaphor</span>, <span class="tag phil">Philosophy</span>, or <span class="tag vis">Visual</span>.
            The engineering spine (Chapters 2–12, 19–21) stands alone; Love, God, and creditor tributes (16–18) are a
            <em>bracketed philosophical track</em> — optional, labeled, never smuggled into thermodynamic proofs.
          </p>
          <p>
            You will learn how AMOURANTHRTX treats GPU texels as addressable state, how NEXUS turns sockets into
            readable perimeter, how Queen holds browser gates when <code>QUEEN_READY</code> without amputating the web,
            and how KILROY seals Field Die discipline at the kernel boundary. Illustration follows Mayer density (~1 figure / 1,000 words).
            You will also learn what we <em>cannot</em> measure — proxy entropy is not joules; SDF plates are not fMRI — and we say so in place.
          </p>
          <p>
            Read Chapter 1 for thesis, operator map, and validation table. Read Chapter 12 before you treat a shader as a spectrum analyzer.
            Read Chapters 19–21 for sovereign time, public services, and Queen. Skip 16–18 if you want engineering only.
          </p>"""
    text = re.sub(
        r'<section id="about".*?</section>',
        f'<section id="about" class="v3-launch">\n      <div class="v3-launch-inner">\n        <div class="v3-copy">\n          <p class="eyebrow">What v5 is</p>\n          <h2>An operator textbook you can actually read</h2>\n{about_block}\n        </div>\n        <figure class="v3-covers">\n          <img src="assets/images/fabric-triple.jpg" alt="Phi Thermo Flow" loading="lazy" />\n          <img src="assets/images/field-die.jpg" alt="Field Die" loading="lazy" />\n        </figure>\n      </div>\n    </section>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    return text


def patch_hero_lead(text: str) -> str:
    lead = """        <strong>Twenty-two chapters of operator prose</strong> — manuscript-grade, honesty-labeled, grep-first.
        Engineering core on Phi, Thermo, Flow, Field Die, packet field, observability, sovereign time, and Queen.
        Sacred chapters (16–18) and creditor tributes sit beside the math — bracketed, not mixed into proofs. The rocks stay visible."""
    text = re.sub(
        r'<p class="lead">\s*.*?\s*</p>',
        f'<p class="lead">\n        {lead}\n      </p>',
        text,
        count=1,
        flags=re.DOTALL,
    )
    return text


READER_ROOM_START = "  <!-- reader-room -->"
READER_ROOM_END = "  <!-- /reader-room -->"

READER_ROOM_HTML = """  <!-- reader-room -->
  <section id="reader-room" class="reader-room" aria-labelledby="reader-room-heading">
    <div class="reader-room-inner">
      <div class="reader-room-copy">
        <p class="eyebrow">Schools · home · any device</p>
        <h2 id="reader-room-heading">Reading room — vanilla paper, your colors</h2>
        <p>
          Every chapter opens in <strong>full-screen reader mode</strong>: warm cream paper, brown ink, soft grain —
          like a textbook page, not a tech demo. Tap <strong>Read</strong> on any chapter, or start below.
          Customize paper, ink, accent, muted text, code blocks, typeface, and column width. Settings sync across chapters on this device.
        </p>
        <ul class="reader-room-features">
          <li>Works on phone, tablet, and desktop — large touch targets, bottom-sheet settings on mobile</li>
          <li><strong>Classroom</strong> preset: high-contrast cream paper for projectors and bright rooms</li>
          <li>Keyboard: <kbd>+</kbd>/<kbd>−</kbd> size, <kbd>Esc</kbd> exit</li>
        </ul>
        <div class="reader-room-cta">
          <a class="btn btn-reader-vanilla" href="chapters/01-preface.html?reader=1">Open Chapter 1 in reader</a>
          <a class="btn secondary" href="#chapters">Browse all 22 chapters</a>
        </div>
      </div>
      <div class="reader-preview-wrap" aria-hidden="true">
        <span class="reader-preview-label">Your paper</span>
        <div id="reader-room-preview">
          <p class="reader-preview-title">Field Technology v5</p>
          <p class="reader-preview-body">Reality is 3D. Time is linear. Energy can be moved.</p>
          <span class="reader-preview-muted">Caption and muted text</span>
          <code class="reader-preview-code">grep THERMO run.log</code>
        </div>
      </div>
    </div>
  </section>
  <!-- /reader-room -->"""


def patch_reader_room(text: str) -> str:
    if READER_ROOM_START in text:
        return re.sub(
            rf"{re.escape(READER_ROOM_START)}.*?{re.escape(READER_ROOM_END)}",
            READER_ROOM_HTML.strip(),
            text,
            count=1,
            flags=re.DOTALL,
        )
    return text.replace(
        "  </header>\n\n  <main>",
        "  </header>\n\n" + READER_ROOM_HTML + "\n\n  <main>",
        1,
    )


def patch_rocks_table(text: str) -> str:
    rows = master_rocks_index_rows().strip()
    return re.sub(
        r'(<section id="rocks">.*?<tbody>)\s*.*?\s*(</tbody>)',
        rf"\1\n{rows}\n        \2",
        text,
        count=1,
        flags=re.DOTALL,
    )


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    text = INDEX.read_text(encoding="utf-8")

    meta = social_meta(
        title="Field Technology v5 — Serious Book · Textbook of 2026",
        description=(
            "22-chapter operator textbook manuscript · honesty labels · operator map · master rocks table · "
            "Field Die · packet field · sovereign time · Queen. Reality is 3D. Time is linear. Energy can be moved."
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
    text = patch_hero_lead(text)
    text = patch_reader_room(text)
    text = patch_rocks_table(text)
    text = patch_reader_assets(text)
    text = patch_reader_cta(text)
    INDEX.write_text(text, encoding="utf-8")
    print(f"index.html updated — {len(chapter_keys(manifest))} chapter cards from manifest")


if __name__ == "__main__":
    main()