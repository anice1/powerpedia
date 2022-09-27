#!/usr/bin/python3
"""
 Here is where you can register all sql services you'd like to run during
 automation. 
 These sql files are loaded into the Kernel. Now create something great!

"""
import sys

sys.path.append("../data2bot/scripts/")
from Handlers.log_handler import LogHandler
from Handlers.service_handler import Service
from Handlers.db_connect_handler import DatabaseConn


logger = LogHandler(log_file="logs/analytics.log")


class AnalyticsServiceProvider(Service):

    # name of analytics in sql e.g. "product_analysis.sql"
    service_list = [
        "product_orders_on_holidays.sql",
        "total_late_and_undelivered_shipments.sql",
        "product_reviews_analytics.sql",
    ]

    service_path = "../data2bot/sql"

    def __init__(self) -> None:
        print("Running Analysis...")

    def services(self):
        return ["/".join([self.service_path, service]) for service in self.service_list]

    def execute_service(self):
        # Read the sql file
        conn = DatabaseConn()
        conn = conn.connect()
        conn.autocommit = True

        for f in self.services():
            try:
                # instantiate class
                print(f"Running Query... {f}\t")
                cur = conn.cursor()
                cur.execute(open(f, "r").read())
                print("Successful! \n")
            except Exception as e:
                print(": ", e)
                logger.logger.error(e)
        conn.close()
        print("Analysis Completed")
