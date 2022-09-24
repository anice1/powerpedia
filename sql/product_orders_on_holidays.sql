CREATE TABLE
    IF NOT EXISTS acnice6032_analytics.agg_public_holiday (
        ingestion_date DATE PRIMARY KEY NOT NULL,
        tt_order_hol_jan INT NOT NULL,
        tt_order_hol_feb INT NOT NULL,
        tt_order_hol_mar INT NOT NULL,
        tt_order_hol_apr INT NOT NULL,
        tt_order_hol_may INT NOT NULL,
        tt_order_hol_jun INT NOT NULL,
        tt_order_hol_jul INT NOT NULL,
        tt_order_hol_aug INT NOT NULL,
        tt_order_hol_sep INT NOT NULL,
        tt_order_hol_oct INT NOT NULL,
        tt_order_hol_nov INT NOT NULL,
        tt_order_hol_dec INT NOT NULL
    );

INSERT INTO
    acnice6032_analytics.agg_public_holiday (
        ingestion_date,
        tt_order_hol_jan,
        tt_order_hol_feb,
        tt_order_hol_mar,
        tt_order_hol_apr,
        tt_order_hol_may,
        tt_order_hol_jun,
        tt_order_hol_jul,
        tt_order_hol_aug,
        tt_order_hol_sep,
        tt_order_hol_oct,
        tt_order_hol_nov,
        tt_order_hol_dec
    )
SELECT ords.order_date,
    COUNT(CASE WHEN ords.month_of_the_year_num = 1) jan,
    COUNT(CASE WHEN ords.month_of_the_year_num = 2) feb,
    COUNT(CASE WHEN ords.month_of_the_year_num = 3) mar, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 4) apr, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 5) may, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 6) jun, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 7) jul, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 8) aug,
    COUNT(CASE WHEN ords.month_of_the_year_num = 9) sep, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 10) oct, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 11) nov,
    COUNT(CASE WHEN ords.month_of_the_year_num = 12) decc

FROM if_common.dim_dates dt
    JOIN acnice6032_staging.orders ords ON TO_DATE(ords.order_date, 'YYYY-MM-DD') <= dt.calendar_dt;
GROUP BY
    dt.month_of_the_year_num
HAVING
    dt.working_day = 'false'
    AND (dt.day_of_the_week_num BETWEEN 1 AND 5)
    AND (YEAR(ords.order_date) = YEAR(GETDATE())) - 1;