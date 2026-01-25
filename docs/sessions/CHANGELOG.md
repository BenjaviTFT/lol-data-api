# CHANGELOG - LoL Analytics

Historique des modifications du projet. Chaque session de développement est documentée ici.

---

## [V1.0.0] - 2026-01-25 - VERSION STABLE - VPS READY

### Milestone
**Codebase figée pour déploiement VPS Hostinger.**
Cette version consolide l'ensemble des fonctionnalités développées pour la V1 :
- Tracking 10 joueurs (Patch 16.x)
- Dashboard Ranking + Live Games
- Profils détaillés avec Stats avancées (@12/@20, Synergies)
- Vue DuoQ optimisée
- Architecture stable (PostgreSQL + FastAPI + Vanilla JS)

### Actions
- Nettoyage final du code
- Tag git `v1.0.0` créé
- Documentation à jour (`PROJECT_STATE.md`, `ARCHITECTURE.md`)

---

## [2026-01-25] - Fix DuoQ Partenaires page joueur

### Probleme
La section "DuoQ Partenaires" sur les pages joueurs affichait "Donnees non disponibles" au lieu des partenaires de duo.

### Causes racines
1. **Modele Pydantic trop strict** : Les champs `p1_avg_kda` et `p2_avg_kda` dans `DuoQSynergy` etaient declares comme `float` obligatoire, mais la vue SQL retourne `NULL` quand un joueur a 0 deaths (division par zero evitee avec `NULLIF`).
2. **Filtre `is_tracked` manquant** : La vue SQL `duoq_synergies` ne filtrait pas par `is_tracked = TRUE`, affichant des joueurs non suivis.

### Solution

**1. Correction modele Pydantic (`api/models.py`)**
```python
# Avant
p1_avg_kda: float
p2_avg_kda: float

# Apres
p1_avg_kda: Optional[float] = None
p2_avg_kda: Optional[float] = None
```

**2. Ajout filtre dans la vue SQL (`db/views/create_analytics_views_patch_filtered.sql`)**
```sql
WHERE mg.patch_version LIKE '16.%'
  AND mg.game_start >= '2026-01-08 00:00:00'
  AND p1.is_tracked = TRUE   -- AJOUTE
  AND p2.is_tracked = TRUE   -- AJOUTE
```

### Fichiers modifies
- `api/models.py` : Champs KDA rendus optionnels
- `db/views/create_analytics_views_patch_filtered.sql` : Filtre is_tracked ajoute

### Documentation mise a jour
- `docs/PROJECT_STATE.md` : Liste joueurs corrigee (Bardella2027 au lieu de FlaqueDepisse)

---

## [2026-01-25] - Refonte Tracking LP et Table Historique

### Suppression du systeme d'estimation LP

#### Probleme identifie
Le script `backfill_lp.py` ecrivait des valeurs estimees (+/-20 LP par victoire/defaite) dans la colonne `lp_after_game`. Ces estimations faussaient :
- Le calcul du gain/perte LP journalier
- Les graphiques d'evolution
- Les statistiques de progression

#### Solution implementee

**1. Suppression du script `backfill_lp.py`**
- Le script a ete supprime car il corrompait les donnees reelles

**2. Nouvelle table `lp_history`**
- **Migration** : `db/migrations/create_lp_history_table.sql`
- **Colonnes** : `player_id`, `captured_at`, `tier`, `division`, `lp`, `rank_score`, `source`
- **Score numerique** : Iron IV 0LP = 0 ... Challenger 1000LP = 3800
- **Vues associees** :
  - `riot_analytics.player_lp_current` : Dernier LP de chaque joueur
  - `riot_analytics.player_lp_daily` : Evolution quotidienne (min/max/delta par jour)

**3. Enregistrement automatique des LPs**
- **Fonction** : `RankService.record_lp_snapshot()` dans `api/services/rank_service.py`
- **Integration** : Appelee automatiquement a chaque cycle d'auto-update (60s)
- **Rate limiting** : 0.3s entre chaque appel API pour eviter les 429

**4. Affichage LP corrige**
- La vue SQL `recent_matches` utilise `LAG(lp_after_game)` pour calculer la difference
- Si le LP precedent est NULL, `lp_change` = NULL, pas d'affichage (au lieu d'une estimation)

### Fichiers modifies

| Fichier | Modification |
|---------|--------------|
| `scripts/backfill_lp.py` | **SUPPRIME** |
| `api/services/rank_service.py` | Ajout `record_lp_snapshot()` |
| `api/services/update_service.py` | Integration enregistrement LP |
| `db/migrations/create_lp_history_table.sql` | **NOUVEAU** |
| `docs/KNOWN_PITFALLS.md` | Mise a jour section LP |
| `docs/PROJECT_STATE.md` | Mise a jour section LP |
| `docs/AGENT_CONTEXT.md` | Ajout section lp_history |
| `docs/ARCHITECTURE.md` | Ajout table lp_history |

### Migration requise
```bash
psql -U postgres -d lol_analytics -p 5433 -f db/migrations/create_lp_history_table.sql
```

---

## [2026-01-25] - Persistance des Rangs, Tracking LP et Nettoyage Data

### Nouveautés Majeures

#### 1. Système de Persistance des Rangs (Fix "UNRANKED")
- **Base de Données** : Ajout des colonnes `tier`, `rank`, `lp` et `profile_icon_id` dans la table `riot_dim.dim_player`.
- **RankService** : Mise à jour de la logique de récupération des rangs. Le service utilise désormais les données locales de la DB en "fallback" si l'API Riot échoue ou met trop de temps à répondre.
- **Vue SQL** : La vue `riot_analytics.player_stats` intègre maintenant ces colonnes pour un affichage instantané sur tous les profils.

#### 2. Tracking et Historique des LP (+/- LP)
- **Ingestion** : Les scripts d'importation (`manual_import_debug.py`, `auto_update_service.py`) récupèrent désormais les LPs du joueur au moment du match.
- ~~**Backfill LP** : Création d'un script de "Reverse Engineering" (`backfill_lp.py`) pour reconstruire l'historique des LPs sur les matchs passés.~~ **SUPPRIME** - voir entree ci-dessus.
- **Synchronisation** : Nouveau script `sync_lps.py` pour caler les LPs actuels de l'API Riot sur le dernier match en base.

#### 3. Nettoyage et Filtrage Strict des Joueurs
- **Qualité Data** : Nettoyage de la table `dim_player` pour ne garder que les 10 joueurs suivis.
- **Filtrage Analytics** : Mise à jour des vues analytics (notamment `recent_matches`) pour filtrer strictement via `is_tracked = TRUE`. Les joueurs "fantômes" n'apparaissent plus sur le Dashboard.

#### 4. Interface DuoQ
- **Performance** : Retour à une interface basée sur un tableau haute performance (simplifiée) pour garantir une fluidité maximale malgré le volume de données.

#### 5. Visibilité des Adversaires
- **Fix Icônes** : Restauration des icônes de champions adverses sur les lignes de matchs grâce à l'utilisation systématique de `opponent_champion_id` dans les vues.

### Fichiers Créés / Modifiés

#### Backend & Scripts
- `riot/match_ingestion.py` : Migration du schema `dim_player` et `fact_player_match`.
- `api/services/rank_service.py` : Logique de fallback DB pour les rangs + `record_lp_snapshot()`.
- ~~`scripts/backfill_lp.py`~~ : **SUPPRIME** (voir entree ci-dessus).
- `scripts/full_sync_profiles_and_lps.py` : Synchronisation globale.
- `scripts/auto_update_service.py` : Support du tracking LP en temps reel.
- `scripts/migrate_db.py` : Prise en charge des nouvelles migrations.
- `db/migrations/create_lp_history_table.sql` : **NOUVEAU** - Table historique LP.

