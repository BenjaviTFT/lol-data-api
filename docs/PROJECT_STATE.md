# PROJECT STATE – LoL Analytics

## Objectif
Analytics privé League of Legends pour 7 joueurs :
ranking interne, stats individuelles, synergies DuoQ, dashboard dark, auto-update.

## Stack
PostgreSQL 15 · Python 3.9 · FastAPI · Vanilla JS (no Node).

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

## Tâche en cours
Ajout des **items (frontend + API)**.

## Refactor terminé (3 phases)
1. **Phase 1** ✅ – Nettoyage racine (tests → `tests/`, scripts → `scripts/`, docs → `docs/`)
2. **Phase 2** ✅ – Structuration backend (`api/services/` avec services métier)
3. **Phase 3** ✅ – Organisation SQL (`db/schema/`, `db/views/`, `db/migrations/`)

## Prochaine action attendue
Implémenter UI items :
- Section items populaires (dashboard)
- Items par joueur (page profil)

## Source de vérité
- Vues SQL dans `riot_analytics`
- Filtres patch/date appliqués dans les vues
- Architecture décrite dans `docs/ARCHITECTURE.md`
