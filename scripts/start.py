#!/usr/bin/python3

import typer
from Providers.AnalyticsServiceProvider import AnalyticsServiceProvider
from Providers.ExportDataServiceProvider import ExportDataServiceProvider
from Providers.ImportDataServiceProvider import ImportDataServiceProvider

app = typer.Typer()


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
    export_service = ExportDataServiceProvider(export_to="DB")
    export_service.service_list = [
        "../data2bot/data/raw/orders.csv",
        "../data2bot/data/raw/reviews.csv",
        "../data2bot/data/raw/shipment_deliveries.csv",
    ]
    return export_service.execute_service()


def start_analysis():
    analytics_service = AnalyticsServiceProvider()

    analytics_service.service_list = [
        "../data2bot/sql/product_orders_on_holidays.sql",
        "../data2bot/sql/total_late_and_undelivered_shipments.sql",
        "../data2bot/sql/best_performing_product.sql",
    ]
    analytics_service.execute_service()


def export_data_to_warehouse():
    export_service = ExportDataServiceProvider(export_to="WAREHOUSE")

    # table names to export
    export_service.service_list = [
        "agg_public_holiday",
        "agg_shipments",
        "best_performing_product",
    ]
    export_service.execute_service()


@app.command()
def run():
    # Extract data from warehouse
    print("------" * 20)
    import_from_warehouse()

    # # Load data into DB
    export_data_to_db()

    # # Perform registered analytics
    start_analysis()

    # Import transfored to from db
    export_data_to_warehouse()


if __name__ == "__main__":
    app()
