from .irc import IRCThread
from . import config

twitch_config = {"server": "irc.chat.twitch.tv",
                 "nick": config.CHATBOT_NICK,
                 "oauth": config.CHATBOT_OAUTH,
                 "channel_name": None,
                 "port": 6667,
                 'reqs': ['twitch.tv/membership', 
                          'twitch.tv/tags', 
                          'twitch.tv/commands']
                 }