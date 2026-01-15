import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_connection

conn = get_connection()
cur = conn.cursor()

# Compter les matchs en base
cur.execute("SELECT COUNT(*) FROM riot_fact.match_game")
count_match = cur.fetchone()[0]
print(f"Nombre de matchs en base : {count_match}")

# Compter les stats joueurs
cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match")
count_stats = cur.fetchone()[0]
print(f"Nombre de stats joueurs : {count_stats}")

# Lister les match_ids
cur.execute("SELECT match_id FROM riot_fact.match_game ORDER BY game_start DESC LIMIT 10")
matches = cur.fetchall()
print(f"\nDerniers matchs en base :")
for m in matches:
    print(f"  - {m[0]}")

cur.close()
conn.close()
