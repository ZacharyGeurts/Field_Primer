#!/usr/bin/env python3
"""Inject shared social meta into docs/index.html."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from social_meta import social_meta  # noqa: E402

INDEX = ROOT / "docs/index.html"
MARKER_START = "  <!-- social-meta -->"
MARKER_END = "  <!-- /social-meta -->"


def main() -> None:
    text = INDEX.read_text(encoding="utf-8")
    meta = social_meta(
        title="Field Technology v4 — Textbook of 2026",
        description=(
            "18 chapters. Creditor tributes. Love and God beside the math. "
            "Reality is 3D. Time is linear. Energy can be moved."
        ),
        url="https://zacharygeurts.github.io/Field_Primer/",
        image_alt="Field Technology v4 — Textbook of 2026 cover and axioms",
        path_prefix="",
    )
    block = f"{MARKER_START}\n{meta}\n{MARKER_END}"
    if MARKER_START not in text:
        raise SystemExit("index.html missing social-meta markers — add them after <title>")
    text = re.sub(
        rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}",
        block,
        text,
        count=1,
        flags=re.DOTALL,
    )
    INDEX.write_text(text, encoding="utf-8")
    print("index.html social meta updated")


if __name__ == "__main__":
    main()