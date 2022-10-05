#!/usr/bin/python3
import sys
from typing import List
from handlers.env_handler import env
from sqlalchemy import create_engine
from handlers.service_handler import Service


sys.path.append("../d2b/scripts/")
from models import export_to_db, export_to_warehouse


class ExportDataServiceProvider(Service):

    # get the data stores from config.ini
    __upload_to_list = env("SERVER", "DATA_STORES")

    def __init__(
        self,
        service_list: List = None,
        export_to: str = "DB",
        schema=env("SERVER", "DB_STAGING_SCHEMA"),
    ) -> None:
        """uploads

        Args:
            service_list (List): Name of files to upload.
            upload_to (str, optional): where to upload the files, either 'DB' or 'WAREHOUSE'. Defaults to "DB".

        Raises:
            TypeError: if upload_to_type is not registered in config.ini
        """
        print("Uploading Data...")

        # validate if upload_to type is registered in config
        self.__validate_upload_to(export_to)

        self.export_to = export_to.upper()
        # name of files in data/raw to upload.
        self.service_list = service_list
        # name of the postgres schema
        self.default_schema = schema

    def __validate_upload_to(self, export_to):
        if not export_to.upper() in self.__upload_to_list:
            raise TypeError(
                f"Upload type only expects one of these: {env('SERVER', 'DATA_STORES')}, {export_to} was given"
            )

    def execute_service(self):
        if self.export_to == "DB":
            export_to_db(files=self.service_list, schema=self.default_schema)

        elif self.export_to == "WAREHOUSE":
            export_to_warehouse(table_names=self.service_list)
        else:
            raise TypeError(
                f"Nothing happened, please check {__file__} execute_service() method"
            )

        print("Upload Completed! \n")
