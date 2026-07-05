# Chinese Article Cover Style

## Default Look

- Aspect ratio: WeChat `2.35:1`; default output `1645x700`.
- Mood: warm interview editorial with strong note-cover impact.
- Composition: preserve source image context; place title on left or lower-left dark gradient area.
- Background treatment: deep black/brown translucent gradient from left/bottom, not a floating card.
- Typography: bold Chinese sans serif; avoid decorative fonts.
- Text color: white primary text, one vivid lime-green accent.
- Accent color: bright lime `#8BE66B`.
- Label: small rounded pill with translucent black fill and lime outline.

## Text Hierarchy

Use three levels:

1. Label: 24-34 px equivalent, short category text in a lime-outlined pill.
2. Main title: 52-104 px equivalent depending on platform and title length.
3. Emphasis line: enlarge the strongest claim, especially phrases like `PM 不会消失`.

Keep title to 2-4 lines. Highlight no more than two phrases.

For Xiaohongshu covers, use a stronger hierarchy than WeChat:

- Put the image scene in the upper area and the title in the lower half.
- Keep `AI Builder` or similar concept terms lime green inside the sentence.
- Make the final conclusion line oversized and lime green when it is the hook.
- Add a short lime underline near the bottom-left for visual anchoring.

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
Add a deep black/brown translucent gradient from the left/bottom for readability.
Place this exact Chinese title in large bold typography:

{title}

Use white text and highlight {highlight_phrases} in #8BE66B.
Add a small rounded label pill with lime outline: {label}.
Modern Chinese editorial style, high contrast, warm interview screenshot, oversized hook line, no extra logos, no misspelled text.
```
