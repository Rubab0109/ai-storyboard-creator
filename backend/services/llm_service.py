import json
import os
import re
from typing import Any, Dict, List

import requests
from dotenv import load_dotenv

load_dotenv()


def _extract_json(text: str) -> Dict[str, Any]:
    """Extract JSON safely from an LLM response."""
    try:
        return json.loads(text)
    except Exception:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return {}
    return {}


def _call_gemini(prompt: str) -> str | None:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.75,
            "maxOutputTokens": 1600,
        },
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return None


def _call_openai_chat(prompt: str) -> str | None:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    if not api_key:
        return None

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a professional AI multimedia prompt engineer. Return only valid JSON when JSON is requested."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
    }

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception:
        return None


def _llm(prompt: str) -> str | None:
    """Try Gemini first, then OpenAI. Return None if no key/API fails."""
    return _call_gemini(prompt) or _call_openai_chat(prompt)


def refine_image_prompt(user_prompt: str, genre: str, tone: str, style: str) -> Dict[str, str]:
    """Create one polished image prompt. This is not a storyboard flow."""
    prompt = f"""
Return only valid JSON.
Create ONE professional AI image prompt from the user request.
Do not split into multiple scenes. Do not create storyboard.

User request: {user_prompt}
Genre: {genre}
Tone: {tone}
Visual style: {style}

JSON format:
{{
  "title": "short image title",
  "refined_prompt": "highly detailed single image prompt, vertical or horizontal depending on content, cinematic lighting, subject details, environment, mood, camera angle",
  "negative_prompt": "things to avoid"
}}
""".strip()

    raw = _llm(prompt)
    if raw:
        data = _extract_json(raw)
        if data.get("refined_prompt"):
            return {
                "title": str(data.get("title", "Generated Image")),
                "refined_prompt": str(data["refined_prompt"]),
                "negative_prompt": str(data.get("negative_prompt", "blurry, distorted, low quality, extra fingers, unreadable text")),
                "llm_provider": "gemini_or_openai",
            }

    fallback = (
        f"Create one high-quality {style} image. Genre: {genre}. Tone: {tone}. "
        f"Scene/request: {user_prompt}. Use cinematic composition, professional lighting, clear subject, "
        f"detailed background, expressive mood, sharp focus, modern creative multimedia style."
    )
    return {
        "title": "Generated Image",
        "refined_prompt": fallback,
        "negative_prompt": "blurry, distorted, low quality, watermark, unreadable text",
        "llm_provider": "local_fallback",
    }


def _fallback_scenes(user_prompt: str, duration: int, style: str, tone: str) -> List[Dict[str, Any]]:
    scene_count = 4 if duration <= 20 else 6
    parts = [
        "opening visual introduction",
        "main character or subject appears",
        "conflict or important moment",
        "emotional turning point",
        "final reveal or message",
        "closing cinematic shot",
    ][:scene_count]
    seconds = max(2, round(duration / scene_count))

    return [
        {
            "scene_number": index + 1,
            "caption": part.title(),
            "visual_prompt": f"{style}, {tone} tone, vertical 9:16 scene about: {user_prompt}. Moment: {part}. Cinematic lighting, animated storytelling, expressive character focus.",
            "camera_motion": "slow zoom with gentle pan",
            "duration_seconds": seconds,
        }
        for index, part in enumerate(parts)
    ]


def create_video_plan(user_prompt: str, genre: str, tone: str, style: str, duration: int) -> Dict[str, Any]:
    """Create an independent video plan for the video generator only."""
    prompt = f"""
Return only valid JSON.
Create a short AI video generation plan. This is separate from image generation.
The output should look like a vertical social media cinematic animated story video.

User video idea/script/prompt: {user_prompt}
Genre: {genre}
Tone: {tone}
Visual style: {style}
Duration: {duration} seconds

The style should be inspired by vertical 9:16 short animated cinematic videos with emotional storytelling, smooth transitions, captions, and narration.

JSON format:
{{
  "title": "short video title",
  "video_prompt": "single detailed prompt for an AI video model",
  "narration": "short narration voiceover text",
  "scenes": [
    {{
      "scene_number": 1,
      "caption": "short caption",
      "visual_prompt": "detailed visual prompt for this video scene",
      "camera_motion": "camera movement",
      "duration_seconds": 3
    }}
  ]
}}
""".strip()

    raw = _llm(prompt)
    if raw:
        data = _extract_json(raw)
        if data.get("video_prompt") and isinstance(data.get("scenes"), list):
            return {
                "title": str(data.get("title", "AI Generated Video")),
                "video_prompt": str(data["video_prompt"]),
                "narration": str(data.get("narration", user_prompt)),
                "scenes": data["scenes"][:8],
                "llm_provider": "gemini_or_openai",
            }

    scenes = _fallback_scenes(user_prompt, duration, style, tone)
    return {
        "title": "AI Video Story",
        "video_prompt": (
            f"Generate a {duration}-second vertical 9:16 {style} video. Genre: {genre}. "
            f"Tone: {tone}. Story/script: {user_prompt}. Use emotional storytelling, smooth transitions, "
            f"cinematic lighting, animated characters, subtitles, and social media short-video pacing."
        ),
        "narration": f"{user_prompt}. A short cinematic story unfolds with emotional visuals and smooth movement.",
        "scenes": scenes,
        "llm_provider": "local_fallback",
    }
