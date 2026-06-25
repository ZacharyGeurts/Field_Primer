#!/usr/bin/env python3
"""Build picture-led chapter HTML from image manifest + expanded prose."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/data/image-manifest.json"
OUT = ROOT / "docs/chapters"

CHAPTER_BODY: dict[str, str] = {
    "01": """
<p>A <strong>field</strong> in this stack is any continuous quantity stored over space that other systems read and write every tick. That includes GPU storage images, a die-resident guest RAM map, and JSON telemetry describing network flows.</p>
<div class="callout everyone"><strong>Plain English:</strong> A program is a recipe. A field is the state of the kitchen — heat on every burner, not just the timer.</div>
<h3>Three families you will meet</h3>
<table><thead><tr><th>Family</th><th>Where</th><th>Stores</th></tr></thead>
<tbody>
<tr><td>GPU analog fabric</td><td>Bindings 8–10</td><td>Phi, Thermo, Flow</td></tr>
<tr><td>Field Die</td><td>SSBO binding 1</td><td>x86 guest, VGA, tile cache</td></tr>
<tr><td>Packet field</td><td>NEXUS state</td><td>TX/RX, ports, corroboration</td></tr>
</tbody></table>
<p>Labels used throughout: <span class="tag impl">Implemented</span> <span class="tag meta">Metaphor</span> <span class="tag phil">Philosophy</span> <span class="tag vis">Visual</span></p>
""",
    "02": """
<p>Fields appear at three scales in the sovereign stack — from texels on the GPU to packets on the wire. Understanding the scale prevents category errors (treating a shader metaphor as a spectrum analyzer).</p>
<h3>GPU fabric path</h3>
<pre class="eq">RayCanvas → createAnalogFieldFabric() → CANVAS.comp / x86.comp → hardwareFabric mirror</pre>
<p>The host <em>never</em> runs a CPU PDE solver on Phi/Thermo/Flow. Evolution is compute-shader work each dispatch.</p>
<h3>Field Die path</h3>
<p><code>FieldX86Die</code> holds 64 MiB guest linear map, VGA at <code>0xB8000</code>, C mirror at <code>0x01000000</code>. Guest RAM is where DOS lives; <code>data_bus[64]</code> is the dashboard.</p>
<h3>Packet field path</h3>
<p>NEXUS turns sockets into sentences: process path, port habit, harm candidates, permanent KILL archive. Panel is the window; <code>field jsonl</code> is the library.</p>
""",
    "03": """
<p>Every classic canvas dispatch evolves three coupled <code>R32G32B32A32</code> images. Thermodynamics here is <strong>accounting</strong> — tracking irreversibility like a power meter, not claiming laboratory calorimetry.</p>
<figure class="figure inline-wide"><img src="../assets/images/fabric-triple.jpg" alt="Phi Thermo Flow fabric" loading="lazy" /><figcaption>Figure 3.1 — Coupled fabric channels at Vulkan bindings 8–10.</figcaption></figure>
<h3>Per-texel evolution</h3>
<ol><li><strong>Phi</strong> — Laplacian wave step + <code>WaveSpeed</code> + propalactic forcing</li>
<li><strong>Thermo</strong> — diffusion, entropy floor, coupling to Phi</li>
<li><strong>Flow</strong> — gradients mixed with <code>GateFidelity</code> + Tesla relaxation</li></ol>
<div class="eq">newPhi ∈ [-2, 2] · newThermo ∈ [0, 1.5] · newFlow ∈ [0, 1]</div>
<h3>CFL guard (host)</h3>
<div class="eq">waveCFL = c·Δt/Δx ≤ 1 · thermoCFL = α·Δt/Δx² ≤ 1</div>
<p class="tag impl">Implemented on classic canvases. Body-temperature seeding is normalized simulation flavor.</p>
""",
    "04": """
