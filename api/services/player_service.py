"""
Service pour la gestion des joueurs
"""

from typing import List, Dict, Any, Optional
from api.database import execute_query


class PlayerService:
    """Gestion des stats et données joueurs"""

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Récupère tous les joueurs avec leurs stats"""
        return execute_query("SELECT * FROM riot_analytics.player_stats")

    @staticmethod
    def get_by_id(player_id: int) -> Optional[Dict[str, Any]]:
        """Récupère les stats d'un joueur spécifique"""
        results = execute_query(
            "SELECT * FROM riot_analytics.player_stats WHERE player_id = %s",
            (player_id,)
        )
        return results[0] if results else None

    @staticmethod
    def get_champions(player_id: int) -> List[Dict[str, Any]]:
        """Récupère les champions joués par un joueur"""
        return execute_query(
            "SELECT * FROM riot_analytics.player_champions WHERE player_id = %s ORDER BY games_played DESC",
            (player_id,)
        )

    @staticmethod
    def get_stats_by_role(player_id: int) -> List[Dict[str, Any]]:
        """Récupère les stats par rôle d'un joueur"""
        return execute_query(
            "SELECT * FROM riot_analytics.player_stats_by_role WHERE player_id = %s ORDER BY games_played DESC",
            (player_id,)
        )

    @staticmethod
    def get_ranking() -> List[Dict[str, Any]]:
        """Récupère le classement interne"""
        return execute_query("SELECT * FROM riot_analytics.player_ranking")

    @staticmethod
    def get_global_stats() -> Dict[str, Any]:
        """Calcule les stats globales du groupe"""
        players = PlayerService.get_all()

        if not players:
            return {
                "total_players": 0,
                "total_games": 0,
                "total_wins": 0,
                "total_losses": 0,
                "avg_winrate": 0,
                "avg_kda": 0
            }

        total_games = sum(p["total_games"] for p in players)
        total_wins = sum(p["wins"] for p in players)
        avg_winrate = total_wins / total_games * 100 if total_games > 0 else 0

        return {
            "total_players": len(players),
            "total_games": total_games,
            "total_wins": total_wins,
            "total_losses": total_games - total_wins,
            "avg_winrate": round(avg_winrate, 1),
            "avg_kda": round(sum(p["kda_ratio"] for p in players) / len(players), 2)
        }
