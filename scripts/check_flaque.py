"""
Verifie specifiquement FlaqueDepisse
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection

puuid = "4-hnAlOAhFA_vOEVDdPOb_fB1LhFgEBW4HXqacZtEMNqnMN9JK7dUlQ3fbl0rxWHR6FK9bNoWRxuQA"

conn = get_connection()
cur = conn.cursor()

print("Verification FlaqueDepisse")
print("="*70)

# Verifier dans dim_player
cur.execute("SELECT player_id, summoner_name, tag_line FROM riot_dim.dim_player WHERE puuid = %s", (puuid,))
player = cur.fetchone()

if not player:
    print("JOUEUR INTROUVABLE dans dim_player!")
else:
    player_id, name, tag = player
    print(f"Joueur trouve: {name}#{tag} (ID: {player_id})")

    # Total matchs
    cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match WHERE player_id = %s", (player_id,))
    total = cur.fetchone()[0]
    print(f"Total matchs (tous): {total}")

    # Matchs filtres
    cur.execute("""
        SELECT COUNT(*)
        FROM riot_fact.fact_player_match fpm
        JOIN riot_fact.match_game mg ON fpm.match_id = mg.match_id
        WHERE fpm.player_id = %s
          AND mg.patch_version LIKE '16.1%'
          AND mg.game_start >= '2026-01-08 00:00:00'
    """, (player_id,))
    filtered = cur.fetchone()[0]
    print(f"Matchs filtres (patch 16.1 + >= 08/01): {filtered}")

    if filtered == 0:
        print("\nATTENTION: 0 matchs dans la periode filtree!")
        print("Le joueur a joue mais pas dans la bonne periode.")

cur.close()
conn.close()
