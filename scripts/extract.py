import boto3
import logging
from handlers.Env import env
from handlers.log_handler import LogHandler
from db_connect import DatabaseConn


def initiate_s3():
    logger = LogHandler()
    try:
        s3 = boto3.client("s3")
        s3.download_file(
            env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"), "orders_data", "orders.csv"
        )
    except Exception as e:
        print("An error occcured, check", logger.file_handler.baseFilename)
        logger.logger.debug(e)


def raw_data_extract():
    """Extracts raw data from specified cloud (AWS) s3: bucket"""

    pass


# instantiate class
db_conn = DatabaseConn()

# Extract the tables in the schema
# addresses = db_conn.extract(table="dim_addresses")
# print(addresses)
# customers = db_conn.extract(table="dim_customers")
# products = db_conn.extract(table="dim_products")
# dates = db_conn.extract(table="dim_dates")

initiate_s3()