<p><code>ThermoAccountant</code> at Vulkan binding <strong>2</strong> writes an entropy ledger every <code>dispatch_canvas()</code>. NEXUS runs a separate <strong>Shannon oracle</strong> on files. Same word — different layers.</p>
<figure class="figure"><img src="../assets/images/entropy-chapter.jpg" alt="Entropy chapter art" loading="lazy" /><figcaption>Figure 4.1 — Irreversibility: fabric floor, frame proxy, file randomness.</figcaption></figure>
<h3>Landauer (theory)</h3>
<div class="eq">E_min = k_B T ln 2</div>
<p class="tag meta">In-engine <code>entropyThisFrame</code> is a proxy integral — not joules from nvidia-smi.</p>
<h3>Shannon (NEXUS)</h3>
<div class="eq">H = −Σ p_i log₂ p_i</div>
<p>High H suggests packed, encrypted, or obfuscated payloads. Daemon thresholds tune calm / alert / storm polling.</p>
<h3>Operator grep</h3>
<pre class="eq">./linux.sh run 2>&1 | tee run.log
grep -E 'THERMO|entropy|Boundary|prevMaint' run.log</pre>
""",
    "05": """
<p>The packet field is the <strong>meaning layer</strong> on top of sockets. <code>ss</code> shows existence; tcpdump shows frames; NEXUS adds intent, habit, and corroboration before permanent action.</p>
<figure class="figure"><img src="../assets/images/packet-field.jpg" alt="Packet field" loading="lazy" /><figcaption>Figure 5.1 — Local flows as an operator-readable field.</figcaption></figure>
<h3>Gatekeeper verdicts</h3>
<table><thead><tr><th>Verdict</th><th>Meaning</th></tr></thead>
<tbody>
<tr><td>USER_OK</td><td>Permitted flow</td></tr>
<tr><td>EPHEMERAL</td><td>Short-lived, low risk</td></tr>
<tr><td>SUSPICIOUS</td><td>Watchlist — not auto-block</td></tr>
<tr><td>HARM_CANDIDATE</td><td>Harm signature — operator review</td></tr>
</tbody></table>
<p class="tag phil">94/6 truth filter is operator philosophy — watchlist before KILL.</p>
<p class="tag impl">Implemented in NEXUS-Shield — not inside AMOURANTHRTX Vulkan engine.</p>
""",
    "06": """
<p>“RF” means three different things here. Keep them separated or you will argue with a shader about ionospheric physics.</p>
<figure class="figure"><img src="../assets/images/chapters/ch06-planetary-weave.jpg" alt="Planetary weave" loading="lazy" /><figcaption>Figure 6.1 — Visual RF shell in planetary_weave.comp (not instrumentation).</figcaption></figure>
<table><thead><tr><th>Context</th><th>RF means</th></tr></thead>
<tbody>
<tr><td>planetary_weave.comp</td><td><span class="tag vis">Visual</span> atmospheric shell layer</td></tr>
<tr><td>NEXUS Field Antenna</td><td><span class="tag impl">Implemented</span> local orchestration</td></tr>
<tr><td>Engine fieldPhi</td><td>Gate voltage / wave potential</td></tr>
</tbody></table>
<div class="eq">FSPL ∝ 20 log₁₀(d) + 20 log₁₀(f) — teaching reference, not shader math</div>
""",
    "07": """
<p>C++ opens the window. The GPU runs the world. Default <code>./linux.sh run</code> launches the <strong>Field Die</strong> (<code>x86.comp</code>), not a decorative raymarch demo.</p>
<figure class="figure"><img src="../assets/images/chapters/ch07-gpu-engine.jpg" alt="GPU engine" loading="lazy" /><figcaption>Figure 7.1 — Thin host, fat GPU — dispatch spine.</figcaption></figure>
<pre class="eq">main → navigator_main() → RayCanvas → Pipeline::dispatch_canvas() → vkCmdDispatch</pre>
<h3>Descriptor layout (x86)</h3>
<table><thead><tr><th>Binding</th><th>Resource</th></tr></thead>
<tbody>
<tr><td>0</td><td>HDR output</td></tr>
<tr><td>1</td><td>FieldX86Die SSBO</td></tr>
<tr><td>2</td><td>ThermoAccountant</td></tr>
<tr><td>8–10</td><td>Phi, Thermo, Flow</td></tr>
</tbody></table>
<p><code>TotalTime::seal()</code> provides monotonic session clock — frame-rate drift cannot rewrite physics time.</p>
""",
    "08": """
