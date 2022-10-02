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

-- Get the product with highest reviews

DO $$
BEGIN 
INSERT INTO acnice6032_analytics.best_performing_product(
	ingestion_date,
	product_name,
	most_ordered_day,
	is_public_holiday,
	tt_review_points,
	pct_one_star_review,
	pct_two_star_review,
	pct_three_star_review,
	pct_four_star_review,
	pct_five_star_review,
	pct_early_shipments,
	pct_late_shipments
)
WITH
    product_with_highest_rev AS (
        SELECT
            pro.product_name,
            pro.product_id,
            SUM(rev.review) AS tt_review_point
        FROM
            if_common.dim_products pro
            JOIN acnice6032_staging.reviews rev ON rev.product_id = pro.product_id
        GROUP BY
            pro.product_name,
            pro.product_id
        ORDER BY tt_review_point DESC
        LIMIT
            1
    ), most_ordered_date AS (
        SELECT
            pro.product_id,
            pro.product_name,
            ords.order_date,
            pro.tt_review_point,
            COUNT(ords.order_date) num_orders
        FROM
            product_with_highest_rev pro
            JOIN acnice6032_staging.orders ords ON ords.product_id = pro.product_id
        GROUP BY
            pro.product_id,
            ords.order_date,
            pro.product_name,
            pro.tt_review_point
        ORDER BY num_orders DESC
        LIMIT 1
    ), is_working_day AS (
        SELECT
            most_ordered_date.product_id,
            most_ordered_date.product_name,
            most_ordered_date.order_date AS most_ordered_day,
            dt.working_day,
            most_ordered_date.tt_review_point
        FROM most_ordered_date
            JOIN if_common.dim_dates dt ON dt.calendar_dt = TO_DATE(
                most_ordered_date.order_date :: text, 'YYYY-MM-DD'
            )
    ), review_dist AS (
        SELECT
            wd.product_id,
            wd.product_name,
            wd.most_ordered_day,
            wd.working_day,
            wd.tt_review_point,
            SUM(
                CASE
                    WHEN rev.review = 1 THEN 1
                END
            ) AS pct_one_star_review,
            SUM(
                CASE
                    WHEN rev.review = 2 THEN 2
                END
            ) AS pct_two_star_review,
            SUM(
                CASE
                    WHEN rev.review = 3 THEN 3
                END
            ) AS pct_three_star_review,
            SUM(
                CASE
                    WHEN rev.review = 4 THEN 4
                END
            ) AS pct_four_star_review,
            SUM(
                CASE
                    WHEN rev.review = 5 THEN 5
                END
            ) AS pct_five_star_review
        FROM is_working_day wd
            JOIN acnice6032_staging.reviews rev ON rev.product_id = wd.product_id
        GROUP BY
            wd.product_id,
            wd.product_name,
            wd.most_ordered_day,
            wd.working_day,
            wd.tt_review_point
    ),
    reviews_dist_pct AS (
        SELECT
            rd.product_id,
            ords.order_id,
            rd.product_name,
            rd.most_ordered_day,
            rd.working_day,
            rd.tt_review_point,
            ROUND( (
                    rd.pct_one_star_review / rd.tt_review_point
                ) * 100 :: numeric,
                2
            ) pct_one_star_review,
            ROUND( (
                    rd.pct_two_star_review / rd.tt_review_point
                ) * 100 :: numeric,
                2
            ) pct_two_star_review,
            ROUND( (
                    rd.pct_three_star_review / rd.tt_review_point
                ) * 100 :: numeric,
                2
            ) pct_three_star_review,
            ROUND( (
                    rd.pct_four_star_review / rd.tt_review_point
                ) * 100 :: numeric,
                2
            ) pct_four_star_review,
            ROUND( (
                    rd.pct_five_star_review / rd.tt_review_point
                ) * 100 :: numeric,
                2
            ) pct_five_star_review
        FROM review_dist rd
            JOIN acnice6032_staging.orders ords ON ords.product_id = rd.product_id
    ), shipment_dist AS (
        SELECT
            rdp.product_id,
            rdp.product_name,
            rdp.most_ordered_day,
            rdp.working_day,
            rdp.tt_review_point,
            rdp.pct_one_star_review,
            rdp.pct_two_star_review,
            rdp.pct_three_star_review,
            rdp.pct_four_star_review,
            rdp.pct_five_star_review,
            COUNT(
                CASE
                    WHEN (
                        TO_DATE(
                            ships.shipment_date :: text,
                            'YYYY-MM-DD'
                        ) - TO_DATE(
                            rdp.most_ordered_day :: text,
                            'YYYY-MM-DD'
                        )
                    ) < 6
                    AND ships.delivery_date IS NOT NULL THEN 'EARLY'
                END
            ) AS pct_early_shipments,
            COUNT(
                CASE
                    WHEN (
                        TO_DATE(
                            ships.shipment_date :: text,
                            'YYYY-MM-DD'
                        ) - TO_DATE(
                            rdp.most_ordered_day :: text,
                            'YYYY-MM-DD'
                        )
                    ) >= 6
                    AND ships.delivery_date IS NULL THEN 'LATE'
                END
            ) AS pct_late_shipments,
            COUNT(*) AS shipment_count
        FROM reviews_dist_pct rdp
            JOIN acnice6032_staging.shipment_deliveries ships ON ships.order_id = rdp.order_id
        GROUP BY
            rdp.product_id,
            rdp.product_name,
            rdp.most_ordered_day,
            rdp.working_day,
            rdp.tt_review_point,
            rdp.pct_one_star_review,
            rdp.pct_two_star_review,
            rdp.pct_three_star_review,
            rdp.pct_four_star_review,
            rdp.pct_five_star_review
    ),
    shipment_dist_pct AS (
        SELECT
            DATE(NOW()) AS ingestion_date,
            ship_dist.product_name,
            ship_dist.most_ordered_day::date,
            ship_dist.working_day,
            ship_dist.tt_review_point,
            ship_dist.pct_one_star_review,
            ship_dist.pct_two_star_review,
            ship_dist.pct_three_star_review,
            ship_dist.pct_four_star_review,
            ship_dist.pct_five_star_review,
            ROUND( (
                    ship_dist.pct_early_shipments / ship_dist.shipment_count
                ) * 100 :: numeric,
                2
            ) pct_early_shipments,
            ROUND( (
                    ship_dist.pct_late_shipments / ship_dist.shipment_count
                ) * 100 :: numeric,
                2
            ) pct_late_shipments
        FROM shipment_dist ship_dist
    )
select *
from shipment_dist_pct;

EXCEPTION WHEN unique_violation THEN RAISE NOTICE 'row skipped';

END;

$$ 