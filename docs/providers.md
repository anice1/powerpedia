
# Service Providers
## Extracting Data From Warehouse

```python
# scripts/Providers/ExtractDataServiceProvider.py

class ExtractDataServiceProvider(Service):

    # names of objects to download
    service_list = [
        "orders.csv", 
        "reviews.csv", 
        "shipment_deliveries.csv"
        "..."
    ]

    # path where object will be stored
    service_path = "../Data2bot-Assessment/data/raw"

```
## DataLoad Service Provider

```python
# scripts/Providers/DataLoadServiceProvider.py

class DataLoadServiceProvider(Service):

    # name of files in data/raw to upload. 
    # Don't include the full file path. 
    # You must set service_path=None "
    service_list = [
        "orders.csv",
        "reviews.csv",
        "shipment_deliveries.csv",
    ]

    service_path = "../Data2bot-Assessment/data/raw"
```

## Analytics Service Provider
```python
# scripts/Providers/AnalyticsServiceProvider.py

class AnalyticsServiceProvider(Service):

    # name of analytics in /SQL e.g. "product_analysis.sql"
    service_list = [
        "analytics1.sql",
        "analytics2.sql",
        '...'
    ]

    service_path = "../Data2bot-Assessment/sql"
```