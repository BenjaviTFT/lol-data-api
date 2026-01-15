# 🎨 Guide Complet - Frontend LoL Analytics

## 🚀 Démarrage en 3 étapes

### ✅ Étape 1 : Lancer l'API Backend

**Terminal 1 (API) :**
```bash
python run_api.py
```

**Vérification :**
- API accessible sur : http://127.0.0.1:8000
- Documentation Swagger : http://127.0.0.1:8000/docs

### ✅ Étape 2 : Lancer le Frontend

**Terminal 2 (Frontend) :**
```bash
cd frontend
python -m http.server 8080
```

OU double-cliquer sur `start_frontend.bat`

**Vérification :**
- Frontend accessible sur : http://localhost:8080

### ✅ Étape 3 : Accéder aux pages

1. **Dashboard** : http://localhost:8080
2. **Profil Joueur** : Cliquer sur un joueur depuis le dashboard
3. **Comparateur** : http://localhost:8080/comparator.html
4. **Matrice DuoQ** : http://localhost:8080/duoq.html

---

## 📊 Fonctionnalités par Page

### 🏠 1. Dashboard (Page Principale)

**URL :** http://localhost:8080/index.html

**Ce que tu verras :**

#### A. Stats Globales (4 cartes en haut)
```
👥 Joueurs    🎮 Total Games    🏆 Winrate Global    ⚔️ KDA Moyen
   6              124               54.0%                3.39
```

#### B. Classement Interne
Ranking avec score composite :
```
#1  Reaper#491        59.07 pts  |  65% WR  |  3.52 KDA
#2  Me no murderer   54.10 pts  |  65% WR  |  3.99 KDA
#3  Shoré            53.59 pts  |  55% WR  |  3.31 KDA
```

**Badges :**
- 🥇 Or : Rank 1
- 🥈 Argent : Rank 2
- 🥉 Bronze : Rank 3

#### C. Grille des Joueurs
Cards cliquables avec :
- Nom du joueur
- Total games
- Winrate %
- KDA Ratio
- CS/min
- DPM

**Action :** Cliquer sur une card → profil détaillé

---

### 👤 2. Profil Joueur

**URL :** http://localhost:8080/player.html?id=1

**Ce que tu verras :**

#### A. Header Profil
- Nom en grand (dégradé violet)
- Total Games, Winrate, KDA, Record (W/L)

#### B. Vue d'ensemble (7 stats cards)
```
⚔️ Kills    💀 Deaths    🤝 Assists    🌾 CS/min
🔥 DPM      💰 GPM       👁️ Vision
```

#### C. Graphiques

**1. Radar Chart - Performance Globale**
- 6 axes : Winrate, KDA, CS/min, DPM, GPM, Vision
- Normalisé sur 100
- Forme polygonale représentant les forces/faiblesses

**2. Donut Chart - Top Champions**
- Top 5 champions les plus joués
- Taille proportionnelle au nombre de games
- Couleurs distinctes par champion

#### D. Table Champions
Toutes les stats par champion :
- Nom du champion
- Games joués
- Winrate (badge coloré)
- KDA moyen
- CS/min
- DPM

#### E. Performance par Rôle
Cards pour chaque position jouée :
```
⚔️ TOP         Games: 12   WR: 58%   KDA: 3.2
🌳 JUNGLE      Games: 8    WR: 62%   KDA: 4.1
✨ MIDDLE      Games: 15   WR: 53%   KDA: 3.8
```

---

### ⚖️ 3. Comparateur

**URL :** http://localhost:8080/comparator.html

**Ce que tu verras :**

#### A. Sélection
```
[Dropdown Joueur 1]    VS    [Dropdown Joueur 2]
```

#### B. Radar Chart Superposé
- Joueur 1 : Courbe bleue
- Joueur 2 : Courbe orange
- Comparaison visuelle instantanée

