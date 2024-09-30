CREATE VIEW IF NOT EXISTS per_rating_revenues AS
SELECT
    m.rated AS rating,
    SUM(r.revenue) AS total_revenue
FROM
    dwh_dim__movies m
JOIN
    dwh_fact__revenues r ON m.id = r.movie_id
GROUP BY
    m.rated
ORDER BY
	total_revenue DESC;