# WoWoSIM AI Marketing Automation — Creative Director Version

This version is focused on **better social media image quality**.

Instead of asking the image model to create the whole ad, the app now uses this workflow:

1. Trend/post prompt
2. Creative Director AI creates a structured visual brief
3. Prompt Engineer builds a stronger image prompt
4. Gemini or Pollinations generates 1–4 background variations
5. The app scores the options
6. Brand Composer adds WoWoSIM branding, title, CTA, orange overlays, and clean text
7. Final image is saved locally

This avoids fake logos, broken letters, distorted brand text, and messy AI layouts.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Required for captions

Run Ollama locally:

```bash
ollama serve
ollama pull llama3.1:latest
ollama pull qwen3:8b
```

## Optional Gemini API for images

Create `.env` in the project folder:

```text
GEMINI_API_KEY=your_key_here
```

Then go to **Settings → Image Provider → gemini**.

If Gemini fails, enable fallback in Settings and the app will use Pollinations.

## New files in this version

```text
ai/creative_director.py
ai/design_templates.py
```

Main updated files:

```text
ai/image_engine.py
ai/brand_composer.py
ui/image_studio.py
```

## Best usage

1. Collect trends
2. Generate a post
3. Go to AI Creative Director
4. Select a template
5. Generate 4 variations
6. Download the best creative



## Gemini API Key from Settings

This version supports entering the Gemini API key inside the app.

1. Run the app.
2. Open **Settings & Model Manager**.
3. Paste your Gemini API key under **API Keys**.
4. Click **Save API Keys**.
5. Set **Default Image Provider** to `gemini`.
6. Set **Gemini Image Model** to `gemini-3.1-flash-image`.

The key is stored locally in SQLite on your PC. Do not share your database file publicly.
