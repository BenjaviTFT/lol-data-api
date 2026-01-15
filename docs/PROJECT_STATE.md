# PROJECT STATE – LoL Analytics

## Objectif
Analytics privé League of Legends pour 7 joueurs :
ranking interne, stats individuelles, synergies DuoQ, dashboard dark, auto-update.

## Stack
PostgreSQL 15 · Python 3.11 · FastAPI · Vanilla JS (no Node).

## Deploiement
- **API** : Render (`https://lol-data-api.onrender.com`)
- **DB** : Supabase PostgreSQL
- **Connexion** : `DATABASE_URL` (auto-detection local/prod)

## Données actives
- 547 matchs total
- 176 filtrés (patch 16.1 + >= 2026-01-08)
- 6 joueurs visibles (1 sans match filtré)

## Fonctionnalités OK
- Dashboard global
- Profil joueur
- Comparateur
- DuoQ
- Auto-update (10 min)

## Architecture
- Structure du projet **figée et validée**
- Séparation stricte routes / services / DB
- Calculs analytiques exclusivement en SQL (vues)

## Tache en cours
Deploiement production - en attente de validation Render.

## Commits recents (deploiement)
- `95942d0` - Add PlayerRankedInfo model + RankService
- `de7a116` - Fix root main.py (logging, /health/db, /ranking/ranked)
- `c8f5876` - Support DATABASE_URL dans db/connection.py

## Refactor termine (3 phases)
1. **Phase 1** ✅ – Nettoyage racine (tests → `tests/`, scripts → `scripts/`, docs → `docs/`)
2. **Phase 2** ✅ – Structuration backend (`api/services/` avec services métier)
3. **Phase 3** ✅ – Organisation SQL (`db/schema/`, `db/views/`, `db/migrations/`)

## Prochaine action attendue
1. **Valider deploiement Render** - tester `/health/db` puis `/players`
2. Si erreur DB → verifier schema `riot_analytics` sur Supabase
3. Ensuite : UI items (dashboard + profil)

## Source de vérité
- Vues SQL dans `riot_analytics`
- Filtres patch/date appliqués dans les vues
- Architecture décrite dans `docs/ARCHITECTURE.md`
