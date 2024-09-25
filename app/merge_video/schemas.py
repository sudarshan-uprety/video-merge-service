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
    status: bool
    message: str
