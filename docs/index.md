# D2b Data Pipeline
## **Overview**
D2b is a simple data pipeline designed to help automate the processes involved in extracting, transforming, analysing and exporting data insights carried out by data professionals at Data2bot. The automation pipeline is designed to abstract complexities and allow the analysts to focus solely on SQL.

<img src='assets/system.svg' alt='System flow'>

## Installation and setup 🔩🪛
Clone the repository.
```bash 
git clone https://github.com/anochima/Data2Bot-Assessment.git
cd data2bot-assessments
```
```bash
pip3 install -r configs/requirements.txt
cp configs/config.ini.example config.ini
```
The above commands will: 

* Download the project pipeline into your device
* Install all neccessary packages needed to successfully run the project
* Create a configuration file for setting up the Database connections, etc.


## **Database Configuration** 👨🏽‍💻
After running the above script, a new configuration file will be added to the project directory `config.ini`. Make sure to set up all necessary configurations for the database. 


Note ℹ️: The `config.ini` file is intended to abstract valuable information regarding database connection. 
Hence informations added here will be ignored during deployment.


```MD
[SERVER]
DB_CONNECTION=pgsql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=postgres
DB_USERNAME=root
DB_PASSWORD=''

DB_DEFAULT_SCHEMA =
DB_STAGING_SCHEMA =
DB_ANALYTICS_SCHEMA =  

S3_WAREHOUSE_BUCKET_NAME =

```
### **config.ini:** Retrieving configuration variables
To access the configuration variables into your python script. Import `env` function from `handlers.env_handler`.

The env() function sets or returns config file section, key value `env('SECTION', 'KEY', 'VALUE')`

* **section:** The config file section e.g SERVER
* **key:** A key in the selected section
* **value:(str, optional)** If set, overides the existing section key value in config.ini and set new key to the value specified.

```python
# scripts/Handlers/env_handler.py

from handlers.env_handler import env

# Get the database username
DB_USERNAME = env('SERVER', 'DB_USERNAME')
print(DB_USERNAME) 
#output: root 

# Change the DB_USERNAME from script
NEW_DB_USERNAME = env('SERVER', 'DB_USERNAME', 'new_username')
print(NEW_DB_USERNAME) 
#output: new_username

```

## Extracting Data From Warehouse 🏬

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

## Loading Data to Database ⬆️

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

## Running SQL Queries
All external SQL queries are stored inside the `/SQL` directory.
Any external query must be registered inside the <a href="https://github.com/anochima/Data2Bot-Assessment/blob/master/providers/AnalyticsServiceProvider.py" target='_blank'> Analytics Service Provider</a> class.

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
## Running the Pipeline ⚡️
To run the pipeline, simply run the following command in your terminal.
```bash
python3 scripts/start.py
```

## Documentation
To read the documentation, run `mkdocs serve` on terminal

# Handlers
