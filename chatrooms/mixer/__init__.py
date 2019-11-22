'''Chat Bot Stuff'''

from .connection import Connection

from .event_handler import Handler as ChatEventHandler

def create(*args, **kwargs):
    """Helper function for the creation of connections."""
    return Connection(*args, **kwargs)
