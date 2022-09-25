CREATE TABLE
    IF NOT EXISTS acnice6032_analytics.agg_shipments (
        ingestion_date DATE PRIMARY KEY NOT NULL,
        tt_late_shipments INT NOT NULL,
        tt_undelivered_items INT NOT NULL
    );

DO $$ BEGIN
INSERT INTO
    acnice6032_analytics.agg_shipments (
        ingestion_date,
        tt_late_shipments,
        tt_undelivered_items
    )
SELECT
    DATE(NOW()) AS ing_dt,
    COUNT(
        CASE
            WHEN (
                DATE_PART(
                    'day',
                    ships.shipment_date:: timestamp - ords.order_date:: timestamp
                )
            ) >= 6
            AND ships.delivery_date IS NULL THEN 'LATE'
        END
    ) AS tt_late_shipments,
    COUNT(
        CASE
            WHEN ships.delivery_date IS NULL
            AND ships.shipment_date IS NULL
            AND DATE_PART(
                'day',
                '2022-09-05':: timestamp - ords.order_date:: timestamp
            ) >= 15 THEN 'NOT DELIVERED'
        END
    ) AS tt_undelivered_shipments
FROM
    acnice6032_staging.shipment_deliveries ships
    JOIN acnice6032_staging.orders ords ON ords.order_id = ships.order_id
GROUP BY ing_dt;

EXCEPTION WHEN unique_violation THEN RAISE NOTICE 'row skipped';

END;

$$;