"""
RESET de la base de donnees (ATTENTION : supprime toutes les donnees)
"""

from db.connection import get_connection

print("="*70)
print("RESET DE LA BASE DE DONNEES")
print("="*70)
print("\nATTENTION : Cette action va supprimer toutes les donnees existantes.")

response = input("\nTaper 'CONFIRMER' pour continuer : ")

if response != "CONFIRMER":
    print("\nAnnulation - aucune donnee supprimee")
    exit(0)

print("\nSuppression en cours...")

conn = get_connection()
cur = conn.cursor()

# Supprimer les donnees (pas les tables)
cur.execute("TRUNCATE TABLE riot_fact.fact_player_match CASCADE")
cur.execute("TRUNCATE TABLE riot_fact.match_game CASCADE")
cur.execute("TRUNCATE TABLE riot_dim.dim_player RESTART IDENTITY CASCADE")

conn.commit()
cur.close()
conn.close()

print("\nBase de donnees resetee avec succes")
print("Toutes les tables sont vides et pretes pour une nouvelle ingestion")
