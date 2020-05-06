import logging
import logging.config


class LoggerInstance(object):
    def __init__(self):
        logging.config.fileConfig("config/logger.ini")
        print("logger init ok")

    @classmethod
    def _GetCurrent(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance

    @classmethod
    def getLogger(cls, name):
        return cls._GetCurrent()._Singular_GetLogger(name=name)

    def _Singular_GetLogger(self, name):
        return logging.getLogger(name=name)
