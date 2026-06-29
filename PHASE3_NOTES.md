# Phase 3 — Marketing Brain

This sprint adds a structured creative workflow instead of sending one vague prompt to the image model.

## New modules

```text
ai/research_agent.py
ai/campaign_planner.py
ai/scene_planner.py
ai/prompt_library.py
ai/negative_prompts.py
ai/quality_scorer.py
ai/prompt_templates/*.md
```

## New workflow

```text
Topic / Post Image Prompt
↓
Research Agent
↓
Campaign Planner
↓
Scene Planner
↓
Prompt Engine
↓
Generate 1–4 background options
↓
Quality Scorer
↓
Brand Composer
↓
Final WoWoSIM PNG
```

## Notes

- Pollinations is still free but less predictable than paid image APIs.
- Gemini image models may require paid quota, even if the text API key works.
- The design engine adds the final text/logo/CTA, so image providers should only generate clean backgrounds.
