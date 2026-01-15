-- ============================================================
-- VUE : ITEMS PAR JOUEUR (filtre patch 16.1 + date)
-- ============================================================

CREATE OR REPLACE VIEW riot_analytics.player_items AS
SELECT
    dp.player_id,
    dp.summoner_name AS display_name,
    unnested_item AS item_id,
    COALESCE(di.item_name, 'Unknown Item') AS item_name,
    COUNT(*) AS times_bought,
    ROUND(100.0 * SUM(CASE WHEN fpm.win THEN 1 ELSE 0 END) / COUNT(*), 1) AS winrate_with_item
FROM riot_fact.fact_player_match fpm
JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
CROSS JOIN LATERAL unnest(fpm.items) AS unnested_item
LEFT JOIN riot_dim.dim_item di ON unnested_item = di.item_id
WHERE unnested_item > 0
  AND mg.patch_version LIKE '16.1%'
  AND mg.game_start >= '2026-01-08 00:00:00'
GROUP BY dp.player_id, dp.summoner_name, unnested_item, di.item_name
HAVING COUNT(*) >= 1
ORDER BY dp.player_id, times_bought DESC;
