"""
 Here is where you can register all sql services you'd like to run during automation. 
 These sql files are loaded into the Kernel. Now create something great!

 """
import sys

sys.path.append("../Data2Bot-Assessment/scripts/")
from Handlers.service_handler import Service


class SqlServiceProvider(Service):

    # name of service in sql_services e.g. "product_analysis.sql"
    service_list = [
        "product_orders_on_holidays.sql",
    ]

    service_path = "../Data2bot/services/sql_services"

    def services(self):
        return ["".join([self.service_path, service]) for service in self.service_list]


print(SqlServiceProvider().services())
