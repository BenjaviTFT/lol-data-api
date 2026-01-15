# Base de Donnees

## Schemas
- riot_dim : players, champions, items
- riot_fact : match_game, fact_player_match
- riot_analytics : vues analytics (9 vues)

## Vues Analytics
1. player_stats - Stats agregees par joueur
2. player_champions - Stats par champion par joueur
3. player_stats_by_role - Stats par role
4. player_ranking - Classement performance interne
5. duoq_synergies - Synergies DuoQ
6. popular_items - Items populaires globaux
7. recent_matches - Historique matchs
8. player_items - Items par joueur
9. player_champion_items - Items par champion par joueur (NEW)

## Items
- Colonne : items INT[]
- 7 slots (0-6)
- item_id = 0 = slot vide

## Filtres globaux (dans les vues)
WHERE patch_version LIKE '16.1%'
AND game_start >= '2026-01-08'

## Regles SQL importantes
- Toujours caster avant ROUND :
  ROUND(AVG(x)::numeric, 1)
- Si schema vue modifie :
  DROP VIEW ... CASCADE puis recreer
- DISTINCT ON pour PostgreSQL (top N par groupe)
