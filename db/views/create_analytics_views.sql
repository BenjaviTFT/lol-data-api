-- ============================================================
-- SCHEMA ANALYTICS
-- ============================================================

CREATE SCHEMA IF NOT EXISTS riot_analytics;

-- ============================================================
-- VUE 1 : STATS PAR JOUEUR (vue de base)
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.player_stats AS
SELECT
    dp.player_id,
    dp.summoner_name || '#' || dp.tag_line AS display_name,
    dp.summoner_name,
    dp.tag_line,

    COUNT(*) AS total_games,
    SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN NOT fpm.win THEN 1 ELSE 0 END) AS losses,
    ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_pct,

    ROUND(AVG(fpm.kills)::numeric, 1) AS avg_kills,
    ROUND(AVG(fpm.deaths)::numeric, 1) AS avg_deaths,
    ROUND(AVG(fpm.assists)::numeric, 1) AS avg_assists,
    ROUND(AVG((fpm.kills + fpm.assists)::float / NULLIF(fpm.deaths, 0))::numeric, 2) AS kda_ratio,

    ROUND(AVG(fpm.cs_per_min)::numeric, 1) AS avg_cs_per_min,
    ROUND(AVG(fpm.damage_per_min)::numeric, 0) AS avg_dpm,
    ROUND(AVG(fpm.gold_per_min)::numeric, 0) AS avg_gpm,
    ROUND(AVG(fpm.vision_score)::numeric, 1) AS avg_vision
FROM riot_fact.fact_player_match fpm
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
GROUP BY dp.player_id, dp.summoner_name, dp.tag_line;

-- ============================================================
-- VUE 2 : CHAMPIONS JOUES PAR JOUEUR
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.player_champions AS
SELECT
    dp.player_id,
    dp.summoner_name || '#' || dp.tag_line AS display_name,
    fpm.champion_id,
    COALESCE(dc.champion_name, 'Unknown') AS champion_name,
    COALESCE(dc.champion_key, 'Unknown') AS champion_key,

    COUNT(*) AS games_played,
    SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN NOT fpm.win THEN 1 ELSE 0 END) AS losses,
    ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_pct,

    ROUND(AVG(fpm.kills)::numeric, 1) AS avg_kills,
    ROUND(AVG(fpm.deaths)::numeric, 1) AS avg_deaths,
    ROUND(AVG(fpm.assists)::numeric, 1) AS avg_assists,
    ROUND(AVG((fpm.kills + fpm.assists)::float / NULLIF(fpm.deaths, 0))::numeric, 2) AS avg_kda,

    ROUND(AVG(fpm.cs_per_min)::numeric, 1) AS avg_cs_per_min,
    ROUND(AVG(fpm.damage_per_min)::numeric, 0) AS avg_dpm
FROM riot_fact.fact_player_match fpm
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
LEFT JOIN riot_dim.dim_champion dc ON fpm.champion_id = dc.champion_id
GROUP BY dp.player_id, dp.summoner_name, dp.tag_line, fpm.champion_id, dc.champion_name, dc.champion_key
ORDER BY dp.player_id, games_played DESC;

