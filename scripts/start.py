#!/usr/bin/python3

import logging
import typer

from Providers.AnalyticsServiceProvider import AnalyticsServiceProvider
from Providers.DataLoadServiceProvider import DataLoadServiceProvider
from Providers.ExtractDataServiceProvider import ExtractDataServiceProvider


logging.basicConfig(
    filename="../Data2Bot-Assessment/logs/runtime.log",
    format="%(asctime)s:  %(filename)s: %(message)s: %(funcName)s: @ %(pathname)s",
    level=logging.DEBUG,
)

app = typer.Typer()


@app.command()
def run():
    # Extract data from warehouse
    ExtractDataServiceProvider().execute_service()

    # Load data into DB
    DataLoadServiceProvider().execute_service()

    # Perform registered analytics
    # AnalyticsServiceProvider().execute_service()


if __name__ == "__main__":
    app()
