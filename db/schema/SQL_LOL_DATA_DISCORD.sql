SELECT 
    fpm.match_id,
    dp.summoner_name,
    fpm.champion_id,
    fpm.kills,
    fpm.deaths,
    fpm.assists,
    fpm.win,
    fpm.total_cs,
    fpm.cs_per_min,
    fpm.gold_earned
FROM riot_fact.fact_player_match fpm
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
ORDER BY fpm.match_id, dp.summoner_name
LIMIT 20;
