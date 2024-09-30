INSERT INTO dwh_dim__movies (
	title
	,start_year_date_id
	,end_year_date_id
	,rated
	,release_date_id
	,length_min
	,genre
	,directors
	,writers
	,actors
	,plot
	,languages
	,countries
	,awards
	,poster_url
	,imdb_votes_number
	,imdb_id
	,"type"
	,dvd_release_date_id
	,boxoffice
	,production
	)
SELECT *
FROM (
	SELECT title AS title
	    ,dates3.id AS start_year_date_id
        ,dates4.id AS end_year_date_id
        ,rated AS rated
		,dates1.id AS release_date_id
		,CAST(runtime AS INT) AS length_min
		,replace(json_array(trim(replace(genre, ', ', '","'))), '\', '') AS genre
		,CASE
			WHEN directors = 'N/A'
				THEN NULL
			ELSE replace(json_array(trim(replace(directors, ', ', '","'))), '\', '')
			END AS directors
		,CASE
			WHEN writers = 'N/A'
				THEN NULL
			ELSE replace(json_array(trim(replace(writers, ', ', '","'))), '\', '')
			END AS writers
		,replace(json_array(trim(replace(actors, ', ', '","'))), '\', '') AS actors
		,CASE
			WHEN plot = 'N/A'
				THEN NULL
			ELSE plot
			END AS plot
		,CASE
			WHEN languages = 'N/A'
				THEN NULL
			ELSE replace(json_array(trim(replace(languages, ', ', '","'))), '\', '')
			END AS languages
		,replace(json_array(trim(replace(countries, ', ', '","'))), '\', '') AS countries
		,CASE
			WHEN awards = 'N/A'
				THEN NULL
			ELSE awards
			END AS awards
		,CASE
			WHEN poster = 'N/A'
				THEN NULL
			ELSE poster
			END AS poster_url
		,CAST(REPLACE(imdb_votes, ',', '') AS INT) AS imdb_votes_number
		,imdb_id AS imdb_id
		,upper(type_) AS "type"
		,dates2.id AS dvd_release_date_id
		,CAST(REPLACE(REPLACE(boxoffice, '$', ''), ',', '') AS INT) AS boxoffice
		,CASE
			WHEN production = 'N/A'
				THEN NULL
			ELSE production
			END AS production
	FROM (
		SELECT json_extract(response, '$.Title') title
		    ,CASE
                WHEN substr(json_extract(response, '$.Year'), 1, 4)
                    THEN substr(json_extract(response, '$.Year'), 1, 4) || '-01-01'
                ELSE NULL
                END start_year_date
            ,CASE
                WHEN substr(json_extract(response, '$.Year'), 6, 4)
                    THEN substr(json_extract(response, '$.Year'), 6, 4) || '-01-01'
                ELSE NULL
                END end_year_date
			,json_extract(response, '$.Rated') rated
			,strftime('%Y-%m-%d', substr(json_extract(response, '$.Released'), 8, 4) || '-' || CASE substr(json_extract(response, '$.Released'), 4, 3)
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
					END || '-' || substr(json_extract(response, '$.Released'), 1, 2)) AS release_date
			,json_extract(response, '$.Runtime') runtime
			,json_extract(response, '$.Genre') genre
			,json_extract(response, '$.Director') directors
			,json_extract(response, '$.Writer') writers
			,json_extract(response, '$.Actors') actors
			,json_extract(response, '$.Plot') plot
			,json_extract(response, '$.Language') languages
			,json_extract(response, '$.Country') countries
			,json_extract(response, '$.Awards') awards
			,json_extract(response, '$.Poster') poster
			,json_extract(response, '$.imdbVotes') imdb_votes
			,json_extract(response, '$.imdbID') imdb_id
			,json_extract(response, '$.Type') type_
			,strftime('%Y-%m-%d', substr(json_extract(response, '$.DVD'), 8, 4) || '-' || CASE substr(json_extract(response, '$.DVD'), 4, 3)
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
					END || '-' || substr(json_extract(response, '$.DVD'), 1, 2)) AS dvd_release_date
			,json_extract(response, '$.BoxOffice') boxoffice
			,json_extract(response, '$.Production') production
		FROM stg_movies_details
		) a
	LEFT JOIN dwh_dim__dates dates1 ON a.release_date = dates1.value
	LEFT JOIN dwh_dim__dates dates2 ON a.dvd_release_date = dates2.value
	LEFT JOIN dwh_dim__dates dates3 ON a.start_year_date = dates3.value
	LEFT JOIN dwh_dim__dates dates4 ON a.end_year_date = dates4.value
	) b
WHERE 1 ON CONFLICT(imdb_id) DO UPDATE
SET title = excluded.title
	,start_year_date_id = excluded.start_year_date_id
	,end_year_date_id = excluded.end_year_date_id
	,rated = excluded.rated
	,release_date_id = excluded.release_date_id
	,length_min = excluded.length_min
	,genre = excluded.genre
	,directors = excluded.directors
	,writers = excluded.writers
	,actors = excluded.actors
	,plot = excluded.plot
	,languages = excluded.languages
	,countries = excluded.countries
	,awards = excluded.awards
	,poster_url = excluded.poster_url
	,imdb_votes_number = excluded.imdb_votes_number
	,"type" = excluded."type"
	,dvd_release_date_id = excluded.dvd_release_date_id
	,boxoffice = excluded.boxoffice
	,production = excluded.production
WHERE title != excluded.title
	OR start_year_date_id != excluded.start_year_date_id
	OR end_year_date_id != excluded.end_year_date_id
	OR rated != excluded.rated
	OR release_date_id != excluded.release_date_id
	OR length_min != excluded.length_min
	OR genre != excluded.genre
	OR directors != excluded.directors
	OR writers != excluded.writers
	OR actors != excluded.actors
	OR plot != excluded.plot
	OR languages != excluded.languages
	OR countries != excluded.countries
	OR awards != excluded.awards
	OR poster_url != excluded.poster_url
	OR imdb_votes_number != excluded.imdb_votes_number
	OR "type" != excluded."type"
	OR dvd_release_date_id != excluded.dvd_release_date_id
	OR boxoffice != excluded.boxoffice
	OR production != excluded.production
