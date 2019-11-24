import threading
from collections import deque
import os
import datetime

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

from chatrooms.models.message import Message
from chatrooms import lock
from chatrooms.utils import get_timestamp_from_iso

import logging
import chatrooms.youtube.logging
from .auth import get_credentials_via_oauth, get_saved_credentials


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class YoutubeThread(threading.Thread):
    def __init__(self, config_path="./config/client_secret.json"):
        super().__init__()
        self.running = True
        self.messages = deque()
        self.config_path = config_path

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        api_service_name = "youtube"
        api_version = "v3"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.config_path, scopes)

        credentials = get_saved_credentials()
        if credentials is None:
            credentials = get_credentials_via_oauth(scopes, filename=self.config_path)
            
        self.api = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    @property
    def last_message(self):
        try:
            return self.messages.popleft()
        except IndexError:
            return None

    def parse_response(self, response):
        snippet = None
        try:
            items = response['items']
        except KeyError:
            return None

        messages = []

        for item in items:
            snippet = item['snippet']
            data = {"display_name": item["authorDetails"]["displayName"],
                    "message_id": item["id"],
                    "timestamp": get_timestamp_from_iso(snippet["publishedAt"]),
                    "user_id": snippet["authorChannelId"],
                    "channel_name": "",
                    "message": snippet["displayMessage"],
                    }
            messages.append(Message(**data))
        for m in messages:
            logging.info(str(m))
        self.messages.extend(messages)

    def run(self):
        while self.running:
            with lock:
                request = self.api.liveBroadcasts().list(  # TODO: We don't want mine=True, but we want to specify the livestream to connect to.
                    part="snippet,contentDetails,status",
                    broadcastType="all",
                    mine=True
                )
                response = request.execute()
                if "liveChatId" in response["items"][0]["snippet"]:
                    request = self.api.liveChatMessages().list(
                        liveChatId=response["items"][0]["snippet"]["liveChatId"],
                        part="snippet,authorDetails"
                    )
                response = request.execute()
                self.parse_response(response)

    def quit(self):
        self.running = False
