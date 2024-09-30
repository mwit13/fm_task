CREATE VIEW IF NOT EXISTS writers_revenues AS
WITH writer_data AS (
    SELECT
        m.id,
        json_each.value AS writer,
        r.revenue
    FROM
        dwh_dim__movies m
        ,json_each(m.writers)
    JOIN
        dwh_fact__revenues r ON m.id = r.movie_id

)
SELECT
    writer,
    SUM(revenue) AS total_revenue
FROM
    writer_data
GROUP BY
    writer
ORDER BY
	total_revenue DESC;