"""
Service pour la gestion des items
"""

from typing import List, Dict, Any
from api.database import execute_query


class ItemService:
    """Gestion des donnees d'items"""

    @staticmethod
    def get_popular(limit: int = 20) -> List[Dict[str, Any]]:
        """Recupere les items les plus populaires"""
        if limit > 50:
            limit = 50
        return execute_query(
            "SELECT * FROM riot_analytics.popular_items LIMIT %s",
            (limit,)
        )

    @staticmethod
    def get_by_player(player_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Recupere les items utilises par un joueur"""
        return execute_query(
            "SELECT * FROM riot_analytics.player_items WHERE player_id = %s ORDER BY times_bought DESC LIMIT %s",
            (player_id, limit)
        )

    @staticmethod
    def get_by_player_champion(player_id: int, champion_id: int) -> List[Dict[str, Any]]:
        """Recupere les items utilises par un joueur sur un champion specifique"""
        return execute_query(
            """
            SELECT item_id, item_name, times_bought, winrate_with_item
            FROM riot_analytics.player_champion_items
            WHERE player_id = %s AND champion_id = %s
            ORDER BY times_bought DESC
            LIMIT 6
            """,
            (player_id, champion_id)
        )

    @staticmethod
    def get_champion_builds(player_id: int) -> List[Dict[str, Any]]:
        """Recupere les top items pour chaque champion joue par un joueur"""
        return execute_query(
            """
            SELECT DISTINCT ON (champion_id)
                champion_id, champion_name, item_id, item_name, times_bought, winrate_with_item
            FROM riot_analytics.player_champion_items
            WHERE player_id = %s
            ORDER BY champion_id, times_bought DESC
            """,
            (player_id,)
        )
