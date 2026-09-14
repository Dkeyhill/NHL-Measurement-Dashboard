SELECT
	game_id
,	game_date
,	season
,	game_type_desc                            AS game_type
,	game_state
,	start_time_eastern
,	home_team_abbrev                          AS home_team
,	away_team_abbrev                          AS away_team
,	venue_name
FROM {{ ref('stg_schedule') }}