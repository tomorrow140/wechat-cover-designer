# WeChat Cover Designer

Create polished Chinese article cover images for WeChat public account posts and Xiaohongshu notes from screenshots or photos.

This repository contains:

- A reusable Codex skill: `wechat-cover-designer`
- A Python CLI for deterministic cover generation
- A style guide for modern Chinese editorial covers

## Features

- Generate WeChat public account covers in `2.35:1`
- Generate Xiaohongshu-style vertical covers in `3:4`
- Preserve the original image subject while adding a readable title overlay
- Add dark translucent gradients for editorial-style readability
- Remove or cover bottom subtitles and small UI stickers
- Auto-wrap Chinese/English mixed titles
- Highlight key phrases such as `AI Builder` or `PM 不会消失`

## Example

```bash
python3 scripts/wechat_cover.py \
  --input input.png \
  --output cover.png \
  --title $'OpenAI Codex 负责人：\n人人都是 AI Builder 的时代，\nPM 不会消失' \
  --platform wechat
```

Default WeChat output size is `1645x700`.

## Install

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
python3 scripts/wechat_cover.py --help
```

## Codex Skill Usage

Install or copy this folder into your Codex skills directory:

```bash
~/.codex/skills/wechat-cover-designer
```

Then ask Codex:

```text
Use $wechat-cover-designer to create a 2.35:1 WeChat article cover from this image and title.
```

## Recommended Use Cases

- WeChat public account cover images
- Xiaohongshu note cover images
- AI product analysis article covers
- Podcast/interview screenshot covers
- Chinese business/product/tech editorial thumbnails
- Codex skill demos for social content creation

## Style

The default look is modern Chinese editorial:

- warm source image preserved
- dark gradient title area
- large white title
- green accent highlights
- minimal clutter
- no fake logos

See [`references/cover-style.md`](references/cover-style.md) for the design guide.

## License

MIT
