---
name: playwright
description: Browser automation and HTML-to-image rendering with Playwright in this sandbox. Use for rendering styled caption cards, title cards, thumbnails, and graphics as PNGs for the video pipeline, and for scraping allowlisted domains. Covers the hard network limits (egress allowlist blocks social media) so time isn't wasted attempting blocked sites.
---

# Playwright in this sandbox

## Status: PRE-INSTALLED. Do not install.
- Python `playwright` importable · Node `playwright` v1.56.0 · Chromium launches clean
- No `~/.cache/ms-playwright` dir, yet browsers work — binaries live elsewhere. Don't run `playwright install`.

## ⚠️ THE NETWORK LIMIT (verified by test)
Playwright goes through the same egress proxy as everything else.

| Domain | Result |
|---|---|
| github.com, npmjs.com, pypi.org, files.pythonhosted.org, ubuntu repos | ✅ HTTP 200 |
| youtube.com, tiktok.com, facebook.com, instagram.com, higgsfield.ai, **any non-allowlisted site** | ❌ **HTTP 403** |

**So Playwright CANNOT:** scrape social media, analyse a YouTube video, log into Higgsfield's web UI, post content, or read arbitrary web pages.
**For those:** use `web_search` / `web_fetch` (different egress path), the Higgsfield MCP tools, or ask the user to download and upload the file.

## ✅ THE HIGH-VALUE USE: HTML → PNG for the video pipeline
Local HTML renders perfectly. This is far better-looking than FFmpeg `drawtext`, which produces flat, unstyled captions.

Use it to render, as transparent PNGs, then composite with FFmpeg:
- kinetic caption cards · title/hook cards · CTA end-cards
- series title cards (pillar branding, file 14) · lower-thirds
- thumbnails · pricing/spec graphics · comparison tables

### Pattern
```python
from playwright.sync_api import sync_playwright

HTML = """
<body style="margin:0;width:1080px;height:400px;background:transparent;
             display:flex;align-items:center;justify-content:center;
             font-family:'DejaVu Sans',sans-serif">
  <div style="color:#fff;font-size:78px;font-weight:800;text-align:center;
              line-height:1.1;text-shadow:0 6px 24px rgba(0,0,0,.85);
              -webkit-text-stroke:3px rgba(0,0,0,.6)">
    POV: selling recond cars<br><span style="font-size:52px">the real side</span>
  </div>
</body>"""

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width':1080,'height':400})
    pg.set_content(HTML)
    pg.screenshot(path='card.png', omit_background=True)   # transparent
    b.close()
```

### Composite into video (FFmpeg)
```bash
ffmpeg -i clip.mp4 -i card.png -filter_complex \
  "[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1[c];[0:v][c]overlay=0:H*0.62" out.mp4
```

## Rules
- Always `omit_background=True` for overlays — you want alpha, not a black box.
- Set an explicit `viewport` matching the target width (1080 for 9:16).
- Fonts available: DejaVu family. Don't reference webfonts — no CDN access.
- Screenshots of local content only. Never plan a workflow around fetching a blocked domain.
