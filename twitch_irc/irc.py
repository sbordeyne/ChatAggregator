import threading
import socket
import collections
import time
import logging
import re


from . import logging as log_config
from . import config


lock = threading.RLock()


twitch_args = ["irc.chat.twitch.tv", config.CHATBOT_NICK, config.CHATBOT_OAUTH, "dogeek"]
twitch_kwargs = {'reqs': ['twitch.tv/membership', 'twitch.tv/tags', 'twitch.tv/commands']}


class IRCThread(threading.Thread):
    message_parsing_re = re.compile(r'((@badge-info=(\d*))?;?'
                                    r'(badges=(\S+/\d+)*)?;?'
                                    r'(bits=(\d+))?;?'
                                    r'(color=(#[0-9ABCDEF]{6})?)?;?'
                                    r'(display-name=([A-Za-z0-9]+))?;?'
                                    r'(emotes=((\d+):((\d+-\d+,?)*)/?)*);?'
                                    r'(flags=)?;?'
                                    r'(id=([a-z0-9\-]+))?;?'
                                    r'(mod=(\d))?;?'
                                    r'(room-id=(\d+))?;?'
                                    r'(subscriber=(\d+))?;?'
                                    r'(tmi-sent-ts=(\d+))?;?'
                                    r'(turbo=(\d))?;?'
                                    r'(user-id=(\d+))?;?'
                                    r'(user-type=[ a-z]+)?)?'
                                    r':([A-Za-z0-9]+)!([A-Za-z0-9]+)@([A-Za-z0-9]+).tmi.twitch.tv '
                                    r'([A-Z]+) #([A-Za-z0-9]+)( :(.+))?')

    def __init__(self, server, nick, password, channel_name,
                 port=6667, reqs=None, max_messages=100, message_callbacks=None,
                 on_leave_callbacks=None, **kwargs):
        """
        IRC handler class, handling any IRC server, sending the necessary commands to join a
        channel automatically, setting the name and pass.

        :param server: server host name to join
        :param nick: nickname of the bot
        :param password: password or OAuth token to log in
        :param channel_name: channel name to join
        :param port: port for the IRC server (default : 6667)
        :param reqs: permission request list. Sends CAP REQ commands to the IRC server. (default : [])
        :param max_messages: maximum messages to send the server in 30 seconds. set to -1 for unlimited. (default:100)
        :param message_callbacks: dictionary of callable/list of callables to map to specific IRC commands received.
                                  callbacks will be passed a 'parsed' argument, which is the parsed text
                                  the bot received. 'parsed' is a dictionary with the following keys:
                                      {"badge_info", "badges", "bits", "color", "display_name", "emotes", "message_id",
                                       "mod", "room_id", "subscriber", "timestamp", "turbo", "user_id", "user",
                                       "command", "channel_name", "message"} (default: defaultdict(list))
        :param on_leave_callbacks: list of callables to call when the bot successfully
                                   parts the IRC server. (default: [])
        :param kwargs: kwargs to pass the threading.Thread superclass.
        """
        super().__init__(**kwargs)
        self.running = True
        self.message_queue = collections.deque()
        self.number_of_messages_sent = 0
        self.time_start_daemon = time.time()

        self.server = server
        self.nickname = nick
        self.password = password
        self.channel_name = channel_name
        self.port = port
        self.reqs = [] if reqs is None else reqs
        self.max_messages = max_messages

        if on_leave_callbacks is None:
            self.on_leave_callbacks = []
        elif callable(on_leave_callbacks):
            self.on_leave_callbacks = [on_leave_callbacks]
        elif isinstance(on_leave_callbacks, (list, tuple)):
            self.on_leave_callbacks = list(on_leave_callbacks)
        else:
            raise ValueError("on_leave_callbacks kwargs must be None, a callable, a list or a tuple")

        if message_callbacks is None:
            self.message_callbacks = collections.defaultdict(list)
        elif isinstance(message_callbacks, dict):
            for k in message_callbacks:
                if callable(message_callbacks[k]):
                    message_callbacks[k] = [message_callbacks[k]]
            self.message_callbacks = message_callbacks
        else:
            raise ValueError("message_callbacks kwargs must be None or a dictionary")

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))
        self.socket.setblocking(False)

        self.send(f"PASS {self.password}")
        self.send(f"NICK {self.nickname}")
        self.send(f"JOIN {self.channel_name}")
        for req in self.reqs:
            self.send(f"CAP REQ :{req}")
        self.send(':{0}!{0}@{0}.tmi.twitch.tv JOIN #{1}'.format(self.nickname, self.channel_name))

    def send(self, text):
        """
        Sends a command to the IRC server. Appends a newline if the text doesn't have one already.

        Silently fails if the amount of messages exceeds the limit.
        :param text: command to send the server.
        :return: Boolean. True if the command was sent successfully. False otherwise (the limit has been exceeded)
        """
        if self.number_of_messages_sent < self.max_messages or self.max_messages < 0:
            self.number_of_messages_sent += 1
            if not text.endswith("\n"):
                text += '\n'
            self.socket.send(text.encode("utf8"))
            return True
        else:
            return False

    def send_message(self, message):
        """
        Sends a text message using the PRIVMSG command.

        :param message: message to send to the server.
        :return: None
        """
        self.send(f"PRIVMSG #{self.channel_name} : {str(message)}")

    @property
    def last_message(self):
        """
        Pops the first text message from the queue.

        :return: str, first message of the queue.
        """
        return self.message_queue.popleft()

    def parse_message(self, text):
        """
        Parses a twitch IRC message using the self.message_parsing_re regex

        :param text: raw twitch IRC message
        :return: dictionary of parsed values.
        """
        res = self.message_parsing_re.search(text)

        if res is None:
            return {}

        # parse emote string separately cause it's complicated to use only regex for it
        # format : <emote ID>:<index_start>-<index_end>,<index_start>-<index_end>/
        #          <emote ID>:<index_start>-<index_end>...

        emotes = []
        if res.group(12):
            emote_str = res.group(12).split('=')[1]
            emote_str = emote_str.split("/")
            print(emote_str)
            for emote in emote_str:
                if emote:
                    emote_id, rest = emote.split(':')
                    indices = rest.split(",")
                    emotes.append({emote_id: indices})

        return {"badge_info": res.group(3),
                "badges": [] if res.group(5) is None else res.group(5).split(","),
                "bits": res.group(7),
                "color": res.group(9),
                "display_name": res.group(11),
                "emotes": emotes,
                "message_id": res.group(19),
                "mod": res.group(21),
                "room_id": res.group(23),
                "subscriber": res.group(25),
                "timestamp": res.group(27),
                "turbo": res.group(29),
                "user_id": res.group(31),
                "user": res.group(33),
                "command": res.group(36),
                "channel_name": res.group(37),
                "message": res.group(39)}

    def run(self):
        """
        Runs the thread and process messages.

        :return: None
        """
        while self.running:
            with lock:
                if int(time.time() - self.time_start_daemon) % 30 == 0:
                    self.number_of_messages_sent = 0
                try:
                    texts = self.socket.recv(4096).decode().split('\n')
                    for text in texts:
                        print(text)
                        logging.debug(text)
                        parsed = self.parse_message(text)
                        print(parsed)
                        if parsed.get("command") == 'PING':  # Prevent time out
                            self.send(f'PONG {parsed["message"]}\r')
                        elif parsed.get("command") == 'PRIVMSG':
                            self.message_queue.append(parsed)

                        for k in self.message_callbacks:
                            if parsed.get("command") == k.upper():
                                for cb in self.message_callbacks.get(k, []):
                                    cb(parsed)
                except socket.error as e:
                    if "10035" not in repr(e):
                        logging.exception("{} : {}".format(type(e), e))
                    continue

    def quit(self):
        """
        Quits the thread and stops the socket after parting the bot.

        :return: None
        """
        if self.socket.send('PART'.encode()):
            self.running = False
            self.socket.close()
            for cb in self.on_leave_callbacks:
                cb()


irc = IRCThread(*twitch_args, **twitch_kwargs)
