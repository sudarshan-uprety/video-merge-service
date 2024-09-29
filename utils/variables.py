import os

from dotenv import load_dotenv

load_dotenv()


REDIS_URL = os.getenv('REDIS_URL')
AccountID = os.getenv('AccountID')
AWSAccessKeyId = os.getenv('AWSAccessKeyId')
AWSSecretKeyID = os.getenv('AWSSecretKeyId')
S3Bucket = os.getenv('S3Bucket')
