-- Active: 1663811583289@@d2b-internal-assessment-dwh.cxeuj0ektqdz.eu-central-1.rds.amazonaws.com@5432@d2b_assessment
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

-- SELECT COUNT(rev) AS num_reviews(

SELECT
    pro.product_name,
    COUNT(rev),
    ords.order_date,
    dt.working_day
FROM
    acnice6032_staging.reviews rev
    JOIN if_common.dim_products pro ON rev.product_id = pro.product_id
    JOIN acnice6032_staging.orders ords ON pro.product_id = ords.product_id
    JOIN if_common.dim_dates dt ON TO_DATE(ords.order_date, 'YYYY-MM-DD') <= dt.calendar_dt
GROUP BY product_name, ords.order_date, dt.working_day;