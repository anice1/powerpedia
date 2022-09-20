from cgitb import handler

#!/usr/bin/python3

from handlers.db_connect_handler import DatabaseConn
from handlers.log_handler import LogHandler
import glob


def execute_sql(filename):

    # Read the sql file
    file = open(filename, "r")
    sql_file = file.read()
    file.close()

    # all SQL commands (split on ';')
    commands = sql_file.split(";")

    # instantiate class
    # conn = DatabaseConn().connect()
    # for command in commands:
    #     try:
    #         cur = conn.cursor()
    #         cur.execute(command)
    #     except Exception as e:
    #         print(": ", e)


path = "../Data2Bot-Assessment/Analysis/"
sql_files = glob.glob(path + "*.sql")

execute_sql(filename=path + "product_orders_on_holidays.sql")
