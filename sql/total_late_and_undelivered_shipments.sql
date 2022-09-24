CREATE TABLE
    IF NOT EXISTS acnice6032_analytics.agg_shipments (
        ingestion_date DATE PRIMARY KEY NOT NULL,
        tt_late_shipments INT NOT NULL,
        tt_undelivered_items INT NOT NULL
    );

-- INSERT INTO

--     acnice6032_analytics.agg_shipments (

--         ingestion_date,

--         tt_late_shipments,

--         tt_undelivered_items

--     ) -- A late shipment is one with shipment_date greater than or equal to 6 days after the order_date and delivery_date is NULL

SELECT 
    DATE(NOW()) AS ingestion_date

    COUNT(
        CASE WHEN (ships.shipment_date - ords.order_date ) >= 6 AND ships.delivery_date = NULL THEN 'LATE'
    ) END tt_late_shipments,
    
    -- COUNT(
    --     CASE WHEN  (ships.delivery_date AND ships.shipment_date) = NULL AND (TO_DATE('20220905', 'YYYYMMDD') - ords.order_date) >= 15
    -- ) tt_undelivered_shipments
FROM
    acnice6032_staging.shipment_deliveries ships
    JOIN acnice6032_staging.orders ords ON ords.order_id = ships.order_id;