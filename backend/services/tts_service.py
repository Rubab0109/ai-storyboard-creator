import base64
import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def generate_tts_audio(text: str) -> Dict[str, str | None]:
    """Optional ElevenLabs TTS. Browser speech fallback is used when missing/failing."""
    api_key = os.getenv("ELEVENLABS_API_KEY", "").strip()
    voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")

    if not api_key:
        return {
            "audio_url": None,
            "provider": "browser_speech_fallback",
            "status": "fallback_no_tts_key",
        }

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text[:4500],
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.75},
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=45)
        response.raise_for_status()
        encoded = base64.b64encode(response.content).decode("utf-8")
        return {
            "audio_url": f"data:audio/mpeg;base64,{encoded}",
            "provider": "elevenlabs",
            "status": "success",
        }
    except Exception as exc:
        return {
            "audio_url": None,
            "provider": "browser_speech_fallback",
            "status": f"fallback_tts_error: {str(exc)[:160]}",
        }
