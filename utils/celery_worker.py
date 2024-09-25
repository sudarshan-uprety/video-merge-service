import os
import sys

from celery import Celery

from utils.variables import REDIS_URL

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

print('hey'*100)
print(REDIS_URL)
celery = Celery('tasks', broker=REDIS_URL)


celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

celery.autodiscover_tasks(['app.merge_video'])
