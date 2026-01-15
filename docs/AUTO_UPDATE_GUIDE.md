# Guide d'Auto-Update - Mise à Jour Automatique

Ce guide explique les 3 systèmes de mise à jour automatique mis en place.

---

## 🎯 Objectif

**Plus besoin de lancer manuellement les mises à jour !** Le système détecte et ajoute automatiquement les nouveaux matchs.

---

## ✅ 3 Systèmes d'Auto-Update

### 1. **Auto-Update au Chargement de Page** (Recommandé)

**Comment ça marche :**
- Quand tu ouvres le site (http://localhost:8080), une mise à jour se déclenche automatiquement
- Les nouveaux matchs sont détectés et ajoutés
- Les données se rafraîchissent toutes les 10 minutes tant que la page est ouverte

**Avantages :**
- ✅ Totalement transparent
- ✅ Aucune action manuelle requise
- ✅ Les données sont toujours fraîches

**Fonctionnement technique :**
```javascript
// Dans frontend/js/dashboard.js
document.addEventListener('DOMContentLoaded', async () => {
    await triggerAutoUpdate();  // Mise à jour au chargement

    // Mise à jour toutes les 10 minutes
    setInterval(async () => {
        await triggerAutoUpdate();
        await refreshAllData();
    }, 10 * 60 * 1000);
});
```

**Endpoint API :**
```
POST http://localhost:8000/update
GET  http://localhost:8000/update/status
```

---

### 2. **Service Standalone (Optionnel)**

**Quand l'utiliser :**
- Si tu veux que les mises à jour se fassent même quand le site n'est pas ouvert
- Pour un serveur qui tourne 24/7

**Démarrage :**
- Double-clic sur `start_auto_update.bat`
- Ou : `python scripts/auto_update_service.py`

**Arrêt :**
- Appuie sur `Ctrl+C` dans la fenêtre

**Avantages :**
- ✅ Fonctionne en arrière-plan
- ✅ Indépendant du site web
- ✅ Logs en temps réel

**Inconvénients :**
- ⚠️ Une fenêtre doit rester ouverte
- ⚠️ Redondant avec le système #1

---

### 3. **Mise à Jour Manuelle (Fallback)**

Si besoin de forcer une mise à jour :

**Option A : Batch file**
```bash
update.bat  # Double-clic
```

**Option B : Script Python**
```bash
python scripts/update_matches.py
```

---

## 🔍 Vérifier le Statut

### Via l'API

```bash
curl http://localhost:8000/update/status
```

Retourne :
```json
{
  "last_update": "2026-01-14T23:45:12",
  "update_in_progress": false
}
```

### Via les logs

Ouvre la console du navigateur (F12) :
```
Auto-update: {status: "started", message: "Mise a jour demarree en arriere-plan"}
```

---

## ⚙️ Configuration

### Intervalle de Mise à Jour

**Frontend (dashboard.js) :**
```javascript
setInterval(async () => {
    await triggerAutoUpdate();
    await refreshAllData();
}, 10 * 60 * 1000);  // 10 minutes (modifiable)
```

**Service Standalone (auto_update_service.py) :**
```python
UPDATE_INTERVAL = 600  # 10 minutes en secondes (modifiable)
```

### Nombre de Matchs Vérifiés

Par défaut, le système vérifie les **20 derniers matchs** de chaque joueur.

Pour modifier :
```python
# Dans api/main.py, ligne 178
match_ids = get_match_ids(puuid, count=20)  # Changer 20

# Dans scripts/update_matches.py, ligne 37
match_ids = get_match_ids(puuid, count=20)  # Changer 20
```

---

## 📊 Filtres Appliqués

Les données affichées sont filtrées sur :

### 1. Patch 16.1
```sql
WHERE mg.patch_version LIKE '16.1%'
```

### 2. Date >= 08/01/2026
```sql
AND mg.game_start >= '2026-01-08 00:00:00'
```

**Résultat :** Seuls les matchs du patch 16.1 joués depuis le 08/01/2026 apparaissent sur le site.

---

## 🚀 Workflow Recommandé

### Démarrage du Système

```bash
# Terminal 1 : Backend API
python api/main.py

# Terminal 2 : Frontend
cd frontend
python -m http.server 8080
```

### Utilisation

1. Ouvre le site : http://localhost:8080
2. La mise à jour se déclenche automatiquement
3. Les données se rafraîchissent toutes les 10 min
4. **C'est tout !** Plus rien à faire manuellement

### Si tu veux forcer une mise à jour

- Rafraîchis la page (F5 ou Ctrl+R)
- Ou lance `update.bat`

---

## 📈 Performances

### Temps de Mise à Jour

- **1 joueur, 20 matchs** : ~10 secondes
- **7 joueurs, 20 matchs** : ~30 secondes
- **En arrière-plan** : N'impacte pas la navigation

### Consommation API Riot

- **Delay entre appels** : 0.5s (2 req/s)
- **Limite Riot** : 20 req/s (EUW)
- **Sécurité** : Large marge, aucun risque de rate limit

---

## 🛠️ Dépannage

### La mise à jour ne se déclenche pas

1. **Vérifie que l'API tourne :**
   ```bash
   curl http://localhost:8000/health
   ```
   Doit retourner : `{"status": "healthy"}`

2. **Vérifie les logs du navigateur (F12) :**
   - Cherche "Auto-update" dans la console
   - S'il y a une erreur, elle apparaîtra ici

3. **Vérifie la clé API Riot :**
   ```bash
   # Dans config/.env
   RIOT_API_KEY=RGAPI-xxxxx
   ```

### "Update already running"

Une mise à jour est déjà en cours. Attends 30 secondes et réessaye.

### Aucun nouveau match détecté

C'est normal ! Le système ne trouve que les matchs qui n'existent pas déjà en base.

Si tes collègues ont joué :
- Attends que la mise à jour auto se déclenche (max 10 min)
- Ou rafraîchis la page (F5)

---

## 📝 Changement de Patch (Futur)

Quand le patch 16.2 sortira :

1. **Modifier le filtre SQL :**
   ```bash
   # Ouvrir db/create_analytics_views_patch_filtered.sql
   # Remplacer '16.1%' par '16.2%'
   # Remplacer '2026-01-08' par la date du patch 16.2
   ```

2. **Appliquer les changements :**
   ```bash
   python scripts/apply_patch_filter.py
   ```

3. **Les mises à jour auto continueront de fonctionner**

---

## 🎯 Résumé

| Méthode | Automatique | Fréquence | Recommandé |
|---------|-------------|-----------|------------|
| **Auto-update page** | ✅ Oui | Au chargement + toutes les 10 min | ✅ **OUI** |
| **Service standalone** | ✅ Oui | Toutes les 10 min | ⚠️ Optionnel |
| **update.bat** | ❌ Non | Manuel | ⚠️ Fallback uniquement |

**Configuration recommandée :**
- ✅ Utilise l'auto-update intégré au site (système #1)
- ✅ Laisse la page ouverte en arrière-plan si possible
- ✅ Lance le service standalone uniquement si tu veux un système 24/7

---

**Tout est automatisé ! Plus besoin de penser aux mises à jour.** 🚀
