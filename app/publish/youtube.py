import json
import google_auth_oauthlib.flow
import google.auth.transport.requests
import google.oauth2.credentials
from googleapiclient.discovery import build

# Define the OAuth 2.0 scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


def get_refresh_token():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)

    # Save the refresh token and client secrets for later use
    with open('refresh_token.json', 'w') as token_file:
        token_info = {
            'refresh_token': credentials.refresh_token,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret
        }
        json.dump(token_info, token_file)


def get_access_token():
    with open('refresh_token.json', 'r') as token_file:
        token_info = json.load(token_file)

    refresh_token = token_info['refresh_token']
    client_id = token_info['client_id']
    client_secret = token_info['client_secret']

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


def upload_video(file_path, title, description):
    credentials = get_access_token()
    youtube = build('youtube', 'v3', credentials=credentials)

    # Define the video body
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['tag1', 'tag2'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    # Call the API's videos.insert method
    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=file_path
    )

    response = request.execute()
