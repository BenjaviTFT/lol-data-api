# Pieges Connus

## Deploiement Render/Supabase

### StaticFiles ecrase les routes API
**Probleme** : `app.mount("/", StaticFiles(...))` capture toutes les requetes.
**Solution** : Monter sur `/css`, `/js` et servir HTML via `FileResponse`.

### Port Supabase
**Probleme** : Port 5432 direct souvent bloque depuis Render.
**Solution** : Utiliser le pooler Supabase (port **6543**).

### RIOT_API_KEY manquante
**Probleme** : `riot_api.py` crashait a l'import sans la cle.
**Solution** : Warning au lieu de RuntimeError, API demarre sans la cle.

### Frontend API_BASE_URL
**Probleme** : `http://127.0.0.1:8000` ne marche pas en prod.
**Solution** : `API_BASE_URL = ''` (URL relative, meme origine).

## Python imports
Toujours ajouter :
```python
sys.path.insert(0, project_root)
```

## SQL
ROUND() necessite `::numeric` en PostgreSQL.

## Auto-update
`run_update()` doit reset flag avec try/finally sinon update bloque.

## Encoding
Summoner names UTF-8 (Windows logs sensibles).

## Donnees manquantes
Joueur sans match = normal si hors filtre date/patch.

## API Riot - League v4
Pour recuperer les rangs, utiliser directement `League v4 by-puuid` :
```
GET https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}
```

## Joueurs UNRANKED
Un joueur apparait UNRANKED si :
- Pas de parties ranked cette saison
- PUUID invalide ou region incorrecte
- Erreur API Riot (rate limit, cle expiree)
- RIOT_API_KEY non configuree sur Render
