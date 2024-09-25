import logging
from fastapi import FastAPI, File
from celery.result import AsyncResult

from .schemas import VideoProcessingRequest, VideoProcessingStatus, AudioSource
from .utils import create_output_dirs, get_nepal_time
from ..utils.celery_worker import celery
from .merge_video.tasks import process_videos

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Video service.",
    description="This is a service which is responsible for merging multiple videos.",
    docs_url="/api/docs/",
)

