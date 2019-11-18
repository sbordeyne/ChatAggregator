import tkinter.ttk as ttk
import tkinter as tk
import textwrap


class ChatLine(ttk.Frame):
    def __init__(self, master=None, name_text=None, message_text=None):
        super().__init__(master)
        self.master = master
        message_lines = textwrap.wrap(message_text, width=50)
        self.name_label = ttk.Label(self, text=name_text, anchor="nw")
        self.colon = ttk.Label(self, text=":", anchor="w")
        self.message = ttk.Label(self, text="\n".join(message_lines), anchor="w", justify=tk.LEFT)
        self.name_label.grid(row=0, column=0)
        self.colon.grid(row=0, column=1)
        self.message.grid(row=0, column=2)
