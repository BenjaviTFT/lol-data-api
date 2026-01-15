"""
Service pour la gestion des mises à jour automatiques
"""

import time
from datetime import datetime
from typing import Dict, Any

from db.connection import get_connection
from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats
from config.players import TRACKED_PLAYERS


class UpdateService:
    """Gestion des mises à jour de données depuis l'API Riot"""

    # État global du service
    _last_update_time = None
    _update_in_progress = False

    @classmethod
    def is_running(cls) -> bool:
        """Vérifie si une mise à jour est en cours"""
        return cls._update_in_progress

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        """Récupère le statut de la dernière mise à jour"""
        return {
            "last_update": cls._last_update_time.isoformat() if cls._last_update_time else None,
            "update_in_progress": cls._update_in_progress
        }

    @classmethod
    def _get_existing_match_ids(cls) -> set:
        """Récupère tous les match_ids déjà en base"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT match_id FROM riot_fact.match_game")
        existing_ids = {row[0] for row in cur.fetchall()}
        cur.close()
        conn.close()
        return existing_ids

    @classmethod
    def run_update(cls) -> Dict[str, Any]:
        """
        Exécute une mise à jour incrémentale.
        IMPORTANT: Utilise try/finally pour garantir le reset du flag.
        """
        if cls._update_in_progress:
            return {"status": "already_running"}

        cls._update_in_progress = True
        start_time = time.time()

        try:
            existing_ids = cls._get_existing_match_ids()
            total_nouveaux = 0
            DELAY_API = 0.5

            for name, puuid in TRACKED_PLAYERS.items():
                try:
                    match_ids = get_match_ids(puuid, count=20)

                    for match_id in match_ids:
                        if match_id in existing_ids:
                            continue

                        match = get_match_detail(match_id)
                        if match is None:
                            continue

                        insert_match(match)
                        insert_player_stats(match, tracked_only=True)
                        existing_ids.add(match_id)
                        total_nouveaux += 1

                        time.sleep(DELAY_API)

                except Exception as e:
                    print(f"Erreur sur {name}: {e}")
                    continue

            duration = time.time() - start_time
            cls._last_update_time = datetime.now()

            return {
                "status": "completed",
                "new_matches": total_nouveaux,
                "duration_seconds": round(duration, 1),
                "timestamp": cls._last_update_time.isoformat()
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

        finally:
            # CRITIQUE: Toujours reset le flag, même en cas d'erreur
            cls._update_in_progress = False
