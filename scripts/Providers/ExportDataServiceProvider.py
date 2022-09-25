import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError

sys.path.append("../data2bot/scripts/")
from Handlers.env_handler import env
from Handlers.log_handler import LogHandler
from Handlers.service_handler import Service

logger = LogHandler(log_file="logs/exports.log")


class ExportDataServiceProvider(Service):

    # names of objects to download
    service_list = ["orders.csv", "reviews.csv", "shipment_deliveries.csv"]

    # Path where object will be stored
    service_path = "../data2bot/data/transformed"

    def __init__(self) -> None:
        print("Exporting Analytics...")

    def services(self):
        return ["/".join([self.service_path, service]) for service in self.service_list]

    def execute_service(self, file_name, bucket, object_name=None):
        """Upload a file to an S3 bucket"""

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        # Upload the file
        s3_client = boto3.client("s3")
        try:
            response = s3_client.upload_file(file_name, bucket, object_name)
        except Exception as e:
            logger.logger.error(e)
            return False
        return True
