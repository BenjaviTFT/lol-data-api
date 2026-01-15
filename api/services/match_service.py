"""
Service pour la gestion des matchs
"""

from typing import List, Dict, Any
from api.database import execute_query


class MatchService:
    """Gestion des données de matchs"""

    @staticmethod
    def get_recent(limit: int = 20) -> List[Dict[str, Any]]:
        """Récupère les derniers matchs"""
        if limit > 100:
            limit = 100
        return execute_query(
            "SELECT * FROM riot_analytics.recent_matches LIMIT %s",
            (limit,)
        )
