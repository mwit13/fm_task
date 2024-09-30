INSERT INTO dwh_dim__movies_reviewers (name)
SELECT a.name
FROM (
	SELECT DISTINCT json_extract(value, '$.Source') AS name
	FROM stg_movies_details
		,json_each(stg_movies_details.response, '$.Ratings')
	UNION ALL
	SELECT 'IMDb'
	) a
WHERE 1 ON CONFLICT(NAME) DO NOTHING;
