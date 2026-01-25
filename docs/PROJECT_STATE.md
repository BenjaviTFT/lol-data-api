# LOL ANALYTICS - V1.0.0 STABLE

## Objectif
Analytics privé League of Legends pour 10 joueurs : ranking SoloQ avec stats de performance, profils détaillés, synergies DuoQ.
**VERSION FIGÉE V1.0.0 (25/01/2026)** - Base stable pour déploiement.

## Stack
PostgreSQL 15 • Python 3.11 • FastAPI • Vanilla JS (no Node)

## Déploiement
- **VPS Hostinger** : En cours de déploiement (V1.0.0)
- **Local** : http://localhost:8080 (`python -m uvicorn api.main:app --reload --port 8080`)
- **Ngrok** : Tunnel public via ngrok (`ngrok http 8080`) - URL temporaire pour partage avec amis

## Joueurs Trackés (10)
Nawfou, Nawlol, Reaper, Shore, Bardella2027, Me no murderer, Viirtu, T1 KRKING, Benjavii, loki
- Source : `config/players.py` (TRACKED_PLAYERS)
- Région : EUW1 (tous)

## Données Actives
- ~850 matchs locaux (PostgreSQL)
- Filtre strict : **patch 16.x (saison 16)** + date >= 2026-01-08 + **Ranked Solo/Duo (queue 420)**
- **Filtrage strict tracking** : Seuls les matchs des 10 joueurs officiels (`is_tracked = TRUE`) sont affichés.
- Vues SQL filtrées : toutes les vues `riot_analytics.*` appliquent ces filtres.
- **Auto-update permanent** : Collecte automatique toutes les 60 secondes en arrière-plan (backend).

## Fonctionnalités Déployées

### Dashboard
✅ Classement SoloQ unifié (rangs officiels + stats performance)
✅ **Persistance des Rangs** : Les informations de palier (Tier, Rank, LP) sont stockées en DB (`dim_player`).
✅ **Fallback DB intelligent** : En cas d'erreur API Riot, le site affiche le dernier rang connu en base au lieu de "UNRANKED".
✅ **Tracking LP (+/- LP)** : Affichage du gain/perte de LPs directement sur les lignes de matchs.
✅ Tableau SoloQ triable : Joueur, Rank↕, Games↕, WR↕, KDA↕, DPM↕, GPM↕, **G@12↕**, **CS@12↕**, **G@20↕**, **CS@20↕**, Rôle, Best champs
✅ **Icônes de rôle** : Remplacent le texte dans le tableau SoloQ et les dernières parties (Community Dragon SVG)
✅ Icônes de profil (summoner icons Riot)
✅ **Section "En game"** : Joueurs en partie en temps réel
  - Point rouge animé (pulse) + timer qui s'incrémente chaque seconde
  - Icône champion + nom joueur, cliquable vers profil
  - Cache localStorage (2 min) pour affichage instantané
  - Refresh automatique toutes les 60 secondes
  - Section masquée si aucun joueur en game
✅ Section "Dernières parties" interactive :
  - **Lignes cliquables** : Navigation vers profil joueur au clic
  - **Bouton MORE** : Charge +5 parties (20 parties en cache)
  - **Icône de rôle** au lieu du texte
  - **Icône Adversaire** : Affichage systématique du champion adverse.
  - Affichage Victoire/Defaite en texte
