# Claude Code Instructions

Use this repository as a general-purpose CLI project, not as a Codex-only skill.

## Use

1. Read `AGENTS.md`.
2. Prefer the CLI in `scripts/wechat_cover.py`.
3. Read `references/cover-style.md` before modifying visual style.
4. Preserve `SKILL.md` and `agents/openai.yaml` for Codex compatibility.

## Example

```bash
python3 -m pip install -r requirements.txt
python3 scripts/wechat_cover.py \
  --input input.png \
  --output cover.png \
  --title $'OpenAI Codex 负责人：\n人人都是 AI Builder 的时代，\nPM 不会消失' \
  --platform wechat
```

## Editing Guidance

- Keep the CLI backward-compatible.
- Add new layout options as flags instead of hardcoding one-off behavior.
- Test WeChat output ratio after changes.
- Preserve the default warm interview, deep gradient, solid heavy title, vivid lime accent, and oversized hook-line style.
