CREATE VIEW IF NOT EXISTS per_month_revenues AS
SELECT
    strftime('%m', d.value) AS release_month,
    CAST(AVG(r.revenue) AS INT) AS total_revenue
FROM
    dwh_dim__movies m
JOIN
    dwh_fact__revenues r ON m.id = r.movie_id
JOIN
    dwh_dim__dates d ON m.release_date_id = d.id
GROUP BY
    release_month
ORDER BY
    total_revenue DESC;