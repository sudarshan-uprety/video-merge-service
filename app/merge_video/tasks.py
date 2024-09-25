import subprocess
import os
import logging
from celery import shared_task
from app.merge_video.schemas import AudioSource


@shared_task(name="process_videos")
def process_videos(video1_path: str, video2_path: str, audio_from: AudioSource, timestamp: str):
    try:
        cache_dir = "/app/cache_video/"
        base_dir = f"/app/videos/{timestamp}/"
        merged_video_path = f"{cache_dir}/merged_video_{timestamp}.mp4"
        output_video_path = f"{base_dir}/output_video_{timestamp}.mp4"

        # Step 1: Scale and crop both videos to fit 1080x960 (half of 1080x1920)
        for i, video_path in enumerate([video1_path, video2_path], start=1):
            scale_command = [
                "ffmpeg", "-y", "-i", video_path,
                "-vf", "scale=1080:960:force_original_aspect_ratio=increase,crop=1080:960",
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
                f"{cache_dir}scaled_video{i}_{timestamp}.mp4"
            ]
            subprocess.run(scale_command, check=True)

        scaled_video1_path = f"{cache_dir}scaled_video1_{timestamp}.mp4"
        scaled_video2_path = f"{cache_dir}scaled_video2_{timestamp}.mp4"

        # Step 2: Merge the two scaled videos, stacking them vertically
        merge_command = [
            "ffmpeg", "-y", "-i", scaled_video1_path, "-i", scaled_video2_path,
            "-filter_complex", "[0:v][1:v]vstack=inputs=2[v]",
            "-map", "[v]", "-map", f"{0 if audio_from == AudioSource.VIDEO1 else 1}:a",
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23",
            "-c:a", "aac", "-b:a", "128k", merged_video_path
        ]
        subprocess.run(merge_command, check=True)

        # Rename the merged video to the final output path
        os.rename(merged_video_path, output_video_path)

        # Clean up temporary cache files
        for file in [video1_path, video2_path, scaled_video1_path, scaled_video2_path]:
            os.remove(file)

        # Trigger notification or callback here (e.g., send email, push notification, etc.)
        send_completion_notification(output_video_path)

        return output_video_path

    except subprocess.CalledProcessError as e:
        logging.error(f"Error during video processing: {str(e)}")
        raise Exception("Video processing failed")


def send_completion_notification(output_path):
    # Implement your notification logic here
    logging.info(f"Video processing completed. Output: {output_path}")
