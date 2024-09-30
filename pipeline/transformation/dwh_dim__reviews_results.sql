INSERT INTO dwh_dim__reviews_results (
	movie_id
	,reviewer_id
	,score_percent
	)
SELECT *
FROM (
	SELECT a.movie_id
		,a.reviewer_id
		,CASE
			WHEN a.value LIKE '%\%%' ESCAPE '\'
				THEN replace(a.value, '%', '')
			ELSE CASE
					WHEN a.value LIKE '%/%'
						THEN CAST(SUBSTR(a.value, 1, INSTR(a.value, '/') - 1) AS FLOAT) / CAST(SUBSTR(a.value, INSTR(a.value, '/') + 1, 3) AS FLOAT) * 100
					ELSE a.value
					END
			END AS score_percent
	FROM (
		SELECT json_extract(value, '$.Value') AS value
			,dim_movies.id AS movie_id
			,dim_reviewers.id reviewer_id
		FROM stg_movies_details stg_md
			,json_each(stg_md.response, '$.Ratings')
		LEFT JOIN dwh_dim__movies dim_movies ON json_extract(stg_md.response, '$.Title') = dim_movies.title
		LEFT JOIN dwh_dim__movies_reviewers dim_reviewers ON json_extract(value, '$.Source') = dim_reviewers.NAME
		WHERE dim_movies.id IS NOT NULL
			AND dim_reviewers.id IS NOT NULL
		) a
	UNION ALL
	SELECT dim_movies.id AS movie_id
		,dim_reviewers.id AS reviewer_id
		,json_extract(stg_md.response, '$.imdbRating') * 10 AS score_percent
	FROM stg_movies_details stg_md
	LEFT JOIN dwh_dim__movies dim_movies ON json_extract(stg_md.response, '$.Title') = dim_movies.title
	LEFT JOIN dwh_dim__movies_reviewers dim_reviewers ON 'IMDb' = dim_reviewers.NAME
	WHERE dim_movies.id IS NOT NULL
		AND dim_reviewers.id IS NOT NULL
	) b
WHERE 1
ON CONFLICT(movie_id, reviewer_id) DO UPDATE
SET score_percent = excluded.score_percent
WHERE score_percent != excluded.score_percent;
