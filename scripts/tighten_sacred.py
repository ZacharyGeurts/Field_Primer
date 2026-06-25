"""Remove per-section boilerplate from sacred chapters 16–17; one workshop block."""

from __future__ import annotations

import re

BOILERPLATE = re.compile(
    r"<p>(?:Pedagogy for «[^»]+»:|Workshop exercise \d+:|Synthesis question for «[^»]+»:|"
    r"Field note \d+ on [^:<]+:|Lab pairing for «[^»]+»:|Citation drill:)[^<]*</p>\s*",
    re.DOTALL,
)

SACRED_WORKSHOP = """
<div class="sacred-workshop">
<h2>Sacred track workshop — complete once</h2>
<p><span class="tag phil">Philosophy track.</span> These exercises apply to Chapters 16–18 collectively — not once per section above.</p>
<ol>
<li><strong>Memo:</strong> Two pages — one <a href="../creditors/index.html">creditor tribute</a> cited, one <code>grep</code> command proving an <span class="tag impl">Implemented</span> claim from this chapter.</li>
<li><strong>Pair drill:</strong> Matched 90-second sessions; diff THERMO or jsonl; resolve disputes with headers, not vibes.</li>
<li><strong>Status email:</strong> Three sentences to management — one Implemented, one Metaphor, one Philosophy (Chapter 12 labels).</li>
<li><strong>Journal entry:</strong> Date, git hash, three log lines, one surprise, one honesty label. Bring to Chapter 18 audit.</li>
</ol>
</div>
"""


def tighten_sacred(body: str, chapter_key: str) -> str:
    if chapter_key not in ("16", "17"):
        return body
    if "sacred-workshop" in body:
        return body
    cleaned = BOILERPLATE.sub("", body)
    marker = "<h2>Operator journal"
    if marker in cleaned:
        return cleaned.replace(marker, SACRED_WORKSHOP + "\n" + marker, 1)
    marker2 = "<h2>Chapter closing"
    if marker2 in cleaned:
        return cleaned.replace(marker2, SACRED_WORKSHOP + "\n" + marker2, 1)
    return cleaned + SACRED_WORKSHOP