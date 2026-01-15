# Exemples d'utilisation de l'API

## Démarrage

```bash
python run_api.py
```

L'API sera accessible sur : http://127.0.0.1:8000

---

## Exemples avec cURL

### 1. Health check
```bash
curl http://127.0.0.1:8000/health
```

**Réponse :**
```json
{"status": "healthy"}
```

---

### 2. Liste des joueurs
```bash
curl http://127.0.0.1:8000/players
```

**Réponse :**
```json
[
  {
    "player_id": 1,
    "display_name": "Nawfou#EUW",
    "total_games": 24,
    "winrate_pct": 54.2,
    "kda_ratio": 4.53,
    "avg_kills": 8.0,
    "avg_deaths": 5.9,
    "avg_assists": 7.6
  }
]
```

---

### 3. Ranking
```bash
curl http://127.0.0.1:8000/ranking
```

**Réponse :**
```json
[
  {
    "rank": 1,
    "display_name": "Reaper#491",
    "score": 59.07,
    "winrate_pct": 65.0,
    "kda_ratio": 3.52
  }
]
```

---

### 4. Champions d'un joueur
```bash
curl http://127.0.0.1:8000/players/1/champions
```

**Réponse :**
```json
[
  {
    "champion_id": 245,
    "champion_name": "Ekko",
    "games_played": 13,
    "winrate_pct": 53.8,
    "avg_kda": 4.2
  }
]
```

---

### 5. DuoQ synergies
```bash
curl http://127.0.0.1:8000/duoq
```

**Réponse :**
```json
[
  {
    "player_1_name": "Nawfou#EUW",
    "player_2_name": "Shoré#EUW",
    "games_together": 4,
    "winrate_pct": 75.0,
    "p1_avg_kda": 5.2,
    "p2_avg_kda": 4.8
  }
]
```

---

### 6. Derniers matchs
```bash
curl http://127.0.0.1:8000/matches/recent?limit=5
```

**Réponse :**
```json
[
  {
    "match_id": "EUW1_7684993070",
    "game_start": "2024-01-14T15:30:00",
    "player_name": "Reaper#491",
    "champion": "K'Sante",
    "win": true,
    "kills": 5,
    "deaths": 5,
    "assists": 10,
    "kda": 3.0,
    "role": "TOP"
  }
]
```

---

### 7. Stats globales
```bash
curl http://127.0.0.1:8000/stats/global
```

**Réponse :**
```json
{
  "total_players": 6,
  "total_games": 124,
  "total_wins": 67,
  "total_losses": 57,
  "avg_winrate": 54.0,
  "avg_kda": 3.39
}
```

---

## Exemples avec Python requests

### Installation
```bash
pip install requests
```

### Code
```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Get all players
response = requests.get(f"{BASE_URL}/players")
players = response.json()

for player in players:
    print(f"{player['display_name']}: {player['winrate_pct']}% WR")

# 2. Get ranking
response = requests.get(f"{BASE_URL}/ranking")
ranking = response.json()

print("\n🏆 RANKING INTERNE")
for p in ranking[:3]:
    print(f"#{p['rank']} {p['display_name']}: {p['score']} pts")

# 3. Get DuoQ synergies
response = requests.get(f"{BASE_URL}/duoq")
duos = response.json()

print("\n🤝 MEILLEURES SYNERGIES")
for duo in duos[:3]:
    print(f"{duo['player_1_name']} + {duo['player_2_name']}: {duo['winrate_pct']}% WR")
```

---

## Exemples avec JavaScript (fetch)

```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Get players
fetch(`${BASE_URL}/players`)
  .then(res => res.json())
  .then(players => {
    console.log("Joueurs:", players.length);
    players.forEach(p => {
      console.log(`${p.display_name}: ${p.winrate_pct}% WR`);
    });
  });

// Get ranking
fetch(`${BASE_URL}/ranking`)
  .then(res => res.json())
  .then(ranking => {
    console.log("\nTop 3:");
    ranking.slice(0, 3).forEach(p => {
      console.log(`#${p.rank} ${p.display_name}: ${p.score} pts`);
    });
  });
```

---

## Documentation interactive Swagger

Accède à http://127.0.0.1:8000/docs pour :
- Voir tous les endpoints
- Tester les requêtes directement
- Voir les schémas de réponse
- Générer du code client

---

## Codes HTTP

| Code | Signification |
|------|---------------|
| 200 | Succès |
| 404 | Joueur non trouvé |
| 422 | Paramètres invalides |
| 500 | Erreur serveur |

---

## CORS

Par défaut, CORS est ouvert (`allow_origins=["*"]`).

Pour production, restreindre dans `api/main.py` :

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ton-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Rate Limiting

⚠️ **Non implémenté** pour l'instant.

Pour ajouter :
```bash
pip install slowapi
```

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/players")
@limiter.limit("10/minute")
def get_players():
    ...
```
