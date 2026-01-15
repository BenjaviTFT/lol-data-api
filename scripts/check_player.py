"""
Verifie si un joueur specifique a des donnees en base.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

def check_player_by_puuid(puuid):
    """Verifie les donnees d'un joueur par son PUUID."""
    conn = get_connection()
    cur = conn.cursor()

    print("="*70)
    print("VERIFICATION DU JOUEUR")
    print("="*70)
    print(f"PUUID: {puuid}")
    print()

    # Verifier si le joueur existe dans dim_player
    cur.execute("""
        SELECT player_id, summoner_name, tag_line
        FROM riot_dim.dim_player
        WHERE puuid = %s
    """, (puuid,))

    player = cur.fetchone()

    if player:
        player_id, summoner_name, tag_line = player
        print(f"Joueur trouve dans dim_player:")
        print(f"  ID: {player_id}")
        print(f"  Nom: {summoner_name}#{tag_line}")
        print()

        # Compter ses matchs
        cur.execute("""
            SELECT COUNT(*)
            FROM riot_fact.fact_player_match
            WHERE player_id = %s
        """, (player_id,))

        match_count = cur.fetchone()[0]
        print(f"Nombre de matchs: {match_count}")

        if match_count > 0:
            # Details par patch
            cur.execute("""
                SELECT
                    mg.patch_version,
                    COUNT(*) as nb_games
                FROM riot_fact.fact_player_match fpm
                JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
                WHERE fpm.player_id = %s
                GROUP BY mg.patch_version
                ORDER BY mg.patch_version DESC
            """, (player_id,))

            print("\nRepartition par patch:")
            for row in cur.fetchall():
                patch, nb = row
                print(f"  {patch}: {nb} games")

            # Dates
            cur.execute("""
                SELECT
                    MIN(mg.game_start) as first_game,
                    MAX(mg.game_start) as last_game
                FROM riot_fact.fact_player_match fpm
                JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
                WHERE fpm.player_id = %s
            """, (player_id,))

            first, last = cur.fetchone()
            print(f"\nPremiere game: {first.strftime('%Y-%m-%d %H:%M')}")
            print(f"Derniere game: {last.strftime('%Y-%m-%d %H:%M')}")
        else:
            print("\nATTENTION: Le joueur existe mais n'a AUCUN match en base!")
            print("Lance 'python ingest_all_players.py' pour charger ses matchs.")
    else:
        print("ATTENTION: Ce joueur n'existe PAS dans dim_player!")
        print("Il n'a jamais ete vu dans un match.")
        print("\nLance 'python ingest_all_players.py' pour le decouvrir.")

    print("="*70)

    cur.close()
    conn.close()

if __name__ == "__main__":
    puuid = "4-hnAlOAhFA_vOEVDdPOb_fB1LhFgEBW4HXqacZtEMNqnMN9JK7dUlQ3fbl0rxWHR6FK9bNoWRxuQA"
    check_player_by_puuid(puuid)
