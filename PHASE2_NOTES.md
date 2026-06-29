# Phase 2 — Creative Director + Sharper Backgrounds

This version improves the image pipeline without asking Gemini/Pollinations to create the full ad.

## What changed

- Added `ai/background_processor.py`
- Updated `ai/creative_director.py`
- Updated `ai/image_engine.py`
- Updated `ui/image_studio.py`
- Updated `ui/settings.py`

## New image pipeline

```text
Trend / Image Prompt
↓
Creative Director JSON brief
↓
Production prompt with text-safe composition
↓
Generate 1–4 larger AI backgrounds
↓
Crop + resize + sharpen locally
↓
Brand composer adds WoWoSIM layout
↓
Final PNG
```

## Important setting

Go to **Settings → Background Quality Mode**.

- `high`: requests a larger background and sharpens locally. Better quality.
- `fast`: uses the final size directly. Faster but softer.

## Recommended

For best quality:

```text
Image Provider: gemini
Gemini Image Model: gemini-3.1-flash-image
Background Quality Mode: high
Variations: 4
```

If Gemini fails, enable Pollinations fallback.
