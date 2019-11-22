import asyncio
import threading
from .connection import MixerConnection
from .utils import get_channel_id
from chatrooms import lock


class MixerThread(threading.Thread):
    def __init__(self, **kwargs):
        super().__init__()
        self.channel_id = get_channel_id(kwargs.pop("channel_name"))
        self.mixer_connection = MixerConnection(self.channel_id, 
                                                kwargs.pop("oauth_token", None))
    
    @property
    def last_message(self):
        """
        Pops the first text message from the queue.

        :return: str, first message of the queue.
        """
        try:
            return self.mixer_connection.messages.popleft()
        except IndexError:
            return None
    
    def run(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        with lock:
            asyncio.get_event_loop().run_until_complete(self.mixer_connection.run())
    
    def quit(self):
        self.mixer_connection.running = False
        asyncio.get_event_loop().close()