#### SQL & Frontend
- `db/views/create_analytics_views_patch_filtered.sql` : Ajout des colonnes de rang et filtrage `is_tracked`.
- `frontend/duoq.html` & `frontend/js/duoq.js` : Retour au design tableau.

---

## [2026-01-24] - Amélioration layout Champion Pool

### Corrections CSS

#### Alignement horizontal sidebar / champion pool
- **`.profile-main`** : Ajout `display: flex` et `flex-direction: column` pour permettre le réordonnancement
- **`.champion-pool-view`** : Ajout `order: -1` pour positionner en haut du main, aligné avec la sidebar

#### Centrage colonnes tableau Champion Pool
- **Header "CHAMPION"** : `grid-column: 1 / 3` pour s'étendre sur les 2 colonnes (icône + nom) + `text-align: center`
- **`.col-icon`** du header : `display: none` (masqué car Champion couvre les 2 colonnes)
- **`.pool-champ-name`** : Ajout `text-align: center`
- **`.pool-kda`** : Ajout `justify-content: center` et `text-align: center`
- **`.col-dpm`** du header : Ajout `text-align: center`

### Fichiers modifiés
- `frontend/css/player.css`

---

## [2026-01-24] - Vue Champion Pool détaillée

### Nouveauté majeure

**Vue "Voir tous les champions"** : Nouveau bouton rouge au-dessus du bloc Top Champions sur la page profil joueur. Affiche un tableau complet de tous les champions joués par le joueur avec statistiques détaillées et items favoris.

### Frontend

#### HTML (frontend/player.html)
- **Bouton rouge "Voir tous les champions"** : Ajouté au-dessus du bloc top champions
- **Div `championPoolView`** : Conteneur pour la vue détaillée des champions
- **Mise à jour versions cache** : Scripts JS incrémentés pour forcer le rechargement

#### CSS (frontend/css/player.css)
- **Style bouton** :
  - Couleur rouge avec effet hover (rouge plus clair)
  - État actif : gris quand la vue est ouverte
