"""
 Here is where you can register all sql services you'd like to run during automation. 
 These sql files are loaded into the Kernel. Now create something great!

 """
import os
import pandas as pd
from sqlalchemy import create_engine

import sys

sys.path.append("../Data2Bot-Assessment/scripts/")
from Handlers.env_handler import env
from Handlers.service_handler import Service
from Handlers.db_connect_handler import DatabaseConn

dbc = DatabaseConn()


class DataLoadServiceProvider(Service):

    # name of files in data/raw to upload. Do not include the full file path. You must set service_path=None "
    service_list = [
        "orders.csv",
        "reviews.csv",
        "shipment_deliveries.csv",
    ]

    service_path = "../Data2bot-Assessment/data/raw"

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
            dbc.logger.debug(e)
        print('Upload completed! \n')
