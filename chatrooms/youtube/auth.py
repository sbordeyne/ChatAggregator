import logging
import json
import chatrooms.youtube.logging
import os
import os.path

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials


def get_saved_credentials(filename='youtube_oauth_creds.json'):
    file_data = {}
    try:
        with open(os.path.join('config/', filename), 'r') as file:
            file_data = json.load(file)
    except FileNotFoundError:
        return None
    if file_data and 'refresh_token' in file_data and 'client_id' in file_data and 'client_secret' in file_data:
        return Credentials(**file_data)
    return None


def store_creds(credentials, filename='youtube_oauth_creds.json'):
    if not isinstance(credentials, Credentials):
        return
    file_data = {'refresh_token': credentials.refresh_token,
                 'token': credentials.token,
                 'client_id': credentials.client_id,
                 'client_secret': credentials.client_secret,
                 'token_uri': credentials.token_uri}
    with open(os.path.join('config/', filename), 'w') as file:
        json.dump(file_data, file)
    logging.info(f'Credentials serialized to {filename}.')


def get_credentials_via_oauth(scopes, filename='client_secret.json', save_data=True) -> Credentials:
    '''Use data in the given filename to get oauth data
    '''
    iaflow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        filename, scopes)
    iaflow.run_local_server(
        host='localhost',
        port=8088,
        authorization_prompt_message='Please visit this URL: {url}',
        success_message='The auth flow is complete; you may close this window.',
        open_browser=True
    )
    if save_data:
        store_creds(iaflow.credentials)
    return iaflow.credentials
