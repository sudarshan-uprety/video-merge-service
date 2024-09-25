from typing import Optional
from enum import Enum

from fastapi import UploadFile
from pydantic import BaseModel


class AudioSource(str, Enum):
    VIDEO1 = "video1"
    VIDEO2 = "video2"


class VideoProcessingRequest(BaseModel):
    video1: UploadFile
    video2: UploadFile
    audio_from: AudioSource


class VideoProcessingResponse(BaseModel):
    instagram_tiktok_facebook_video: str
    youtube_reels_video: str


class VideoProcessingStatus(BaseModel):
    task_id: str
    status: str
    output_path: Optional[str] = None
    error: Optional[str] = None

