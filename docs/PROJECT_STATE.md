# PROJECT STATE – LoL Analytics

## Objectif
Analytics privé League of Legends pour 7 joueurs :
ranking interne, stats individuelles, synergies DuoQ, dashboard dark, auto-update.

## Stack
PostgreSQL 15 · Python 3.11 · FastAPI · Vanilla JS (no Node).

## Deploiement PRODUCTION ✅
- **URL** : `https://lol-data-api.onrender.com`
- **API** : Render (Web Service)
- **DB** : Supabase PostgreSQL (pooler port 6543)
- **Frontend** : Servi par FastAPI (meme origine)

## Donnees actives
- 574 matchs total (migres sur Supabase)
- 633 entries fact_player_match
- 7 joueurs
- Filtre actif : patch 16.1 + date >= 2026-01-08

## Fonctionnalites OK
- Dashboard global (stats, classements, items populaires)
- Classement SoloQ (rangs officiels Riot)
- Classement Performance (score composite)
- Profil joueur (stats, champions, roles, items)
- Comparateur 2 joueurs
- DuoQ Matrix + synergies
- Auto-update (10 min)

## Architecture
- Structure du projet **figee et validee**
- Separation stricte routes / services / DB
- Calculs analytiques exclusivement en SQL (vues)
- Frontend servi via FileResponse + StaticFiles

## Commits recents (deploiement)
- `9573f20` - Sync frontend files
- `0fa4719` - Fix API_BASE_URL relative
- `a80d8b4` - Serve frontend from API
- `858e881` - Fix riot_api.py import crash
- `85bd4f1` - Fix StaticFiles overriding routes

## Configuration requise (Render Environment)
- `DATABASE_URL` : URL Supabase pooler (port 6543)
- `RIOT_API_KEY` : Optionnel (pour /ranking/ranked live)

## Source de verite
- Vues SQL dans `riot_analytics` (8 vues)
- Filtres patch/date appliques dans les vues
- Tables dans `riot_dim` et `riot_fact`
