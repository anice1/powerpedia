# D2b Data Pipeline
## **Overview**
D2b is a simple data pipeline designed to help automate the processes involved in extracting, transforming, analysing and exporting data insights carried out by data professionals at Data2bot. The automation pipeline is designed to abstract complexities and allow the analysts to focus solely on SQL.

<img src='assets/system.svg' alt='System flow'>

## Setup 🔩🪛
```bash
pip3 install -r configs/requirements.txt
cp configs/config.ini.example config.ini
```
The above commands will: 

* Download the project pipeline to you device
* Install all neccessary packages needed to successfull run the project
* Create a configuration file for setting up the Database connections, etc.

After running the above script, a new configuration file will be added to your file structure `config.ini`. Make sure to set up all necessary configurations for the database.

## **Database Configuration** 👨🏽‍💻
To set up the database connection, go to `config.ini` under the SERVER collection and add the database connection information.
```MD
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
## **Extracting Data From Warehouse 🏬**

## Running SQL Queries
All external SQL queries are stored inside the `/SQL directory.
Any external query must be registered inside the <a href="https://github.com/anochima/Data2Bot-Assessment/blob/master/providers/AnalyticsServiceProvider.py" target='_blank'> Analytics Service Provider</a> class.

```python
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
