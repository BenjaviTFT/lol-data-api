"""
Ajoute la colonne items a fact_player_match
"""

from db.connection import get_connection

print("Ajout de la colonne items...")

conn = get_connection()
cur = conn.cursor()

# Ajouter colonne items (array d'entiers)
cur.execute("""
    ALTER TABLE riot_fact.fact_player_match
    ADD COLUMN IF NOT EXISTS items INT[] DEFAULT ARRAY[0,0,0,0,0,0,0];
""")

conn.commit()
cur.close()
conn.close()

print("Colonne items ajoutee avec succes")
