import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COVER_SIZE = (1200, 1600)
MARGIN = 100

# Calibre (a hard dependency) bundles Liberation; DejaVu is a common fallback
# on Debian/Ubuntu. If neither is present, Pillow's own scalable default font
# is used so cover generation never hard-fails on a missing system font.
_FONT_CANDIDATES = [
    "/usr/share/calibre/fonts/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
]


def generate_cover(title: str, dest: Path) -> Path:
    max_width = COVER_SIZE[0] - 2 * MARGIN
    max_height = COVER_SIZE[1] - 2 * MARGIN

    img = Image.new("RGB", COVER_SIZE, "white")
    draw = ImageDraw.Draw(img)

    font_size = 140
    font = _load_font(font_size)
    lines = _wrap(draw, title, font, max_width)
    line_height = font.getbbox("Ag")[3] + font_size // 5
    while line_height * len(lines) > max_height and font_size > 24:
        font_size -= 4
        font = _load_font(font_size)
        lines = _wrap(draw, title, font, max_width)
        line_height = font.getbbox("Ag")[3] + font_size // 5

    total_height = line_height * len(lines)
    y = MARGIN + (max_height - total_height) / 2
    for line in lines:
        width = draw.textlength(line, font=font)
        x = (COVER_SIZE[0] - width) / 2
        draw.text((x, y), line, font=font, fill="black")
        y += line_height

    img.save(dest, "JPEG", quality=90)
    return dest


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in _FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def _wrap(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    # Filenames rarely have spaces (e.g. "pr-24-explain-something"), so treat
    # hyphens and underscores as breakable too, not just whitespace.
    tokens = [t for t in re.split(r"(?<=[\s\-_])", text) if t]
    lines = []
    current = ""
    for token in tokens:
        candidate = current + token
        if not current.strip() or draw.textlength(candidate.strip(), font=font) <= max_width:
            current = candidate
        else:
            lines.append(current.strip())
            current = token
    if current.strip():
        lines.append(current.strip())
    return [piece for line in lines for piece in _break_overlong(draw, line, font, max_width)]


def _break_overlong(draw: ImageDraw.ImageDraw, line: str, font: ImageFont.FreeTypeFont, max_width: float) -> list[str]:
    if draw.textlength(line, font=font) <= max_width:
        return [line]
    pieces = []
    current = ""
    for ch in line:
        candidate = current + ch
        if not current or draw.textlength(candidate, font=font) <= max_width:
            current = candidate
        else:
            pieces.append(current)
            current = ch
    if current:
        pieces.append(current)
    return pieces
