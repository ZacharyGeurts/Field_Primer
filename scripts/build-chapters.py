#!/usr/bin/env python3
"""Build Field Technology v3 chapter HTML from manifest + v3 prose."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_bodies_v3 import CHAPTER_BODY  # noqa: E402
from social_meta import chapter_meta  # noqa: E402

MANIFEST = ROOT / "docs/data/image-manifest.json"
OUT = ROOT / "docs/chapters"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{num} — {title} · Field Technology v3</title>
{social_meta}
  <link rel="stylesheet" href="../css/field-primer.css" />
  <link rel="stylesheet" href="../css/chapters.css" />
</head>
<body class="chapter-page accent-{accent}">
  <nav class="top"><div class="inner">
    <a class="logo" href="../index.html">FIELD TECHNOLOGY <span class="v3-badge">v3</span></a>
    <ul>
      <li><a href="../index.html#axioms">Axioms</a></li>
      <li><a href="../gallery.html">Gallery</a></li>
      <li><a href="../index.html#chapters">Chapters</a></li>
      <li><a href="https://github.com/ZacharyGeurts/Field_Primer/wiki/{wiki}">Wiki</a></li>
    </ul>
  </div></nav>
  <header class="chapter-hero" style="background-image:url('../assets/images/{image}')">
    <div class="chapter-hero-overlay"></div>
    <div class="chapter-hero-content">
      <p class="eyebrow">Chapter {num} · Field Technology v3</p>
      <h1>{title}</h1>
    </div>
  </header>
  <main class="chapter-main">
    <nav class="chapter-nav">{prev_link} {next_link}</nav>
    {body}
    <nav class="chapter-nav bottom">{prev_link} {next_link}</nav>
  </main>
  <footer><p>Field Technology v3 · CC BY-NC-SA 4.0 · We do not hide the rocks.</p></footer>
</body>
</html>
"""


def nav_link(num: int, manifest: dict, direction: str) -> str:
    if direction == "prev":
        if num <= 1:
            return '<a class="btn secondary" href="../index.html">← Home</a>'
        prev = str(num - 1).zfill(2)
        ch = manifest["chapters"][prev]
        return f'<a class="btn secondary" href="{ch["slug"]}.html">← Ch {num - 1}</a>'
    if num >= 12:
        return '<a class="btn" href="../gallery.html">Gallery →</a>'
    nxt = str(num + 1).zfill(2)
    ch = manifest["chapters"][nxt]
    return f'<a class="btn" href="{ch["slug"]}.html">Ch {num + 1} →</a>'


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    for key, ch in manifest["chapters"].items():
        num = int(key)
        body = CHAPTER_BODY.get(key, "<p>See wiki for full prose.</p>")
        prev_link = nav_link(num, manifest, "prev")
        next_link = nav_link(num, manifest, "next")
        meta = chapter_meta(
            num,
            ch["title"],
            ch["slug"],
            ch["image"],
            ch.get("alt", ch["title"]),
        )
        html_out = TEMPLATE.format(
            num=num,
            title=html.escape(ch["title"]),
            accent=ch["accent"],
            wiki=ch["wiki"],
            image=ch["image"],
            body=body,
            prev_link=prev_link,
            next_link=next_link,
            social_meta=meta,
        )
        (OUT / f"{ch['slug']}.html").write_text(html_out, encoding="utf-8")
        print(f"wrote {ch['slug']}.html")
    print("done")


if __name__ == "__main__":
    main()