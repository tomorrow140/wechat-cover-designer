# Agent Instructions

This repository is agent-neutral. Any coding agent can use it to create Chinese social media cover images.

## Primary Interface

Use the CLI first. It is the stable interface across agents:

```bash
python3 scripts/wechat_cover.py \
  --input input.png \
  --output cover.png \
  --title "文章标题" \
  --platform wechat
```

Install dependencies if needed:

```bash
python3 -m pip install -r requirements.txt
```

## Common Tasks

### Create a WeChat public account cover

Use `--platform wechat`. The output is `1645x700` (`2.35:1`).

Recommended title format:

```bash
--title $'主标题第一行\n主标题第二行\n主标题第三行'
```

### Create a Xiaohongshu cover

Use `--platform xiaohongshu`. The output is vertical `3:4`.

### Match the repository style

Read `references/cover-style.md` before changing layout, colors, typography, or prompt wording.

## Design Rules

- Preserve the meaningful subject of the source image.
- Keep interview speakers visible when possible.
- Cover distracting subtitles, subscribe stickers, playback UI, and bottom captions.
- Use a dark translucent gradient, not a floating card.
- Use large solid heavy Chinese title text with drop shadow.
- Highlight no more than two phrases with vivid lime `#8BE66B`.
- Use a lime-outlined label pill for the category label.
- For Xiaohongshu, place the title in the lower half and make the strongest hook line oversized.
- Avoid black outline-only typography; the letters should look filled and heavy.
- Do not add fake logos or invented source marks.

## Validation

Run:

```bash
python3 scripts/wechat_cover.py --help
python3 scripts/wechat_cover.py --input input.png --output cover.png --title "测试标题" --platform wechat
```

For Codex skill validation, run the external `quick_validate.py` tool if available.
