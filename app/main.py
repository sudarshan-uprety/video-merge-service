import logging
from fastapi import FastAPI, File
from celery.result import AsyncResult

from .schemas import VideoProcessingRequest, VideoProcessingStatus, AudioSource
from .utils import create_output_dirs, get_nepal_time
from .celery_worker import celery
from .tasks import process_videos

# Configure logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.post("/merge_and_convert_videos/", response_model=VideoProcessingStatus)
async def merge_and_convert_videos(request: VideoProcessingRequest = File(...)):
    timestamp = get_nepal_time().strftime("%Y-%m-%d-%H-%M")
    cache_dir = "/app/cache_video/"
    create_output_dirs(cache_dir)
    base_dir = f"/app/videos/{timestamp}/"
    create_output_dirs(base_dir)

    video1_path = f"{cache_dir}{request.video1.filename}"
    video2_path = f"{cache_dir}{request.video2.filename}"

    # Save the uploaded videos to cache directory
    with open(video1_path, "wb") as f1:
        f1.write(await request.video1.read())
    with open(video2_path, "wb") as f2:
        f2.write(await request.video2.read())

    # Start the Celery task
    task = process_videos.delay(video1_path, video2_path, request.audio_from, timestamp)

    return VideoProcessingStatus(task_id=task.id, status="Processing")

@app.get("/video_status/{task_id}", response_model=VideoProcessingStatus)
async def get_video_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery)
    if task_result.ready():
        if task_result.successful():
            return VideoProcessingStatus(
                task_id=task_id,
                status="Completed",
                output_path=task_result.result
            )
        else:
            return VideoProcessingStatus(
                task_id=task_id,
                status="Failed",
                error=str(task_result.result)
            )
    else:
        return VideoProcessingStatus(task_id=task_id, status="Processing")

@app.get("/")
def read_root():
    return {"message": "Video merging API is running"}
