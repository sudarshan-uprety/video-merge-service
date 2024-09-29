import os
import json
import google_auth_oauthlib.flow
import googleapiclient.discovery

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


if __name__ == '__main__':
    get_refresh_token()
