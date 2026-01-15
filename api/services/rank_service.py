"""
Service pour la gestion des rangs ranked
"""

import time
from typing import List, Dict, Any, Optional
from api.database import execute_query

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from riot.riot_api import get_player_rank
from config.players import TRACKED_PLAYERS


# Ordre des tiers pour le tri
TIER_ORDER = {
    "CHALLENGER": 9,
    "GRANDMASTER": 8,
    "MASTER": 7,
    "DIAMOND": 6,
    "EMERALD": 5,
    "PLATINUM": 4,
    "GOLD": 3,
    "SILVER": 2,
    "BRONZE": 1,
    "IRON": 0
}

RANK_ORDER = {
    "I": 4,
    "II": 3,
    "III": 2,
    "IV": 1
}


def calculate_rank_score(tier: str, rank: str, lp: int) -> int:
    """
    Calcule un score numerique pour le classement
    Ex: Diamond I 75LP = 6*400 + 4*100 + 75 = 2875
    """
    tier_value = TIER_ORDER.get(tier, 0) * 400
    rank_value = RANK_ORDER.get(rank, 0) * 100
    return tier_value + rank_value + lp


class RankService:
    """Gestion des rangs ranked des joueurs"""

    @staticmethod
    def get_all_ranks() -> List[Dict[str, Any]]:
        """
        Recupere les rangs de tous les joueurs tracked
        Retourne une liste triee par rang (du plus haut au plus bas)
        """
        try:
            # Recuperer les player_id et display_name depuis la base
            players_db = execute_query("""
                SELECT player_id, summoner_name as display_name, puuid
                FROM riot_dim.dim_player
                WHERE puuid IS NOT NULL
            """)
        except Exception as e:
            print(f"Erreur requete DB: {e}")
            return []

        results = []

        for player in players_db:
            puuid = player.get("puuid")
            if not puuid:
                continue

            try:
                # Determiner la region (par defaut EUW)
                region = "euw1"
                # Pour les joueurs KR/JP, adapter la region
                if "KRJPN" in str(player.get("display_name", "")):
                    region = "kr"

                rank_data = get_player_rank(puuid, region)

                if rank_data:
                    score = calculate_rank_score(
                        rank_data["tier"],
                        rank_data["rank"],
                        rank_data["lp"]
                    )
                    results.append({
                        "player_id": player["player_id"],
                        "display_name": player["display_name"],
                        "tier": rank_data["tier"],
                        "rank": rank_data["rank"],
                        "lp": rank_data["lp"],
                        "wins": rank_data["wins"],
                        "losses": rank_data["losses"],
                        "winrate": round(rank_data["wins"] / (rank_data["wins"] + rank_data["losses"]) * 100, 1) if (rank_data["wins"] + rank_data["losses"]) > 0 else 0,
                        "score": score
                    })
                else:
                    # Joueur sans rang (unranked)
                    results.append({
                        "player_id": player["player_id"],
                        "display_name": player["display_name"],
                        "tier": "UNRANKED",
                        "rank": "",
                        "lp": 0,
                        "wins": 0,
                        "losses": 0,
                        "winrate": 0.0,
                        "score": -1
                    })
            except Exception as e:
                print(f"Erreur pour joueur {player.get('display_name')}: {e}")
                # Ajouter comme unranked en cas d'erreur
                results.append({
                    "player_id": player["player_id"],
                    "display_name": player["display_name"],
                    "tier": "UNRANKED",
                    "rank": "",
                    "lp": 0,
                    "wins": 0,
                    "losses": 0,
                    "winrate": 0.0,
                    "score": -1
                })

            # Rate limit: 0.5s entre chaque appel
            time.sleep(0.5)

        # Trier par score decroissant
        results.sort(key=lambda x: x["score"], reverse=True)

        # Ajouter le classement
        for i, player in enumerate(results, 1):
            player["position"] = i

        return results

    @staticmethod
    def get_player_rank(player_id: int) -> Optional[Dict[str, Any]]:
        """
        Recupere le rang d'un joueur specifique
        """
        player = execute_query(
            "SELECT puuid FROM riot_dim.dim_player WHERE player_id = %s",
            (player_id,)
        )

        if not player or not player[0].get("puuid"):
            return None

        return get_player_rank(player[0]["puuid"])
