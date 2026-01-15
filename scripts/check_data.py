"""
Script pour verifier l'etat actuel des donnees dans la base.
Affiche les stats par patch et par joueur.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

def check_data():
    """Affiche un resume des donnees en base."""
    conn = get_connection()
    cur = conn.cursor()

    print("="*70)
    print("ETAT DES DONNEES - RIOT DB")
    print("="*70)
    print()

    # Total matchs
    cur.execute("SELECT COUNT(*) FROM riot_fact.match_game")
    total_matches = cur.fetchone()[0]
    print(f"Total matchs en base : {total_matches}")

    # Total stats joueurs
    cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match")
    total_stats = cur.fetchone()[0]
    print(f"Total stats joueurs : {total_stats}")

    print()
    print("-"*70)
    print("REPARTITION PAR PATCH")
    print("-"*70)

    cur.execute("""
        SELECT
            patch_version,
            COUNT(*) as nb_matchs,
            MIN(game_start) as first_game,
            MAX(game_start) as last_game
        FROM riot_fact.match_game
        GROUP BY patch_version
        ORDER BY patch_version DESC
    """)

    for row in cur.fetchall():
        patch, nb, first, last = row
        print(f"{patch:8} : {nb:4} matchs  (du {first.strftime('%Y-%m-%d')} au {last.strftime('%Y-%m-%d')})")

    print()
    print("-"*70)
    print("STATS PAR JOUEUR (tous patchs)")
    print("-"*70)

    cur.execute("""
        SELECT
            dp.summoner_name || '#' || dp.tag_line as display_name,
            COUNT(*) as total_games
        FROM riot_fact.fact_player_match fpm
        JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
        GROUP BY dp.summoner_name, dp.tag_line
        ORDER BY total_games DESC
    """)

    for row in cur.fetchall():
        name, games = row
        print(f"{name:30} : {games:4} games")

    print()
    print("-"*70)
    print("STATS PATCH 16.1 UNIQUEMENT")
    print("-"*70)

    cur.execute("""
        SELECT
            dp.summoner_name || '#' || dp.tag_line as display_name,
            COUNT(*) as total_games
        FROM riot_fact.fact_player_match fpm
        JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
        JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
        WHERE mg.patch_version LIKE '16.1%'
        GROUP BY dp.summoner_name, dp.tag_line
        ORDER BY total_games DESC
    """)

    rows = cur.fetchall()
    if rows:
        for row in rows:
            name, games = row
            print(f"{name:30} : {games:4} games")
    else:
        print("ATTENTION : Aucun match sur le patch 16.1 !")
        print("Lance 'python ingest_all_players.py' pour charger des matchs recents.")

    print()
    print("="*70)

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_data()
