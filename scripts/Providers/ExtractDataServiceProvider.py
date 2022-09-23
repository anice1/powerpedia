"""
 Here is where you can register all sql services you'd like to run during automation. 
 These sql files are loaded into the Kernel. Now create something great!

 """

from pprint import pprint
import boto3
from botocore import UNSIGNED
from botocore.client import Config

import sys

sys.path.append("../Data2Bot-Assessment/scripts/")
from Handlers.env_handler import env
from Handlers.log_handler import LogHandler
from Handlers.service_handler import Service
from Handlers.db_connect_handler import DatabaseConn

dbc = DatabaseConn()
handler = LogHandler()


class ExtractDataServiceProvider(Service):

    # names of objects to download
    service_list = ["orders.csv", "reviews.csv", "shipment_deliveries.csv"]

    # Path where object will be stored
    service_path = "../Data2bot-Assessment/data/raw"

    def __init__(self) -> None:
        print("Extracting Data...")

    def services(self):
        # return ["/".join([self.service_path, service]) for service in self.service_list]
        return self.service_list

    def execute_service(self):
        """
        Extracts raw data from specified cloud (AWS) s3: bucket

        Args:
        obj_name: name of s3 object
        filename: preferred name for the file downloaded
        path: path where downloaded file will be stored
        """
        prefix = "orders_data"
        bucket_name = env("SERVER", "S3_WAREHOUSE_BUCKET_NAME")

        for object_name in self.service_list:
            save_path = "/".join([self.service_path, object_name])
            object_path = "/".join([prefix, object_name])

            try:
                s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
                # response = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
                s3.download_file(bucket_name, object_path, save_path)
            except Exception as e:
                print(e)
                print("An error occcured, check", handler.file_handler.baseFilename)
                handler.logger.debug(e)
        print("Extraction completed! \n")
