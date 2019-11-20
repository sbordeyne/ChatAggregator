class TkLibException(Exception):
    pass

class ConfigError(TkLibException):
    pass

class ControllerNotPassedError(ConfigError):
    pass

class ServiceNotRecognizedError(ConfigError):
    pass
