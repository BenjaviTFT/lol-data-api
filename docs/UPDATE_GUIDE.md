# Guide de Mise à Jour et Gestion des Données

Ce guide explique comment gérer les données du projet : mise à jour automatique, filtrage par patch, et ajout de nouveaux joueurs.

---

## 1. Filtre Patch 16.1

### Pourquoi ?
Les données sont maintenant filtrées pour ne montrer **que les matchs du patch 16.1**, pour des stats pertinentes sur la version actuelle du jeu.

### Appliquer le filtre

Exécute ce fichier SQL pour mettre à jour toutes les vues analytics :

```bash
psql -U postgres -d riot_db -f db/create_analytics_views_patch_filtered.sql
```

Ou via pgAdmin :
1. Ouvre `db/create_analytics_views_patch_filtered.sql`
2. Copie-colle le contenu dans une Query Tool
3. Exécute (F5)

**Résultat :** Toutes les vues (ranking, stats, DuoQ, etc.) ne montrent que les matchs patch 16.1+

---

## 2. Mise à Jour Incrémentale (Auto-refresh)

### Script de mise à jour automatique

Le script `scripts/update_matches.py` vérifie les **20 derniers matchs de chaque joueur** et ajoute uniquement les nouveaux.

```bash
cd c:\Users\Benjamin Ferreira\OneDrive\Bureau\DATA ANALYST\lol-data
python scripts/update_matches.py
```

**Ce qu'il fait :**
- Charge tous les match_ids déjà en base
- Pour chaque joueur, vérifie les 20 derniers matchs
- N'insère que les matchs **non présents** en base
- Rapide : environ 30 secondes pour 7 joueurs

**Utilisation recommandée :**
- Après chaque session de jeu de tes collègues
- 1 fois par jour pour rester à jour
- Avant d'accéder au site pour voir les nouvelles stats

### Automatiser avec une tâche planifiée (optionnel)

**Windows Task Scheduler :**
```bash
# Créer un fichier .bat
echo python "c:\Users\Benjamin Ferreira\OneDrive\Bureau\DATA ANALYST\lol-data\scripts\update_matches.py" > update_lol.bat

# Ajouter une tâche qui lance ce .bat toutes les heures
```

---

## 3. Ingestion Complète (après changement de patch)

### Configuration améliorée

Le fichier `ingest_all_players.py` a été optimisé :

- **MATCHS_PAR_JOUEUR** : passé de 20 à **100 matchs**
- **DELAY_API** : réduit de 1.2s à **0.5s** (Riot API supporte 20 req/s)

```python
MATCHS_PAR_JOUEUR = 100  # 100 matchs par joueur
DELAY_API = 0.5          # 0.5 seconde entre chaque appel
```

### Lancer l'ingestion complète

```bash
python ingest_all_players.py
```

**Temps estimé :**
- 100 matchs × 7 joueurs = ~700 appels API
- 700 × 0.5s = **~6 minutes** (vs 14 minutes avant)

**Quand l'utiliser :**
- Nouveau patch (ex: passage au 16.2)
- Ajout de plusieurs nouveaux joueurs
- Réinitialisation complète des données

---

## 4. Ajouter un Nouveau Joueur

### Méthode Simple : Script Interactif

```bash
python scripts/add_player.py
```

Le script te demande :
1. **Riot ID complet** : `NouveauJoueur#EUW`
2. **PUUID** : Le PUUID Riot du joueur

Le script ajoute automatiquement le joueur dans `config/players.py`.

### Méthode Ligne de Commande

```bash
python scripts/add_player.py "NouveauJoueur#EUW" "puuid_du_joueur_ici"
```

### Ensuite : Charger les matchs du nouveau joueur

```bash
python ingest_all_players.py
```

Cela chargera les 100 derniers matchs de **tous les joueurs**, y compris le nouveau.

---

## 5. Trouver le PUUID d'un Joueur

### Méthode 1 : Via l'API Riot (Python)

```python
from riot.riot_api import HEADERS
import requests

# Remplace par le nom du joueur
summoner_name = "PlayerName"
tag_line = "EUW"

url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}"
response = requests.get(url, headers=HEADERS)

if response.status_code == 200:
    data = response.json()
    print(f"PUUID: {data['puuid']}")
else:
    print("Joueur introuvable")
```

### Méthode 2 : Site externe

Utilise des sites comme :
- https://www.op.gg/
- https://u.gg/

Recherche le joueur, puis inspecte l'URL ou utilise l'API de ces sites.

---

## 6. Workflow Complet Recommandé

### Démarrage du projet

```bash
# 1. Lancer le backend API
python api/main.py

# 2. Dans un nouveau terminal, lancer le frontend
cd frontend
python -m http.server 8080
```

### Mise à jour quotidienne

```bash
# 1. Mettre à jour les matchs
python scripts/update_matches.py

# 2. Rafraîchir le site dans le navigateur
# http://localhost:8080
```

### Nouveau patch (ex: 16.2)

```bash
# 1. Modifier le filtre dans create_analytics_views_patch_filtered.sql
# Remplacer '16.1%' par '16.2%'

# 2. Re-créer les vues
psql -U postgres -d riot_db -f db/create_analytics_views_patch_filtered.sql

# 3. Ingérer de nouveaux matchs
python ingest_all_players.py
```

---

## 7. Dépannage

### Erreur : "RIOT_API_KEY non trouvée"
→ Vérifie que `config/.env` contient :
```
RIOT_API_KEY=RGAPI-xxxxx-xxxxx
```

### Erreur : "Rate limit exceeded (429)"
→ Augmente `DELAY_API` à 1.0 ou 1.5 dans les scripts

### Le site ne se rafraîchit pas
→ Vide le cache du navigateur (Ctrl+Shift+R sur Chrome)

### Les nouvelles stats n'apparaissent pas
→ Les vues SQL sont peut-être en cache. Re-créer les vues :
```bash
psql -U postgres -d riot_db -f db/create_analytics_views_patch_filtered.sql
```

---

## 8. Performances et Optimisation

### Stats actuelles
- **7 joueurs** trackés
- **~100 matchs** par joueur = 700 matchs
- **~1,400 player_match** records (2 joueurs trackés par match en moyenne)

### Limite API Riot
- **20 requêtes / seconde** (Rate Limit EUW)
- **100 requêtes / 2 minutes** (Burst)

Avec `DELAY_API = 0.5s`, on est à **2 req/s** = largement safe.

### Si tu as beaucoup de joueurs (20+)
- Utilise `DELAY_API = 0.3` (3 req/s)
- Lance l'ingestion la nuit ou en arrière-plan

---

## 9. Résumé des Commandes

| Action | Commande |
|--------|----------|
| Mise à jour incrémentale | `python scripts/update_matches.py` |
| Ingestion complète (100 matchs) | `python ingest_all_players.py` |
| Ajouter un joueur | `python scripts/add_player.py` |
| Appliquer filtre patch 16.1 | `psql -U postgres -d riot_db -f db/create_analytics_views_patch_filtered.sql` |
| Lancer backend API | `python api/main.py` |
| Lancer frontend | `cd frontend && python -m http.server 8080` |

---

**Tout est prêt !** 🚀

Tu peux maintenant :
- Filtrer par patch 16.1
- Mettre à jour automatiquement les données
- Ajouter des joueurs facilement
- Ingérer 100 matchs par joueur en ~6 minutes