-- ============================================================
-- VUE 3 : DUOQ SYNERGIES
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.duoq_synergies AS
SELECT
    p1.player_id AS player_1_id,
    p1.summoner_name || '#' || p1.tag_line AS player_1_name,
    p2.player_id AS player_2_id,
    p2.summoner_name || '#' || p2.tag_line AS player_2_name,

    COUNT(*) AS games_together,
    SUM(CASE WHEN fpm1.win THEN 1 ELSE 0 END) AS wins_together,
    SUM(CASE WHEN NOT fpm1.win THEN 1 ELSE 0 END) AS losses_together,
    ROUND(100.0 * SUM(CASE WHEN fpm1.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_pct,

    ROUND(AVG((fpm1.kills + fpm1.assists)::float / NULLIF(fpm1.deaths, 0))::numeric, 2) AS p1_avg_kda,
    ROUND(AVG((fpm2.kills + fpm2.assists)::float / NULLIF(fpm2.deaths, 0))::numeric, 2) AS p2_avg_kda,

    MAX(mg.game_start) AS last_played
FROM riot_fact.fact_player_match fpm1
JOIN riot_fact.fact_player_match fpm2
    ON fpm1.match_id = fpm2.match_id
    AND fpm1.player_id < fpm2.player_id
JOIN riot_dim.dim_player p1 ON fpm1.player_id = p1.player_id
JOIN riot_dim.dim_player p2 ON fpm2.player_id = p2.player_id
JOIN riot_fact.match_game mg ON fpm1.match_id = mg.match_id
GROUP BY p1.player_id, p1.summoner_name, p1.tag_line, p2.player_id, p2.summoner_name, p2.tag_line
HAVING COUNT(*) >= 1
ORDER BY games_together DESC;

-- ============================================================
-- VUE 4 : RANKING INTERNE (score composite)
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.player_ranking AS
SELECT
    ROW_NUMBER() OVER (ORDER BY ranking_score DESC) AS rank,
    player_id,
    display_name,
    total_games,
    winrate_pct,
    kda_ratio,
    avg_dpm,
    avg_cs_per_min,
    avg_vision,
    ROUND(ranking_score::numeric, 2) AS score
FROM (
    SELECT
        dp.player_id,
        dp.summoner_name || '#' || dp.tag_line AS display_name,
        COUNT(*) AS total_games,
        ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_pct,
        ROUND(AVG((fpm.kills + fpm.assists)::float / NULLIF(fpm.deaths, 0))::numeric, 2) AS kda_ratio,
        ROUND(AVG(fpm.damage_per_min)::numeric, 0) AS avg_dpm,
        ROUND(AVG(fpm.cs_per_min)::numeric, 1) AS avg_cs_per_min,
        ROUND(AVG(fpm.vision_score)::numeric, 1) AS avg_vision,

        -- Score composite (pondere)
        (
            (100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*)) * 0.35 +
            LEAST(AVG((fpm.kills + fpm.assists) / NULLIF(fpm.deaths, 0)) * 10, 50) * 0.25 +
            (AVG(fpm.damage_per_min) / 10) * 0.20 +
            (AVG(fpm.cs_per_min) * 5) * 0.15 +
            (AVG(fpm.vision_score) * 2) * 0.05
        ) AS ranking_score
    FROM riot_fact.fact_player_match fpm
    JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
    GROUP BY dp.player_id, dp.summoner_name, dp.tag_line
    HAVING COUNT(*) >= 5
) ranked
ORDER BY ranking_score DESC;

-- ============================================================
-- VUE 5 : STATS PAR ROLE
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.player_stats_by_role AS
SELECT
    dp.player_id,
    dp.summoner_name || '#' || dp.tag_line AS display_name,
    fpm.position AS role,

    COUNT(*) AS games_played,
    SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) AS wins,
    ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_pct,

    ROUND(AVG((fpm.kills + fpm.assists)::float / NULLIF(fpm.deaths, 0))::numeric, 2) AS avg_kda,
    ROUND(AVG(fpm.cs_per_min)::numeric, 1) AS avg_cs_per_min,
    ROUND(AVG(fpm.damage_per_min)::numeric, 0) AS avg_dpm
FROM riot_fact.fact_player_match fpm
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
WHERE fpm.position != ''
GROUP BY dp.player_id, dp.summoner_name, dp.tag_line, fpm.position
ORDER BY dp.player_id, games_played DESC;

-- ============================================================
-- VUE 6 : ITEMS POPULAIRES
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.popular_items AS
SELECT
    unnested_item AS item_id,
    COALESCE(di.item_name, 'Unknown Item') AS item_name,
    COUNT(*) AS times_bought,
    ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_with_item
FROM riot_fact.fact_player_match fpm
CROSS JOIN LATERAL unnest(fpm.items) AS unnested_item
LEFT JOIN riot_dim.dim_item di ON unnested_item = di.item_id
WHERE unnested_item > 0
GROUP BY unnested_item, di.item_name
HAVING COUNT(*) >= 3
ORDER BY times_bought DESC
LIMIT 50;

-- ============================================================
-- VUE 7 : HISTORIQUE RECENT (derniers matchs)
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.recent_matches AS
SELECT
    mg.match_id,
    mg.game_start,
    mg.game_duration,
    dp.summoner_name || '#' || dp.tag_line AS player_name,
    COALESCE(dc.champion_name, 'Unknown') AS champion,
    fpm.win,
    fpm.kills,
    fpm.deaths,
    fpm.assists,
    ROUND(((fpm.kills + fpm.assists)::float / NULLIF(fpm.deaths, 0))::numeric, 2) AS kda,
    fpm.position AS role
FROM riot_fact.fact_player_match fpm
JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
LEFT JOIN riot_dim.dim_champion dc ON fpm.champion_id = dc.champion_id
ORDER BY mg.game_start DESC;
