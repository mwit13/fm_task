CREATE VIEW IF NOT EXISTS country_revenue AS
WITH country_data AS (
    SELECT
        m.id,
        json_each.value AS country,
        r.revenue
    FROM
        dwh_dim__movies m
        ,json_each(m.countries)
    JOIN
        dwh_fact__revenues r ON m.id = r.movie_id
)
SELECT
    country,
    SUM(revenue) AS total_revenue
FROM
    country_data
GROUP BY
    country
ORDER BY
	total_revenue DESC;