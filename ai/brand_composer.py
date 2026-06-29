from pathlib import Path
from textwrap import wrap

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ORANGE = (255, 95, 0)
WHITE = (255, 255, 255)
DARK = (8, 13, 24)
MUTED = (214, 220, 230)


def _font(size: int, bold: bool = False):
    """Cross-platform font loader with safe fallback."""
    candidates = []
    if bold:
        candidates += [
            "C:/Windows/Fonts/arialbd.ttf",
            "C:/Windows/Fonts/segoeuib.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        ]
    candidates += [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
    ]
    for path in candidates:
        try:
            if Path(path).exists():
                return ImageFont.truetype(path, size=size)
        except Exception:
            pass
    return ImageFont.load_default()


def _fit_text(draw, text, font, max_width, max_lines=3):
    words = (text or "").strip().split()
    if not words:
        return []
    lines = []
    current = ""
    for word in words:
        test = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
        if len(lines) >= max_lines:
            break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) == max_lines and len(" ".join(lines).split()) < len(words):
        lines[-1] = lines[-1].rstrip("., ") + "…"
    return lines


def _rounded_rect(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def compose_branded_creative(
    background_path: str,
    output_path: str,
    title: str = "Stay connected wherever you travel",
    subtitle: str = "Travel eSIMs for maps, rides, uploads, and real-time updates.",
    cta: str = "Explore plans at WoWoSIM",
    size=(1080, 1350),
    template_name: str = "Travel Tip",
    kicker: str | None = None,
):
    """Turn an AI background into a consistent WoWoSIM social creative.

    Image AI creates only the visual background. This function adds perfect
    text, brand pill, overlays, and CTA using Pillow.
    """
    w, h = size
    img = Image.open(background_path).convert("RGB")
    img_ratio = img.width / img.height
    target_ratio = w / h

    # Cover crop to target size.
    if img_ratio > target_ratio:
        new_h = h
        new_w = int(h * img_ratio)
    else:
        new_w = w
        new_h = int(w / img_ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - w) // 2
    top = (new_h - h) // 2
    img = img.crop((left, top, left + w, top + h))

    # Slight polish.
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=115, threshold=3))
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    # Top and bottom gradients for readability.
    for y in range(h):
        top_alpha = int(max(0, 150 * (1 - y / (h * 0.42)))) if y < h * 0.42 else 0
        bottom_alpha = int(max(0, 190 * ((y - h * 0.50) / (h * 0.50)))) if y > h * 0.50 else 0
        alpha = max(top_alpha, bottom_alpha)
        if alpha:
            od.line([(0, y), (w, y)], fill=(3, 7, 18, alpha))

    # Brand accent shapes.
    od.ellipse((w - 250, -120, w + 130, 260), fill=(255, 95, 0, 50))
    od.rounded_rectangle((48, 48, 320, 116), radius=28, fill=(8, 13, 24, 190), outline=(255, 255, 255, 50), width=2)
    od.ellipse((68, 63, 108, 103), fill=ORANGE + (255,))

    img = Image.alpha_composite(img.convert("RGBA"), overlay)
    d = ImageDraw.Draw(img)

    brand_font = _font(30, bold=True)
    small_font = _font(24, bold=True)
    title_font = _font(70, bold=True)
    subtitle_font = _font(32, bold=False)
    cta_font = _font(30, bold=True)
    micro_font = _font(23, bold=True)

    d.text((82, 66), "W", font=_font(26, bold=True), fill=WHITE)
    d.text((124, 66), "WoWoSIM", font=brand_font, fill=WHITE)

    # Text block card.
    template_kicker = (kicker or {
        "Travel Tip": "TRAVEL TIP",
        "Destination Highlight": "DESTINATION READY",
        "Breaking Trend": "TRENDING NOW",
        "FIFA / Event Travel": "EVENT TRAVEL",
        "Discount Offer": "LIMITED OFFER",
    }.get(template_name, "TRAVEL eSIM"))

    card_x, card_y = 54, h - 465
    card_w, card_h = w - 108, 360
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cd = ImageDraw.Draw(card)
    _rounded_rect(cd, (card_x, card_y, card_x + card_w, card_y + card_h), 34, (8, 13, 24, 210), (255, 255, 255, 45), 2)
    cd.rounded_rectangle((card_x + 30, card_y + 30, card_x + 210, card_y + 72), radius=18, fill=ORANGE + (255,))
    img = Image.alpha_composite(img, card)
    d = ImageDraw.Draw(img)

    d.text((card_x + 52, card_y + 38), template_kicker[:22], font=micro_font, fill=WHITE)

    title_lines = _fit_text(d, title, title_font, card_w - 72, max_lines=2)
    y = card_y + 96
    for line in title_lines:
        d.text((card_x + 34, y), line, font=title_font, fill=WHITE)
        y += 78

    subtitle_lines = _fit_text(d, subtitle, subtitle_font, card_w - 72, max_lines=2)
    y += 8
    for line in subtitle_lines:
        d.text((card_x + 36, y), line, font=subtitle_font, fill=MUTED)
        y += 44

    # CTA pill.
    cta_y = card_y + card_h - 82
    d.rounded_rectangle((card_x + 34, cta_y, card_x + 440, cta_y + 54), radius=24, fill=ORANGE)
    d.text((card_x + 62, cta_y + 12), cta[:32], font=cta_font, fill=WHITE)

    # Footer tag.
    d.text((card_x + card_w - 260, cta_y + 16), "No roaming stress", font=small_font, fill=(230, 235, 245))

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, quality=95)
    return str(output_path)
