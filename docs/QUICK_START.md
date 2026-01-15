# Quick Start - Commandes Essentielles

## Démarrage du Site

```bash
# Terminal 1 : Backend API
python api/main.py

# Terminal 2 : Frontend
cd frontend
python -m http.server 8080
```

**Site accessible à :** http://localhost:8080

---

## Mise à Jour des Données

### Option 1 : Double-clic (Windows)
- Double-clic sur `update.bat`

### Option 2 : Ligne de commande
```bash
python scripts/update_matches.py
```

**Quoi :** Charge les 20 derniers matchs de chaque joueur
**Durée :** ~30 secondes
**Quand :** Après chaque session de jeu, 1x/jour

---

## Ajouter un Nouveau Joueur

### Option 1 : Double-clic (Windows)
- Double-clic sur `add_player.bat`

### Option 2 : Ligne de commande
```bash
python scripts/add_player.py
```

Ensuite, charge les matchs :
```bash
python ingest_all_players.py
```

---

## Vérifier l'État des Données

```bash
python scripts/check_data.py
```

Affiche :
- Total matchs en base
- Répartition par patch
- Stats par joueur

---

## Changement de Patch (ex: 16.1 → 16.2)

1. **Modifier le filtre SQL**
   - Ouvrir `db/create_analytics_views_patch_filtered.sql`
   - Remplacer `'16.1%'` par `'16.2%'` (7 occurrences)

2. **Appliquer le nouveau filtre**
   ```bash
   python scripts/apply_patch_filter.py
   ```

3. **Charger de nouveaux matchs**
   ```bash
   python ingest_all_players.py
   ```

---

## Résumé des Fichiers

| Fichier | Description |
|---------|-------------|
| `update.bat` | Mise à jour rapide (20 matchs/joueur) |
| `add_player.bat` | Ajouter un joueur interactivement |
| `ingest_all_players.py` | Charger 100 matchs par joueur (~6 min) |
| `scripts/update_matches.py` | Mise à jour incrémentale |
| `scripts/add_player.py` | Ajouter un joueur |
| `scripts/check_data.py` | Vérifier l'état des données |
| `scripts/apply_patch_filter.py` | Changer le filtre de patch |

---

## Améliorations Appliquées (Session Actuelle)

✅ **Filtre Patch 16.1** : Toutes les vues analytics ne montrent que les matchs 16.1+
✅ **100 matchs/joueur** : Augmenté de 20 à 100 matchs
✅ **Délai API réduit** : 1.2s → 0.5s (ingestion 2.4x plus rapide)
✅ **Mise à jour auto** : Script `update_matches.py` pour refresh quotidien
✅ **Ajout facile de joueurs** : Script interactif `add_player.py`
✅ **Vérification données** : Script `check_data.py` pour diagnostics

---

## État Actuel

**Matchs en base :** 114 (94 sur patch 16.1)
**Joueurs trackés :** 6
**Stats joueurs :** 124

**Vues filtrées :** ✅ Actives sur patch 16.1

---

## Dépannage Rapide

**Site inaccessible :**
```bash
netstat -ano | findstr ":8080"  # Vérifier si le frontend tourne
netstat -ano | findstr ":8000"  # Vérifier si le backend tourne
```

**Nouvelles stats invisibles :**
→ Vide le cache du navigateur (Ctrl+Shift+R)

**Erreur API Riot :**
→ Vérifie `config/.env` contient une clé API valide
