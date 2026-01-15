"""
Script de mise a jour incrementale des matchs.
Verifie les nouveaux matchs pour tous les joueurs trackes et les ajoute a la base.
"""

import sys
from pathlib import Path

# Ajouter le repertoire parent au path pour les imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from riot.riot_api import get_match_ids, get_match_detail
from riot.match_ingestion import insert_match, insert_player_stats
from config.players import TRACKED_PLAYERS
from db.connection import get_connection
import time

DELAY_API = 0.5  # Delai entre appels API

def get_existing_match_ids():
    """Recupere tous les match_ids deja en base."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT match_id FROM riot_fact.match_game")
    existing_ids = {row[0] for row in cur.fetchall()}

    cur.close()
    conn.close()

    return existing_ids

def update_all_players():
    """
    Verifie les nouveaux matchs pour chaque joueur et les ajoute.
    Ne traite que les matchs qui ne sont pas encore en base.
    """
    print("="*70)
    print("MISE A JOUR INCREMENTALE - NOUVEAUX MATCHS")
    print("="*70)

    # Recuperer les matchs deja en base
    existing_ids = get_existing_match_ids()
    print(f"Matchs deja en base : {len(existing_ids)}")
    print("="*70 + "\n")

    total_nouveaux_matchs = 0
    total_stats_inserees = 0

    for i, (name, puuid) in enumerate(TRACKED_PLAYERS.items(), 1):
        print(f"\n[{i}/{len(TRACKED_PLAYERS)}] Verification de {name}")
        print("-" * 70)

        try:
            # Recuperer les 20 derniers matchs du joueur
            match_ids = get_match_ids(puuid, count=20)
            print(f"  -> {len(match_ids)} matchs recents trouves")

            nouveaux = 0

            for j, match_id in enumerate(match_ids, 1):
                # Verifier si le match existe deja
                if match_id in existing_ids:
                    continue

                # Nouveau match trouve
                nouveaux += 1

                # Recuperer le detail
                match = get_match_detail(match_id)

                if match is None:
                    print(f"  [{j}/{len(match_ids)}] {match_id} - Erreur API (skip)")
                    continue

                # Insertion
                insert_match(match)
                insert_player_stats(match, tracked_only=True)

                # Ajouter aux existants pour eviter les doublons dans cette session
                existing_ids.add(match_id)

                total_nouveaux_matchs += 1

                # Compter les joueurs trackes dans ce match
                tracked_in_match = sum(
                    1 for p in match["info"]["participants"]
                    if p["puuid"] in TRACKED_PLAYERS.values()
                )
                total_stats_inserees += tracked_in_match

                print(f"  [{j}/{len(match_ids)}] {match_id} - NOUVEAU ({tracked_in_match} joueurs)")

                # Rate limiting
                time.sleep(DELAY_API)

            if nouveaux == 0:
                print(f"  -> Aucun nouveau match pour {name}")

        except Exception as e:
            print(f"  ERREUR sur {name} : {e}")
            continue

    # Resume final
    print("\n" + "="*70)
    print("MISE A JOUR TERMINEE")
    print("="*70)
    print(f"Nouveaux matchs ajoutes : {total_nouveaux_matchs}")
    print(f"Stats inserees : {total_stats_inserees}")
    print("="*70)

if __name__ == "__main__":
    update_all_players()
