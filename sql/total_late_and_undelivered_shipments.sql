
CREATE TABLE IF NOT EXISTS  acnice6032_analytics.agg_shipments (
    ingestion_date DATE PRIMARY KEY NOT NULL,
    tt_late_shipments INT NOT NULL,
    tt_undelivered_items INT NOT NULL
);

INSERT INTO acnice6032_analytics.agg_shipments VALUES (
    ingestion_date,
    tt_late_shipments,
    tt_undelivered_items
)
-- A late shipment is one with shipment_date greater than or equal to 6 days after the order_date and delivery_date is NULL 
SELECT COUNT(ship.shipment_date) AS tt_late_shipments
FROM (SELECT * FROM acnice6032_staging.shipments_deliveries)


-- SELECT userid, max(prdate)
-- from table1
-- group by 1

