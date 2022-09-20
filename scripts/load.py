#!/usr/bin/python3
import pandas as pd
from Handlers.db_connect_handler import DatabaseConn
from Handlers.env_handler import env


def load_data(file: str, table):

    # connect the database
    conn = DatabaseConn().connect()

    data = pd.read_csv(file, delimiter=",", index_col=False)
    # loop through the data frame
    for i, row in data.iterrows():
        # here %S means string values
        sql = f"INSERT INTO {env('SERVER','DB_USERNAME')}_staging.{table} VALUES ()"
        cursor.execute(sql, tuple(row))
        print("Record inserted")
        # the connection is not auto committed by default, so we must commit to save our changes
        conn.commit()
    conn.close()
