import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# ============================================================
# Chargement du fichier .env (clé API Riot)
# ============================================================

env_path = Path(__file__).resolve().parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("RIOT_API_KEY")

if not API_KEY:
    raise RuntimeError(
        "RIOT_API_KEY non trouvée. Vérifie le fichier config/.env"
    )

HEADERS = {
    "X-Riot-Token": API_KEY
}

# ============================================================
# TEST SIMPLE DE CONNEXION API RIOT (PLATFORM ROUTING)
# ============================================================

def test_riot_api():
    """
    Test de la clé Riot sur un endpoint EUW1 (platform routing)
    """
    url = "https://euw1.api.riotgames.com/lol/status/v4/platform-data"

    response = requests.get(url, headers=HEADERS)

    print("Status code :", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Clé API Riot valide ✅")
        print("Plateforme :", data.get("id"))
    else:
        print("Erreur API Riot ❌")
        print(response.text)

# RECUPERER LES GAMES IDs

def get_match_ids(puuid, count=5):
    """
    Récupère les IDs des derniers matchs d'un joueur (Match v5)
    """
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"

    params = {
        "start": 0,
        "count": count
    }

    response = requests.get(url, headers=HEADERS, params=params)

    print("Status code :", response.status_code)

    if response.status_code != 200:
        print("Erreur récupération match IDs ❌")
        print(response.text)
        return []

    match_ids = response.json()
    return match_ids


# RECUPERER LES DETAILS DE GAME

def get_match_detail(match_id):
    """
    Récupère le détail complet d'un match (Match v5)
    """
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"

    response = requests.get(url, headers=HEADERS)

    print("Status code :", response.status_code)

    if response.status_code != 200:
        print("Erreur récupération match detail ❌")
        print(response.text)
        return None

    return response.json()
