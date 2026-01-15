# Pièges Connus

## Python imports
Toujours ajouter :
sys.path.insert(0, project_root)

## SQL
ROUND() nécessite ::numeric

## Auto-update
run_update() doit reset flag avec try/finally
sinon update bloqué

## Encoding
Summoner names UTF-8 (Windows logs sensibles)

## Données manquantes
Joueur sans match = normal si hors filtre date/patch
