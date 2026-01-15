from db.connection import get_connection

print("=== DEBUG COMPLET DE LA BASE ===\n")

conn = get_connection()
cur = conn.cursor()

# 1. Verification de la connexion
print(f"Base de donnees : {conn.info.dbname}")
print(f"Utilisateur : {conn.info.user}")
print(f"Port : {conn.info.port}\n")

# 2. Verifier les schemas
cur.execute("""
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name IN ('riot_dim', 'riot_fact')
    ORDER BY schema_name
""")
schemas = cur.fetchall()
print(f"Schemas disponibles : {[s[0] for s in schemas]}\n")

# 3. Verifier les tables
cur.execute("""
    SELECT table_schema, table_name
    FROM information_schema.tables
    WHERE table_schema IN ('riot_dim', 'riot_fact')
    ORDER BY table_schema, table_name
""")
tables = cur.fetchall()
print("Tables disponibles :")
for t in tables:
    print(f"  - {t[0]}.{t[1]}")
print()

# 4. Compter les lignes dans chaque table
print("Nombre de lignes par table :")

cur.execute("SELECT COUNT(*) FROM riot_dim.dim_player")
count_players = cur.fetchone()[0]
print(f"  - riot_dim.dim_player : {count_players} joueurs")

cur.execute("SELECT COUNT(*) FROM riot_fact.match_game")
count_matches = cur.fetchone()[0]
print(f"  - riot_fact.match_game : {count_matches} matchs")

cur.execute("SELECT COUNT(*) FROM riot_fact.fact_player_match")
count_stats = cur.fetchone()[0]
print(f"  - riot_fact.fact_player_match : {count_stats} stats\n")

# 5. Si fact_player_match a des donnees, afficher un echantillon
if count_stats > 0:
    print("=== ECHANTILLON DE DONNEES ===\n")
    cur.execute("""
        SELECT
            fpm.match_id,
            dp.summoner_name,
            fpm.champion_id,
            fpm.kills,
            fpm.deaths,
            fpm.assists,
            fpm.win
        FROM riot_fact.fact_player_match fpm
        JOIN riot_dim.dim_player dp ON fpm.player_id = dp.player_id
        LIMIT 5
    """)

    rows = cur.fetchall()
    print("Match ID | Joueur | Champion | K/D/A | Win")
    print("-" * 70)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[2]} | {row[3]}/{row[4]}/{row[5]} | {row[6]}")
else:
    print("!!! AUCUNE DONNEE DANS fact_player_match !!!")
    print("\nVerification de match_game :")
    if count_matches > 0:
        cur.execute("SELECT match_id FROM riot_fact.match_game LIMIT 3")
        match_ids = cur.fetchall()
        print(f"Match IDs presents : {[m[0] for m in match_ids]}")

    print("\nVerification de dim_player :")
    if count_players > 0:
        cur.execute("SELECT player_id, summoner_name, puuid FROM riot_dim.dim_player LIMIT 3")
        players = cur.fetchall()
        for p in players:
            print(f"  - Player ID {p[0]} : {p[1]} ({p[2][:20]}...)")

cur.close()
conn.close()

print("\n=== FIN DU DEBUG ===")
