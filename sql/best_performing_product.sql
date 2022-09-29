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
    DATE(NOW()) ingestion_date,
    product_name,
    tt_review_point, (
        pct_one_star_review / tt_review_point :: float
    ) * 100 pct_one_star_review, (
        pct_two_star_review / tt_review_point :: float
    ) * 100 pct_two_star_review, (
        pct_three_star_review / tt_review_point :: float
    ) * 100 pct_three_star_review, (
        pct_four_star_review / tt_review_point :: float
    ) * 100 pct_four_star_review, (
        pct_five_star_review / tt_review_point :: float
    ) * 100 pct_five_star_review
FROM (
        SELECT
            pro.product_name,
            SUM(rev.review) AS tt_review_point,
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
        FROM
            if_common.dim_products pro
            JOIN acnice6032_staging.reviews rev ON pro.product_id = rev.product_id
        GROUP BY
            product_name
    ) p_rev
ORDER BY
    tt_review_point,
    pct_one_star_review,
    pct_two_star_review,
    pct_three_star_review,
    pct_four_star_review,
    pct_five_star_review DESC