<p>The Field Die is a 64 MiB guest linear map on the GPU — VGA at <code>0xB8000</code>, not DOSBox. <code>x86.comp</code> interprets guest instructions; <code>FieldX86Emu</code> assists when <code>ControlHostCpu</code> is set.</p>
<figure class="figure"><img src="../assets/images/field-die.jpg" alt="Field die" loading="lazy" /><figcaption>Figure 8.1 — Guest RAM, holographic boundary, fabric channels.</figcaption></figure>
<h3>data_bus[64] spine</h3>
<table><thead><tr><th>Slots</th><th>Content</th></tr></thead>
<tbody>
<tr><td>[16–23]</td><td>Analog FCC floats</td></tr>
<tr><td>[24–28]</td><td>ThermoAccountant mirrors</td></tr>
<tr><td>[31, 34]</td><td>Tesla valve bias</td></tr>
</tbody></table>
<p><code>ZMM1024</code> tile cache at SSBO tail — fabric samples for HUD hex dumps.</p>
""",
    "09": """
<p>Before fabric evolution, the host enforces CFL stability. The Tesla valve adds <strong>directional</strong> flow bias — forward paths ease, reverse paths resist.</p>
<figure class="figure"><img src="../assets/images/chapters/ch09-tesla-valve.jpg" alt="Tesla valve" loading="lazy" /><figcaption>Figure 9.1 — Directional resistance metaphor (not a literal fluidic part).</figcaption></figure>
<div class="eq">TESLA_R_FORWARD = 0.18 · TESLA_R_REVERSE = 3.2 · FIELD_PHI_MILLI = 618</div>
<p class="tag meta">Named after Tesla's fluidic diode — code metaphor for anisotropic damping.</p>
""",
    "10": """
<p><code>updateHardwareFromAnalogFields()</code> mirrors averaged Phi/Thermo/Flow into <code>hardwareFabric</code> — a read-only dashboard, not a second simulation mesh.</p>
<figure class="figure"><img src="../assets/images/chapters/ch10-spiderweb.jpg" alt="Spiderweb" loading="lazy" /><figcaption>Figure 10.1 — Spiderweb util graph driven by fabric averages.</figcaption></figure>
<table><thead><tr><th>Tier</th><th>Operator access</th></tr></thead>
<tbody>
<tr><td>Puny</td><td>Status log, real sysfs clocks</td></tr>
<tr><td>Adept</td><td>Target clock, SimulateSubMicron</td></tr>
<tr><td>Tidewalker</td><td>Full spiderweb graph override</td></tr>
</tbody></table>
<p class="tag meta">“Sub-micron zero cost” = procedural detail at pixel scale — not SEM imaging.</p>
""",
    "11": """
<p>Trust stderr before screenshots. <code>ELLIE</code> categories — <code>THERMO</code>, <code>STATUS</code>, <code>RTXPROBE</code> — are how operators audit reality without a marketing deck.</p>
<figure class="figure"><img src="../assets/images/chapters/ch11-observability.jpg" alt="Observability" loading="lazy" /><figcaption>Figure 11.1 — Logs, probes, and the NEXUS panel as one observability stack.</figcaption></figure>
<pre class="eq">set AnalogFields.GateFidelity 0.85
list Hardware
RTX_PROBES=1   # optional GPU timestamps</pre>
<p>NEXUS panel at <code>https://127.0.0.1:9477/</code> — RTX Zero mode via <code>?rtx=1</code>.</p>
""",
    "12": """
