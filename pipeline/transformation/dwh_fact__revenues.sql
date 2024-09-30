INSERT INTO dwh_fact__revenues (
	movie_id
	,distributor_id
	,date_id
	,revenue
	,theaters_number
	)
SELECT *
FROM (
	SELECT dim_movies.id AS movie_id
		,distributors.id AS distributor_id
		,dates.id AS date_id
		,revenue
		,theaters AS theaters_number
	FROM stg_revenues_per_day stg_revenues
	LEFT JOIN stg_movies_details stg_movies ON stg_revenues.title = stg_movies.title
	LEFT JOIN dwh_dim__movies dim_movies ON json_extract(stg_movies.response, '$.Title') = dim_movies.title
	LEFT JOIN dwh_dim__dates dates ON stg_revenues.DATE = dates.value
	LEFT JOIN dwh_dim__distributors distributors ON stg_revenues.distributor = distributors.NAME
	WHERE stg_movies.title IS NOT NULL
	) a
WHERE 1
ON CONFLICT(movie_id, date_id) DO UPDATE
SET distributor_id = excluded.distributor_id
	,revenue = excluded.revenue
	,theaters_number = excluded.theaters_number
WHERE revenue != excluded.revenue
	OR theaters_number != excluded.theaters_number;
