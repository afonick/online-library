CREATE MATERIALIZED VIEW top_authors AS
SELECT
    b.author_id,
    u.username,
    COUNT(DISTINCT b.id) AS book_count,
    COUNT(r.id) AS review_count,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM books b
JOIN users u ON u.id = b.author_id
LEFT JOIN reviews r ON r.book_id = b.id
GROUP BY b.author_id, u.username
HAVING COUNT(r.id) > 0
ORDER BY avg_rating DESC;