✅ Cache double niveau (backend 5min + localStorage 5min)
✅ **Spinners de chargement élégants** : Cercles animés au lieu de textes "Chargement..."
✅ **Titres simplifiés** : Labels "Ranked" et "Dernières parties" épurés (retrait d'émojis et sous-titres redondants)

### Profil Joueur
✅ Layout 2 colonnes : sidebar stats (400px) + historique matchs (1fr)
✅ Header minimaliste : icone 64x64px + badge rang (W/L avant LP)
✅ Stats globales en grid 2 colonnes : Games, WR, KDA, CS/min, **G@12**, **CS@12**, **G@20**, **CS@20**
✅ **Stats depuis ranking SoloQ** : Games et Winrate proviennent des donnees API Riot (priorité API, fallback DB)
✅ **Performance radar chart ameliore** : Axes KDA/DPM/GPM + stats early game + ligne comparaison moyenne groupe (orange pointille)
✅ **Stats Block unifié** (au-dessus des matchs) :
  - **Top 3 Champions** : Icône + rôle superposé + nom + games + WR%
  - **Performance par rôle** : Icône rôle + games + WR% (format compact horizontal)
  - Affiché immédiatement au chargement (même si données vides)
✅ **Vue Champion Pool détaillée** :
  - **Bouton rouge "Voir tous les champions"** : Toggle entre vue matchs et vue champion pool
  - **Tableau complet** : Champion (icône + rôle), Parties, WR (coloré), KDA, DPM, CS/m, Items favoris
  - **Highlight top 3** : Or/Argent/Bronze sur les 3 premières lignes
  - **Items favoris** : Top 4 items avec leur WR% individuel en badge
  - **Rôle calculé** : Rôle le plus fréquent pour chaque champion depuis l'historique
✅ **Filtres par rôle** : Barre de boutons (All/TOP/JGL/MID/ADC/SUP) pour filtrer l'historique des matchs
  - Icônes de rôle cliquables (Community Dragon SVG)
  - Reset automatique de la pagination au changement de filtre
  - Bouton MORE adapté au nombre de matchs filtrés
✅ Historique matchs format ultra-compact (48px hauteur) : date/heure + duree + champion 44px + K/D/A | KDA | CS (CS/min) + 6 items 32px + badge DuoQ + **+/- LP**
✅ **Badge DuoQ violet cliquable** : detection automatique + affichage partenaire (nom, champion 32px, role, KDA, CS) + navigation vers profil au clic
✅ Pagination historique : 10 matchs par defaut + bouton MORE
✅ Optimisation espaces verticaux : gaps reduits (0.35rem entre cartes, 0.4rem entre colonnes)
✅ **Panneau de comparaison lane matchup** : Au clic sur un match, panneau expandable avec stats comparatives vs adversaire de lane
✅ **Matchup WR (Diamond+)** : Winrate du matchup scrappé depuis Lolalytics, affiché dans le panneau de comparaison
✅ **Stats adaptees par role** : TOP (matchup, structure), JUNGLE (objectifs, vision), MID (teamfight), ADC (economie, impact), SUPPORT (vision, KP)
✅ **Graphiques timeline adaptatifs par role** avec **ligne zero pointillee** :
  - Laners (TOP/MID/ADC) : Gold Diff + CS Diff ("Avantage Lane")
  - Jungle : Gold Diff + XP Diff ("Avantage Jungle")
  - Support : XP Diff + Level Diff ("Avantage XP & Niveau")
✅ **Graphique secondaire adaptatif** :
  - ADC : Bar chart horizontal (Dmg/Gold/CS/KP) joueur vs adversaire
  - JUNGLE/MID/SUPPORT : KP% et Vision Score
  - TOP : Damage dealt vs Damage taken
✅ **Multi-kills en mini-badge** : Badge circulaire a cote du nom avec tooltip hover (double=orange, triple=violet, quadra=rose, penta=rouge)
✅ **Spinners de chargement élégants** : Design moderne avec animations fluides (3 tailles disponibles)
✅ **Icônes Smart Metrics (Lane Dominance)** : Migration vers des icônes SVG propres avec colorimétrie adaptive
✅ **Infobulles (Tooltips)** : Explications détaillées pour Dmg Efficiency et Vision / Gold accessibles au survol

### Autres
✅ Comparateur 2 joueurs
✅ DuoQ Matrix + synergies (Interface Tableau Haute-Performance)
✅ Auto-update (polling 60s)
✅ Items filtrés (finaux uniquement, pas de composants/wards/potions)
✅ Mapping rôles automatique (UTILITY→SUPPORT, BOTTOM→ADC, MIDDLE→MID)
✅ Visuels darkintaqt.com CDN (champions + items)
✅ **UX moderne** : Spinners animés partout (dashboard, profils, DuoQ) au lieu de textes statiques

## Architecture
- Structure projet **FIGEE** (voir [ARCHITECTURE.md](ARCHITECTURE.md))
- Vues SQL = source de verite (10 vues dans `riot_analytics`, filtrage par `is_tracked` obligatoire)
- Separation stricte routes / services / DB
- Frontend servi via StaticFiles FastAPI
- **Timeline API** : `riot_api.get_match_timeline()` pour stats diff @12/@15/@20 (vs adversaire lane)
- **Configuration centralisée** : `config/settings.py` charge variables depuis `config/.env`
- **Auto-update backend** : Boucle asyncio polling 60s (startup FastAPI)
- **Rechargement dynamique clé API** : `riot_api.get_api_key()` relit `.env` à chaque appel
- **Codage défensif frontend** : `config.js` utilities protègent contre null, `player.js` utilise try/catch + nullish coalescing

## Historique des modifications
Voir [CHANGELOG.md](../CHANGELOG.md) pour l'historique complet des sessions de développement.

## Problèmes Connus Actifs
Voir [KNOWN_PITFALLS.md](KNOWN_PITFALLS.md)
- **Historique des LP** : Les games non capturées en temps réel n'affichent pas de gain/perte LP (affichage vide au lieu d'estimation).
- **Table lp_history** : Nouvelle table pour tracker l'évolution des LPs. Voir `db/migrations/create_lp_history_table.sql`.
- **RIOT_API_KEY** : Expire toutes les 24h, rechargée dynamiquement depuis `.env` (voir [HOWTO_UPDATE_API_KEY.md](../HOWTO_UPDATE_API_KEY.md))
- **Rate limiting API Riot** : Délai de 1.3s entre chaque appel (update_service.py)
- **Cache navigateur** : Ctrl+Shift+R pour forcer rechargement JS/CSS
- **Cache backend ranking** : 5 min, automatiquement rafraîchi par auto-update

