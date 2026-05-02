import os
import time
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_ai_video(video_prompt: str, duration: int) -> Dict[str, Any]:
    """Try optional Replicate video generation. Otherwise return frontend animated preview fallback.

    This keeps Vercel deployment lightweight and prevents MoviePy/binary dependency errors.
    """
    token = os.getenv("REPLICATE_API_TOKEN", "").strip()
    model = os.getenv("REPLICATE_VIDEO_MODEL", "").strip()

    if not token or not model:
        return {
            "video_url": None,
            "provider": "frontend_animated_preview_fallback",
            "status": "fallback_no_video_api_key",
            "message": "No video API configured. Frontend will create an animated vertical preview from the AI video plan.",
        }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Prefer": "wait=10",
    }

    payload = {
        "input": {
            "prompt": video_prompt,
            "duration": duration,
            "aspect_ratio": "9:16",
        }
    }

    try:
        create_url = f"https://api.replicate.com/v1/models/{model}/predictions"
        response = requests.post(create_url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        prediction = response.json()

        get_url = prediction.get("urls", {}).get("get")
        if not get_url:
            return {
                "video_url": None,
                "provider": "replicate",
                "status": "pending_without_poll_url",
                "message": "Video job created but no polling URL returned.",
            }

        for _ in range(5):
            poll = requests.get(get_url, headers={"Authorization": f"Bearer {token}"}, timeout=20)
            poll.raise_for_status()
            data = poll.json()
            status = data.get("status")
            if status == "succeeded":
                output = data.get("output")
                if isinstance(output, list) and output:
                    output = output[0]
                return {"video_url": output, "provider": "replicate", "status": "success"}
            if status in {"failed", "canceled"}:
                return {"video_url": None, "provider": "replicate", "status": status, "message": str(data.get("error", "Video failed"))}
            time.sleep(2)

        return {
            "video_url": None,
            "provider": "replicate",
            "status": "processing",
            "message": "Video is still processing. Use fallback preview now or check provider dashboard.",
        }
    except Exception as exc:
        return {
            "video_url": None,
            "provider": "frontend_animated_preview_fallback",
            "status": f"fallback_video_api_error: {str(exc)[:160]}",
            "message": "Video API failed, so frontend will show animated preview fallback.",
        }
