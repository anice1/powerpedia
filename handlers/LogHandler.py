import logging
from Env import env


class LogHandler:
    def __init__(self, logger_name):
        # set our database logger
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(env("LOG", "LOG_LEVEL"))

        # set the log formatter
        self.formatter = logging.Formatter(
            "------------------------\n%(asctime)s \n------------------------\n %(name)s: %(message)s"
        )
        # set the file handler
        self.file_handler = logging.FileHandler(filename=env("LOG", "DB_ERROR_LOG"))
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
