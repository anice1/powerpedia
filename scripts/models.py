#!/usr/bin/python3

import os
import boto3
import pandas as pd
from typing import List
from botocore import UNSIGNED
from botocore.client import Config
from Handlers.env_handler import env
from sqlalchemy import create_engine, inspect
from Handlers.log_handler import LogHandler
from Handlers.db_connect_handler import DatabaseConn

logger = LogHandler(log_file="logs/models.log")

conn = DatabaseConn(connector="alchemy")
engine = conn.connect()


def export_to_db(files: List, schema=env("SERVER", "DB_STAGING_SCHEMA")):
    """Exports files to database

    Args:
        files (List): A list of filepaths
        schema (_type_, optional): _description_. Defaults to env("SERVER", "DB_STAGING_SCHEMA").
    """
    try:
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


def export_to_warehouse(
    table_names: List = ['agg_public_holiday','agg_shipments','best_performing_product'],
    schema=env('SERVER', 'DB_ANALYTICS_SCHEMA'),
    bucket=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME")
):
    """Upload a file to an Warehouse bucket"""

    for table in table_names:
        query = pd.read_sql_query(f"""SELECT * FROM {schema}.{table}""", con=engine)
        df = pd.DataFrame(query)
        df.to_csv(f'../data2bot/data/transformed/{table}.csv', index=False)

    upload_path = '../data2bot/data/transformed'
    for file in os.listdir('../data2bot/data/transformed'):
        object_name = os.path.basename(file)
        file = '/'.join([upload_path, object_name])

        # Upload the file
        s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        try:
            print(f"uploading... {file}")
            response = s3_client.upload_file(file, bucket, object_name)
        except Exception as e:
            logger.logger.error(e)
            print(e)
    print("------" * 20)



def import_from_db(files: List):
    return "Feature coming!"


def import_from_warehouse(
    object_names: List,
    bucket_name=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"),
    prefix="orders_data",
    path="../data2bot/data/raw",
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
