from pathlib import Path
import random
from typing import Dict, List, Tuple

from config import IMAGE_DIR
from database.database import insert_image, get_setting
from ai.image_providers import pollinations, gemini
from ai.brand_composer import compose_branded_creative
from ai.background_processor import save_processed_background
from ai.research_agent import research_topic
from ai.campaign_planner import plan_campaign
from ai.scene_planner import create_scene_plan
from ai.prompt_engine import make_prompt_variations_from_plan, optimize_background_prompt
from ai.quality_scorer import score_image_file
from ai.design_templates import get_template

IMAGE_DIR.mkdir(parents=True, exist_ok=True)


def _safe_canvas_request(width: int, height: int, provider: str) -> Tuple[int, int]:
    quality_mode = get_setting("background_quality_mode", "high")
    if quality_mode == "fast":
        return width, height
    if provider == "pollinations":
        return 1280, 1280
    return 1536, 1536


def _save_raw_image(img, prefix="background"):
    seed = random.randint(10000, 999999)
    path = IMAGE_DIR / f"{prefix}_{seed}.png"
    img.save(path, format="PNG", optimize=True)
    return str(path)


def _save_processed_image(img, width: int, height: int, anchor="center", prefix="processed"):
    seed = random.randint(10000, 999999)
    path = IMAGE_DIR / f"{prefix}_{seed}.png"
    return save_processed_background(img, str(path), size=(width, height), anchor=anchor)


def _generate_background(final_prompt, width, height, provider, model):
    request_w, request_h = _safe_canvas_request(width, height, provider)
    if provider == "gemini":
        image_model = model or get_setting("gemini_image_model", "gemini-3.1-flash-image")
        return gemini.generate(final_prompt, width=request_w, height=request_h, model=image_model)
    image_model = model or get_setting("pollinations_image_model", "turbo")
    # Pollinations is URL-based; keep prompts compact and safe.
    safe_prompt = optimize_background_prompt(final_prompt)
    return pollinations.generate(safe_prompt, width=request_w, height=request_h, model=image_model)


def generate_image(
    prompt,
    post_id=None,
    width=1080,
    height=1350,
    provider=None,
    model=None,
    title=None,
    caption=None,
    cta="Explore plans at WoWoSIM",
    compose=True,
    template_name="Travel Tip",
):
    result = generate_creative_set(
        prompt=prompt,
        post_id=post_id,
        width=width,
        height=height,
        provider=provider,
        model=model,
        title=title,
        caption=caption,
        cta=cta,
        compose=compose,
        template_name=template_name,
        variations=1,
    )
    return result["best"]["final_path"]


def generate_creative_set(
    prompt,
    post_id=None,
    width=1080,
    height=1350,
    provider=None,
    model=None,
    title=None,
    caption=None,
    cta="Explore plans at WoWoSIM",
    compose=True,
    template_name="Travel Tip",
    variations=4,
) -> Dict[str, List[Dict]]:
    """Phase 3 Marketing Brain pipeline.

    1. Research Agent explains the topic and brand angle.
    2. Campaign Planner chooses campaign type, template, CTA, and tone.
    3. Scene Planner produces a structured photography brief.
    4. Prompt Engine creates provider-safe prompt variations.
    5. Image provider generates backgrounds.
    6. Local processor crops/sharpens.
    7. Quality scorer picks the best option.
    8. Brand composer adds the WoWoSIM design layer.
    """
    provider = (provider or get_setting("image_provider", "pollinations")).strip().lower()
    fallback_enabled = get_setting("image_fallback", "yes") == "yes"

    research = research_topic(prompt, caption or "")
    campaign = plan_campaign(prompt, research, platform="Instagram")

    # Manual UI template choice still wins if the user chose one explicitly.
    if template_name:
        campaign["template"] = template_name
    template = get_template(campaign.get("template", template_name or "Travel Tip"))
    cta = cta or campaign.get("cta") or template.get("cta") or "Explore WoWoSIM eSIM plans"

    scene = create_scene_plan(prompt, research, campaign)
    crop_anchor = scene.get("crop_anchor", "center")
    prompt_variations = make_prompt_variations_from_plan(prompt, research, campaign, scene, count=variations)

    outputs = []
    for idx, final_prompt in enumerate(prompt_variations, start=1):
        try:
            img = _generate_background(final_prompt, width, height, provider, model)
            used_provider = provider
        except Exception as first_error:
            if provider != "pollinations" and fallback_enabled:
                fallback_prompt = optimize_background_prompt(final_prompt)
                img = pollinations.generate(fallback_prompt, width=1280, height=1280, model="turbo")
                used_provider = "pollinations-fallback"
            else:
                raise first_error

        raw_path = _save_raw_image(img, prefix=f"wowosim_raw_v{idx}_{post_id or 'image'}")
        processed_path = _save_processed_image(
            img,
            width=width,
            height=height,
            anchor=crop_anchor,
            prefix=f"wowosim_bg_sharp_v{idx}_{post_id or 'image'}",
        )

        score_details = score_image_file(processed_path, final_prompt, scene)
        score = int(score_details.get("final", 50))

        if compose:
            seed = random.randint(10000, 999999)
            final_path = IMAGE_DIR / f"wowosim_final_v{idx}_{post_id or 'image'}_{seed}.png"
            subtitle = (caption or research.get("brand_connection") or template.get("subtitle") or "Travel eSIMs for maps, rides, uploads, and real-time updates.").strip()
            if len(subtitle.split()) > 18:
                subtitle = " ".join(subtitle.split()[:18]) + "…"
            output_path = compose_branded_creative(
                processed_path,
                str(final_path),
                title=title or campaign.get("headline_direction") or "Stay connected wherever you travel",
                subtitle=subtitle,
                cta=cta,
                size=(width, height),
                template_name=campaign.get("template", template_name),
                kicker=template.get("kicker"),
            )
        else:
            output_path = processed_path

        stored_prompt = (
            f"PHASE 3 MARKETING BRAIN\n\n"
            f"RESEARCH:\n{research}\n\n"
            f"CAMPAIGN PLAN:\n{campaign}\n\n"
            f"SCENE PLAN:\n{scene}\n\n"
            f"PRODUCTION PROMPT VARIATION {idx}:\n{final_prompt}\n\n"
            f"PROVIDER: {used_provider}\nSCORE: {score}\nSCORE DETAILS: {score_details}\nTEMPLATE: {campaign.get('template')}\n"
            f"RAW: {raw_path}\nPROCESSED: {processed_path}"
        )
        if post_id:
            insert_image(post_id, output_path, stored_prompt)

        outputs.append({
            "index": idx,
            "score": score,
            "score_details": score_details,
            "provider": used_provider,
            "raw_path": raw_path,
            "processed_path": processed_path,
            "final_path": output_path,
            "prompt": final_prompt,
        })

    best = sorted(outputs, key=lambda x: x["score"], reverse=True)[0]
    return {
        "research": research,
        "campaign": campaign,
        "scene": scene,
        "brief": {"research": research, "campaign": campaign, "scene": scene},
        "outputs": outputs,
        "best": best,
    }
