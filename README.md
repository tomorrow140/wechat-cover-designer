# WeChat Cover Designer

Create polished Chinese article cover images for WeChat public account posts and Xiaohongshu notes from screenshots or photos.

This repository is **agent-neutral**. It can be used by Codex, Claude Code, Cursor, other coding agents, or directly from the command line.

This repository contains:

- A reusable Codex skill: `wechat-cover-designer`
- A Python CLI for deterministic cover generation
- A style guide for modern Chinese editorial covers
- Agent instructions for non-Codex tools

## Features

- Generate WeChat public account covers in `2.35:1`
- Generate Xiaohongshu-style vertical covers in `3:4`
- Preserve the original image subject while adding a readable title overlay
- Add deep black/brown translucent gradients for editorial-style readability
- Remove or cover bottom subtitles and small UI stickers
- Auto-wrap Chinese/English mixed titles
- Highlight key phrases such as `AI Builder` or `PM 不会消失` in vivid lime green
- Render solid heavy Chinese title text with bundled `Noto Sans CJK SC Black` and drop shadow, closer to editorial note-cover typography

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

## Other Agent Usage

For Claude Code, Cursor, or other coding agents:

- Read [`AGENTS.md`](AGENTS.md) for generic agent instructions.
- Read [`CLAUDE.md`](CLAUDE.md) for Claude Code-specific guidance.
- Use [`.cursor/rules/wechat-cover-designer.mdc`](.cursor/rules/wechat-cover-designer.mdc) in Cursor.
- Read [`llms.txt`](llms.txt) for a compact LLM-facing project summary.

The stable integration surface is always the CLI:

```bash
python3 scripts/wechat_cover.py --input input.png --output cover.png --title "标题" --platform wechat
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
- deep black/brown gradient title area
- large solid heavy white title
- vivid lime-green accent highlights
- smooth lime-outlined label pill with compact heavy text
- oversized hook line for Xiaohongshu covers
- minimal clutter
- no fake logos

See [`references/cover-style.md`](references/cover-style.md) for the design guide.

## Font License

The bundled title font `assets/fonts/NotoSansCJKsc-Black.otf` is from Google/Adobe's Noto Sans CJK project and is distributed under the SIL Open Font License. See [`assets/fonts/NotoSansCJK-LICENSE.txt`](assets/fonts/NotoSansCJK-LICENSE.txt).

## License

MIT
