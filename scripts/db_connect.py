import psycopg2 as pg
from handlers.Env import env
from handlers.log_handler import LogHandler
import os


class DatabaseConn(LogHandler):
    def __init__(self, logger_name=__file__) -> None:
        """Establish database connection based on the server settings in config.ini

        Args:
            logger_name (str, optional): the name of the operation. Defaults to __name__.
        """
        super().__init__(logger_name=logger_name)
        self.logger.getChild(logger_name)

        self.conn = None
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

        self.logger.info(self.conn)
        return self.conn

    def extract(self, table, schema=env("SERVER", "DB_DEFAULT_SCHEMA")):
        """
        Queries and export data from specified schema table

        parameters:
        -----------
        table: the name of the table you'd like to extract
        """
        print(f"Querying {schema}.{table} ... \n")

        try:
            conn = self.connect()
            cur = conn.cursor()
            cur.execute(f"""SELECT * FROM {schema}.{table}""")
            result = cur.fetchall()
            print("\n Successful!")

            conn.close()
            return result

        except Exception as e:
            self.logger.debug(e)
            self.error()

    def error(self):
        print("An error occcured, check", self.file_handler.baseFilename)
