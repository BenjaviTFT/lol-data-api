"""
Test de l'API en production (necessite que l'API soit lancee)

Lance d'abord : python run_api.py
Puis execute ce script dans un autre terminal
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("="*70)
print("TEST API LIVE")
print("="*70)
print(f"Base URL : {BASE_URL}\n")

try:
    # Test 1: Root
    print("1. GET /")
    r = requests.get(f"{BASE_URL}/")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {json.dumps(r.json(), indent=2)}\n")

    # Test 2: Health check
    print("2. GET /health")
    r = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {r.status_code}")
    print(f"   Response: {r.json()}\n")

    # Test 3: Players
    print("3. GET /players")
    r = requests.get(f"{BASE_URL}/players")
    print(f"   Status: {r.status_code}")
    players = r.json()
    print(f"   Joueurs: {len(players)}")
    for p in players[:3]:
        print(f"      - {p['display_name']}: {p['winrate_pct']}% WR, KDA {p['kda_ratio']}")
    print()

    # Test 4: Ranking
    print("4. GET /ranking")
    r = requests.get(f"{BASE_URL}/ranking")
    print(f"   Status: {r.status_code}")
    ranking = r.json()
    print(f"   Top 3:")
    for p in ranking[:3]:
        print(f"      #{p['rank']} {p['display_name']}: {p['score']} pts")
    print()

    # Test 5: DuoQ
    print("5. GET /duoq")
    r = requests.get(f"{BASE_URL}/duoq")
    print(f"   Status: {r.status_code}")
    duos = r.json()
    print(f"   Duos: {len(duos)}")
    for d in duos[:3]:
        print(f"      - {d['player_1_name']} + {d['player_2_name']}: {d['winrate_pct']}% WR ({d['games_together']} games)")
    print()

    # Test 6: Stats globales
    print("6. GET /stats/global")
    r = requests.get(f"{BASE_URL}/stats/global")
    print(f"   Status: {r.status_code}")
    stats = r.json()
    print(f"   {json.dumps(stats, indent=2)}\n")

    print("="*70)
    print("TOUS LES TESTS PASSES")
    print("="*70)
    print(f"\nDocumentation Swagger : {BASE_URL}/docs")

except requests.exceptions.ConnectionError:
    print("\n❌ ERREUR : Impossible de se connecter a l'API")
    print("\nLance d'abord l'API avec : python run_api.py")
except Exception as e:
    print(f"\n❌ ERREUR : {e}")
