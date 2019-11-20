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
        self.selected = defaultdict(tk.IntVar)
        
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
        
        self.service_selector_frame = tk.LabelFrame(self, text="Select Services")
        self.twitch_cb = tk.Checkbutton(self.service_selector_frame, text= "Twitch", variable=self.selected['twitch'])
        self.mixer_cb = tk.Checkbutton(self.service_selector_frame, text= "Mixer", variable=self.selected['mixer'])
        self.youtube_cb = tk.Checkbutton(self.service_selector_frame, text= "YouTube", variable=self.selected['youtube'])
        self.facebook_cb = tk.Checkbutton(self.service_selector_frame, text= "Facebook", variable=self.selected['facebook'])
        
        self.twitch_cb.grid(row=0, column=0)
        self.mixer_cb.grid(row=1, column=0)
        self.youtube_cb.grid(row=2, column=0)
        self.facebook_cb.grid(row=3, column=0)
        self.service_selector_frame.grid(row=0, column=1, rowspan=4)
        self.set_from_config(self.controller.controller.config.data)
    
    def _as_dict(self):
        usernames = {k: v.get() for k, v in self.usernames.items()}
        selected = [k for k, v in self.selected.items() if v.get() == 1]
        return {"display_name": self.display_name.get(),
                "usernames": usernames,
                "selected": selected,
        }
    
    def set_from_config(self, config):
        for service, usr in config['usernames'].items():
            self.usernames[service].set(usr)
        for service in config["selected"]:
            self.selected[service].set(1)
        self.display_name.set(config["display_name"])
    
    def on_close(self, *args):  # TODO: config doesn't seem to save && settings window doesn't re open once opened then closed.
        if self.controller is not None:
            self.controller.controller.config.update(self._as_dict())
            self.controller.controller.config.save()
            self.controller.settings_toplevel.destroy()
            self.controller.settings_toplevel = None


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Settings")
    gui = SettingsWindow(root)
    gui.grid(sticky='nswe')
    root.mainloop()

