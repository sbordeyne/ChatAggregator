import tkinter.ttk as ttk

class ChatLine(ttk.Frame):
    def __init__(self, master=None, name_text=None, message=None):
        super().__init__(master)
        self.master = master
        self.name_label = ttk.Label(self, text=name_text)
        self.colon = ttk.Label(self, text=":")
        self.message = ttk.Label(self, text=message)
        self.name_label.grid(row=0, column=0)
        self.colon.grid(row=0, column=1)
        self.message.grid(row=0, column=2)
     