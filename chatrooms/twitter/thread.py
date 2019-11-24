import threading
from chatrooms import lock


class TwitterThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
    
    @property
    def last_message(self):
        return None
    
    def run(self):
        while self.running:
            with lock:
                pass
    
    def quit(self):
        self.running = False
