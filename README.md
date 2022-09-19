# Data2Bot-Assessment

## File Structure
```
Data2Bot-Assessment
├── README.md
├── requirements.txt
├── .gitignore
├── config.ini
├── config.ini.example
├── analytics
│   └── product_analytics.sql
│   └── product_orders_on_holidays.sql
│   └── total_shipment.sql
│   └── total_undelivered_shipments.sql
├── assets
├── data
│   ├── Raw
|   |   └── orders.csv
|   |   └── reviews.csv
|   |   └── shipments_deliveries.csv
│   ├── Transformed
|   |   └── 2022_09_18_agg_public_holiday.sql
├── logs
│   └── database.log
├── scripts
│   └── db_connect.py
│   └── extract.py
│   └── load.py 
├──handlers
│   └── LogHandler.py 
    └── Env.py 
```

## Setup
```bash
pip3 install -r requirements.txt
cp config.ini.example config.ini
```

After running the above script a new configuration file will be added to your file structure `config.ini`. Make sure to setup all necessary configurations with respect to the database.

Now run: 

```bash
python3 scripts/start.py
```