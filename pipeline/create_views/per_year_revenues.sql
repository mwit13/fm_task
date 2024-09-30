CREATE VIEW IF NOT EXISTS per_year_revenues AS
SELECT
    strftime('%Y', d.value) AS release_year,
    CAST(AVG(r.revenue) AS INT) AS total_revenue
FROM
    dwh_dim__movies m
JOIN
    dwh_fact__revenues r ON m.id = r.movie_id
JOIN
    dwh_dim__dates d ON m.release_date_id = d.id
GROUP BY
    release_year
ORDER BY
	total_revenue DESC;