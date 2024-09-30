CREATE VIEW IF NOT EXISTS directors_revenues AS
WITH director_data AS (
    SELECT
        m.id,
        json_each.value AS director,
        r.revenue
    FROM
        dwh_dim__movies m
        ,json_each(m.directors)
    JOIN
        dwh_fact__revenues r ON m.id = r.movie_id
)
SELECT
    director,
    SUM(revenue) AS total_revenue
FROM
    director_data
GROUP BY
    director
ORDER BY
	total_revenue DESC;