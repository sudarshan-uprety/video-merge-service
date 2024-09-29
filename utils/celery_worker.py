import os
import sys

from celery import Celery

from utils.variables import REDIS_URL

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

celery = Celery('tasks', broker=REDIS_URL, backend=REDIS_URL)


celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
celery.conf.broker_connection_retry_on_startup = True
celery.autodiscover_tasks(['app.merge_video'])