<p>Chapter 12 is the contract with the reader: we label poetry so scientists stay rigorous and newcomers stay safe.</p>
<figure class="figure"><img src="../assets/images/chapters/ch12-honesty.jpg" alt="Reality vs theory" loading="lazy" /><figcaption>Figure 12.1 — Metaphor glow vs measured grid — both have a place, never confused.</figcaption></figure>
<table><thead><tr><th>Claim</th><th>Reality</th></tr></thead>
<tbody>
<tr><td>Living thermodynamic computer</td><td>ThermoAccountant in logs</td></tr>
<tr><td>Packet field sees everything</td><td>Local sockets + heuristics only</td></tr>
<tr><td>RF planetary shell</td><td>Visual shader layer</td></tr>
<tr><td>Landauer joules from GPU</td><td>Proxy integral</td></tr>
</tbody></table>
<p>What you can <code>grep</code>, <code>set</code>, and screenshot is real. What sounds like cosmology is often a knob with a poetic name.</p>
""",
}

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{num} — {title} · Field Primer</title>
  <link rel="stylesheet" href="../css/field-primer.css" />
  <link rel="stylesheet" href="../css/chapters.css" />
</head>
<body class="chapter-page accent-{accent}">
  <nav class="top"><div class="inner">
    <a class="logo" href="../index.html">FIELD PRIMER</a>
    <ul>
      <li><a href="../gallery.html">Gallery</a></li>
      <li><a href="../index.html#chapters">Chapters</a></li>
      <li><a href="https://github.com/ZacharyGeurts/Field_Primer/wiki/{wiki}">Wiki</a></li>
    </ul>
  </div></nav>
  <header class="chapter-hero" style="background-image:url('../assets/images/{image}')">
    <div class="chapter-hero-overlay"></div>
    <div class="chapter-hero-content">
      <p class="eyebrow">Chapter {num}</p>
      <h1>{title}</h1>
    </div>
  </header>
  <main class="chapter-main">
    <nav class="chapter-nav">{prev_link} {next_link}</nav>
    {body}
    <nav class="chapter-nav bottom">{prev_link} {next_link}</nav>
  </main>
  <footer><p>Field Primer · CC BY-NC-SA 4.0 · <a href="https://github.com/ZacharyGeurts/AMOURANTHRTX">AmouranthRTX</a> engine branding</p></footer>
</body>
</html>
"""


def nav_link(num: int, manifest: dict, direction: str) -> str:
    chapters = sorted(manifest["chapters"].items(), key=lambda x: int(x[0]))
    keys = [int(k) for k, _ in chapters]
    if direction == "prev":
        if num <= 1:
            return '<a class="btn secondary" href="../index.html">← Home</a>'
        prev = str(num - 1).zfill(2)
        ch = manifest["chapters"][prev]
        return f'<a class="btn secondary" href="{ch["slug"]}.html">← Ch {num-1}</a>'
    if num >= 12:
        return '<a class="btn" href="../gallery.html">Gallery →</a>'
    nxt = str(num + 1).zfill(2)
    ch = manifest["chapters"][nxt]
    return f'<a class="btn" href="{ch["slug"]}.html">Ch {num+1} →</a>'


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    for key, ch in manifest["chapters"].items():
        num = int(key)
        body = CHAPTER_BODY.get(key, "<p>See wiki for full prose.</p>")
        prev_link = nav_link(num, manifest, "prev")
        next_link = nav_link(num, manifest, "next")
        html_out = TEMPLATE.format(
            num=num,
            title=html.escape(ch["title"]),
            accent=ch["accent"],
            wiki=ch["wiki"],
            image=ch["image"],
            body=body,
            prev_link=prev_link,
            next_link=next_link,
        )
        (OUT / f"{ch['slug']}.html").write_text(html_out, encoding="utf-8")
        print(f"wrote {ch['slug']}.html")
    print("done")


if __name__ == "__main__":
    main()