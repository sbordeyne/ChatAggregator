import requests
from authlib.integrations.requests_client import OAuth2Session
import webbrowser
from .errors import MixerException


def get_channel_id(username):
    response = requests.get(f"https://mixer.com/api/v1/channels/{username}?fields=id")
    if response.status_code == 200:
        return response.json()["id"]
    else:
        raise MixerException(f"Could not retrieve channel id : {response.json().get('message')}")


def get_oauth_authorization_uri(client_id, client_secret=None, scopes=None):
    if scopes is None:
        scopes = []
    endpoint = "https://mixer.com/oauth/authorize"
    client = OAuth2Session(client_id, client_secret, redirect_uri='http://localhost')
    uri, state = client.create_authorization_url(endpoint)
    webbrowser.open(uri)
    return


def get_mixer_header(oauth_token):
    return {"Authorization": f"Bearer {oauth_token}"}