#### C. Grille de Stats (10 métriques)
Chaque carte affiche :
```
         WINRATE
Player1: 65%    vs    Player2: 54%
(meilleur en vert)
```

Métriques comparées :
- Total Games
- Winrate
- KDA Ratio
- Kills/Deaths/Assists (moyennes)
- CS/min
- DPM / GPM
- Vision Score

#### D. Face-à-Face (Barres horizontales)
Barres de comparaison pour :
- Winrate
- KDA Ratio
- Damage Per Minute
- CS Per Minute
- Vision Score

**Exemple :**
```
Winrate
Player1 (65%)  ████████████░░░░  Player2 (54%)
     35%                              65%
```

**Comment utiliser :**
1. Sélectionner 2 joueurs différents
2. Comparaison s'affiche automatiquement
3. Analyser les forces/faiblesses

---

### 🤝 4. Matrice DuoQ

**URL :** http://localhost:8080/duoq.html

**Ce que tu verras :**

#### A. Matrice Interactive (NxN)

**Structure :**
```
        Nawfou  Reaper  Shoré   Viirtu
Nawfou    -      --     75% 4G   --
Reaper   --      -     100% 3G   --
Shoré    75%   100%      -       --
Viirtu   --     --      --       -
```

**Code couleur :**
- 🟢 **Vert foncé** : ≥70% WR (excellente synergie)
- 🔵 **Bleu/Violet** : 50-70% WR (bonne synergie)
- 🟠 **Orange** : <50% WR (à améliorer)
- ⚪ **Gris** : Aucune game ensemble

**Interactions :**
- **Hover** : zoom léger sur la cellule
- **Click** : popup avec détails du duo

#### B. Top Synergies (Liste)

Cartes triées par winrate :
```
#1  🏆  Nawfou + Shoré
        4 games | 3 wins | 75.0% WR
        KDA P1: 5.2  |  KDA P2: 4.8
```

#### C. Légende

Guide visuel :
- Carré vert : Excellente synergie
- Carré bleu : Bonne synergie
- Carré orange : Synergie moyenne
- Carré gris : Pas de game

**Comment utiliser :**
1. Scanner visuellement la matrice
2. Identifier les zones vertes (meilleures synergies)
3. Cliquer pour plus de détails
4. Consulter le top pour confirmer

---

## 🎨 Design & UX

### Palette de Couleurs

