import requests
import socket


class MixerConnection:
    def __init__(self, channel_id, oauth_token):
        resp = requests.get(f"https://mixer.com/api/v1/chats/{channel_id}")
        