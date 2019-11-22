import tkinter.ttk as ttk
import tkinter as tk
from . import utils
import textwrap
from .errors import ControllerNotPassedError


class _Chatbox(tk.Canvas):
    def __init__(self, master=None, controller=None, **kwargs):
        if controller is None:
            raise ControllerNotPassedError("Controller object must be passed to _Chatbox constructor in tklib.chatbox module.")
        self.controller = controller
        self.text_spacing = kwargs.pop("text_spacing", 10)
        self.x_offset = kwargs.pop("x_offset", 10)
        
        super().__init__(master, **kwargs)
        self.last_chatline_pos_y = 0
        self.last_chatline_index = 0
        
    
    def create_chatline(self, message, **kwargs):
        name_text = message.get("display_name")
        message_text = message.get("message")
        message_lines = textwrap.wrap(message_text, width=50)
        text = [f"{name_text} : {message_lines[0]}"] + message_lines[1:]
        x, y = self.x_offset, self.last_chatline_pos_y
        tags = kwargs.pop("tags", []) + [f"chatline{self.last_chatline_index}"]
        for i, txt in enumerate(text):
            y += i * self.text_spacing
            self.create_text(x, y, anchor=tk.NW, text=txt, tags=tags, **kwargs)
        self.last_chatline_index += 1
        self.last_chatline_pos_y = y + self.text_spacing
        return tags[-1]
    
    def on_loop(self):
        messages = self.controller.aggregator.aggregate()
        for message in messages:
            self.create_chatline(message)
        if messages:
            self.update()
            self.update_idletasks()


class Chatbox(ttk.Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.vsb = ttk.Scrollbar(self)
        self._chatbox = _Chatbox(self, bd=0, highlightthickness=0,
                                 yscrollcommand=lambda f, l: utils.auto_scroll(self.vsb, f, l),
                                 controller=controller)

        self._chatbox.grid(row=0, column=0, sticky="nswe")

        self.vsb.config(command=self._chatbox.yview)
        self._chatbox.xview_moveto(0)
        self._chatbox.yview_moveto(0)
        
        self.vsb.grid(row=0, column=1, sticky='ns')

    def on_loop(self):
        self._chatbox.on_loop()

