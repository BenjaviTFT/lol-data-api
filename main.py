"""
API FastAPI pour League of Legends Analytics
"""

import sys
from pathlib import Path

# Ajouter le repertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List

from api.models import (
    PlayerStats,
    PlayerChampion,
    DuoQSynergy,
    PlayerRanking,
    RecentMatch,
    PlayerStatsByRole,
    PopularItem,
    PlayerItem
)
from api.services import (
    PlayerService,
    MatchService,
    DuoQService,
    ItemService,
    UpdateService
)

# ============================================================
# CONFIGURATION
# ============================================================

app = FastAPI(
    title="LoL Analytics API",
    description="API privee pour l'analyse des performances League of Legends",
    version="1.0.0"
)

# CORS (a restreindre en production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# ENDPOINTS - PLAYERS
# ============================================================

@app.get("/")
def root():
    """Endpoint racine"""
    return {
        "message": "LoL Analytics API",
        "version": "1.0.0",
        "endpoints": {
            "players": "/players",
            "ranking": "/ranking",
            "duoq": "/duoq",
            "recent_matches": "/matches/recent",
            "items_popular": "/items/popular",
            "player_items": "/players/{id}/items"
        }
    }


@app.get("/players", response_model=List[PlayerStats])
def get_players():
    """Recupere tous les joueurs avec leurs stats"""
    return PlayerService.get_all()


@app.get("/players/{player_id}", response_model=PlayerStats)
def get_player(player_id: int):
    """Recupere les stats d'un joueur specifique"""
    player = PlayerService.get_by_id(player_id)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.get("/players/{player_id}/champions", response_model=List[PlayerChampion])
def get_player_champions(player_id: int):
    """Recupere les champions joues par un joueur"""
    return PlayerService.get_champions(player_id)


@app.get("/players/{player_id}/roles", response_model=List[PlayerStatsByRole])
def get_player_roles(player_id: int):
    """Recupere les stats par role d'un joueur"""
    return PlayerService.get_stats_by_role(player_id)


@app.get("/ranking", response_model=List[PlayerRanking])
def get_ranking():
    """Recupere le classement interne"""
    return PlayerService.get_ranking()


# ============================================================
# ENDPOINTS - MATCHES
# ============================================================

@app.get("/matches/recent", response_model=List[RecentMatch])
def get_recent_matches(limit: int = 20):
    """Recupere les derniers matchs"""
    return MatchService.get_recent(limit)


# ============================================================
# ENDPOINTS - DUOQ
# ============================================================

@app.get("/duoq", response_model=List[DuoQSynergy])
def get_duoq():
    """Recupere les synergies DuoQ"""
    return DuoQService.get_synergies()


# ============================================================
# ENDPOINTS - ITEMS
# ============================================================

@app.get("/items/popular", response_model=List[PopularItem])
def get_popular_items(limit: int = 20):
    """Recupere les items les plus populaires"""
    return ItemService.get_popular(limit)


@app.get("/players/{player_id}/items", response_model=List[PlayerItem])
def get_player_items(player_id: int):
    """Recupere les items utilises par un joueur"""
    return ItemService.get_by_player(player_id)


# ============================================================
# ENDPOINTS - STATS GLOBALES
# ============================================================

@app.get("/stats/global")
def get_global_stats():
    """Stats globales du groupe"""
    return PlayerService.get_global_stats()


# ============================================================
# ENDPOINTS - HEALTH & UPDATE
# ============================================================

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/update")
async def trigger_update(background_tasks: BackgroundTasks):
    """
    Declenche une mise a jour incrementale des matchs.
    S'execute en arriere-plan pour ne pas bloquer la requete.
    """
    if UpdateService.is_running():
        return {
            "status": "already_running",
            "message": "Une mise a jour est deja en cours"
        }

    background_tasks.add_task(UpdateService.run_update)

    return {
        "status": "started",
        "message": "Mise a jour demarree en arriere-plan"
    }


@app.get("/update/status")
def get_update_status():
    """Recupere le statut de la derniere mise a jour."""
    return UpdateService.get_status()


# Servir le frontend (DOIT être après toutes les routes API)
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
