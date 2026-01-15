# 🚀 START HERE - Démarrage Ultra Rapide

## ⚡ Lancer le Projet en 2 Minutes

### Étape 1 : Backend (Terminal 1)

```bash
python run_api.py
```

✅ **Vérification :** http://127.0.0.1:8000/health

### Étape 2 : Frontend (Terminal 2)

```bash
cd frontend
python -m http.server 8080
```

✅ **Vérification :** http://localhost:8080

---

## 🎯 Accéder aux Pages

| Page | URL | Description |
|------|-----|-------------|
| 🏠 **Dashboard** | http://localhost:8080 | Ranking + Stats globales |
| 👤 **Profil** | Cliquer sur un joueur | Stats détaillées + graphiques |
| ⚖️ **Comparateur** | http://localhost:8080/comparator.html | Comparer 2 joueurs |
| 🤝 **DuoQ** | http://localhost:8080/duoq.html | Matrice des synergies |

---

## 📊 Ce que tu vas voir

### Dashboard
- 4 stats cards (Joueurs, Games, Winrate, KDA)
- Classement avec badges 🥇🥈🥉
- Grille de joueurs cliquables

### Profil Joueur
- Radar chart (6 axes de performance)
- Donut chart (top 5 champions)
- Table complète des champions
- Stats par rôle

### Comparateur
- Sélection 2 joueurs
- Radar superposé
- 10 métriques comparées
- Barres face-à-face

### Matrice DuoQ
- Grille interactive NxN
- Code couleur par winrate
- Top synergies
- Stats détaillées

---

## 🔧 Problème ?

### Backend ne démarre pas
```bash
pip install -r requirements.txt
```

### Frontend ne charge pas
Utilise un serveur HTTP, pas `file://`

### Données vides
```bash
python check_data.py
python ingest_all_players.py
```

---

## 📚 Documentation Complète

Pour plus de détails, consulte :

- **[QUICKSTART.md](QUICKSTART.md)** - Guide de démarrage
- **[FRONTEND_GUIDE.md](FRONTEND_GUIDE.md)** - Guide frontend détaillé
- **[PROJECT_COMPLETE.md](PROJECT_COMPLETE.md)** - Vue d'ensemble complète
- **[API_EXAMPLES.md](API_EXAMPLES.md)** - Exemples d'utilisation API

---

## ✅ Checklist Rapide

- [ ] API lancée (http://127.0.0.1:8000/health)
- [ ] Frontend lancé (http://localhost:8080)
- [ ] Dashboard affiche les données
- [ ] Profil joueur accessible
- [ ] Comparateur fonctionne
- [ ] Matrice DuoQ visible

**Si toutes les cases sont cochées → Projet opérationnel !** 🎉

---

**Version 1.0.0** | **Production Ready** ✅
