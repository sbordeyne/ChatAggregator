import glob
import json
from copy import copy
from os.path import split

from chatrooms.twitch import twitch_config
from .errors import ServiceNotRecognizedError


class Theme:
    def __init__(self, filename, id_):
        self.filename = filename
        self.data = None
        self.name = split(filename)[-1].split('.')[0]
        self.id = id_
        with open(self.filename) as f:
            self.data = json.load(f)
    
    @classmethod
    def get_all_themes(cls):
        return [Theme(filename=fn, id_=i) for i, fn in enumerate(glob.glob("themes/**.catheme"))]
    
    def __getitem__(self, item):
        return self.data[item]


class Config:
    def __init__(self):
        self.data = {}
        self.load()
    
    def __getitem__(self, item):
        return self.data.get(item)
        
    def load(self):
        """
        Loads config data from .caconfig file if it exists
        """
        data = {"display_name": "camixerbot",
                "usernames": {"twitch": "",
                              "mixer": "",
                              "youtube": "",
                              "facebook": ""},
                "selected": [],
                "twitch_config": twitch_config,
                "mixer_config": None,
                "youtube_config": None,
                "facebook_config": None,
               }
        try:
            with open(".caconfig", "r") as f:
                data.update(json.load(f))
        except FileNotFoundError:
            pass
        self.data.update(data)
    
    def save(self):
        """
        Saves config data to .caconfig file, overwriting in the process.
        """
        with open(".caconfig", "w") as f:
            json.dump(self._as_dict, f, indent=4)
    
    def update(self, data):
        """
        Updates config object's data variable with new data.
        """
        self.data.update(data)
    
    def get_config(self, service_name):
        """
        Gets the config for a given service.
        
        :param service_name: (required) name of the service to get the config from.
                             one of either : (twitch|mixer|youtube|facebook)
        
        :return: dictionary of values to use as that service's API
        :raises: tklib.errors.ServiceNotRecognizedError if service_name is not allowed
        """
        if service_name not in ("twitch", "youtube", "mixer", "facebook"):
            raise ServiceNotRecognizedError(f"Service {service_name} not recognized." \
                                            f" Enter one of (twitch|mixer|youtube|facebook)")
        service_config = copy(self.data[service_name + "_config"])
        service_config["channel_name"] = self.data["usernames"]["twitch"]
        return copy(service_config)

    def get_aggregator_args(self):
        """
        Gets keyword arguments for Aggregator constructor based on configuration options
        
        :return: dictionary of keyword arguments for the Aggregator class.
        """
        kwargs = {}
        for service in self['selected']:
            kwargs[service + '_config'] = self.get_config(service)
        return kwargs
