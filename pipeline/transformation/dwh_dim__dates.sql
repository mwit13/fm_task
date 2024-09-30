INSERT INTO dwh_dim__dates (value)
SELECT a.value
FROM (
	SELECT DISTINCT "date" AS value
	FROM stg_revenues_per_day
	UNION
	SELECT DISTINCT strftime('%Y-%m-%d', substr(json_extract(response, '$.Released'), 8, 4) || '-' || CASE substr(json_extract(response, '$.Released'), 4, 3)
				WHEN 'Jan'
					THEN '01'
				WHEN 'Feb'
					THEN '02'
				WHEN 'Mar'
					THEN '03'
				WHEN 'Apr'
					THEN '04'
				WHEN 'May'
					THEN '05'
				WHEN 'Jun'
					THEN '06'
				WHEN 'Jul'
					THEN '07'
				WHEN 'Aug'
					THEN '08'
				WHEN 'Sep'
					THEN '09'
				WHEN 'Oct'
					THEN '10'
				WHEN 'Nov'
					THEN '11'
				WHEN 'Dec'
					THEN '12'
				END || '-' || substr(json_extract(response, '$.Released'), 1, 2)) AS value
	FROM stg_movies_details
	UNION
	SELECT strftime('%Y-%m-%d', substr(json_extract(response, '$.DVD'), 8, 4) || '-' || CASE substr(json_extract(response, '$.DVD'), 4, 3)
				WHEN 'Jan'
					THEN '01'
				WHEN 'Feb'
					THEN '02'
				WHEN 'Mar'
					THEN '03'
				WHEN 'Apr'
					THEN '04'
				WHEN 'May'
					THEN '05'
				WHEN 'Jun'
					THEN '06'
				WHEN 'Jul'
					THEN '07'
				WHEN 'Aug'
					THEN '08'
				WHEN 'Sep'
					THEN '09'
				WHEN 'Oct'
					THEN '10'
				WHEN 'Nov'
					THEN '11'
				WHEN 'Dec'
					THEN '12'
				END || '-' || substr(json_extract(response, '$.DVD'), 1, 2)) AS value
	FROM stg_movies_details
    UNION
    SELECT
        CASE
            WHEN substr(json_extract(response, '$.Year'), 1, 4)
                THEN substr(json_extract(response, '$.Year'), 1, 4) || '-01-01'
            ELSE NULL
            END AS value
	FROM stg_movies_details
    UNION
    SELECT
        CASE
            WHEN substr(json_extract(response, '$.Year'), 6, 4)
                THEN substr(json_extract(response, '$.Year'), 6, 4) || '-01-01'
            ELSE NULL
            END value
    FROM stg_movies_details
	) a
WHERE value IS NOT NULL ON CONFLICT(value) DO NOTHING;
