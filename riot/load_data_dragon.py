"""
Charge les donnees statiques depuis Data Dragon API (champions + items)
"""

import sys
sys.path.insert(0, '.')

import requests
from db.connection import get_connection

# Version du patch (mettre a jour regulierement)
PATCH_VERSION = "14.1.1"

BASE_URL = f"https://ddragon.leagueoflegends.com/cdn/{PATCH_VERSION}/data/en_US"

print("="*70)
print("CHARGEMENT DATA DRAGON")
print("="*70)
print(f"Patch version : {PATCH_VERSION}\n")

# ========================================
# CHAMPIONS
# ========================================

print("Chargement des champions...")
response = requests.get(f"{BASE_URL}/champion.json")

if response.status_code != 200:
    print(f"Erreur API Data Dragon : {response.status_code}")
    exit(1)

data = response.json()
champions = data["data"]

conn = get_connection()
cur = conn.cursor()

# Truncate pour recharger proprement
cur.execute("TRUNCATE TABLE riot_dim.dim_champion")

count_champions = 0
for champ_key, champ_data in champions.items():
    cur.execute("""
        INSERT INTO riot_dim.dim_champion (champion_id, champion_name, champion_key, title)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (champion_id) DO UPDATE
        SET
            champion_name = EXCLUDED.champion_name,
            champion_key = EXCLUDED.champion_key,
            title = EXCLUDED.title
    """, (
        int(champ_data["key"]),
        champ_data["name"],
        champ_data["id"],
        champ_data["title"]
    ))
    count_champions += 1

conn.commit()
print(f"  -> {count_champions} champions charges\n")

# ========================================
# ITEMS
# ========================================

print("Chargement des items...")
response = requests.get(f"{BASE_URL}/item.json")

if response.status_code != 200:
    print(f"Erreur API Data Dragon : {response.status_code}")
    cur.close()
    conn.close()
    exit(1)

data = response.json()
items = data["data"]

# Truncate pour recharger proprement
cur.execute("TRUNCATE TABLE riot_dim.dim_item")

count_items = 0
for item_id, item_data in items.items():
    # Nettoyer description HTML
    description = item_data.get("plaintext", "") or item_data.get("description", "")

    cur.execute("""
        INSERT INTO riot_dim.dim_item (item_id, item_name, description, total_gold, tags)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (item_id) DO UPDATE
        SET
            item_name = EXCLUDED.item_name,
            description = EXCLUDED.description,
            total_gold = EXCLUDED.total_gold,
            tags = EXCLUDED.tags
    """, (
        int(item_id),
        item_data["name"],
        description[:500],  # Limiter la longueur
        item_data.get("gold", {}).get("total", 0),
        item_data.get("tags", [])
    ))
    count_items += 1

conn.commit()
print(f"  -> {count_items} items charges\n")

cur.close()
conn.close()

print("="*70)
print("CHARGEMENT TERMINE")
print("="*70)
print(f"Total champions : {count_champions}")
print(f"Total items : {count_items}")
