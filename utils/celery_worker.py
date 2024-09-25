import os
from celery import Celery

# Create a Celery instance with the Redis URL from environment variables
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
celery = Celery('tasks', broker=redis_url)

# Import the tasks module to ensure all tasks are registered
from app.merge_video import tasks

# Optional: Configure Celery
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)