"""
Database queries pour l'API
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection
from typing import List, Dict, Any


def execute_query(query: str, params: tuple = None) -> List[Dict[str, Any]]:
    """
    Execute une requete SQL et retourne les resultats en dict
    """
    conn = get_connection()
    cur = conn.cursor()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    columns = [desc[0] for desc in cur.description]
    results = []

    for row in cur.fetchall():
        results.append(dict(zip(columns, row)))

    cur.close()
    conn.close()

    return results


def get_all_players() -> List[Dict]:
    """Recupere tous les joueurs avec leurs stats"""
    return execute_query("SELECT * FROM riot_analytics.player_stats")


def get_player_by_id(player_id: int) -> Dict:
    """Recupere les stats d'un joueur specifique"""
    results = execute_query(
        "SELECT * FROM riot_analytics.player_stats WHERE player_id = %s",
        (player_id,)
    )
    return results[0] if results else None


def get_player_champions(player_id: int) -> List[Dict]:
    """Recupere les champions joues par un joueur"""
    return execute_query(
        "SELECT * FROM riot_analytics.player_champions WHERE player_id = %s ORDER BY games_played DESC",
        (player_id,)
    )


def get_duoq_synergies() -> List[Dict]:
    """Recupere toutes les synergies DuoQ"""
    return execute_query("SELECT * FROM riot_analytics.duoq_synergies ORDER BY games_together DESC")


def get_player_ranking() -> List[Dict]:
    """Recupere le classement interne"""
    return execute_query("SELECT * FROM riot_analytics.player_ranking")


def get_recent_matches(limit: int = 20) -> List[Dict]:
    """Recupere les derniers matchs"""
    return execute_query(
        "SELECT * FROM riot_analytics.recent_matches LIMIT %s",
        (limit,)
    )


def get_player_stats_by_role(player_id: int) -> List[Dict]:
    """Recupere les stats par role d'un joueur"""
    return execute_query(
        "SELECT * FROM riot_analytics.player_stats_by_role WHERE player_id = %s ORDER BY games_played DESC",
        (player_id,)
    )


def get_popular_items(limit: int = 20) -> List[Dict]:
    """Recupere les items les plus populaires"""
    return execute_query(
        "SELECT * FROM riot_analytics.popular_items LIMIT %s",
        (limit,)
    )


def get_player_items(player_id: int) -> List[Dict]:
    """Recupere les items utilises par un joueur"""
    return execute_query(
        "SELECT * FROM riot_analytics.player_items WHERE player_id = %s ORDER BY times_bought DESC",
        (player_id,)
    )
