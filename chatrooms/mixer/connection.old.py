import requests
import socket
from .utils import get_mixer_header
import websockets
from collections import deque


class MixerConnection:
    def __init__(self, channel_id, oauth_token):
        self.channel_id = channel_id
        self.oauth_token = oauth_token
        resp = requests.get(f"https://mixer.com/api/v1/chats/{channel_id}", 
                            headers=get_mixer_header(oauth_token)).json()
        self.authkey = resp.get("authkey")
        self.endpoints = resp.get("endpoints")
        self.messages = deque()
        self.running = True
    
    async def run(self):
        for endpoint in self.endpoints:
            async with websockets.connect(endpoint) as ws:
                while self.running:
                    self.messages.append(await ws.recv())