# Sample Python code for youtube.liveBroadcasts.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pprint
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import threading

from google.oauth2.credentials import Credentials


class YouTube():
    def __init__(self):
        self.youtube = None

    def start_poll(self):  # use lock
        threading.Timer(5.0, self.poll_chat).start()

    def get_saved_credentials(self, filename='youtube_oauth_creds.json'):
        fileData = {}
        try:
                with open(os.path.join('chatrooms/youtube', filename), 'r') as file:
                    fileData: dict = json.load(file)
        except FileNotFoundError:
            return None
        if fileData and 'refresh_token' in fileData and 'client_id' in fileData and 'client_secret' in fileData:
            return Credentials(**fileData)
        return None

    def store_creds(self, credentials, filename='youtube_oauth_creds.json'):
        if not isinstance(credentials, Credentials):
            return
        fileData = {'refresh_token': credentials.refresh_token,
                    'token': credentials.token,
                    'client_id': credentials.client_id,
                    'client_secret': credentials.client_secret,
                    'token_uri': credentials.token_uri}
        with open(os.path.join('chatrooms/youtube/', filename), 'w') as file:
            json.dump(fileData, file)
        print(f'Credentials serialized to {filename}.')

    def get_credentials_via_oauth(self, scopes, filename='client_secret.json', saveData=True) -> Credentials:
        '''Use data in the given filename to get oauth data
        '''
        iaflow: InstalledAppFlow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            filename, scopes)
        iaflow.run_local_server(
            host='localhost',
            port=8088,
            authorization_prompt_message='Please visit this URL: {url}',
            success_message='The auth flow is complete; you may close this window.',
            open_browser=True
        )
        if saveData:
            self.store_creds(iaflow.credentials)
        return iaflow.credentials

    def poll_chat(self):
        print("polling chat")
        request = self.youtube.liveBroadcasts().list(
            part="snippet,contentDetails,status",
            broadcastType="all",
            mine=True
        )
        response = request.execute()

        print('GETTING CHATS')

        if "liveChatId" in response["items"][0]["snippet"]:
            request = self.youtube.liveChatMessages().list(
                liveChatId=response["items"][0]["snippet"]["liveChatId"],
                part="snippet"
            )
        response = request.execute()
        pprint.pprint(response)
        self.start_poll()

    def get_live_broadcast(self):
        # -*- coding: utf-8 -*-
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "./chatrooms/youtube/client_secret.json"
        youtube_creds_filename = "youtube_oauth_creds.json"


        if os.path.exists(os.path.join('chatrooms/youtube', youtube_creds_filename)):
            creds = self.get_saved_credentials()
        else:
            creds = self.get_credentials_via_oauth(scopes, client_secrets_file)

        # Get credentials and create an API client
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=creds)

        request = self.youtube.liveBroadcasts().list(
            part="snippet,contentDetails,status",
            broadcastType="all",
            mine=True
        )
        response = request.execute()

        print('GETTING CHATS')

        if "liveChatId" in response["items"][0]["snippet"]:
            request = self.youtube.liveChatMessages().list(
                liveChatId=response["items"][0]["snippet"]["liveChatId"],
                part="snippet"
            )
        response = request.execute()
        print(response)
        self.start_poll()
