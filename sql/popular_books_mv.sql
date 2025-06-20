CREATE MATERIALIZED VIEW popular_books AS
SELECT
    b.id AS book_id,
    b.title,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM books b
JOIN favorites f ON b.id = f.book_id
LEFT JOIN reviews r ON b.id = r.book_id
GROUP BY b.id, b.title
HAVING COUNT(r.id) > 0
ORDER BY avg_rating DESC;


