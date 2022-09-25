CREATE TABLE
    IF NOT EXISTS acnice6032_analytics.best_performing_product(
        ingestion_date DATE PRIMARY KEY NOT NULL,
        product_name VARCHAR NOT NULL,
        most_ordered_day date NOT NULL,
        is_public_holiday BOOLEAN NOT NULL,
        tt_review_points INT NOT NULL,
        pct_one_star_review FLOAT NOT NULL,
        pct_two_star_review FLOAT NOT NULL,
        pct_three_star_review FLOAT NOT NULL,
        pct_four_star_review FLOAT NOT NULL,
        pct_five_star_review FLOAT NOT NULL,
        pct_early_shipments FLOAT NOT NULL,
        pct_late_shipments FLOAT NOT NULL
    );

SELECT pro.product_name 
FROM 
if_common.dim_products