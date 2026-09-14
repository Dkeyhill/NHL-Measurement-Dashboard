SELECT
	game_date
,	day_abbrev
,	game_id
,	season
,	game_type
,	CASE game_type
		WHEN 1 THEN 'Preseason'
		WHEN 2 THEN 'Regular Season'
		WHEN 3 THEN 'Playoffs'
		ELSE 'Unknown'
	END                                        AS game_type_desc
,	game_state
,	start_time_utc
,	CONVERT_TIMEZONE('UTC', 'America/New_York', start_time_utc) AS start_time_eastern
,	home_team_abbrev
,	away_team_abbrev
,	venue_name
,	loaded_at
FROM {{ ref('schedule') }}
QUALIFY ROW_NUMBER() OVER (
	PARTITION BY game_id
	ORDER BY loaded_at DESC
) = 1