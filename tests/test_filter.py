"""
Test du filtre : verifie que seuls les joueurs trackes sont inseres
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats
from config.players import TRACKED_PLAYERS, TRACKED_PUUIDS
from db.connection import get_connection

PUUID_TEST = "rFWCHHZRZA6WmzfkBofol2jN5BKoPD0S8CYwPr-gmRhnOx6oRmeRNELX-rCL-nB8fCbpjAHswbWQSw"

# Compter avant
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match")
count_avant = cur.fetchone()[0]
cur.close()
conn.close()

print(f"Stats en base AVANT test : {count_avant}\n")

# Traiter 1 match avec filtre active
match_ids = get_match_ids(PUUID_TEST, count=1)
match_id = match_ids[0]
match = get_match_detail(match_id)

print(f"Match a traiter : {match_id}")
print(f"Participants totaux : {len(match['info']['participants'])}")

# Compter combien sont trackes
tracked_count = sum(
    1 for p in match["info"]["participants"]
    if p["puuid"] in TRACKED_PUUIDS
)
print(f"Participants trackes : {tracked_count}\n")

# Ingestion avec filtre
insert_match(match)
insert_player_stats(match, tracked_only=True)

# Compter apres
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match")
count_apres = cur.fetchone()[0]
cur.close()
conn.close()

print(f"\nStats en base APRES test : {count_apres}")
print(f"Stats ajoutees : {count_apres - count_avant}")
print(f"Attendu : {tracked_count} (ou 0 si match deja en base)")

if count_apres - count_avant == 0:
    print("\nMatch deja en base -> ON CONFLICT a fonctionne")
elif count_apres - count_avant == tracked_count:
    print("\nFiltre fonctionne correctement !")
else:
    print("\nATTENTION : nombre inattendu de stats inserees")
