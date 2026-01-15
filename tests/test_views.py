"""
Test des vues SQL analytiques
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_connection

conn = get_connection()
cur = conn.cursor()

print("="*70)
print("TEST DES VUES SQL")
print("="*70)

# Vue 1 : Player stats
print("\n1. PLAYER STATS")
print("-"*70)
cur.execute("SELECT display_name, total_games, winrate_pct, kda_ratio FROM riot_analytics.player_stats LIMIT 5")
for row in cur.fetchall():
    print(f"  {row[0]:<25} {row[1]} games | WR: {row[2]}% | KDA: {row[3]}")

# Vue 2 : Player champions (top 3 par joueur)
print("\n2. PLAYER CHAMPIONS (top 3)")
print("-"*70)
cur.execute("""
    SELECT display_name, champion_name, games_played, winrate_pct
    FROM riot_analytics.player_champions
    WHERE games_played >= 2
    ORDER BY display_name, games_played DESC
    LIMIT 15
""")
for row in cur.fetchall():
    print(f"  {row[0]:<25} {row[1]:<15} {row[2]} games | WR: {row[3]}%")

# Vue 3 : DuoQ synergies
print("\n3. DUOQ SYNERGIES")
print("-"*70)
cur.execute("""
    SELECT player_1_name, player_2_name, games_together, winrate_pct
    FROM riot_analytics.duoq_synergies
    ORDER BY games_together DESC
    LIMIT 10
""")
for row in cur.fetchall():
    print(f"  {row[0]:<25} + {row[1]:<25} | {row[2]} games | WR: {row[3]}%")

# Vue 4 : Ranking
print("\n4. RANKING INTERNE")
print("-"*70)
cur.execute("SELECT rank, display_name, score, winrate_pct, kda_ratio FROM riot_analytics.player_ranking")
for row in cur.fetchall():
    print(f"  #{row[0]} {row[1]:<25} Score: {row[2]} | WR: {row[3]}% | KDA: {row[4]}")

cur.close()
conn.close()

print("\n" + "="*70)
print("TOUTES LES VUES FONCTIONNENT")
print("="*70)
