"""
Service pour la gestion des synergies DuoQ
"""

from typing import List, Dict, Any
from api.database import execute_query


class DuoQService:
    """Gestion des données de synergies DuoQ"""

    @staticmethod
    def get_synergies() -> List[Dict[str, Any]]:
        """Récupère toutes les synergies DuoQ"""
        return execute_query(
            "SELECT * FROM riot_analytics.duoq_synergies ORDER BY games_together DESC"
        )
