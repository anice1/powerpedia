#!/usr/bin/python3

import boto3
from botocore import UNSIGNED
from botocore.client import Config

from Handlers.env_handler import env
from Handlers.log_handler import LogHandler
from Handlers.db_connect_handler import DatabaseConn


def download_raw_data(
    object_name="orders.csv",
    filename=None,
    prefix="orders_data",
    path="../Data2Bot-Assessment/data/raw/",
    bucket_name=env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"),
):
    """
    Extracts raw data from specified cloud (AWS) s3: bucket

    Args:
    obj_name: name of s3 object
    filename: preferred name for the file downloaded
    path: path where downloaded file will be stored
    """
    # set filename to be same as object name if none
    if filename is None:
        filename = object_name

    handler = LogHandler()
    try:
        s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
        s3.download_file(
            bucket_name, "/".join([prefix, object_name]), "/".join([path, filename])
        )
    except Exception as e:
        print(e)
        print("An error occcured, check", handler.file_handler.baseFilename)
        handler.logger.debug(e)


download_raw_data(object_name="orders.csv")
download_raw_data(object_name="reviews.csv")
download_raw_data(object_name="shipment_deliveries.csv")

# instantiate class
# db_conn = DatabaseConn()

# # Extract the tables in the schema
# addresses = db_conn.extract(table="dim_addresses")
# customers = db_conn.extract(table="dim_customers")
# products = db_conn.extract(table="dim_products")
# dates = db_conn.extract(table="dim_dates")
