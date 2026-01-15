# Architecture Technique

## Pipeline Global
PostgreSQL → FastAPI → Vanilla JS

- Calculs analytiques effectués en base via vues SQL
- API = couche d’accès et d’orchestration
- Frontend = affichage uniquement

---

## Structure du Repository (FIGÉE)

lol-data/
├── main.py # point d’entrée principal
├── run_api.py # lancement FastAPI
├── api/
│ ├── main.py # routes uniquement
│ ├── database.py # accès DB (bas niveau)
│ ├── models.py # modèles Pydantic
│ └── services/ # logique métier
│ ├── player_service.py
│ ├── match_service.py
│ ├── duoq_service.py
│ ├── item_service.py
│ └── update_service.py
│
├── db/
│ ├── connection.py # connexion PostgreSQL
│ ├── schema/ # création tables
│ ├── views/ # vues analytiques (source de vérité)
│ └── migrations/ # scripts numérotés (000_, 001_...)
│
├── frontend/ # HTML / CSS / JS
├── riot/ # client API Riot
├── config/ # config & players
├── scripts/ # utilitaires
├── tests/ # tests Python
├── bin/ # scripts Windows
└── docs/ # documentation


⛔ Cette structure est considérée comme **stable**.  
Aucun refactor global n’est autorisé sans mise à jour de ce fichier.

---

## Architecture Backend (FastAPI)

### Séparation des responsabilités
- `api/main.py`  
  → **routes uniquement**, aucune logique métier
- `api/services/*_service.py`  
  → logique métier, accès DB indirect
- `api/database.py`  
  → helpers DB bas niveau (jamais appelé depuis les routes)

📌 **Règle stricte**  
Les routes appellent **uniquement** les services.

---

## Base de Données & SQL

### Organisation
- `db/schema/` : création tables
- `db/views/` : vues analytiques (riot_analytics)
- `db/migrations/` : évolutions incrémentales

### Règles SQL
- Les vues sont la **source de vérité analytique**
- Aucun calcul complexe côté API
- `ROUND()` nécessite toujours `::numeric`

---

## Auto-update

- Déclenché via `POST /update`
- Appelé au chargement frontend + refresh 10 min
- Rate limit interne : 0.5s (safe Riot)
- Gestion du flag via `UpdateService`
- `try/finally` obligatoire (pas de variable globale)

---

## Frontend

- Vanilla JS uniquement (pas de framework)
- Appels API centralisés dans `frontend/js/api.js`
- Configuration dans `frontend/js/config.js`
- Aucune logique métier côté frontend

---

## Assets & Images

Data Dragon CDN :
- Champions : `/img/champion/{key}.png`
- Items : `/img/item/{id}.png`

---

## Règles de Stabilité

- ❌ Pas de refactor structurel sans mise à jour de ce fichier
- ❌ Pas de logique métier dans les routes
- ❌ Pas de calcul analytique hors SQL
- ✅ Lisibilité > optimisation
