"""
Cree les tables de reference : dim_champion et dim_item
"""

import sys
sys.path.insert(0, '.')

from db.connection import get_connection

print("Creation des tables de reference...")

conn = get_connection()
cur = conn.cursor()

# Table dim_champion
cur.execute("""
    CREATE TABLE IF NOT EXISTS riot_dim.dim_champion (
        champion_id INT PRIMARY KEY,
        champion_name TEXT NOT NULL,
        champion_key TEXT NOT NULL,
        title TEXT
    );
""")

# Table dim_item
cur.execute("""
    CREATE TABLE IF NOT EXISTS riot_dim.dim_item (
        item_id INT PRIMARY KEY,
        item_name TEXT NOT NULL,
        description TEXT,
        total_gold INT,
        tags TEXT[]
    );
""")

conn.commit()
cur.close()
conn.close()

print("Tables dim_champion et dim_item creees avec succes")