- **Encodage Windows** : Éviter les emojis dans les print() Python (erreur UnicodeEncodeError)
- **Nouveau patch** : Vues SQL filtrent sur patch 16.x (tous patchs saison 16 acceptés)
- **Database Reference** : Synchronisée avec Data Dragon **v16.2.1** (tous les champions récents inclus)
- **Valeurs NULL en JS** : Les utilitaires `config.js` protègent contre null (`wr != null ? ... : '-'`)

## Points Critiques
- TRACKED_PLAYERS (`config/players.py`) = source joueurs (pas `dim_player` en DB)
- Tous les joueurs sont sur EUW1 (y compris T1 KRKING malgré tag #KRJPN)
- Ne PAS modifier la structure projet sans mise à jour de [ARCHITECTURE.md](ARCHITECTURE.md)
- Calculs analytiques exclusivement en SQL (pas Python/JS)

## Configuration
📌 **Variables d'environnement** (`config/.env`) :
- `POSTGRES_PASSWORD` : Mot de passe PostgreSQL local
- `RIOT_API_KEY` : Clé API Riot Games (expire 24h, rechargée dynamiquement)

📌 **Chargement centralisé** : `config/settings.py`
- Toutes les imports doivent utiliser `from config.settings import RIOT_API_KEY, POSTGRES_PASSWORD`
- `riot_api.get_api_key()` : Recharge dynamiquement depuis `.env` (pas de variable globale)
- Modifier `.env` suffit, avec `--reload` uvicorn détecte le changement automatiquement

## Features Principales
- ✅ Classement SoloQ unifie (rangs Riot + stats performance)
- ✅ **Section Live "En game"** : Joueurs en partie avec timer temps reel + clic vers profil
- ✅ Profils joueurs detailles (layout 2 colonnes, design minimaliste)
- ✅ **Stats Early Game** : G@12, CS@12, G@20, CS@20 vs adversaire direct de lane (colonnes triables)
- ✅ Historique matchs avec pagination (+10 par clic)
- ✅ **Panneau comparaison lane matchup** : Clic sur match = stats adaptees au role + graphique timeline adaptatif
- ✅ **Graphiques adaptes par role** : Laners (Gold/CS), Jungle (Gold/XP), Support (XP/Level)
- ✅ Detection DuoQ automatique avec badge violet
- ✅ Icones de roles officielles Riot (Community Dragon SVG)
- ✅ **Vue Champion Pool détaillée** : Bouton "Voir tous les champions" avec tableau complet (stats + items favoris)
- ✅ Cache backend 5min + tri colonnes tableau
- ✅ Tunnel ngrok pour partage temporaire
- ✅ **Auto-update permanent backend** : Polling 60s en arrière-plan (boucle asyncio)
- ✅ **Rechargement dynamique clé API** : Modifier `.env` suffit, pas de redémarrage manuel
- ✅ **Filtres patch dynamiques** : Vues SQL acceptent tous patchs 16.x (futur-proof)
- ✅ Script de backfill stats @12/@15/@20 (`scripts/backfill_early_stats.py`) - patch 16.x uniquement
- ✅ **Matchup WR Lolalytics** : Données Diamond+ scrappées pour afficher le WR du matchup champion vs champion