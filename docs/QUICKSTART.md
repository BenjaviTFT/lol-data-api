# 🚀 Guide de démarrage rapide

## 1️⃣ Vérification de l'installation

Tout est déjà installé et configuré. Vérifie que tout fonctionne :

```bash
python check_data.py
```

**Résultat attendu :**
- 114 matchs uniques
- 6 joueurs
- 124 stats individuelles
- Aucun doublon

---

## 2️⃣ Lancer l'API

### Option A : Script automatique (Windows)
```bash
start.bat
```

### Option B : Commande manuelle
```bash
python run_api.py
```

L'API sera accessible sur :
- **Base URL :** http://127.0.0.1:8000
- **Documentation Swagger :** http://127.0.0.1:8000/docs

---

## 3️⃣ Tester l'API

### Depuis un autre terminal

```bash
python test_api_live.py
```

Ou ouvre directement : http://127.0.0.1:8000/docs

---

## 4️⃣ Endpoints principaux

### Ranking interne
```
GET http://127.0.0.1:8000/ranking
```

### Liste des joueurs
```
GET http://127.0.0.1:8000/players
```

### Stats d'un joueur (ID = 1)
```
GET http://127.0.0.1:8000/players/1
```

### Champions d'un joueur
```
GET http://127.0.0.1:8000/players/1/champions
```

### DuoQ synergies
```
GET http://127.0.0.1:8000/duoq
```

### Derniers matchs
```
GET http://127.0.0.1:8000/matches/recent?limit=10
```

---

## 5️⃣ Mettre à jour les données

### Charger plus de matchs

Édite [ingest_all_players.py](ingest_all_players.py) :
```python
MATCHS_PAR_JOUEUR = 50  # Augmente à 50 ou 100
```

Puis lance :
```bash
python ingest_all_players.py
```

⏱️ **Durée estimée :** 5-10 minutes pour 50 matchs × 7 joueurs

---

## 6️⃣ Consulter les données SQL

### Directement dans pgAdmin

#### Ranking
```sql
SELECT * FROM riot_analytics.player_ranking;
```

#### Stats par joueur
```sql
SELECT * FROM riot_analytics.player_stats;
```

#### Champions joués
```sql
SELECT *
FROM riot_analytics.player_champions
WHERE player_id = 1
ORDER BY games_played DESC;
```

#### DuoQ
```sql
SELECT *
FROM riot_analytics.duoq_synergies
ORDER BY games_together DESC;
```

---

## 7️⃣ Structure du projet

```
lol-data/
│
├── api/                      # 🔌 API FastAPI
│   ├── main.py              # Application principale
│   ├── models.py            # Modèles Pydantic
│   └── database.py          # Queries SQL
│
├── db/                       # 🗄️ PostgreSQL
│   ├── postgres.py          # Connexion
│   └── create_analytics_views.sql
│
├── riot/                     # 🎮 API Riot
│   ├── riot_api.py          # Appels API
│   ├── match_ingestion.py   # Ingestion
│   └── load_data_dragon.py  # Référentiels
│
├── config/                   # ⚙️ Configuration
│   ├── .env                 # Clés API (ne pas partager)
│   └── players.py           # Liste des joueurs trackés
│
├── ingest_all_players.py    # 📥 Ingestion massive
├── run_api.py               # 🚀 Lancer l'API
├── check_data.py            # ✅ Vérifier les données
├── test_api.py              # 🧪 Tester l'API
│
└── Documentation/
    ├── README.md
    ├── IMPLEMENTATION_SUMMARY.md
    ├── API_EXAMPLES.md
    └── QUICKSTART.md (ce fichier)
```

---

## 8️⃣ Commandes utiles

### Données
```bash
python check_data.py          # Vérifier l'état de la base
python test_views.py          # Tester les vues SQL
python debug_db.py            # Debug complet
```

### API
```bash
python run_api.py             # Lancer l'API
python test_api.py            # Tester (API arrêtée)
python test_api_live.py       # Tester (API lancée)
```

### Ingestion
```bash
python main.py                # Test ingestion (1 joueur, 5 matchs)
python ingest_all_players.py  # Ingestion massive
```

### Reset
```bash
python reset_db.py            # ⚠️ Vider toute la base
```

---

## 9️⃣ Trouver l'ID d'un joueur

```bash
python -c "import sys; sys.path.insert(0, '.'); from db.connection import get_connection; conn = get_connection(); cur = conn.cursor(); cur.execute('SELECT player_id, summoner_name, tag_line FROM riot_dim.dim_player'); rows = cur.fetchall(); print('ID | Joueur'); print('-'*40); [print(f'{r[0]:2} | {r[1]}#{r[2]}') for r in rows]; cur.close(); conn.close()"
```

---

## 🔟 Prochaines étapes

### Frontend (Recommandé)
1. Créer un projet React/Vue
2. Consommer l'API (exemples dans [API_EXAMPLES.md](API_EXAMPLES.md))
3. Créer un dashboard avec :
   - Tableau du ranking
   - Profils joueurs
   - Graphiques (Chart.js)
   - Matrice DuoQ

### Backend avancé
- Authentification JWT
- WebSockets (ranking live)
- Champion mastery
- Items analytics détaillés

---

## ❓ Problèmes courants

### L'API ne démarre pas
```bash
# Vérifier que PostgreSQL est lancé
python -c "from db.connection import get_connection; get_connection()"
```

### Pas de données
```bash
# Relancer l'ingestion
python ingest_all_players.py
```

### Erreur 404 sur un endpoint
- Vérifie que l'API est bien lancée
- Vérifie l'URL complète : http://127.0.0.1:8000/players

---

## 📖 Documentation complète

- **[README.md](README.md)** - Vue d'ensemble du projet
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Détails techniques
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - Exemples de requêtes

---

**Projet opérationnel** ✅

Pour toute question, consulte [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