**Backgrounds :**
- Primaire : Bleu très foncé (#0a0e27)
- Cartes : Bleu foncé (#232842)
- Hover : Légèrement plus clair

**Accents :**
- Principal : Violet (#6366f1)
- Succès : Vert (#10b981)
- Warning : Orange (#f59e0b)
- Danger : Rouge (#ef4444)

**Texte :**
- Primaire : Blanc cassé (#e8eaed)
- Secondaire : Gris clair (#9ca3af)
- Muted : Gris (#6b7280)

### Animations & Transitions

**Hover effects :**
- Cards : `transform: translateY(-4px)`
- Rank cards : `transform: translateX(4px)`
- Matrix cells : `transform: scale(1.05)`

**Durée :** 0.3s ease

### Responsive Design

**Desktop (>768px) :**
- Grilles 3-4 colonnes
- Navigation horizontale
- Charts côte à côte

**Mobile (≤768px) :**
- Grilles 1-2 colonnes
- Navigation simplifiée
- Charts empilés
- Tables scrollables

---

## 🔧 Personnalisation

### Changer les couleurs

Éditer [`css/styles.css`](frontend/css/styles.css) :

```css
:root {
    --accent-primary: #6366f1;  /* Modifier ici */
    --bg-card: #232842;         /* Modifier ici */
}
```

### Ajouter une nouvelle page

1. Créer `nouvelle-page.html`
2. Inclure les CSS/JS nécessaires
3. Ajouter le lien dans la navbar
4. Créer le JS correspondant

### Modifier le ranking

Ajuster les poids dans la vue SQL backend :
```sql
-- api/create_analytics_views.sql
(winrate * 0.35) +      -- 35% winrate
(kda * 10 * 0.25) +     -- 25% KDA
(dpm / 10 * 0.20) +     -- 20% DPM
...
```

---

## 🐛 Résolution de Problèmes

### Problème 1 : Page blanche

**Symptôme :** Page charge mais reste blanche

**Solution :**
1. Ouvrir console (F12)
2. Vérifier les erreurs JavaScript
3. Vérifier que l'API répond :
   ```
   curl http://127.0.0.1:8000/health
   ```

### Problème 2 : "Chargement..." infini

**Symptôme :** Loading ne se termine jamais

**Causes possibles :**
- API non lancée
- CORS bloqué
- Données vides en base

**Solutions :**
```bash
# 1. Vérifier l'API
curl http://127.0.0.1:8000/players

# 2. Vérifier les données
python check_data.py

# 3. Relancer avec serveur HTTP
cd frontend
python -m http.server 8080
```

### Problème 3 : Charts ne s'affichent pas

**Symptôme :** Espace vide à la place des graphiques

**Solution :**
Vérifier que Chart.js se charge :
```html
<!-- Dans <head> -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

### Problème 4 : Styles cassés

**Symptôme :** Mise en page désorganisée

**Solution :**
Vérifier les imports CSS :
```html
<link rel="stylesheet" href="css/styles.css">
```

Chemins relatifs corrects depuis chaque page.

### Problème 5 : Matrice DuoQ vide

**Symptôme :** Matrice affiche "Chargement..."

**Cause :** Pas assez de games en duo

**Solution :**
```bash
# Vérifier les duos
curl http://127.0.0.1:8000/duoq

# Ingérer plus de matchs
python ingest_all_players.py
```

---

## 📈 Performance

### Temps de chargement

| Page | Taille | Load Time |
|------|--------|-----------|
| Dashboard | ~15 KB | <500ms |
| Profil | ~18 KB | <600ms |
| Comparateur | ~16 KB | <550ms |
| DuoQ | ~14 KB | <500ms |

### Optimisations appliquées

- ✅ CSS minifié avec variables
- ✅ Pas de framework lourd
- ✅ Chart.js via CDN (cache navigateur)
- ✅ API calls optimisés (1 par page)
- ✅ Lazy loading des charts

---

## 🎯 Cas d'Usage

### 1. Identifier le meilleur joueur

**Méthode :**
1. Aller sur Dashboard
2. Regarder le classement interne
3. Analyser le score composite

**Interprétation :**
- Score > 60 : Excellent joueur
- Score 50-60 : Bon joueur
- Score < 50 : À améliorer

### 2. Trouver son meilleur champion

**Méthode :**
1. Cliquer sur son profil
2. Consulter le donut chart
3. Regarder le winrate dans la table

**Action :**
- Focus sur champions >60% WR
- Éviter champions <40% WR

### 3. Former un duo optimal

**Méthode :**
1. Aller sur Matrice DuoQ
2. Scanner les cellules vertes
3. Consulter le Top Synergies

**Décision :**
- Privilégier duos ≥70% WR
- Éviter duos <45% WR

### 4. Comparer deux joueurs

**Méthode :**
1. Aller sur Comparateur
2. Sélectionner les 2 joueurs
3. Analyser le radar chart

**Insights :**
- Zone plus grande = meilleur
- Axes faibles = points à travailler

---

## 🚀 Prochaines Améliorations

### Court terme
- [ ] Dark/Light mode toggle
- [ ] Recherche de joueur
- [ ] Filtres par période
- [ ] Export stats en PDF

### Moyen terme
- [ ] Animations CSS avancées
- [ ] Progressive Web App
- [ ] Offline mode
- [ ] Notifications push

### Long terme
- [ ] Migration React/Vue
- [ ] Backend GraphQL
- [ ] Real-time avec WebSockets
- [ ] Mobile app native

---

**Frontend opérationnel et prêt à l'emploi** ✅
