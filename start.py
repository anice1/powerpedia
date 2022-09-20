#!/usr/bin/python3

from pprint import pprint
from providers.SqlServiceProvider import SqlServiceProvider
import sys

sys.path.append("../Data2Bot-Assessment/scripts/")

from Handlers.db_connect_handler import DatabaseConn
from Handlers.log_handler import LogHandler
import glob


def execute_sql(filenames):

    # Read the sql file
    try:
        for f in filenames:
            file = open(f, "r")
            sql_file = file.read()
            file.close()

            # all SQL commands (split on ';')
            commands = sql_file.strip().split(";")
            pprint(commands)
            print(len(commands))

            # # instantiate class
            # conn = DatabaseConn().connect()
            # for command in commands:
            #     try:
            #         print(f'Running Query...{f}\t')
            #         cur = conn.cursor()
            #         cur.execute(command)
            #     except Exception as e:
            #         print(": ", e)
            # print('Successful!')
            # conn.close()
    except Exception as e:
        print(e)


# Run sql services
sql_services = SqlServiceProvider().services()
execute_sql(sql_services)
