"""
 Here is where you can register all sql services you'd like to run during automation. 
 These sql files are loaded into the Kernel. Now create something great!

 """
import os

# import sys

import pandas as pd

# sys.path.append("../Data2Bot-Assessment/scripts/")
from Handlers.env_handler import env
from Handlers.log_handler import LogHandler
from Handlers.service_handler import Service
from sqlalchemy import create_engine

logger = LogHandler(log_file="logs/dataload.log")


class DataLoadServiceProvider(Service):

    # name of files in data/raw to upload.
    # Do not include the full file path."
    service_list = [
        "orders.csv",
        "reviews.csv",
        "shipment_deliveries.csv",
    ]

    # path to pick the data for upload
    service_path = "../data2bot/data/raw"

    def __init__(self) -> None:
        print("Uploading Raw Data...")

    def services(self):
        return ["/".join([self.service_path, service]) for service in self.service_list]

    def execute_service(self):
        try:
            engine = create_engine(
                f"postgresql+psycopg2://{env('SERVER','DB_USERNAME')}:{env('SERVER','DB_PASSWORD')}@{env('SERVER','DB_HOST')}/{env('SERVER','DB_DATABASE')}"
            )
            for file in self.services():
                # Get the table name
                table_name = os.path.split(file)[-1].split(".")[0]

                data = pd.read_csv(file, delimiter=",", index_col=None).reset_index(
                    drop=True
                )
                data.to_sql(
                    name=table_name,
                    con=engine,
                    schema=env("SERVER", "DB_STAGING_SCHEMA"),
                    if_exists="replace",
                    method="multi",
                )
                print(f"{table_name} records seeded successfuly")
        except Exception as e:
            print(e)
            logger.logger.error(e)
        print("Upload completed! \n")
