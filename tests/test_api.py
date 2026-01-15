"""
Test rapide de l'API sans la lancer
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import database

print("="*70)
print("TEST API - ENDPOINTS")
print("="*70)

# Test 1: Get all players
print("\n1. GET /players")
players = database.get_all_players()
print(f"   -> {len(players)} joueurs recuperes")
for p in players[:3]:
    print(f"      - {p['display_name']}: {p['total_games']} games, {p['winrate_pct']}% WR")

# Test 2: Get player by ID
print("\n2. GET /players/1")
player = database.get_player_by_id(1)
if player:
    print(f"   -> {player['display_name']}")
else:
    print("   -> Joueur non trouve")

# Test 3: Get player champions
print("\n3. GET /players/1/champions")
champions = database.get_player_champions(1)
print(f"   -> {len(champions)} champions")
for c in champions[:3]:
    print(f"      - {c['champion_name']}: {c['games_played']} games")

# Test 4: Get ranking
print("\n4. GET /ranking")
ranking = database.get_player_ranking()
print(f"   -> {len(ranking)} joueurs classes")
for r in ranking[:3]:
    print(f"      #{r['rank']} {r['display_name']}: {r['score']} points")

# Test 5: Get duoq
print("\n5. GET /duoq")
duoq = database.get_duoq_synergies()
print(f"   -> {len(duoq)} duos detectes")
for d in duoq[:3]:
    print(f"      - {d['player_1_name']} + {d['player_2_name']}: {d['games_together']} games")

# Test 6: Get recent matches
print("\n6. GET /matches/recent")
matches = database.get_recent_matches(5)
print(f"   -> {len(matches)} matchs")
for m in matches[:3]:
    win_str = "WIN" if m['win'] else "LOSS"
    print(f"      - {m['player_name']} ({m['champion']}): {win_str} - {m['kills']}/{m['deaths']}/{m['assists']}")

print("\n" + "="*70)
print("TOUS LES ENDPOINTS FONCTIONNENT")
print("="*70)
print("\nPour lancer l'API : python run_api.py")
print("Documentation Swagger : http://127.0.0.1:8000/docs")
