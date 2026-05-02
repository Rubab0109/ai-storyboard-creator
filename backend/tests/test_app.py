import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))
from index import app  # noqa: E402

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_empty_image_prompt_validation():
    response = client.post("/api/generate-image", json={"prompt": ""})
    assert response.status_code == 422


def test_very_short_video_prompt_validation():
    response = client.post("/api/generate-video", json={"prompt": "hi"})
    assert response.status_code == 422


def test_invalid_duration_validation():
    response = client.post("/api/generate-video", json={"prompt": "A brave cup in a cartoon courtroom", "duration": 100})
    assert response.status_code == 422


def test_image_fallback_without_api_key():
    response = client.post(
        "/api/generate-image",
        json={
            "prompt": "A cute biscuit standing in a cinematic courtroom",
            "genre": "Comedy",
            "tone": "Funny",
            "style": "3D animated",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "image_generator"
    assert data["image_url"].startswith("data:image") or data["image_url"].startswith("http")


def test_video_fallback_without_api_key():
    response = client.post(
        "/api/generate-video",
        json={
            "prompt": "A biscuit and a tea cup become friends after a funny argument",
            "genre": "Comedy",
            "tone": "Emotional",
            "style": "vertical 3D animated cinematic",
            "duration": 15,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "video_generator"
    assert "video_prompt" in data
    assert isinstance(data["scenes"], list)
