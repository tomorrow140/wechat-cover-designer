#!/usr/bin/env python3
"""Create WeChat/Xiaohongshu article covers from a source image."""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

Image = ImageDraw = ImageFont = ImageFilter = None


ACCENT = (139, 230, 107)
WHITE = (255, 255, 255)
DEEP_SHADOW = (0, 0, 0)


@dataclass(frozen=True)
class PlatformSpec:
    width: int
    height: int
    margin_x: int
    margin_y: int
    title_max_width: int
    title_min_size: int
    title_max_size: int
    label_size: int


SPECS = {
    "wechat": PlatformSpec(1645, 700, 110, 74, 1290, 52, 94, 31),
    "xiaohongshu": PlatformSpec(1200, 1600, 76, 82, 1048, 62, 104, 34),
}


FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/STHeiti Light.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Songti.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def find_font(explicit: str | None = None) -> str:
    if explicit:
        if Path(explicit).exists():
            return explicit
        raise SystemExit(f"Font not found: {explicit}")
    for candidate in FONT_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("No Chinese-capable font found. Pass --font /path/to/font.ttf")


def ensure_pillow() -> None:
    global Image, ImageDraw, ImageFont, ImageFilter
    if Image is not None:
        return
    try:
        from PIL import Image as PILImage
        from PIL import ImageDraw as PILImageDraw
        from PIL import ImageFilter as PILImageFilter
        from PIL import ImageFont as PILImageFont
    except ImportError as exc:  # pragma: no cover - exercised by users without Pillow
        raise SystemExit(
            "Pillow is required. Install with `python3 -m pip install pillow`, "
            "or run with Codex bundled Python."
        ) from exc
    Image = PILImage
    ImageDraw = PILImageDraw
    ImageFilter = PILImageFilter
    ImageFont = PILImageFont


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def center_crop_to_ratio(img: Image.Image, ratio: float) -> Image.Image:
    width, height = img.size
    current = width / height
    if current > ratio:
        new_width = int(height * ratio)
        left = (width - new_width) // 2
        return img.crop((left, 0, left + new_width, height))
    new_height = int(width / ratio)
    top = max(0, (height - new_height) // 2)
    return img.crop((0, top, width, top + new_height))


def apply_neon_editorial_gradient(base: Image.Image, dim: float) -> Image.Image:
    width, height = base.size
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    pixels = overlay.load()
    max_alpha = int(255 * max(0.0, min(dim, 0.92)))
    for y in range(height):
        vertical = (y / max(height, 1)) ** 1.65
        top = max(0.0, 1.0 - y / max(height * 0.58, 1))
        for x in range(width):
            left = max(0.0, 1.0 - x / max(width * 0.55, 1))
            alpha = int(max_alpha * max(vertical, left * 0.78, top * 0.32))
            pixels[x, y] = (0, 0, 0, alpha)
    return Image.alpha_composite(base.convert("RGBA"), overlay)


def compose_xiaohongshu_scene(source: Image.Image, spec: PlatformSpec, dim: float, remove_bottom_ratio: float) -> Image.Image:
    background = center_crop_to_ratio(source, spec.width / spec.height)
    background = background.resize((spec.width, spec.height), Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(24)).convert("RGBA")
    background = Image.alpha_composite(background, Image.new("RGBA", background.size, (0, 0, 0, 115)))

    clean = source.crop((0, 0, source.size[0], int(source.size[1] * max(0.68, 1 - remove_bottom_ratio))))
    foreground_width = spec.width
    foreground_height = int(clean.size[1] * foreground_width / clean.size[0])
    foreground = clean.resize((foreground_width, foreground_height), Image.Resampling.LANCZOS).convert("RGBA")
    background.alpha_composite(foreground, (0, 0))
    return apply_neon_editorial_gradient(background, dim)


def cover_bottom_ui(img: Image.Image, ratio: float) -> Image.Image:
    if ratio <= 0:
        return img
    width, height = img.size
    band_h = int(height * ratio)
    if band_h <= 0:
        return img
    result = img.copy()
    crop_top = max(0, height - band_h - int(height * 0.08))
    sample = result.crop((0, crop_top, width, height - band_h))
    blurred = sample.resize((width, band_h)).filter(ImageFilter.GaussianBlur(radius=18))
    mask = Image.new("L", (width, band_h), 190)
    result.paste(blurred, (0, height - band_h), mask)
    shade = Image.new("RGBA", (width, band_h), (0, 0, 0, 68))
    result.alpha_composite(shade, (0, height - band_h))
    return result


def text_width(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> int:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def split_long_token(token: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    pieces: list[str] = []
    current = ""
    for char in token:
        trial = current + char
        if current and text_width(draw, trial, font) > max_width:
            pieces.append(current)
            current = char
        else:
            current = trial
    if current:
        pieces.append(current)
    return pieces


def wrap_title(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    if "\n" in text:
        lines: list[str] = []
        for raw_line in text.splitlines():
            raw_line = raw_line.strip()
            if raw_line:
                lines.extend(wrap_title(raw_line, draw, font, max_width))
        return lines

    normalized = text.replace("：", "： ").replace("，", "， ").replace("。", "。 ")
    tokens = [part for part in normalized.split() if part]
    lines: list[str] = []
    current = ""
    for token in tokens:
        if text_width(draw, token, font) > max_width:
            for piece in split_long_token(token, draw, font, max_width):
                if current:
                    lines.append(current.rstrip())
                    current = ""
                lines.append(piece)
            continue
        separator = " " if needs_space(current, token) else ""
        trial = token if not current else current + separator + token
        if current and text_width(draw, trial, font) > max_width:
            lines.append(current.rstrip())
            current = token
        else:
            current = trial
    if current:
        lines.append(current.rstrip())
    return lines


def is_ascii_word_char(char: str) -> bool:
    return char.isascii() and (char.isalnum() or char in {"_", "-", "/"})


def needs_space(left: str, right: str) -> bool:
    if not left or not right:
        return False
    return is_ascii_word_char(left[-1]) or is_ascii_word_char(right[0])


def choose_title_font(
    title: str,
    draw: ImageDraw.ImageDraw,
    font_path: str,
    spec: PlatformSpec,
    max_lines: int,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    for size in range(spec.title_max_size, spec.title_min_size - 1, -2):
        font = load_font(font_path, size)
        lines = wrap_title(title, draw, font, spec.title_max_width)
        if len(lines) <= max_lines:
            return font, lines
    font = load_font(font_path, spec.title_min_size)
    return font, wrap_title(title, draw, font, spec.title_max_width)


def line_fragments(line: str, highlights: Sequence[str]) -> list[tuple[str, bool]]:
    fragments: list[tuple[str, bool]] = [(line, False)]
    for phrase in sorted([p for p in highlights if p], key=len, reverse=True):
        next_fragments: list[tuple[str, bool]] = []
        for text, marked in fragments:
            if marked or phrase not in text:
                next_fragments.append((text, marked))
                continue
            parts = text.split(phrase)
            for index, part in enumerate(parts):
                if part:
                    next_fragments.append((part, False))
                if index < len(parts) - 1:
                    next_fragments.append((phrase, True))
        fragments = next_fragments
    return fragments


def draw_rich_line(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    line: str,
    font: ImageFont.FreeTypeFont,
    highlights: Sequence[str],
    stroke_width: int = 2,
) -> None:
    x, y = xy
    for fragment, marked in line_fragments(line, highlights):
        color = ACCENT if marked else WHITE
        draw.text((x, y), fragment, font=font, fill=color, stroke_width=stroke_width, stroke_fill=DEEP_SHADOW)
        x += text_width(draw, fragment, font)


def draw_label_pill(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
) -> int:
    x, y = xy
    padding_x = 34
    padding_y = 14
    box = draw.textbbox((0, 0), text, font=font)
    width = box[2] - box[0] + padding_x * 2
    height = box[3] - box[1] + padding_y * 2
    radius = height // 2
    draw.rounded_rectangle(
        (x, y, x + width, y + height),
        radius=radius,
        fill=(0, 0, 0, 118),
        outline=ACCENT,
        width=2,
    )
    draw.text((x + padding_x, y + padding_y - 2), text, font=font, fill=WHITE, stroke_width=1, stroke_fill=DEEP_SHADOW)
    return height


def is_emphasis_line(line: str, highlights: Sequence[str]) -> bool:
    return any(phrase and phrase in line for phrase in highlights)


def render_cover(args: argparse.Namespace) -> Path:
    ensure_pillow()
    spec = SPECS[args.platform]
    source = Image.open(args.input).convert("RGB")
    if args.platform == "xiaohongshu":
        base = compose_xiaohongshu_scene(source, spec, args.dim, args.remove_bottom_ratio)
    else:
        cropped = center_crop_to_ratio(source, spec.width / spec.height)
        base = cropped.resize((spec.width, spec.height), Image.Resampling.LANCZOS).convert("RGBA")
        base = cover_bottom_ui(base, args.remove_bottom_ratio)
        base = apply_neon_editorial_gradient(base, args.dim)

    draw = ImageDraw.Draw(base)
    font_path = find_font(args.font)
    label_font = load_font(font_path, args.label_size or spec.label_size)
    title_font, lines = choose_title_font(args.title, draw, font_path, spec, args.max_lines)
    emphasis_font = load_font(font_path, int(title_font.size * (1.28 if args.platform == "wechat" else 1.32)))
    line_gap = int(title_font.size * 0.22)
    line_fonts = [emphasis_font if is_emphasis_line(line, args.highlight) and ("PM" in line or len(lines) <= 3) else title_font for line in lines]
    title_height = sum(font.size for font in line_fonts) + max(0, len(lines) - 1) * line_gap
    label_height = spec.label_size + 38 if args.label else 0

    if args.platform == "wechat":
        y = max(spec.margin_y, spec.height - spec.margin_y - title_height - label_height)
    else:
        lower_anchor = int(spec.height * 0.44)
        max_y = spec.height - spec.margin_y - title_height - label_height - 96
        y = max(spec.margin_y, min(lower_anchor, max_y))
    x = spec.margin_x

    if args.label:
        y += draw_label_pill(draw, (x, y), args.label, label_font) + 34

    for line, font in zip(lines, line_fonts):
        draw_rich_line(draw, (x, y), line, font, args.highlight, stroke_width=3 if font.size > 90 else 2)
        y += font.size + line_gap

    underline_y = min(base.size[1] - 54, y + 16)
    draw.line((x, underline_y, x + 170, underline_y), fill=ACCENT, width=4)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    base.convert("RGB").save(output, quality=95)
    return output


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Source image path")
    parser.add_argument("--output", required=True, help="Output image path")
    parser.add_argument("--title", required=True, help="Cover title")
    parser.add_argument("--platform", choices=sorted(SPECS), default="wechat")
    parser.add_argument("--label", default="AI 产品工作新范式")
    parser.add_argument("--highlight", action="append", default=["AI Builder", "PM 不会消失"])
    parser.add_argument("--font", help="Optional Chinese-capable font path")
    parser.add_argument("--dim", type=float, default=0.72, help="Gradient darkness, 0-0.9")
    parser.add_argument("--remove-bottom-ratio", type=float, default=0.14)
    parser.add_argument("--max-lines", type=int, default=4)
    parser.add_argument("--label-size", type=int)
    return parser.parse_args(list(argv))


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    output = render_cover(args)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
