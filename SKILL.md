---
name: wechat-cover-designer
description: Create polished Chinese article cover images for WeChat public account and Xiaohongshu posts from screenshots or photos. Use when the user asks to make, edit, format, or reproduce a social-media cover style, especially 2.35:1 WeChat covers, interview/article thumbnails, Chinese editorial title overlays, gradient panels, title wrapping, or AI/product/business note covers.
---

# WeChat Cover Designer

## Quick Start

Use `scripts/wechat_cover.py` when the user wants a deterministic cover image from a source image and title.

```bash
python3 scripts/wechat_cover.py \
  --input source.png \
  --output cover.png \
  --title "OpenAI Codex 负责人：人人都是 AI Builder 的时代，PM 不会消失" \
  --platform wechat
```

For image-generation requests, use this skill to define the art direction, aspect ratio, text hierarchy, and exact title. If the user wants the original screenshot preserved, prefer the CLI first; if they want a more stylized or heavily edited image, use image generation with the style guide in `references/cover-style.md`.

## Workflow

1. Identify platform:
   - WeChat public account cover: `--platform wechat`, 2.35:1.
   - Xiaohongshu cover: `--platform xiaohongshu`, 3:4.
2. Preserve the meaningful subject of the source image. For interview screenshots, keep both people visible when possible.
3. Remove or cover distracting subtitles, subscribe badges, playback UI, and watermarks only when the user asks for a clean cover and has provided the image for editing.
4. Use concise Chinese editorial hierarchy:
   - Small label: topic/category, e.g. `AI 产品工作新范式`.
   - Main title: 2-4 lines, large, bold, high contrast.
   - Highlight 1-2 key phrases, e.g. `AI Builder`, `PM 不会消失`.
5. Export a high-resolution PNG. For WeChat, use 1645x700 by default.

## CLI Notes

The CLI uses Pillow. In Codex desktop, prefer the bundled Python if system Python lacks Pillow:

```bash
/Users/silin/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  scripts/wechat_cover.py --help
```

Outside Codex, install the dependency first:

```bash
python3 -m pip install -r requirements.txt
```

Key options:

- `--title`: exact title text to place on the cover.
- `--label`: small label above the title. Defaults to `AI 产品工作新范式`.
- `--highlight`: phrase to render in accent color. Can be repeated.
- `--remove-bottom-ratio`: fraction of image height covered by the bottom cleanup band.
- `--dim`: overlay strength. Increase for busy backgrounds.

## Style Guidance

Read `references/cover-style.md` before designing a new visual variant or writing an image-generation prompt.
