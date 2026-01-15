# Plan de Refactor – Validé le 2026-01-15

## Phase 1 – Nettoyage de la Racine
**Statut** : ✅ TERMINÉ (2026-01-15)
**Risque** : Faible

### Actions réalisées
- [x] Créer `tests/` et déplacer : test_db.py, test_api.py, test_api_live.py, test_views.py, test_filter.py
- [x] Déplacer vers `scripts/` : ingest_all_players.py, update_existing_matches.py, debug_db.py, reset_db.py
- [x] Consolider docs vers `docs/` (11 fichiers .md + DEMARRAGE_RAPIDE.txt)
- [x] Supprimer doublon `check_data.py`
- [x] Créer `bin/` pour les `.bat` Windows (4 fichiers)
- [x] Mettre à jour les chemins dans les .bat (`cd /d "%~dp0.."`)
- [x] Corriger les imports `sys.path` dans tests/ et scripts/

### Structure finale (racine)
```
lol-data/
├── README.md
├── requirements.txt
├── run_api.py
├── main.py
├── start.bat
├── api/
├── bin/
├── config/
├── db/
├── docs/
├── frontend/
├── riot/
├── scripts/
└── tests/
```

---

## Phase 2 – Structuration Backend
**Statut** : ✅ TERMINÉ (2026-01-15)
**Risque** : Moyen

### Actions réalisées
- [x] Créer `api/services/` avec 5 services :
  ```
  api/services/
  ├── __init__.py
  ├── player_service.py   (get_all, get_by_id, get_champions, get_stats_by_role, get_ranking, get_global_stats)
  ├── match_service.py    (get_recent)
  ├── duoq_service.py     (get_synergies)
  ├── item_service.py     (get_popular, get_by_player)
  └── update_service.py   (is_running, get_status, run_update)
  ```

- [x] Refactorer `main.py` : routes appellent services (plus de logique métier)
- [x] Corriger `sys.path` dans `api/database.py` (Path dynamique)
- [x] `UpdateService` utilise `try/finally` pour reset du flag (fix KNOWN_PITFALLS)

### Note
`pyproject.toml` non créé (optionnel) – les `sys.path.insert` restent nécessaires sans package installé

---

## Phase 3 – Organisation SQL
**Statut** : ✅ TERMINÉ (2026-01-15)
**Risque** : Faible

### Actions réalisées
- [x] Créer `db/schema/` et déplacer `SQL_LOL_DATA_DISCORD.sql`
- [x] Créer `db/views/` et déplacer les 3 fichiers SQL de vues analytiques
- [x] Créer `db/migrations/` et renommer les scripts :
  - `000_create_reference_tables.py`
  - `001_add_items_column.py`
- [x] Renommer `postgres.py` → `connection.py`
- [x] Mettre à jour 22 fichiers avec le nouvel import `db.connection`

### Structure finale db/
```
db/
├── connection.py
├── schema/
│   └── SQL_LOL_DATA_DISCORD.sql
├── views/
│   ├── create_analytics_views.sql
│   ├── create_analytics_views_patch_filtered.sql
│   └── create_player_items_view.sql
└── migrations/
    ├── 000_create_reference_tables.py
    └── 001_add_items_column.py
```

---

## Récapitulatif
| Phase | Statut | Description |
|-------|--------|-------------|
| Phase 1 | ✅ | Nettoyage racine |
| Phase 2 | ✅ | Structuration backend (services) |
| Phase 3 | ✅ | Organisation SQL |

**Refactor complet terminé le 2026-01-15.**
