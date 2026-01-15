# ⚔️ League of Legends Analytics

> Plateforme complète d'analyse de performances pour un groupe privé de joueurs

**Status :** ✅ Production Ready | **Version :** 1.0.0

---

## 🚀 Démarrage Ultra-Rapide

**Voir :** [START_HERE.md](START_HERE.md) ⭐⭐⭐

```bash
# Terminal 1 - Backend
python run_api.py

# Terminal 2 - Frontend
cd frontend && python -m http.server 8080
```

**Accès :** http://localhost:8080

---

## 📊 Projet Complet

## Architecture

```
lol-data/
├── api/                      # API FastAPI
│   ├── main.py              # Application principale
│   ├── models.py            # Modèles Pydantic
│   └── database.py          # Requêtes SQL
├── db/                       # PostgreSQL
│   ├── postgres.py          # Connexion
│   └── create_analytics_views.sql
├── riot/                     # API Riot Games
│   ├── riot_api.py          # Appels API
│   ├── match_ingestion.py   # Ingestion données
│   └── load_data_dragon.py  # Référentiels statiques
├── config/
│   ├── .env                 # Clés API
│   └── players.py           # Liste des joueurs trackés
└── main.py                  # Script ingestion test
```

## Stack technique

- **Backend:** FastAPI + Uvicorn
- **Base de données:** PostgreSQL 15+
- **API externe:** Riot Games Match v5
- **Python:** 3.9+

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Créer `config/.env` :
```env
RIOT_API_KEY=RGAPI-xxxxx
POSTGRES_PASSWORD=xxxxx
```

## Utilisation

### 1. Ingestion des données

Charger les matchs de tous les joueurs :
```bash
python ingest_all_players.py
```

Mettre à jour un joueur spécifique :
```bash
python main.py
```

### 2. Lancer l'API

```bash
python run_api.py
```

L'API sera disponible sur : http://127.0.0.1:8000

Documentation Swagger : http://127.0.0.1:8000/docs

### 3. Endpoints disponibles

#### Players
- `GET /players` - Liste tous les joueurs
- `GET /players/{id}` - Stats d'un joueur
- `GET /players/{id}/champions` - Champions joués
- `GET /players/{id}/roles` - Stats par rôle

#### Ranking
- `GET /ranking` - Classement interne

#### DuoQ
- `GET /duoq` - Synergies entre joueurs

#### Matches
- `GET /matches/recent?limit=20` - Derniers matchs

#### Stats globales
- `GET /stats/global` - Stats du groupe
- `GET /health` - Health check

## Base de données

### Schémas

- `riot_dim` : Dimensions (joueurs, champions, items)
- `riot_fact` : Faits (matchs, stats joueurs)
- `riot_analytics` : Vues analytiques

### Vues principales

1. **player_stats** - Stats agrégées par joueur
2. **player_champions** - Pool de champions
3. **duoq_synergies** - Synergies DuoQ
4. **player_ranking** - Ranking interne (score composite)
5. **player_stats_by_role** - Performance par rôle
6. **recent_matches** - Historique récent

### Score de ranking

Formule pondérée :
- 35% Winrate
- 25% KDA (cappé à 5.0)
- 20% DPM (damage per minute)
- 15% CS/min
- 5% Vision score

Minimum 5 games pour être classé.

## Données trackées

### Par match
- K/D/A, Win/Loss
- CS/min, DPM, GPM
- Vision score
- Position/rôle
- Champion joué
- **Items (slots 0-6)**
- Durée de game

### Référentiels
- 166 champions (Data Dragon)
- 498 items (Data Dragon)

## Scripts utiles

```bash
# Vérifier les données
python check_data.py

# Tester les vues SQL
python test_views.py

# Tester l'API (sans la lancer)
python test_api.py

# Reset complet de la base
python reset_db.py
```

## Limites connues

- Historique limité aux ~100 derniers matchs par joueur (API Riot)
- Matchs très anciens peuvent être purgés par Riot
- Runes non disponibles (API Riot 2021+)
- Timeline détaillée nécessite un endpoint séparé (non implémenté)

## Roadmap

### Implémenté ✅
- [x] Ingestion matchs filtrés (joueurs trackés uniquement)
- [x] Items tracking
- [x] Vues analytiques SQL
- [x] API REST complète
- [x] Ranking interne
- [x] DuoQ analytics

### À venir
- [ ] Frontend React/Vue
- [ ] Champion mastery (API League v4)
- [ ] Items build analytics
- [ ] Achievements/badges
- [ ] Authentification JWT
- [ ] WebSockets (ranking live)

## Sécurité

⚠️ **Projet privé** - Accès limité au groupe défini dans `config/players.py`

Pour production :
1. Ajouter authentification JWT
2. Restreindre CORS
3. Variables d'environnement sécurisées
4. Rate limiting API

## Support

Projet maintenu par Benjamin Ferreira
