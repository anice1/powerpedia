#!/usr/bin/python3

import logging

from Handlers.env_handler import env


class LogHandler:
    def __init__(self, log_file=env("LOG", "ERROR_LOG")):
        # set our database logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(env("LOG", "LOG_LEVEL"))

        # set the log formatter
        self.formatter = logging.Formatter(
            "------------------------\n%(asctime)s \n------------------------\n %(filename)s:  \n \
            \n %(message)s \n  @ %(funcName)s: %(pathname)s"
        )
        # set the file handler
        self.file_handler = logging.FileHandler(filename=log_file)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
