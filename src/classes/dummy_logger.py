import datetime

class DummyLogger(object):
    def _log(self, message):
        print ("[%s]: %s" % ( datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message ))

    def debug(self, message):
        self._log(message)

    def info(self, message):
        self._log(message)

    def warn(self, message):
        self._log(message)

    def warning(self, message):
        self._log(message)

    def exception(self, message):
        self._log(message)
