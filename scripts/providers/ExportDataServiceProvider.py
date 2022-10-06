#!/usr/bin/python3
import os
import boto3
import pandas as pd
from typing import List
from botocore import UNSIGNED
from botocore.client import Config
from handlers.env_handler import env
from sqlalchemy import create_engine
from handlers.log_handler import LogHandler
from handlers.service_handler import Service
from handlers.db_connect_handler import DatabaseConn

logger = LogHandler("logs/export.log")


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
            self.__export_to_db(files=self.service_list, schema=self.default_schema)

        elif self.export_to == "WAREHOUSE":
            self.__export_to_warehouse(table_names=self.service_list)
        else:
            raise TypeError(
                f"Nothing happened, please check {__file__} execute_service() method"
            )

        print("Upload Completed! \n")

    def __export_to_warehouse(
        self,
        table_names: List = [
            "agg_public_holiday",
            "agg_shipments",
            "best_performing_product",
        ],
        schema=env("SERVER", "DB_ANALYTICS_SCHEMA"),
        bucket=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"),
    ):
        """Upload a file to an Warehouse bucket"""

        conn = DatabaseConn(connector="alchemy")
        engine = conn.connect()
        for table in table_names:
            query = pd.read_sql_query(f"""SELECT * FROM {schema}.{table}""", con=engine)
            df = pd.DataFrame(query)
            df.to_csv(f"../d2b/data/transformed/{table}.csv", index=False)

        upload_path = "../d2b/data/transformed"
        for file in os.listdir("../d2b/data/transformed"):
            object_name = os.path.basename(file)
            file = "/".join([upload_path, object_name])

            # Upload the file
            s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
            try:
                print(f"uploading... {file}")
                response = s3_client.upload_file(file, bucket, object_name)
            except Exception as e:
                logger.logger.error(e)
                print(e)
        print("------" * 20)

    def __export_to_db(self, files: List, schema=env("SERVER", "DB_STAGING_SCHEMA")):
        """Exports files to database

        Args:
            files (List): A list of filepaths
            schema (_type_, optional): _description_. Defaults to env("SERVER", "DB_STAGING_SCHEMA").
        """
        try:

            conn = DatabaseConn(connector="alchemy")
            engine = conn.connect()
            for file in files:
                # Get the table name
                table_name = os.path.split(file)[-1].split(".")[0]

                data = pd.read_csv(file, delimiter=",", index_col=None).reset_index(
                    drop=True
                )
                data.to_sql(
                    name=table_name,
                    con=engine,
                    schema=schema,
                    if_exists="replace",
                    method="multi",
                )
                print(f"{table_name} records seeded successfuly")
        except Exception as e:
            print(e)
            logger.logger.error(e)
        print("------" * 20)
