# API FastAPI

**URL Production** : `https://lol-data-api.onrender.com`

## Endpoints

| Route | Méthode | Description |
|-------|---------|-------------|
| `/health` | GET | Healthcheck |
| `/health/db` | GET | Test connexion DB (diagnostic) |
| `/players` | GET | Liste tous les joueurs |
| `/players/{id}` | GET | Detail d'un joueur |
| `/players/{id}/champions` | GET | Champions du joueur |
| `/players/{id}/roles` | GET | Roles du joueur |
| `/players/{id}/items` | GET | Items du joueur (param: `limit`) |
| `/players/{id}/champions/{champ_id}/items` | GET | Items par champion (NEW) |
| `/players/{id}/builds` | GET | Top item par champion (NEW) |
| `/ranking` | GET | Classement performance (score composite) |
| `/ranking/ranked` | GET | Classement SoloQ (rangs officiels Riot) |
| `/duoq` | GET | Stats duo |
| `/stats/global` | GET | Stats globales |
| `/items/popular` | GET | Items populaires (param: `limit`) |
| `/update` | POST | Declenche mise a jour donnees |
| `/update/status` | GET | Statut de mise a jour |

## Conventions

- Réponses basées sur vues SQL (riot_analytics)
- Pas de logique métier lourde côté API
- Services = couche intermédiaire obligatoire
- Rate limit 0.5s entre appels Riot API

## Endpoint `/ranking/ranked`

Cet endpoint appelle l'API Riot en temps réel pour récupérer les rangs SoloQ.

**Response:**
```json
[
  {
    "position": 1,
    "player_id": 1,
    "display_name": "Nawfou",
    "tier": "PLATINUM",
    "rank": "III",
    "lp": 55,
    "wins": 22,
    "losses": 24,
    "winrate": 47.8,
    "score": 1855
  }
]
```

**Note:** Le score est calculé comme suit :
- `score = tier_value * 400 + rank_value * 100 + lp`
- Permet un tri précis des joueurs
