#!/usr/bin/env python3
"""Build Field Technology v4 chapter HTML."""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from chapter_bodies_v4 import CHAPTER_BODY  # noqa: E402
from social_meta import chapter_meta  # noqa: E402

MANIFEST = ROOT / "docs/data/image-manifest.json"
OUT = ROOT / "docs/chapters"

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{num} — {title} · Field Technology v4</title>
{social_meta}
  <link rel="stylesheet" href="../css/field-primer.css" />
  <link rel="stylesheet" href="../css/chapters.css" />
</head>
<body class="chapter-page accent-{accent}">
  <nav class="top"><div class="inner">
    <a class="logo" href="../index.html">FIELD TECHNOLOGY <span class="v4-badge">v4</span></a>
    <ul>
      <li><a href="../creditors/index.html">Creditors</a></li>
      <li><a href="../index.html#love-god">Love &amp; God</a></li>
      <li><a href="../index.html#chapters">Chapters</a></li>
      <li><a href="https://github.com/ZacharyGeurts/Field_Primer/wiki/{wiki}">Wiki</a></li>
    </ul>
  </div></nav>
  <header class="chapter-hero" style="background-image:url('../assets/images/{image}')">
    <div class="chapter-hero-overlay"></div>
    <div class="chapter-hero-content">
      <p class="eyebrow">Chapter {num} · Field Technology v4</p>
      <h1>{title}</h1>
    </div>
  </header>
  <main class="chapter-main">
    <nav class="chapter-nav">{prev_link} {next_link}</nav>
    {body}
    <nav class="chapter-nav bottom">{prev_link} {next_link}</nav>
  </main>
  <footer><p>Field Technology v4 · With love · We do not hide the rocks.</p></footer>
</body>
</html>
"""


def chapter_keys(manifest: dict) -> list[str]:
    return sorted(manifest["chapters"].keys(), key=lambda x: int(x))


def nav_link(num: int, keys: list[str], manifest: dict, direction: str) -> str:
    key = str(num).zfill(2)
    idx = keys.index(key)
    if direction == "prev":
        if idx <= 0:
            return '<a class="btn secondary" href="../index.html">← Home</a>'
        prev_key = keys[idx - 1]
        ch = manifest["chapters"][prev_key]
        return f'<a class="btn secondary" href="{ch["slug"]}.html">← Ch {int(prev_key)}</a>'
    if idx >= len(keys) - 1:
        return '<a class="btn" href="../creditors/love-and-god.html">Love &amp; God →</a>'
    nxt_key = keys[idx + 1]
    ch = manifest["chapters"][nxt_key]
    return f'<a class="btn" href="{ch["slug"]}.html">Ch {int(nxt_key)} →</a>'


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    keys = chapter_keys(manifest)
    OUT.mkdir(parents=True, exist_ok=True)
    for key in keys:
        ch = manifest["chapters"][key]
        num = int(key)
        body = CHAPTER_BODY.get(key, "<p>See wiki for full prose.</p>")
        prev_link = nav_link(num, keys, manifest, "prev")
        next_link = nav_link(num, keys, manifest, "next")
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