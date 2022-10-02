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

DO $$
BEGIN
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
WITH monthly_holday_order AS (
    SELECT
        DATE(NOW()) AS ing_dt,
        ords.order_date,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 1 THEN 1
                ELSE 0
            END
        ) AS jan,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 2 THEN 2
                ELSE 0
            END
        ) AS feb,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 3 THEN 3
                ELSE 0
            END
        ) AS mar,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 4 THEN 4
                ELSE 0
            END
        ) AS apr,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 5 THEN 5
                ELSE 0
            END
        ) AS may,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 6 THEN 6
                ELSE 0
            END
        ) AS jun,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 7 THEN 7
                ELSE 0
            END
        ) AS jul,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 8 THEN 8
                ELSE 0
            END
        ) AS aug,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 9 THEN 9
                ELSE 0
            END
        ) AS sep,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 10 THEN 10
                ELSE 0
            END
        ) AS oct,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 11 THEN 11
                ELSE 0
            END
        ) AS nov,
        SUM(
            CASE
                WHEN dt.month_of_the_year_num = 12 THEN 12
                ELSE 0
            END
        ) AS dec
    FROM
        acnice6032_staging.orders ords
        JOIN if_common.dim_dates dt ON TO_DATE(
            ords.order_date:: text,
            'YYYY-MM-DD'
        ) <= dt.calendar_dt
    WHERE
        dt.working_day IS NOT TRUE
        AND (
            dt.day_of_the_week_num BETWEEN 1 AND 5
        )
        AND (
            EXTRACT(
                YEAR
                FROM
                    TO_DATE(
                        ords.order_date:: text,
                        'YYYY-MM-DD'
                    )
            ) = EXTRACT(
                YEAR
                FROM NOW()
            ) - 1
        )
    GROUP BY
        ords.order_date,
        dt.working_day,
        ing_dt
    ),
    tt_orders_placed AS (
    SELECT
        SUM(monthly.jan) AS tt_order_hol_jan,
        SUM(monthly.feb) AS tt_order_hol_feb,
        SUM(monthly.mar) AS tt_order_hol_apr,
        SUM(monthly.apr) AS tt_order_hol_may,
        SUM(monthly.may) AS tt_order_hol_jun,
        SUM(monthly.jul) AS tt_order_hol_jul,
        SUM(monthly.aug) AS tt_order_hol_aug,
        SUM(monthly.sep) AS tt_order_hol_sep,
        SUM(monthly.oct) AS tt_order_hol_oct,
        SUM(monthly.nov) AS tt_order_hol_nov,
        SUM(monthly.dec) AS tt_order_hol_dec
    FROM
        monthly_holday_order monthly
    )
    SELECT *
    FROM tt_orders_placed;

EXCEPTION WHEN unique_violation THEN RAISE NOTICE 'row skipped';

END;
$$ 