BASE_NEGATIVE_PROMPT = """
no text, no logo, no watermark, no random letters, no misspelled words,
no fake user interface text, no messy typography, no poster layout,
no cartoon, no painting, no low resolution, no blur, no over-sharpened artifacts,
no distorted hands, no extra fingers, no distorted faces, no duplicate people,
no crowded scene, no clutter, no dark muddy shadows, no broken phone, no QR code
""".strip()


def get_negative_prompt(extra: str = "") -> str:
    extra = (extra or "").strip()
    if extra:
        return f"{BASE_NEGATIVE_PROMPT}, {extra}"
    return BASE_NEGATIVE_PROMPT
