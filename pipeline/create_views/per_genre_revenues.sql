CREATE VIEW IF NOT EXISTS genre_revenues AS
WITH genre_data AS (
    SELECT
        m.id,
        json_each.value AS genre,
        r.revenue
    FROM
        dwh_dim__movies m
        ,json_each(m.genre)
    JOIN
        dwh_fact__revenues r ON m.id = r.movie_id
)
SELECT
    genre,
    SUM(revenue) AS total_revenue
FROM
    genre_data
GROUP BY
    genre
ORDER BY
	total_revenue DESC;