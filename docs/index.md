# D2b Data Pipeline
## **Overview** 
D2b is a simple data pipeline designed to help automate the processes involved in extracting, transforming, analysing and exporting data insights carried out by data professionals at Data2bot. The automation pipeline is designed to abstract complexities and allow the analysts to focus solely on SQL.

<img src='assets/system.svg' alt='System flow'>

## Setup 🔩🪛
```bash
pip3 install -r configs/requirements.txt
cp configs/config.ini.example config.ini
```

After running the above script a new configuration file will be added to your file structure `config.ini`. Make sure to setup all necessary configurations with respect to the database.

## Database Configuration 👨🏽‍💻
To setup the database connection, goto `config.ini` unders the SERVER collection add the database connection information.
```md
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

## Running the Pipeline ⚡️
To run the pipeline, simply run the following command in your terminal.
```bash
python3 scripts/start.py
```

## Documentation
For help run `mkdocs serve` on terminal