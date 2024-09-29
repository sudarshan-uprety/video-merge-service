import boto3

from utils.variables import AWSAccessKeyId, AWSSecretKeyID


def s3_client():
    client = boto3.client(
        's3', region_name='ap-south-1',
        aws_access_key_id=AWSAccessKeyId,
        aws_secret_access_key=AWSSecretKeyID

    )
    return client
