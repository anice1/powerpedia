from db_connect import DatabaseConn
import boto3
from handlers.Env import env


def initiate_s3():
    s3 = boto3.client("s3")
    s3.download_file(env("SERVER", "S3_WAREHOUSE_BUCKET_NAME"), "orders_data", "*")


def raw_data_extract():
    """Extracts raw data from specified cloud (AWS) s3: bucket"""

    pass


# instantiate class
db_conn = DatabaseConn("extract")

# Extract the tables in the schema
addresses = db_conn.extract(table="dim_addresses")
customers = db_conn.extract(table="dim_customers")
products = db_conn.extract(table="dim_products")
dates = db_conn.extract(table="dim_dates")

initiate_s3()
