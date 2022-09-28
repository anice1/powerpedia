#!/usr/bin/python3

import os
import boto3
import pandas as pd
from typing import List
from botocore import UNSIGNED
from botocore.client import Config
from Handlers.env_handler import env
from sqlalchemy import create_engine
from Handlers.log_handler import LogHandler

logger = LogHandler(log_file="logs/models.log")


def export_to_db(files: List, schema=env("SERVER", "DB_STAGING_SCHEMA")):
    """Exports files to database

    Args:
        files (List): A list of filepaths
        schema (_type_, optional): _description_. Defaults to env("SERVER", "DB_STAGING_SCHEMA").
    """
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{env('SERVER','DB_USERNAME')}:{env('SERVER','DB_PASSWORD')}@{env('SERVER','DB_HOST')}/{env('SERVER','DB_DATABASE')}"
        )
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


def export_to_warehouse(files: List=None, bucket=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME")):
    """Upload a file to an Warehouse bucket"""

    engine = create_engine(
        f"postgresql+psycopg2://{env('SERVER','DB_USERNAME')}:{env('SERVER','DB_PASSWORD')}@{env('SERVER','DB_HOST')}/{env('SERVER','DB_DATABASE')}"
    )
    pd.read_sql_query(
        '''
        SELECT * FROM acnice6032_analytics.tables
        '''
    )

    for file in files:
        object_name = os.path.basename(file)

        # Upload the file
        s3_client = boto3.client("s3")
        try:
            response = s3_client.upload_file(file, bucket, object_name)
            print(f"uploading... {file}")
        except Exception as e:
            logger.logger.error(e)


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

    for object_name in object_names:
        save_path = "/".join([path, object_name])
        object_path = "/".join([prefix, object_name])
        try:
            s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
            # response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
            s3.download_file(bucket_name, object_path, save_path)
            print(f"{object_name} imported successfully")
        except Exception as e:
            print(e)
            print("An error occcured, check", logger.file_handler.baseFilename)
            logger.logger.debug(e)
