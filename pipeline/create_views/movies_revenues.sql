CREATE VIEW IF NOT EXISTS movies_revenues AS
SELECT
    m.title,
    SUM(r.revenue) AS total_revenue
FROM
    dwh_dim__movies m
JOIN
    dwh_fact__revenues r ON m.id = r.movie_id
GROUP BY
    m.title
ORDER BY
	total_revenue DESC;