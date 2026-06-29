from pathlib import Path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps


def cover_crop(img: Image.Image, size=(1080, 1350), anchor="center") -> Image.Image:
    """Resize and crop an image to fill the target canvas without stretching."""
    img = img.convert("RGB")
    target_w, target_h = size
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        new_h = target_h
        new_w = int(new_h * src_ratio)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)

    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    if anchor == "top":
        left = (new_w - target_w) // 2
        top = 0
    elif anchor == "bottom":
        left = (new_w - target_w) // 2
        top = max(0, new_h - target_h)
    elif anchor == "left":
        left = 0
        top = (new_h - target_h) // 2
    elif anchor == "right":
        left = max(0, new_w - target_w)
        top = (new_h - target_h) // 2
    else:
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2

    return img.crop((left, top, left + target_w, top + target_h))


def polish_background(img: Image.Image, size=(1080, 1350), anchor="center") -> Image.Image:
    """Prepare AI background for branded composition.

    This improves perceived sharpness without destroying the image.
    It is intentionally conservative because aggressive sharpening creates halos.
    """
    img = ImageOps.exif_transpose(img.convert("RGB"))
    img = cover_crop(img, size=size, anchor=anchor)

    # Mild enhancement only. The design engine will add readability overlays later.
    img = ImageEnhance.Contrast(img).enhance(1.06)
    img = ImageEnhance.Sharpness(img).enhance(1.18)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.15, percent=135, threshold=3))
    return img


def save_processed_background(img: Image.Image, output_path: str, size=(1080, 1350), anchor="center") -> str:
    out = polish_background(img, size=size, anchor=anchor)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    out.save(output_path, format="PNG", optimize=True)
    return str(output_path)
