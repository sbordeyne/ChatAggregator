from copy import copy
import pprint

class Message:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.data = copy(kwargs)
    
    def __str__(self):
        return str(self.data)
    
    def __getitem__(self, key):
        return self.data[key]
    
    def __iter__(self):
        return iter(self.data)
    
    def __len__(self):
        return len(self.data)

    def get(self, key, default=None):
        """
        Gets a key from this 'dictionary'

        :param key: (required) key to get the value from
        :param default: (default:None) default value to return
        
        :return: value mapped to the given key, if that key exists, else returns default
        """
        return self.data.get(key, default)

    def is_command(self, command):
        return self.command.upper() == command.upper()