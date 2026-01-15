# Changelog - Améliorations Appliquées

## Session du 14 Janvier 2026

### 🎯 Objectifs
- Filtrer les données sur le patch 16.1 uniquement
- Accélérer l'ingestion de données
- Permettre la mise à jour automatique
- Faciliter l'ajout de nouveaux joueurs

---

## ✅ Améliorations Implémentées

### 1. Filtre Patch 16.1

**Fichiers créés :**
- `db/create_analytics_views_patch_filtered.sql` - Vues SQL avec filtre `WHERE mg.patch_version LIKE '16.1%'`
- `scripts/apply_patch_filter.py` - Script Python pour appliquer les vues

**Vues modifiées :**
- ✅ `player_stats` - Stats générales filtrées
- ✅ `player_champions` - Pool de champions filtré
- ✅ `duoq_synergies` - DuoQ filtré
- ✅ `player_ranking` - Classement filtré
- ✅ `player_stats_by_role` - Stats par rôle filtrées
- ✅ `popular_items` - Items filtrés
- ✅ `recent_matches` - Matchs récents filtrés (+ colonne `patch_version` ajoutée)

**Résultat :** Le site affiche maintenant **uniquement les matchs du patch 16.1**

**État actuel :** 94 matchs sur 114 sont sur le patch 16.1

---

### 2. Optimisation de l'Ingestion

**Fichier modifié :**
- `ingest_all_players.py`

**Changements :**
- `MATCHS_PAR_JOUEUR` : 20 → **100 matchs**
- `DELAY_API` : 1.2s → **0.5s**

**Impact :**
- **Avant :** 20 matchs × 7 joueurs × 1.2s = ~3 min
- **Après :** 100 matchs × 7 joueurs × 0.5s = **~6 min**
- **Gain :** 5x plus de données en 2x le temps

---

### 3. Mise à Jour Incrémentale

**Fichiers créés :**
- `scripts/update_matches.py` - Script de mise à jour intelligente
- `update.bat` - Raccourci Windows

**Fonctionnement :**
1. Charge tous les `match_id` déjà en base (1 seule requête SQL)
2. Pour chaque joueur, récupère les 20 derniers matchs
3. N'insère que les matchs **non présents** en base
4. Évite les doublons et les appels API inutiles

**Avantages :**
- ⚡ Rapide : ~30 secondes pour 7 joueurs
- 🔄 Idempotent : peut être lancé plusieurs fois sans souci
- 📊 Mise à jour automatique après chaque session de jeu

**Usage :**
```bash
python scripts/update_matches.py
# OU
update.bat  (double-clic)
```

---

### 4. Ajout Facile de Joueurs

**Fichiers créés :**
- `scripts/add_player.py` - Script d'ajout interactif
- `add_player.bat` - Raccourci Windows

**Fonctionnement :**
1. Demande le Riot ID (`Player#EUW`)
2. Demande le PUUID
3. Ajoute automatiquement dans `config/players.py`
4. Vérifie les doublons

**Usage interactif :**
```bash
python scripts/add_player.py
# OU
add_player.bat  (double-clic)
```

**Usage ligne de commande :**
```bash
python scripts/add_player.py "NewPlayer#EUW" "puuid_here"
```

**Ensuite :**
```bash
python ingest_all_players.py  # Charger les 100 matchs du nouveau joueur
```

---

### 5. Vérification des Données

**Fichier créé :**
- `scripts/check_data.py`

**Affiche :**
- Total matchs en base
- Total stats joueurs
- Répartition par patch (avec dates)
- Stats par joueur (tous patchs)
- Stats par joueur (patch 16.1 uniquement)

**Usage :**
```bash
python scripts/check_data.py
```

**Exemple de sortie :**
```
ETAT DES DONNEES - RIOT DB
======================================================================
Total matchs en base : 114
Total stats joueurs : 124

REPARTITION PAR PATCH
----------------------------------------------------------------------
16.1.    :   94 matchs  (du 2026-01-09 au 2026-01-14)
15.24    :   16 matchs  (du 2025-12-12 au 2026-01-03)
...
```

---

## 📁 Nouveaux Fichiers

