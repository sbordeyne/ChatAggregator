# Sample Python code for youtube.liveBroadcasts.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pprint

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors



class YouTube():
    def __init__(self):
        pass

    @staticmethod
    def get_live_broadcast():
        # -*- coding: utf-8 -*-
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "./chatrooms/youtube/client_secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = youtube.liveBroadcasts().list(
            part="snippet,contentDetails,status",
            broadcastType="all",
            mine=True
        )
        response = request.execute()

        pprint.pprint(response)
        print('<-----LIVE CHAT----->')
   

        request = youtube.liveChatMessages().list(
            liveChatId="Cg0KC2dzRVR6VVF5S1RnKicKGFVDX0RuNnJUYmJWZ2dXT05adGd6VkhJURILZ3NFVHpVUXlLVGc",
            part="snippet"
        )
        response = request.execute()

        print(response)


