"""
Verifie combien de matchs correspondent aux filtres appliques.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

def check_filtered():
    """Affiche les stats avec les filtres appliques."""
    conn = get_connection()
    cur = conn.cursor()

    print("="*70)
    print("DONNEES FILTREES : PATCH 16.1 + DATE >= 08/01/2026")
    print("="*70)
    print()

    # Matchs correspondant aux criteres
    cur.execute("""
        SELECT COUNT(*)
        FROM riot_fact.match_game
        WHERE patch_version LIKE '16.1%'
          AND game_start >= '2026-01-08 00:00:00'
    """)

    filtered_matches = cur.fetchone()[0]
    print(f"Matchs correspondants : {filtered_matches}")

    # Stats joueurs correspondantes
    cur.execute("""
        SELECT COUNT(*)
        FROM riot_fact.fact_player_match fpm
        JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
        WHERE mg.patch_version LIKE '16.1%'
          AND mg.game_start >= '2026-01-08 00:00:00'
    """)

    filtered_stats = cur.fetchone()[0]
    print(f"Stats joueurs correspondantes : {filtered_stats}")

    print()
    print("-"*70)
    print("REPARTITION PAR JOUR")
    print("-"*70)

    cur.execute("""
        SELECT
            DATE(mg.game_start) as game_date,
            COUNT(*) as nb_games
        FROM riot_fact.match_game mg
        WHERE mg.patch_version LIKE '16.1%'
          AND mg.game_start >= '2026-01-08 00:00:00'
        GROUP BY DATE(mg.game_start)
        ORDER BY game_date DESC
    """)

    for row in cur.fetchall():
        date, nb = row
        print(f"  {date}: {nb} matchs")

    print()
    print("-"*70)
    print("STATS PAR JOUEUR (vues filtrees)")
    print("-"*70)

    cur.execute("""
        SELECT
            display_name,
            total_games,
            winrate_pct,
            kda_ratio
        FROM riot_analytics.player_stats
        ORDER BY total_games DESC
    """)

    rows = cur.fetchall()
    if rows:
        for row in rows:
            name, games, wr, kda = row
            print(f"  {name:30} : {games:3} games | {wr:5.1f}% WR | {kda:4.2f} KDA")
    else:
        print("  AUCUN JOUEUR - Aucun match ne correspond aux filtres!")
        print("  Lance 'python ingest_all_players.py' pour charger des matchs recents.")

    print()
    print("="*70)

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_filtered()
