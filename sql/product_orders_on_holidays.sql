
DROP TABLE IF EXISTS acnice6032_analytics.agg_public_holiday;


CREATE TABLE acnice6032_analytics.agg_public_holiday (ingestion_date DATE PRIMARY KEY NOT NULL,
                                                                                      _month DATE NOT NULL,
                                                                                                  num_orders INTEGER NOT NULL);


INSERT INTO acnice6032_analytics.agg_public_holiday
VALUES (ingestion_date,
        _month,
        num_orders)
SELECT ords.order_date AS ingestion_date,
       dt.month_of_the_year_num AS _month,
       COUNT(ords) AS num_orders
FROM if_common.dim_dates dt
JOIN acnice6032_staging.orders ords ON ords.order_date = dt.calendar_date
GROUP BY _month
HAVING dt.working_day = false
AND YEAR(ords.order_date) = YEAR(GETDATE()) - 1;