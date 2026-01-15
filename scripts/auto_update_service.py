"""
Service d'auto-refresh des donnees toutes les 10 minutes.
Lance ce script en arriere-plan et il mettra a jour automatiquement les matchs.
"""

import sys
from pathlib import Path
import time
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats
from config.players import TRACKED_PLAYERS
from db.connection import get_connection

DELAY_API = 0.5  # Delai entre appels API
UPDATE_INTERVAL = 600  # 10 minutes en secondes

def get_existing_match_ids():
    """Recupere tous les match_ids deja en base."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT match_id FROM riot_fact.match_game")
    existing_ids = {row[0] for row in cur.fetchall()}
    cur.close()
    conn.close()
    return existing_ids

def update_once():
    """Execute une mise a jour incrementale."""
    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Debut de la mise a jour...")

    existing_ids = get_existing_match_ids()
    total_nouveaux = 0

    for name, puuid in TRACKED_PLAYERS.items():
        try:
            match_ids = get_match_ids(puuid, count=20)
            nouveaux = 0

            for match_id in match_ids:
                if match_id in existing_ids:
                    continue

                match = get_match_detail(match_id)
                if match is None:
                    continue

                insert_match(match)
                insert_player_stats(match, tracked_only=True)
                existing_ids.add(match_id)
                nouveaux += 1
                total_nouveaux += 1

                time.sleep(DELAY_API)

            if nouveaux > 0:
                print(f"  {name}: {nouveaux} nouveaux matchs")

        except Exception as e:
            print(f"  Erreur sur {name}: {e}")
            continue

    if total_nouveaux > 0:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {total_nouveaux} nouveaux matchs ajoutes")
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Aucun nouveau match")

def run_service():
    """Lance le service d'auto-update en boucle infinie."""
    print("="*70)
    print("SERVICE D'AUTO-UPDATE - DEMARRAGE")
    print("="*70)
    print(f"Intervalle de mise a jour: {UPDATE_INTERVAL // 60} minutes")
    print(f"Joueurs trackés: {len(TRACKED_PLAYERS)}")
    print()
    print("Appuyez sur Ctrl+C pour arreter le service")
    print("="*70)

    iteration = 0

    try:
        while True:
            iteration += 1
            print(f"\n--- Iteration #{iteration} ---")
            update_once()

            next_update = datetime.now().timestamp() + UPDATE_INTERVAL
            next_update_str = datetime.fromtimestamp(next_update).strftime('%H:%M:%S')
            print(f"\nProchaine mise a jour: {next_update_str}")

            time.sleep(UPDATE_INTERVAL)

    except KeyboardInterrupt:
        print("\n\n="*70)
        print("SERVICE ARRETE PAR L'UTILISATEUR")
        print("="*70)
        print(f"Total d'iterations executees: {iteration}")

if __name__ == "__main__":
    run_service()
