CREATE MATERIALIZED VIEW book_rating_stats AS
SELECT
    b.id AS book_id,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.id) AS review_count
FROM books b
LEFT JOIN reviews r ON b.id = r.book_id
GROUP BY b.id;
