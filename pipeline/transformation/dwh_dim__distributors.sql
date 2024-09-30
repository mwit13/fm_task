INSERT INTO dwh_dim__distributors (name)
SELECT a.name
FROM (
	SELECT DISTINCT distributor AS name
	FROM stg_revenues_per_day
	WHERE distributor IS NOT '-'
	AND distributor IS NOT NULL
	) a
WHERE 1 ON CONFLICT(name) DO NOTHING;
