"""
Service pour la gestion des items
"""

from typing import List, Dict, Any
from api.database import execute_query


class ItemService:
    """Gestion des données d'items"""

    @staticmethod
    def get_popular(limit: int = 20) -> List[Dict[str, Any]]:
        """Récupère les items les plus populaires"""
        if limit > 50:
            limit = 50
        return execute_query(
            "SELECT * FROM riot_analytics.popular_items LIMIT %s",
            (limit,)
        )

    @staticmethod
    def get_by_player(player_id: int) -> List[Dict[str, Any]]:
        """Récupère les items utilisés par un joueur"""
        return execute_query(
            "SELECT * FROM riot_analytics.player_items WHERE player_id = %s ORDER BY times_bought DESC",
            (player_id,)
        )
