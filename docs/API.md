# API FastAPI

## Endpoints existants
- POST /update
- GET /update/status
- GET /players
- GET /players/{id}
- GET /duoq
- GET /ranking

## Endpoints Items (à implémenter)
- GET /items/popular?limit=20
- GET /players/{id}/items
- GET /players/{id}/champions/{cid}/items (futur)

## Conventions
- Réponses basées sur vues SQL
- Pas de logique métier lourde côté API
