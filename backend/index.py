from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from models.schemas import ImageRequest, TTSRequest, VideoRequest
from services.image_service import generate_image
from services.llm_service import create_video_plan, refine_image_prompt
from services.storage_service import save_metadata
from services.tts_service import generate_tts_audio
from services.video_service import generate_ai_video

load_dotenv()

app = FastAPI(
    title="AI Storyboard Creator API",
    description="Independent AI Image Generator and AI Video Generator backend.",
    version="1.0.0",
)

frontend_url = os.getenv("FRONTEND_URL", "*").strip() or "*"
allow_origins = [frontend_url] if frontend_url != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "app": "AI Storyboard Creator API",
        "status": "running",
        "modules": ["single_image_generator", "independent_video_generator"],
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/generate-image")
def generate_single_image(request: ImageRequest):
    """Generate exactly one image from a scene/script/prompt."""
    refined = refine_image_prompt(
        user_prompt=request.prompt,
        genre=request.genre,
        tone=request.tone,
        style=request.style,
    )
    image_result = generate_image(
        refined_prompt=refined["refined_prompt"],
        title=refined.get("title", "Generated Image"),
    )

    response = {
        "mode": "image_generator",
        "title": refined.get("title", "Generated Image"),
        "original_prompt": request.prompt,
        "genre": request.genre,
        "tone": request.tone,
        "style": request.style,
        "refined_prompt": refined["refined_prompt"],
        "negative_prompt": refined.get("negative_prompt"),
        "llm_provider": refined.get("llm_provider"),
        "image_url": image_result["image_url"],
        "image_provider": image_result["provider"],
        "image_status": image_result["status"],
    }
    response["storage"] = save_metadata("image", response)
    return response


@app.post("/api/generate-video")
def generate_independent_video(request: VideoRequest):
    """Generate an independent AI video plan and optional AI video output."""
    plan = create_video_plan(
        user_prompt=request.prompt,
        genre=request.genre,
        tone=request.tone,
        style=request.style,
        duration=request.duration,
    )
    video_result = generate_ai_video(plan["video_prompt"], request.duration)
    tts_result = generate_tts_audio(plan.get("narration", request.prompt))

    response = {
        "mode": "video_generator",
        "title": plan.get("title", "AI Generated Video"),
        "original_prompt": request.prompt,
        "genre": request.genre,
        "tone": request.tone,
        "style": request.style,
        "duration": request.duration,
        "video_prompt": plan["video_prompt"],
        "narration": plan.get("narration", request.prompt),
        "scenes": plan.get("scenes", []),
        "llm_provider": plan.get("llm_provider"),
        "video_url": video_result.get("video_url"),
        "video_provider": video_result.get("provider"),
        "video_status": video_result.get("status"),
        "video_message": video_result.get("message"),
        "audio_url": tts_result.get("audio_url"),
        "audio_provider": tts_result.get("provider"),
        "audio_status": tts_result.get("status"),
    }
    response["storage"] = save_metadata("video", response)
    return response


@app.post("/api/tts")
def tts(request: TTSRequest):
    return generate_tts_audio(request.text)
