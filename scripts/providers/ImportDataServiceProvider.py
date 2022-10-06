#!/usr/bin/python3

from typing import List
from handlers.env_handler import env
from handlers.log_handler import LogHandler
from handlers.service_handler import Service
from models import import_from_warehouse, import_from_db

handler = LogHandler("logs/import.log")


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

        if self.import_from == "DB":
            import_from_db(files=self.service_list)

        elif self.import_from == "WAREHOUSE":
            import_from_warehouse(object_names=self.service_list)
        else:
            print(f"Nothing happened, please check {__file__} execute_service() method")
            return None

        print("Import completed! \n")
