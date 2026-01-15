"""
Met a jour les matchs existants pour ajouter les items
(sans tout reinitialiser)
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from db.connection import get_connection
from riot.riot_api import get_match_detail
import time

print("="*70)
print("MISE A JOUR DES MATCHS EXISTANTS AVEC ITEMS")
print("="*70)

conn = get_connection()
cur = conn.cursor()

# Recuperer tous les match_ids existants
cur.execute("SELECT match_id FROM riot_fact.match_game ORDER BY game_start DESC")
match_ids = [row[0] for row in cur.fetchall()]

print(f"\nMatchs a mettre a jour : {len(match_ids)}\n")

updated_count = 0
error_count = 0

for i, match_id in enumerate(match_ids, 1):
    try:
        print(f"[{i}/{len(match_ids)}] {match_id}...", end=" ")

        # Recuperer le detail du match
        match = get_match_detail(match_id)

        if match is None:
            print("ERREUR API")
            error_count += 1
            continue

        # Mettre a jour chaque participant
        for p in match["info"]["participants"]:
            items = [
                p.get("item0", 0),
                p.get("item1", 0),
                p.get("item2", 0),
                p.get("item3", 0),
                p.get("item4", 0),
                p.get("item5", 0),
                p.get("item6", 0)
            ]

            # UPDATE uniquement si le joueur est dans notre base
            cur.execute("""
                UPDATE riot_fact.fact_player_match
                SET items = %s
                WHERE match_id = %s
                  AND player_id = (SELECT player_id FROM riot_dim.dim_player WHERE puuid = %s)
            """, (items, match_id, p["puuid"]))

        conn.commit()
        updated_count += 1
        print("OK")

        # Rate limiting
        time.sleep(1.2)

    except Exception as e:
        print(f"ERREUR : {e}")
        error_count += 1
        continue

cur.close()
conn.close()

print("\n" + "="*70)
print("MISE A JOUR TERMINEE")
print("="*70)
print(f"Matchs mis a jour : {updated_count}")
print(f"Erreurs : {error_count}")
