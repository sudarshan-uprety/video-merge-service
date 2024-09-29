import os

from celery import shared_task

from utils.variables import S3Bucket
from app.s3 import utils


@shared_task('upload_to_s3')
def upload_to_s3(file_location):
    s3 = utils.s3_client()
    with open(file_location, 'rb') as data:
        s3.put_object(
            Body=data,
            Bucket=S3Bucket,
            Key=file_location
        )

