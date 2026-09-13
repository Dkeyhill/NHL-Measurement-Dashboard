{{ config(
    materialized='incremental',
    incremental_strategy='append'
) }}

SELECT
	day.value:date::date                     AS game_date
,	day.value:dayAbbrev::string               AS day_abbrev
,	game.value:id::number                    AS game_id
,	game.value:season::number                 AS season
,	game.value:gameType::number               AS game_type
,	game.value:gameState::string              AS game_state
,	game.value:startTimeUTC::timestamp_ntz    AS start_time_utc
,	game.value:homeTeam:abbrev::string        AS home_team_abbrev
,	game.value:awayTeam:abbrev::string        AS away_team_abbrev
,	game.value:venue:default::string          AS venue_name
,	s.loaded_at
FROM {{ source('raw', 'schedule') }} s
,	LATERAL FLATTEN(input => s.raw_json:gameWeek) day
,	LATERAL FLATTEN(input => day.value:games) game

{% if is_incremental() %}
WHERE s.loaded_at > (SELECT MAX(loaded_at) FROM {{ this }})
{% endif %}