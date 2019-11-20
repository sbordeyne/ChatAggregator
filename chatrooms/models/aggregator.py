from copy import copy
from chatrooms import twitch, mixer, youtube


class Aggregator:
    def __init__(self, twitch_config=None, mixer_config=None, 
                 youtube_config=None, facebook_config=None):
        self._connected_chats = []
    
    def connect(self, twitch_config=None, mixer_config=None,
                youtube_config=None, facebook_config=None):
        
        if twitch_config is not None and "twitch" not in self._connected_chats:
            self.twitch = twitch.IRCThread(**twitch_config)
            self._connected_chats.append("twitch")
        
        if mixer_config is not None and "mixer" not in self._connected_chats:
            self.mixer = mixer.MixerThread(**mixer_config)
            self._connected_chats.append("mixer")
        
        if youtube_config is not None and "youtube" not in self._connected_chats:
            self.youtube = youtube.YoutubeThread(**youtube_config)
            self._connected_chats.append("youtube")
    
    def aggregate(self):
        messages = []
        def _sort(m):
            return m.timestamp
        
        if "twitch" in self._connected_chats:
            msg = ""
            while msg is not None:
                msg = self.twitch.last_message
                messages.append(msg)
        
        if "mixer" in self._connected_chats:
            msg = ""
            while msg is not None:
                msg = self.mixer.last_message
                messages.append(msg)
        
        
        if "youtube" in self._connected_chats:
            msg = ""
            while msg is not None:
                msg = self.youtube.last_message
                messages.append(msg)
        
        messages.sort(key=_sort)  # sorts the messages in ascending timestamp order (oldest first)
                                  # .sort sorts the list in place and is slightly faster than the sorted() built-in
        return messages

    def start(self):
        """
        Starts every valid thread.
        """
        if "twitch" in self._connected_chats:
            self.twitch.start()
        
        if "mixer" in self._connected_chats:
            self.mixer.start()
        
        
        if "youtube" in self._connected_chats:
            self.youtube.start()

    def quit(self):
        """
        Quits every started thread.
        """
        if "twitch" in self._connected_chats:
            self.twitch.quit()
        
        if "mixer" in self._connected_chats:
            self.mixer.quit()
        
        
        if "youtube" in self._connected_chats:
            self.youtube.quit()
