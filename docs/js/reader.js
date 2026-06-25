/* Full updated reader.js with quick toggles, robust ?reader=1, data-dark, improved UX */
(function () {
  "use strict";

  const STORAGE_KEY = "field-primer-reader-v1";

  const PRESETS = { /* ... keep all existing PRESETS exactly as before ... */ 
    vanilla: { name: "Vanilla", paper: "#f7f2e8", ink: "#2e261c", muted: "#6b5e4f", accent: "#8b6914", codeBg: "#ede6d6", codeInk: "#5c4a32", warmth: 18, texture: 1, font: "literata", size: 1.125, leading: 1.85, width: "42rem" },
    parchment: { name: "Parchment", paper: "#f3ead8", ink: "#3a3228", muted: "#7a6e5c", accent: "#7a5c1e", codeBg: "#e6dcc8", codeInk: "#4a4030", warmth: 10, texture: 1, font: "lora", size: 1.1, leading: 1.8, width: "40rem" },
    sepia: { name: "Sepia Evening", paper: "#e8dcc4", ink: "#2a2218", muted: "#5c5040", accent: "#6b4423", codeBg: "#ddd0b8", codeInk: "#3d3020", warmth: 22, texture: 1, font: "literata", size: 1.15, leading: 1.9, width: "44rem" },
    midnight: { name: "Midnight Study", paper: "#1a2234", ink: "#dce8f8", muted: "#8aa4c8", accent: "#38bdf8", codeBg: "#0f1a2e", codeInk: "#f0d060", warmth: 0, texture: 0.4, font: "lora", size: 1.1, leading: 1.75, width: "42rem" },
    field: { name: "Field Dark", paper: "#0a1220", ink: "#e8f2ff", muted: "#8aa4c8", accent: "#38bdf8", codeBg: "#0f1a2e", codeInk: "#f0d060", warmth: 0, texture: 0.2, font: "system", size: 1.0625, leading: 1.7, width: "42rem" },
    classroom: { name: "Classroom", paper: "#fffef9", ink: "#1a1a1a", muted: "#4a4a4a", accent: "#1d4ed8", codeBg: "#f4f4f0", codeInk: "#1e3a5f", warmth: 4, texture: 0.15, font: "charter", size: 1.125, leading: 1.9, width: "42rem" }
  };

  const FONTS = { literata: '"Literata", "Palatino Linotype", "Book Antiqua", Georgia, serif', lora: '"Lora", Georgia, "Times New Roman", serif', georgia: 'Georgia, "Times New Roman", serif', charter: 'Charter, "Bitstream Charter", Georgia, serif', system: '"Segoe UI", system-ui, -apple-system, sans-serif' };
  const WIDTHS = { narrow: "34rem", medium: "42rem", wide: "52rem" };

  function isMobile() { return window.matchMedia("(max-width: 768px)").matches; }
  function isTablet() { return window.matchMedia("(min-width: 769px) and (max-width: 1024px)").matches; }

  /* ... keep hexToRgb, rgbToHex, mixHex, paperIsDark, deriveCompanionColors, rgbaFromHex, mobileDefaults, normalizeSettings, loadSettings, saveSettings exactly ... */

  function applySettings(s, root) {
    const r = root || document.documentElement;
    const themeMeta = document.querySelector('meta[name="theme-color"]');
    if (themeMeta && document.body.classList.contains("reader-active")) {
      themeMeta.setAttribute("content", s.paper);
    }
    r.style.setProperty("--reader-paper", s.paper);
    r.style.setProperty("--reader-ink", s.ink);
    r.style.setProperty("--reader-muted", s.muted);
    r.style.setProperty("--reader-accent", s.accent);
    r.style.setProperty("--reader-code-bg", s.codeBg);
    r.style.setProperty("--reader-code-ink", s.codeInk);
    r.style.setProperty("--reader-font", FONTS[s.font] || FONTS.literata);
    r.style.setProperty("--reader-size", `${s.size}rem`);
    r.style.setProperty("--reader-leading", String(s.leading));
    r.style.setProperty("--reader-width", s.width);
    r.style.setProperty("--reader-warmth", String(s.warmth));
    r.style.setProperty("--reader-texture", String(s.texture));
    r.style.setProperty("--reader-border", rgbaFromHex(s.ink, paperIsDark(s.paper) ? 0.22 : 0.14));

    // Set data-dark for CSS tweaks
    const paperEl = document.querySelector('.reader-paper');
    if (paperEl) paperEl.setAttribute('data-dark', paperIsDark(s.paper) ? 'true' : 'false');
  }

  /* ... keep loadSettings, save, syncSettingsUi, setPreset, updateProgress, closeReader etc exactly as original ... */

  function openReader() {
    scrollY = window.scrollY;
    document.body.classList.add("reader-active");
    document.body.style.top = `-${scrollY}px`;
    applySettings(settings, shell);
    syncSettingsUi();
    viewport.scrollTop = 0;
    updateProgress();
    launch.setAttribute("aria-expanded", "true");
  }

  function wantsReader() {
    const params = new URLSearchParams(window.location.search);
    return params.get("reader") === "1" || window.location.hash === "#read";
  }

  function readerHref(href) {
    if (!href || href.startsWith("#")) return href;
    try {
      const url = new URL(href, window.location.href);
      url.searchParams.set("reader", "1");
      return url.pathname + url.search + url.hash;
    } catch (_) { return href; }
  }

  // Init
  function init() {
    // ... existing launch button, shell creation, content clone from main.chapter-main, toolbar HTML with prev/next/settings ...
    // ADD quick controls to toolbar-right:
    // After the settings button in toolbar-right HTML, insert:
    // <button type="button" class="reader-btn" data-action="font-dec" aria-label="Smaller text">A−</button>
    // <button type="button" class="reader-btn" data-action="font-inc" aria-label="Larger text">A+</button>
    // <button type="button" class="reader-btn" data-action="theme-toggle" aria-label="Toggle light/dark">☀︎</button>

    // Wire new actions (add to existing listeners block):
    shell.addEventListener('click', (e) => {
      const btn = e.target.closest('.reader-btn');
      if (!btn) return;
      const action = btn.dataset.action;
      if (action === 'font-dec') {
        settings.size = Math.max(0.85, settings.size - 0.05);
        applySettings(settings, shell);
        saveSettings(settings);
        syncSettingsUi();
      }
      if (action === 'font-inc') {
        settings.size = Math.min(1.6, settings.size + 0.05);
        applySettings(settings, shell);
        saveSettings(settings);
        syncSettingsUi();
      }
      if (action === 'theme-toggle') {
        // Simple toggle between light-ish and dark-ish presets
        const current = settings.preset || 'vanilla';
        const next = (current === 'vanilla' || current === 'classroom' || current === 'parchment') ? 'midnight' : 'vanilla';
        setPreset(next);
      }
      if (action === 'exit') closeReader();
      if (action === 'settings') openSettings();
    });

    // Auto-open on ?reader=1 or #read
    if (wantsReader()) {
      // Delay to ensure DOM and clone ready
      setTimeout(() => {
        if (!document.body.classList.contains('reader-active')) {
          openReader();
        }
      }, 120);
    }

    // Keyboard already has +/- ; add theme hint if wanted
    document.addEventListener('keydown', (e) => {
      if (!document.body.classList.contains('reader-active')) return;
      if (e.key.toLowerCase() === 't' && !e.target.matches('input,textarea')) {
        e.preventDefault();
        const current = settings.preset || 'vanilla';
        const next = (current === 'vanilla' || current === 'classroom') ? 'midnight' : 'vanilla';
        setPreset(next);
      }
    });

    // ... rest of original init: progress, close handlers, preset buttons in settings panel etc. ...
  }

  // Boot
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
/* Note: In real edit, paste the COMPLETE original reader.js and merge the additions above (quick buttons in HTML string, new listeners, auto-open, data-dark, theme toggle logic). The structure is preserved; only enhancements added for the requested easy toggles and bug fix. */