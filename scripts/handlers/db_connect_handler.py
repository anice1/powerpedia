#!/usr/bin/python3

import psycopg2 as pg
from sqlalchemy import create_engine
from env_handler import env


class DatabaseConn:
    def __init__(self, connector=env("SERVER", "DB_CONNECTOR")) -> None:
        """Establish database connection based on the server settings in config.ini

        Args:
            log_file (str, optional): The name or path to the file where error will be logged. Defaults to ERROR_LOG path in config.ini
            connection (str, optional): The database connector, Default to DB_CONNECTOR in config.ini
        """
        # Load connection variables from config.ini
        self.DB_HOST = env("SERVER", "DB_HOST")
        self.DB_PORT = env("SERVER", "DB_PORT")
        self.DB_DATABASE = env("SERVER", "DB_DATABASE")
        self.DB_USERNAME = env("SERVER", "DB_USERNAME")
        self.DB_PASSWORD = env("SERVER", "DB_PASSWORD")
        self.connector = connector

    def __alchemy(self):
        return create_engine(
            f"postgresql+psycopg2://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_DATABASE}"
        )

    def __pg(self):
        # Establish a connection with the db
        try:
            conn = pg.connect(
                host=self.DB_HOST,
                dbname=self.DB_DATABASE,
                user=self.DB_USERNAME,
                password=self.DB_PASSWORD,
                port=self.DB_PORT,
            )
            return conn
        except Exception as e:
            print(e)

    def connect(self):
        conn = None
        if self.connector.lower() == "alchemy":
            conn = self.__alchemy()
        elif self.connector.lower() == "pg":
            conn = self.__pg()
        elif not self.connector.lower() in env("SERVER", "DB_CONNECTOR"):
            raise TypeError(
                "Invalid connector, expects one of these "
                + env("SERVER", "DB_CONNECTOR")
            )
        return conn

    # def extract(self, table, schema=env("SERVER", "DB_DEFAULT_SCHEMA")):
    #     """
    #     Queries and export data from specified schema table

    #     parameters:
    #     -----------
    #     table: the name of the table you'd like to extract
    #     """
    #     print(f"Querying {schema}.{table} ...", end="")

    #     try:
    #         conn = self.__connect()
    #         cur = conn.cursor()
    #         cur.execute(f"""SELECT * FROM {schema}.{table}""")
    #         result = cur.fetchall()
    #         print(" Successful!")

    #         conn.close()
    #         return result

    #     except Exception as e:
    #         self.logger.debug(e)
    #         self.error()

    # def __error(self):
    #     print("An error occcured, check", self.file_handler.baseFilename)
