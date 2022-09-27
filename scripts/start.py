#!/usr/bin/python3

import typer
from Providers.AnalyticsServiceProvider import AnalyticsServiceProvider
from Providers.ExportDataServiceProvider import ExportDataServiceProvider
from Providers.ImportDataServiceProvider import ImportDataServiceProvider

app = typer.Typer()
analytics_service = AnalyticsServiceProvider()


def import_from_warehouse():
    import_service = ImportDataServiceProvider()
    import_service.service_list = [
        "orders.csv",
        "reviews.csv",
        "shipment_deliveries.csv",
    ]
    import_service.import_from = "WAREHOUSE"
    return import_service.execute_service()


def export_data_to_db():
    export_service = ExportDataServiceProvider()
    export_service.service_list = [
        "/Users/cosmoremit/Documents/AcNice/data2bot/data/raw/orders.csv",
        "/Users/cosmoremit/Documents/AcNice/data2bot/data/raw/reviews.csv",
        "/Users/cosmoremit/Documents/AcNice/data2bot/data/raw/shipment_deliveries.csv",
    ]
    export_service.upload_to = "DB"
    return export_service.execute_service()


@app.command()
def run():
    # Extract data from warehouse
    import_from_warehouse()

    # Load data into DB
    export_data_to_db()

    # Perform registered analytics
    analytics_service.execute_service()


if __name__ == "__main__":
    app()
