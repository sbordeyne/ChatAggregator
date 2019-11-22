class MixerException(Exception):
    pass

class RequestError(Exception):
    def __init__(self, response):
        self.response = response


class NotAuthenticatedError(RequestError):
    """Failed to connect to the Mixer server."""
    pass

class UnknownError(RequestError):
    pass
