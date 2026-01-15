"""
Affiche tous les joueurs de la base avec leur vrai summoner_name
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

def check_all():
    conn = get_connection()
    cur = conn.cursor()

    print("="*70)
    print("TOUS LES JOUEURS EN BASE")
    print("="*70)
    print()

    cur.execute("""
        SELECT
            player_id,
            summoner_name,
            tag_line,
            puuid
        FROM riot_dim.dim_player
        ORDER BY summoner_name
    """)

    for row in cur.fetchall():
        player_id, summoner, tag, puuid = row
        print(f"ID: {player_id:3} | {summoner:20} | #{tag:10} | PUUID: {puuid[:40]}...")

    print()
    print("="*70)

    cur.close()
    conn.close()

if __name__ == "__main__":
    check_all()
