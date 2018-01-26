from logger import logE


class GrafcetError(Exception):

    def __init__(self, message):
        assert isinstance(message, str)
        logE(message)
        self._message = message

    @property
    def message(self):
        return self._message
