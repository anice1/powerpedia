
# Service Providers
## Import Data Service Provider

```python
# scripts/Providers/ImportDataServiceProvider.py
class ImportDataServiceProvider(Service):

    # get the data stores from config.ini
    __import_froms = env("SERVER", "DATA_STORES")

    def __init__(self, service_list: List = None, import_from: str = "DB") -> None:
        """Imports data from provided source, Database or Warehouse

        Args:
            service_list (names of objects to import, optional): _description_. Defaults to None.
            import_from (str, optional): specifies where to import/download data from DB|WAREHOUSE. Defaults to "DB".
        """
        print("Importing Data...")

        # validate if import_from is registered in config
        self.__validate_import_from(import_from)

        self.import_from = import_from.upper()

        # names of objects to import
        self.service_list = service_list

```
## Export Data Service Provider

```python
# scripts/Providers/ImportDataServiceProvider.py
class ExportDataServiceProvider(Service):

    # get the data stores from config.ini
    __upload_to_list = env("SERVER", "DATA_STORES")

    def __init__(
        self,
        service_list: List = None,
        export_to: str = "DB",
        schema=env("SERVER", "DB_STAGING_SCHEMA"),
    ) -> None:
        """uploads

        Args:
            service_list (List): Name of files to upload.
            upload_to (str, optional): where to upload the files, either 'DB' or 'WAREHOUSE'. Defaults to "DB".

        Raises:
            TypeError: if upload_to_type is not registered in config.ini
        """
        print("Uploading Data...")

        # validate if upload_to type is registered in config
        self.__validate_upload_to(upload_to)

        self.export_to = export_to.upper()
        # name of files in data/raw to upload.
        self.service_list = service_list
        # name of the postgres schema
        self.default_schema = schema


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

    service_path = "../d2b/sql"
```