- **Tableau champion pool** :
  - Header avec colonnes : Champion, Parties, WR, KDA, DPM, CS/m, Items favoris
  - **Highlight top 3** : Or (#FFD700), Argent (#C0C0C0), Bronze (#CD7F32) sur les 3 premières lignes
  - **Badge de rôle** : Icône rôle superposée sur l'icône du champion
  - **Items favoris** : Affichage des 4 items les plus utilisés avec leur WR% en badge

#### JavaScript (frontend/js/champion-pool-functions.js)
Nouveau fichier dédié aux fonctions du champion pool :

| Fonction | Description |
|----------|-------------|
| `toggleChampionPoolView()` | Toggle entre la vue matchs et la vue champion pool |
| `renderChampionPoolView()` | Génère le HTML complet du tableau avec tous les champions |
| `calculateChampionRolesForPool()` | Calcule le rôle principal de chaque champion depuis l'historique des matchs |
| `loadChampionPoolItems()` | Charge les items favoris pour chaque champion (avec cache API) |
| `renderChampionPoolItemsHTML()` | Génère le HTML des 4 items favoris avec leur WR% individuel |

### Colonnes du tableau Champion Pool

| Colonne | Description |
|---------|-------------|
| **Champion** | Icône (48px) + badge de rôle le plus joué superposé |
| **Parties** | Nombre de games jouées |
| **WR** | Winrate avec code couleur (vert >60%, bleu >50%, rouge <45%) |
| **KDA** | Ratio KDA + détail K/D/A entre parenthèses |
| **DPM** | Dégâts par minute moyens |
| **CS/m** | CS par minute moyen |
| **Items favoris** | Top 4 items avec leur WR% individuel en badge |

### Fonctionnalités UX
- **Toggle fluide** : Clic sur le bouton masque les matchs et affiche le tableau champion pool
- **Bouton adaptatif** : Couleur change (rouge → gris) selon l'état
- **Cache items** : Les items favoris sont chargés une seule fois par session
- **Rôle calculé** : Le rôle affiché est le plus fréquent pour ce champion dans l'historique du joueur

### Fichiers créés
- `frontend/js/champion-pool-functions.js` : Toutes les fonctions du champion pool

### Fichiers modifiés
- `frontend/player.html`
- `frontend/css/player.css`
- `frontend/js/player.js` (import des fonctions)

---

## [2026-01-24] - Migration Stats @15 → @12/@15/@20

### Changement majeur
Remplacement des stats @15 par un système triple timestamp : **@12, @15, @20 minutes**. Le dashboard affiche maintenant 4 colonnes (G@12, CS@12, G@20, CS@20) au lieu de 2.

### Backend

#### Modèle Pydantic (api/models.py)
```python
# PlayerRankedInfo - nouveaux champs
avg_gold_diff_12: Optional[float] = None
avg_cs_diff_12: Optional[float] = None
avg_gold_diff_20: Optional[float] = None
avg_cs_diff_20: Optional[float] = None
```

#### Service Ranking (api/services/rank_service.py)
- Renommage `get_diff15_stats()` → `get_diff_stats()`
- Récupère les 4 colonnes (@12 et @20) depuis la vue SQL

### SQL

#### Vue player_diff_at_15 (db/views/create_analytics_views_patch_filtered.sql)
```sql
-- Filtre patch 16.x (tous les patchs saison 16)
WHERE mg.patch_version LIKE '16.%'
  AND mg.game_start >= '2026-01-08 00:00:00'
  AND (fpm.gold_diff_12 IS NOT NULL OR fpm.gold_diff_20 IS NOT NULL)
```

Colonnes exposées :
- `avg_gold_diff_12`, `avg_cs_diff_12`
- `avg_gold_diff_20`, `avg_cs_diff_20`

### Frontend

#### Dashboard (frontend/js/dashboard.js)
- 4 nouvelles colonnes triables : G@12, CS@12, G@20, CS@20
- Seuils de coloration adaptés (@12: ±200 gold, @20: ±400 gold)
- Tri par `gd12`, `csd12`, `gd20`, `csd20`

#### Index (frontend/index.html)
```html
<th data-sort="gd12">G@12</th>
<th data-sort="csd12">CS@12</th>
<th data-sort="gd20">G@20</th>
<th data-sort="csd20">CS@20</th>
```

### Script de backfill

#### backfill_early_stats.py
- Mis à jour pour récupérer les 6 colonnes (@12/@15/@20)
- **Filtre patch 16.x** : Ne traite que les matchs `patch_version LIKE '16.%'`
- Limite aux joueurs trackés (`dp.puuid IS NOT NULL`)

```python
# Requête de sélection des matchs à backfill
WHERE m.game_duration > 720  -- > 12 mins
  AND (fpm.gold_diff_12 IS NULL OR fpm.gold_diff_15 IS NULL)
  AND dp.puuid IS NOT NULL
  AND m.patch_version LIKE '16.%%'
  AND m.game_start >= '2026-01-08 00:00:00'
```

### Documentation mise à jour
- `docs/AGENT_CONTEXT.md` : Références @12/@20 au lieu de @15
- `docs/PROJECT_STATE.md` : Nouvelles colonnes dashboard, script backfill

### Fichiers modifiés
- `api/models.py`
- `api/services/rank_service.py`
- `db/views/create_analytics_views_patch_filtered.sql`
- `frontend/index.html`
- `frontend/js/dashboard.js`
- `scripts/backfill_early_stats.py`
- `docs/AGENT_CONTEXT.md`
- `docs/PROJECT_STATE.md`

### Notes techniques
- Les matchs avant patch 16.1 ne sont plus backfillés (données non pertinentes)
- Le backfill prend ~5 secondes par match (rate limiting API Riot)
- 426 matchs patch 16.x au total, backfill en cours

---

## [2026-01-24] - Data Dragon v16.2.1 + Nettoyage UI Dashboard + Refonte Icônes Smart Metrics

### Nouveautés

#### 1. Synchronisation Data Dragon v16.2.1
- **Correction des Champions "Unknown"** : Mise à jour de `PATCH_VERSION` vers **16.2.1** dans `riot/load_data_dragon.py`.
- **Support des nouveaux champions** : Ambessa, Mel et les futurs champions sont désormais correctement identifiés par nom et icône.
- **Mise à jour des items** : Base de données synchronisée (697 items chargés).

#### 2. Nettoyage UI Dashboard (Page d'accueil)
- **Titres simplifiés** :
  - Section Ranked : "Ranked" au lieu de "Classement ranked SoloQ" (plus moderne).
  - Section Matchs : "Dernières parties" (retrait de l'icône horloge et de la phrase explicative redondante).
- **Consistance visuelle** : Hiérarchie des titres (h2) normalisée.

#### 3. Refonte Icônes Smart Metrics (Panneau Comparaison)
- **Migration SVG** : Remplacement de `xp_icon.png` par un fichier SVG propre (`xp_icon.svg`).
- **Correction Transparence** : Suppression de l'effet "damier" (faux détourage) présent sur l'ancienne icône.
- **Colorimétrie adaptive** : Couleur de l'éclair harmonisée avec le reste du thème (`#a1a1aa` / Zinc-400).

#### 4. Améliorations Métriques Support
- **Métrique Vision / Gold** : Ajout d'une métrique de rentabilité utilitaire pour les supports.
- **Infobulles (Tooltips)** : Implémentation de tooltips explicatifs pour "Vision / Gold" et "Dmg Efficiency" dans le panneau de comparaison.

### Fichiers modifiés

#### Backend / Scripts
- `riot/load_data_dragon.py` : Version patch MAJ vers 16.2.1.
- `frontend/img/xp_icon.svg` : Création de l'icône vectorielle.

#### Frontend
- `frontend/index.html` : Modifications des titres et nettoyage des en-têtes de section.
- `frontend/js/player.js` :
  - Utilisation de l'icône SVG pour la Lane Dominance.
  - Correction de l'affichage des rangs (gestion plus robuste des UNRANKED).
- `frontend/css/player.css` : Ajustements mineurs sur le positionnement des icônes de stats.

### Notes techniques
- Le passage au SVG permet une meilleure scalabilité et évite les artefacts de compression sur les petits formats (14x14px).
- La base de données de référence (riot_dim.dim_champion) doit être mise à jour via `python riot/load_data_dragon.py` à chaque patch majeur de League of Legends.

---


### Nouveautés

#### 1. Matchup Winrate depuis Lolalytics (Diamond+)
Le panneau de comparaison affiche maintenant le **winrate réel du matchup** scrappé depuis Lolalytics (données Diamond+) au lieu de données estimées.

**Fonctionnement :**
- URL scrappée : `https://lolalytics.com/lol/{champ1}/vs/{champ2}/build/?lane={lane}&tier=diamond_plus`
- Extraction du WR% et nombre de games via regex sur le HTML
- Cache 24h pour éviter les requêtes répétées
- Rate limiting 2s entre requêtes

**Affichage frontend :**
- Badge "Matchup WR (Diamond+)" avec pourcentage et nombre de games
- Couleur verte si >= 50%, rouge sinon

#### 2. Suppression éléments UI page joueur
- **Doughnut chart "Top Champions"** : Supprimé de la sidebar (redondant avec le bloc stats)
- **Section "Items Favoris"** : Supprimée de la sidebar (peu utilisée)

#### 3. Ajout nouveaux champions au mapping
- Ambessa (ID 799)
- Zaahen (ID 904)
- Correction ID Naafiri (950)

### Fichiers modifiés

#### Backend
- `api/services/lolalytics_service.py` : Réécrit pour scraper Lolalytics au lieu de l'API U.GG (403 Forbidden)
- `api/services/match_service.py` : Utilise uniquement Lolalytics (plus de fallback DB locale)
- `api/services/champion_mapping.py` : Ajout Ambessa, Zaahen, correction Naafiri

#### Frontend
- `frontend/player.html` : Suppression sections doughnut chart et items favoris
- `frontend/js/player.js` :
  - Suppression variable `championsChart`
  - Suppression fonction `createChampionsChart()`
  - Suppression fonction `loadPlayerItems()`
  - Mise à jour affichage source matchup "(Diamond+)"

### Notes techniques
- L'API U.GG retourne 403 Forbidden, d'où le passage au scraping Lolalytics
- Si un champion n'est pas dans le mapping, le matchup ne s'affiche pas
- Le scraping est robuste avec plusieurs patterns regex de fallback

---

## [2026-01-23] - Fix affichage bloc Top Champions / Roles pour certains joueurs

### Problème
Le bloc "Top Champions" et "Roles" (ainsi que les filtres par rôle) n'apparaissait pas pour certains joueurs comme "Me no murderer" et "Shoré", alors que les données existaient bien en base.

### Cause racine
Erreurs JavaScript silencieuses causées par des valeurs `null`/`undefined` lors du formatage des données. La fonction `utils.formatWinrate(wr)` appelait `wr.toFixed(1)` sans vérifier si `wr` était null, ce qui crashait le rendu.

### Solution
1. **Protection des utilitaires de formatage** (`config.js`) :
   - `formatWinrate: (wr) => wr != null ? \`${wr.toFixed(1)}%\` : '-'`
   - `formatKDA: (kda) => kda != null ? kda.toFixed(2) : '-'`
   - `formatNumber: (num) => num != null ? Math.round(num) : '-'`

2. **Sécurisation de `renderStatsBlock()`** (`player.js`) :
   - Ajout de blocs `try/catch` autour du rendu des champions et des rôles
   - Utilisation de l'opérateur `??` (nullish coalescing) pour les valeurs potentiellement null
   - Protection des propriétés `winrate_pct`, `games_played`, `champion_name`

### Fichiers modifiés
- `frontend/js/config.js` : Protections null dans utils
- `frontend/js/player.js` : try/catch + nullish coalescing dans renderStatsBlock()

### Notes techniques
- L'API retournait bien les données, le problème était côté rendu frontend
- Les erreurs JavaScript silencieuses empêchaient tout le bloc de s'afficher
- Solution appliquée de manière défensive pour éviter de futurs problèmes similaires

---

## [2026-01-22] - Filtres par rôle + Icônes de rôle dans tableaux

### Nouveautés

#### 1. Filtres par rôle sur la page profil joueur
Nouvelle barre de boutons au-dessus de la liste des matchs permettant de filtrer l'historique par rôle :
- **Boutons** : All / TOP / JGL / MID / ADC / SUP
- **Icônes SVG** : Community Dragon (même source que ailleurs dans l'app)
- **Reset pagination** : Au changement de filtre, la pagination revient à 10 matchs
- **Bouton MORE adaptatif** : Affiche le nombre de matchs filtrés restants

#### 2. Icônes de rôle dans les tableaux du dashboard
- **Tableau SoloQ** : Colonne "Rôle" affiche maintenant une icône au lieu du texte
- **Dernières parties** : Colonne "Rôle" affiche une icône au lieu du texte
- **Stockage rôle brut** : `mainRoleRaw` stocké séparément de `mainRole` pour les URLs d'icônes

#### 3. Amélioration affichage Stats Block
- **Initialisation immédiate** : Le bloc stats s'affiche dès le chargement (même avec données vides)
- **Placeholder CSS** : Texte "Chargement..." si le bloc est vide via `::before`

### Fichiers modifiés

#### Frontend
- `frontend/player.html` : Ajout barre de filtres par rôle (6 boutons)
- `frontend/js/player.js` :
  - Variable `currentRoleFilter`
  - Fonction `getFilteredMatches()` avec mapping des rôles
  - Event listeners sur boutons de filtre
  - Initialisation `renderStatsBlock()` au chargement
- `frontend/js/dashboard.js` :
  - Variable `rolesRawByPlayer` pour stocker les rôles bruts
  - Icônes de rôle dans `renderSoloQTable()` et `displayLastGames()`
- `frontend/css/player.css` :
  - Styles `.role-filter-bar`, `.role-filter-btn`
  - CSS `:empty` pour placeholder bloc stats
- `frontend/css/styles.css` :
  - Classe `.role-icon-small` (20x20px)

### Notes techniques
- Le mapping des rôles gère les variantes API (MIDDLE→MID, BOTTOM→ADC, UTILITY→SUPPORT)
- Les icônes utilisent `ASSETS_URLS.roleIcon()` défini dans `config.js`
- Le cache localStorage doit être vidé pour voir les icônes dans le dashboard (`localStorage.clear()`)

---

## [2026-01-22] - Refonte UI Profil Joueur : Stats Block unifié

### Changement majeur

**Nouveau bloc stats au-dessus des matchs** : Les top champions et les performances par rôle sont maintenant affichés dans un bloc compact et unifié au-dessus de la liste des matchs, au lieu d'être dispersés dans la sidebar.

### Modifications Frontend

#### Nouveau Stats Block
- **Top 3 Champions** : Affichés horizontalement avec icône champion, icône de rôle superposée, nom, games, et winrate coloré
- **Performance par rôle** : Icône de rôle + nombre de games + winrate pour chaque rôle joué
- **Layout horizontal** : Champions à gauche, séparateur vertical, rôles à droite

#### Calcul du rôle principal par champion
- Nouvelle fonction `getChampionMainRole(championId)` : Analyse les matchs pour déterminer le rôle le plus fréquent pour chaque champion
- Icône de rôle superposée en bas à droite de l'icône du champion

#### Suppression sections redondantes
- **Pool de Champions** (tableau expandable) : Supprimé de la sidebar
- **Performance par Rôle** (cartes détaillées) : Supprimé de la sidebar (intégré au stats block)

### Fichiers modifiés
- `frontend/player.html` : Suppression sections Pool de Champions et Performance par Rôle, ajout du bloc stats
- `frontend/js/player.js` :
  - Ajout variable `currentRoles`
  - Ajout fonction `getChampionMainRole()`
  - Refonte `renderStatsBlock()` (remplace `renderTopChampionsBlock()`)
  - Simplification `loadPlayerChampions()` et `loadPlayerRoles()`
- `frontend/css/player.css` :
  - Nouveaux styles `.stats-block-row`, `.stats-block-section`, `.stats-block-divider`
  - Styles `.top-champ-img-wrapper`, `.top-champ-role-icon` (icône superposée)
  - Styles `.roles-stats-grid`, `.role-stat-card`, `.role-stat-icon`

### Résultat
- Interface plus compacte et lisible
- Informations importantes visibles immédiatement au-dessus des matchs
- Sidebar allégée (seulement les charts et items favoris)

---

## [2026-01-22] - Auto-Update Permanent + Rechargement Dynamique Clé API + Patch 16.x

### Problème identifié
Les données n'étaient pas à jour sur le site malgré l'auto-update. Diagnostic :
1. Auto-update fonctionnait mais uniquement quand la page était ouverte
2. Clé API non rechargée dynamiquement après modification du `.env`
3. Patch 16.2 sorti aujourd'hui, vues SQL filtraient sur `16.1%` uniquement

### Modifications Backend

#### Auto-update permanent (api/main.py)
- **Boucle asyncio** : `auto_update_loop()` démarre au `@app.on_event("startup")`
- **Polling 60s** : Exécution toutes les minutes en arrière-plan (indépendant du frontend)
- **Shutdown propre** : `@app.on_event("shutdown")` arrête la boucle proprement
- **Logs** : `[AUTO-UPDATE] Demarrage...` / `Termine: X nouveaux matchs en Ys`

#### Rechargement dynamique clé API (riot/riot_api.py)
- **Fonction `get_api_key()`** : Relit `config/.env` à chaque appel (pas de variable globale)
- **Fonction `get_headers()`** : Génère headers avec clé actuelle
- **Tous les appels API** : Remplacé `headers=HEADERS` par `headers=get_headers()`
- **Avantage** : Modifier `.env` suffit, avec `--reload` uvicorn détecte le changement

#### Logs détaillés update_service.py
- **Logging par joueur** : `[UPDATE] Nawfou#EUW: 20 matchs recuperes`
- **Logs nouveaux matchs** : `[UPDATE] Nouveau match detecte {match_id}, insertion...`
- **Logs erreurs** : `logger.error()` au lieu de `print()`
- **Délai augmenté** : `DELAY_API = 1.3s` (au lieu de 0.5s) pour éviter rate limit 429

### Modifications SQL

#### Migration patch 16.x (db/migrations/update_views_patch_16x.sql)
- **Problème** : Patch 16.2 sorti, matchs collectés mais invisibles (filtre `LIKE '16.1%'`)
- **Solution** : Filtre `LIKE '16.%'` pour tous les patchs saison 16
- **Futur-proof** : Plus besoin de mettre à jour les vues à chaque nouveau patch
- **Script** : `update_views_patch.py` génère le SQL, `apply_view_update.py` l'applique

### Documentation

#### Nouveaux guides
- **HOWTO_UPDATE_API_KEY.md** : Guide utilisateur simple pour changer la clé
- **docs/API_KEY_RELOAD.md** : Documentation technique détaillée
- **test_api_key_reload.py** : Script de test du rechargement

#### Scripts utiles
- **check_recent_matches.py** : Vérifie derniers matchs de tous les joueurs
- **update_views_patch.py** : Génère SQL migration automatiquement
- **apply_view_update.py** : Applique migration et vérifie résultat

#### Documentation mise à jour
- **PROJECT_STATE.md** : 10 joueurs, patch 16.x, auto-update permanent
- **AGENT_CONTEXT.md** : get_api_key(), auto-update loop, migration patch
- **KNOWN_PITFALLS.md** : Nouveau patch sorti, rechargement clé API, rate limiting 1.3s

### Résultat
- **Auto-update** : Tourne en permanence (polling 60s), logs détaillés
- **Clé API** : Rechargeable sans redémarrage (modifier `.env` suffit)
- **Patch** : Tous patchs 16.x acceptés (16.1, 16.2, 16.3...)
- **Données** : 830 matchs en base, 8 matchs récents patch 16.2 visibles

---

## [2026-01-21] - Support Synergy Score - Widget compact dans panneau expandable

### Changement majeur

**Affichage du Support Synergy Score** : Le score n'apparaît plus dans l'historique des matchs mais **uniquement dans le panneau de comparaison expandable** pour les matchs SUPPORT, avec un design compact et une formule corrigée.

### Modifications Frontend

#### Widget compact dans le panneau expandable
- **Affichage conditionnel** : Widget remplace le graphique secondaire pour les matchs UTILITY avec score
- **Design compact** : Score principal (ex: "94/100"), interprétation textuelle, formule visible en bas
- **Classes CSS** : `.synergy-widget-compact`, `.synergy-compact-score`, `.synergy-compact-formula`
- **Couleurs adaptatives** : Vert (80+), Bleu (60-79), Orange (40-59), Rouge (<40)

#### Suppression du badge dans l'historique
- Badge "SYNERGY" supprimé des lignes de matchs (trop imposant)
- Score visible uniquement au clic sur un match SUPPORT

### Modifications Backend (formule corrigée)

#### Calcul du score ajusté
Ancien calcul (surcotait) :
```sql
(assists_supp / kp_jungle) plafonné à 1.0 × 50%
```

Nouveau calcul (plus réaliste) :
```sql
-- Jungle (50%)
(assists_supp / assists_jungle) × 0.5 × 50.0

-- Mid (30%)
(assists_supp / assists_mid) × 0.6 × 30.0

-- Team (20%)
(assists_supp / total_assists_team) × 5.0 × 20.0
```

**Multiplicateurs** : 0.5, 0.6, 5.0 pour normaliser et éviter la sur-notation.

#### Vue SQL recréée
- `db/views/create_analytics_views_patch_filtered.sql` : CTE `support_synergy_per_match` mise à jour
- Script Python `recreate_views.py` pour recréer les vues facilement

### Fichiers modifiés
- `frontend/js/player.js` : Widget compact, suppression badge historique
- `frontend/css/player.css` : Styles `.synergy-widget-compact` et variantes
- `db/views/create_analytics_views_patch_filtered.sql` : Formule corrigée
- `docs/PROJECT_STATE.md` : Mise à jour description widget
- `docs/AGENT_CONTEXT.md` : Documentation graphique secondaire adaptatif
- `docs/SUPPORT_SYNERGY_SCORE.md` : Formule et exemples mis à jour

### Fichiers créés
- `recreate_views.py` : Utilitaire pour recréer les vues SQL

### Résultat
- Scores plus réalistes (distribution élargie 0-100 au lieu de concentrée 80-100)
- Affichage discret et contextuel (uniquement dans le panneau expandable)
- Widget compact, lisible, avec formule explicite

---

## [2026-01-21] - Support Synergy Score par match

### Nouveauté majeure

**Score de synergie support calculé par match** : Chaque game où un joueur joue UTILITY (support) affiche maintenant un score normé 0-100 mesurant la synergie avec jungle (50%), mid (30%) et l'équipe (20%).

### Formule du score

```
Score = (
    (Assists / KP_Jungle) × 50% +
    (Assists / KP_Mid) × 30% +
    (Assists / Total_Assists_Team) × 20%
)
```

**Normalisation** : Chaque ratio plafonné à 1.0 → Score entre 0-100

### Backend

#### Vue SQL modifiée
- `db/views/create_analytics_views_patch_filtered.sql` :
  - **CTE `support_synergy_per_match`** : Calcule le score pour chaque match UTILITY
  - Identifie les coéquipiers jungle et mid (via `win = win`)
  - Calcule les ratios de synergie (assists vs KP des coéquipiers)
  - **LEFT JOIN** dans `recent_matches` → Score NULL pour tous les rôles sauf UTILITY

#### Modèle Pydantic
- `api/models.py` :
  - Ajout champ `support_synergy_score: Optional[float] = None` dans `RecentMatch`
  - NULL si le joueur n'est pas support

#### Services support (conservés)
- `api/services/support_service.py` : Score global par joueur (min 3 games)
- Endpoints `/support/synergy` et `/players/{id}/support-synergy` toujours disponibles

### Frontend

Le score s'affiche automatiquement dans l'historique des matchs pour tous les rôles UTILITY.

**Réponse API** (`/players/{id}/matches`) :
```json
{
  "role": "UTILITY",
  "champion": "Bard",
  "assists": 24,
  "support_synergy_score": 93.7
}
```

Pour les autres rôles (JUNGLE, MIDDLE, TOP, BOTTOM) : `support_synergy_score: null`

### Résultats observés

**Exemple : FlaqueDepisse (15 games support)**
- Bard avec 24 assists : **93.7/100** (excellente synergie)
- Bard avec 31 assists : **92.7/100** (excellente synergie)
- Bard avec 1 assist : **100.0/100** (synergie parfaite proportionnellement)

**Exemple : Me no murderer (64 games support)**
- Score moyen : **22.9/100** (synergie faible avec jungle/mid, mais 95.2% présence team)
- Style teamfight-oriented plutôt que early jungle/mid synergy

### Fichiers modifiés
- `db/views/create_analytics_views_patch_filtered.sql`
- `api/models.py`

### Fichiers créés (documentation)
- `SUPPORT_SCORE_PER_MATCH.md` - Guide complet
- `FINAL_SUMMARY.txt` - Résumé technique
- `db/views/create_support_synergy_score.sql` - Vue score global (conservée)
- `api/services/support_service.py` - Service score global (conservé)

### Notes techniques

**Granularité** : Score par match (pas moyenne globale)
**Performance** : Calcul intégré à la vue `recent_matches` (pas d'endpoint supplémentaire)
**Filtrage** : Uniquement matchs UTILITY, pas de minimum de games requis
**Identification équipe** : Via champ `win` (même résultat = même équipe)

### Migration

Vue SQL recréée automatiquement :
```bash
# Mise à jour appliquée
94 matchs UTILITY avec score calculé (100%)
Tous les autres rôles : score NULL
```

---

## [2026-01-21] - Spinners de chargement élégants

### Nouveautés UX

#### Remplacement complet des textes de chargement
Tous les textes "Chargement...", "Loading..." et messages similaires ont été remplacés par des spinners animés élégants sur toutes les pages.

### Frontend

#### CSS - Système de spinners complet
- `frontend/css/styles.css` :
  - **Spinner standard** : Cercle animé avec bordure colorée (`--accent-primary`)
  - **Tailles variables** : `.spinner.small` (24px), normal (40px), `.spinner.large` (56px)
  - **Variantes** : `.spinner-gradient`, `.spinner-pulse`, `.spinner-double`
  - **Loading inline** : `.loading-inline` pour tableaux et espaces restreints
  - Animation fluide à 0.8s avec `@keyframes spin`

#### HTML - Mise à jour initiale des pages
- `frontend/index.html` : Spinner dans la table "Dernières parties"
- `frontend/player.html` : Spinners dans profil, champions, rôles, items, matches
- `frontend/duoq.html` : Spinners dans matrice et liste synergies

#### JavaScript - Intégration complète
- `frontend/js/dashboard.js` :
  - Erreur ranking SoloQ → `<div class="spinner"></div>`
  - Aucune partie trouvée → spinner
  - Erreur last games → spinner

- `frontend/js/player.js` :
  - Profil en chargement → spinner
  - Badge rang → `<div class="spinner small"></div>`
  - Champions vides → spinner small
  - Items champions → `<div class="loading-inline"><div class="spinner"></div></div>`
  - Rôles, items, matches → spinners appropriés
  - Panel comparaison → spinner

- `frontend/js/duoq.js` :
  - Aucune synergie → spinner

#### Nettoyage CSS
- `frontend/css/player.css` : Suppression des anciens styles `.comparison-loading` et `.comparison-error` (maintenant centralisés dans styles.css)

### Résultat
Interface plus moderne et professionnelle avec des indicateurs de chargement visuels cohérents sur toute l'application.

### Fichiers modifiés
- `frontend/css/styles.css`
- `frontend/css/player.css`
- `frontend/index.html`
- `frontend/player.html`
- `frontend/duoq.html`
- `frontend/js/dashboard.js`
- `frontend/js/player.js`
- `frontend/js/duoq.js`

---

## [2026-01-20] - Section Live "En game" + Dashboard interactif

### Nouveautes Live

#### Section "En game" sur le Dashboard
Nouvelle section affichant en temps reel les joueurs actuellement en partie :
- **Point rouge anime** (pulse) indiquant l'activite live
- **Cartes joueurs** : Icone champion + nom joueur + timer en temps reel
- **Timer dynamique** : Le compteur s'incremente chaque seconde (cote client)
- **Cliquable** : Navigation vers le profil du joueur au clic
- **Cache localStorage** : Affichage instantane au chargement (cache 2 min)
- **Rafraichissement auto** : Appel API `/live` toutes les 60 secondes
- **Masquage intelligent** : Section cachee si aucun joueur en game

### Backend
- `api/main.py` : Nouvel endpoint `GET /live`
  - Appelle l'API Riot Spectator v5 pour chaque joueur tracke
  - Retourne `{live_count, players: [{player_name, champion_id, game_mode, game_length}]}`
- `riot/riot_api.py` : Nouvelle fonction `get_active_game(puuid)`
  - Endpoint : `lol/spectator/v5/active-games/by-summoner/{puuid}`
  - Retourne les donnees de game si en cours, `None` sinon (404)

### Frontend
- `frontend/index.html` : Section HTML "En game" entre SoloQ et Dernieres parties
- `frontend/js/dashboard.js` :
  - `loadLiveFromCache()` : Charge depuis localStorage au demarrage
  - `loadLiveGames()` : Fetch API + sauvegarde cache
  - `renderLiveCards()` : Render avec timer calcule dynamiquement
  - `goToPlayerByName()` : Navigation vers profil par nom
  - Timer `setInterval` 1s pour mise a jour compteur
  - Intervalle 60s pour refresh API
- `frontend/css/styles.css` :
  - `.live-section`, `.live-header`, `.live-dot` (animation pulse)
  - `.live-container`, `.live-card` (bordure rouge, glow)
  - `.live-champion-icon`, `.live-player-info`, `.live-game-time`

### Fichiers modifies
- `api/main.py`
- `riot/riot_api.py`
- `frontend/index.html`
- `frontend/js/dashboard.js`
- `frontend/css/styles.css`

---

## [2026-01-20] - Dashboard interactif + Radar chart ameliore + Graphiques timeline

### Nouveautes Dashboard

#### 1. Section "Dernieres parties" interactive
- **Lignes cliquables** : Clic sur une partie → navigation vers le profil du joueur
- **Bouton MORE** : Charge +5 parties supplementaires (20 parties en cache)
- **Pagination dynamique** : Le bouton affiche le nombre de parties restantes

#### 2. Affichage Victoire/Defaite
- Remplacement des symboles par texte complet ("Victoire" / "Defaite")

### Nouveautes Profil Joueur

#### 1. Radar "Performance globale" ameliore
- **Nouveaux axes** : KDA, DPM, GPM, **G@15**, **CS@15** (Winrate supprime)
- **Comparaison groupe** : Ligne pointillee orange = moyenne de tous les joueurs ranked
- **Legende** : Affichee en bas quand la comparaison est active
- **Tooltips** : Affichent les vraies valeurs (pas les valeurs normalisees)

#### 2. Graphique timeline avec ligne zero
- **Ligne pointillee a 0** : Visualisation claire si ahead ou behind
- Plugin Chart.js custom `zeroLinePlugin`

#### 3. Graphique secondaire ADC redesigne
- **Bar chart horizontal** : Dmg (k), Gold (k), CS/min, KP%
- Joueur en violet, adversaire en rouge
- Plus lisible que le radar precedent

### Frontend
- `frontend/js/dashboard.js` :
  - Variables `lastGamesDisplayed`, `allLastGames` pour pagination
  - `displayLastGames(games, append)` avec onclick sur lignes
  - `updateMoreButton()`, `loadMoreLastGames()`
  - Charge 20 parties au lieu de 5
- `frontend/js/player.js` :
  - `loadRadarChartData()` : Charge diff@15, ranking, players, roles en parallele
  - `calculateRoleAverages()` : Fusionne ranking + players pour moyennes completes
  - `createRadarChart(player, diff15, roleAverages, mainRole)` : Nouveaux axes + comparaison
  - `zeroLinePlugin` : Ligne pointillee a 0 sur graphiques timeline
  - Graphique secondaire ADC : bar horizontal au lieu de radar
- `frontend/index.html` : Bouton MORE sous la table des dernieres parties
- `frontend/css/styles.css` : Styles `.game-row.clickable`, `.more-btn`

### Fichiers modifies
- `frontend/js/dashboard.js`
- `frontend/js/player.js`
- `frontend/index.html`
- `frontend/css/styles.css`

---

## [2026-01-19] - Refonte panneau comparaison : graphiques adaptatifs + UI simplifiee

### Nouveautes

#### 1. Graphiques adaptes selon le role
Les graphiques d'evolution temporelle affichent maintenant des metriques pertinentes selon le role :

| Role | Metriques affichees | Titre du graphique |
|------|---------------------|-------------------|
| **TOP, MID, ADC** | Gold Diff + CS Diff | "Avantage Lane" |
| **JUNGLE** | Gold Diff + XP Diff | "Avantage Jungle" |
| **SUPPORT** | XP Diff + Level Diff | "Avantage XP & Niveau" |

**Justification :**
- Laners : Gold et CS sont les metriques cles de lane
- Jungle : Le CS n'est pas pertinent (camps vs minions), donc XP + Gold
- Support : Pas de farm, peu de gold propre. XP et Level montrent si le support est en retard/avance

#### 2. Simplification visuelle du panneau de comparaison
- **Suppression des items** du panneau de comparaison (deja visibles sur la ligne du match)
- **Multi-kills en mini-badge** : Petit badge circulaire a cote du nom avec tooltip au survol
  - Couleur selon le meilleur multi-kill (double=orange, triple=violet, quadra=rose, penta=rouge pulsant)
  - Affiche le total de multi-kills, details au hover

#### 3. Items conserves sur les lignes de matchs
- Les 6 slots d'items restent visibles sur chaque ligne de match
- Grille CSS restauree avec la colonne items

#### 4. Auto-update corrige pour les stats @15
- L'auto-update (`update_service.py`) recupere maintenant la timeline pour chaque nouveau match
- Les stats `gold_diff_15` et `cs_diff_15` sont calculees automatiquement

### Backend
- `api/services/update_service.py` :
  - Import de `get_match_timeline`
  - Appel timeline pour chaque nouveau match collecte
- `api/services/match_service.py` :
  - Ajout de `level` dans les diffs de timeline (`timeline.diff.level`)

### Frontend
- `frontend/js/player.js` :
  - `createTimelineCharts()` adapte selon `position` (UTILITY, JUNGLE, autres)
  - Helper `renderMultikillsBadge()` pour les mini-badges multi-kills
  - Suppression section items et multi-kills du panneau
- `frontend/css/player.css` :
  - Styles `.mk-mini-badge` (4 variantes de couleur)
  - `.timeline-chart-full` pour graphique pleine largeur

### Fichiers modifies
- `api/services/update_service.py`
- `api/services/match_service.py`
- `frontend/js/player.js`
- `frontend/css/player.css`

---

## [2026-01-19] - Panneau comparaison adaptatif par role + Graphiques timeline

### Nouveautes

#### 1. Stats adaptees selon le role
Le panneau de comparaison affiche maintenant des statistiques differentes selon le role du joueur :

| Role | Sections affichees |
|------|-------------------|
| **TOP** | Matchup (solo kills, gold/cs/xp @15), Economie, Impact Structure (turret dmg) |
| **JUNGLE** | Combat (KDA), Farming & Objectifs (CS, objective dmg), Economie, Vision |
| **MID** | Matchup (solo kills, @15), Degats & Teamfight (dmg, CC time), Economie, Vision |
| **ADC** | Matchup (KDA, @15), Economie (gold/CS complet), Impact Global (dmg, turret, objectives) |
| **SUPPORT** | Controle Vision (vision score, wards), Impact & KP (assists, CC, healing), Economie |

#### 2. Graphiques d'evolution temporelle
Ajout de courbes montrant l'evolution de l'avantage/desavantage au cours de la partie :
- **Gold Advantage** (courbe orange) : difference de gold minute par minute
- **CS Advantage** (courbe violette) : difference de CS minute par minute
- Fill colore sous la courbe (vert si positif, rouge si negatif)
- Tooltips interactifs au survol

#### 3. Ameliorations visuelles
- Valeurs des joueurs en gris neutre (au lieu de bleu/rouge)
- Seule la colonne diff est coloree (vert = positif, rouge = negatif)
- Label du role affiche au-dessus du "VS" dans le header
- Grid responsive pour les sections (auto-fit selon le nombre)

### Backend
- `api/services/match_service.py` :
  - `_extract_timeline_history()` : Extrait l'historique complet de la timeline (gold, cs, xp, level) pour chaque minute
  - Reponse de `get_match_comparison()` inclut maintenant `timeline` avec :
    - `minutes` : liste [0, 1, 2, ...]
    - `player` / `opponent` : gold, cs, xp, level par minute
    - `diff` : differences gold, cs, xp (joueur - adversaire)

### Frontend
- `frontend/js/player.js` :
  - `renderComparisonPanel()` refactorise avec `buildStatsHTML()` adaptatif selon `position`
  - Helper `row()` pour generer les lignes de stats
  - Cache `timelineCharts` pour eviter les fuites memoire
  - `createTimelineCharts()` : creation des graphiques Chart.js (gold diff + cs diff)
- `frontend/css/player.css` :
  - `.comp-role-label` : badge du role au-dessus du VS
  - `.comparison-timeline` : conteneur des graphiques
  - `.timeline-charts-container` : grid 2 colonnes
  - `.timeline-chart-wrapper` : wrapper 150px pour les canvas
  - `.comp-value-you`, `.comp-value-enemy` : couleur grise neutre
  - Media query mobile (1 colonne, 120px)

### Fichiers modifies
- `api/services/match_service.py`
- `frontend/js/player.js`
- `frontend/css/player.css`

---

## [2026-01-19] - Fix chargement des dernieres parties + Detection cle API

### Probleme 1 : Parties non affichees
Les dernieres parties jouees n'apparaissaient pas dans le dashboard ni sur les pages joueurs. Les matchs etaient bien collectes dans `match_game` mais les stats des joueurs n'etaient pas inserees dans `fact_player_match`.

### Cause racine
Deux problemes combines :
1. **Noms de colonnes incorrects** : Le code Python utilisait `gold_at_15` et `cs_at_15` alors que la table PostgreSQL avait `gold_diff_15` et `cs_diff_15`. L'insertion SQL echouait silencieusement.
2. **Pas de filtre queue_type** : `update_service.py` recuperait tous les types de matchs sans filtrer sur Ranked Solo/Duo (queue 420).

### Solution
1. Correction des noms de colonnes dans `riot/match_ingestion.py` (lignes 276-277)
2. Ajout du parametre `queue_type=420` dans `api/services/update_service.py` (ligne 65)
3. Re-insertion des stats pour les matchs orphelins

### Probleme 2 : Cle API expiree non detectee
La cle API Riot expirait silencieusement, causant des joueurs "UNRANKED" et des parties non collectees sans message d'erreur clair.

### Solution
1. **Endpoint `/health/riot`** : Permet de verifier rapidement si la cle est valide
2. **Warning au demarrage** : Le serveur affiche un message clair si la cle est invalide
3. **`override=True`** : Force le rechargement de la cle depuis `.env` a chaque demarrage

### Fichiers modifies
- `riot/match_ingestion.py` : Correction noms colonnes
- `api/services/update_service.py` : Ajout `queue_type=420`
- `riot/riot_api.py` : Fonction `check_api_key()`, `override=True` pour load_dotenv
- `api/main.py` : Endpoint `/health/riot`, verification au demarrage

### Diagnostic rapide
```bash
curl http://localhost:8080/health/riot
```

---

## [2026-01-18] - Panneau de comparaison lane matchup expandable

### Nouveaute
**Panneau de comparaison detaille** : Au clic sur un match dans le profil joueur, un panneau s'ouvre avec des stats comparatives exhaustives entre le joueur et son adversaire de lane.

### Backend
- `api/services/match_service.py` :
  - `get_match_comparison(match_id, player_id)` : Recupere les details du match via API Riot et extrait les stats comparatives
  - `_extract_stats_at_15()` : Extrait les stats Gold/CS/XP/Level a 15 minutes depuis la timeline
  - Identification automatique de l'adversaire de lane (meme position, equipe opposee)
- `api/main.py` : Nouvel endpoint `GET /matches/{match_id}/comparison/{player_id}`

### Frontend
- `frontend/js/config.js` : Ajout endpoint `matchComparison`
- `frontend/js/api.js` : Ajout methode `getMatchComparison(matchId, playerId)`
- `frontend/js/player.js` :
  - Matchs cliquables avec fleche d'expansion
  - `toggleMatchComparison()` : Gestion ouverture/fermeture du panneau
  - `renderComparisonPanel()` : Affichage des stats comparatives en 4 sections
  - Cache des comparaisons (evite appels API repetes)
- `frontend/css/player.css` : ~350 lignes de styles pour le panneau de comparaison

### Donnees affichees dans le panneau
| Section | Donnees |
|---------|---------|
| Combat | K/D/A, KDA ratio, Solo Kills, Largest Spree |
| Economie | Gold Total, Gold/min, Gold@15, CS Total, CS/min, CS@15 |
| Degats | Damage Dealt, DPM, Damage Taken, Turret Damage, Objective Damage |
| Vision | Vision Score, Wards Placed/Killed, Control Wards, CC Time |
| Items | Comparaison visuelle des builds (7 slots) |
| Multi-kills | Badges Double/Triple/Quadra/Penta (si applicable) |

### Notes techniques
- L'endpoint appelle l'API Riot en temps reel (match detail + timeline)
- Rate limit de 1.2s entre chaque appel API Riot
- Le panneau est responsive (4 colonnes → 2 colonnes → 1 colonne selon la largeur)
- Les differences sont colorees (vert = positif, rouge = negatif)
- Les stats @15 ne sont disponibles que si le match a dure plus de 15 minutes

---

## [2026-01-18] - Stats Diff @15 vs Adversaire Direct

### Changement majeur
Les stats @15 affichent maintenant le **differentiel vs adversaire direct de lane** au lieu des valeurs absolues.

Mapping adversaire : `1v6, 2v7, 3v8, 4v9, 5v10` (meme position, equipe opposee)

### Backend
- `riot/match_ingestion.py` :
  - `extract_stats_at_15()` calcule maintenant `gold_diff_15` et `cs_diff_15` (joueur - adversaire)
  - Valeur positive = ahead, negative = behind

### SQL
- **Migration** : `db/migrations/rename_stats_at_15_to_diff.sql`
  - Renomme `gold_at_15` → `gold_diff_15`
  - Renomme `cs_at_15` → `cs_diff_15`
  - Reset les valeurs (anciennes donnees absolues invalides)
- `db/views/create_analytics_views_patch_filtered.sql` :
  - Colonnes renommees `avg_gold_diff_15`, `avg_cs_diff_15` dans `player_stats`
  - Vue `player_diff_at_15` mise a jour

### Scripts
- `scripts/update_stats_at_15.py` : Adapte pour les nouvelles colonnes diff

### Backfill execute
- 270 timelines telechargees
- 331 matchs mis a jour
- 9 matchs skips (< 15 min)
- 0 erreurs

---

## [2026-01-18] - Stats @15 completes (Gold@15, CS@15)

### Nouveautes
- **Stats Gold@15 et CS@15** : Moyennes de gold et CS a 15 minutes affichees sur le dashboard et les profils joueurs
- **Colonnes triables** : G@15 et CS@15 triables dans le tableau SoloQ du dashboard
- **Script de backfill** : `scripts/update_stats_at_15.py` pour mettre a jour les matchs existants

### Backend
- `api/services/rank_service.py` :
  - Ajout methode `get_diff15_stats()` pour recuperer les stats @15 depuis la vue SQL
  - Integration des stats @15 dans le ranking (avec conversion Decimal → float)
- `api/models.py` : Ajout champs `avg_gold_diff_15`, `avg_cs_diff_15` (Optional) dans `PlayerRankedInfo`
- `scripts/collect_with_lp_tracking.py` : Appel a `get_match_timeline()` pour collecter les stats @15 a chaque collecte
- `scripts/update_stats_at_15.py` : Nouveau script pour backfill les stats @15 des matchs existants

### SQL
- `db/views/create_analytics_views_patch_filtered.sql` :
  - VUE 10 : `player_diff_at_15` simplifiee - moyennes gold@15 et cs@15 (pas de diff vs adversaire)

### Frontend
- `frontend/index.html` : Colonnes "G@15" et "CS@15" triables dans le tableau SoloQ
- `frontend/js/dashboard.js` :
  - Affichage des stats @15 dans le tableau
  - Tri par G@15 et CS@15
- `frontend/js/player.js` : Affichage "Gold@15" et "CS@15" dans le profil joueur

### Notes
- Les stats @15 affichent les valeurs absolues (gold moyen, CS moyen a 15 min)
- Le calcul de diff vs adversaire necessite de stocker les stats de tous les participants (pas implemente)
- Apres modification, redemarrer le serveur pour vider le cache ranking (5 min)

---

## [2026-01-18] - Ajout stats @15 et fix chargement

### Nouveautes
- **Stats G.Diff@15 et CS.Diff@15** : Ajout des statistiques de difference d'or et CS a 15 minutes vs adversaire de meme lane
- **Vues SQL manquantes** : Creation de `player_items` et `player_champion_items` (fix items qui ne chargeaient pas)
- **Stats joueur depuis SoloQ** : Le profil joueur utilise maintenant les stats du ranking SoloQ (Games, Winrate) au lieu des donnees filtrees

### Backend
- `riot/riot_api.py` : Ajout fonction `get_match_timeline()` pour recuperer les timelines
- `riot/match_ingestion.py` :
  - Ajout fonction `extract_stats_at_15()` pour extraire gold/cs a 15min
  - Modification `insert_player_stats()` pour stocker les nouvelles colonnes
- `api/main.py` : Ajout endpoint `/players/{id}/diff15`
- `api/models.py` : Ajout champs `avg_gold_at_15`, `avg_cs_at_15` dans `PlayerStats`

### SQL
- `db/views/create_analytics_views_patch_filtered.sql` :
  - VUE 8 : `player_items` - Items par joueur
  - VUE 9 : `player_champion_items` - Items par joueur et champion
  - VUE 10 : `player_diff_at_15` - Diff gold/CS @15 vs adversaire meme lane
  - Colonnes `avg_gold_at_15`, `avg_cs_at_15` ajoutees a `player_stats`
- Table `riot_fact.fact_player_match` : Ajout colonnes `gold_at_15`, `cs_at_15`

### Frontend
- `frontend/js/config.js` : Ajout endpoint `playerDiff15`
- `frontend/js/api.js` : Ajout methode `getPlayerDiff15()`
- `frontend/js/player.js` :
  - Chargement des stats diff@15 en parallele
  - Affichage G.Diff@15 et CS.Diff@15 dans le bloc stats (avec couleur vert/rouge)
  - Stats Games/Winrate proviennent maintenant du ranking SoloQ

### Note
Les stats @15 seront disponibles apres la prochaine collecte avec une cle API valide.
La collecte backfill des matchs existants necessite de renouveler la RIOT_API_KEY (expiree).

---

## [2026-01-18] - Fix affichage matchs joueurs

### Problème
Les pages de **Nawfou, Me no murderer, Shore et Reaper** n'affichaient pas leurs matchs (erreur 500 Internal Server Error).

### Cause racine
Certains matchs avaient `kda = NULL` dans la base de données (calcul impossible quand `deaths = 0`). Les modèles Pydantic déclaraient ces champs comme `float` (non-nullable), causant une erreur de validation FastAPI.

### Diagnostic
```
Nawfou (ID=1): 2 matchs avec kda=NULL
Me no murderer (ID=2): 2 matchs avec kda=NULL
Shore (ID=23): 1 match avec kda=NULL
Reaper (ID=26): 3 matchs avec kda=NULL
```
Les joueurs qui fonctionnaient (FlaqueDepisse, Nawlol, etc.) n'avaient aucun match avec `kda=NULL`.

### Solution
Modification de `api/models.py` - Rendu nullable les champs float pouvant être NULL :

**RecentMatch** (ligne 89) :
```python
# Avant
kda: float

# Après
kda: Optional[float] = None
```

**PlayerChampion** (lignes 38-44) :
```python
# Avant
winrate_pct: float
avg_kills: float
avg_deaths: float
avg_assists: float
avg_kda: float
avg_cs_per_min: float
avg_dpm: float

# Après
winrate_pct: Optional[float] = None
avg_kills: Optional[float] = None
avg_deaths: Optional[float] = None
avg_assists: Optional[float] = None
avg_kda: Optional[float] = None
avg_cs_per_min: Optional[float] = None
avg_dpm: Optional[float] = None
```

**PlayerStatsByRole** (lignes 114-117) :
```python
# Avant
winrate_pct: float
avg_kda: float
avg_cs_per_min: float
avg_dpm: float

# Après
winrate_pct: Optional[float] = None
avg_kda: Optional[float] = None
avg_cs_per_min: Optional[float] = None
avg_dpm: Optional[float] = None
```

### Fichiers modifiés
- `api/models.py`

### Fichiers de test créés (peuvent être supprimés)
- `find_null_kda.py`
- `test_all_players.py`
- `debug_players.py`
- `test_reaper_sql.py`
- `test_player_ids.html`
- `frontend/test-links.html`
- `frontend/clear-cache.html`
- `DIAGNOSTIC.md`
- `FIX_SUMMARY.md`

---

## [2026-01-17] - Corrections multiples dashboard/profils

### Problèmes résolus
1. **Concordance données dashboard/joueurs** : Jointure frontend par `player_id` au lieu de `display_name`
2. **Filtre SQL manquant** : Vue `player_stats_by_role` applique maintenant le filtre `game_start >= 2026-01-08`
3. **Modèle Pydantic incomplet** : `RecentMatch` déclare tous les champs (items, duo_kda, player_id, etc.)
4. **Pages joueurs sans matchs** : Correction type `duo_kda` (float au lieu de str)

### Fichiers modifiés
- `api/models.py`
- `db/views/create_analytics_views_patch_filtered.sql`
- `frontend/js/dashboard.js`

---

## [2026-01-16] - Mise en place initiale

### Fonctionnalités
- Dashboard avec classement SoloQ
- Profils joueurs détaillés
- Historique matchs avec pagination
- Détection DuoQ automatique
- Cache backend + localStorage
- Tunnel ngrok pour partage

### Stack technique
- PostgreSQL 15
- Python 3.11 + FastAPI
- Vanilla JS (no Node)
- Vues SQL analytiques

---

## Template pour nouvelles sessions

```markdown
## [YYYY-MM-DD] - Titre de la session

### Problème
Description du problème rencontré.

### Cause racine
Analyse technique de la cause.

### Solution
Description de la solution appliquée avec extraits de code si pertinent.

### Fichiers modifiés
- Liste des fichiers modifiés

### Notes
Remarques additionnelles si nécessaire.
```
