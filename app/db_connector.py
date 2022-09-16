from datetime import datetime
import logging
import psycopg2 as pg

import sys

sys.path.insert(0, "../Data2Bot-Assessment/")
from setup import env


class LogHandler:
    def __init__(self) -> None:
        # set our database logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # set the log formatter
        self.formatter = logging.Formatter(
            "------------------------\n%(asctime)s \n------------------------\n %(name)s: %(message)s"
        )
        # set the file handler
        self.file_handler = logging.FileHandler(
            filename="logs/" + env("LOG", "DB_ERROR_LOG")
        )
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)


class DatabaseConn(LogHandler):
    def __init__(self) -> None:
        super().__init__()

        # Load connection variables from config.ini
        self.DB_CONNECTION = env("SERVER", "DB_CONNECTION")
        self.DB_HOST = env("SERVER", "DB_HOST")
        self.DB_PORT = env("SERVER", "DB_PORT")
        self.DB_DATABASE = env("SERVER", "DB_DATABASE")
        self.DB_USERNAME = env("SERVER", "DB_USERNAME")
        self.DB_PASSWORD = env("SERVER", "DB_PASSWORD")

    def connect(self):
        # Establish a connection with the db
        try:
            conn = pg.connect(
                host=self.DB_HOST,
                dbname=self.DB_DATABASE,
                user=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                port=self.DB_PORT,
            )

            # close connection
            conn.close()
        except Exception as e:
            # log error to file
            self.logger.debug(e)
            print("An error occcured, check", self.file_handler.get_name.__str__())

        return conn
