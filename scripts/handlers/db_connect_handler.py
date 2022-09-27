#!/usr/bin/python3

import psycopg2 as pg
from Handlers.env_handler import env
from Handlers.log_handler import LogHandler


class DatabaseConn(LogHandler):
    def __init__(self, log_file=env("LOG", "ERROR_LOG")) -> None:
        """Establish database connection based on the server settings in config.ini

        Args:
            log_file (str, optional): the name or path to the file where error will be logged. Defaults to ERROR_LOG path in config.ini
        """
        super().__init__(log_file=log_file)

        # Load connection variables from config.ini
        self.DB_HOST = env("SERVER", "DB_HOST")
        self.DB_PORT = env("SERVER", "DB_PORT")
        self.DB_DATABASE = env("SERVER", "DB_DATABASE")
        self.DB_USERNAME = env("SERVER", "DB_USERNAME")
        self.DB_PASSWORD = env("SERVER", "DB_PASSWORD")

    def connect(self):
        # Establish a connection with the db
        try:
            self.conn = pg.connect(
                host=self.DB_HOST,
                dbname=self.DB_DATABASE,
                user=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                port=self.DB_PORT,
            )

        except Exception as e:
            # log error to file
            self.logger.debug(e)
            self.error()
        return self.conn

    def extract(self, table, schema=env("SERVER", "DB_DEFAULT_SCHEMA")):
        """
        Queries and export data from specified schema table

        parameters:
        -----------
        table: the name of the table you'd like to extract
        """
        print(f"Querying {schema}.{table} ...", end="")

        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM {schema}.{table}""")
            result = cur.fetchall()
            print(" Successful!")

            conn.close()
            return result

        except Exception as e:
            self.logger.debug(e)
            self.error()

    def error(self):
        print("An error occcured, check", self.file_handler.baseFilename)
