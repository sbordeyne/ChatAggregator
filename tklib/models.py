import glob
import json


class Theme:
    def __init__(self, filename):
        self.filename = filename
        self.data = None
        with open(self.filename) as f:
            self.data = json.load(f)
    
    @classmethod
    def get_all_themes(cls):
        return [Theme(fn) for fn in glob.glob("themes/**.catheme")]
    
    def __getitem__(self, item):
        return self.data[item]
