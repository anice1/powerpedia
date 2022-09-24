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

-- INSERT INTO
--     acnice6032_analytics.agg_public_holiday (
--         ingestion_date,
--         tt_order_hol_jan,
--         tt_order_hol_feb,
--         tt_order_hol_mar,
--         tt_order_hol_apr,
--         tt_order_hol_may,
--         tt_order_hol_jun,
--         tt_order_hol_jul,
--         tt_order_hol_aug,
--         tt_order_hol_sep,
--         tt_order_hol_oct,
--         tt_order_hol_nov,
--         tt_order_hol_dec
--     )
SELECT poh.ingestion_date, poh.jan, poh.feb, poh.mar, poh.apr FROM(

SELECT 
    DATE(NOW()) AS ingestion_date
    COUNT(CASE WHEN ords.month_of_the_year_num = 1 THEN 1) AS jan,
    COUNT(CASE WHEN ords.month_of_the_year_num = 2 THEN 2) AS feb,
    COUNT(CASE WHEN ords.month_of_the_year_num = 3 THEN 3) AS mar, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 4 THEN 4) AS apr, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 5 THEN 5) AS  may, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 6 THEN 6) AS jun, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 7 THEN 7) AS jul, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 8 THEN 8) AS aug,
    COUNT(CASE WHEN ords.month_of_the_year_num = 9 THEN 9) AS sep, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 10 THEN 10) AS oct, 
    COUNT(CASE WHEN ords.month_of_the_year_num = 11 THEN 11) AS nov,
    COUNT(CASE WHEN ords.month_of_the_year_num = 12 THEN 12) AS decc,
    dt.working_day,
    dt.day_of_the_week_num,
    ords.order_date

FROM acnice6032_staging.orders ords
    JOIN if_common.dim_dates dt ON TO_DATE(ords.order_date, 'YYYY-MM-DD') <= dt.calendar_dt;
GROUP BY
    dt.month_of_the_year_num
) poh 
WHERE 
    poh.working_day = 'false'
    AND (dt.day_of_the_week_num BETWEEN 1 AND 5)
    AND (YEAR(ords.order_date) = YEAR(NOW()) - 1);