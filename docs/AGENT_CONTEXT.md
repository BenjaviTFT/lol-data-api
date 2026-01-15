# LOL-DATA - CONTEXTE AGENT

## Etat actuel : PRODUCTION OK
URL : https://lol-data-api.onrender.com

## Stack
- Backend : FastAPI (Python 3.11) sur Render
- DB : Supabase PostgreSQL (pooler port 6543)
- Frontend : Vanilla JS servi par FastAPI (meme origine)

## Architecture
```
lol-data/
├── main.py              <- Entry point (importe api/main.py)
├── api/
│   ├── main.py          <- Routes FastAPI + StaticFiles
│   ├── models.py        <- Pydantic models
│   ├── database.py      <- execute_query()
│   └── services/        <- PlayerService, RankService, ItemService...
├── config/players.py    <- TRACKED_PLAYERS (8 joueurs, source de verite)
├── db/
│   ├── connection.py    <- get_connection() (auto local/prod)
│   └── views/           <- SQL des vues analytics (9 vues)
├── frontend/
│   ├── index.html       <- Dashboard
│   ├── player.html      <- Profil joueur
│   ├── css/styles.css   <- Styles globaux
│   └── js/              <- config.js, api.js, dashboard.js, player.js
├── riot/riot_api.py     <- Appels API Riot (ranks, matches)
└── docs/                <- Documentation
```

## DB Schemas
- riot_dim : dim_player, dim_champion, dim_item
- riot_fact : fact_player_match, match_game
- riot_analytics : 9 vues (player_stats, player_champions, player_items, etc.)

## Joueurs Tracked (8)
Nawfou, Nawlol, Reaper, Shore, FlaqueDepisse, Me no murderer, Viirtu, T1 KRKING
- Definis dans `config/players.py` (TRACKED_PLAYERS dict)
- Le ranking SoloQ (`/ranking/ranked`) utilise TRACKED_PLAYERS comme source
- Joueurs sans matchs apparaissent quand meme (ex: FlaqueDepisse)

## Endpoints principaux
- `/players` - Liste joueurs avec stats
- `/players/{id}/champions` - Champions du joueur
- `/players/{id}/champions/{champ}/items` - Items par champion (NEW)
- `/ranking/ranked` - Classement SoloQ (appel Riot API live)
- `/ranking` - Classement performance interne
- `/update` - Trigger mise a jour matchs

## Regles importantes
1. Vues SQL = source de verite (pas de calculs cote Python)
2. Filtre actif dans vues : patch 16.1 + date >= 2026-01-08
3. Ne pas modifier la structure du projet (figee)
4. TRACKED_PLAYERS = source pour listing joueurs (pas dim_player)
5. Rate limit 0.5s entre appels Riot API

## Fichiers cles a connaitre
- `api/services/rank_service.py` - Logique ranking SoloQ
- `api/services/player_service.py` - Stats joueurs
- `api/services/item_service.py` - Items et builds
- `frontend/js/dashboard.js` - Affichage dashboard
- `frontend/js/player.js` - Profil joueur (champions expandables)
- `frontend/css/styles.css` - Variables CSS, styles ranking

## Derniers changements (session actuelle)
1. RankService utilise TRACKED_PLAYERS (fix FlaqueDepisse)
2. Nouveau endpoint `/players/{id}/champions/{champ}/items`
3. Nouvelle vue SQL `player_champion_items`
4. CSS ranking SoloQ avec bordures colorees par tier
5. Champions table expandable avec items dans profil joueur

## Action requise post-session
Executer sur Supabase : `db/views/create_player_champion_items_view.sql`
