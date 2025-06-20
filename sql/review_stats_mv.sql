CREATE MATERIALIZED VIEW review_stats AS
SELECT
    COUNT(*) AS total_reviews,
    ROUND(AVG(rating), 2) AS avg_rating,
    MIN(rating) AS min_rating,
    MAX(rating) AS max_rating
FROM reviews;