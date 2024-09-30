CREATE VIEW IF NOT EXISTS actors_revenues AS
WITH actor_data AS (
    SELECT
        m.id,
        json_each.value AS actor,
        r.revenue
    FROM
        dwh_dim__movies m
        ,json_each(m.actors)
    JOIN
        dwh_fact__revenues r ON m.id = r.movie_id
)
SELECT
    actor,
    SUM(revenue) AS total_revenue
FROM
    actor_data
GROUP BY
    actor
ORDER BY
	total_revenue DESC;

