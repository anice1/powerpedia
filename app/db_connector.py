from datetime import datetime
import logging
import psycopg2 as pg

import sys

sys.path.insert(0, "../Data2Bot-Assessment/")
from setup import env

# set our database logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# set the log formatter 
formatter = logging.Formatter('------------------------\n%(asctime)s \n------------------------\n %(name)s: %(message)s')
# set the file handler
file_handler = logging.FileHandler(filename='logs/'+env('LOG', 'DB_ERROR_LOG'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Load connection variables from config.ini
DB_CONNECTION = env("SERVER", "DB_CONNECTION")
DB_HOST = env("SERVER", "DB_HOST")
DB_PORT = env("SERVER", "DB_PORT")
DB_DATABASE = env("SERVER", "DB_DATABASE")
DB_USERNAME = env("SERVER", "DB_USERNAME")
DB_PASSWORD = env("SERVER", "DB_PASSWORD")

# Establish a connection with the db
try:
    conn = pg.connect(
        host=DB_HOST,
        dbname=DB_DATABASE,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        port=DB_PORT,
    )

    # close connection
    conn.close()
except Exception as e:
    # log error to file
    logger.debug(e)
    print('An error occcured, check', file_handler.get_name.__str__())
