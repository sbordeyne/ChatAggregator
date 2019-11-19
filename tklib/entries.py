import tkinter as tk


class EntryWithPlaceholder(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey', **kwargs):
        super().__init__(master, **kwargs)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()


class LabelEntry(tk.Frame):
    def __init__(self, master=None, entry_widget=None, **kwargs):
        super().__init__(master)
        self.master = master
        label_kwargs = {k[6:]: v for k, v in kwargs.items() if k.startswith("label_")}
        entry_kwargs = {k[6:]: v for k, v in kwargs.items() if k.startswith("entry_")}
        self.label = tk.Label(self, **label_kwargs)
        self.entry = tk.Entry(self, **entry_kwargs) if entry_widget is None else entry_widget(self, **entry_kwargs)
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
