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

# Ne pas crash si la cle n'existe pas (permet l'import en prod sans la cle)
# Les fonctions qui l'utilisent retourneront des erreurs appropriees
if not API_KEY:
    print("WARNING: RIOT_API_KEY non trouvee - les appels Riot API echoueront")

HEADERS = {
    "X-Riot-Token": API_KEY or ""
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


# ============================================================
# RECUPERER LE RANG RANKED D'UN JOUEUR
# ============================================================

def get_summoner_by_puuid(puuid: str, region: str = "euw1"):
    """
    Recupere les infos summoner depuis le PUUID
    """
    url = f"https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    return response.json()


def get_ranked_stats(summoner_id: str, region: str = "euw1"):
    """
    Recupere les stats ranked d'un joueur via son summoner ID
    Retourne une liste avec les queues (RANKED_SOLO_5x5, RANKED_FLEX_SR, etc.)
    """
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return []

    return response.json()


def get_ranked_by_puuid(puuid: str, region: str = "euw1"):
    """
    Recupere les stats ranked d'un joueur directement via PUUID
    Endpoint: League v4 by-puuid
    """
    url = f"https://{region}.api.riotgames.com/lol/league/v4/entries/by-puuid/{puuid}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return []

    return response.json()


def get_player_rank(puuid: str, region: str = "euw1"):
    """
    Recupere le rang SoloQ d'un joueur depuis son PUUID
    Retourne: {tier, rank, lp, wins, losses} ou None
    """
    # Utiliser directement League v4 by-puuid
    ranked_entries = get_ranked_by_puuid(puuid, region)

    # Chercher la queue SoloQ
    for entry in ranked_entries:
        if entry.get("queueType") == "RANKED_SOLO_5x5":
            return {
                "tier": entry.get("tier"),
                "rank": entry.get("rank"),
                "lp": entry.get("leaguePoints"),
                "wins": entry.get("wins"),
                "losses": entry.get("losses")
            }

    return None
