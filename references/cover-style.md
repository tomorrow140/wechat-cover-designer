# Chinese Article Cover Style

## Default Look

- Aspect ratio: WeChat `2.35:1`; default output `1645x700`.
- Mood: modern editorial, warm, restrained, high-signal.
- Composition: preserve source image context; place title on left or lower-left gradient panel.
- Background treatment: dark translucent gradient from left/bottom, not a floating card.
- Typography: bold Chinese sans serif; avoid decorative fonts.
- Text color: white primary text, muted white label, one green accent.
- Accent color: OpenAI-like green `#10A37F`.

## Text Hierarchy

Use three levels:

1. Label: 24-34 px equivalent, short category text.
2. Title: 52-82 px equivalent depending on title length.
3. Optional source line: only when the user asks.

Keep title to 2-4 lines. Highlight no more than two phrases.

## Interview Screenshot Treatment

- Keep both speakers visible if possible.
- Cover bottom subtitles with a subtle dark band or crop them away.
- Do not add fake logos, fake badges, or invented source marks.
- Avoid cluttering the center if faces occupy left and right sides.

## Prompt Template

```text
Create a 2.35:1 WeChat public account cover based on the provided image.
Preserve the main subjects and warm editorial atmosphere.
Remove or cover subtitles and small UI stickers.
Add a subtle dark translucent gradient from the left/bottom for readability.
Place this exact Chinese title in large bold typography:

{title}

Use white text and highlight {highlight_phrases} in #10A37F.
Add a small label: {label}.
Modern Chinese editorial style, high contrast, restrained, no extra logos, no misspelled text.
```
