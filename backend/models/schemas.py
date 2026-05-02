from pydantic import BaseModel, Field, field_validator


class ImageRequest(BaseModel):
    """Request body for the single image generator."""

    prompt: str = Field(..., min_length=3, max_length=4000)
    genre: str = Field(default="General", max_length=80)
    tone: str = Field(default="Cinematic", max_length=80)
    style: str = Field(default="3D animated cinematic", max_length=120)

    @field_validator("prompt")
    @classmethod
    def clean_prompt(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Prompt must contain at least 3 characters.")
        return cleaned


class VideoRequest(BaseModel):
    """Request body for the independent video generator."""

    prompt: str = Field(..., min_length=3, max_length=6000)
    genre: str = Field(default="General", max_length=80)
    tone: str = Field(default="Emotional", max_length=80)
    style: str = Field(default="vertical 3D cinematic animated story", max_length=150)
    duration: int = Field(default=15, ge=5, le=60)

    @field_validator("prompt")
    @classmethod
    def clean_prompt(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("Prompt must contain at least 3 characters.")
        return cleaned


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=3, max_length=5000)
