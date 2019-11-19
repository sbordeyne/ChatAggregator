import tkinter as tk
import tkinter.ttk as ttk
from .entries import LabelEntry
from collections import defaultdict
import json
from .utils import get_root_widget


class SettingsWindow(ttk.Frame):
    def __init__(self, master=None, controller=None, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        
        self.display_name = tk.StringVar()
        self.usernames = defaultdict(tk.StringVar)
        self.display_name_ety = LabelEntry(self, label_text="Display Name :", 
                                           entry_textvariable=self.display_name)
        
        self.twitch_user = LabelEntry(self, label_text="Twitch channel :",
                                      entry_textvariable=self.usernames["twitch"])
        self.mixer_user = LabelEntry(self, label_text="Mixer channel :",
                                     entry_textvariable=self.usernames["mixer"])
        self.youtube_user = LabelEntry(self, label_text="YouTube channel :",
                                       entry_textvariable=self.usernames["youtube"])
        self.facebook_user = LabelEntry(self, label_text="Facebook channel :",
                                        entry_textvariable=self.usernames["facebook"])
        
        self.display_name_ety.grid(row=0, column=0)
        self.twitch_user.grid(row=1, column=0)
        self.mixer_user.grid(row=2, column=0)
        self.youtube_user.grid(row=3, column=0)
        self.facebook_user.grid(row=4, column=0)
    
    def _as_dict(self):
        usernames = {k: v.get() for k, v in self.usernames.items()}
        return {"display_name": self.display_name.get(),
                "usernames": usernames,
        }
    
    def save_config(self):
        with open(".caconfig", "w") as f:
            json.dump(self._as_dict, f, indent=4)
    
    def on_close(self, *args):
        self.save_config()
        if self.controller is not None:
            self.controller.settings_toplevel.destroy()
            self.controller.settings_toplevel = None


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Settings")
    gui = SettingsWindow(root)
    gui.grid(sticky='nswe')
    root.mainloop()

