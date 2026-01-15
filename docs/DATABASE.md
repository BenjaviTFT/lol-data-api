# Base de Données

## Schémas
- riot_dim : players, champions, items
- riot_fact : match_game, fact_player_match
- riot_analytics : vues analytics (7)

## Items
- Colonne : items INT[]
- 7 slots (0–6)
- item_id = 0 → slot vide

## Filtres globaux (dans les vues)
WHERE patch_version LIKE '16.1%'
AND game_start >= '2026-01-08'

## Règles SQL importantes
- Toujours caster avant ROUND :
  ROUND(AVG(x)::numeric, 1)
- Si schéma vue modifié :
  DROP VIEW ... CASCADE puis recréer
