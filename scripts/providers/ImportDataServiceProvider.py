#!/usr/bin/python3
import boto3
from typing import List
from botocore import UNSIGNED
from botocore.client import Config
from handlers.env_handler import env
from handlers.log_handler import LogHandler
from handlers.service_handler import Service
from handlers.db_connect_handler import DatabaseConn

logger = LogHandler("logs/import.log")


class ImportDataServiceProvider(Service):

    # get the data stores from config.ini
    __import_froms = env("SERVER", "DATA_STORES")

    def __init__(self, service_list: List = None, import_from: str = "DB") -> None:
        """Imports data from provided source, Database or Warehouse

        Args:
            service_list (names of objects to import, optional): _description_. Defaults to None.
            import_from (str, optional): _description_. Defaults to "DB".
        """
        print("Importing Data...")

        # validate if import_from is registered in config
        self.__validate_import_from(import_from)

        self.import_from = import_from.upper()

        # names of objects to import
        self.service_list = service_list

    def __validate_import_from(self, import_from):
        if not import_from.upper() in self.__import_froms:
            raise TypeError(
                f"import_from type only expects one of these: {env('SERVER', 'DATA_STORES')}, {import_from} was given"
            )

    def execute_service(self):

        if self.import_from.lower() == "db":
            self.__import_from_db(files=self.service_list)

        elif self.import_from.lower() == "warehouse":
            self.__import_from_warehouse(object_names=self.service_list)
        else:
            print(f"Nothing happened, please check {__file__} execute_service() method")
            return None

        print("Import completed! \n")

    def __import_from_warehouse(
        self,
        object_names: List,
        bucket_name=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"),
        prefix="orders_data",
        path="../d2b/data/raw",
    ):
        """
        Extracts raw data from specified cloud (AWS) s3: bucket

        Args:
        object_names: a list of warehouse objects
        bucket_name: Name of the warehouse bucket
        prefix: warehouse object name prefix
        path: path where downloaded file will be stored
        """

        try:
            conn = DatabaseConn(connector="alchemy")
            engine = conn.connect()
            for object_name in object_names:
                save_path = "/".join([path, object_name])
                object_path = "/".join([prefix, object_name])
                s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
                # response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
                s3.download_file(bucket_name, object_path, save_path)
                print(f"{object_name} imported successfully")
        except Exception as e:
            print(e)
            print("An error occcured, check", logger.file_handler.baseFilename)
            logger.logger.debug(e)
        print("------" * 20)

    def __import_from_db(self, files: List):
        return "Feature coming!"
