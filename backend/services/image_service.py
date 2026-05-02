import base64
import html
import os
import textwrap
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def _svg_placeholder(prompt: str, title: str = "AI Image Preview") -> str:
    """Create a safe SVG placeholder when no image API is configured."""
    safe_title = html.escape(title[:80])
    short_prompt = html.escape(prompt[:260])
    wrapped = textwrap.wrap(short_prompt, width=42)[:7]
    lines = "".join(
        f'<text x="64" y="{250 + i * 34}" fill="#dbeafe" font-size="22" font-family="Arial">{line}</text>'
        for i, line in enumerate(wrapped)
    )
    svg = f"""
<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#0f172a"/>
      <stop offset="45%" stop-color="#312e81"/>
      <stop offset="100%" stop-color="#020617"/>
    </linearGradient>
    <radialGradient id="r" cx="50%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#60a5fa" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0f172a" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect width="1024" height="1024" fill="url(#g)"/>
  <rect width="1024" height="1024" fill="url(#r)"/>
  <circle cx="780" cy="180" r="130" fill="#a855f7" opacity="0.25"/>
  <circle cx="230" cy="780" r="180" fill="#06b6d4" opacity="0.18"/>
  <rect x="54" y="54" width="916" height="916" rx="42" fill="none" stroke="#93c5fd" stroke-width="4" opacity="0.55"/>
  <text x="64" y="140" fill="#ffffff" font-size="48" font-weight="700" font-family="Arial">{safe_title}</text>
  <text x="64" y="195" fill="#93c5fd" font-size="24" font-family="Arial">Fallback preview generated because image API is not configured.</text>
  {lines}
  <text x="64" y="910" fill="#a7f3d0" font-size="24" font-family="Arial">Set OPENAI_API_KEY for real AI image generation.</text>
</svg>
""".strip()
    encoded = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{encoded}"


def generate_image(refined_prompt: str, title: str = "Generated Image") -> Dict[str, str]:
    """Generate one image. If API is missing/fails, return placeholder instead of crashing."""
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    image_model = os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-1")

    if not api_key:
        return {
            "image_url": _svg_placeholder(refined_prompt, title),
            "provider": "placeholder_fallback",
            "status": "fallback_no_openai_key",
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": image_model,
        "prompt": refined_prompt,
        "size": "1024x1024",
        "n": 1,
    }

    try:
        response = requests.post("https://api.openai.com/v1/images/generations", headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        first = data.get("data", [{}])[0]

        if first.get("url"):
            return {"image_url": first["url"], "provider": "openai", "status": "success"}
        if first.get("b64_json"):
            return {
                "image_url": f"data:image/png;base64,{first['b64_json']}",
                "provider": "openai",
                "status": "success",
            }
    except Exception as exc:
        return {
            "image_url": _svg_placeholder(refined_prompt, title),
            "provider": "placeholder_fallback",
            "status": f"fallback_image_api_error: {str(exc)[:140]}",
        }

    return {
        "image_url": _svg_placeholder(refined_prompt, title),
        "provider": "placeholder_fallback",
        "status": "fallback_unexpected_image_response",
    }
