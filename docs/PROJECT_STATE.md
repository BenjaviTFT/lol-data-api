# PROJECT STATE - LoL Analytics

## Objectif
Analytics prive League of Legends pour 8 joueurs :
ranking interne, stats individuelles, synergies DuoQ, dashboard dark, auto-update.

## Stack
PostgreSQL 15 - Python 3.11 - FastAPI - Vanilla JS (no Node).

## Deploiement PRODUCTION
- **URL** : `https://lol-data-api.onrender.com`
- **API** : Render (Web Service)
- **DB** : Supabase PostgreSQL (pooler port 6543)
- **Frontend** : Servi par FastAPI (meme origine)

## Joueurs Tracked (8)
Nawfou, Nawlol, Reaper, Shore, FlaqueDepisse, Me no murderer, Viirtu, T1 KRKING
- Config : `config/players.py` (TRACKED_PLAYERS)
- Ranking SoloQ utilise TRACKED_PLAYERS comme source (pas dim_player)

## Donnees actives
- ~600+ matchs (Supabase)
- 8 joueurs tracked
- Filtre actif : patch 16.1 + date >= 2026-01-08

## Fonctionnalites OK
- Dashboard global (stats, classements, items populaires)
- Classement SoloQ (rangs officiels Riot) - affiche TOUS les joueurs tracked
- Classement Performance (score composite)
- Profil joueur (stats, champions expandables avec items, roles, items)
- Comparateur 2 joueurs
- DuoQ Matrix + synergies
- Auto-update (10 min)

## Architecture
- Structure du projet **figee et validee**
- Separation stricte routes / services / DB
- Calculs analytiques exclusivement en SQL (vues)
- Frontend servi via FileResponse + StaticFiles

## Vues SQL (9 total)
- player_stats, player_champions, player_stats_by_role
- player_ranking, duoq_synergies, popular_items
- recent_matches, player_items, player_champion_items (NEW)

## Configuration requise (Render Environment)
- `DATABASE_URL` : URL Supabase pooler (port 6543)
- `RIOT_API_KEY` : Requis pour /ranking/ranked

## Source de verite
- Vues SQL dans `riot_analytics`
- Filtres patch/date appliques dans les vues
- Tables dans `riot_dim` et `riot_fact`
- TRACKED_PLAYERS pour liste joueurs (pas DB)
