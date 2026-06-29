from pathlib import Path
from typing import Dict

from PIL import Image, ImageStat, ImageFilter


def _laplacian_proxy(img: Image.Image) -> float:
    gray = img.convert("L").resize((256, 256))
    edges = gray.filter(ImageFilter.FIND_EDGES)
    stat = ImageStat.Stat(edges)
    return float(stat.mean[0])


def _brightness_score(img: Image.Image) -> float:
    stat = ImageStat.Stat(img.convert("L").resize((256, 256)))
    mean = float(stat.mean[0])
    # Favor mid-to-bright images; very dark or blown-out images lose points.
    return max(0, 100 - abs(mean - 145) * 0.9)


def _negative_space_score(img: Image.Image, preferred: str = "upper") -> float:
    w, h = img.size
    crop = img.crop((0, 0, w, int(h * 0.42))) if preferred == "upper" else img.crop((0, int(h * 0.58), w, h))
    small = crop.convert("L").resize((128, 64))
    stat = ImageStat.Stat(small)
    # Lower stddev generally means cleaner space for text, but not completely flat.
    std = float(stat.stddev[0])
    return max(0, min(100, 115 - std * 1.4))


def score_image_file(path: str, prompt: str = "", scene: Dict | None = None) -> Dict:
    scene = scene or {}
    try:
        img = Image.open(path).convert("RGB")
        sharp = min(100, _laplacian_proxy(img) * 3.2)
        bright = _brightness_score(img)
        space = _negative_space_score(img, "upper")
        composition = 76
        text = (prompt + " " + str(scene)).lower()
        for kw in ["negative space", "clean", "premium", "sharp", "realistic", "golden", "commercial"]:
            if kw in text:
                composition += 3
        composition = min(96, composition)
        final = round((sharp * 0.30) + (bright * 0.20) + (space * 0.25) + (composition * 0.25))
        return {
            "final": int(max(1, min(99, final))),
            "sharpness": round(sharp, 1),
            "brightness": round(bright, 1),
            "text_space": round(space, 1),
            "composition": round(composition, 1),
        }
    except Exception:
        return {"final": 50, "sharpness": 0, "brightness": 0, "text_space": 0, "composition": 50}
