# Example call to googles auth server
#
# https://accounts.google.com/o/oauth2/auth?
#   client_id=1084945748469-eg34imk572gdhu83gj5p0an9fut6urp5.apps.googleusercontent.com&
#   redirect_uri=http%3A%2F%2Flocalhost%2Foauth2callback&
#   scope=https://www.googleapis.com/auth/youtube&
#   response_type=code&
#   access_type=offline
import requests

class YouTubeConnection():
    def __init__(self):
        self.auth_server = "https://accounts.google.com/o/oauth2/auth?"
        self.client_id = ""
        self.redirect_uri = "http%3A%2F%2Flocalhost%2Foauth2callback"
        self.response_type = "code"
        self.scope = "https://www.googleapis.com/auth/youtube"
        self.access_type="offline"
        self.authorize()
        
    
    def authorize(self):
        r = requests.get(f"{self.auth_server}client_id={self.client_id}" \
                         f"&redirect_uri={self.redirect_uri}&scope={self.scope}" \
                         f"&response_type={self.response_type}&access_type={self.access_type}")
        print(r.status_code)
        print(r.json())

