import tkinter.ttk as ttk
import tkinter as tk
import twitch_irc
from .labels import ChatLine
from . import utils


class _Chatbox(ttk.Frame):
    def __init__(self, master, irc_config=None, **kwargs):
        super().__init__(master, **kwargs)
        if irc_config is None:
            self.irc = twitch_irc.irc
        else:
            self.irc = twitch_irc.IRCThread(**irc_config)
        self.chat_list = []
        self.irc.start()

    def loop(self):
        message = twitch_irc.irc.last_message
        if message is not None:
            chat_line = ChatLine(self, name_text=message.get('display_name'),
                                 message_text=message.get('message'))
            chat_line.grid(row=len(self.chat_list), column=0, sticky="we")
            self.chat_list.append(chat_line)
            self.update()
            self.update_idletasks()


class Chatbox(ttk.Frame):
    def __init__(self, master=None, irc_config=None, **kwargs):
        super().__init__(master, **kwargs)
        self.vsb = ttk.Scrollbar(self)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                                yscrollcommand=lambda f, l: utils.auto_scroll(self.vsb, f, l))

        self.canvas.grid(row=0, column=0, sticky="nswe")

        self.vsb.config(command=self.canvas.yview)
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)
        interior_id = self._chatbox = _Chatbox(self.canvas, irc_config)
        self.canvas.create_window(0, 0, window=self._chatbox,
                                  anchor=tk.NW)
        self.vsb.grid(row=0, column=1, sticky='ns')

        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (self._chatbox.winfo_reqwidth(), self._chatbox.winfo_reqheight())
            self.canvas.config(scrollregion="0 0 %s %s" % size)
            if self._chatbox.winfo_reqwidth() != self.canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                self.canvas.config(width=self._chatbox.winfo_reqwidth())

        self._chatbox.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self._chatbox.winfo_reqwidth() != self.canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())

        self.canvas.bind('<Configure>', _configure_canvas)

    def loop(self):
        self._chatbox.loop()

    @property
    def irc(self):
        return self._chatbox.irc
