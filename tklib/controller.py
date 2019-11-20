from chatrooms.models.aggregator import Aggregator
from .errors import ConfigError


class Controller:
    def __init__(self, config, aggregator_args=None):
        if config is None:
            raise ConfigError("Config must be passed to Controller constructor in module tklib.controller")
        self.config = config
        self.aggregator = Aggregator(**self.config.get_aggregator_args())
        
        self.aggregator.start()