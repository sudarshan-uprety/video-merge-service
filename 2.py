import time
import random
import json
import logging
import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
DAILY_QUOTA = 10000
UPLOAD_COST = 1600  # Approximate cost for a video upload

class QuotaTracker:
    def __init__(self):
        self.used_quota = 0

    def can_make_request(self, cost):
        return (self.used_quota + cost) <= DAILY_QUOTA

    def update_quota(self, cost):
        self.used_quota += cost

quota_tracker = QuotaTracker()

def get_credentials():
    # Load refresh token and client secrets
    with open('refresh_token.json', 'r') as token_file:
        token_info = json.load(token_file)

    # Get the refresh token
    refresh_token = token_info['refresh_token']
    client_id = token_info['client_id']
    client_secret = token_info['client_secret']

    # Create credentials object
    credentials = google.oauth2.credentials.Credentials(
        None,
        refresh_token=refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id=client_id,
        client_secret=client_secret
    )

    # Refresh the access token
    credentials.refresh(google.auth.transport.requests.Request())
    return credentials

def upload_video_with_quota_check(file_path, title, description, max_retries=5):
    if not quota_tracker.can_make_request(UPLOAD_COST):
        raise Exception("Daily quota limit reached. Try again tomorrow.")

    credentials = get_credentials()
    youtube = build('youtube', 'v3', credentials=credentials)
    logging.info("YouTube API client built successfully")

    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['shorts', 'tag1', 'tag2'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    media = MediaFileUpload(file_path, resumable=True)
    logging.info(f"Attempting to upload video: {file_path}")

    for attempt in range(max_retries):
        try:
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            logging.info("Executing upload request")
            response = request.execute()
            quota_tracker.update_quota(UPLOAD_COST)
            logging.info(f"Video id '{response['id']}' was successfully uploaded.")
            logging.info(f"Estimated quota usage: {quota_tracker.used_quota}/{DAILY_QUOTA}")
            return response['id']
        except HttpError as e:
            logging.error(f"HTTP error occurred: {e.resp.status} {e.content}")
            if e.resp.status in [401, 403, 429] and 'quota' in str(e).lower():
                if attempt == max_retries - 1:
                    logging.error("Max retries reached. Raising exception.")
                    raise
                wait_time = (2 ** attempt) + random.random()
                logging.warning(f"Quota exceeded or unauthorized. Waiting for {wait_time:.2f} seconds before retrying.")
                time.sleep(wait_time)
            else:
                logging.error(f"Unhandled HTTP error: {str(e)}")
                raise
        except Exception as e:
            logging.error(f"Unexpected error: {str(e)}")
            raise

if __name__ == "__main__":
    video_file_path = "/Users/sudarshanuprety/Downloads/3.mp4"
    video_title = "My Uploaded Video"
    video_description = "This is a test video uploaded via the YouTube API"

    try:
        video_id = upload_video_with_quota_check(video_file_path, video_title, video_description)
        print(f"Video uploaded successfully. Video ID: {video_id}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
