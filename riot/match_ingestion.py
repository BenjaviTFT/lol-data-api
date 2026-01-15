print(">>> MATCH_INGESTION FILE LOADED <<<")

from db.connection import get_connection
from config.players import TRACKED_PUUIDS

def ensure_fact_player_match_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS riot_fact;

        CREATE TABLE IF NOT EXISTS riot_fact.fact_player_match (
            match_id TEXT,
            player_id INT,
            champion_id INT,

            win BOOLEAN,
            kills INT,
            deaths INT,
            assists INT,

            total_cs INT,
            cs_per_min FLOAT,
            gold_earned INT,
            gold_per_min FLOAT,

            damage_to_champions INT,
            damage_per_min FLOAT,

            role TEXT,
            position TEXT,
            vision_score INT,

            game_duration INT,

            PRIMARY KEY (match_id, player_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def ensure_match_game_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS riot_fact;

        CREATE TABLE IF NOT EXISTS riot_fact.match_game (
            match_id TEXT PRIMARY KEY,
            queue_id INT,
            game_duration INT,
            game_start TIMESTAMP,
            patch_version TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def ensure_dim_player_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE SCHEMA IF NOT EXISTS riot_dim;

        CREATE TABLE IF NOT EXISTS riot_dim.dim_player (
            player_id SERIAL PRIMARY KEY,
            summoner_name TEXT NOT NULL,
            tag_line TEXT NOT NULL,
            puuid TEXT UNIQUE NOT NULL,
            region TEXT DEFAULT 'EUW'
        );
    """)

    conn.commit()
    cur.close()
    conn.close()



def insert_match(match):
    ensure_match_game_table()

    conn = get_connection()
    cur = conn.cursor()

   
    info = match["info"]
    metadata = match["metadata"]

    cur.execute("""
        INSERT INTO riot_fact.match_game (
            match_id,
            queue_id,
            game_duration,
            game_start,
            patch_version
        )
        VALUES (%s, %s, %s, to_timestamp(%s / 1000), %s)
        ON CONFLICT DO NOTHING
    """, (
        metadata["matchId"],
        info["queueId"],
        info["gameDuration"],
        info["gameStartTimestamp"],
        info["gameVersion"][:5]
    ))

    conn.commit()
    cur.close()
    conn.close()


def insert_player_stats(match, tracked_only=True):
    ensure_dim_player_table()
    ensure_fact_player_match_table()

    match_id = match["metadata"]["matchId"]
    game_duration_min = match["info"]["gameDuration"] / 60

    conn = get_connection()

    try:
        with conn:
            with conn.cursor() as cur:

                for p in match["info"]["participants"]:

                    # FILTRE : ignorer les joueurs hors de la liste
                    if tracked_only and p["puuid"] not in TRACKED_PUUIDS:
                        continue

                    # 1️⃣ UPSERT joueur (DIM)
                    cur.execute("""
                        INSERT INTO riot_dim.dim_player (summoner_name, tag_line, puuid)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (puuid) DO UPDATE
                        SET
                            summoner_name = EXCLUDED.summoner_name,
                            tag_line = EXCLUDED.tag_line
                    """, (
                        p.get("riotIdGameName") or p.get("summonerName"),
                        p.get("riotIdTagline") or "EUW",
                        p["puuid"]
                    ))

                    # 2️⃣ Récupérer player_id
                    cur.execute(
                        "SELECT player_id FROM riot_dim.dim_player WHERE puuid = %s",
                        (p["puuid"],)
                    )
                    row = cur.fetchone()

                    if row is None:
                        continue

                    player_id = row[0]

                    # 3️⃣ Extraire items (slots 0-6)
                    items = [
                        p.get("item0", 0),
                        p.get("item1", 0),
                        p.get("item2", 0),
                        p.get("item3", 0),
                        p.get("item4", 0),
                        p.get("item5", 0),
                        p.get("item6", 0)
                    ]

                    # 4️⃣ INSERT FACT
                    cur.execute("""
                        INSERT INTO riot_fact.fact_player_match (
                            match_id,
                            player_id,
                            champion_id,
                            win,
                            kills,
                            deaths,
                            assists,
                            total_cs,
                            cs_per_min,
                            gold_earned,
                            gold_per_min,
                            damage_to_champions,
                            damage_per_min,
                            role,
                            position,
                            vision_score,
                            game_duration,
                            items
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (match_id, player_id) DO NOTHING
                    """, (
                        match_id,
                        player_id,
                        p["championId"],
                        p["win"],
                        p["kills"],
                        p["deaths"],
                        p["assists"],
                        p["totalMinionsKilled"] + p["neutralMinionsKilled"],
                        (p["totalMinionsKilled"] + p["neutralMinionsKilled"]) / game_duration_min,
                        p["goldEarned"],
                        p["goldEarned"] / game_duration_min,
                        p["totalDamageDealtToChampions"],
                        p["totalDamageDealtToChampions"] / game_duration_min,
                        p["role"],
                        p["teamPosition"],
                        p["visionScore"],
                        match["info"]["gameDuration"],
                        items
                    ))
                    print("ROWCOUNT INSERT FACT:", cur.rowcount)


    finally:
        conn.close()