import tkinter as tk
from tkinter.font import Font
from .chatbox import Chatbox
from .entries import EntryWithPlaceholder


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        self.chat_string = tk.StringVar()
        self.chatbox = Chatbox()
        self.entry_font = Font(family='TkTextFont', size=8)
        self.chat_entry = EntryWithPlaceholder(self, placeholder="Chat...",
                                               textvariable=self.chat_string,
                                               font=self.entry_font)
        self.chat_entry.bind('<Return>', self.on_chat_send_message)
        self.master.bind('<Configure>', self.on_configure)
        self.chatbox.grid(row=0, column=0, sticky='nswe')
        self.chat_entry.grid(row=1, column=0, sticky="we", padx=0)
        self.loop()
        
    def loop(self):
        self.chatbox.loop()
        self.after(5, self.loop)

    def on_chat_send_message(self, *event):
        self.chatbox.irc.send_message(self.chat_string.get())
        self.chat_string.set("")
        self.chat_entry.foc_out(*event)

    def on_configure(self, *event):
        self.update_idletasks()
        w = self.master.winfo_width()
        avg_character_width = 6.1923076923076925
        target_width = int(w / avg_character_width)
        self.chat_entry.config(width=target_width)
        self.update()

    def on_close(self):
        self.chatbox.irc.quit()
        self.master.destroy()