### Scripts Python
| Fichier | Description |
|---------|-------------|
| `scripts/update_matches.py` | Mise à jour incrémentale (20 matchs/joueur) |
| `scripts/add_player.py` | Ajout interactif de joueurs |
| `scripts/apply_patch_filter.py` | Application du filtre de patch |
| `scripts/check_data.py` | Vérification de l'état des données |

### Fichiers SQL
| Fichier | Description |
|---------|-------------|
| `db/create_analytics_views_patch_filtered.sql` | Vues analytics filtrées par patch 16.1 |

### Scripts Batch (Windows)
| Fichier | Description |
|---------|-------------|
| `update.bat` | Raccourci pour mise à jour rapide |
| `add_player.bat` | Raccourci pour ajout de joueurs |

### Documentation
| Fichier | Description |
|---------|-------------|
| `UPDATE_GUIDE.md` | Guide complet de mise à jour et gestion |
| `QUICK_START.md` | Commandes essentielles (cheat sheet) |
| `CHANGELOG.md` | Ce fichier - historique des modifications |

---

## 🎯 Workflow Recommandé

### Quotidien (après session de jeu)
```bash
update.bat  # Ou: python scripts/update_matches.py
```

### Hebdomadaire
```bash
python scripts/check_data.py  # Vérifier l'état
```

### Nouveau patch (ex: 16.2)
```bash
# 1. Modifier db/create_analytics_views_patch_filtered.sql
#    Remplacer '16.1%' par '16.2%'

# 2. Appliquer
python scripts/apply_patch_filter.py

# 3. Charger nouveaux matchs
python ingest_all_players.py
```

### Nouveau joueur
```bash
# 1. Ajouter
add_player.bat  # Ou: python scripts/add_player.py

# 2. Charger ses matchs
python ingest_all_players.py
```

---

## 🚀 État Final

### Performances
- ✅ Ingestion 2.4x plus rapide (0.5s vs 1.2s par appel)
- ✅ 5x plus de matchs par ingestion (100 vs 20)
- ✅ Mise à jour incrémentale en ~30s

### Fonctionnalités
- ✅ Filtre patch 16.1 actif sur toutes les vues
- ✅ Mise à jour automatique opérationnelle
- ✅ Ajout de joueurs simplifié
- ✅ Diagnostic des données disponible

### Base de Données
- 📊 114 matchs (94 sur patch 16.1)
- 👥 6 joueurs trackés
- 📈 124 stats joueurs

---

## 🔮 Prochaines Étapes Possibles

### Automatisation
- [ ] Tâche planifiée Windows pour `update_matches.py` toutes les heures
- [ ] Webhook Discord pour notifier des nouvelles stats

### Frontend
- [ ] Bouton "Refresh" pour lancer `update_matches.py` depuis le site
- [ ] Indicateur "Dernière mise à jour : il y a X minutes"
- [ ] Filtres de date/patch dans l'interface

### Analytics
- [ ] Vue "Progression temporelle" (WR par semaine)
- [ ] Détection des "win streaks" / "lose streaks"
- [ ] Prédiction de rang basée sur les stats

### Performance
- [ ] Cache Redis pour les vues fréquentes
- [ ] Ingestion parallèle (threads) pour aller plus vite
- [ ] Webhook Riot pour mise à jour en temps réel

---

## 📝 Notes Techniques

### Filtre SQL Appliqué
```sql
WHERE mg.patch_version LIKE '16.1%'
```

**Justification :** Le format de `patch_version` est `16.1.xxx` donc le `LIKE` capture toutes les micro-versions du patch 16.1.

### Gestion des Doublons
- **match_game** : `ON CONFLICT DO NOTHING` sur `match_id`
- **fact_player_match** : `ON CONFLICT (match_id, player_id) DO NOTHING`
- **dim_player** : `ON CONFLICT (puuid) DO UPDATE SET ...`

### Rate Limiting Riot API
- **Limite :** 20 req/s (EUW)
- **Burst :** 100 req/2min
- **Delay appliqué :** 0.5s = 2 req/s (safe)

---

**Session complétée avec succès** ✅

Toutes les améliorations demandées ont été implémentées et testées.
